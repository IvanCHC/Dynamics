"""
Author: Ivan (Chon-Hou) Chan
This is a numerical solution of spring-damper to understand ordinary different equation.
The 2nd order differential equation: ma = - cv - kx.

    Whereas (attributes):
        a:  translational acceleration
        v:  translational velocity 
        x:  translational distance
        m:  mass
        c:  damping coeff.
        k:  spring constant

A phase portait is constructed to visualise the motion of the spring-damper.
The phase portait is described using the following expression:
(Two 1st order differential equations.)
    since,
    d[x, v]/dt = [v, a];
    thus,
    d[x, v]/dt = [v, -m(cv + kx)]

"""
import numpy as np

class SpringDamper(object):
    """
    Class to initalise the simulation of motion of spring-damper.
        Attributes:
            m: float - kilogram
                mass
            c: float - newtons second per meter
                damping coefficient
            k: float - newtons per meter
                spring constant
            l: float - meters
                natural length of the spring
            time_step: float - seconds
                time step of the simulation.
            terminal_condition: float - seconds
                time for simulation to stop.
            resolution: float 
                resolution of the phase portait.
            x_init: float - meters
                Initial displacement of the spring-damper.
            v_init: float - meters per second
                Initial velocity of the spring-damper.
            x_up: float - meters
                upper bound of the displacement.
            x_low: float - meters
                lower bound of the displacement.
            v_up: float - meters per second
                upper bound of the velocity.
            v_low: float - meters per second
                lower bound of the veloctiy.
            result_phase: floats <np.array>
                phase portait of the system. 
    """

    def __init__(self, m=1, c=0, k=1, time_step=1e-3,
                x_init=0, v_init=0, resolution=0.1,
                x_up=1, x_low=-1, v_up=1, v_low=-1,
                terminal_condition=20, l=1):
        "Constructor to initialise parameters."
        # Initialise Inputs
        self.m = m
        self.c = c
        self.k = k
        self.time_step = time_step
        self.terminal_condition = terminal_condition
        self.resolution = resolution
        self.x_init = x_init
        self.v_init = v_init
        self.x_low = x_low
        self.x_up = x_up
        self.v_low = v_low
        self.v_up = v_up
        self.l = l
        self.resolution = resolution

        # Initialis output arrays
        self.result_phase = {}
        self.result = {}

    def setup(self, c=None, k=None, m=None, x_init=None,
              v_init=None, x_low=None, x_up=None,
              v_low=None, v_up=None, resolution=None):
        "Method to reinitialise parameters."
        if c is not None:
            self.c = c
        if k is not None:
            self.k = k
        if m is not None:
            self.m = m
        if x_init is not None:
            self.x_init = x_init
        if v_init is not None:
            self.v_init = v_init
        if x_low is not None:
            x_low = self.x_low
        if x_up is not None:
            x_up = self.x_up
        if v_low is not None:
            v_low = self.v_low
        if v_up is not None:
            v_up = self.v_up
        if resolution is not None:
            resolution = self.resolution

    def run(self):
        "Method to run the simulation."
        
        # Initialise parameters
        x_init = self.x_init
        v_init = self.v_init
        time_step = self.time_step
        terminal_condition = self.terminal_condition

        time = np.arange(0, terminal_condition, time_step)

        # Initialise outputs arrays 
        x = np.ones(len(time)) * x_init
        v = np.ones(len(time)) * v_init
        time_step = np.diff(time)

        # results evaluation
        for i in range(len(time)-1):
            v[i+1] = v[i] + (- self.m**-1 * (self.c * v[i] + self.k * x[i])) * time_step[i]
            x[i+1] = x[i] + v[i] * time_step[i]
        self.result = {
            "time" : time,
            "x" : x,
            "v" : v,
        }

    def get_phase_portait(self):
        "Mwthod to evaluate the phase portait of the system."
        
        # Initialise parameters
        x_low = self.x_low
        x_up = self.x_up
        v_low = self.v_low
        v_up = self.v_up
        resolution = self.resolution

        x = np.arange(x_low, x_up, resolution)
        v = np.arange(v_low, v_up, resolution)

        # Initialise outputs arrays 
        omega_results = np.zeros((len(v), len(x)))
        alpha_results = np.zeros((len(v), len(x)))

        # Phase portait evaluation
        for i in range(len(v)):
            v_results[:][i] = v[i] 
            a_results[:][i] = - self.m**-1 * (self.c * v[i] + self.k * x[i])        
        self.result_phase = {
            "x_input" : x,
            "v_input" : v,
            "v" : v_results,
            "a" : a_results
        }