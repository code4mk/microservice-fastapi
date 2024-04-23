import os
import json
from confluent_kafka import Producer, Consumer, KafkaError
from dotenv import load_dotenv

load_dotenv()

producer_config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_USERNAME'),
    'sasl.password': os.getenv('KAFKA_PASSWORD'),
    'default.topic.config': {'api.version.request': True}
}

consumer_config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_USERNAME'),
    'sasl.password': os.getenv('KAFKA_PASSWORD'),
    'default.topic.config': {'api.version.request': True},
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}

class KafkaService:
    def __init__(self):
        self.producer = Producer(producer_config)
        self.consumer = Consumer(consumer_config)

    def produce_to_kafka(self, topic, data):
        the_data = {
            'topic_name': topic,
            'data': data
        }
        data_json = json.dumps(the_data)
        self.producer.produce(topic, value=data_json.encode('utf-8'))
        self.producer.flush()

    def consume_from_kafka(self, topic):
        self.consumer.subscribe([topic])

        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print("Consumer error: {}".format(msg.error()))
                        break

                data = json.loads(msg.value().decode('utf-8'))
                print("Received message: {}".format(data))

        finally:
            self.consumer.close()
