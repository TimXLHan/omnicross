import random
import sys
import requests
from time import sleep

node = sys.argv[1]
print("Calling cluster at: ", node)

def run_request(node, index):
    print("Running put request...")
    resp = requests.put(node + "/apply", json={
        "data": {
            "car_id": index,
            "from": random.randint(0, 3),
            "to": random.randint(0, 3)
        }
    })
    print(resp)

for i in range(0, 5):
    run_request(node, i)

sleep(2)
print("Reading log...")
resp = requests.get(node + "/read/0")
print(resp.text)