"""
Author: Ivan (Chon-Hou) Chan
This is the core of Dynamics, which is consisted of four
different modules: Model, Simulation, Components and
Solver.
"""
from abc import ABCMeta, abstractmethod
# import numpy as np
# from scipy import constants
# import sympy

class Model:
    """
    This is the abstract class for building `model` of the dynamic simulation
    using the list of user defined components.

    Note: Default gravity is acting on the vertical (Z) direction, i.e. (0, 0, -g).
          Any change of frame of reference may result in the gravity definition.

    Attributes:
    -----------
        components: list
            The components of the user defined dynamic model. Each component can be
            a tuple `(component, kwargs, component_name)` or an class `component`.
            Whereas, if the component is the class attribute, component name is the name
            of the component and the kwargs are the user define settings for the components.
        reference: tuple
            Co-ordinate of the reference component, the default value is (0, 0, 0).
    """

    __metaclass__ = ABCMeta

    def __init__(self,
                 components=None,
                 reference=(0, 0, 0)):
        self.components = components if isinstance(components, list) else [components]
        self.reference = reference

    @abstractmethod
    def setup(self):
        "Setup"
        raise NotImplementedError("Method is not implemented.")

    @abstractmethod
    def build(self):
        "Build"
        raise NotImplementedError("Method is not implemented.")


class Simulation:
    """
    This is the abstract class for simulation, simulation uses numerical solver to
    perform computation. The motion of equations are derived using Lagrangian formulation
    and symbollic toolbox library.

    Attributes:
    -----------
        model:
            The dynamic model with defined components.
        solver:
            The numerical solver of simulation.
    """

    __metaclass__ = ABCMeta

    def __init__(self,
                 problem=None,
                 solver=None):
        self.problem = problem
        self.solver = solver

    @abstractmethod
    def calc_mass_matrix(self, displacement, velocity):
        "mass matrix"
        raise NotImplementedError("Method is not implemented.")

    @abstractmethod
    def calc_reaction_matrix(self, displacement, velocity):
        "reaction matrix"
        raise NotImplementedError("Method is not implemented.")


class Component:
    """
    This class is an abstract class, which creates component
    objects for the simulation.

    Attributes:
    -----------
    properties: dict
            The dictionart of properties for the component object.
    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.properties = {}
        self.define_properties()

    @abstractmethod
    def define_properties(self):
        "Method to define properties of the component."
        raise NotImplementedError("Method is not implemented.")

    def update_properties(self, **kwargs):
        "Method to update properties of the component."
        for key, value in kwargs.items():
            self.properties[key] = value

class Solver:
    """
    This class is an abstract class, which is the numerical solver for the simulation.

    Attributes:
    -----------
        time_step: float
            The numerical increment for the solver.
        dof: int
            The degree of freedom of the numerical system.
    """

    __metaclass__ = ABCMeta

    def __init__(self, time_step, dof):
        self.time_step = time_step
        self.dof = dof

    @abstractmethod
    def solve(self):
        "solve"
        raise NotImplementedError("method is not implemented.")
