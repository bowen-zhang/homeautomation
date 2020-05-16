import grpc
import time

from absl import flags
from concurrent import futures

from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc
from irrigation.libs import core_lib
from irrigation.libs import service_lib
from irrigation.libs import task_manager_lib
from third_party.common import app

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.protoascii',
                    'Path to config protoascii file.')
flags.DEFINE_boolean('dry_run', False,
                     'Simulates irrigation run without watering.')


class FrontendApp(app.App):
  def __init__(self):
    super().__init__(name='irrigation-frontend', config_path=FLAGS.config_path,
                     config_proto_cls=irrigation_pb2.Config)
    self.init_logging(log_path='/tmp')

    self._context = core_lib.Context(
        config=self.config,
        livemode=not FLAGS.dry_run,
    )

  def run(self):
    task_manager = task_manager_lib.TaskManager(self._context)
    task_manager.start()

    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    irrigation_pb2_grpc.add_IrrigationServiceServicer_to_server(
        service_lib.IrrigationService(
            context=self._context, task_manager=task_manager),
        grpc_server)

    port = self._context.config.irrigation_service.port
    grpc_server.add_insecure_port('[::]:{0}'.format(port))
    grpc_server.start()
    self.logger.info('Started GRPC service on port {0}.'.format(port))

    try:
      self.logger.info('Running...')
      while True:
        time.sleep(1)
    finally:
      task_manager.stop()


if __name__ == '__main__':
  app.start(FrontendApp)
