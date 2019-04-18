"""
Author: Ivan (Chon-Hou) Chan
This is the full simulation of spring-damper model.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics.spring_damper.src.spring_damper import SpringDamper

# Construct simulation object
simulation = SpringDamper(m=1, c=0.0, k=1, terminal_condition=15, 
                time_step=1e-4, l=1)

# Run simulation
simulation.setup(x_init=0.1, v_init=0)
simulation.run()

# Exact parameters from the simulation
x = simulation.result['x']
v = simulation.result['v']
time = simulation.result['time']
length = simulation.l

# Set up for the figure
fig = plt.figure(figsize=(14,8))

# Set up simulation subplot
ax = fig.add_subplot(121, autoscale_on=True, 
                    xlim=(0, 1.2*(length+np.max(x))),
                    ylim=(-1, 1), aspect='equal')
position, = ax.plot([], [], 'o-', lw=2)

# Set up the messages on the simulation plot
time_message = 'time = %.2fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
x_message = 'displacement = %.3fm'
x_text = ax.text(0.05, 0.8, '', transform=ax.transAxes)
v_message = 'velocity = %.3fm/s'
v_text = ax.text(0.05, 0.85, '', transform=ax.transAxes)

# Set up the result [x] subplot
ax = fig.add_subplot(222, autoscale_on=True)
ax.grid()
x_result, = ax.plot(time, x)
plt.ylabel('displacement (m)')
plt.xlabel('time (s)')

# Set up the result [x] subplot
ax = fig.add_subplot(224, autoscale_on=True)
ax.grid()
v_result, = ax.plot(time, v)
plt.ylabel('velocity (m/s)')
plt.xlabel('time (s)')

# Animation init function
def init():
    position.set_data([], [])
    x_result.set_data([], [])
    v_result.set_data([], [])
    time_text.set_text('')
    x_text.set_text('')
    v_text.set_text('')
    return position, time_text, x_text, v_text, \
            x_result, v_result

# Animation frame function
def animate(i):
    # Set up the position of pendulum
    position_x = [0, length+x[i]]
    position_y = [0, 0]

    # Set up the results
    time_i = time[:i]
    x_i = x[:i]
    v_i = v[:i]

    # Update the next frame
    position.set_data(position_x, position_y)
    x_result.set_data(time_i, x_i)
    v_result.set_data(time_i, v_i)
    time_text.set_text(time_message % (time[i]))
    x_text.set_text(x_message % (x[i]))
    v_text.set_text(v_message % (v[i]))
    return position, time_text, x_text, v_text, \
            x_result, v_result

# Define animation object
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(x), 600),
                              interval=0, blit=True, init_func=init)

plt.show()

