# TODO

- [ ] Make easier to run and test the entire flow maybe use a Makefile or Docker
- [ ] Save the full timestamp in the Raw Database Writer (need to update log-watcher and aggregator)
- [ ] Add tests to the program
- [ ] Error handling in the application: where and how to send information about problems
     - [ ] Create the Logger class
- [ ] Investigate why sometimes I cannot CTRL + C out of the Aggregator app
- [ ] Change how we treat times in Agg and Reducer (for now, no better option)
     - [ ] What are the downsides of using the way it is today? (ask neto)
- [ ] Remove static database connection information from scripts

# Done

- [x] See if modules are making sense within the project (utils)
- [x] Test again the whole process
- [x] Try using MaxHeap to improve data aggregation and sorting in Aggregators
- [x] Finish writing Reducer 
- [x] Test the entire flow
- [x] Refactor Reducer
- [x] Finish the first Raw Database Writer (raw ad clicks)
- [x] Finish the second Database Writer (top ad clicks)
- [x] Decide between polling or batching for the Aggregator
     - I decided to continue using polling for now,
       but if escalating becomes an issue, moving to batching is fairly simple
