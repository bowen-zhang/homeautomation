import pymongo
import time

from absl import flags
from concurrent import futures

from irrigation.proto import irrigation_pb2
from irrigation.libs import core_lib
from irrigation.libs import mock_lib
from irrigation.libs import monitor_lib
from third_party.common import app

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.protoascii',
                    'Path to config protoascii file.')
flags.DEFINE_boolean('dry_run', False,
                     'Simulates irrigation run without watering.')


class MonitorApp(app.App):
  def __init__(self):
    super().__init__(name='monitor', config_path=FLAGS.config_path,
                     config_proto_cls=irrigation_pb2.Config)
    self.init_logging(log_path='/tmp')

    self._context = core_lib.Context(
        config=self.config,
        livemode=not FLAGS.dry_run,
    )
    if FLAGS.dry_run:
      mock_lib.init_test_db(self._context)

    self._components = [
        monitor_lib.IrrigationMonitor(self._context),
        monitor_lib.EvaporationMonitor(self._context),
        monitor_lib.RainMonitor(
            self._context),
        monitor_lib.WaterLevelChangeMonitor(self._context),
        monitor_lib.WaterLevelMonitor(self._context),
    ]

  def run(self):
    try:
      self.logger.info('Starting components...')
      for component in self._components:
        component.start()
      self.logger.info('Started all components.')

      self.logger.info('Running...')
      while True:
        if FLAGS.dry_run:
          self._dump()
        time.sleep(1)
    finally:
      self.logger.info('Stopping components...')
      for component in self._components:
        component.stop()
      self.logger.info('Stopped all components.')

  def _dump(self):
    now = self._context.clock.now()
    water_levels = []
    for zone_id in self._context.zone_ids:
      water_level = self._context.storage.water_levels.find_one(
          filter={'zone_id': zone_id},
          sort=[('timeslot', pymongo.DESCENDING)],
          limit=1,
      )
      if water_level:
        water_levels.append(water_level)

    print('{0}: {1}'.format(
        now,
        ','.join(['#{0}={1:.1f}'.format(x.zone_id, x.current_amount_mm)
                  for x in water_levels]),
    ))


if __name__ == '__main__':
  app.start(MonitorApp)
