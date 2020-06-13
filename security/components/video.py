import datetime
import io
import picamera
import queue
import threading
import time

from security.proto import security_pb2
from third_party.common import pattern
from third_party.hal import camera


class StreamingException(Exception):
  pass


class _StreamProxy(pattern.Logger):
  """Middleman to deal recorded frames from Pi camera to uploader."""
  _MAX_READ_BLOCK_SEC = 1
  _MAX_WRITE_BLOCK_SEC = 5

  def __init__(self, max_cache_frames, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._max_cache_frames = max_cache_frames
    self._frame_queue = queue.Queue(maxsize=self._max_cache_frames)

  @property
  def closed(self):
    return self._frame_queue is None

  def close(self):
    self._frame_queue = None

  def read(self):
    frame_queue = self._frame_queue
    if not frame_queue:
      raise StreamingException("Streaming has been aborted.")

    try:
      return frame_queue.get(timeout=self._MAX_READ_BLOCK_SEC)
    except:
      raise StreamingException("Timed out while waiting for recording.")

  def write(self, data):
    frame_queue = self._frame_queue
    if not frame_queue:
      return

    request = security_pb2.StreamVideoRequest()
    request.timestamp.FromDatetime(datetime.datetime.now())
    request.image = data

    if frame_queue.full():
      self.logger.warn("Video streaming is slower than capturing.")

    try:
      frame_queue.put(request, timeout=self._MAX_WRITE_BLOCK_SEC)
    except queue.Full:
      self.logger.error(
          "Timed out while waiting for video streaming to catch up.")
      self.stop()


class VideoCapturer(pattern.Worker):
  _MAX_QUEUE_LENGTH_SEC = 3
  _MAX_STREAMING_DELAY_SEC = 5

  def __init__(self, context, config, *args, **kwargs):
    super().__init__(interval=datetime.timedelta(
        seconds=5), clock=context.clock, *args, **kwargs)
    self._context = context
    self._config = config
    self._proxy = None
    self._camera = None
    self._ready = threading.Event()

  def _on_start(self):
    self._camera = picamera.PiCamera(framerate=self._config.framerate,
                                     resolution=(self._config.width, self._config.height))
    self._camera.annotate_text_size = 20
    self._camera.annotate_background = picamera.color.Color('#000000')
    threading.Thread(target=self._update_annotation, daemon=True).start()

  def _on_run(self):
    self.logger.info('Starting streaming...')

    self._proxy = _StreamProxy(
        max_cache_frames=self._config.framerate * self._MAX_QUEUE_LENGTH_SEC)

    try:
      for _ in self._context.security_service.StreamVideo(self._stream_frames()):
        self._ready.set()
    finally:
      self._proxy.close()
      self.logger.info('Streaming stopped.')

  def _update_annotation(self):
    while True:
      now = self._context.clock.now()
      self._camera.annotate_text = '{0} - {1: %b %d, %Y - %H:%M:%S}'.format(
          self._context.name, now)
      time.sleep(1)

  def _stream_frames(self):
    yield security_pb2.StreamVideoRequest(
        node_id=self._context.id,
        spec=security_pb2.VideoSpec(
            width=self._config.width,
            height=self._config.height,
            framerate=self._config.framerate
        )
    )

    if not self._ready.wait(timeout=5):
      raise StreamingException(
          "Timed out while waiting for server to respond to initial streaming request.")

    self._camera.start_recording(self._proxy,
                                 format='h264',
                                 quality=self._config.quality)
    try:
      while True:
        self._ready.clear()

        request = self._proxy.read()
        request.node_id = self._context.id
        yield request

        if not self._ready.wait(timeout=self._MAX_STREAMING_DELAY_SEC):
          raise StreamingException(
              "Timed out while waiting for server to respond to streaming request.")
    finally:
      self._camera.stop_recording()
