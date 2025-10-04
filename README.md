# Data Aggregation Service

This DAG consists of a couple different parts. Here's a short appresentation of the flow
and the nodes within it.

- Log Watcher: this simulates a service that receives Ad Clicks information from many different places
- Kafka: Log Watcher sends each Ad Click to a corresponding topic "ad-clicks" in Kafka
- Raw Database Writer: this database writer is consuming every message that arrives in "ad-clicks" and 
  saves them in a raw schema inside the Postgres database. As Kafka only stores the data for a specific
  amount of days, using Postgres we have this data reliably stored for later usage.
- Aggregator Nodes: each Aggregator node will receive Ad Clicks for the same Ad IDs it's responsible for.
  So, the first Aggregator, may be responsible for Ad Ids 1, 2 and 3, therefore it'll only aggregate the
  clicks for these Ads. After a previous set amount of time has passed, it gets the top X (default: 10)
  most clicked Ads and send that to the Reducer.
- Reducer: the Reducer is responsible for aggregating the data from each Aggregator node for the amount
  of time specified previously. Each Aggregator, aggregates for their own Ad Ids, but the Reducer does
  it for all Ad Ids it received. It then gets the top X (default: 10) Ads within the lists it gets
  from the Aggregator nodes and send it to the Top Ads Database Writer.
- Top Ads Database Writer: service responsible for storing in the database the information it receives
  from Reducer node. It's responsible for the data validation and consistency, rejecting mal-formed or
  ivnalid information.
