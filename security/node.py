import grpc
import time
from absl import flags

from security.components import factory
from security.libs import context_lib
from security.proto import security_pb2
from third_party.common import app

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.pbtxt',
                    'Path to config protoascii file.')


class NodeApp(app.App):
  def __init__(self):
    super().__init__(name='node',
                     config_path=FLAGS.config_path,
                     config_proto_cls=security_pb2.Config)
    self.init_logging(log_path='/tmp')

    self._context = context_lib.NodeContext(config=self.config)
    self._node_proto = None

  def run(self):
    self._init()

    self.logger.info('Starting node \"{0}\"...'.format(self._node_proto.name))

    component_factory = factory.ComponentFactory(self._context)
    self._components = [component_factory.create(
        x) for x in self._node_proto.components]
    for component in self._components:
      component.start()

    try:
      while True:
        time.sleep(1)
    except:
      for component in self._components:
        component.stop()

  def _init(self):
    self.logger.info('Registering node {0}...'.format(self._context.id))

    request = security_pb2.RegisterNodeRequest(node_id=self._context.id)
    while True:
      try:
        response = self._context.security_service.RegisterNode(request)
        self._node_proto = response.node
        self.logger.info('Received node configuration.')
        break
      except grpc.RpcError:
        time.sleep(5)

    self._context.set_name(self._node_proto.name)


if __name__ == '__main__':
  app.start(NodeApp)
