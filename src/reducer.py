import pika
import json
from datetime import datetime
from collections import Counter

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

initial_time = datetime.now()
data = Counter()

def sort_and_send_rank():
    top_n_ads = data.most_common()

    pass

def message_handler(ch, method, properties, body):
    payload = json.loads(body)

    if "created_at" not in payload or "data" not in payload:
        return

    created_at = datetime.strptime(payload['created_at'], "%Y-%m-%dT%H:%M:%S").replace(second=0)

    if initial_time > created_at:
        return
    
    if initial_time != created_at:
        # handle sending to the next queue
        sort_and_send_rank()
        initial_time = created_at

    for item in payload['data']:
        if 'id' not in item or 'count' not in item:
            return

        data[item['id']] = item['count']
    
    # I dont know what a delivery tag is in RabbitMQ
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='top-ad-clicks',
    # auto_ack=True,
    on_message_callback=message_handler
)
channel.start_consuming()