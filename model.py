import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_cars = 10
v_desired = 70  # m/s (desired speed)
k = 0.9  # acceleration factor
c = 10   # deceleration constant
dt = 0.1  # time step in seconds
time_total = 20  # total simulation time in seconds

# Initial conditions
num_steps = int(time_total / dt)
velocities = np.zeros((num_cars, num_steps))
positions = np.zeros((num_cars, num_steps))

# Initial position setup (spacing cars)
initial_distance = 50
positions[0, 0] = 0  # Lead car starts at 0
for i in range(1, num_cars):
    positions[i, 0] = positions[i-1, 0] - initial_distance

# Simulation
for t in range(1, num_steps):
    for i in range(num_cars):
        if i == 0:
            # Lead car acceleration
            a = k * (v_desired - velocities[i, t-1])
        else:
            # Distance to the car in front
            d = positions[i-1, t-1] - positions[i, t-1]
            a = k * (v_desired - velocities[i, t-1]) - c / max(d, 1)
            if d < 2:  # Safety check to prevent overlap
                a = -5  # Hard braking

        # Update velocity and position
        velocities[i, t] = max(0, velocities[i, t-1] + a * dt)
        positions[i, t] = positions[i, t-1] + velocities[i, t-1] * dt + 0.5 * a * dt**2

# Plot the results
for i in range(num_cars):
    plt.plot(np.arange(0, time_total, dt), positions[i], label=f"Car {i+1}")

plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position of Cars Over Time")
plt.legend()
plt.show()
