
import datetime


class ManualModel(object):
  def run(self, stations):
    pass


class NaiveModel(object):
  _TIME_BETWEEN_STATIONS_SEC = 7

  def __init__(self, proto, clock):
    self._proto = proto
    self._clock = clock

    if not self._proto.HasField('last_update'):
      self._proto.last_update.FromDatetime(self._clock.now())
      self._proto.amount_in = 0

  def run(self, stations):
    print('Running at: {0}'.format(self._clock.now()))
    self._update_current_amount()
    print('Current amount: {0}'.format(self._proto.amount_in))
    if self._proto.amount_in <= 0:
      duration = datetime.timedelta(minutes=self._proto.water_amount_in /
                                    self._proto.flow_rate_inpm)
      print('Water for {0} minutes / station...'.format(
          duration.total_seconds() / 60))
      for station in stations:
        station.on()
        self._clock.sleep(duration.total_seconds())
        station.off()
        self._clock.sleep(self._TIME_BETWEEN_STATIONS_SEC)
      self._proto.amount_in = self._proto.water_amount_in

  def _update_current_amount(self):
    now = self._clock.now()
    elapsed = now - self._proto.last_update.ToDatetime()
    self._proto.last_update.FromDatetime(now)
    self._proto.amount_in -= self._proto.consumption_rate_inpd * elapsed.total_seconds(
    ) / 86400.0
    if self._proto.amount_in < 0:
      self._proto.amount_in = 0


class WeatherBasedModel(object):
  _API_KEY = '199e5d392d1a0faf2f99111a34ed9657'
  _URL = 'https://api.darksky.net/forecast/{key}/{lat},{lon},{time}'

  def __init__(self, proto, location_proto, clock):
    self._proto = proto
    self._location_proto = location_proto
    self._clock = clock

  def run(self, stations):
    url = self._URL.format(
        key=self._API_KEY,
        lat=self._location_proto.lat,
        lon=self._location_proto.lon,
        time=self._clock.now().strftime('%Y-%m-%dT%H:%M:%S'))
