"""
Author: Ivan (Chon-Hou) Chan
This is the core of Dynamics, which creates a structure of the dynamics
models and simulations.
"""
import numpy as np
from scipy import constants
from abc import ABCMeta, abstractmethod

class Problem(object):
    """
    This is the problem class, which is an object that
    encapsulates all problem parameters and components.

    Attributes:
        dof: int
            The degree of freedom of the dynamic model.
        initial_displacement: FixedLengthArray of float
            The inital displacement of the dynamic model.
        initial_velocity: FixedLengthArray of float
            The inital velocity of the dynamic model.
        time_step: float
            The time (numerical) increment.
        time_end: float
            The end condition of the simulation.
        reference_point: FixedLengthArray of float
            The reference point for the simulation
    """

    __metaclass__ = ABCMeta

    def __init__(self, dof=1, initial_displacement=[0],
                initial_velocity=[0], time_step=1e-4,
                time_end=100, reference_point=(0,0)):
        """
        Create a new problem.
        """
        self.dof = dof
        self.initial_displacement = initial_displacement
        self.initial_velocity = initial_velocity
        self.time_step = time_step
        self.time_end = time_end
        self.reference_point = reference_point
        self.g = constants.g

    def initialise(self, dof=None, initial_displacement=None, 
                initial_velocity=None, time_step=None,
                time_end=None, reference_point=None):
        """
        initialise the problem parameters
        """
        if dof is not None:
            self.dof = dof
        if initial_displacement is not None:
            self.initial_displacement = initial_displacement
        if initial_velocity is not None:
            self.initial_velocity = initial_velocity
        if time_step is not None:
            self.time_step = time_step
        if time_end is not None:
            self.time_end = time_end
        if reference_point is not None:
            self.reference_point = reference_point

    @abstractmethod
    def setup(self):
        raise NotImplementedError("method is not implemented.")

class DynamicModel(object):
    """
    This is the top level abstract class, which encapsulates
    all method and variable attributes for a dynamic simulation.

    DynamicModel is based on the motion of equations derived from
    Lagrangian formulation.

        matrix(M) x matrix(a) = martrix(R)
      =>matrix(a) = inv(matrix(M)) X matrix(R)

    Note: matrix(M) : Equivalent mass matrix;
          matrix(a) : acceleration matrix;
          matrix(R) : Equivalent reaction martix

    The acceleration matrix was used to construct a system 
    of 1st order equations:
        
        d[x_i, v_i]/dt = [v_i, a_i]
    
        Attribute:
            problem: object
                problem object that contains all parameters.
    """
    
    __metaclass__ = ABCMeta

    def __init__(self, problem):
        """Construct the dynamic model."""
        self.problem = problem

    def run(self):
        """Method to run the simulation."""
        
        # construct problem variable
        problem = self.problem

        # construct time array
        time = np.arange(0, problem.time_end, problem.time_step)

        # Initialise outputs arrays 
        displacement = np.zeros((problem.dof, len(time)))
        velocity = np.zeros((problem.dof, len(time)))
        for i in range(problem.dof):
            displacement[i][0] = problem.initial_displacement[i]
            velocity[i][0] = problem.initial_velocity[i]
        time_step = np.diff(time)

        # Results evaluation
        for i in range(len(time_step)):
            # Evaluate equivalent mass matrix
            M = self.calc_mass_matrix(displacement[:,i], velocity[:,i])
            # Evaluate equivalent reaction matrix 
            R = self.calc_reaction_matrix(displacement[:,i], velocity[:,i])

            # Calculate the invert of equivalent mass matrix
            if problem.dof > 1:
                M_inverted = np.linalg.inv(M)
            else:
                M_inverted = [M**-1]

            # Calculate the theta and omega for the next time step
            for j in range(problem.dof):
                displacement[j][i+1] = displacement[j][i] + velocity[j][i] * time_step[i]
                velocity[j][i+1] = velocity[j][i] + np.dot(M_inverted[j], R) * time_step[i]

        results = {
            "time" : time,
            "displacement" : displacement,
            "velocity" : velocity,
        }
        
        return results

    @abstractmethod
    def calc_mass_matrix(self, displacement, velocity):
        raise NotImplementedError("method is not implemented.")

    @abstractmethod
    def calc_reaction_matrix(self, displacement, velocity):
        raise NotImplementedError("method is not implemented.")

class Component(object):
    """
    This class is an abstract class, which creates component
    objects for the simulation.

        Attribute:
            create: callable
                method to component object.
    """
    
    def __init__(self, **kwargs):
        """Create a new component."""
        super().__init__(**kwargs)
