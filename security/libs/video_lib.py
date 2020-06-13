import collections
import cv2
import datetime
import numpy as np
import queue
import os
import threading

from security.libs import video_utils
from third_party.common import pattern


class VideoProcessor(pattern.Logger, pattern.Closable):
  def __init__(self, downstreams=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._downstreams = downstreams or []

  def close(self):
    pass

  def process(self, timestamp, frame):
    output_frame = self._on_process(timestamp, frame)
    if output_frame:
      self.to_downstream(timestamp, output_frame)

  def to_downstream(self, timestamp, frame):
    for downstream in self._downstreams:
      downstream.process(timestamp, frame)

  def _on_process(self, timestamp, frame):
    return frame


class H264Decoder(VideoProcessor):
  """Decodes H264 frames to raw (bgr24) frames."""

  _TIMESTAMP_QUEUE_MAX_DURATION_SEC = 30

  def __init__(self, video_spec, downstreams=None, *args, **kwargs):
    super().__init__(downstreams=downstreams, *args, **kwargs)
    self._video_spec = video_spec
    self._timestamp_queue = queue.Queue(
        maxsize=self._TIMESTAMP_QUEUE_MAX_DURATION_SEC * self._video_spec.framerate)

    self._ffmpeg = video_utils.Ffmpeg()
    self._ffmpeg.from_reader(None, container='h264', vcodec='h264')
    self._ffmpeg.map('0:v')
    self._ffmpeg.to_writer(self._write, container='rawvideo',
                           vcodec='rawvideo', pixel_format='bgr24')
    self._ffmpeg.start()

  def close(self):
    self._ffmpeg.stop()

  def _on_process(self, timestamp, frame):
    self._timestamp_queue.put(timestamp)
    self._ffmpeg.send_input(frame)
    return None

  def _write(self, pipe):
    data = pipe.read(self._video_spec.width * self._video_spec.height * 3)
    if not data:
      return False

    timestamp = self._timestamp_queue.get()
    frame = np.frombuffer(data, dtype="uint8")
    frame = frame.reshape((self._video_spec.height, self._video_spec.width, 3))
    self.to_downstream(timestamp, frame)
    return True


class Mp4Writer(VideoProcessor):
  """Encodes raw (bgr24) frames to H264 with MPEG4 container and writes to file."""

  def __init__(self, video_spec, output_dir, max_record_duration, clock, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._video_spec = video_spec
    self._output_dir = output_dir
    self._max_record_duration = max_record_duration
    self._clock = clock

    self._output = None
    self._start_time = None
    self._next_split_time = datetime.datetime.max
    self._ffmpeg = None

    if not os.path.exists(self._output_dir):
      os.makedirs(self._output_dir)

  def _on_process(self, timestamp, frame):
    if self._clock.now() > self._next_split_time:
      self.close()
    if not self._ffmpeg:
      self._new_output(self._get_output_filepath(timestamp))

    self._ffmpeg.send_input(frame)
    return None

  def close(self):
    if self._ffmpeg:
      self._ffmpeg.stop()
      self._ffmpeg = None
      self.logger.info('Stopped writing video.')

  def _get_output_filepath(self, timestamp):
    return os.path.join(self._output_dir,
                        '{0:%Y%m%d-%H%M%S}.mkv'.format(timestamp))

  def _new_output(self, filepath):
    self.logger.info('Writing video to {0}...'.format(filepath))
    self._start_time = self._clock.now()
    self._next_split_time = self._start_time + self._max_record_duration

    self._ffmpeg = video_utils.Ffmpeg()
    self._ffmpeg.from_reader(None, container='rawvideo', vcodec='rawvideo', framerate=self._video_spec.framerate, size=(
        self._video_spec.width, self._video_spec.height), pixel_format='bgr24')
    self._ffmpeg.to_file(filepath, container='mp4', vcodec='h264')
    self._ffmpeg.start()


class LatestFrameCache(VideoProcessor):
  _Snippet = collections.namedtuple('Snippet', ['timestamp', 'data'])

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._frame = self._Snippet(data=None, timestamp=datetime.datetime.min)
    self._trigger = threading.Condition()
    self._abort = False

  def _on_process(self, timestamp, frame):
    self._frame = self._Snippet(timestamp=timestamp, data=frame)
    with self._trigger:
      self._trigger.notify_all()
    return None

  def close(self):
    with self._trigger:
      self._abort = True
      self._trigger.notify_all()

  def get(self):
    frame = self._frame
    return (frame.timestamp, frame.data)

  def next(self, last_timestamp):
    frame = self._frame
    while not self._abort and last_timestamp >= frame.timestamp:
      with self._trigger:
        self._trigger.wait()
        frame = self._frame

    if self._abort:
      return (None, None)
    else:
      return (frame.timestamp, frame.data)
