import time
from google.protobuf import empty_pb2
from google.protobuf import timestamp_pb2

from security.proto import security_pb2
from security.proto import security_pb2_grpc
from third_party.common import pattern


class SecurityService(security_pb2_grpc.SecurityServiceServicer, pattern.Logger):
  def __init__(self, context, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._context = context

  def StreamVideo(self, request_iterator, context):
    for request in request_iterator:
      print(request.timestamp.ToDatetime())
      time.sleep(2)
      yield security_pb2.StreamVideoResponse()