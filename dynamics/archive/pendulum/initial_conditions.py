"""
Author: Ivan (Chon-Hou) Chan
This is the visual demonstration of simple pendulum model
with different initial conditions.
"""
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics.pendulum.src.pendulum import Pendulum

# Construct simulation object
model = Pendulum(mu=0.0, l=1, time_step=4e-4, terminal_condition=30)

# Set up a range of initial theta
theta_init = np.linspace(0.0, 2.7, 5)

# Initialise variables
simulation = {}
theta = {}
time = {}
omega = {}
length = {}

# Run simulation
for i in range(len(theta_init)):
    simulation[i] = copy.deepcopy(model)
    simulation[i].setup(theta_init=theta_init[i], omega_init=0)
    simulation[i].run()

# Exact theta and other parameters from the simulation
for i in range(len(simulation)):
    theta[i] = simulation[i].result['theta']
    time[i] = simulation[i].result['time']
    omega[i] = simulation[i].result['omega']
    length[i] = simulation[i].l

# Set up for the figure
fig = plt.figure(figsize=(16,6))


# Set up simulation subplot
ax = fig.add_subplot(1, len(simulation), 1, autoscale_on=True,
                    xlim=(-1.2*length[0], 1.2*length[0]),
                    ylim=(-1.2*length[0], 1.2*length[0]),
                    aspect='equal')
support_0, = ax.plot([0, 0], [-1.2*length[0], 0], 'k--', lw=1)
position_0, = ax.plot([], [], 'o-', lw=2)
path_0, = ax.plot([], [], 'k-.', lw=1)
plt.title('Initial theta = %.3frad' % theta_init[0])

ax = fig.add_subplot(1, len(simulation), 2, autoscale_on=True,
                    xlim=(-1.2*length[1], 1.2*length[1]),
                    ylim=(-1.2*length[1], 1.2*length[1]),
                    aspect='equal')
support_1, = ax.plot([0, 0], [-1.2*length[1], 0], 'k--', lw=1)
position_1, = ax.plot([], [], 'o-', lw=2)
path_1, = ax.plot([], [], 'k-.', lw=1)
plt.title('Initial theta = %.3frad' % theta_init[1])

ax = fig.add_subplot(1, len(simulation), 3, autoscale_on=True,
                    xlim=(-1.2*length[2], 1.2*length[2]),
                    ylim=(-1.2*length[2], 1.2*length[2]),
                    aspect='equal')
support_2, = ax.plot([0, 0], [-1.2*length[2], 0], 'k--', lw=1)
position_2, = ax.plot([], [], 'o-', lw=2)
path_2, = ax.plot([], [], 'k-.', lw=1)
plt.title('Initial theta = %.3frad' % theta_init[2])

ax = fig.add_subplot(1, len(simulation), 4, autoscale_on=True,
                    xlim=(-1.2*length[3], 1.2*length[3]),
                    ylim=(-1.2*length[3], 1.2*length[3]),
                    aspect='equal')
support_3, = ax.plot([0, 0], [-1.2*length[3], 0], 'k--', lw=1)
position_3, = ax.plot([], [], 'o-', lw=2)
path_3, = ax.plot([], [], 'k-.', lw=1)
plt.title('Initial theta = %.3frad' % theta_init[3])

ax = fig.add_subplot(1, len(simulation), 5, autoscale_on=True,
                    xlim=(-1.2*length[4], 1.2*length[4]),
                    ylim=(-1.2*length[4], 1.2*length[4]),
                    aspect='equal')
support_4, = ax.plot([0, 0], [-1.2*length[4], 0], 'k--', lw=1)
position_4, = ax.plot([], [], 'o-', lw=2)
path_4, = ax.plot([], [], 'k-.', lw=1)
plt.title('Initial theta = %.3frad' % theta_init[4])

# Animation init function
def init():
    position_0.set_data([], [])
    path_0.set_data([], [])

    position_1.set_data([], [])
    path_1.set_data([], [])

    position_2.set_data([], [])
    path_2.set_data([], [])
    
    position_3.set_data([], [])
    path_3.set_data([], [])
    
    position_4.set_data([], [])
    path_4.set_data([], [])

    return position_0, path_0, position_1, path_1, position_2, path_2, \
        position_3, path_3, position_4, path_4


position_x = {}
position_y = {}
path_x = {}
path_y = {}
# Animation frame function
def animate(i):
    for key in range(len(theta_init)):
        # Set up the position of pendulum
        position_x[key] = [0, length[key] * np.sin(simulation[key].result['theta'][i])]
        position_y[key] = [0, -length[key] * np.cos(simulation[key].result['theta'][i])]

        # Set up the path of pendulum
        path_x[key] = 0.2 * length[key] * np.sin(np.linspace(0,simulation[key].result['theta'][i],500))
        path_y[key] = -0.2 * length[key] * np.cos(np.linspace(0,simulation[key].result['theta'][i],500))

    # Update the next frame
    position_0.set_data(position_x[0], position_y[0])
    path_0.set_data(path_x[0], path_y[0])
    position_1.set_data(position_x[1], position_y[1])
    path_1.set_data(path_x[1], path_y[1])
    position_2.set_data(position_x[2], position_y[2])
    path_2.set_data(path_x[2], path_y[2])
    position_3.set_data(position_x[3], position_y[3])
    path_3.set_data(path_x[3], path_y[3])
    position_4.set_data(position_x[4], position_y[4])
    path_4.set_data(path_x[4], path_y[4])

    return position_0, path_0, position_1, path_1, position_2, path_2, \
        position_3, path_3, position_4, path_4

# Define animation object
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(time[0]), 80),
                              interval=0, blit=True, init_func=init)

plt.show()
