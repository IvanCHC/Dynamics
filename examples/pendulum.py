"""
Author: Ivan (Chon-Hou) Chan
This is a numerical simulation of pendulum.
"""
# from dynamics.core import Model, Simulation
# from dynamics.component import Mass, Connection, Support

# class PendulumModel(Model):
#     """
#     Simple pendulum dynamic model, the model is consisted of mass,
#     connection and support.

#     Components inputs must have a mass, connection and support objects. 
#     """

#     def __init__(self,
#                  components=[Mass, Connection, Support],
#                  reference=(0, 0, 0)):
#         super().__init__(componets, reference)

#     def setup(self):
#         "Setup of the pendulum dynamic model."
#         # Construct the components
#         mass = self.build_component(self.component[0])
#         connection = self.build_component(self.component[1])
#         support = self.build_component(self.component[2])

#%%
# Import all module for the simulation
from dynamics import base, creator, model
from dynamics.tools import Body, kinectic, potentialGrav, rotation
import sympy as sp
from sympy.physics.vector import dynamicsymbols

simulation = base.Simulation()

# Register mass component
# body = creator.create('body', Body, **{'mass':2, 'drag_coeff':0.1, 'length':2})
simulation.register("mass", Body, 1, 0, 1, name="test")

#%%
motion = rotation(simulation.mass().length)
a = model.Model(motion, simulation.mass())
expre = a.acceleration()
print(expre)