# omnicross

An intersection crossing simulation for automate cars, powered by [omnipaxos](https://github.com/haraldng/omnipaxos) consensus algorithm.

## System architecture

<img src="README.assets/image-20230424212243243.png" alt="image-20230424212243243" style="zoom:80%;" />

## Deployment

The application is deployed in kubernetes. Where each pod runs one unique instance of the application.
Each pod hosts two containers. One for the client/application code and one spereate container for the replicated state machine that is used to establish a consensus between the nodes.

## Development

There is a dev container avaiable who will install all necessary dependencies for developing the application.
But not for running it locally. To run the application locally you need the following:

## Dependencies

- Docker
- minikube
- werf

## Commands

To run everything locally and access the cluster you really only need two commands.

This command builds the docker images and applies them to your local kubernetes cluster.
```bash
werf converge --repo <dockerhub_id>/omnicross
```

This commands gives you an IP address to access the cluster load balancer from your machine.
```bash
minikube service omnicross -n omnicross --url
```

To read logs from a specific container you can use `kubectl logs -c <container_name>` option.
```bash
k logs -n omnicross -c <container_name> omnicross-<pod_ordinal>
```

## API

To read the decided entries in the log:
```
[get] /dependency-graph/[from_idx]

Path: [from_idx] - Integer indicating the log index from which to read from

// NOTE: right now this function only returns the log
// TODO: return actual dependency graph
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

Here is a current example response:
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