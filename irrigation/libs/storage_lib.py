import pymongo

from irrigation.proto import irrigation_pb2
from third_party.common import pattern
from third_party.mongo_utils import storage as mongo_storage


class MongoStorage(pattern.Singleton):
  def __init__(self, database_name, client=None):
    self._zones = mongo_storage.ProtobufMongoStorage(
        proto_cls=irrigation_pb2.Zone,
        database=database_name,
        collection='zones',
        client=client)
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
  def water_levels(self):
    return self._water_levels

  @property
  def alerts(self):
    return self._alerts

  def create_indexes(self):
    self._zones.create_indexes()
    self._water_levels.create_indexes()
    self._alerts.create_indexes()
