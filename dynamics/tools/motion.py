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

def translation(length: float, var_name: str):
    """This function creates the expressions of motions of a body.
    
    Parameters:
        length (float): Length of the connection.
        var_name (string): name of symbollic variable.

    Returns:
        x (Symbol): Symbollic variable.
        l (Symbol): Symbollic Generalised expression of motion in x-axis.

    """
    x = dynamicsymbols(var_name)
    l = length + x

    return x, l

#####################
# Rotational Motion #
#####################

def rotation(length: float, var_name: str):
    """This function creates the expressions of motions of a body.
    
    Parameters:
        length (float): Length of the connection.
        var_name (string): name of symbollic variable.

    Returns:
        x (Symbol): Generalised expression of motion in x-axis.
        y (Symbol): Generalised expression of motion in y-axis.
        theta (Symbol): Symbollic variable.
    """
    theta = dynamicsymbols(var_name)

    # # Resolve vector motion
    x = length * sp.sin(theta)
    y = length * sp.cos(theta)

    return x, y, theta
