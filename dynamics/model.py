"""The module `dynamics.model` creates the dynamic model for the system 
defined."""

from functools import reduce

import sympy as sp
from sympy.physics.vector import dynamicsymbols

from dynamics.tools import kinectic, potentialGrav
from dynamics.tools.solver import euler

class Model:
    """A model class for evaluating the expression of motions of the system.
    The model object contains a list of tuples describing the motion of the
    system.
    """

    def __init__(self, motion: list, component:list):
        self.motion = [motion] if not isinstance(motion, list) else motion
        self.component = [component] if not isinstance(component, list) \
            else component
        
        self.direction_grav = (0, 1, 0)

    def initialiser(self, direction_grav=None):
        """This class to initalise a set of prescribed
        motions based on the degree of freedom of the system. It should
        provide a way to generalise all energy methods."""
        if direction_grav is None:
            self.direction_grav = (0, 1, 0)
        else:
            self.direction_grav = direction_grav 

    def acceleration(self):
        """Evaluate the model of sytem of motion equations."""
        T = self._kinectic_energy()
        V = self._potential_energy()

        L = T - V

        dL_dx = sp.diff(L , dynamicsymbols('x')).doit()

        x_dot = self._time_derivative(dynamicsymbols("x"))
        x_ddot = sp.Derivative(dynamicsymbols('xdot'), sp.Symbol('t'))

        dL_dx_dot_dt = self._time_derivative(sp.diff(L , dynamicsymbols('xdot')).subs(x_dot, dynamicsymbols("xdot")))
        dL_dx_dot_dt = dL_dx_dot_dt.subs(x_dot, dynamicsymbols("xdot"))
        dL_dx_dot_dt = dL_dx_dot_dt.subs(x_ddot, dynamicsymbols("xddot"))

        expression = dL_dx - dL_dx_dot_dt
        expression = sp.simplify(expression)

        return expression
    
    def solve(self, solver=euler):
        """Solve the model using the given solver."""
        pass

    # TODO(Ivan): Generalise it for multi-nodes system.
    def _kinectic_energy(self):
        """Evaluate the kinetic energy term of the Lagrangian."""
        T = []
        for i, expre in enumerate(self.motion):
            for j in range(len(expre)-1):
                velo = self._time_derivative(self.motion[i][j])
                T.append(kinectic(self.component[i].mass, velo))
        
        T = reduce((lambda x, y: x + y), T)
        T = sp.simplify(T)

        for _, expre in enumerate(self.motion):
            x_dot_exper = self._time_derivative(expre[0])
            T = T.subs(x_dot_exper, dynamicsymbols('xdot'))
            y_dot_exper = self._time_derivative(expre[1])
            T = T.subs(y_dot_exper, dynamicsymbols('ydot'))

        return T

    def _potential_energy(self):
        """Evaluate the kinetic energy term of the Lagrangian."""
        V = []
        direction_grav = self.direction_grav
        for i, expre in enumerate(self.motion):
            # Gravitational potential energy
            for j in range(len(expre)-1):
                # TODO(Ivan): change the '1' to length
                disp = (1 - self.motion[i][j]) * direction_grav[j]
                V.append(potentialGrav(self.component[i].mass, disp))
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
