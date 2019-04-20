"""
Author: Ivan (Chon-Hou) Chan
This is the component constructor, which creates components for simulations.
"""
import numpy as np
from dynamics.core import Component

class Mass(Component):
    """
    Mass object, which is the main mass body for the simulation.

        Attribute:
            _mass: float
                The mass (weight) of the mass object.
    """

    def __init__(self, mass=1, drag_coeff=0, **kwargs):
        """Create a new mass component."""
        super().__init__(**kwargs)
        self._mass = mass
        self._drag_coeff = drag_coeff

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value

    @property
    def drag_coeff(self):
        return self._drag_coeff
    
    @drag_coeff.setter
    def drag_coeff(self, value):
        self._drag_coeff = value

class String(Component):
    """
    Connection object, which is used to connect the main mass bodies together
    for the simulation, this connection objection is assumed to be massless,
    and with infinite stiffness.

        Attribute:
            _length: float
                The length of the connection.
            _drag_coeff: float
                The drag coefficient of the connection.
    """

    def __init__(self, length=1, *args, **kwargs):
        """Create a new string component."""
        super().__init__(*args, **kwargs)
        self._length = length

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

class SpringDamper(String):
    """
    This is the extension of String class. However, this connection component
    is assumed to have stiffness constant and damping coefficient.

        Attribute:
            length: float
                The length of the connection.
            stiffness_constant: float
                The stiffness constant of the connection.
            c: float
                The damping coefficient of the connection.
    """

    def __init__(self, length=1, stiffness_constant=1,
        damping_coeff=0, *args, **kwargs):
        """Create a new string component."""
        super().__init__(length, *args, **kwargs)
        self._stiffness_constant = stiffness_constant
        self._damping_coeff = damping_coeff

    @property
    def stiffness_constant(self):
        return self._stiffness_constant

    @stiffness_constant.setter
    def stiffness_constant(self, value):
        self._stiffness_constant = value

    @property
    def damping_coeff(self):
        return self._damping_coeff

    @damping_coeff.setter
    def damping_coeff(self, value):
        self._damping_coeff = value