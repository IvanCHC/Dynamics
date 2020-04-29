""" The module `dynamics.tools.energy` provide methods to construct lagrange's
equation."""

from scipy.constants import g as g_acc

###################
# Kinectic Energy #
###################

def kinectic(mass, velo=None):
    """This function creates an expression of kinectic energy of a body for
    the given mass and velocity expression.

    Parameters:
        mass (float): Mass of the body.
        velo (Symbol): Symbolic expression of velocity.
    
    Returns:
        Symbolic expression of kinetic energy.
    """
    if velo is not None:
        return mass * velo ** 2 / 2
    else:
        return 0


####################
# Potential Energy #
####################

def potentialGrav(mass, disp=None, g=g_acc):
    """This function creates an expression of gravitation potential energy
    of a body for the given mass, acceleration due to gravity and displacement
    expression.

    Parameters:
        mass (float): Mass of the body.
        disp (Symbol): Symbolic expression of displacement.
        g (float): Acceleration due to gravity.
    
    Returns:
        Symbolic expression of potential energy.
    """
    if disp is not None:
        return mass * disp * g
    else:
        return 0


def potentialElas(stiff, disp=None):
    """This function creates an expression of elastic potential energy
    of a body for the given stiffness and displacement expression.

    Parameters:
        stiff (float): Mass of the body.
        disp (Symbol): Symbolic expression of displacement.
    
    Returns:
        Symbolic expression of potential energy.
    """
    if disp is not None:
        return stiff * disp ** 2 / 2
    else:
        return 0

##############################
# Rayleigh Dissipated Energy #
##############################

def dissipated(coeff, velo=None):
    """This function creates an expression of dissipated energy of a body for
    the given coefficient and velocity expression.

    Parameters:
        coeff (float): Coefficient of dissipation.
        velo (Symbol): Symbolic expression of velocity.
    
    Returns:
        Symbolic expression of dissipated energy.
    """
    if velo is not None:
        return coeff * velo ** 2 / 2
    else:
        return 0

###############################
# Generalised External Energy #
###############################
