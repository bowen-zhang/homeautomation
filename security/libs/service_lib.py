import datetime
import flask
import os
import time

from security.libs import image_lib
from security.libs import video_lib
from security.proto import security_pb2
from security.proto import security_pb2_grpc
from third_party.common import pattern


class SecurityService(security_pb2_grpc.SecurityServiceServicer, pattern.Logger):
  def __init__(self, context, image_server, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._context = context
    self._image_server = image_server

  def RegisterNode(self, request, context):
    node_proto = self._context.storage.nodes.find_one(filter={
        'id': request.node_id
    })
    return security_pb2.RegisterNodeResponse(node=node_proto)

  def StreamVideo(self, request_iterator, context):
    initialized = False
    node_id = None
    processors = []
    try:
      for request in request_iterator:
        if not initialized:
          initialized = True
          node_id = request.node_id
          processors = self._create_processors(
              node_id=node_id, spec=request.spec)
          self.logger.info('Start to stream video from {0}...'.format(node_id))
        else:
          for processor in processors:
            processor.process(request.timestamp.ToDatetime(), request.image)

        yield security_pb2.StreamVideoResponse()

    finally:
      self.logger.info('Stopping streaming video from {0}...'.format(node_id))
      for processor in processors:
        processor.close()
      self._image_server.unregister_frame_cache(node_id)
      self.logger.info('Stopped streaming video from {0}.'.format(node_id))

  def _create_processors(self, node_id, spec):
    dirpath = os.path.join(
        self._context.config.server.video_archive_location, node_id)

    frame_cache = video_lib.LatestFrameCache()
    self._image_server.register_frame_cache(node_id, frame_cache)

    return [
        video_lib.H264Decoder(video_spec=spec, downstreams=[
            video_lib.Mp4Writer(video_spec=spec, output_dir=dirpath, max_record_duration=datetime.timedelta(
                seconds=self._context.config.server.max_record_duration_sec), clock=self._context.clock),
            frame_cache,
        ])
    ]
