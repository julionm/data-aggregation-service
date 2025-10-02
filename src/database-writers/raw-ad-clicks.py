from utils import MyKafkaConsumer
import psycopg
import json

KAFKA_TOPIC = 'ad-clicks'

consumer = MyKafkaConsumer("raw-database-writer")
consumer.subscribe([KAFKA_TOPIC])

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

        try:
            while True:
                # understand how this works for multiple consumer groups
                msg = consumer.poll()

                if msg is None:
                    continue
                elif msg.error():
                    print('[ERROR] Error receiving message.')
                else:
                    payload = msg.value()
        except Exception as e:
            print(f'[ERROR] An exception occured while waiting for messages: {e}')

        
    