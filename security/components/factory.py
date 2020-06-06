from security.components import video
from security.proto import security_pb2


class ComponentFactoryException(Exception):
  pass


class ComponentFactory(object):
  _COMPONENTS = {
      security_pb2.Video: video.VideoCapturer
  }

  def __init__(self, context):
    self._context = context

  def create(self, component_proto):
    name = component_proto.WhichOneof("kind")
    config_proto = getattr(component_proto, name)
    config_proto_cls = type(config_proto)
    if config_proto_cls not in self._COMPONENTS:
      raise ComponentFactoryException(
          "Component not found for config \"{0}\".".format(name))

    component_cls = self._COMPONENTS[config_proto_cls]
    return component_cls(context=self._context, config=config_proto)
