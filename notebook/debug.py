from dynamics import core, creator, model
from dynamics.asset import Asset
from dynamics.tools import Body, kinectic, potentialGrav, rotation, solution
from dynamics.tools.solver import euler, improved_euler, RK2, RK4

simulation = core.Simulation()


# Double Pen
# body = creator.create('body', Body, **{'mass':1, 'drag_coeff':0, 'length':1})
# sol = solution.Solution(disp_0=3.0, velo_0=0)
# asset = Asset(**{'name': 'mass', 'var_name': 'theta', 'component': body, 'motion_func': rotation, 'solution': sol})
# sol_1 = solution.Solution(disp_0=0, velo_0=0)
# asset_1 = Asset(**{'name': 'mass', 'var_name': 'theta1', 'component': body, 'motion_func': rotation, 'solution': sol_1, 'connection': asset})

# simulation.register('model', model.Model([asset, asset_1]))
# simulation.register('solver', RK4)



# Single Pen
body = creator.create('body', Body, **{'mass':1, 'drag_coeff':0.1, 'length':1})
sol = solution.Solution(disp_0=3.0, velo_0=0)
asset = Asset(**{'name': 'mass', 'var_name': 'theta', 'component': body, 'motion_func': rotation, 'solution': sol})

simulation.register('model', model.Model(asset))
simulation.register('solver', RK4)


simulation.set_paramters(time_step=2.5e-3, time_end=5)
# simulation.set_paramters(time_step=75e-3, time_end=10)
simulation.run()


# https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-07-dynamics-fall-2009/lecture-notes/MIT16_07F09_Lec20.pdf
