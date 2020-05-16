import grpc
import kafka

from shared import topics
from third_party.common import pattern


class Context(pattern.Logger):
  def __init__(self, config, livemode=True, clock=None, kafka_endpoint=None, storage=None, *args, **kwargs):
    super().__init__(self, *args, **kwargs)
    self._config = config
    self._livemode = livemode
    self._clock = clock
    self._storage = storage
    self._topic_prefix = '' if livemode else 'test.'
    self._kafka_server = '{0}:{1}'.format(
        kafka_endpoint.host, kafka_endpoint.port)
    self._kafka_producer = None

    self.logger.info('Running in %s mode.', 'LIVE' if livemode else 'TEST')

  @property
  def livemode(self):
    return self._livemode

  @property
  def config(self):
    return self._config

  @property
  def clock(self):
    return self._clock

  @property
  def storage(self):
    return self._storage

  @property
  def kafka_producer(self):
    if not self._kafka_producer:
      self.logger.info('Creating Kafka producer to %s...', self._kafka_server)
      self._kafka_producer = kafka.KafkaProducer(
          bootstrap_servers=[self._kafka_server],
          acks='all')
    return self._kafka_producer

  def send_event(self, topic, proto):
    actual_topic = self._topic_prefix + topic
    self.logger.info('Sending event: [{0}]:\n{1}'.format(actual_topic, proto))
    self.kafka_producer.send(actual_topic, proto.SerializeToString())
    self.kafka_producer.flush()
    self.logger.info('Event is sent.')

  def create_event_consumer(self, topic, group=None, proto_cls=None, *args, **kwargs):
    if not proto_cls:
      proto_cls = topics.TOPIC_PROTO_MAP[topic]

    def _proto_deserializer(raw):
      proto = proto_cls()
      proto.ParseFromString(raw)
      return proto

    actual_topic = self._topic_prefix + topic
    self.logger.debug(
        'Creating Kafka consumer: [{0}:{1}]'.format(actual_topic, group))
    consumer = kafka.KafkaConsumer(actual_topic,
                                   bootstrap_servers=[self._kafka_server],
                                   group_id=group,
                                   value_deserializer=_proto_deserializer,
                                   *args,
                                   **kwargs)
    if not self._livemode:
      self.logger.debug(
          '[{0}:{1}] Obtaining assignment...'.format(actual_topic, group))
      while not consumer.assignment():
        consumer.poll(timeout_ms=100)
      partition = list(consumer.assignment())[0]
      pos = consumer.position(partition)
      self.logger.debug(
          '[{0}:{1}] Last position: {2}'.format(actual_topic, group, pos))
      if group:
        consumer.seek_to_end()
        consumer.position(partition)
        self.logger.debug(
            '[{0}:{1}] Moved to latest position: {2}'.format(actual_topic, group, pos))

    return consumer

  def consume_events(self, topic, group=None, proto_cls=None):
    consumer = self.create_event_consumer(topic, group, proto_cls)
    for msg in consumer:
      yield msg.value

  def create_grpc_service_stub(self, stub_class, endpoint):
    channel = grpc.insecure_channel(
        '{0}:{1}'.format(endpoint.host, endpoint.port))
    return stub_class(channel)
