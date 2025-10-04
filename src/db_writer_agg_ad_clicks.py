import pika
import psycopg
import json
from datetime import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

print("[INFO] Success connecting to RabbitMQ instance.")

QUEUE_NAME = 'red-top-ad-clicks'

channel.queue_declare(
    queue=QUEUE_NAME,
)

# TODO Remove this fixed values

with psycopg.connect("host=localhost port=5432 dbname=farloomdb user=admin password=admin123") as conn:

    print("[INFO] Success connecting to PostgreSQL instance.")

    with conn.cursor() as cur:
        def callback(ch, method, properties, body):
            print(f'[INFO] Received new message: {body}')
            payload = json.loads(body)
            
            if "created_at" not in payload or "data" not in payload:
                print(f'[ERROR] Mal-formed payload: {payload}.')
                return
            
            aggregated_at = datetime.strptime(payload["created_at"], "%Y-%m-%dT%H:%M:%S").replace(second=0)

            for item in payload['data']:
                if "id" in item and "count" in item:
                    cur.execute("""INSERT INTO public.top_ad_clicks (ad_id, clicks, agg_time, created_at) VALUES (%s, %s, %s, %s)"""
                                , (item["id"], item["count"], aggregated_at, datetime.now().replace(microsecond=0).isoformat()))
                else:
                    print(f"[ERROR] Failed parsing item: {item}.")
            
            conn.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=callback
            # this means that rabbitmq will control acknowledgment that this message has been completed by itself
            # if we do not specify, rabbitmq may just
        )

        channel.start_consuming()