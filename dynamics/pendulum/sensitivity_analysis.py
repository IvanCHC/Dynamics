"""
Author: Ivan (Chon-Hou) Chan

This is a script used to visualise the sensetivity of
pendulum simulation.
"""
import pylab as p
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics.pendulum.src.pendulum import Pendulum

# Construct simulation object
simulation = Pendulum(mu=0.0, l=1, terminal_condition=30, time_step=1e-5)

# Run simulation and phase portait evaluation
simulation.setup(theta_init=np.pi-1, omega_init=0)
simulation.run()
simulation.get_phase_portait()

# Extract phase portait results
omega_phase = simulation.result_phase['omega']
alpha_phase = simulation.result_phase['alpha']
# Normalise the phase portait "arrows"
M = (p.hypot(simulation.result_phase['omega'], simulation.result_phase['alpha']))
M[M == 0] = 1.                            # Avoid zero division errors 
simulation.result_phase['omega'] /= M       # Normalize each arrows
simulation.result_phase['alpha'] /= M 

# Set up for the figure
fig = plt.figure(figsize=(14,8))

# Plot the stream plot of phase portait
X, Y = np.meshgrid(simulation.result_phase['theta_input'],
                   simulation.result_phase['omega_input'])
p.streamplot(X[::5,::5], Y[::5,::5], 
    simulation.result_phase['omega'][::5,::5], 
    simulation.result_phase['alpha'][::5,::5], density=5
    )

# Visualise the results
phase, = plt.plot(simulation.result['theta'], simulation.result['omega'])

# Animation init function
def init():
    phase.set_data([], [])

    return phase

# Animation frame function
def animate(i):
    # Set up the phase position of the pendulum
    phase_theta = simulation.result['theta'][:i]
    phase_omega = simulation.result['omega'][:i]

    # Update the next frame
    phase.set_data(phase_theta, phase_omega)

    return phase

# Define animation object
ani = animation.FuncAnimation(fig, animate, np.arange(1, len(simulation.result['time']), 12),
                              interval=0, blit=True, init_func=init)

plt.show()