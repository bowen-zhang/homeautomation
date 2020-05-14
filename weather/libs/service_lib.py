import datetime
import pymongo

from third_party.common import pattern
from weather.proto import weather_pb2
from weather.proto import weather_pb2_grpc


class WeatherService(weather_pb2_grpc.WeatherServiceServicer, pattern.Logger):
  def __init__(self, context, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._context = context

  def GetSnapshots(self, request, context):
    snapshots = self._context.storage.snapshots.find(
        filter={
            'zipcode': request.zipcode,
            'timestamp': {'$gte': datetime.datetime.now() - datetime.timedelta(days=request.max_days)},
        },
        sort=[('timestamp', pymongo.ASCENDING)])
    return weather_pb2.GetSnapshotsResponse(snapshots=list(snapshots))
