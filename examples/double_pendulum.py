"""
Author: Ivan (Chon-Hou) Chan
This is a numerical solution of double pendulum.
"""
import numpy as np
from dynamics.core import Problem, DynamicModel
from dynamics.component import Mass, String
from dynamics.solver import *

class DoublePendulumProblem(Problem):
    """Extended Class from Problem class."""

    def __init__(self, dof=1, initial_displacement=[0],
                initial_velocity=[0], time_step=1e-4,
                time_end=100, reference_point=[0,0]):
        "Create pendulum problem class."
        super().__init__(dof, initial_displacement, 
                initial_velocity, time_step,
                time_end, reference_point)

    def setup(self):
        self.body_1 = Mass(mass=1, drag_coeff=0)
        self.body_2 = Mass(mass=1, drag_coeff=0)
        self.connection_1 = String(length=1)
        self.connection_2 = String(length=1)

class DoublePendulumModel(DynamicModel):
    """Extended Class from DynamicModel class."""

    def calc_mass_matrix(self, displacement, velocity):
        """Function to calculate the mass matrix."""
        # Evaluate mass matrix component
        M_11 = (self.problem.body_1.mass + self.problem.body_2.mass) * \
            self.problem.connection_1.length**2
        M_12 = self.problem.body_2.mass * self.problem.connection_1.length * \
            self.problem.connection_2.length * np.cos(displacement[0] - displacement[1])
        M_21 = self.problem.body_2.mass * self.problem.connection_1.length * \
            self.problem.connection_2.length * np.cos(displacement[0] - displacement[1])
        M_22 = self.problem.body_2.mass * self.problem.connection_2.length**2

        return np.array([[M_11, M_12], [M_21, M_22]])

    def calc_reaction_matrix(self, displacement, velocity):
        """Function to calculate the reaction matrix."""
        # Evaluare reaction matrix component
        R_1 = -1 * ((self.problem.body_1.mass + self.problem.body_2.mass) * 
            self.problem.connection_1.length * self.problem.g *
            np.sin(displacement[0]) + self.problem.body_2.mass * 
            self.problem.connection_1.length * self.problem.connection_2.length *
            velocity[1]**2 * np.sin(displacement[0] - displacement[1]) + 
            self.problem.body_1.drag_coeff * velocity[0] +
            self.problem.body_2.drag_coeff * (velocity[0] - velocity[1]))
        R_2 = -1 * (self.problem.body_2.mass * self.problem.connection_2.length *
            self.problem.g * np.sin(displacement[1]) - self.problem.body_2.mass *
            self.problem.connection_1.length * self.problem.connection_2.length *
            velocity[0]**2 * np.sin(displacement[0] - displacement[1]) + 
            self.problem.body_2.drag_coeff * (velocity[1] - velocity[0]))

        return np.array([R_1, R_2])

if __name__ == "__main__":
    
    problem = DoublePendulumProblem()
    problem.initialise(dof=2, initial_displacement=[2.7, -1.5],
        initial_velocity=[0, 0], time_step=100e-4, time_end=15,
        reference_point=(0,0))
    problem.setup()


    solver = RungeKuttafour()

    simulation = DoublePendulumModel(problem, solver)
    
    simulation.problem.connection_1.length = 3
    simulation.problem.connection_2.length = 3
    
    result = simulation.run()

    import matplotlib.pyplot as plt
    plt.plot(result['time'], result['displacement'][0])
    plt.show()