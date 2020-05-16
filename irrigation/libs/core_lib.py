import datetime
import kafka
import mongomock
import time

from shared import topics
from irrigation.libs import mock_lib
from irrigation.libs import storage_lib
from shared import context_lib
from third_party.common import pattern
from third_party.common import time_util


class Context(context_lib.Context):
  def __init__(self, config=None, livemode=True, clock=None, storage=None, *args, **kwargs):
    if livemode:
      clock = time_util.RealWorldClock()
      storage = storage_lib.MongoStorage(database_name='irrigation')
    else:
      clock = clock or time_util.MockClock(now=datetime.datetime(2020, 1, 1, 4, 0, 0),
                                           elapse_rate=500.0)
      storage = storage or storage_lib.MongoStorage(
          client=mongomock.MongoClient(),
          database_name='irrigation_test')

    super().__init__(config=config, livemode=livemode, storage=storage, clock=clock,
                     kafka_endpoint=config.kafka, *args, **kwargs)

    self._zone_ids = None

  @property
  def zone_ids(self):
    if self._zone_ids is None:
      zone_protos = list(self._storage.zones.find())
      self._zone_ids = [x.id for x in zone_protos]
    return self._zone_ids
