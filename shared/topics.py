class Irrigation(object):
  ZONE_TOPIC = 'ha.irrigation.zone'
  WATER_LEVEL_CHANGE_TOPIC = 'ha.irrigation.water_level_change'
  WATER_LEVEL_TOPIC = 'ha.irrigation.water_level'


class Weather(object):
  WEATHER_SNAPSHOT_TOPIC = 'ha.weather.snapshot'


TOPIC_PROTO_MAP = {}

try:
  from irrigation.proto import irrigation_pb2
  TOPIC_PROTO_MAP[Irrigation.ZONE_TOPIC] = irrigation_pb2.ZoneEvent
  TOPIC_PROTO_MAP[Irrigation.WATER_LEVEL_CHANGE_TOPIC] = irrigation_pb2.WaterLevelChangeEvent
  TOPIC_PROTO_MAP[Irrigation.WATER_LEVEL_TOPIC] = irrigation_pb2.WaterLevelEvent
except:
  pass

try:
  from weather.proto import weather_pb2
  TOPIC_PROTO_MAP[Weather.WEATHER_SNAPSHOT_TOPIC] = weather_pb2.Snapshot
except:
  pass
