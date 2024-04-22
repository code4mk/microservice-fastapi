# app/utils/kafka.py
import os
from confluent_kafka import Producer, Consumer, KafkaError
from app.models.order import Order
from dotenv import load_dotenv

load_dotenv()

producer_config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_USERNAME'),
    'sasl.password': os.getenv('KAFKA_PASSWORD'),
    'default.topic.config': {'api.version.request': True},
    'session.timeout.ms': 45000
}

consumer_config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_USERNAME'),
    'sasl.password': os.getenv('KAFKA_PASSWORD'),
    'default.topic.config': {'api.version.request': True},
    'session.timeout.ms': 45000,
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}

producer = Producer(producer_config)

def send_order_to_kafka(order: Order):
    producer.produce('order_topic', value=order.model_dump_json().encode('utf-8'))
    producer.flush()

consumer = Consumer(consumer_config)

def consume_order_from_kafka():
    consumer.subscribe(['order_topic'])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print("Consumer error: {}".format(msg.error()))
                    break

            # Process the order
            order = Order.parse_raw(msg.value().decode('utf-8'))
            print("Received order:", order)
    finally:
        # Close the consumer when done
        consumer.close()
