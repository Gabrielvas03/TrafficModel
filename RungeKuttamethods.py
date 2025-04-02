import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Given parameters for the IDM
v0 = 30  # Desired velocity (m/s)
T = 1.5  # Safe time headway (s)
a = 0.73  # Maximum acceleration (m/s^2)
b = 1.67  # Comfortable deceleration (m/s^2)
delta = 4  # Acceleration exponent
s0 = 2  # Minimum distance (m)
vehicle_length = 5  # Vehicle length (m)
num_vehicles = 50  # Number of vehicles in the ring road
ring_length = num_vehicles * (vehicle_length + 10)  # Total length of the ring road

# Define the ODE system based on IDM
def idm_system(t, y):
    positions = y[:num_vehicles]
    velocities = y[num_vehicles:]
    
    d_positions_dt = velocities
    d_velocities_dt = np.zeros(num_vehicles)
    
    for i in range(num_vehicles):
        front_index = (i - 1) % num_vehicles  # The index of the vehicle in front
        
        # Compute the actual gap s and handle the ring road condition
        s = (positions[front_index] - positions[i] - vehicle_length) % ring_length
        if s <= 0:
            s += ring_length  # Ensure the gap is positive
        
        delta_v = velocities[i] - velocities[front_index]  # Relative speed between vehicles
        
        # Desired gap function s*
        s_star = s0 + velocities[i] * T + (velocities[i] * delta_v) / (2 * np.sqrt(a * b))
        
        # IDM acceleration equation
        if s > 0:
            d_velocities_dt[i] = a * (1 - (velocities[i] / v0)**delta - (s_star / s)**2)
        else:
            d_velocities_dt[i] = -b  # Strong deceleration if vehicles are too close
    
    return np.concatenate([d_positions_dt, d_velocities_dt])

# Initial positions and velocities
initial_positions = np.linspace(0, ring_length, num_vehicles, endpoint=False)
initial_velocities = np.random.uniform(20, 30, num_vehicles)  # Initial velocities between 20 and 30 m/s
initial_conditions = np.concatenate([initial_positions, initial_velocities])

# Time span for the simulation
t_span = (0, 50)  # Simulate for 50 seconds
t_eval = np.linspace(0, 50, 1000)  # Time points for evaluation

# Solve the ODE using different Runge–Kutta methods
sol_rk1 = solve_ivp(idm_system, t_span, initial_conditions, method='RK23', t_eval=t_eval, rtol=1e-1)
sol_rk3 = solve_ivp(idm_system, t_span, initial_conditions, method='RK45', t_eval=t_eval)
sol_rk5 = solve_ivp(idm_system, t_span, initial_conditions, method='RK45', t_eval=t_eval, atol=1e-8, rtol=1e-8)

# Plot displacement over time for each method
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

methods = [('RK1', sol_rk1), ('RK3', sol_rk3), ('RK5', sol_rk5)]
for ax, (label, solution) in zip(axes, methods):
    for i in range(num_vehicles):
        ax.plot(solution.t, solution.y[i, :], label=f'Vehicle {i+1}', linewidth=0.7, alpha=0.7)
    ax.set_title(label)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Displacement (m)')

plt.tight_layout()
plt.show()
