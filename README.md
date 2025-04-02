# TrafficModel

## Overview
This repository contains various traffic simulation models to analyze vehicle behavior in different scenarios. The main focus is on car-following models that simulate how vehicles adjust their speed and position in response to the vehicles ahead of them.

## Description
This project implements multiple car-following models:

1. The Helly model is a car-following model that calculates a vehicle's acceleration based on:
   - The relative speed between the vehicle and the one ahead of it
   - The difference between the actual distance and the desired safe distance to the vehicle ahead

2. The Follow-the-Leader model, which produced the best results, uses a simplified approach where:
   - The lead vehicle accelerates toward a desired speed
   - Following vehicles adjust their acceleration based on the distance and relative speed to the vehicle ahead
   - Safety mechanisms prevent vehicles from getting too close

3. Variations of the car-following model with different parameters and conditions

4. A Runge-Kutta implementation of the Intelligent Driver Model (IDM) 

## Files in this Repository

### Main Models
- `follow-the-leader.py`: The primary model with the most realistic results. Simulates 10 vehicles with a simple yet effective car-following behavior. Includes visualization of positions over time and handles safety measures to prevent collisions.

- `modeloHellycoches.py`: Implementation of the Helly car-following model that tracks positions, speeds, and accelerations of multiple vehicles with comprehensive visualization.

- `RungeKuttamethods.py`: Advanced implementation using different Runge-Kutta numerical methods to solve the IDM equations on a ring road with 50 vehicles. Includes comparison between RK1, RK3, and RK5 methods.

### Other Models
- `model.py`: Basic implementation of a car-following model with 10 vehicles.

- `model2.py`: Enhanced version simulating 20 vehicles with reaction delay and an introduced slowdown to study traffic jam formation.

- `modeloHelly.py`: Simplified macroscopic implementation of traffic flow based on density-speed relationships across road segments.

## Features
- Simulation of multiple vehicles (varying by model)
- Visualization of position, speed, and acceleration over time
- Analysis of vehicle spacing during simulation
- Configurable parameters for realistic traffic behavior
- Different mathematical approaches to traffic modeling
- Comparison of numerical integration methods

## Parameters
- `num_vehicles/num_cars`: Number of vehicles in the simulation
- `street_length/ring_length`: Length of the simulated road
- `time_steps/time_total`: Duration of simulation
- `dt`: Time step size in seconds
- `v_min`, `v_max`, `v_desired`: Speed parameters in different models

### Follow-the-Leader Model Parameters
- `k`: Acceleration factor for the lead car (default: 0.5)
- `c`: Proportional factor for following cars (default: 0.5)
- `b`: Deceleration constant for following cars (default: 10)
- `initial_distance`: Initial spacing between cars (default: 30m)

### Helly Model Parameters
- `alpha`: Sensitivity to speed difference (default: 0.5)
- `beta`: Sensitivity to distance difference (default: 0.2)
- `s0`: Desired spacing in meters (default: 10m)
- `T`: Time headway in seconds (default: 1.5s)

## Requirements
- Python 3.x
- NumPy
- Matplotlib
- SciPy (for RungeKuttamethods.py)

## Usage
Run any of the models using Python:
```
python follow-the-leader.py   # For the best results
python modeloHellycoches.py   # For Helly model
python RungeKuttamethods.py   # For IDM with different numerical methods
```

Modify the parameter values in the scripts to experiment with different traffic conditions.

## Outputs
The simulations produce visualizations relevant to each model:

### Follow-the-Leader Model
- Position of cars over time, showing how traffic flow evolves and how following cars react to the lead car
- Clear demonstration of traffic waves propagating backward through the line of vehicles

### Helly Model
1. Position vs. Time for each vehicle
2. Speed vs. Time for each vehicle
3. Acceleration vs. Time for each vehicle
4. Vehicle spacing over time

### Runge-Kutta Methods
- Comparison of different numerical integration methods (RK1, RK3, RK5) for solving traffic flow equations
- Position plots showing how these methods handle the simulation differently

## Results and Insights
The Follow-the-Leader model provides the most realistic traffic behavior, accurately capturing:
- How traffic disturbances propagate backward through a line of vehicles
- The accordion effect where vehicles compress and expand their spacing in response to speed changes
- Safety behaviors that prevent collisions while maintaining realistic flow

## Future Improvements
- Add command-line parameter options
- Include different traffic scenarios (e.g., traffic light, bottleneck)
- Implement additional car-following models for comparison
- Create animation of vehicle movement
- Calibrate models with real-world traffic data
- Extend to multi-lane traffic simulation

## License
[MIT License](LICENSE)
