"""The module `dynamics.model` creates the dynamic model for the system 
defined."""

from functools import reduce
from typing import TYPE_CHECKING, List

import sympy as sp
from sympy.physics.vector import dynamicsymbols

from dynamics.tools import kinectic, potentialGrav

if TYPE_CHECKING:
    from dynamics.asset import Asset

class Model:
    """A model class for evaluating the expression of motions of the system.
    The model object contains a list of tuples describing the motion of the
    system.
    """

    def __init__(self, asset: List['Asset']):
        self.asset = [asset] if not isinstance(asset, list) else asset
        
        self.direction_grav = (0, 1)
        self.time_start = 0.0
        self.time_step = 1e-3
        self.n_iter = 100
        self.results = None

    def initialise(self, direction_grav=None, time_step=None,
                   n_iter=None, time_start=None):
        """This class to initalise a set of prescribed
        motions based on the degree of freedom of the system. It should
        provide a way to generalise all energy methods."""
        if direction_grav is None:
            self.direction_grav = (0, 1)
        else:
            self.direction_grav = direction_grav
        
        if time_start is not None:
            self.time_start = time_start

        if time_step is not None:
            self.time_step = time_step
        
        if n_iter is not None:
            self.n_iter = n_iter

    def lagrangian(self):
        """Evaluate the model of sytem of motion equations."""

        T = self._kinectic_energy()
        V = self._potential_energy()

        L = T - V
        L = sp.simplify(L)

        lagrangian = []
        variables = []
        for _, asset in enumerate(self.asset):
            var_name = asset.var_name
            x_dot = self._time_derivative(dynamicsymbols(var_name))
            x_ddot = sp.Derivative(dynamicsymbols(var_name+'dot'), sp.Symbol('t'))

            dL_dx = sp.diff(L , dynamicsymbols(var_name)).doit()
            dL_dx_dot_dt = self._time_derivative(sp.diff(L , dynamicsymbols(var_name+"dot")))

            expression = dL_dx - dL_dx_dot_dt
            expression = sp.simplify(expression)
            lagrangian.append(expression)
            variables.append([var_name, x_dot, x_ddot])

        for i, lagran in enumerate(lagrangian):
            for j, variable in enumerate(variables):
                lagran = lagran.subs(variable[1], dynamicsymbols(variable[0]+"dot"))
                lagran = lagran.subs(variable[2], dynamicsymbols(variable[0]+"ddot"))
                lagrangian[i] = lagran
            lagrangian[i] = sp.simplify(lagrangian[i])

        return lagrangian
    
    def solve(self, solver):
        """Solve the model using the given solver."""
        expre = self.lagrangian()

        for i, asset in enumerate(self.asset):
            var_name = asset.var_name
            mass_equ = expre[i].coeff(dynamicsymbols(var_name+'ddot'))
            react_equ = sp.simplify(-expre[i].subs(dynamicsymbols(var_name+'ddot'), 0))
            acc = sp.simplify(react_equ / mass_equ)

            from tqdm import tqdm
            s, v, _, _ = asset.solution.initial_conditions
            t = self.time_start
            asset.solution.time = t
            for i in tqdm(range(self.n_iter)):
                s, v, t = solver(acc, s, v, t, dynamicsymbols(var_name),
                                dynamicsymbols(var_name+'dot'), self.time_step)

                s, v, t = s, v.evalf(), t            

                asset.solution.displacement.append(s)
                asset.solution.velocity.append(v)
                asset.solution.time.append(t)

    def _kinectic_energy(self):
        """Evaluate the kinetic energy term of the Lagrangian."""
        T = []
        for _, asset in enumerate(self.asset):
            for i, motion in enumerate(asset.motion):
                if asset.connection is not None:
                    motion = motion + asset.connection.motion[i]
                velo = self._time_derivative(motion)
                T.append(kinectic(asset.component.mass, velo))
        
        T = reduce((lambda x, y: x + y), T)
        T = sp.simplify(T)

        for _, asset in enumerate(self.asset):
            var_name = asset.var_name
            var_dot_exper = self._time_derivative(dynamicsymbols(var_name))
            T = T.subs(var_dot_exper, dynamicsymbols(var_name+'dot'))

        T = sp.simplify(T)
        return T

    def _potential_energy(self):
        """Evaluate the kinetic energy term of the Lagrangian."""
        V = []
        direction_grav = self.direction_grav
        for i, asset in enumerate(self.asset):
            # Gravitational potential energy
            for j, motion in enumerate(asset.motion):
                if asset.connection is not None:
                    motion = motion + asset.connection.motion[j]
                disp = (motion) * direction_grav[j]
                V.append(potentialGrav(asset.component.mass, disp))
            del disp

        V = reduce((lambda x, y: x + y), V)
        V = sp.simplify(V)

        return V

    def _time_derivative(self, expre):
        """Evaluate the time derivative of the symbolic expression.
        
        Parameters:
            expre (Symbol): Symbolic expression.

        Returns:
            deriv (Symbol): Symbolic expression of the derivative.
        """
        t = sp.Symbol("t")

        if not t in expre.free_symbols:
            raise ValueError('Variable t is not found in expersion: \
                {}'.format(expre))

        try:
            deriv = sp.Derivative(expre, t).doit()
        except Exception as err:
            print('Unxpected Dynamics Error: {}').format(err)
        else:
            return deriv

