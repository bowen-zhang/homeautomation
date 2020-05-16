from irrigation.proto import irrigation_pb2


class MockGPIO(object):
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


def init_test_db(context):
  for i in range(1, 4):
    zone = irrigation_pb2.Zone(
        id=i,
        name='Zone {0}'.format(i),
        pin=i,
        flow_rate_mmpm=0.6,
        max_water_amount_mm=9,
        evaporation_rate_mmpm=0.0019,
    )
    context.storage.zones.save(zone)
