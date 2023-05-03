import sys
import requests
from time import sleep

node = sys.argv[1]
print("Addr: ", node)

def run_request(node, text):
    print("Running put request...")
    resp = requests.put(node + "/apply", json={"command": text})
    print(resp)
    sleep(1)

run_request(node, "HI")
run_request(node, "WE")
run_request(node, "ARE")
run_request(node, "THE")
run_request(node, "CLUSTER")

print("Issueing print...")
resp = requests.get(node + "/print_log")
print(resp)