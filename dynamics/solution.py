"""The module `dynamics.solution` store information and results of the solution."""

class Solution:
    """A solution class for the storage the results motion of the simulation.
    Each solution object should only store results motion of one moving body."""

    def __init__(self, var_name: str = "x", disp_0: float = 0.0,
                 velo_0: float = 0.0, time_0: float = 0.0):
        self.var_name = var_name
        self._displacement = [disp_0]
        self._velocity = [velo_0]
        self._acceleration = [0.0]
        self._time = [time_0]

    @property
    def displacement(self):
        return self._displacement

    @displacement.setter
    def displacement(self, value):
        self._displacement.append(value)

    @property
    def disp_0(self):
        return self._displacement[0]

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity.append(value)

    @property
    def velo_0(self):
        return self._velocity[0]

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration.append(value)

    @property
    def acc_0(self):
        return self._acceleration[0]

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time.append(value)

    @property
    def time_0(self):
        return self._time[0]

