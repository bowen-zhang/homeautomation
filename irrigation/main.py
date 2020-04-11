import datetime
import grpc
import time

from absl import flags
from concurrent import futures
from google.protobuf import text_format

from third_party.common import app
from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc
from irrigation.libs import controller as controller_lib
from irrigation.libs import model as model_lib
from irrigation.libs import service as service_lib
from irrigation.libs import test as test_lib

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.protoascii',
                    'Path to config protoascii file.')
flags.DEFINE_boolean('dry_run', False,
                     'Simulates irrigation run without watering.')


class Clock(object):
  def now(self):
    return datetime.datetime.now()

  def sleep(self, seconds):
    time.sleep(seconds)


class IrrigationApp(app.App):
  def __init__(self):
    super().__init__(name='irrigation', config_path=FLAGS.config_path,
                     config_proto_cls=irrigation_pb2.Config)

    if FLAGS.dry_run:
      print('Running in simulation mode.')
      self._clock = test_lib.FakeClock()
    else:
      self._clock = Clock()

    stations = [self._create_station(x) for x in self.config.stations]
    self._model = model_lib.ManualModel()
    self._task_manager = controller_lib.TaskManager(stations)

  def _create_station(self, proto):
    if FLAGS.dry_run:
      return controller_lib.Station(proto, self._clock, gpio_module=test_lib.FakeGPIO())
    else:
      from RPi import GPIO
      return controller_lib.Station(proto, self._clock, gpio_module=GPIO)

  def run(self):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = service_lib.IrrigationService(
        config_proto=self.config, task_manager=self._task_manager)
    irrigation_pb2_grpc.add_IrrigationServiceServicer_to_server(
        service, server)
    server.add_insecure_port('[::]:17051')
    server.start()

    self._task_manager.start()
    print('Running...')
    while True:
      time.sleep(1)

    # now = self._clock.now()
    # next_time = datetime.datetime(now.year, now.month, now.day,
    #                               self.config.schedule_hour, 0, 0)
    # if next_time < now:
    #   next_time += datetime.timedelta(days=1)
    # print('Current time: {0}, next run at {1} (after {2})'.format(
    #     now, next_time, next_time - now))

    # while True:
    #   if next_time < self._clock.now():
    #     self._model.run(self._stations)
    #     self._save_config()
    #     next_time += datetime.timedelta(days=1)
    #     print('Next run at {0}'.format(next_time))
    #   self._clock.sleep(60)

  def _save_config(self):
    with open(self._config_path, 'w') as f:
      f.write(text_format.MessageToString(self.config))
    print('Saved config.')


if __name__ == '__main__':
  app.start(IrrigationApp)
