import datetime
import time


class FakeGPIO(object):
  IN = 0
  OUT = 1
  HIGH = 0
  LOW = 1
  BCM = 0

  def setwarnings(self, value):
    pass

  def setmode(self, mode):
    pass

  def setup(self, pin, in_out, initial=None):
    pass

  def output(self, pin, value):
    print('Pin {0} = {1}'.format(pin, value))


class FakeClock(object):
  def __init__(self):
    self._now = datetime.datetime.now()

  def now(self):
    return self._now

  def sleep(self, seconds):
    rate = 1000
    self._now += datetime.timedelta(seconds=seconds)
    time.sleep(seconds / rate)
