from security.proto import security_pb2
from security.proto import security_pb2_grpc
from shared import context_lib
from third_party.common import net


class NodeContext(context_lib.Context):
  def __init__(self, config):
    super().__init__(config=config)
    self._id = None
    self._security_service = None
    self._node_proto = None

  @property
  def id(self):
    if not self._id:
      self._id = net.Interface.first().mac_address.lower()
      self.logger.info('Node id: {0}'.format(self._id))
    return self._id

  @property
  def security_service(self):
    if not self._security_service:
      self._security_service = self.create_grpc_service_stub(
          security_pb2_grpc.SecurityServiceStub,
          self.config.security_service)
    return self._security_service
