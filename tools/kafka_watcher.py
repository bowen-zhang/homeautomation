import kafka

from shared import topics

LIVEMODE = True


def main():
  all_topics = [x if LIVEMODE else 'test.' +
                x for x in topics.TOPIC_PROTO_MAP.keys()]

  consumer = kafka.KafkaConsumer(*all_topics,
                                 auto_offset_reset='earliest')

  print('Watching:')
  for topic in all_topics:
    print('\t' + topic)
  print()

  num = 1
  for msg in consumer:
    print('[{0}] TOPIC: {1} - {2}:{3}'.format(
        num, msg.topic, msg.partition, msg.offset))
    if not LIVEMODE:
      proto_cls = topics.TOPIC_PROTO_MAP[msg.topic[5:]]
    else:
      proto_cls = topics.TOPIC_PROTO_MAP[msg.topic]
    proto = proto_cls()
    try:
      proto.ParseFromString(msg.value)
      print(proto)
    except:
      print('Unable to parse: %s', msg.value)
    print()


if __name__ == '__main__':
  main()
