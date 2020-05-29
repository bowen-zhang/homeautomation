import datetime
import grpc
import time

from absl import flags
from concurrent import futures

from security.components import video
from security.libs import service_lib
from security.proto import security_pb2
from security.proto import security_pb2_grpc
from shared import context_lib
from third_party.common import app

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.protoascii',
                    'Path to config protoascii file.')


class NodeApp(app.App):
  def __init__(self):
    super().__init__(name='node',
                     config_path=FLAGS.config_path,
                     config_proto_cls=security_pb2.Config)
    self.init_logging(log_path='/tmp')

    self._context = context_lib.Context(config=self.config)

    self._security_service = self._context.create_grpc_service_stub(
        security_pb2_grpc.SecurityServiceStub,
        self._context.config.security_service)

  def run(self):
    video.VideoCapturer(self._context, self._security_service).run()

if __name__ == '__main__':
  app.start(NodeApp)