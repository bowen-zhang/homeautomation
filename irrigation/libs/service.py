from google.protobuf import empty_pb2

from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc


class IrrigationService(irrigation_pb2_grpc.IrrigationServiceServicer):
  def __init__(self, config_proto, task_manager):
    self._config_proto = config_proto
    self._task_manager = task_manager

  def GetConfig(self, request, context):
    return self._config_proto

  def SubmitTasks(self, request, context):
    self._task_manager.clear_tasks()
    self._task_manager.submit_tasks(request.tasks)
    return empty_pb2.Empty()

  def GetCurrentTask(self, request, context):
    return self._task_manager.current_task

  def GetPendingTasks(self, request, context):
    return irrigation_pb2.TaskList(
        tasks=self._task_manager.get_tasks(),
    )
