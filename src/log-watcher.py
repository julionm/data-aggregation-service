# https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-message
from confluent_kafka import Producer
from datetime import datetime
from random import choice
from time import sleep
import json

# TODO (MAYBE) try to make this work for different timestamps

KAFKA_TOPIC = 'ad-clicks'

config = {
    # here the client will try to connect to a list of different brokers
    # to get information about the Kafka cluster
    # for example, other brokers and partition leaders
    'bootstrap.servers': 'localhost:9092',
    'security.protocol': 'PLAINTEXT',
    'acks': 'all', # I dont know very well how this works in Kafka

    # 'debug': 'broker,protocol,security'
}

producer = Producer(config)

ad_ids = list(range(1, 51))

for _ in range(200):

    ad_id = choice(ad_ids)
    created_at = datetime.now().replace(microsecond=0).isoformat()
    payload = {
        "ad_id": ad_id,
        "created_at": f"{created_at}"
    }
    
    producer.produce(
        KAFKA_TOPIC,
        json.dumps(payload).encode('utf-8'),
        json.dumps(ad_id),
    )

    # logging for test purposes
    # print(f'{created_at} [INFO] New event produced for ad_id: {ad_id}')

    # poll is used to ensure the message was delivered, we can call it everytime we send a message
    # but I believe, that in my use-case I can just ignore this
    # producer.poll(20)

    sleep(1)
    
producer.flush()
