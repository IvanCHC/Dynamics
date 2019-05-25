""" The module `dynamics.base` provides basic structure for building nonlinear
dynamics simulations. This module contains a class `dynamics.base.Simulation`
to store simulation model, components and solver; and a virtual class
`dynamics.base.Results` for the results of the simulation. """

import sys

from functools import partial

class Simulation:
    """A simulation class for nonlinear dynamics that contains model, solver
    and componets. At first the simulation object contains a method
    `dynamics.Simulation.map` method that applies the function to every items
    of the iterables.

    Users can extend the simulation class with any other function by using
    the method `dynamics.base.Simulation.register`.
    """

    def __init__(self):
        self.register("map", map)

    def register(self, alias, function, *args, **kwargs):
        """Register (/extend) the given *function* in the simulation object under
        the given name *alias*.

        Parameters:
            alias (str): The name of function will take in the simulation object.
                         If the alias has already existed, the new one will overwrite
                         the old one.
            function (method): The function which alias is referring to.
            argument (~): Argument(s) and keyword argument(s) that would pass to the
                          registered function when called.
        
        The registered function `rfunc` would have attribute `__name__` same as
        alias and attribute `__doc__` same as the function's documentation.
        Similarily, if the function has attribure `__dict__`, the registered
        function will also be updated.
        """
        rfunc = partial(function, *args, **kwargs)
        rfunc.__name__ = alias
        rfunc.__doc__ = function.__doc__

        if hasattr(function, "__dict__") and not isinstance(function, type):
            rfunc.__dict__.update(function.__dict__.copy())

        setattr(self, alias, rfunc)

    def unregister(self, alias):
        """Decouple (/remove) alias and function from the simulation.

        Parameters:
            alias (str): The name of function will remove from simulation.
        """
        delattr(self, alias)
        