import numpy as np
import matplotlib.pyplot as plt

# Parameters
street_length = 1000  # meters
num_segments = 10
segment_length = street_length / num_segments
time_steps = 50

# Traffic parameters
v_min = 20  # km/h
v_max = 60  # km/h
rho_max = 30  # vehicles/km
initial_density = initial_density = np.array([10, 12, 14, 16, 18, 20, 22, 24, 26, 28])  # Fixed initial density


# Simulation arrays
densities = np.zeros((time_steps, num_segments))
speeds = np.zeros((time_steps, num_segments))
densities[0, :] = initial_density

# Update rules
def update_speed(density, v_min, v_max, rho_max):
    # Linear relationship: higher density -> lower speed
    return np.clip(v_max * (1 - density / rho_max), v_min, v_max)

def update_density(densities, speeds, segment_length, dt):
    new_densities = densities.copy()
    for i in range(1, len(densities) - 1):
        flow_in = speeds[i - 1] * densities[i - 1]
        flow_out = speeds[i] * densities[i]
        new_densities[i] += (flow_in - flow_out) * dt / segment_length
    return np.clip(new_densities, 0, rho_max)

# Simulation loop
dt = 1  # Time step in seconds
for t in range(1, time_steps):
    speeds[t - 1, :] = update_speed(densities[t - 1, :], v_min, v_max, rho_max)
    densities[t, :] = update_density(densities[t - 1, :], speeds[t - 1, :], segment_length, dt)

# Visualization
time = np.arange(time_steps)
x_positions = np.linspace(0, street_length, num_segments)

# Plot Density Evolution
for t in range(0, time_steps, 10):
    plt.plot(x_positions, densities[t, :], label=f"Time step {t}")
plt.xlabel("Street Position (m)")
plt.ylabel("Density (vehicles/km)")
plt.title("Density Evolution Along the Street")
plt.legend()
plt.show()

# Plot Speed Evolution
for t in range(0, time_steps, 10):
    plt.plot(x_positions, speeds[t, :], label=f"Time step {t}")
plt.xlabel("Street Position (m)")
plt.ylabel("Speed (km/h)")
plt.title("Speed Evolution Along the Street")
plt.legend()
plt.show()

