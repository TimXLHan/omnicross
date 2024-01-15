import os
os.environ['SUMO_HOME'] = '/var/lib/flatpak/app/org.eclipse.sumo/x86_64/stable/active/files/share/sumo'
import sys
import traci
import traci.constants as tc
import json

def read_json_data_dependencies_for_junciton():
    dependencies_sim_file = open("dependencies_sim_random.json")
    
    dependencies_sim_data = json.load(dependencies_sim_file)
    
    return dependencies_sim_data["dependencies"]

# Required to find SUMO tools
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable for 'SUMO_HOME'")

sumoCmd = ["/app/bin/sumo-gui", "-c", "/home/simulator/simulation/simulation_all_random/sumo.cfg.xml"]

# Example of hash map
vehicle_order = read_json_data_dependencies_for_junciton()
# {"car1": 1, "car2": 2, "car3": 3, "car4": 4}

def has_cleared_junction(vehicle_id):
    edge = traci.vehicle.getRoadID(vehicle_id)
    return edge.startswith("0to")

def all_before_cleared(vehicle_id, vehicle_order):
    for vehicle in vehicle_order:
        if not vehicle["wait_for"]:
            return True
        else:
            for car_id in vehicle["wait_for"]:
                if not has_cleared_junction(car_id):
                    return False
            return True
                
    #order = vehicle_order[vehicle_id]
    #for v_id, v_order in vehicle_order.items():
    #    if v_order < order and v_id in traci.vehicle.getIDList():
    #        if not has_cleared_junction(v_id):
    #            return False
    #return True



traci.start(sumoCmd)

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    
    # Check if a car can move or should wait
    for vehicle in vehicle_order.copy(): # Note the use of list() here to make a copy
        if vehicle["car_id"] in [car[-1] for car in traci.vehicle.getIDList()]:
            # If the vehicle has cleared the junction or all before it have cleared, let it go
            if has_cleared_junction(vehicle["car_id"]) or all_before_cleared(vehicle["car_id"], vehicle_order):
                traci.vehicle.setSpeed(vehicle["car_id"], -1)
            else:
                traci.vehicle.setSpeed(vehicle["car_id"], 0)
            
            # Remove cars from vehicle_order once they pass the junction
            if has_cleared_junction(vehicle["car_id"]):
                vehicle_order.remove(vehicle)
                
traci.close()
