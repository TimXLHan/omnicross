# RSM

This application provides a replicated state machine based on the omnipaxos consensus algorithm.

## API

In order to apply something to the log:
```
[put] /apply

RequestJson: {
    data {
        car_id: Integer,
        from: Integer,
        to: Integer,
    }
}
```

To read the decided entries in the log:
```
[get] /read/[from_idx]

Path: [from_idx] - Integer indicating the log index from which to read from

ResponseJson: {
    node_id: Integer, #node you got your response from
    decided_idx: Integer, #decided index of log at time of reading
    log_data: [{
        id: [NodeId, Uuid], #proposer id, random identifier
        data: {
            car_id: Integer,
            from: Integer,
            to: Integer,
        }
    },...]
}
```