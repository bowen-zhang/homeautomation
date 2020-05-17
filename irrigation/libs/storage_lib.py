import pymongo

from irrigation.proto import irrigation_pb2
from third_party.common import pattern
from third_party.mongo_utils import storage as mongo_storage


class MongoStorage(pattern.Singleton):
  def __init__(self, database_name, server=None, port=27017, client=None):
    if server:
      client = pymongo.MongoClient(host=server, port=port)

    self._zones = mongo_storage.ProtobufMongoStorage(
        proto_cls=irrigation_pb2.Zone,
        database=database_name,
        collection='zones',
        client=client)
    self._runs = mongo_storage.ProtobufMongoStorage(
        proto_cls=irrigation_pb2.Run,
        database=database_name,
        collection='runs',
        client=client,
        indexes={
            'start_at_zone_id': [('start_at', pymongo.DESCENDING), ('zone_id', pymongo.ASCENDING)]
        })
    self._water_levels = mongo_storage.ProtobufMongoStorage(
        proto_cls=irrigation_pb2.WaterLevel,
        database=database_name,
        collection='water_levels',
        client=client,
        indexes={
            'timeslot_zone_id': [('timeslot', pymongo.DESCENDING), ('zone_id', pymongo.ASCENDING)]
        })
    self._alerts = mongo_storage.ProtobufMongoStorage(
        proto_cls=irrigation_pb2.Alert,
        database=database_name,
        collection='alerts',
        client=client,
        indexes={
            'timestamp': [('timestamp', pymongo.DESCENDING)]
        })

  @property
  def zones(self):
    return self._zones

  @property
  def runs(self):
    return self._runs

  @property
  def water_levels(self):
    return self._water_levels

  @property
  def alerts(self):
    return self._alerts

  def create_indexes(self):
    self._zones.create_indexes()
    self._runs.create_indexes()
    self._water_levels.create_indexes()
    self._alerts.create_indexes()
