# https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-message
from confluent_kafka import Consumer
import json
import pika
from datetime import datetime
from utils import MyKafkaConsumer
from collections import Counter

class Queue():
    def __init__(self):
        queue_conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.queue_channel = queue_conn.channel()
        self.queue_channel.queue_declare(
            queue="agg-top-ad-clicks",
            durable=False,
        )
    
    def send(self, data: dict):
        self.queue_channel.basic_publish(
            exchange='',
            routing_key='agg-top-ad-clicks',
            body=json.dumps(data).encode('utf-8')
        )

class Aggregator():

    def __init__(self):
        # TODO make this information load from somewhere else
        KAFKA_TOPIC = 'ad-clicks'
        KAFKA_CONSUMER_GROUP = 'aggregators'

        # this should be available for both systems (agg, red)
        self.TOP_N_ADS = 10 

        self.queue = Queue()
        
        try:
            self.kafka_consumer = MyKafkaConsumer(KAFKA_CONSUMER_GROUP)
            self.kafka_consumer.subscribe([KAFKA_TOPIC])
        except Exception as e:
            print(f'[ERROR] Error when subscribing to Kafka: {e}')

        self.data = Counter()
        self.initial_time = datetime.now().replace(second=0)

    def __handle_aggregation(self):
        top_n_ads = list(map(
            lambda item: { 'id': item[0], 'count': item[1] },
            self.data.most_common(self.TOP_N_ADS)
        ))
        
        payload = {
            "created_at": f'{self.initial_time.replace(microsecond=0).isoformat()}',
            'data': top_n_ads
        }

        print('[INFO] Sending aggregated data.')

        self.queue.send(payload)
        self.data = Counter()

    def __message_handler(self, msg):
        ad_id = json.loads(msg.key())
        payload = json.loads(msg.value())
        
        if "created_at" not in payload:
            return

        # getting a created_at that has only date, hour and minute
        # because the aggregation time is 1 minute
        created_at = datetime.strptime(payload['created_at'], "%Y-%m-%dT%H:%M:%S").replace(second=0)
        print(f'[INFO] Received new message ID: {ad_id}.')

        # In order for this to work, I need to test:
        # 1. Is the new date lesser than the initial? Then discard this
        # 2. Is the new date equal to initial? Then we aggregate
        # 3. Is the new date greater than the initial? Then I submit the old aggregated data
        if self.initial_time > created_at:
            # maybe raise exception or send a notification that this happened
            return
        
        if self.initial_time != created_at:
            print('[INFO] Started sending data.')
            self.__handle_aggregation()
            self.initial_time = created_at
        
        ad_agg_id = f'ad_click{ad_id}'
        self.data.update([ad_agg_id])
    
    def process(self):
        msg = self.kafka_consumer.poll()

        if msg is None:
            return
        if msg.error():
            print(f'[ERROR] Error received: {msg.error()}')
        elif msg is not None:
            self.__message_handler(msg)
    
    def start(self):
        try:
            print('[INFO] Aggregator is now listening to messages.')
            while True:
                self.process()
        except KeyboardInterrupt:
            pass
        finally:
            self.kafka_consumer.close()

aggregator = Aggregator()
aggregator.start()
