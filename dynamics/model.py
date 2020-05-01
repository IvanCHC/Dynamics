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

    def __init__(self, motion: list, component:list, solution:list):
        self.motion = [motion] if not isinstance(motion, list) else motion
        self.component = [component] if not isinstance(component, list) \
            else component
        self.solution = [solution] if not isinstance(solution, list) \
            else solution
        
        self.direction_grav = (0, 1, 0)
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
            self.direction_grav = (0, 1, 0)
        else:
            self.direction_grav = direction_grav
        
        if time_start is not None:
            self.time_start = time_start

        if time_step is not None:
            self.time_step = time_step
        
        if n_iter is not None:
            self.n_iter = n_iter

    def acceleration(self):
        """Evaluate the model of sytem of motion equations."""

        T = self._kinectic_energy()
        V = self._potential_energy()

        L = T - V
        L = sp.simplify(L)

        var_name = self.solution[0].var_name
        dL_dx = sp.diff(L , dynamicsymbols(var_name)).doit()

        x_dot = self._time_derivative(dynamicsymbols(var_name))
        x_ddot = sp.Derivative(dynamicsymbols(var_name+'dot'), sp.Symbol('t'))

        dL_dx_dot_dt = self._time_derivative(sp.diff(L , x_dot).subs(x_dot, dynamicsymbols(var_name+"dot")))
        dL_dx_dot_dt = dL_dx_dot_dt.subs(x_dot, dynamicsymbols(var_name+"dot"))
        dL_dx_dot_dt = dL_dx_dot_dt.subs(x_ddot, dynamicsymbols(var_name+"ddot"))

        expression = dL_dx - dL_dx_dot_dt
        expression = sp.simplify(expression)

        return expression
    
    def solve(self, solver):
        """Solve the model using the given solver."""
        expre = self.acceleration()

        var_name = self.solution[0].var_name
        mass_equ = expre.coeff(dynamicsymbols(var_name+'ddot'))
        react_equ = sp.simplify(-expre.subs(dynamicsymbols(var_name+'ddot'), 0))
        acc = sp.simplify(react_equ / mass_equ)

        from tqdm import tqdm

        s, v, _, _ = self.solution[0].initial_conditions
        t = self.time_start
        self.solution[0].time = t
        for i in tqdm(range(self.n_iter)):
            s, v, t = solver(acc, s, v, t, dynamicsymbols(var_name),
                            dynamicsymbols(var_name+'dot'), self.time_step)

            s, v, t = s, v.evalf(), t            

            self.solution[0].displacement.append(s)
            self.solution[0].velocity.append(v)
            self.solution[0].time.append(t)

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
            var_name = self.solution[0].var_name
            x_dot_exper = self._time_derivative(expre[0])
            T = T.subs(x_dot_exper, dynamicsymbols(var_name+'dot'))
            y_dot_exper = self._time_derivative(expre[1])
            T = T.subs(y_dot_exper, dynamicsymbols(var_name+'dot'))

        return T

    def _potential_energy(self):
        """Evaluate the kinetic energy term of the Lagrangian."""
        V = []
        direction_grav = self.direction_grav
        for i, expre in enumerate(self.motion):
            # Gravitational potential energy
            for j in range(len(expre)-1):
                disp = (- self.motion[i][j]) * direction_grav[j]
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
