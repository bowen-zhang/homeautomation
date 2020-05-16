import datetime
import grpc
import threading
from google.protobuf import empty_pb2

from shared import topics
from irrigation.proto import irrigation_pb2
from irrigation.proto import irrigation_pb2_grpc
from third_party.common import pattern


class TaskManager(pattern.Worker):
  def __init__(self, context, *args, **kwargs):
    super().__init__(worker_name='task manager',
                     interval=datetime.timedelta(seconds=1),
                     clock=context.clock, *args, **kwargs)
    self._context = context
    self._tasks = []
    self._current_task = None
    self._expiration = None
    self._lock = threading.Lock()

    self._controller_service = self._context.create_grpc_service_stub(
        irrigation_pb2_grpc.ControllerServiceStub,
        self._context.config.controller_service)

  @property
  def is_busy(self):
    with self._lock:
      return self._current_task or self._tasks

  def _on_start(self):
    self.clear_tasks()
    self.logger.info('Started.')

  def _on_stop(self):
    self.clear_tasks()
    self.logger.info('Stopped.')

  def _on_run(self):
    now = self._context.clock.now()

    with self._lock:
      if self._current_task:
        if now > self._expiration:
          self._stop_current_task()

      if not self._current_task:
        if self._tasks:
          self._start_task(self._tasks.pop(0))

  def clear_tasks(self):
    with self._lock:
      self._clear_tasks()

  def submit_tasks(self, tasks):
    with self._lock:
      self._clear_tasks()

      for task in tasks:
        self.logger.debug('Enqueuing task {0}'.format(task))
        cloned_task = irrigation_pb2.Task()
        cloned_task.CopyFrom(task)
        self._tasks.append(cloned_task)

  def get_tasks(self):
    with self._lock:
      tasks = []
      if self._current_task:
        cloned_task = irrigation_pb2.Task()
        cloned_task.CopyFrom(self._current_task)
        cloned_task.duration.FromTimedelta(
            self._expiration - self._context.clock.now())
        tasks.append(cloned_task)

      for task in self._tasks:
        cloned_task = irrigation_pb2.Task()
        cloned_task.CopyFrom(task)
        tasks.append(cloned_task)

      return tasks

  @property
  def current_task(self):
    with self._lock:
      if self._current_task:
        cloned_task = irrigation_pb2.Task()
        cloned_task.CopyFrom(self._current_task)
        cloned_task.duration.FromTimedelta(
            self._expiration - self._context.clock.now())
        return cloned_task
      else:
        return irrigation_pb2.Task(zone_id=-1)

  def _clear_tasks(self):
    if self._current_task:
      self._stop_current_task()

    self._tasks.clear()

  def _start_task(self, task):
    self._controller_service.Start(task)
    self._current_task = task
    self._expiration = self._context.clock.now() + task.duration.ToTimedelta()

  def _stop_current_task(self):
    self._controller_service.Stop(empty_pb2.Empty())
    self._current_task = None
    self._expiration = None
