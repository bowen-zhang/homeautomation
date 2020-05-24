from irrigation.libs import mock_lib
from third_party.common import pattern


class Zone(pattern.Logger):
  _gpio_initialized = False

  def __init__(self, context, proto):
    super().__init__()
    self._proto = proto
    self._clock = context.clock
    if context.livemode:
      from RPi import GPIO
      self._gpio = GPIO
    else:
      self._gpio = mock_lib.MockGPIO()
    self._running = False
    self._start_time = None

    if not self._gpio_initialized:
      self._gpio.setwarnings(False)
      self._gpio.setmode(self._gpio.BCM)
      self._gpio_initialized = True

    self._gpio.setup(self._proto.pin, self._gpio.OUT, initial=self._gpio.HIGH)

  @property
  def id(self):
    return self._proto.id

  @property
  def proto(self):
    return self._proto

  @property
  def running(self):
    return self._running

  def on(self):
    if self._running:
      return

    self._running = True
    self._start_time = self._clock.now()
    self._gpio.output(self._proto.pin, self._gpio.LOW)
    self.logger.info('Zone {0} ("{1}"): started at {2}.'.format(
        self._proto.id, self._proto.name, self._start_time))

  def off(self):
    if not self._running:
      return

    self._running = False
    duration = self._clock.now() - self._start_time
    self._gpio.output(self._proto.pin, self._gpio.HIGH)
    self.logger.info('Zone {0} ("{1}"): stopped at {2}. ({3} minutes)'.format(
        self._proto.id, self._proto.name, self._clock.now(),
        duration.total_seconds() / 60))
