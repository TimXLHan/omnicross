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