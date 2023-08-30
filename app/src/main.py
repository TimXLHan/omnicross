import os
import random
from time import sleep
import requests
from flask import Flask, jsonify
from wait_for_finder import find_wait_for
import config

app = Flask(__name__)

# increment by one required because pod ordinals start at 0,
# but omnipaxos only allows nodeids to start at 1
PID = int(os.environ['PODNAME'].split("-").pop())+1
if PID is None:
    raise TypeError("PID should not be none")

PORT = int(os.environ['PORT'])
if PORT is None:
    raise TypeError("PORT should not be none")

RSM_PORT = os.environ['RSM_PORT']
if RSM_PORT is None:
    raise TypeError("RSM_PORT should not be none")

REPLICAS = int(os.environ['REPLICAS'])
if REPLICAS is None:
    raise TypeError("REPLICAS should not be none")


def create_apply_req(from_entrance, to_exit):
    return {
        "data": {
            "car_id": PID,
            "from": from_entrance,
            "to": to_exit,
        },
    }


def apply_to_log(from_entrance, to_exit):
    url = f"http://localhost:{RSM_PORT}/apply"
    json = create_apply_req(from_entrance, to_exit)
    resp = requests.put(url=url, json=json)
    resp.raise_for_status


def read_from_log(from_idx):
    url = f"http://localhost:{RSM_PORT}/read/{from_idx}"
    resp = requests.get(url)
    resp.raise_for_status
    data = resp.json()
    return data

@app.route('/logs/<from_idx>')
def read_log(from_idx):
    log_data = read_from_log(from_idx)
    return jsonify(log_data)

@app.route('/dependency-graph/<from_idx>')
def create_dependency_graph(from_idx):
    log_data = read_from_log(from_idx)
    # find depedencies for every car
    dependencies = [
        {
            "car_id": x,
            "wait_for": find_wait_for(x, log_data)
        }
        for x in range(1, REPLICAS + 1)]

    res = {
        "log": log_data,
        "dependencies": dependencies
    }
    return jsonify(res)


if __name__ == "__main__":
    print("Waiting for cluster startup...")
    sleep(5)
    print("Telling cluster where I plan to go...")
    apply_to_log(PID, config.destinations[PID])
    print(f"Starting webserver on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT)
