# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import weather_pb2 as weather__pb2


class WeatherServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetSnapshots = channel.unary_unary(
        '/ha.weather.WeatherService/GetSnapshots',
        request_serializer=weather__pb2.GetSnapshotsRequest.SerializeToString,
        response_deserializer=weather__pb2.GetSnapshotsResponse.FromString,
        )


class WeatherServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetSnapshots(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WeatherServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetSnapshots': grpc.unary_unary_rpc_method_handler(
          servicer.GetSnapshots,
          request_deserializer=weather__pb2.GetSnapshotsRequest.FromString,
          response_serializer=weather__pb2.GetSnapshotsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ha.weather.WeatherService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
