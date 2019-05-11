"""
Author: Ivan (Chon-Hou) Chan
This is the components constructor, coomponent can classified as
mass, connection and support.
"""
from dynamics.core import Component

class Mass(Component):
    """
    Mass object, which is the mass body for the simulation.

    Attributes:
    -----------
        mass: float
            The mass (weight) of the mass body.
        drag_coeff: float
            The coefficient of drag of the mass body.
    """

    def __init__(self, mass=1, drag_coeff=0, name=None):
        self._mass = mass
        self._drag_coeff = drag_coeff
        super().__init__(name)

    def define_properties(self):
        "Method to define properties."
        self.properties = {"name": self.name,
                           "mass": self.mass,
                           "drag_coeff": self.drag_coeff}

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
