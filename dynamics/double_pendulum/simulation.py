import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics.double_pendulum.src.double_pendulum import DoublePendulum

# Construct simulation object
simulation = DoublePendulum(dof=2, mass=(1,1), l=(1,1),
    c=(0,0), theta_init=(2.1,-2.5), omega_init=(0,0),
    time_step=1e-4, terminal_condition=100)

# Run simulation
simulation.run()

# Exact theta and position parameters from the simulation
time = simulation.result['time']
theta = simulation.result['theta']
omega = simulation.result['omega']
length = simulation.l

# Calculate the postions
x = np.zeros(theta.shape)
y = np.zeros(theta.shape)
x[0] = length[0] * np.sin(theta[0])
y[0] = -1 * length[0] * np.cos(theta[0])
x[1] = x[0] + length[1] * np.sin(theta[1])
y[1] = y[0] - length[1] * np.cos(theta[1])

# Set up for the figure
fig = plt.figure(figsize=(14,8))

# Set up simulation subplot
ax = fig.add_subplot(121, autoscale_on=True, xlim=(-1.2*np.sum(length),
                    1.2*np.sum(length)), ylim=(-1.2*np.sum(length), 1.2*np.sum(length)),
                    aspect='equal')
support, = ax.plot([0, 0], [-1.2*np.sum(length), 0], 'k--', lw=1)
position, = ax.plot([], [], 'o-', lw=2)

# Set up the messages on the simulation plot
time_message = 'time = %.2fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# Set up result [theta] subplot
ax = fig.add_subplot(222, autoscale_on=True)
ax.grid()
theta_result_0, = ax.plot(time, theta[0])
theta_result_1, = ax.plot(time, theta[1])
plt.ylabel('angular displacement (rad)')
plt.xlabel('time (s)')

# Set up result [omega] subplot
ax = fig.add_subplot(224, autoscale_on=True)
ax.grid()
omega_result_0, = ax.plot(time, omega[0])
omega_result_1, = ax.plot(time, omega[1])
plt.ylabel('angular velocity (rad/s)')
plt.xlabel('time (s)')

# Animation init function
def init():
    position.set_data([0, x[0][0], x[1][0]], [0, y[0][0], y[1][0]])
    time_text.set_text('')
    theta_result_0.set_data(time, [np.nan] * len(time))
    omega_result_0.set_data(time, [np.nan] * len(time))
    theta_result_1.set_data(time, [np.nan] * len(time))
    omega_result_1.set_data(time, [np.nan] * len(time))
    return position, time_text, theta_result_0, omega_result_0, \
        theta_result_1, omega_result_1

# Animation frame function
def animate(i):
    # Update the next frame
    position.set_data([0, x[0][i], x[1][i]], [0, y[0][i], y[1][i]])
    time_text.set_text(time_message % (time[i]))
    theta_result_0.set_data(time[:i], theta[0][:i])
    omega_result_0.set_data(time[:i], omega[0][:i])
    theta_result_1.set_data(time[:i], theta[1][:i])
    omega_result_1.set_data(time[:i], omega[1][:i])
    return position, time_text, theta_result_0, omega_result_0, \
        theta_result_1, omega_result_1

# Define animation object
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(time), 100),
                              interval=0, blit=True, init_func=init)

plt.show()