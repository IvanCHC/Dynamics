"""
Author: Ivan (Chon-Hou) Chan
This is a numerical solution of pendulum.
"""
import numpy as np
from dynamics.core import Problem, DynamicModel
from dynamics.component import Mass, String
from dynamics.solver import *

class PendulumProblem(Problem):
    """Extended Class from Problem class."""

    def __init__(self, dof=1, initial_displacement=[0],
                initial_velocity=[0], time_step=1e-4,
                time_end=100, reference_point=[0,0]):
        "Create pendulum problem class."
        super().__init__(dof, initial_displacement, 
                initial_velocity, time_step,
                time_end, reference_point)

    def setup(self):
        self.body = Mass(mass=1, drag_coeff=0)
        self.connection = String(length=1)

class PendulumModel(DynamicModel):
    """Extended Class from DynamicModel class."""

    def calc_mass_matrix(self, displacement, velocity):
        return self.problem.body.mass

    def calc_reaction_matrix(self, displacement, velocity):
        problem = self.problem
        return -1 * (problem.g/problem.connection.length * np.sin(displacement) + \
            problem.body.drag_coeff * velocity)

if __name__ == "__main__":
    
    problem = PendulumProblem()
    problem.initialise(dof=1, initial_displacement=[2.7],
        initial_velocity=[0], time_step=1e-3, time_end=30,
        reference_point=(0,0))
    problem.setup()

    solver = RungeKuttatwo()

    simulation = PendulumModel(problem, solver)
    result = simulation.run()

    import matplotlib.pyplot as plt
    plt.plot(result['time'], result['displacement'][0])
    plt.show()
