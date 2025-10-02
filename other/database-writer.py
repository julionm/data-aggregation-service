import pika
import psycopg
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

print("[INFO] Success connecting to RabbitMQ instance.")

channel.exchange_declare(exchange="ad_clicks_logs", exchange_type="fanout")

result = channel.queue_declare(queue='', exclusive=True) # this means, this is a temporary queue
queue_name = result.method.queue

channel.queue_bind(exchange="ad_clicks_logs", queue=queue_name)

with psycopg.connect("host=localhost port=5432 dbname=farloomdb user=admin password=admin123") as conn:

    print("[INFO] Success connecting to PostgreSQL instance.")

    with conn.cursor() as cur:
        def callback(ch, method, properties, body):
            # log info will be sent to raw database table
            print(f'[INFO] Received new message: {body}')
            payload = json.loads(body)
            # would use ch to acknowledge rabbitmq that this is complete and that it should
            # drop the message from the queue
            if "ad_id" in payload and "created_at" in payload:
                cur.execute("""INSERT INTO raw.ad_clicks_logs (ad_id, created_at) VALUES (%s, %s)"""
                            , (payload["ad_id"], payload["created_at"]))
                conn.commit()
            else:
                print("[ERROR] Failed parsing payload.")

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
            # this means that rabbitmq will control acknowledgment that this message has been completed by itself
            # if we do not specify, rabbitmq may just
        )

        channel.start_consuming()