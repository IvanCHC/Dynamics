from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

import numpy as np
import sympy as sp
from sympy.physics.vector import dynamicsymbols

if TYPE_CHECKING:
    from dynamics.tools import Body, Solution

@dataclass
class Asset:
    """An asset data class for the storage of motion, object, and solution of
    an asset. This data class also contians info about the asset relative to
    the simulation, e.g. connection and relative position.
    """
    name: str
    var_name: str
    component: 'Body'
    solution: 'Solution'
    motion_func: callable
    connection: Optional['Asset'] = None

    @property
    def motion(self):
        return self.motion_func(self.component.length, self.var_name)

    @property
    def results(self):
        x_sym, y_sym = self.motion
        x_func = sp.lambdify(dynamicsymbols(self.var_name), x_sym, 'numpy')
        y_func = sp.lambdify(dynamicsymbols(self.var_name), y_sym, 'numpy')
        result_dict = {}
        result_dict['x'] = x_func(np.array(self.solution.displacement, dtype=np.float64))
        result_dict['y'] = y_func(np.array(self.solution.displacement, dtype=np.float64))
        result_dict[self.var_name] = self.solution.displacement
        result_dict[self.var_name+'dot'] = self.solution.velocity
        result_dict['time'] = self.solution.time
        return result_dict