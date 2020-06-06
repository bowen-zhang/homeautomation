from absl import app
from absl import flags
from google.protobuf import text_format

from security.libs import storage_lib
from security.proto import security_pb2


FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', 'config.pbtxt',
                    'Path to config protoascii file.')


def main(_):
  config = security_pb2.Config()
  with open(FLAGS.config_path, 'r') as f:
    text_format.Merge(f.read(), config)

  storage = storage_lib.MongoStorage(server=config.mongodb.host,
                                     port=config.mongodb.port)

  for node in config.nodes:
    storage.nodes.save(node, filter={'id': node.id})

  print("Saved {0} nodes to database.".format(len(config.nodes)))


if __name__ == '__main__':
  app.run(main)
