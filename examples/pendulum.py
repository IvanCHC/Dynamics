"""
Author: Ivan (Chon-Hou) Chan
This is a numerical simulation of pendulum.
"""
#%%
# Import all module for the simulation
from dynamics import base, creator, model
from dynamics.tools import Body, kinectic, potentialGrav, rotation
from dynamics.tools.solver import euler, improved_euler, RK2, RK4
import sympy as sp
from sympy.physics.vector import dynamicsymbols
import matplotlib.pyplot as plt 

simulation = base.Simulation()

# Register mass component
# body = creator.create('body', Body, **{'mass':2, 'drag_coeff':0.1, 'length':2})
simulation.register("mass", Body, 1, 0, 1, name="test")

#%%
motion = rotation(simulation.mass().length)
a = model.Model(motion, simulation.mass())
expre = a.acceleration()
print(expre)

mass_equ = expre.coeff(dynamicsymbols('theta_ddot'))
print(mass_equ)
react_equ = -expre.subs(dynamicsymbols('theta_ddot'), 0)
print(react_equ)

#%%
# Split into systems of linear equations
s = 3.1
v = 0
t = 0
dt = 5e-3

s_rec = [s]
v_rec = [v]
t_rec = [t]


for i in range(250):
    
    s, v, t = RK4(react_equ / mass_equ, s, v, t, dynamicsymbols('theta'),
                    dynamicsymbols('theta_dot'), dt)

    s_rec.append(s)
    v_rec.append(v)
    t_rec.append(t)

plt.plot(t_rec, s_rec)
plt.show()
