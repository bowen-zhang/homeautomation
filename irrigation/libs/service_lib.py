import datetime
import pymongo
from google.protobuf import empty_pb2

from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc
from third_party.common import pattern


class IrrigationService(irrigation_pb2_grpc.IrrigationServiceServicer, pattern.Logger):
  def __init__(self, context, task_manager, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._context = context
    self._task_manager = task_manager

  def GetConfig(self, request, context):
    return self._context.config

  def GetAlerts(self, request, context):
    alerts = list(self._context.storage.alerts.find(
        sort=[('timestamp', pymongo.DESCENDING)],
        limit=request.max_count))
    return irrigation_pb2.GetAlertsResponse(alerts=alerts)

  def DismissAlert(self, request, context):
    self._context.storage.alerts.collection.delete_one(filter={
        'timestamp': request.timestamp.ToDatetime(),
    })
    return empty_pb2.Empty()

  def GetAllZones(self, _, context):
    zones = list(self._context.storage.zones.find())
    return irrigation_pb2.ZoneList(zones=zones)

  def SaveZone(self, zone, context):
    self._context.storage.zones.save(zone, filter={'id': zone.id})
    self.logger.info('Saved zone {0}.'.format(zone.id))
    return empty_pb2.Empty()

  def GetWaterLevelHistory(self, request, context):
    since = self._context.clock.now() - datetime.timedelta(days=request.max_days)
    water_levels = self._context.storage.water_levels.find(
        filter={
            'zone_id': request.zone_id,
            'timeslot': {'$gte': since},
        },
        sort=[('timeslot', pymongo.ASCENDING)])

    runs = self._context.storage.runs.find(
        filter={
            'zone_id': request.zone_id,
            'stop_at': {'$gte': since},
        },
        sort=[('start_at', pymongo.ASCENDING)])

    return irrigation_pb2.GetWaterLevelHistoryResponse(
        water_levels=list(water_levels),
        runs=list(runs),
    )

  def SubmitTasks(self, request, context):
    self._task_manager.submit_tasks(request.tasks)
    return empty_pb2.Empty()

  def GetCurrentTask(self, request, context):
    return self._task_manager.current_task

  def GetPendingTasks(self, request, context):
    return irrigation_pb2.TaskList(
        tasks=self._task_manager.get_tasks(),
    )

  def SetAutoSchedule(self, request, context):
    self._context.set_config('/ha/irrigation/auto_schedule', request.enabled)
    return empty_pb2.Empty()

  def GetAutoSchedule(self, request, context):
    return irrigation_pb2.AutoScheduleStatus(
        enabled=self._context.get_config('/ha/irrigation/auto_schedule', True)
    )
