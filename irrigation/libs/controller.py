import datetime
import threading
import time

from irrigation.proto import irrigation_pb2
from third_party.common import pattern


class Station(object):
  _gpio_initialized = False

  def __init__(self, proto, clock, gpio_module):
    self._running = False
    self._start_time = None
    self._proto = proto
    self._clock = clock
    self._gpio = gpio_module

    if not Station._gpio_initialized:
      self._gpio.setwarnings(False)
      self._gpio.setmode(self._gpio.BCM)
      Station._gpio_initialized = True

    self._gpio.setup(self._proto.pin, self._gpio.OUT, initial=self._gpio.HIGH)

  @property
  def id(self):
    return self._proto.id

  @property
  def running(self):
    return self._running

  def on(self):
    if self._running:
      return

    self._running = True
    self._start_time = self._clock.now()
    self._gpio.output(self._proto.pin, self._gpio.LOW)
    print('Station {0} ("{1}"): started at {2}.'.format(
        self._proto.id, self._proto.name, self._start_time))

  def off(self):
    if not self._running:
      return

    self._running = False
    duration = self._clock.now() - self._start_time
    self._gpio.output(self._proto.pin, self._gpio.HIGH)
    print('Station {0} ("{1}"): stopped at {2}. ({3} minutes)'.format(
        self._proto.id, self._proto.name, self._clock.now(),
        duration.total_seconds() / 60))


class TaskManager(pattern.Worker):
  def __init__(self, stations):
    super().__init__(worker_name='station manager',
                     interval=datetime.timedelta(seconds=1))
    self._stations = stations
    self._tasks = []
    self._current_task = None
    self._expiration = None
    self._lock = threading.Lock()

  def _on_run(self):
    now = time.time()
    with self._lock:
      if self._current_task:
        if now > self._expiration:
          self._all_off()
          self._current_task = None
          self._expiration = None

      if not self._current_task:
        if self._tasks:
          self._current_task = self._tasks.pop(0)
          self._expiration = now + self._current_task.duration_sec
          self._on(self._current_task.station_id)

  def clear_tasks(self):
    with self._lock:
      self._all_off()
      self._tasks.clear()
      self._current_task = None
      self._expiration = None

  def submit_tasks(self, tasks):
    with self._lock:
      self._all_off()
      self._tasks.clear()
      self._current_task = None
      self._expiration = None
      self._tasks = tasks

  def get_tasks(self):
    with self._lock:
      tasks = []
      if self._current_task:
        tasks.append(irrigation_pb2.Task(
            station_id=self._current_task.station_id,
            duration_sec=int(self._expiration - time.time()),
        ))
      for task in self._tasks:
        tasks.append(irrigation_pb2.Task().CopyFrom(task))

      return tasks

  @property
  def current_task(self):
    with self._lock:
      if self._current_task:
        return irrigation_pb2.Task(
            station_id=self._current_task.station_id,
            duration_sec=int(self._expiration - time.time()),
        )
      else:
        return irrigation_pb2.Task(
            station_id=-1,
            duration_sec=0,
        )

  def on(self, id, duration_sec):
    self.submit_tasks([
        irrigation_pb2.Task(
            station_id=id,
            duration_sec=duration_sec
        )
    ])

  def _on(self, id):
    station = next(x for x in self._stations if x.id)
    if not station:
      raise 'Station (id={0}) not found.'.format(id)

    station.on()

  def _all_off(self):
    for station in self._stations:
      station.off()
