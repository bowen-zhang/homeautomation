import datetime
import threading

from security.proto import security_pb2
from third_party.common import pattern
from third_party.hal import camera

class VideoCapturer(pattern.Logger):
  def __init__(self, context, security_service, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._context = context
    self._security_service = security_service
    self._ready = threading.Condition()
    self._camera = camera.Camera()
    self._streamer = camera.Streamer(web=None, camera=self._camera, frame_rate=10)

  def run(self):
    self._streamer.start()
    
    for response in self._security_service.StreamVideo(self._capture_video()):
      with self._ready:
        self._ready.notify()

  def _capture_video(self):
    while True:
      request = security_pb2.StreamVideoRequest()
      request.timestamp.FromDatetime(datetime.datetime.now())
      request.image = self._streamer.frame(0)
      yield request

      with self._ready:
        self._ready.wait()
