import datetime
import threading
from google.protobuf import empty_pb2

from shared import topics
from irrigation.libs import utils
from irrigation.libs import zone_lib
from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc
from third_party.common import pattern


class ControllerException(Exception):
  pass


class Controller(pattern.Worker):
  def __init__(self, context, *args, **kwargs):
    super().__init__(worker_name="controller",
                     interval=datetime.timedelta(seconds=1),
                     clock=context.clock,
                     *args, **kwargs)
    self._context = context
    self._lock = threading.Lock()
    self._running_zone = None
    self._start_time = None
    self._expiration = None
    self._today = self._context.clock.now().date()
    self._total_duration_secs = {}

  def _on_run(self):
    if self._context.clock.now().date() > self._today:
      self._total_duration_secs = {}
      self._today = self._context.clock.now().date()

    if not self._running_zone:
      return

    with self._lock:
      if not self._running_zone:
        return

      if not self._is_valid_time_to_run():
        self._stop()
        msg = 'VIOLATION: Zone {0} is running outside normal time window!'.format(
            self._running_zone.id)
        self._async(self._save_alert, msg)
        raise ControllerException(msg)

      if self._context.clock.now() > self._expiration:
        self._stop()

  def _on_stop(self):
    self.stop_task()

  def start_task(self, task):
    zone_proto = self._context.storage.zones.find_one({'id': task.zone_id})
    if not zone_proto:
      raise ControllerException(
          'Zone {0} not found.'.format(task.zone_id))

    if not self._is_valid_time_to_run():
      msg = 'VIOLATION: Attempt to run zone {0} outside normal time window!'.format(
          task.zone_id)
      self._async(self._save_alert, msg)
      raise ControllerException(msg)

    if self._is_watering_too_much(task):
      msg = 'VIOLATION: Zone {0} is watering too much.'.format(task.zone_id)
      self._async(self._save_alert, msg)
      raise ControllerException(msg)

    with self._lock:
      if self._running_zone:
        self._stop()

      self._running_zone = zone_lib.Zone(self._context, zone_proto)
      self._start_time = self._context.clock.now()
      self._expiration = self._start_time + task.duration.ToTimedelta()
      self.logger.info('Starting zone {0} ({1})...to be stopped by {2}.'.format(
          zone_proto.id, zone_proto.name, self._expiration))
      self._running_zone.on()

      event = irrigation_pb2.ZoneEvent(
          zone_id=task.zone_id,
          action=irrigation_pb2.ZoneEvent.Action.ON,
          by=task.by,
      )
      event.timestamp.FromDatetime(self._start_time)
      self._async(self._context.send_event,
                  topics.Irrigation.ZONE_TOPIC, event)

  def stop_task(self):
    with self._lock:
      if not self._running_zone:
        return
      self._stop()

  def _stop(self):
    zone_id = self._running_zone.id
    end_time = self._context.clock.now()
    duration = end_time - self._start_time

    self.logger.info('Stopping zone {0}...'.format(zone_id))
    self._running_zone.off()
    self._running_zone = None
    self._start_time = None
    self._expiration = None
    self._total_duration_secs[zone_id] = self._total_duration_secs.get(
        zone_id, 0) + duration.total_seconds()

    event = irrigation_pb2.ZoneEvent(
        zone_id=zone_id,
        action=irrigation_pb2.ZoneEvent.Action.OFF,
        by=irrigation_pb2.By.UNKNOWN,
    )
    event.timestamp.FromDatetime(end_time)
    self._async(self._context.send_event, topics.Irrigation.ZONE_TOPIC, event)

  def _async(self, func, *args, **kwargs):
    threading.Thread(target=func, args=args,
                     kwargs=kwargs, daemon=True).start()

  def _save_alert(self, msg):
    alert = irrigation_pb2.Alert(message=msg)
    alert.timestamp.FromDatetime(self._context.clock.now())
    self._context.storage.alerts.save(alert)

  # Violation checks

  def _is_valid_time_to_run(self):
    now = self._context.clock.now()
    return not utils.is_in_any_time_window(now, self._context.config.controller.no_watering_windows)

  def _is_watering_too_much(self, task):
    total = self._total_duration_secs.get(task.zone_id, 0)
    total += task.duration.ToTimedelta().total_seconds()
    return total > self._context.config.controller.max_running_secs_per_day


class ControllerService(irrigation_pb2_grpc.ControllerServiceServicer):
  def __init__(self, controller, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._controller = controller

  def Start(self, task, context):
    self._controller.start_task(task)
    return empty_pb2.Empty()

  def Stop(self, request, context):
    self._controller.stop_task()
    return empty_pb2.Empty()
