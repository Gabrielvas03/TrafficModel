import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_cars = 20
v_desired = 70  # m/s (desired speed)
k = 0.7  # acceleration factor
c = 15   # deceleration constant
dt = 0.1  # time step in seconds
time_total = 40  # total simulation time in seconds
reaction_delay = 0.5  # seconds of reaction delay

# Initial conditions
num_steps = int(time_total / dt)
velocities = np.zeros((num_cars, num_steps))
positions = np.zeros((num_cars, num_steps))
reaction_buffer = int(reaction_delay / dt)  # Number of steps for reaction delay

# Initial position setup (spacing cars)
initial_distance = 20  # Closer spacing to simulate denser traffic
positions[0, 0] = 0  # Lead car starts at 0
for i in range(1, num_cars):
    positions[i, 0] = positions[i-1, 0] - initial_distance

# Introduce a random slowdown in the lead car after a certain time
slowdown_time = 15  # seconds into the simulation to start the slowdown
slowdown_steps = int(slowdown_time / dt)

# Simulation
for t in range(1, num_steps):
    for i in range(num_cars):
        if i == 0:
            # Lead car logic: introduce a slowdown
            if t >= slowdown_steps and t < slowdown_steps + 50:
                a = -2  # Decelerate lead car
            else:
                a = k * (v_desired - velocities[i, t-1])
        else:
            # Distance to the car in front
            d = positions[i-1, t-reaction_buffer] - positions[i, t-1]
            a = k * (v_desired - velocities[i, t-1]) - c / max(d, 1)
            if d < 2:  # Safety check for hard braking
                a = -5  # Hard braking

        # Update velocity and position
        velocities[i, t] = max(0, velocities[i, t-1] + a * dt)
        positions[i, t] = positions[i, t-1] + velocities[i, t-1] * dt + 0.5 * a * dt**2

# Plot the results
plt.figure(figsize=(12, 6))
for i in range(num_cars):
    plt.plot(np.arange(0, time_total, dt), positions[i], label=f"Car {i+1}")

plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position of Cars Over Time - Traffic Jam Simulation")
plt.legend()
plt.show()
