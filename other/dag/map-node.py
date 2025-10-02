# Responsibilities
# - Normalize data
# - Format data
# - Send data evenly to each Aggregate node downstream

# TODO test if blocking connection is actually blocking
# I don't want to make this blocking, if possible, maybe even use something async
 
# TODO add the logic to split logs to each aggregate node
# RabbitMQ will do this automattically, but it'd still be really nice to do it by myself

import pika
from pika import channel
import json

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
main_channel = conn.channel()
main_channel.exchange_declare(exchange="ad_clicks_logs", exchange_type="fanout")

result = main_channel.queue_declare(queue='', exclusive=True) # meaning its temporary
queue_name = result.method.queue

main_channel.queue_bind(exchange="ad_clicks_logs", queue=queue_name)

workers = [
    {}, # one worker
    {}  # another worker
]
 
class RecoverException(Exception):
    pass

def get_worker(id):
    # in this function, I receive an ad_id and based on that, I decide to which node this should go into
    # how to divide the ad_ids evenly between partitions
    # this function returns the number/name/id of the partition where this'll be saved
    return workers[id % 2]    


def send_to_worker(payload):
    # How to deal with partitions?
    # Whole different files? Or something faster?

    worker = get_worker(payload["ad_id"])

    # ! failed connecting to the workers
    raise RecoverException
    

def callback(ch: channel.Channel, method, properties, body):
    # do any normalizations needed
    # do any changes in format
    # or even add more information to the object
    
    parsed_payload = json.loads(body)
    
    if (
        "ad_id" not in parsed_payload
        or "created_at" not in parsed_payload
        or not (type(parsed_payload["ad_id"]) == int)
    ):
        # mal-formed message, thus, we discard it
        ch.basic_reject(delivery_tag=1, requeue=False)
        return

    try:    
        send_to_worker(parsed_payload)
        ch.basic_ack(delivery_tag=1)
    except RecoverException:
        ch.basic_recover(requeue=True)
    except Exception as e:
        ch.basic_reject(delivery_tag=1, requeue=False)


main_channel.basic_consume(
    queue=queue_name,
    auto_ack=True, # leave this for now while I'm not sure if I want somehting more robust
    on_message_callback=callback
)

main_channel.start_consuming()
