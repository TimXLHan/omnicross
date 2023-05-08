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

Here is an example response:
```json
{
  "decided_idx": 3,
  "node_id": 3,
  "log_data": [
    {
      "data": {
        "car_id": 3,
        "from": 3,
        "to": 0
      },
      "id": [
        3,
        "02cbb44d-874f-4f38-98e5-841638dbdc7d"
      ]
    },
    {
      "data": {
        "car_id": 2,
        "from": 2,
        "to": 1
      },
      "id": [
        2,
        "46c46125-a116-40b8-8964-c3e21fbbe99f"
      ]
    },
    {
      "data": {
        "car_id": 1,
        "from": 1,
        "to": 2
      },
      "id": [
        1,
        "448568f8-9972-41aa-a6c7-e09c8009572a"
      ]
    }
  ],
}
```