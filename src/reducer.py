import pika
import json
from datetime import datetime
from collections import Counter

# ! This is not parsing correctly into Counter
# TODO transform this into a class Reducer

# this should be available for both systems (agg, red)
TOP_N_ADS = 10 

conn2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel2 = conn2.channel()

channel2.queue_declare(
    queue="red-top-ad-clicks"
)

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = conn.channel()

channel.queue_declare(
    queue="agg-top-ad-clicks"
)

initial_time = None
data = Counter()

print('[INFO] Application started.')

def sort_and_send_rank():
    global data

    print('[INFO] Aggregated data will be sent to the queue.')

    top_n_ads = data.most_common(TOP_N_ADS)

    channel2.basic_publish(
        exchange='',
        routing_key='red-top-ad-clicks',
        body=json.dumps(top_n_ads).encode('utf-8')
    )

    data = Counter()

def message_handler(ch, method, properties, body):
    global initial_time, data

    print('[INFO] Received new message.')

    payload = json.loads(body)

    if "created_at" not in payload or "data" not in payload:
        return

    created_at = datetime.strptime(payload['created_at'], "%Y-%m-%dT%H:%M:%S").replace(second=0)

    if initial_time is None:
        initial_time = created_at

    if initial_time != created_at:
        # handle sending to the next queue
        sort_and_send_rank()
        initial_time = created_at

    for item in payload['data']:
        if 'id' not in item or 'count' not in item:
            return

        data[item['id']] = item['count']
    
    print('[INFO] Message processed.')
    print(f'[INFO] Current Counter: {data}')

    # I dont know what a delivery tag is in RabbitMQ
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='agg-top-ad-clicks',
    # auto_ack=True,
    on_message_callback=message_handler
)

print('[INFO] Listening queue: "top-ad-clicks".')

channel.start_consuming()