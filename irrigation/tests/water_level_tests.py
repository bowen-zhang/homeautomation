import datetime
import logging
import mongomock
import random
import retrying
import unittest
from google.protobuf import text_format

from shared import topics
from irrigation.libs import core_lib
from irrigation.libs import storage_lib
from irrigation.libs import water_level_lib
from irrigation.proto import irrigation_pb2
from third_party.common import time_util

_test_config = text_format.Parse(
    """
  zones {
    id: 1
    name: "Test Zone"
    pin: 123
    flow_rate_mmpm: 1.5
    max_water_amount_mm: 15
    evaporation_rate_mmpm: 0.002
  }
  kafka {
    host: 'localhost'
    port: 9092
  }
  """, irrigation_pb2.Config()
)

# logger = logging.getLogger('')
# logger.setLevel(logging.INFO)
# logger.addHandler(logging.StreamHandler())


class EventTestBase(unittest.TestCase):
  def _assert_event(self, consumer, expected_event):
    message_groups = consumer.poll(timeout_ms=5000)
    self.assertEqual(len(message_groups), 1)
    messages = list(message_groups.values())[0]
    self.assertEqual(len(messages), 1)
    actual_event = messages[0].value
    self.assertEqual(text_format.MessageToString(actual_event),
                     text_format.MessageToString(expected_event))


class IrrigationMonitorTests(EventTestBase):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._context = None
    self._consumer_under_test = None

  def setUp(self):
    self._context = core_lib.Context(config=_test_config, livemode=False)
    self._water_level_change_consumer = self._context.create_event_consumer(
        topics.Irrigation.WATER_LEVEL_CHANGE_TOPIC)
    self._consumer_under_test = water_level_lib.IrrigationMonitor(
        self._context)
    self._consumer_under_test.start()

  def tearDown(self):
    if self._consumer_under_test:
      self._consumer_under_test.stop()
      self._consumer_under_test = None
    if self._water_level_change_consumer:
      self._water_level_change_consumer.close()
      self._water_level_change_consumer = None

  def test_zone_on_off(self):
    # Turn on irrigation
    event = irrigation_pb2.ZoneEvent(
        zone_id=1,
        action=irrigation_pb2.ZoneEvent.Action.ON,
    )
    event.timestamp.FromDatetime(datetime.datetime(2020, 1, 1, 5, 0, 0))
    self._context.send_event(topics.Irrigation.ZONE_TOPIC, event)

    # Turn off irrigation
    event = irrigation_pb2.ZoneEvent(
        zone_id=1,
        action=irrigation_pb2.ZoneEvent.Action.OFF,
    )
    event.timestamp.FromDatetime(datetime.datetime(2020, 1, 1, 5, 10, 0))
    self._context.send_event(topics.Irrigation.ZONE_TOPIC, event)

    event = irrigation_pb2.WaterLevelChangeEvent(
        zone_id=1,
        change_amount_mm=1.5*10,
    )
    event.timestamp.FromDatetime(datetime.datetime(2020, 1, 1, 5, 10, 0))
    self._assert_event(self._water_level_change_consumer, event)


class EvaporationMonitorTests(EventTestBase):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._clock = None
    self._context = None
    self.updater = None

  def setUp(self):
    self._clock = time_util.TestClock(datetime.datetime(2020, 1, 1, 5, 0, 0))
    self._context = core_lib.Context(
        config=_test_config, livemode=False, clock=self._clock)
    self._water_level_change_consumer = self._context.create_event_consumer(
        topics.Irrigation.WATER_LEVEL_CHANGE_TOPIC)
    self._updater = water_level_lib.EvaporationMonitor(
        self._context)
    self._updater.start()

  def tearDown(self):
    if self._updater:
      self._updater.stop()
      self._updater = None
    if self._water_level_change_consumer:
      self._water_level_change_consumer.close()
      self._water_level_change_consumer = None

  def test_water_level_change(self):
    start_time = datetime.datetime(2020, 1, 1, 5, 0, 0)
    for i in range(24):
      self._clock.set_time(start_time + datetime.timedelta(hours=i+1))
      event = irrigation_pb2.WaterLevelChangeEvent(
          zone_id=1,
          change_amount_mm=-0.12,
      )
      event.timestamp.FromDatetime(start_time + datetime.timedelta(hours=i+1))
      self._assert_event(self._water_level_change_consumer, event)


class WaterLevelChangeMonitorTests(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._clock = None
    self._context = None
    self._water_level_archiver = None

  def setUp(self):
    self._clock = time_util.TestClock(datetime.datetime(2020, 1, 1, 5, 0, 0))
    self._mongo_client = mongomock.MongoClient()
    self._context = core_lib.Context(
        config=_test_config,
        livemode=False,
        clock=self._clock,
        storage=storage_lib.MongoStorage(database_name='test', client=self._mongo_client))
    self._water_level_archiver = water_level_lib.WaterLevelChangeMonitor(
        self._context)
    self._water_level_archiver.start()

  def tearDown(self):
    if self._water_level_archiver:
      self._water_level_archiver.stop()
      self._water_level_archiver = None

  def test_initial_update_to_latest_timeslot(self):
    event = irrigation_pb2.WaterLevelChangeEvent(
        zone_id=1,
        change_amount_mm=random.random(),
    )
    event.timestamp.FromDatetime(datetime.datetime(2020, 1, 1, 5, 30, 0))
    self._context.send_event(
        topics.Irrigation.WATER_LEVEL_CHANGE_TOPIC, event)

    water_level = irrigation_pb2.WaterLevel(
        zone_id=1,
        change_amount_mm=event.change_amount_mm,
        current_amount_mm=event.change_amount_mm)
    water_level.timeslot.FromDatetime(datetime.datetime(2020, 1, 1, 5, 0, 0))

    self._assert_mongo_collection(
        self._context.storage.water_levels, [water_level])

  def test_update_to_latest_timeslot(self):
    start_time = self._clock.now()
    self._add_water_level(start_time, 1, 10, 10)
    self._clock.set_time(start_time + datetime.timedelta(minutes=30))
    self._send_water_level_change_event(self._clock.now(), 1, -1)
    self._assert_mongo_collection(
        self._context.storage.water_levels,
        [
            self._create_water_level(start_time, 1, 9, 9)
        ]
    )

  def test_update_to_past_timeslot(self):
    start_time = self._clock.now()
    one_hour = datetime.timedelta(hours=1)
    self._add_water_level(start_time, 1, -1, 3)
    self._add_water_level(start_time + one_hour, 1, -1, 2)
    self._add_water_level(start_time + one_hour * 2, 1, -1, 1)
    self._add_water_level(start_time + one_hour * 3, 1, -1, 0)
    self._add_water_level(start_time + one_hour * 4, 1, -1, 0)

    self._clock.set_time(start_time + one_hour * 4 +
                         datetime.timedelta(minutes=30))
    self._send_water_level_change_event(
        datetime.datetime(2020, 1, 1, 7, 30, 0), 1, 3)

    self._assert_mongo_collection(
        self._context.storage.water_levels,
        [
            self._create_water_level(start_time + one_hour * 0, 1, -1, 3),
            self._create_water_level(start_time + one_hour * 1, 1, -1, 2),
            self._create_water_level(start_time + one_hour * 2, 1, 2, 4),
            self._create_water_level(start_time + one_hour * 3, 1, -1, 3),
            self._create_water_level(start_time + one_hour * 4, 1, -1, 2),
        ]
    )

  def test_update_to_missing_timeslot(self):
    start_time = self._clock.now()
    one_hour = datetime.timedelta(hours=1)
    self._add_water_level(start_time, 1, -1, 3)
    self._add_water_level(start_time + one_hour, 1, -1, 2)

    self._clock.set_time(start_time + one_hour * 4 +
                         datetime.timedelta(minutes=30))
    self._send_water_level_change_event(
        start_time + datetime.timedelta(hours=2, minutes=30), 1, 3)

    self._assert_mongo_collection(
        self._context.storage.water_levels,
        [
            self._create_water_level(start_time + one_hour * 0, 1, -1, 3),
            self._create_water_level(start_time + one_hour * 1, 1, -1, 2),
            self._create_water_level(start_time + one_hour * 2, 1, 3, 5),
            self._create_water_level(start_time + one_hour * 4, 1, 0, 5),
        ]
    )

  def _create_water_level(self, timeslot, zone_id, change_amount_mm, current_amount_mm):
    water_level = irrigation_pb2.WaterLevel(
        zone_id=zone_id,
        change_amount_mm=change_amount_mm,
        current_amount_mm=current_amount_mm)
    water_level.timeslot.FromDatetime(timeslot)
    return water_level

  def _add_water_level(self, timeslot, zone_id, change_amount_mm, current_amount_mm):
    water_level = self._create_water_level(
        timeslot, zone_id, change_amount_mm, current_amount_mm)
    self._context.storage.water_levels.save(water_level)

  def _send_water_level_change_event(self, timestamp, zone_id, change_amount_mm):
    event = irrigation_pb2.WaterLevelChangeEvent(
        zone_id=zone_id,
        change_amount_mm=change_amount_mm,
    )
    event.timestamp.FromDatetime(timestamp)
    self._context.send_event(topics.Irrigation.WATER_LEVEL_CHANGE_TOPIC, event)

  def _assert_mongo_collection(self, collection, protos):
    try:
      self._assert_mongo_collection_internal(collection, protos)
    except:
      print('Expected:\n{0}'.format(protos))
      print('Actual:\n{0}'.format(list(collection.find())))
      raise

  @retrying.retry(stop_max_delay=5000, wait_fixed=300, retry_on_exception=lambda x: True)
  def _assert_mongo_collection_internal(self, collection, protos):
    actual_protos = list(collection.find())
    self.assertListEqual(actual_protos, protos)


if __name__ == '__main__':
  unittest.main()
