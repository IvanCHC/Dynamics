#%%
# Import all module for the simulation
from dynamics import base, creator
from dynamics.tools import Body, kinectic, potentialGrav, rotation
import sympy as sp
from sympy.physics.vector import dynamicsymbols

simulation = base.Simulation()

# Register mass component
body = creator.create('body', Body, **{'mass':2, 'drag_coeff':0.1, 'length':2})
simulation.register("mass", Body, 1, 0, 1, name="test")

#%%
disp_x, disp_y, theta = rotation(simulation.mass().length)
velo_x = sp.diff(disp_x, sp.Symbol('t'))
velo_y = sp.diff(disp_y, sp.Symbol('t'))

#%%
kinectic_1 = kinectic(simulation.mass().mass, velo_x)
kinectic_2 = kinectic(simulation.mass().mass, velo_y)
T = kinectic_1 + kinectic_2
T = sp.simplify(T)
theta_dot_expr = sp.Derivative(dynamicsymbols('theta'), sp.Symbol('t'))
T = T.subs(theta_dot_expr, dynamicsymbols('theta_dot'))

#%%
potential = potentialGrav(simulation.mass().mass, disp_y)
V = sp.simplify(potential)

#%%
part_a = sp.diff(T, sp.Symbol('theta'))
part_b = sp.diff(sp.diff(T , dynamicsymbols('theta_dot'))).doit()
theta_dot_dot_expr = sp.Derivative(dynamicsymbols('theta_dot'), sp.Symbol('t'))
part_b = part_b.subs(theta_dot_dot_expr, dynamicsymbols('theta_dot_dot'))
part_c = sp.Derivative(V, dynamicsymbols('theta')).doit()

expre = part_b - part_a + part_c

print(expre)