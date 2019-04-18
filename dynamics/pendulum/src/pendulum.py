"""
Author: Ivan (Chon-Hou) Chan
This is a numerical solution of pendulum to understand ordinary different equation.
The 2nd order differential equation: alpha = -mu*omega - g/l * sin(theta).
    
    Whereas (attributes):
        alpha: angular acceleration
        omega: angular velocity
        theta: angular displacement
        mu: friction coeff.
        g: acceleration due to gravity
        l: length of the string


A phase portait is constructed to visualise the motion of the pendulum.
The phase portait is described using the following expression:
(Two 1st order differential equations.)
    since,
    d[theta, omega]/dt = [omega, alpha];
    thus,
    d[theta, omega]/dt = [omega, -mu*omega - g/l * sin(theta)]

Ps. d[theta, omega]/dt has an attribute name - result_phase
"""
import numpy as np
from scipy import constants

class Pendulum(object):
    """
    Class to initalise the simulation of motion of pendulum.
        Attributes:
            mu: float - dimensionless 
                friction coefficient (e.g. air resistance)
            l: float - meter
                length of the string.
            time_step: float - seconds
                time step of the simulation.
            terminal_condition: float - seconds
                time for simulation to stop.
            resolution: float 
                resolution of the phase portait.
            theta_init: float - rad
                Initial angular position of the pendulum.
            omega_init: float - rad per second
                Initial angular velocity of the pendulum.
            theta_up: float - rad
                upper bound of the angular displacement.
            theta_low: float - rad
                lower bound of the angular displacement.
            omega_up: float - rad per second
                upper bound of the angular velocity.
            omega_low: float - rad per second
                lower bound of the angular veloctiy.
            g: float <constant> - meter per second per second
                acceleration due to gravity (scipy constant).
            result_phase: floats <np.array>
                phase portait of the system. 
    """

    def __init__(self, mu=0, l=constants.g, time_step=1e-3,
                theta_init=0, omeega_init=0, resolution=0.1,
                theta_up=15, theta_low=-15, omega_up=10,
                omega_low=-10, terminal_condition=100):
        "Constructor to initialise parameters."
        # Initialise Inputs
        self.mu = mu
        self.l = l
        self.time_step = time_step
        self.terminal_condition = terminal_condition
        self.resolution = resolution
        self.theta_init = theta_init
        self.omega_init = omeega_init
        self.theta_low = theta_low
        self.theta_up = theta_up
        self.omega_low = omega_low
        self.omega_up = omega_up
        self.resolution = resolution

        # Initialise constants 
        self.g = constants.g

        # Initialis output arrays
        self.result_phase = {}
        self.result = {}

    def setup(self, mu=None, l=None, theta_init=None,
              omega_init=None, theta_low=None, theta_up=None,
              omega_low=None, omega_up=None, resolution=None):
        "Method to reinitialise parameters."
        if mu is not None:
            self.mu = mu
        if l is not None:
            self.l = l
        if theta_init is not None:
            self.theta_init = theta_init
        if omega_init is not None:
            self.omega_init = omega_init
        if theta_low is not None:
            theta_low = self.theta_low
        if theta_up is not None:
            theta_up = self.theta_up
        if omega_low is not None:
            omega_low = self.omega_low
        if omega_up is not None:
            omega_up = self.omega_up
        if resolution is not None:
            resolution = self.resolution

    def run(self):
        "Method to run the simulation."
        
        # Initialise parameters
        theta_init = self.theta_init
        omega_init = self.omega_init
        time_step = self.time_step
        terminal_condition = self.terminal_condition

        time = np.arange(0, terminal_condition, time_step)

        # Initialise outputs arrays 
        theta = np.ones(len(time)) * theta_init
        omega = np.ones(len(time)) * omega_init
        time_step = np.diff(time)

        # results evaluation
        for i in range(len(time)-1):
            omega[i+1] = omega[i] + (- self.mu * omega[i] - self.g/self.l * np.sin(theta[i])) * time_step[i]
            theta[i+1] = theta[i] + omega[i] * time_step[i]
        self.result = {
            "time" : time,
            "theta" : theta,
            "omega" : omega,
        }

    def get_phase_portait(self):
        "Mwthod to evaluate the phase portait of the system."
        
        # Initialise parameters
        theta_low = self.theta_low
        theta_up = self.theta_up
        omega_low = self.omega_low
        omega_up = self.omega_up
        resolution = self.resolution

        theta = np.arange(theta_low, theta_up, resolution)
        omega = np.arange(omega_low, omega_up, resolution)

        # Initialise outputs arrays 
        omega_results = np.zeros((len(omega), len(theta)))
        alpha_results = np.zeros((len(omega), len(theta)))

        # Phase portait evaluation
        for i in range(len(omega)):
            omega_results[:][i] = omega[i] 
            alpha_results[:][i] = -self.mu * omega[i] - self.g/self.l * np.sin(theta)        
        self.result_phase = {
            "theta_input" : theta,
            "omega_input" : omega,
            "omega" : omega_results,
            "alpha" : alpha_results
        }