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

  def run(self):
    component_factory = factory.ComponentFactory(self._context)
    self._components = [component_factory.create(
        x) for x in self._context.node_proto.components]
    for component in self._components:
      component.start()

    while True:
      time.sleep(1)


if __name__ == '__main__':
  app.start(NodeApp)
