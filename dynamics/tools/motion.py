""" The module `dynamics.tools.motion` provide methods to generation the
generalised co-ordinate system for the given component of system.

---------> (x)
|\              The diagram on the left shows how the generatlised
|)\ (theta)     co-ordinate system is defined.
|  \            NOTE: The current version can only compute 2D simulation.
v (y)
"""

import sympy as sp
from sympy.physics.vector import dynamicsymbols

########################
# Translational Motion #
########################

def translation(length):
    """This function creates the expressions of motions of a body.
    
    Parameters:
        length (float): Length of the connection.

    Returns:
        l (Symbol): Symbollic Generalised expression of motion in x-axis.
        x (Symbol): Symbollic variable.

    """
    x = dynamicsymbols("x")
    l = length + x

    return l, x

#####################
# Rotational Motion #
#####################

def rotation(length):
    """This function creates the expressions of motions of a body.
    
    Parameters:
        length (float): Length of the connection.

    Returns:
        x (Symbol): Generalised expression of motion in x-axis.
        y (Symbol): Generalised expression of motion in y-axis.
        theta (Symbol): Symbollic variable.
    """
    theta = dynamicsymbols("theta")

    # Resolve vector motion
    x = length * sp.sin(theta)
    y = length * sp.cos(theta)

    return x, y, theta
