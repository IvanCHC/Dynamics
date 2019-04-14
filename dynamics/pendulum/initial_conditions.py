"""
Author: Ivan (Chon-Hou) Chan
This is the visual demonstration of simple pendulum model
with different initial conditions.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics.pendulum.src.pendulum import Pendulum

# Construct simulation object
model = Pendulum(mu=0.1, l=1, time_step=1e-3)

# Run simulation
for i in range
simulation.setup(theta_init=3.1, omeega_init=0)
simulation.run()

# Exact theta and other parameters from the simulation
theta = simulation.result['theta']
time = simulation.result['time']
omega = simulation.result['omega']
length = simulation.l

# Set up for the figure
fig = plt.figure(figsize=(14,8))

# Set up simulation subplot
ax = fig.add_subplot(121, autoscale_on=True, xlim=(-1.2, 1.2),
                     ylim=(-1.2, 1.2), aspect='equal')
support, = ax.plot([0, 0], [-1.2, 0], 'k--', lw=1)
position, = ax.plot([], [], 'o-', lw=2)
path, = ax.plot([], [], 'k-.', lw=1)

# Animation init function
def init():
    position.set_data([], [])
    path.set_data([], [])

    return position, path

# Animation frame function
def animate(i):
    # Set up the position of pendulum
    position_x = [0, length * np.sin(theta)]
    position_y = [0, -length * np.cos(theta)]

    # Set up the path of pendulum
    path_x = 0.2* length * np.sin(np.linspace(0,theta[i],500))
    path_y = -0.2 *length * np.cos(np.linspace(0,theta[i],500))

    # Update the next frame
    position.set_data(position_x, position_y)
    path.set_data(path_x, path_y)

    return position, path

# Define animation object
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(time), 6),
                              interval=0, blit=True, init_func=init)

plt.show()
