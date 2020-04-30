"""The module `dynamics.model` creates the dynamic model for the system 
defined."""

from functools import reduce

import sympy as sp
from sympy.physics.vector import dynamicsymbols

from dynamics.tools import kinectic, potentialGrav

class Model:
    """A model class for evaluating the expression of motions of the system.
    The model object contains a list of tuples describing the motion of the
    system.
    """

    def __init__(self, motion: list, component:list):
        self.motion = [motion] if not isinstance(motion, list) else motion
        self.component = [component] if not isinstance(component, list) \
            else component

    def initialiser(self):
        """TODO(Ivan) :Make this class to initalise a set of prescribed
        motions based on the degree of freedom of the system. It should
        provide a way to generalise all energy methods."""
        pass

    def acceleration(self):
        """Evaluate the model of sytem of motion equations."""
        T = self._kinectic_energy()
        V = self._potential_energy()

        # # # TODO(Ivan): Change the names of terms variables
        # # t_term_1 =  self._time_derivative(sp.diff(T , dynamicsymbols('theta_dot')))
        # dt_dx_dot =  self._time_derivative(sp.diff(T , dynamicsymbols('x_dot')))
        # dt_dy_dot =  self._time_derivative(sp.diff(T , dynamicsymbols('y_dot')))

        # # theta_dot_dot_expr = sp.Derivative(dynamicsymbols('theta_dot'), (sp.Symbol('t'), 2))
        # # theta_dot_dot_expr = sp.Derivative(dynamicsymbols('theta_dot'), sp.Symbol('t'))
        # x_ddot = sp.Derivative(dynamicsymbols('x_dot'), sp.Symbol('t'))
        # y_ddot = sp.Derivative(dynamicsymbols('y_dot'), sp.Symbol('t'))

        # # t_term_1 = t_term_1.subs(theta_dot_dot_expr, dynamicsymbols("theta_ddot"))
        # dt_dx_dot = dt_dx_dot.subs(x_ddot, dynamicsymbols("x_ddot"))
        # dt_dy_dot = dt_dy_dot.subs(y_ddot, dynamicsymbols("y_ddot"))
        # t_term_1 = dt_dx_dot + dt_dy_dot

        # # t_term_2 = sp.diff(T, sp.Symbol('theta')).doit()
        # dt_dx_ddot = sp.diff(T, sp.Symbol('x')).doit()
        # dt_dy_ddot = sp.diff(T, sp.Symbol('y')).doit()
        # t_term_2 = dt_dx_ddot + dt_dy_ddot

        # dv_dx = sp.Derivative(V, dynamicsymbols('x')).doit()
        # dv_dy = sp.Derivative(V, dynamicsymbols('y')).doit()
        # v_term = dv_dx + dv_dy 

        # expression = t_term_1 - t_term_2 + v_term
        # expression = sp.simplify(expression)

        L = T - V

        dL_dx = sp.diff(L , dynamicsymbols('x')).doit()

        x_dot = self._time_derivative(dynamicsymbols("x"))
        x_ddot = sp.Derivative(dynamicsymbols('xdot'), sp.Symbol('t'))

        dL_dx_dot_dt = self._time_derivative(sp.diff(L , dynamicsymbols('xdot')).subs(x_dot, dynamicsymbols("xdot")))
        dL_dx_dot_dt = dL_dx_dot_dt.subs(x_dot, dynamicsymbols("xdot"))
        dL_dx_dot_dt = dL_dx_dot_dt.subs(x_ddot, dynamicsymbols("xddot"))

        expression = dL_dx - dL_dx_dot_dt
        # expression = sp.simplify(expression)

        return expression
    
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
        direction_grav = (0, 1, 0) # TODO(Ivan): Maybe add Quaternions rotation
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
