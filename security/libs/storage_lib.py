import pymongo

from security.proto import security_pb2
from third_party.common import pattern
from third_party.mongo_utils import storage as mongo_storage


class MongoStorage(pattern.Singleton):
  def __init__(self, database_name='security', server=None, port=27017, client=None):
    if server:
      client = pymongo.MongoClient(host=server, port=port)

    self._nodes = mongo_storage.ProtobufMongoStorage(
        proto_cls=security_pb2.Node,
        database=database_name,
        collection='nodes',
        client=client,
        indexes={
            'id': [('id', pymongo.ASCENDING)]
        })

  @property
  def nodes(self):
    return self._nodes

  def create_indexes(self):
    self._nodes.create_indexes()
