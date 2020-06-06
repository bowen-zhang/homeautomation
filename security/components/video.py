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


class _VideoProxy(pattern.Logger):
  """Middleman to deal recorded frames from Pi camera to uploader."""
  _MAX_READ_BLOCK_SEC = 1
  _MAX_WRITE_BLOCK_SEC = 5

  def __init__(self, max_cache_frames, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._max_cache_frames = max_cache_frames
    self._frame_queue = None

  @property
  def is_stopped(self):
    return self._frame_queue is None

  def start(self):
    self._frame_queue = queue.Queue(maxsize=self._max_cache_frames)

  def stop(self):
    self._frame_queue = None

  def read(self):
    frame_queue = self._frame_queue
    if not frame_queue:
      raise StreamingException("Streaming has been aborted.")

    try:
      return frame_queue.get(timeout=self._MAX_READ_BLOCK_SEC)
    except:
      raise StreamingException("Timed out while waiting for recording.")

  def write(self, data, split):
    """Writes a frame.

    Args:
      data: frame.
      split: weather this is beginning of a new file.
    """
    frame_queue = self._frame_queue
    if not frame_queue:
      return

    if split:
      self.logger.info('Recording is splitted.')

    request = security_pb2.StreamVideoRequest()
    request.timestamp.FromDatetime(datetime.datetime.now())
    request.image = data
    request.split = split

    if frame_queue.full():
      self.logger.warn("Video streaming is slower than capturing.")

    try:
      frame_queue.put(request, timeout=self._MAX_WRITE_BLOCK_SEC)
    except queue.Full:
      self.logger.error(
          "Timed out while waiting for video streaming to catch up.")
      self.stop()


class _MemoryStream(object):
  """File-like interface for Pi camera to write frame to middleman.

  This additional layer is necessary, as when splitting recordings, a new
  _MemoryStream is used (to detect split point and notify video receiver)
  but underneath middleman remains the same (so it is easy to manage lifecycle).
  """
  def __init__(self, video_proxy):
    self._proxy = video_proxy
    self._first = True

  def write(self, data):
    self._proxy.write(data, split=self._first)
    self._first = False


class VideoCapturer(pattern.Worker):
  MAX_QUEUE_LENGTH_SEC = 3

  def __init__(self, context, config, *args, **kwargs):
    super().__init__(interval=datetime.timedelta(
        seconds=5), clock=context.clock, *args, **kwargs)
    self._context = context
    self._config = config
    self._proxy = None
    self._camera = None

  def _on_start(self):
    self._proxy = _VideoProxy(
        max_cache_frames=self._config.framerate * self.MAX_QUEUE_LENGTH_SEC)
    self._camera = picamera.PiCamera(framerate=self._config.framerate,
                                     resolution=(self._config.width, self._config.height))
    self._camera.start_recording(_MemoryStream(self._proxy),
                                 format='h264',
                                 quality=self._config.quality)

  def _on_run(self):
    self.logger.info('Starting streaming...')

    splitted = False
    self._proxy.start()

    try:
      for response in self._context.security_service.StreamVideo(self._stream_frames()):
        if not splitted and response.split:
          self.logger.info("Splitting recording per server request...")
          self._camera.split_recording(_MemoryStream(self._proxy))
        splitted = response.split
    finally:
      self._proxy.stop()
      self.logger.info('Streaming stopped.')

  def _stream_frames(self):
    while True:
      request = self._proxy.read()
      request.node_id = self._context.id
      yield request
