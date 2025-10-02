# this supposedly "log watcher" will create ads to send the queue
# it will randomly generate ad clicks data
# which steps to take in order to make it work:
# 1. create the actual ads descriptions in a database - DONE
# 2. randomly generate clicks for them
# 3. each ad click MUST have: Ad ID and TIMESTAMP

# TODO add an external volume to RabbitMQ container, just like I did with postgres

import random
import pika
import time
from datetime import datetime
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

print("[INFO] Success Connecting to RabbitMQ.")

channel.exchange_declare(exchange="ad_clicks_logs", exchange_type='fanout')

ad_ids = list(range(1,51))

for _ in range(10000):
    ad_id = random.choice(ad_ids)
    timestamp = datetime.now()
    payload = { "ad_id": ad_id, "created_at": f'{timestamp}' }
    channel.basic_publish(
        exchange='ad_clicks_logs',
        routing_key='',
        body=json.dumps(payload).encode('utf-8'), # this will need to be a binary or json or whatever
    )
    print('[INFO] New message sent.')
    time.sleep(2)

connection.close()