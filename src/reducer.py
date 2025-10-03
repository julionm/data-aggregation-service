import pika
import json
from datetime import datetime
from collections import Counter

class Reducer():

    def __init__(self):
        # this should be available for both systems (agg, red)
        self.TOP_N_ADS = 10

        receive_conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.receive_channel = receive_conn.channel()
        self.receive_channel.queue_declare(
            queue="agg-top-ad-clicks"
        )

        send_conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.send_channel = send_conn.channel() 
        self.send_channel.queue_declare(
            queue="red-top-ad-clicks"
        )

        self.initial_time = None
        self.data = Counter()

        print('[INFO] Application started.')

    def sort_and_send_rank(self):

        print('[INFO] Aggregated data will be sent to the queue.')

        top_n_ads = self.data.most_common(self.TOP_N_ADS)

        self.send_channel.basic_publish(
            exchange='',
            routing_key='red-top-ad-clicks',
            body=json.dumps(top_n_ads).encode('utf-8')
        )

        self.data = Counter()

    def message_handler(self, ch, method, properties, body):
        print('[INFO] Received new message.')

        payload = json.loads(body)

        if "created_at" not in payload or "data" not in payload:
            return

        created_at = datetime.strptime(payload['created_at'], "%Y-%m-%dT%H:%M:%S").replace(second=0)

        if self.initial_time is None:
            self.initial_time = created_at

        if self.initial_time != created_at:
            # handle sending to the next queue
            self.sort_and_send_rank()
            self.initial_time = created_at

        print(f'[INFO] Payload: {payload}')

        for item in payload['data']:
            if 'id' not in item or 'count' not in item:
                return
            self.data[item['id']] = item['count']
        
        print('[INFO] Message processed.')
        print(f'[INFO] Current Counter: {self.data}')

        # I dont know what a delivery tag is in RabbitMQ
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        try:
            self.receive_channel.basic_consume(
                queue='agg-top-ad-clicks',
                # auto_ack=True,
                on_message_callback=self.message_handler
            )

            print('[INFO] Listening queue: "top-ad-clicks".')

            self.receive_channel.start_consuming()
        except Exception as e:
            print(f'[ERROR] Unexpected error: {e}')


reducer = Reducer()
reducer.start()
