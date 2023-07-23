
# this function is to convert the form_to data to the index
# for example, (1,2) -> 0
def data2index(frm, to):
    index_dict = {
        (1, 2): 0,
        (1, 3): 1,
        (1, 4): 2,
        (2, 1): 3,
        (2, 3): 4,
        (2, 4): 5,
        (3, 1): 6,
        (3, 2): 7,
        (3, 4): 8,
        (4, 1): 9,
        (4, 2): 10,
        (4, 3): 11,
    }
    return index_dict[(frm, to)]


def conflict_rule_setup():
    conflict_matrix = [[False for _ in range(12)] for _ in range(12)]
    # from1 conflicts
    conflict_matrix[data2index(1, 2)][data2index(2, 3)] = True
    conflict_matrix[data2index(1, 2)][data2index(2, 4)] = True
    conflict_matrix[data2index(1, 2)][data2index(2, 3)] = True
    conflict_matrix[data2index(1, 2)][data2index(3, 1)] = True
    conflict_matrix[data2index(1, 2)][data2index(3, 2)] = True
    conflict_matrix[data2index(1, 2)][data2index(4, 1)] = True
    conflict_matrix[data2index(1, 2)][data2index(4, 2)] = True
    conflict_matrix[data2index(1, 3)][data2index(2, 3)] = True
    conflict_matrix[data2index(1, 3)][data2index(2, 4)] = True
    conflict_matrix[data2index(1, 3)][data2index(3, 4)] = True
    conflict_matrix[data2index(1, 3)][data2index(4, 1)] = True
    conflict_matrix[data2index(1, 3)][data2index(4, 2)] = True
    conflict_matrix[data2index(1, 3)][data2index(4, 3)] = True
    conflict_matrix[data2index(1, 4)][data2index(2, 4)] = True
    conflict_matrix[data2index(1, 4)][data2index(3, 4)] = True
    # from2 conflicts
    conflict_matrix[data2index(2, 3)][data2index(3, 4)] = True
    conflict_matrix[data2index(2, 3)][data2index(3, 1)] = True
    conflict_matrix[data2index(2, 3)][data2index(3, 4)] = True
    conflict_matrix[data2index(2, 3)][data2index(4, 2)] = True
    conflict_matrix[data2index(2, 3)][data2index(4, 3)] = True
    conflict_matrix[data2index(2, 3)][data2index(1, 2)] = True
    conflict_matrix[data2index(2, 3)][data2index(1, 3)] = True
    conflict_matrix[data2index(2, 4)][data2index(3, 4)] = True
    conflict_matrix[data2index(2, 4)][data2index(3, 1)] = True
    conflict_matrix[data2index(2, 4)][data2index(4, 1)] = True
    conflict_matrix[data2index(2, 4)][data2index(1, 2)] = True
    conflict_matrix[data2index(2, 4)][data2index(1, 3)] = True
    conflict_matrix[data2index(2, 4)][data2index(1, 4)] = True
    conflict_matrix[data2index(2, 1)][data2index(3, 1)] = True
    conflict_matrix[data2index(2, 1)][data2index(4, 1)] = True
    # from3 conflicts
    conflict_matrix[data2index(3, 4)][data2index(4, 1)] = True
    conflict_matrix[data2index(3, 4)][data2index(4, 2)] = True
    conflict_matrix[data2index(3, 4)][data2index(4, 1)] = True
    conflict_matrix[data2index(3, 4)][data2index(1, 3)] = True
    conflict_matrix[data2index(3, 4)][data2index(1, 4)] = True
    conflict_matrix[data2index(3, 4)][data2index(2, 3)] = True
    conflict_matrix[data2index(3, 4)][data2index(2, 4)] = True
    conflict_matrix[data2index(3, 1)][data2index(4, 1)] = True
    conflict_matrix[data2index(3, 1)][data2index(4, 2)] = True
    conflict_matrix[data2index(3, 1)][data2index(1, 2)] = True
    conflict_matrix[data2index(3, 1)][data2index(2, 3)] = True
    conflict_matrix[data2index(3, 1)][data2index(2, 4)] = True
    conflict_matrix[data2index(3, 1)][data2index(2, 1)] = True
    conflict_matrix[data2index(3, 2)][data2index(4, 2)] = True
    conflict_matrix[data2index(3, 2)][data2index(1, 2)] = True
    # from4 conflicts
    conflict_matrix[data2index(4, 1)][data2index(1, 2)] = True
    conflict_matrix[data2index(4, 1)][data2index(1, 3)] = True
    conflict_matrix[data2index(4, 1)][data2index(1, 2)] = True
    conflict_matrix[data2index(4, 1)][data2index(2, 4)] = True
    conflict_matrix[data2index(4, 1)][data2index(2, 1)] = True
    conflict_matrix[data2index(4, 1)][data2index(3, 4)] = True
    conflict_matrix[data2index(4, 1)][data2index(3, 1)] = True
    conflict_matrix[data2index(4, 2)][data2index(1, 2)] = True
    conflict_matrix[data2index(4, 2)][data2index(1, 3)] = True
    conflict_matrix[data2index(4, 2)][data2index(2, 3)] = True
    conflict_matrix[data2index(4, 2)][data2index(3, 4)] = True
    conflict_matrix[data2index(4, 2)][data2index(3, 1)] = True
    conflict_matrix[data2index(4, 2)][data2index(3, 2)] = True
    conflict_matrix[data2index(4, 3)][data2index(1, 3)] = True
    conflict_matrix[data2index(4, 3)][data2index(2, 3)] = True
    return conflict_matrix

# To see log data format check root/README.md or rsm/README.md
def extract_data_from_log(log):
    return [item['data'] for item in log['log_data']]

# Find which car to wait for, return car id. If could not find current car in the log, return -1
# If no car to wait for, return 0
def find_wait_for(car_id, log, conflict_matrix=conflict_rule_setup()):
    car_id = int(car_id)
    found_flg = False
    frm_to = (0, 0)
    wait_for = []
    data = extract_data_from_log(log)
    for d in data:
        if d["car_id"] == car_id:
            found_flg = True
            frm_to = (d["from"], d["to"])
            break
    if not found_flg:
        return -1
    start_look_flg = False
    for d in data:
        if start_look_flg and d["car_id"] != car_id and conflict_matrix[data2index(frm_to[0], frm_to[1])][data2index(d["from"], d["to"])]:
            wait_for.append(d["car_id"])
        elif d["car_id"] == car_id:
            start_look_flg = True
    return wait_for

# Can be used for testing
if __name__ == '__main__':
    log = {
        "decided_idx": 4,
        "log_data": [
            {
                "data": {
                    "car_id": 3,
                    "from": 3,
                    "to": 2
                },
                "id": [
                    3,
                    "043bc4d7-2810-4098-82b5-fc85ac0252be"
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
                    "c93c9d74-586c-47bb-a91c-d18168dc4420"
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
                    "20a249d8-675e-48e1-9374-e2682ed07f35"
                ]
            },
            {
                "data": {
                    "car_id": 4,
                    "from": 4,
                    "to": 1
                },
                "id": [
                    4,
                    "011e673c-ea61-4a55-9f3d-7a759be22029"
                ]
            }
        ],
        "node_id": 4
    }
    print("Car 1 waits for car", find_wait_for(1, log))
    print("Car 2 waits for car", find_wait_for(2, log))
    print("Car 3 waits for car", find_wait_for(3, log))
    print("Car 4 waits for car", find_wait_for(4, log))
