from shared.proto import common_pb2
from weather.proto import weather_pb2
from third_party.common import pattern
from third_party.mongo_utils import storage as mongo_storage


class MongoStorage(pattern.Singleton):
  def __init__(self, database_name, client=None):
    self._snapshots = mongo_storage.ProtobufMongoStorage(proto_cls=weather_pb2.Snapshot,
                                                         database=database_name,
                                                         collection='snapshots',
                                                         client=client)

    self._locations = mongo_storage.ProtobufMongoStorage(proto_cls=common_pb2.Location,
                                                         database=database_name,
                                                         collection='locations',
                                                         client=client)

  @property
  def snapshots(self):
    return self._snapshots

  @property
  def locations(self):
    return self._locations
