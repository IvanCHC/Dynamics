"""
Author: Ivan (Chon-Hou) Chan
This is the numerical solver for the dynamic system.
"""
from dynamics.core import Solver

class Euler(Solver):
    """
    Euler solver, this uses the Euler method to simulate the dynamic system.
    """

    def solve(self, displacement, velocity, acceleration, time_step, dof):
        """This calculate the variable for the next time step."""
        # Evaluate acceleration
        acc = acceleration(displacement, velocity, dof)
        # Evaluate the displacement and velocity for the next time step
        displacement = displacement + velocity * time_step
        velocity = velocity + acc * time_step
        return displacement, velocity

class ImprovedEuler(Solver):
    """
    Euler solver, this uses the improved Euler method to simulate the dynamic system.
    """

    def solve(self, displacement, velocity, acceleration, time_step, dof):
        """This calculate the variable for the next time step."""
        # Calculate the values of k1 for both parameters
        k1_disp = time_step * velocity
        acc = acceleration(displacement, velocity, dof)
        k1_velo = time_step * acc

        # Calculate the values of k2 for both parameters
        k2_disp = time_step * (velocity + k1_velo)
        acc = acceleration(displacement+k1_disp, velocity+k1_velo, dof)
        k2_velo = time_step * acc

        # Evaluate the displacement and velocity for the next time step
        displacement = displacement + (k1_disp + k2_disp)/2
        velocity = velocity + (k1_velo + k2_velo)/2

        return displacement, velocity

class RungeKuttaTwo(Solver):
    """
    Runge Kutta solver, this uses the 2nd-order Runge Kutta method to simulate the dynamic system.
    """

    def solve(self, displacement, velocity, acceleration, time_step, dof):
        """This calculate the variable for the next time step."""
        # Calculate the value of k1 for displacement
        k1_disp = time_step * velocity

        # Calculate the value of k1 for velocity
        acc = acceleration(displacement, velocity, dof)
        k1_velo = time_step * acc

        # Calculate teh value of k2 for displacement
        k2_disp = time_step * (velocity + k1_velo/2)

        # Calculate the value of k2 for velocity
        acc = acceleration(displacement+k1_disp/2, velocity+k1_velo/2, dof)
        k2_velo = time_step * acc

        # Evaluate the displacement and velocity for the next time step
        displacement = displacement + k2_disp + time_step**3
        velocity = velocity + k2_velo + time_step**3

        return displacement, velocity

class RungeKuttaFour(Solver):
    """
    Runge Kutta solver, this uses the 4th-order Runge Kutta method to simulate the dynamic system.
    """

    def solve(self, displacement, velocity, acceleration, time_step, dof):
        """This calculate the variable for the next time step."""
        # Calculate the value of k1 for velocity
        acc = acceleration(displacement, velocity, dof)
        k1_velo = time_step * acc

        # Calculate the value of k1 for displacement
        k1_disp = time_step * velocity

        # Calculate the value of k2 for velocity
        acc = acceleration(displacement+k1_disp/2, velocity+k1_velo/2, dof)
        k2_velo = time_step * acc

        # Calculate teh value of k2 for displacement
        k2_disp = time_step * (velocity + k1_velo/2)

        # Calculate the value of k3 for velocity
        acc = acceleration(displacement+k2_disp/2, velocity+k2_velo/2, dof)
        k3_velo = time_step * acc

        # Calculate teh value of k3 for displacement
        k3_disp = time_step * (velocity + k2_velo/2)

        # Calculate the value of k4 for velocity
        acc = acceleration(displacement+k3_disp, velocity+k3_velo, dof)
        k4_velo = time_step * acc

        # Calculate teh value of k4 for displacement
        k4_disp = time_step * (velocity + k3_velo)

        # Evaluate the displacement and velocity for the next time step
        displacement = displacement + (k1_disp+2*k2_disp+2*k3_disp+k4_disp)/6 + time_step**5
        velocity = velocity + (k1_velo+2*k2_velo+2*k3_velo+k4_velo)/6 + time_step**5

        return displacement, velocity

# class RungeKuttaFehlberg(Solver):
#     """
#     RKF45 Runge Kutta Fehlberg solver, TODO(Ivan): implement variable time step.
#     """
