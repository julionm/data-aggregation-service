# Learnings from creating a Data Aggregation Service

## Project Structure

For the basic structure, we have a log watcher that received an enormous amount of ad clicks.
We have each ad saved to a database called `farloom_db`.

The log watcher service, just randomly generates ad clicks and send them to a queue in RabbitMQ.
A Database Writer (DW) is subscribed to this queue and saves this as a log in a `raw` schema in `farloom_db`.

The Data Aggregation Service (DAG), also subscribed to the same queue, goes and process the clicks info.
It then spits the ad count and the top 100 ads in the last minute.
This information is published to another queue in RabbitMQ, which is now handled by another DW.

It becomes available in our final database, where the data is already aggregated and ready to be visualized,
using an analytics tool.


## RabbitMQ for queing

Short introduction on how RabbitMQ works.
For this project, we'll be using the Pub/Sub model to publish a single message to multilpe subscribers.

To achieve this in RabbitMQ, you first need to create a new exchange.
Multiple queues can be *binded* to that one exchange, therefore, we create a new temporary queue in each of our subscribed services.
So, when the service is dropped, the queue and all the information within it will be too.

If we want, we can make this information and these queues persistent even after the RabbitMQ service is dropped,
but, in our current scenario, we don't need it.
And if, in the future, we want to scale this system horizontally, we can easily do that by just running the DAG or the DW in a new machine,
without needing a new proper name to the new queue.

As for the queues, I've opted to use the `Pika` library for Python, as recommended in the RabbitMQ documentation.
We can have multiple consumers for a single queue, each consumer will be considered as a worker node that received a message and consumes it,
by default, RabbitMQ drops the message as soon as a consumer receives it, but you can change to do it manually in your code.

### The Round-Robin technique

This structure of having multiple sender and worker nodes is called The Round-Robin technique.
By default, a RabbitMQ queue will evenly send messages to each consumer.
So if we have, 1000 incoming messages and we have 2 worker nodes, each will receive 500 messages.

The catch is, RabbitMQ does not care if it received an acknowledgement or not, so you don't know for sure that the message was 
correctly processed.

```
QoS = Quality of Service
AMQP = Advanced Message Queuing Protocol 
prefetch_count = total number of UNACKNOWLEDGED messages a single consumer is allowed to have
```

But, you can configure this by using `channel.basic_qos(prefetch_count=1)`.
This way, you know that every consumer will only handle one message at a time and no message will be left unacknowledged.

### Auto Acknowledgement

By setting `auto_ack=true`, RabbitMQ will not wait for an acknowledgement from the consumer, it'll just consider that as done,
therefore, dropping the message from the queue and not waiting for a signal from the worker node.


## MapReduce framework and why to use it

We have different with different responsibilities.
The Map node, for instance, will define which ad_logs will go to each aggregator. For example, every ad_id % 2 = 0 goes to Node 1
and the rest goes to Node 2. We could implement a totally different rule if we want.
Also, by having this Map node, we can normalize or clean the data before sending it to the next downstream node.
 
The aggregate nodes, will be responsible to aggregate the data based on the amount of minutes. How to create this?

The reduce node, will simply find the answer based on the results of each node and then send it to a RabbiMQ queue.
How to do this?

Main Problems:
- communication between nodes
  - to take advantage of parallelism in this case, I need to think in a way for the nodes to communicate
  - we could use shared memory, like create different threads, or try using tcp-ip
