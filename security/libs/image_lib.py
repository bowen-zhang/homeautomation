import cv2
import datetime
import flask

from third_party.common import pattern


class ImageServer(pattern.Logger):
  def __init__(self, context, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._context = context
    self._context.web.add_url_rule(
        '/video/<node_id>', view_func=self._on_video)
    self._frame_caches = {}

  def register_frame_cache(self, node_id, cache):
    self._frame_caches[node_id] = cache
    self.logger.info('Registered node {0}.'.format(node_id))

  def unregister_frame_cache(self, node_id):
    del self._frame_caches[node_id]
    self.logger.info('Unregistered node {0}.'.format(node_id))

  def _on_video(self, node_id):
    print(self._frame_caches)
    frame_cache = self._frame_caches.get(node_id, None)
    if not frame_cache:
      self.logger.warn(
          'Frame cache not available for node {0}.'.format(node_id))
      flask.abort(404)

    return flask.Response(
        self._stream_video(frame_cache),
        mimetype='multipart/x-mixed-replace; boundary=frame')

  def _stream_video(self, frame_cache):
    timestamp = datetime.datetime.min
    while True:
      timestamp, frame = frame_cache.next(timestamp)
      if frame is None:
        break
      _, image = cv2.imencode(".jpg", frame)
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + image.tobytes() + b'\r\n')
