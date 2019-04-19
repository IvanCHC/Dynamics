import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dynamics.double_pendulum.src.double_pendulum import DoublePendulum

# Construct simulation object
simulation = DoublePendulum(dof=2, mass=(1,1), l=(1,1),
    c=(0,0), theta_init=(1,0.5), omega_init=(0,0),
    time_step=1e-4, terminal_condition=30)

# Run simulation
simulation.run()

# Exact theta and other parameters from the simulation
time = simulation.result['time']
theta = simulation.result['theta']
omega = simulation.result['omega']
length = simulation.l

plt.plot(time, theta[0])
plt.ylabel('angular displacement (rad)')
plt.xlabel('time (s)')