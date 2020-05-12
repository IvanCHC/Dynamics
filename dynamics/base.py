""" The module `dynamics.base` provides basic structure for building nonlinear
dynamics simulations. This module contains a class `dynamics.base.Simulation`
to store simulation model, components and solver; and a virtual class
`dynamics.base.Results` for the results of the simulation. """

from functools import partial
import sys

from dynamics.tools.solver import euler
from utils import DynamicsError, SimulationParametersNotDefinedError

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
        self.register("model", None)
        self.register("solver", euler)
        self.register("results", None)
        self.register("_parameters", False)

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
        rfunc = None

        if isinstance(function, type):
            rfunc = partial(function, *args, **kwargs)
            rfunc.__name__ = alias
            rfunc.__doc__ = function.__doc__

            if hasattr(function, "__dict__") and not isinstance(function, type):
                rfunc.__dict__.update(function.__dict__.copy())

        if rfunc is not None:
            setattr(self, alias, rfunc)
        else:
            setattr(self, alias, function)

    def unregister(self, alias):
        """Decouple (/remove) alias and function from the simulation.

        Parameters:
            alias (str): The name of function will remove from simulation.
        """
        delattr(self, alias)

    def run(self):
        """Run the simulation for the given model and solver, the results are store
        in attribute `results`."""
        if self._parameters == False:
            raise SimulationParametersNotDefinedError(
                    """Please use set_parameters method to set parameters before
                    running the simulation."""
                )
        elif self.model is None:
            raise DynamicsError("Missing model!! Please register model.")
        elif self.solver is None:
            raise DynamicsError("Missing solver!!! Please register solver.")

        self.model.initialise(time_step=self.time_step, time_start=self.time_start,
                              n_iter=self.n_iter)
        self.model.solve(self.solver)
        self.results = self.model.get_results()

    def set_paramters(self, time_step: float = 1e-3,
                      time_start: float = 0.0, time_end: float = 2.0):
        """Set the simulation parameters."""
        self.time_step, self.time_start, self.time_end = time_step, time_start, time_end
        self.n_iter = int((time_end - time_start) / time_step)
        self._parameters = True
