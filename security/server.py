import flask
import grpc
import time
from absl import flags
from concurrent import futures

from security.libs import context_lib
from security.libs import image_lib
from security.libs import service_lib
from security.proto import security_pb2
from security.proto import security_pb2_grpc
from third_party.common import app

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.pbtxt',
                    'Path to config protoascii file.')


class ServerApp(app.App):
  def __init__(self):
    super().__init__(name='server',
                     config_path=FLAGS.config_path,
                     config_proto_cls=security_pb2.Config)
    self.init_logging(log_path='/tmp')

    self._web = flask.Flask(__name__)
    self._context = context_lib.ServerContext(
        config=self.config, web=self._web)

    self._image_server = image_lib.ImageServer(context=self._context)
    self._security_service = service_lib.SecurityService(
        context=self._context, image_server=self._image_server)

  def run(self):
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    security_pb2_grpc.add_SecurityServiceServicer_to_server(
        self._security_service, grpc_server)
    port = self._context.config.security_service.port
    grpc_server.add_insecure_port('[::]:{0}'.format(port))
    grpc_server.start()
    self.logger.info('Started GRPC service on port {0}.'.format(port))

    self.logger.info('Running...')
    self._web.run(
        host='0.0.0.0', port=self._context.config.webserver.port, debug=True)


if __name__ == '__main__':
  app.start(ServerApp)
