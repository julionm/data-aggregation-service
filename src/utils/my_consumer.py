from confluent_kafka import Consumer

class MyKafkaConsumer(Consumer):
    def __init__(self, groupId):
        config = {
            # here the client will try to connect to a list of different brokers
            # to get information about the Kafka cluster
            # for example, other brokers and partition leaders
            'bootstrap.servers': 'localhost:9092',
            'security.protocol': 'PLAINTEXT',
            'group.id': groupId,

            # 'debug': 'broker,protocol,security'
        }

        super().__init__(config)

my_consumer = MyKafkaConsumer("test-group")
my_consumer.subscribe(["ad-clicks"])