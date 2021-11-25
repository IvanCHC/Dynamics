import matplotlib.pyplot as plt 

from dynamics import core, creator, model
from dynamics.asset import Asset
from dynamics.tools import Body, rotation, solution
from dynamics.tools.solver import RK4

simulation = core.Simulation()

body = creator.create('body', Body, **{'mass':1, 'drag_coeff':0.4, 'length':1})
sol = solution.Solution(disp_0=3.12, velo_0=0)
asset = Asset(**{'name': 'mass', 'var_name': 'theta', 'component': body, 'motion_func': rotation, 'solution': sol})

simulation.register('model', model.Model(asset))
simulation.register('solver', RK4)

simulation.set_paramters(time_step=25e-4, time_end=15)
simulation.run()

solu = simulation.results
plt.plot(solu['time'], solu['displacement'])
plt.plot(solu['time'], solu['velocity'])
plt.show()
