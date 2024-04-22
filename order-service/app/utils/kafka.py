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
    import json
    
    # Define a method in the Order class to convert it to a dictionary
    def order_to_dict(order):
        return {
            "id": order.id,
            "product_id": order.product_id,
            "quantity": order.quantity
        }

    # Convert the Order object to a dictionary
    order_dict = order_to_dict(order)

    # Serialize the dictionary to JSON
    order_json = json.dumps(order_dict)
    
    # Send the JSON data to Kafka
    producer.produce('order_topic', value=order_json.encode('utf-8'))
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
            
            # Decode and print the message value
            print("Received message: {}".format(msg.value().decode('utf-8')))

    finally:
        # Close the consumer when done
        consumer.close()

