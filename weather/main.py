import grpc
import time
from absl import flags
from concurrent import futures

from proto import weather_pb2
from shared import context_lib
from third_party.common import app
from weather.libs import downloader_lib
from weather.libs import service_lib
from weather.libs import storage_lib
from weather.proto import weather_pb2_grpc

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.protoascii',
                    'Path to config protoascii file.')


class WeatherApp(app.App):
  def __init__(self):
    super().__init__(name='weather',
                     config_path=FLAGS.config_path,
                     config_proto_cls=weather_pb2.Config)
    self.init_logging(log_path='/tmp')

    self._context = context_lib.Context(config=self.config,
                                        kafka_endpoint=self.config.kafka,
                                        storage=storage_lib.MongoStorage(database_name='weather'))
    self._downloader = downloader_lib.WeatherDownloader(self._context)
    self._weather_service = service_lib.WeatherService(self._context)

  def run(self):
    self._downloader.start()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(
        self._weather_service, grpc_server)
    port = self._context.config.weather_service_port
    grpc_server.add_insecure_port('[::]:{0}'.format(port))
    grpc_server.start()
    self.logger.info('Started GRPC service on port {0}.'.format(port))

    self.logger.info('Running...')

    while True:
      time.sleep(1)


if __name__ == '__main__':
  app.start(WeatherApp)
