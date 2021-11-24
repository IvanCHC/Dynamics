"""This module provides methods for numerical integrator (solver) for
nonlinear dynamics simulation.

Parameters
----------
    f : Symbolic function of the acceleration.
    s0 : Initial condition for displacement.
    v0 : Initial condition for velocity.
    t0 : Initial condition for time.
    s_sym : Dynamicsymbols for displacement
    v_sym : Dynamicsymbols for velocity.
    dy : Time step.
"""

import numpy as np

def euler(f, s0, v0, t0, dt, j):
    """Numerical integrator using euler's method."""
    a = f(s0, v0)
    v = v0[j] + a * dt
    s = s0[j] + v * dt
    t = t0 + dt

    return s, v, a, t

def improved_euler(f, s0, v0, t0, dt, j):
    """Numerical integrator using improved euler's method."""
    a = f(s0, v0)

    k1_v = a * dt
    k1_s = v0 * dt

    k2_v = f(s0 + dt*k1_s, v0 + dt*k1_v) * dt
    k2_s = (v0 + dt*k1_v) * dt

    s = s0[j] + (k1_s + k2_s)/2
    v = v0[j] + (k1_v + k2_v)/2
    t = t0 + dt

    return s, v, a, t

def RK2(f, s0, v0, t0, dt, j):
    """Numerical integrator using RK2."""
    a = f(s0, v0)

    k1_v = a * dt
    k1_s = v0 * dt

    k2_v = f(s0 + k1_s/2, v0 + k1_v/2) *dt
    k2_s = (v0 + k1_v/2) * dt

    s = s0[j] + k2_s + dt**3
    v = v0[j] + k2_v + dt**3
    t = t0 + dt

    return s, v, a, t

def RK4(f, s0, v0, t0, dt, j):
    """Numerical integrator using RK4."""
    a = f(s0, v0)

    k1_v = a * dt
    k1_s = v0 * dt

    k2_v = f(s0 + k1_s/2, v0 + k1_v/2) * dt
    k2_s = (v0 + k1_v/2) * dt

    k3_v = f(s0 + k2_s/2, v0 + k2_v/2) * dt
    k3_s = (v0 + k2_v/2) * dt

    k4_v = f(s0 + k3_s, v0 + k3_v) * dt
    k4_s = (v0 + k3_v) * dt

    s = s0[j] + ((k1_s + 2*k2_s + 2*k3_s + k4_s)/6)[j] + dt**5
    v = v0[j] + (k1_v + 2*k2_v + 2*k3_v + k4_v)/6 + dt**5
    t = t0 + dt

    return s, v, a, t
