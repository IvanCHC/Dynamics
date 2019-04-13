"""
Author: Ivan (Chon-Hou) Chan

This is a script used to visualise the results of
pendulum simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
import pylab as p
from dynamics.pendulum.pendulum import Pendulum

# Construct simulation object
simulation = Pendulum(mu=0.1, l=1)

# Run simulation and phase portait evaluation
simulation.setup(theta_init=3, omeega_init=0)
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
# Plot the stream plot of phase portait
X, Y = np.meshgrid(simulation.result_phase['theta_input'],
                   simulation.result_phase['omega_input'])
p.streamplot(X[::5,::5], Y[::5,::5], 
    simulation.result_phase['omega'][::5,::5], 
    simulation.result_phase['alpha'][::5,::5], density=5
    )

# Visualise the results
plt.plot(simulation.result['theta'], simulation.result['omega'])
plt.show()