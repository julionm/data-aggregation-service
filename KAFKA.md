# Kafka

## Kafka connection

To improve security, upon Kafka setup, we can configure it to use SASL
to manage Kafka connections, thus, requiring a username and a password.

## Topic



## Partition

## Message

The basic payload that will be stored within each partition in a Kafka topic.

## Producer

Client application that will produce messages to Kafka.
In the __confluent_kafka__ lib the Producer has an internal queue of messages to be delivered.

## Consumer

Client application that will consume messages from Kafka.

## Consumer Groups

## Broker

Kafka instance that stores the topics, partitions and all the information required to manage messages.
In a single Kafka cluster, there may be multiple Kafka brokers.

## Controller

Kafka instance that controls traffic and contains the Kafka brokers.

## Commit

Process of telling Kafka which messages have been successfully processed.
Each commit requires a request to the broker, so it shouldn't be done for every message
because this reduces throughput (thus performance) and increases latency.
**How does this process works??**
**What are the downsides of NOT commiting?**

## Offset

Each message in Kafka has its own sequential ID, attributed by Kafka when the message first arrives at the Broker.
Offset just means what was the last message processed by the Consumer.
This way, if the Consumer processed a message with ID of 25, the Consumer __commits__ the Offset 26 to Kafka, which will be the ID of the next
message.

## KRaft


# Questions

- In the case where I have 2 or more Consumer Groups, consuming from the same topic, how does commit work in this case?
  Does Kafka has a different way to handle commits for each Consumer Group?
  - yes, it's separate

- What exactly happens when a Consumer commits to Kafka?
