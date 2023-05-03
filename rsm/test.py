import requests
from time import sleep

node1 = "http://localhost:8081"
node2 = "http://localhost:8082"
node3 = "http://localhost:8083"

def run_request(node, text):
    print("Running put request...")
    resp = requests.put(node + "/apply", json={"command": text})
    print(resp)
    sleep(1)

run_request(node2, "HI")
run_request(node3, "WE")
run_request(node2, "ARE")
run_request(node2, "THE")
run_request(node1, "CLUSTER")

print("Issueing print...")
resp = requests.get(node1 + "/print_log")
resp = requests.get(node2 + "/print_log")
resp = requests.get(node3 + "/print_log")
print(resp)