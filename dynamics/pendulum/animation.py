import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics.pendulum.pendulum import Pendulum

# Construct simulation object
simulation = Pendulum(mu=0.1, l=1, time_step=1e-3)

# Run simulation
simulation.setup(theta_init=3, omeega_init=0)
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
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=True, xlim=(-1.2, 1.2),
                     ylim=(-1.2, 1.2), aspect='equal')
line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.2fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
omega_template = 'velocity = %.3frad/s'
omega_text = ax.text(0.05, 0.85, '', transform=ax.transAxes)

# Animation init function
def init():
    line.set_data([], [])
    time_text.set_text('')
    omega_text.set_text('')
    return line, time_text, omega_text

# Animation frame function
def animate(i):
    thisx = [0, x[i]]
    thisy = [0, y[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (time[i]))
    omega_text.set_text(omega_template % (omega[i]))
    return line, time_text, omega_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y), 10),
                              interval=0, blit=True, init_func=init)

plt.show()
