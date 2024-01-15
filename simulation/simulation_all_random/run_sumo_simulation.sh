#!/bin/bash

# Path to the Python script
script_path="/home/simulator/simulation/simulation_all_random/junction_traffic_manager.py"

# Run the flatpak command
flatpak run --command=python3 org.eclipse.sumo "$script_path"
