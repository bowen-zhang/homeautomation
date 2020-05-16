import datetime
import pymongo
import time
from google.protobuf import empty_pb2

from shared import topics
from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc
from third_party.common import kafka_util
from third_party.common import pattern


def _timestamp_to_timeslot(timestamp):
  return datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, 0, 0)


def _get_previous_timeslot(timeslot):
  return timeslot - datetime.timedelta(hours=1)


def _get_next_timeslot(timeslot):
  return timeslot + datetime.timedelta(hours=1)


class IrrigationMonitor(kafka_util.EventConsumer):
  def __init__(self, context, *args, **kwargs):
    super().__init__(kafka_consumer_builder=context.create_event_consumer,
                     topic=topics.Irrigation.ZONE_TOPIC,
                     group='IrrigationMonitor', *args, **kwargs)
    self._context = context
    self._last_zone_event = None

  def _on_event(self, zone_event):
    if zone_event.action == irrigation_pb2.ZoneEvent.Action.ON:
      self._last_zone_event = zone_event
    elif zone_event.action == irrigation_pb2.ZoneEvent.Action.OFF:
      self._on_zone_stopped(zone_event)
      self._last_zone_event = None

  def _on_zone_stopped(self, zone_event):
    if not self._last_zone_event:
      raise kafka_util.EventConsumerException(
          'Missing zone event when started.')

    if self._last_zone_event.zone_id != zone_event.zone_id:
      raise kafka_util.EventConsumerException(
          'Mismatch zone id for start and stop events.')

    if self._last_zone_event.action != irrigation_pb2.ZoneEvent.Action.ON:
      raise kafka_util.EventConsumerException('No matching start event found.')

    zone = self._context.storage.zones.find_one({'id': zone_event.zone_id})
    if not zone:
      raise kafka_util.EventConsumerException(
          'Zone not found for id %s.', zone_event.zone_id)

    duration = (zone_event.timestamp.ToDatetime() -
                self._last_zone_event.timestamp.ToDatetime())
    water_amount_mm = zone.flow_rate_mmpm * duration.total_seconds() / 60

    event = irrigation_pb2.WaterLevelChangeEvent(
        timestamp=zone_event.timestamp,
        zone_id=zone_event.zone_id,
        change_amount_mm=water_amount_mm,
    )
    self._context.send_event(topics.Irrigation.WATER_LEVEL_CHANGE_TOPIC, event)


class EvaporationMonitor(pattern.Worker):
  def __init__(self, context, *args, **kwargs):
    super().__init__(worker_name='evaporation updater',
                     interval=datetime.timedelta(minutes=1),
                     clock=context.clock, *args, **kwargs)
    self._context = context
    self._next_timeslot = None

  def _on_start(self):
    current_timeslot = _timestamp_to_timeslot(self._context.clock.now())
    self._next_timeslot = _get_next_timeslot(current_timeslot)

  def _on_run(self):
    if self._context.clock.now() < self._next_timeslot:
      return

    zone_protos = list(self._context.storage.zones.find())
    for zone_proto in zone_protos:
      event = irrigation_pb2.WaterLevelChangeEvent(
          zone_id=zone_proto.id,
          change_amount_mm=-zone_proto.evaporation_rate_mmpm * 60,
      )
      event.timestamp.FromDatetime(self._next_timeslot)
      self._context.send_event(
          topics.Irrigation.WATER_LEVEL_CHANGE_TOPIC, event)

    self._next_timeslot = _get_next_timeslot(self._next_timeslot)


class RainMonitor(kafka_util.EventConsumer):
  def __init__(self, context, *args, **kwargs):
    super().__init__(kafka_consumer_builder=context.create_event_consumer,
                     topic=topics.Weather.WEATHER_SNAPSHOT_TOPIC,
                     group='RainMonitor', *args, **kwargs)
    self._context = context

  def _on_event(self, event):
    if event.last_1_hour_rain_amount_mm == 0:
      return

    self.logger.info('Sending WaterLevelChange event for rain amount of {0:.2f}mm.'.format(
        event.last_1_hour_rain_amount_mm))

    zones = list(self._context.storage.zones.find())
    for zone in zones:
      water_level_change_event = irrigation_pb2.WaterLevelChangeEvent(
          timestamp=event.timestamp,
          zone_id=zone.id,
          change_amount_mm=event.last_1_hour_rain_amount_mm,
      )
      self._context.send_event(topics.Irrigation.WATER_LEVEL_CHANGE_TOPIC,
                               water_level_change_event)

    self.logger.info('Sent events to all {0} zones.'.format(len(zones)))


class WaterLevelChangeMonitor(kafka_util.EventConsumer):
  def __init__(self, context, *args, **kwargs):
    super().__init__(kafka_consumer_builder=context.create_event_consumer,
                     topic=topics.Irrigation.WATER_LEVEL_CHANGE_TOPIC,
                     group='WaterLevelChangeMonitor', *args, **kwargs)
    self._context = context

  def _on_event(self, event):
    current_timeslot = _timestamp_to_timeslot(self._context.clock.now())
    change_timeslot = _timestamp_to_timeslot(event.timestamp.ToDatetime())
    if change_timeslot > current_timeslot:
      raise kafka_util.EventConsumerException(
          'Water level change shall not happen in future time: {0}.'.format(event))

    zone = self._context.storage.zones.find_one({'id': event.zone_id})
    if not zone:
      raise kafka_util.EventConsumerException(
          'Zone not found for id {0}.'.format(event.zone_id))

    self.logger.debug('Changing water level: timeslot={0} zone={1} amount={2:.5f}mm'.format(
        change_timeslot, event.zone_id, event.change_amount_mm))

    previous_timeslot = _get_previous_timeslot(change_timeslot)
    previous_water_level = self._get_last_water_level_by(
        previous_timeslot, event.zone_id)
    water_levels = self._get_water_levels_since(change_timeslot, event.zone_id)

    if not water_levels or water_levels[0].timeslot.ToDatetime() != change_timeslot:
      # Backfill water level for timeslot of change
      water_level = self._new_water_level(change_timeslot, event.zone_id)
      water_level.current_amount_mm = previous_water_level.current_amount_mm
      water_levels.insert(0, water_level)

    if water_levels[-1].timeslot.ToDatetime() != current_timeslot:
      # Add water level for current timeslot
      water_level = self._new_water_level(current_timeslot, event.zone_id)
      water_level.current_amount_mm = water_levels[-1].current_amount_mm
      water_levels.append(water_level)

    # Update water levels from timeslot of change to current timeslot
    water_levels[0].change_amount_mm += event.change_amount_mm
    for water_level in water_levels:
      new_amount_mm = previous_water_level.current_amount_mm + water_level.change_amount_mm
      water_level.current_amount_mm = min(
          max(0, new_amount_mm), zone.max_water_amount_mm)
      self._save_water_level(water_level)

      previous_water_level = water_level

    self.logger.debug('Updated {0} water level record(s). Current water level: {1:.5f}mm.'.format(
        len(water_levels), previous_water_level.current_amount_mm))

    self._send_water_level_event(water_levels[-1])

  def _get_last_water_level_by(self, timeslot, zone_id):
    water_level = self._context.storage.water_levels.find_one(
        filter={'zone_id': zone_id, 'timeslot': {'$lte': timeslot}},
        sort=[('timeslot', pymongo.DESCENDING)])
    if not water_level:
      water_level = self._new_water_level(timeslot, zone_id)

    return water_level

  def _get_water_levels_since(self, timeslot, zone_id):
    return list(self._context.storage.water_levels.find(
        filter={'zone_id': zone_id, 'timeslot': {'$gte': timeslot}},
        sort=[('timeslot', pymongo.ASCENDING)]))

  def _new_water_level(self, timeslot, zone_id):
    water_level = irrigation_pb2.WaterLevel(
        zone_id=zone_id,
        change_amount_mm=0,
        current_amount_mm=0,
    )
    water_level.timeslot.FromDatetime(timeslot)
    return water_level

  def _save_water_level(self, water_level):
    self._context.storage.water_levels.save(
        water_level,
        filter={
            'timeslot': water_level.timeslot.ToDatetime(),
            'zone_id': water_level.zone_id
        }
    )

  def _send_water_level_event(self, water_level):
    event = irrigation_pb2.WaterLevelEvent(
        timeslot=water_level.timeslot,
        zone_id=water_level.zone_id,
        current_amount_mm=water_level.current_amount_mm)
    self._context.send_event(
        topics.Irrigation.WATER_LEVEL_TOPIC, event)


class WaterLevelMonitorException(Exception):
  pass


class WaterLevelMonitor(pattern.Worker):

  def __init__(self, context, *args, **kwargs):
    super().__init__(worker_name='water level monitor',
                     interval=datetime.timedelta(minutes=1),
                     clock=context.clock, *args, **kwargs)
    self._context = context
    self._irrigation_service = self._context.create_grpc_service_stub(
        irrigation_pb2_grpc.IrrigationServiceStub,
        self._context.config.irrigation_service)

  def _on_run(self):
    if not self._should_run():
      return

    water_level = self._get_lowest_water_level()
    if not water_level:
      return
    if water_level.current_amount_mm > self._context.config.min_water_amount_mm:
      return

    zone = self._context.storage.zones.find_one({'id': water_level.zone_id})
    if not zone:
      raise WaterLevelMonitorException(
          'Zone {0} not found.'.format(water_level.zone_id))

    water_amount_mm = zone.max_water_amount_mm - water_level.current_amount_mm
    duration_sec = water_amount_mm / zone.flow_rate_mmpm * 60
    task = irrigation_pb2.Task(
        zone_id=water_level.zone_id, by=irrigation_pb2.By.SCHEDULER)
    task.duration.FromTimedelta(datetime.timedelta(seconds=duration_sec))
    task_list = irrigation_pb2.TaskList(tasks=[task])

    self.logger.info('Scheduling zone {0} to run {1:.1f} minutes...'.format(
        task.zone_id, duration_sec/60))
    self._irrigation_service.SubmitTasks([task])

  def _should_run(self):
    # Don't run if out of watering window.
    now = self._context.clock.now()
    windows = [x for x in self._context.config.watering_windows if x.from_hour <=
               now.hour and now.hour < x.to_hour]
    if not windows:
      return False

    # Don't run if there's pending tasks.
    task_list = self._irrigation_service.GetPendingTasks(empty_pb2.Empty())
    if task_list.tasks:
      return False

    return True

  def _get_lowest_water_level(self):
    earliest_time_to_consider = self._context.clock.now() - datetime.timedelta(hours=2)

    lowest_water_level = None
    for zone_id in self._context.zone_ids:
      water_level = self._context.storage.water_levels.find_one(
          filter={
              'zone_id': zone_id,
              'timeslot': {'$gte': earliest_time_to_consider}},
          sort=[('timeslot', pymongo.DESCENDING)],
          limit=1)
      if not water_level:
        continue
      if not lowest_water_level or water_level.current_amount_mm < lowest_water_level.current_amount_mm:
        lowest_water_level = water_level

    return lowest_water_level
