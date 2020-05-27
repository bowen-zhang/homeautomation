# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import irrigation_pb2 as irrigation__pb2


class IrrigationServiceStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetConfig = channel.unary_unary(
                '/ha.irrigation.IrrigationService/GetConfig',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=irrigation__pb2.Config.FromString,
                )
        self.GetAlerts = channel.unary_unary(
                '/ha.irrigation.IrrigationService/GetAlerts',
                request_serializer=irrigation__pb2.GetAlertsRequest.SerializeToString,
                response_deserializer=irrigation__pb2.GetAlertsResponse.FromString,
                )
        self.DismissAlert = channel.unary_unary(
                '/ha.irrigation.IrrigationService/DismissAlert',
                request_serializer=irrigation__pb2.DismissAlertRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetAllZones = channel.unary_unary(
                '/ha.irrigation.IrrigationService/GetAllZones',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=irrigation__pb2.ZoneList.FromString,
                )
        self.GetZoneInfo = channel.unary_unary(
                '/ha.irrigation.IrrigationService/GetZoneInfo',
                request_serializer=irrigation__pb2.GetZoneInfoRequest.SerializeToString,
                response_deserializer=irrigation__pb2.GetZoneInfoResponse.FromString,
                )
        self.SaveZone = channel.unary_unary(
                '/ha.irrigation.IrrigationService/SaveZone',
                request_serializer=irrigation__pb2.Zone.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetWaterLevelHistory = channel.unary_unary(
                '/ha.irrigation.IrrigationService/GetWaterLevelHistory',
                request_serializer=irrigation__pb2.GetWaterLevelHistoryRequest.SerializeToString,
                response_deserializer=irrigation__pb2.GetWaterLevelHistoryResponse.FromString,
                )
        self.SubmitTasks = channel.unary_unary(
                '/ha.irrigation.IrrigationService/SubmitTasks',
                request_serializer=irrigation__pb2.TaskList.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetCurrentTask = channel.unary_unary(
                '/ha.irrigation.IrrigationService/GetCurrentTask',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=irrigation__pb2.Task.FromString,
                )
        self.GetPendingTasks = channel.unary_unary(
                '/ha.irrigation.IrrigationService/GetPendingTasks',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=irrigation__pb2.TaskList.FromString,
                )
        self.SetAutoSchedule = channel.unary_unary(
                '/ha.irrigation.IrrigationService/SetAutoSchedule',
                request_serializer=irrigation__pb2.AutoScheduleStatus.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetAutoSchedule = channel.unary_unary(
                '/ha.irrigation.IrrigationService/GetAutoSchedule',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=irrigation__pb2.AutoScheduleStatus.FromString,
                )


class IrrigationServiceServicer(object):
    """Missing associated documentation comment in .proto file"""

    def GetConfig(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAlerts(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DismissAlert(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllZones(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetZoneInfo(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveZone(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetWaterLevelHistory(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitTasks(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCurrentTask(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPendingTasks(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetAutoSchedule(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAutoSchedule(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IrrigationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.GetConfig,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=irrigation__pb2.Config.SerializeToString,
            ),
            'GetAlerts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAlerts,
                    request_deserializer=irrigation__pb2.GetAlertsRequest.FromString,
                    response_serializer=irrigation__pb2.GetAlertsResponse.SerializeToString,
            ),
            'DismissAlert': grpc.unary_unary_rpc_method_handler(
                    servicer.DismissAlert,
                    request_deserializer=irrigation__pb2.DismissAlertRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetAllZones': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllZones,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=irrigation__pb2.ZoneList.SerializeToString,
            ),
            'GetZoneInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetZoneInfo,
                    request_deserializer=irrigation__pb2.GetZoneInfoRequest.FromString,
                    response_serializer=irrigation__pb2.GetZoneInfoResponse.SerializeToString,
            ),
            'SaveZone': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveZone,
                    request_deserializer=irrigation__pb2.Zone.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetWaterLevelHistory': grpc.unary_unary_rpc_method_handler(
                    servicer.GetWaterLevelHistory,
                    request_deserializer=irrigation__pb2.GetWaterLevelHistoryRequest.FromString,
                    response_serializer=irrigation__pb2.GetWaterLevelHistoryResponse.SerializeToString,
            ),
            'SubmitTasks': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitTasks,
                    request_deserializer=irrigation__pb2.TaskList.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetCurrentTask': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCurrentTask,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=irrigation__pb2.Task.SerializeToString,
            ),
            'GetPendingTasks': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPendingTasks,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=irrigation__pb2.TaskList.SerializeToString,
            ),
            'SetAutoSchedule': grpc.unary_unary_rpc_method_handler(
                    servicer.SetAutoSchedule,
                    request_deserializer=irrigation__pb2.AutoScheduleStatus.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetAutoSchedule': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAutoSchedule,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=irrigation__pb2.AutoScheduleStatus.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ha.irrigation.IrrigationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IrrigationService(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def GetConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/GetConfig',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            irrigation__pb2.Config.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAlerts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/GetAlerts',
            irrigation__pb2.GetAlertsRequest.SerializeToString,
            irrigation__pb2.GetAlertsResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DismissAlert(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/DismissAlert',
            irrigation__pb2.DismissAlertRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllZones(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/GetAllZones',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            irrigation__pb2.ZoneList.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetZoneInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/GetZoneInfo',
            irrigation__pb2.GetZoneInfoRequest.SerializeToString,
            irrigation__pb2.GetZoneInfoResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveZone(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/SaveZone',
            irrigation__pb2.Zone.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetWaterLevelHistory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/GetWaterLevelHistory',
            irrigation__pb2.GetWaterLevelHistoryRequest.SerializeToString,
            irrigation__pb2.GetWaterLevelHistoryResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubmitTasks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/SubmitTasks',
            irrigation__pb2.TaskList.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCurrentTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/GetCurrentTask',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            irrigation__pb2.Task.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPendingTasks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/GetPendingTasks',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            irrigation__pb2.TaskList.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetAutoSchedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/SetAutoSchedule',
            irrigation__pb2.AutoScheduleStatus.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAutoSchedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.IrrigationService/GetAutoSchedule',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            irrigation__pb2.AutoScheduleStatus.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)


class ControllerServiceStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Start = channel.unary_unary(
                '/ha.irrigation.ControllerService/Start',
                request_serializer=irrigation__pb2.Task.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.Stop = channel.unary_unary(
                '/ha.irrigation.ControllerService/Stop',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class ControllerServiceServicer(object):
    """Missing associated documentation comment in .proto file"""

    def Start(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stop(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ControllerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Start': grpc.unary_unary_rpc_method_handler(
                    servicer.Start,
                    request_deserializer=irrigation__pb2.Task.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'Stop': grpc.unary_unary_rpc_method_handler(
                    servicer.Stop,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ha.irrigation.ControllerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ControllerService(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def Start(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.ControllerService/Start',
            irrigation__pb2.Task.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Stop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ha.irrigation.ControllerService/Stop',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
