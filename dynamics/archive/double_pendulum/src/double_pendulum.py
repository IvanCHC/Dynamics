"""
Author: Ivan (Chon-Hou) Chan
This is a numerical solution of double pendulum.
"""
import numpy as np
from scipy import constants

class DoublePendulum(object):
    
    def __init__(self, dof=2, mass=(1,1), l=(1,1),
                c=(0,0), theta_init=(1,1),
                omega_init=(0,0), time_step=1e-5,
                terminal_condition=20):
        "Constructor to initialise parameters."
        # Initialise Inputs
        self.dof = dof
        self.mass = mass
        self.l  = l
        self.c = c
        self.theta_init = theta_init
        self.omega_init = omega_init
        self.time_step = time_step
        self.terminal_condition = terminal_condition

        # Initialise constants 
        self.g = constants.g

        # Initialis output arrays
        self.result = {}

    def run(self):
        "Method to run the simulation."

        time = np.arange(0, self.terminal_condition, self.time_step)

        # Initialise outputs arrays 
        theta = np.zeros((self.dof, len(time)))
        omega = np.zeros((self.dof, len(time)))
        for i in range(self.dof):
            theta[i][0] = self.theta_init[i]
            omega[i][0] = self.omega_init[i]
        time_step = np.diff(time)

        # Results evaluation
        for i in range(len(time_step)):
            # Evaluate equivalent mass matrix
            M = self._mass_matrix(theta[:,i])
            # Evaluate equivalent reaction matrix 
            R = self._reaction_matrix(theta[:,i], omega[:,i])

            # Calculate the invert of equivalent mass matrix
            M_inverted = np.linalg.inv(M)

            # Calculate the theta and omega for the next time step
            for j in range(self.dof):
                theta[j][i+1] = theta[j][i] + omega[j][i] * time_step[i]
                omega[j][i+1] = omega[j][i] + np.dot(M_inverted[j], R) * time_step[i]

        self.result = {
            "time" : time,
            "theta" : theta,
            "omega" : omega,
        }

    def _mass_matrix(self, theta):
        "function to evaluate the equivalent mass matrix."
        M_11 = (self.mass[0] + self.mass[1]) * self.l[0]**2
        M_12 = self.mass[1] * self.l[0] * self.l[1] * \
            np.cos(theta[0] - theta[1])
        M_21 = self.mass[1] * self.l[0] * self.l[1] * \
            np.cos(theta[0] - theta[1])
        M_22 = self.mass[1] * self.l[1]**2

        return np.array([[M_11, M_12], [M_21, M_22]])

    def _reaction_matrix(self, theta, omega):
        "function to evaluate the equivalent reaction matrix."
        R_1 = -1 * ((self.mass[0] + self.mass[1]) * self.l[0] * self.g *
            np.sin(theta[0]) + self.mass[1] * self.l[0] * self.l[1] *
            omega[1]**2 * np.sin(theta[0] - theta[1]) + self.c[0] *
            omega[0] + self.c[1] * (omega[0] - omega[1]))
        R_2 = -1 * (self.mass[1] * self.l[1] * self.g * np.sin(theta[1]) -
            self.mass[1] * self.l[0] * self.l[1] * omega[0]**2 *
            np.sin(theta[0] - theta[1]) + self.c[1] * (omega[1] - omega[0]))
        
        return np.array([R_1, R_2])