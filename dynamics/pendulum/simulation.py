"""
Author: Ivan (Chon-Hou) Chan
This is the full simulation of simple pendulum model.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics.pendulum.src.pendulum import Pendulum

# Construct simulation object
simulation = Pendulum(mu=0.1, l=1, terminal_condidtion=15, time_step=1e-4)

# Run simulation
simulation.setup(theta_init=2.9, omega_init=0)
simulation.run()

# Exact theta and other parameters from the simulation
theta = simulation.result['theta']
time = simulation.result['time']
omega = simulation.result['omega']
length = simulation.l

# Calculate the postion of the pendulum
x = length * np.sin(theta)
y = -length * np.cos(theta)

# Set up for the figure
fig = plt.figure(figsize=(14,8))

# Set up simulation subplot
ax = fig.add_subplot(121, autoscale_on=True, xlim=(-1.2*length, 1.2*length),
                     ylim=(-1.2*length, 1.2*length), aspect='equal')
support, = ax.plot([0, 0], [-1.2*length, 0], 'k--', lw=1)
position, = ax.plot([], [], 'o-', lw=2)
path, = ax.plot([], [], 'k-.', lw=1)
direction = ax.quiver([0], [0], [1e-16], [1e-16], color='maroon', scale=1)


# Set up the messages on the simulation plot
time_message = 'time = %.2fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
theta_message = 'displacement = %.3frad'
theta_text = ax.text(0.05, 0.8, '', transform=ax.transAxes)
omega_message = 'velocity = %.3frad/s'
omega_text = ax.text(0.05, 0.85, '', transform=ax.transAxes)

# Set up result [theta] subplot
ax = fig.add_subplot(222, autoscale_on=True)
ax.grid()
theta_result, = ax.plot(time, theta)
plt.ylabel('angular displacement (rad)')
plt.xlabel('time (s)')

# Set up result [omega] subplot
ax = fig.add_subplot(224, autoscale_on=True)
ax.grid()
omega_result, = ax.plot(time, omega)
plt.ylabel('angular velocity (rad/s)')
plt.xlabel('time (s)')

# Animation init function
def init():
    position.set_data([], [])
    path.set_data([], [])
    direction.set_offsets([])
    direction.set_UVC([], [])
    theta_result.set_data(time, [np.nan] * len(time))
    omega_result.set_data(time, [np.nan] * len(time))
    time_text.set_text('')
    theta_text.set_text('')
    omega_text.set_text('')
    return position, path, theta_result, omega_result, \
           time_text, theta_text, omega_text, direction

# Animation frame function
def animate(i):
    # Set up the position of pendulum
    position_x = [0, x[i]]
    position_y = [0, y[i]]

    # Set up the path of pendulum
    path_x = 0.2* length * np.sin(np.linspace(0,theta[i],500))
    path_y = -0.2 *length * np.cos(np.linspace(0,theta[i],500))

    # Set up the direction of motion
    direction_x = 0.03 * omega[i] * length * np.sin(theta[i]-np.pi/2)
    direction_y = -0.03 * omega[i] * length * np.cos(theta[i]-np.pi/2)

    # Set up the results
    time_i = time[:i]
    theta_i = theta[:i]
    omega_i = omega[:i]

    # Update the next frame
    position.set_data(position_x, position_y)
    path.set_data(path_x, path_y)
    direction.set_offsets(np.column_stack([position_x[-1], position_y[-1]]))
    direction.set_UVC(direction_x, direction_y)
    theta_result.set_data(time_i, theta_i)
    omega_result.set_data(time_i, omega_i)
    time_text.set_text(time_message % (time[i]))
    theta_text.set_text(theta_message % (theta[i]))
    omega_text.set_text(omega_message % (omega[i]))
    return position, path, theta_result, omega_result, \
           time_text, theta_text, omega_text, direction

# Define animation object
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y), 600),
                              interval=0, blit=True, init_func=init)

plt.show()
