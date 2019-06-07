"""This module provides a method to define the components of the nonlinear
dynamic simulation.
"""

from abc import ABCMeta, abstractmethod

from collections import defaultdict

class Component:
    """
    An Absetract component class, which is used to construct the
    components for the simulation.

    Parameters:
        name (str): Name of the component.

    +----------------+-----------------+-----------------------------+
    | Attributes     | Default         | Details                     |
    +================+=================+=============================+
    | ``name``       | None            | Name of the component.      |
    +----------------+-----------------+-----------------------------+
    | ``properties`` | defaultdict     | Properties of the component.|
    +----------------+-----------------+-----------------------------+
    """

    __metaclass__ = ABCMeta

    def __init__(self, name=None):
        self._name = name
        self.properties = defaultdict()
        self.define_properties()

    @abstractmethod
    def define_properties(self):
        "Method to define properties of the component."
        raise NotImplementedError("Method is not implemented.")

    def update_properties(self, **kwargs):
        "Method to update properties of the component."
        for key, value in kwargs.items():
            self.properties[key] = value

    @property
    def name(self):
        "Call the name property of the component."
        return self._name

    @name.setter
    def name(self, value):
        "Update the name property of the component."
        self._name = value
        self.update_properties(**{"name": self.name})

class Body(Component):
    """
    Body object, which is the mass body for the simulation.

    Parameters:
        mass (float): Mass of the body.
        drag_coeff (float): Drag coefficient.
        length (float): Length of connection.
        name (str): Name of the component.

    +----------------+-----------------+-----------------------------+
    | Attributes     | Default         | Details                     |
    +================+=================+=============================+
    | ``name``       | None            | Name of the component.      |
    +----------------+-----------------+-----------------------------+
    | ``properties`` | defaultdict     | Properties of the component.|
    +----------------+-----------------+-----------------------------+
    | ``mass``       | 1               | Mass of the component.      |
    +----------------+-----------------+-----------------------------+
    | ``drag_coeff`` | 0               | Drag coefficient.           |
    +----------------+-----------------+-----------------------------+
    | ``length``     | 1               | Length of connection.       |
    +----------------+-----------------+-----------------------------+
    TODO(IVAN): Decouple length from the mass.
    """

    def __init__(self, mass=1, drag_coeff=0, length=1, name=None):
        self._mass = mass
        self._drag_coeff = drag_coeff
        self._length = length
        super().__init__(name)

    def define_properties(self):
        "Method to define properties."
        self.properties = {"name": self.name,
                           "mass": self.mass,
                           "drag_coeff": self.drag_coeff,
                           "length": self.length}

    @property
    def mass(self):
        "Call the mass property of the body."
        return self._mass

    @mass.setter
    def mass(self, value):
        "Update the mass property of the body."
        self._mass = value
        self.update_properties(**{"mass": self.mass})

    @property
    def drag_coeff(self):
        "Call the drag coefficient property of the body."
        return self._drag_coeff

    @drag_coeff.setter
    def drag_coeff(self, value):
        "Update the drag coefficient property of the body."
        self._drag_coeff = value
        self.update_properties(**{"drag_coeff": self.drag_coeff})

    @property
    def length(self):
        "Call the length property of the connection."
        return self._length

    @length.setter
    def length(self, value):
        "Update the length property of the connection."
        self._length = value
        self.update_properties(**{"length": self.length})


class Connection(Component):
    """
    Connection object, which is the coneection between parts (components).

    Attributes:
    -----------
        length: float
            The length of the connection.
    """

    def __init__(self, length=1, name=None):
        self._length = length
        super().__init__(name)

    def define_properties(self):
        "Method to define properties."
        self.properties = {"name": self.name,
                           "length": self.length}

    @property
    def length(self):
        "Call the length property of the connection."
        return self._length

    @length.setter
    def length(self, value):
        "Update the length property of the connection."
        self._length = value
        self.update_properties(**{"length": self.length})


class Support(Component):
    """
    Support object, which is the support object for the simulation.

    Attributes:
    -----------
        position: tuple (x, y, z)
            The position (co-ordinate) of the support.
    """

    def __init__(self,
                 position=(0, 0, 0)):
        self._position = position
        super().__init__()

    def define_properties(self):
        "Method to define properties."
        self.properties = {"name": self.name,
                           "position": self.position}

    @property
    def position(self):
        "Call the position property of the support."
        return self.position

    @position.setter
    def position(self, value):
        "Update the position property of the position."
        self.position = value
        self.update_properties(**{"position": self.position})
