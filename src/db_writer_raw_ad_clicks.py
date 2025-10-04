from utils import MyKafkaConsumer
import psycopg
import json

# TODO how to handle different datetime formats across different Consumer Groups?

KAFKA_TOPIC = 'ad-clicks'

consumer = MyKafkaConsumer("raw-database-writer")
consumer.subscribe([KAFKA_TOPIC])

with psycopg.connect("host=localhost port=5432 dbname=farloomdb user=admin password=admin123") as conn:

    print("[INFO] Success connecting to PostgreSQL instance.")

    with conn.cursor() as cur:
        def save_ad(ad_id, created_at):
            # log info will be sent to raw database table
            # would use ch to acknowledge rabbitmq that this is complete and that it should
            # drop the message from the queue
            cur.execute("""INSERT INTO raw.ad_clicks_logs (ad_id, created_at) VALUES (%s, %s)"""
                        , (ad_id, created_at))
            conn.commit()
            print('[INFO] Message saved to Raw Database.')

        try:
            while True:
                # understand how this works for multiple consumer groups
                msg = consumer.poll()

                if msg is None:
                    continue
                elif msg.error():
                    print('[ERROR] Error receiving message.')
                else:
                    print(f'[INFO] Received new message.')

                    ad_id = json.loads(msg.key())
                    payload = json.loads(msg.value())

                    if "created_at" not in payload:
                        print('[ERROR] Message missing created_at attribute.')
                        continue

                    save_ad(ad_id, payload['created_at'])

        except Exception as e:
            print(f'[ERROR] An exception occured while waiting for messages: {e}')

        
    