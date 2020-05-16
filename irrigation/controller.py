import grpc
import time

from absl import flags
from concurrent import futures

from third_party.common import app
from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc
from irrigation.libs import core_lib
from irrigation.libs import controller_lib
from irrigation.libs import mock_lib

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.protoascii',
                    'Path to config protoascii file.')
flags.DEFINE_boolean('dry_run', False,
                     'Simulates irrigation run without watering.')


class ControllerApp(app.App):
  def __init__(self):
    super().__init__(name='controller',
                     config_path=FLAGS.config_path,
                     config_proto_cls=irrigation_pb2.Config)
    self.init_logging(log_path='/tmp')

    self._context = core_lib.Context(config=self.config,
                                     livemode=not FLAGS.dry_run)
    if FLAGS.dry_run:
      mock_lib.init_test_db(self._context)

    self._controller = controller_lib.Controller(self._context)
    self._controller_service = controller_lib.ControllerService(
        self._controller)

  def run(self):
    self._controller.start()

    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    irrigation_pb2_grpc.add_ControllerServiceServicer_to_server(
        self._controller_service, grpc_server)
    port = self._context.config.controller_service.port
    grpc_server.add_insecure_port('[::]:{0}'.format(port))
    grpc_server.start()
    self.logger.info('Started GRPC service on port {0}.'.format(port))

    self.logger.info('Running...')
    try:
      while True:
        time.sleep(1)
    finally:
      self._controller.stop()

if __name__ == '__main__':
  app.start(ControllerApp)
