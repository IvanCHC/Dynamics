"""The module `dynamics.model` creates the dynamic model for the system
defined."""

from functools import reduce
from typing import TYPE_CHECKING, List

import pandas as pd
import numpy as np
import sympy as sp
from sympy.physics.vector import dynamicsymbols
from tqdm import tqdm

from dynamics.tools import kinectic, potentialGrav, dissipated

if TYPE_CHECKING:
    from dynamics.asset import Asset

class Model:
    """A model class for evaluating the expression of motions of the system.
    The model object contains a list of Asset describing the motion of the
    system.
    """

    def __init__(self, asset: List['Asset']) -> None:
        self.asset = [asset] if not isinstance(asset, list) else asset
        self.direction_grav = (0, 1)
        self.time_start = 0.0
        self.time_step = 1e-3
        self.n_iter = 100
        self.results = None

    def initialise(self, direction_grav=None, time_step=None,
                   n_iter=None, time_start=None) -> None:
        """This class to initalise a set of prescribed
        motions based on the degree of freedom of the system. It should
        provide a way to generalise all energy methods."""
        if direction_grav:
            self.direction_grav = direction_grav
        else:
            self.direction_grav = (0, 1)

        if time_start:
            self.time_start = time_start

        if time_step:
            self.time_step = time_step

        if n_iter:
            self.n_iter = n_iter

    def acceleration(self):
        """Evaluate the model of sytem of motion equations."""
        L = self.lagrangian()
        D = self._dissipation()

        equations = []
        variables = []
        for asset in self.asset:
            var_name = asset.var_name
            x_dot = self._time_derivative(dynamicsymbols(var_name))
            x_ddot = sp.Derivative(dynamicsymbols(var_name+'dot'), sp.Symbol('t'))

            dL_dx = sp.diff(L , dynamicsymbols(var_name)).doit()
            dL_dx_dot_dt = self._time_derivative(sp.diff(L , dynamicsymbols(var_name+"dot")))
            dD_dx_dot = sp.diff(D , dynamicsymbols(var_name+"dot")).doit()

            expression = dL_dx_dot_dt - dL_dx - dD_dx_dot
            expression = sp.simplify(expression)
            equations.append(expression)
            variables.append([var_name, x_dot, x_ddot])

        for i, accel in enumerate(equations):
            for variable in variables:
                accel = accel.subs(variable[1], dynamicsymbols(variable[0]+"dot"))
                accel = accel.subs(variable[2], dynamicsymbols(variable[0]+"ddot"))
                equations[i] = accel
            equations[i] = sp.simplify(equations[i])

        return equations

    def solve(self, solver):
        """Solve the model using the given solver and direct numerical method, the system of
        equations are considered as `[M] x [A] = [R]`, where [M] is the mass equalavent
        matrix and [R] is the reaction equalavent matrix. Hence, acceleration can be solved
        by [A] = inv([M]) x [R]."""
        expre = self.acceleration()

        var_names, acc_symbols, vel_symbols, dis_symbols = [], [], [], []
        s, v, t = [], [], self.time_start
        for asset in self.asset:
            var_names.append(asset.var_name)
            acc_symbols.append(dynamicsymbols(asset.var_name+'ddot'))
            vel_symbols.append(dynamicsymbols(asset.var_name+'dot'))
            dis_symbols.append(dynamicsymbols(asset.var_name))
            x, dx, _, _ = asset.solution.initial_conditions
            s.append(x)
            v.append(dx)
        s = np.array(s, dtype=np.float64)
        v = np.array(v, dtype=np.float64)

        mass_matrix, react_matrix = [], []
        for accel_expre in expre:
            mass_row = []
            react_row = accel_expre
            for acc_symbol in acc_symbols:
                mass_row.append(accel_expre.coeff(acc_symbol))
                react_row = sp.simplify(react_row.subs(acc_symbol, 0))
            mass_matrix.append(mass_row)
            react_matrix.append(react_row)
        mass_matrix = sp.Matrix(mass_matrix).inv()
        react_matrix = sp.Matrix(react_matrix)

        acc_matrix = mass_matrix*react_matrix
        acc_matrix = sp.simplify(acc_matrix)

        acc_matrix = [sp.lambdify([dis_symbols, vel_symbols], acc) for acc in acc_matrix]

        for i in tqdm(range(self.n_iter)):
            s, v, a, time = solver(acc_matrix, s, v, t, self.time_step)
            self._update_asset(s, v, a, time)
            if i == 0:
                self._update_asset_initial_acceleration(a)
            t = time

    def get_results(self):
        """Get results from the assets."""
        for i, asset in enumerate(self.asset):
            if i == 0:
                results_df = asset.results
            if i != 0:
                data = asset.results
                results_df = pd.concat([results_df, data])
        return results_df

    def lagrangian(self):
        """Evaluate the lagrangian of the model."""
        T = self._kinectic_energy()
        V = self._potential_energy()
        return sp.simplify(T - V)

    def _kinectic_energy(self):
        """Evaluate the kinetic energy term of the Lagrangian."""
        T = []
        for asset in self.asset:
            for i, motion in enumerate(asset.motion):
                if asset.connection is not None:
                    motion = motion + asset.connection.motion[i]
                velo = self._time_derivative(motion)
                T.append(kinectic(asset.component.mass, velo))

        T = sp.simplify(reduce((lambda x, y: x + y), T))

        for asset in self.asset:
            var_name = asset.var_name
            var_dot_exper = self._time_derivative(dynamicsymbols(var_name))
            T = T.subs(var_dot_exper, dynamicsymbols(var_name+'dot'))

        return sp.simplify(T)

    def _potential_energy(self):
        """Evaluate the kinetic energy term of the Lagrangian."""
        V = []
        direction_grav = self.direction_grav
        for asset in self.asset:
            # Gravitational potential energy
            for i, motion in enumerate(asset.motion):
                if asset.connection is not None:
                    motion = motion + asset.connection.motion[i]
                disp = - (motion) * direction_grav[i]
                V.append(potentialGrav(asset.component.mass, disp))
            del disp

        return sp.simplify(reduce((lambda x, y: x + y), V))

    def _dissipation(self):
        """Evaluate the Rayleigh dissipation term."""
        D = []
        for asset in self.asset:
            for i, motion in enumerate(asset.motion):
                if asset.connection is not None:
                    motion = motion + asset.connection.motion[i]
                velo = self._time_derivative(motion)
                D.append(dissipated(asset.component.drag_coeff, velo))

        D = sp.simplify(reduce((lambda x, y: x + y), D))

        for asset in self.asset:
            var_name = asset.var_name
            var_dot_exper = self._time_derivative(dynamicsymbols(var_name))
            D = D.subs(var_dot_exper, dynamicsymbols(var_name+'dot'))

        return sp.simplify(D)

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
    
    def _update_asset(self, s, v, a, t):
        for i, asset in enumerate(self.asset):
            asset.solution.displacement.append(s[i])
            asset.solution.velocity.append(v[i])
            asset.solution.acceleration.append(a[i])
            asset.solution.time.append(t)

    def _update_asset_initial_acceleration(self, a):
        for i, asset in enumerate(self.asset):
            asset.solution.acceleration[0] = a[i]
