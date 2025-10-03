# TODO

- [ ] Refactor Reducer
- [ ] Finish the first Raw Database Writer (raw ad clicks)
- [ ] Finish the second Database Writer (top ad clicks)
- [ ] Decide between polling or batching for the Aggregator
- [ ] Change how we treat times in Agg and Reducer (for now, no better option)
     - [ ] Answer: What are the downsides of using the way it is today?
- [ ] Add tests to the program
- [ ] Error handling in the application: where and how to send information about problems
     - [ ] Create the Logger class
- [ ] Investigate why sometimes I cannot CTRL + C out of the Aggregator app


## Done

- [x] See if modules are making sense within the project (utils)
- [x] Test again the whole process
- [x] Try using MaxHeap to improve data aggregation and sorting in Aggregators
- [x] Finish writing Reducer 
- [x] Test the entire flow
