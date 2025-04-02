import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_cars = 10
v_desired = 70  # Desired speed for the lead car (m/s)
k = 0.5  # Acceleration factor for the lead car
c = 0.5  # Proportional factor for following cars
b = 10   # Deceleration constant for following cars
dt = 0.1  # Time step in seconds
time_total = 20  # Total simulation time in seconds

# Initial conditions
num_steps = int(time_total / dt)
velocities = np.zeros((num_cars, num_steps))
positions = np.zeros((num_cars, num_steps))

# Initial position setup (spacing cars)
initial_distance = 30  # Initial spacing between cars
positions[0, 0] = 0  # Lead car starts at position 0
for i in range(1, num_cars):
    positions[i, 0] = positions[i-1, 0] - initial_distance  # Cars are positioned behind each other

# Simulation loop
for t in range(1, num_steps):
    for i in range(num_cars):
        if i == 0:
            # Lead car acceleration towards desired speed
            a = k * (v_desired - velocities[i, t-1])
        else:
            # Following cars' behavior
            d = positions[i-1, t-1] - positions[i, t-1]  # Distance to the car in front
            relative_velocity = velocities[i-1, t-1] - velocities[i, t-1]  # Speed difference

            # Acceleration formula for following cars
            a = c * relative_velocity - b / max(d, 1)
            if d < 2:  # Safety check to prevent overlap
                a = -5  # Hard braking

        # Update velocity and position
        velocities[i, t] = max(0, velocities[i, t-1] + a * dt)  # Ensure non-negative velocity
        positions[i, t] = positions[i, t-1] + velocities[i, t-1] * dt + 0.5 * a * dt**2

# Plot the results
plt.figure(figsize=(12, 6))
for i in range(num_cars):
    plt.plot(np.arange(0, time_total, dt), positions[i], label=f"Car {i+1}")

plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position of Cars Over Time - Follow-the-Leader Model")
plt.legend()
plt.show()
