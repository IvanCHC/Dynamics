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
        """Evaluate the lagrangian of the model."""

        T = self._kinectic_energy()
        V = self._potential_energy()

        L = T - V
        L = sp.simplify(L)

        return L

    def acceleration(self):
        """Evaluate the model of sytem of motion equations."""

        L = self.lagrangian()
        D = self._dissipation()

        equations = []
        variables = []
        for _, asset in enumerate(self.asset):
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
            for j, variable in enumerate(variables):
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

        var_names = []
        acc_symbols = []
        vel_symbols = []
        dis_symbols = []
        s = []
        v = []
        t = self.time_start
        for i, asset in enumerate(self.asset):
            var_names.append(asset.var_name)
            acc_symbols.append(dynamicsymbols(asset.var_name+'ddot'))
            vel_symbols.append(dynamicsymbols(asset.var_name+'dot'))
            dis_symbols.append(dynamicsymbols(asset.var_name))
            x, dx, _, _ = asset.solution.initial_conditions
            s.append(x)
            v.append(dx)
        s = np.array(s, dtype=np.float64)
        v = np.array(v, dtype=np.float64)

        mass_matrix = []
        react_matrix = []
        for _, accel_expre in enumerate(expre):
            mass_row = []
            react_row = accel_expre
            for _, acc_symbol in enumerate(acc_symbols):
                mass_row.append(accel_expre.coeff(acc_symbol))
                react_row = sp.simplify(react_row.subs(acc_symbol, 0))
            mass_matrix.append(mass_row)
            react_matrix.append(react_row)
        mass_matrix = sp.Matrix(mass_matrix).inv()
        react_matrix = sp.Matrix(react_matrix)

        acc_matrix = mass_matrix*react_matrix
        acc_matrix = sp.simplify(acc_matrix)

        acc_matrix_lamb = [sp.lambdify([dis_symbols, vel_symbols], acc_express) for acc_express in acc_matrix]

        for i in tqdm(range(self.n_iter)):
            for j, acc in enumerate(acc_matrix_lamb):
                # dx_sym = [x for k,x in enumerate(dis_symbols) if k!=j]
                # dxdot_sym = [x for k,x in enumerate(vel_symbols) if k!=j]
                # for k in range(len(dx_sym)):
                    # accel = acc.subs({dx_sym[k]: s[k], dxdot_sym[k]: v[k]})
                # if len(dx_sym) == 0:
                    # accel = acc
                s_temp, v_temp, a, time = solver(acc, s, v, t, self.time_step, j)
                # s[j], v[j] = s[j].evalf(), v[j].evalf()
                self.asset[j].solution.displacement.append(s_temp)
                self.asset[j].solution.velocity.append(v_temp)
                self.asset[j].solution.acceleration.append(a)
                self.asset[j].solution.time.append(time)
                
                if i == 0:
                    self.asset[j].solution.acceleration[0] = a

                v[j] = v_temp
                s[j] = s_temp
            t = time

    def get_results(self):
        """Get results from the assets."""
        results = None
        for i, asset in enumerate(self.asset):
            if i == 0:
                results_df = asset.results
            if i != 0:
                data = asset.results
                results_df = pd.concat([results_df, data])
        return results_df

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
                disp = - (motion) * direction_grav[j]
                V.append(potentialGrav(asset.component.mass, disp))
            del disp

        V = reduce((lambda x, y: x + y), V)
        V = sp.simplify(V)

        return V

    def _dissipation(self):
        """Evaluate the Rayleigh dissipation term."""
        D = []
        for _, asset in enumerate(self.asset):
            for i, motion in enumerate(asset.motion):
                if asset.connection is not None:
                    motion = motion + asset.connection.motion[i]
                velo = self._time_derivative(motion)
                D.append(dissipated(asset.component.drag_coeff, velo))

        D = reduce((lambda x, y: x + y), D)
        D = sp.simplify(D)

        for _, asset in enumerate(self.asset):
            var_name = asset.var_name
            var_dot_exper = self._time_derivative(dynamicsymbols(var_name))
            D = D.subs(var_dot_exper, dynamicsymbols(var_name+'dot'))

        D = sp.simplify(D)

        return D            

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

