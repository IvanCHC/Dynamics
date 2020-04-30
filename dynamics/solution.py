"""The module `dynamics.solution` store information and results of the solution."""

class Solution:

    def __init__(self, var_name="x", s=0.6, v=0, t=0, dt=5e-3):
        self.var_name = var_name
        self.s = s
        self.v = v
        self.t = t
        self.dt = dt

        self.s_rec = [s]
        self.v_rec = [v]
        self.t_rec = [t]