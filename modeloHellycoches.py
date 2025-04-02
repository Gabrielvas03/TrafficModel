import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_vehicles = 5  # Number of vehicles
street_length = 1000  # meters (visualization limit, but vehicles can exceed this)
time_steps = 200  # Increased for better visualization
dt = 0.1  # Smaller time step for better accuracy

# Traffic parameters
v_min = 0  # km/h (allowing vehicles to stop)
v_max = 60  # km/h

# Convert speeds from km/h to m/s
v_min_mps = v_min * 1000 / 3600
v_max_mps = v_max * 1000 / 3600

# Helly model parameters
alpha = 0.5  # Sensitivity to speed difference
beta = 0.2   # Sensitivity to distance difference
s0 = 10      # Desired spacing (meters)
T = 1.5      # Time headway (seconds)

# Initial positions: Vehicles start with a difference of 20 meters
positions = np.array([0 - i * 20 for i in range(num_vehicles)])

# Speeds: Random initial speeds for each vehicle within the allowed range
speeds = np.random.uniform(v_min_mps, v_max_mps, num_vehicles)

# Arrays to store positions, speeds, and accelerations over time
positions_over_time = np.zeros((time_steps, num_vehicles))
speeds_over_time = np.zeros((time_steps, num_vehicles))
accelerations_over_time = np.zeros((time_steps, num_vehicles))

positions_over_time[0, :] = positions
speeds_over_time[0, :] = speeds

# Simulation loop
for t in range(1, time_steps):
    for i in range(num_vehicles):
        # Calculate acceleration using Helly model
        if i == 0:  # Lead vehicle (no vehicle in front)
            # Lead vehicle maintains constant speed
            acceleration = 0
        else:
            # Calculate distance to vehicle ahead
            distance = positions_over_time[t-1, i-1] - positions_over_time[t-1, i]
            
            # Calculate relative speed
            delta_v = speeds_over_time[t-1, i-1] - speeds_over_time[t-1, i]
            
            # Desired distance based on current speed and time headway
            desired_distance = s0 + T * speeds_over_time[t-1, i]
            
            # Helly model acceleration
            acceleration = alpha * delta_v + beta * (distance - desired_distance)
        
        # Apply acceleration limits (optional)
        acceleration = np.clip(acceleration, -3, 2)  # m/s^2, reasonable acceleration/deceleration limits
        
        # Update speed using acceleration
        new_speed = speeds_over_time[t-1, i] + acceleration * dt
        
        # Ensure speed stays within limits
        new_speed = np.clip(new_speed, v_min_mps, v_max_mps)
        
        # Update position using new speed
        new_position = positions_over_time[t-1, i] + new_speed * dt
        
        # Store values
        accelerations_over_time[t, i] = acceleration
        speeds_over_time[t, i] = new_speed
        positions_over_time[t, i] = new_position

# Visualization
time = np.arange(time_steps) * dt

# Create a figure with 3 subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Plot positions
for i in range(num_vehicles):
    ax1.plot(time, positions_over_time[:, i], label=f"Vehicle {i + 1}")
ax1.set_ylabel("Position (m)")
ax1.set_title("Position vs. Time")
ax1.legend()
ax1.grid(True)

# Plot speeds
for i in range(num_vehicles):
    ax2.plot(time, speeds_over_time[:, i] * 3.6, label=f"Vehicle {i + 1}")  # Convert to km/h for display
ax2.set_ylabel("Speed (km/h)")
ax2.set_title("Speed vs. Time")
ax2.grid(True)

# Plot accelerations
for i in range(num_vehicles):
    ax3.plot(time, accelerations_over_time[:, i], label=f"Vehicle {i + 1}")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Acceleration (m/s²)")
ax3.set_title("Acceleration vs. Time")
ax3.grid(True)

plt.tight_layout()
plt.show()

# Bonus: Visualize vehicle spacing over time
plt.figure(figsize=(10, 6))
for i in range(1, num_vehicles):
    spacing = positions_over_time[:, i-1] - positions_over_time[:, i]
    plt.plot(time, spacing, label=f"Space between vehicles {i} and {i+1}")
plt.xlabel("Time (s)")
plt.ylabel("Spacing (m)")
plt.title("Vehicle Spacing vs. Time")
plt.legend()
plt.grid(True)
plt.show()
