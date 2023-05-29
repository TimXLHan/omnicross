
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

# refer to readme for type of log
def extract_data_from_log(log):
    return [item['data'] for item in log['log_data']]

# Find which car to wait for, return car id. If could not find current car in the log, return -1
# If no car to wait for, return 0
def find_wait_for(car_id, log, conflict_matrix=conflict_rule_setup()):
    found_flg = False
    frm_to = (0, 0)
    wait_for = 0
    data = extract_data_from_log(log)
    for d in data:
        if d["car_id"] == car_id:
            found_flg = True
            frm_to = (d["from"], d["to"])
            break
    if not found_flg:
        return -1
    for d in data:
        if d["car_id"] != car_id and conflict_matrix[data2index(frm_to[0], frm_to[1])][data2index(d["from"], d["to"])]:
            wait_for = d["car_id"]
        elif d["car_id"] == car_id:
            break
    return wait_for

# Can be used for testing
# if __name__ == '__main__':
#     log = {
#         "decided_idx": 3,
#         "node_id": 3,
#         "log_data": [
#             {
#                 "data": {
#                     "car_id": 4,
#                     "from": 4,
#                     "to": 1
#                 },
#                 "id": [
#                     3,
#                     "02cbb44d-874f-4f38-98e5-841638dbdc7d"
#                 ]
#             },
#             {
#                 "data": {
#                     "car_id": 3,
#                     "from": 3,
#                     "to": 4
#                 },
#                 "id": [
#                     3,
#                     "02cbb44d-874f-4f38-98e5-841638dbdc7d"
#                 ]
#             },
#             {
#                 "data": {
#                     "car_id": 2,
#                     "from": 2,
#                     "to": 3
#                 },
#                 "id": [
#                     2,
#                     "46c46125-a116-40b8-8964-c3e21fbbe99f"
#                 ]
#             },
#             {
#                 "data": {
#                     "car_id": 1,
#                     "from": 1,
#                     "to": 2
#                 },
#                 "id": [
#                     1,
#                     "448568f8-9972-41aa-a6c7-e09c8009572a"
#                 ]
#             }
#         ],
#     }
#     print(find_wait_for(1, log))
#     print(find_wait_for(2, log))
#     print(find_wait_for(3, log))
#     print(find_wait_for(4, log))
