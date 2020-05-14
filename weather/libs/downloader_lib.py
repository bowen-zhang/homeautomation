import datetime
import requests

from shared import topics
from third_party.common import pattern
from weather.proto import weather_pb2


def _dig(data, fields, default_value, transformer=None):
  for field in fields:
    if field not in data:
      return default_value

    data = data[field]

  if transformer:
    data = transformer(data)
  return data


class WeatherDownloader(pattern.Worker):
  _API = 'https://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&units=metric&appid={api_key}'

  def __init__(self, context, *args, **kwargs):
    super().__init__(worker_name='Weather Downloader',
                     interval=datetime.timedelta(minutes=1), *args, **kwargs)
    self._context = context

    now = datetime.datetime.now()
    self._next_run = datetime.datetime.combine(
        now.date(), datetime.time(now.hour, 0, 0))
    self._next_run += datetime.timedelta(hours=1)

  def _on_run(self):
    now = datetime.datetime.now()
    if now < self._next_run:
      return

    locations = self._context.storage.locations.find()
    for location in locations:
      snapshot = self._download(location)
      self._context.storage.snapshots.save(snapshot, filter={
          'zipcode': snapshot.zipcode,
          'timestamp': snapshot.timestamp.ToDatetime(),
      })
      self.logger.info('Saved.')
      self._context.send_event(topics.Weather.WEATHER_SNAPSHOT_TOPIC, snapshot)
      self.logger.info('Sent event.')

    self._next_run += datetime.timedelta(hours=1)

  def _download(self, location):
    self.logger.info('Downloading weather data for %s...', location.zipcode)

    url = self._API.format(zipcode=location.zipcode,
                           api_key=self._context.config.open_weather_map_api_key)
    response = requests.get(url)
    data = response.json()

    snapshot = weather_pb2.Snapshot(
        zipcode=location.zipcode,
        temperature_c=_dig(data, ['main', 'temp'], float('nan')),
        pressure_pa=_dig(data, ['main', 'pressure'],
                         float('nan'), lambda x: x*100),
        humidity=_dig(data, ['main', 'humidity'], float('nan')),
        visibility_m=_dig(data, ['visibility'], float('nan')),
        wind_speed_mps=_dig(data, ['wind', 'speed'], 0),
        wind_direction=_dig(data, ['wind', 'deg'], 0),
        last_1_hour_rain_amount_mm=_dig(data, ['rain', '1h'], 0),
        cloudiness=_dig(data, ['clouds', 'all'], 0),
    )
    timestamp = _dig(data, ['dt'], datetime.datetime.now(),
                     lambda x: datetime.datetime.fromtimestamp(x))
    snapshot.timestamp.FromDatetime(timestamp)

    self.logger.info('Downloaded:\n{0}'.format(snapshot))
    return snapshot
