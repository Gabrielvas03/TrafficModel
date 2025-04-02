# TrafficModel

## Overview
This repository contains a traffic simulation model based on the Helly car-following model. The simulation models the behavior of multiple vehicles in a linear road, tracking their positions, speeds, and accelerations over time.

## Description
The Helly model is a car-following model that calculates a vehicle's acceleration based on:
1. The relative speed between the vehicle and the one ahead of it
2. The difference between the actual distance and the desired safe distance to the vehicle ahead

## Features
- Simulation of multiple vehicles (currently set to 5)
- Visualization of position, speed, and acceleration over time
- Analysis of vehicle spacing during simulation
- Configurable parameters for realistic traffic behavior

## Parameters
- `num_vehicles`: Number of vehicles in the simulation (default: 5)
- `street_length`: Visualization limit in meters (default: 1000m)
- `time_steps`: Number of simulation steps (default: 200)
- `dt`: Time step size in seconds (default: 0.1s)
- `v_min`, `v_max`: Minimum and maximum speeds in km/h (default: 0 to 60 km/h)

### Helly Model Parameters
- `alpha`: Sensitivity to speed difference (default: 0.5)
- `beta`: Sensitivity to distance difference (default: 0.2)
- `s0`: Desired spacing in meters (default: 10m)
- `T`: Time headway in seconds (default: 1.5s)

## Requirements
- Python 3.x
- NumPy
- Matplotlib

## Usage
Run the simulation with default parameters:
```
python modeloHellycoches.py
```

Modify the parameter values in the script to experiment with different traffic conditions.

## Outputs
The simulation produces the following visualizations:
1. Position vs. Time for each vehicle
2. Speed vs. Time for each vehicle
3. Acceleration vs. Time for each vehicle
4. Vehicle spacing over time

## Future Improvements
- Add command-line parameter options
- Include different traffic scenarios (e.g., traffic light, bottleneck)
- Implement additional car-following models for comparison
- Create animation of vehicle movement

## License
[MIT License](LICENSE)
