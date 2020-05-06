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


def euler(f, s0, v0, t0, s_sym, v_sym, dt):
    """Numerical integrator using euler's method."""
    v = v0 + f.subs(s_sym, s0).subs(v_sym, v0) * dt
    s = s0 + v0 * dt
    t = t0 + dt

    return s, v, t

def improved_euler(f, s0, v0, t0, s_sym, v_sym, dt):
    """Numerical integrator using improved euler's method."""
    k1_v = f.subs(s_sym, s0).subs(v_sym, v0) * dt
    k1_s = v0 * dt

    k2_v = f.subs(s_sym, s0 + dt*k1_s).subs(v_sym, v0 + dt*k1_v) * dt
    k2_s = (v0 + dt*k1_v) * dt

    s = s0 + (k1_s + k2_s)/2
    v = v0 + (k1_v + k2_v)/2
    t = t0 + dt

    return s, v, t

def RK2(f, s0, v0, t0, s_sym, v_sym, dt):
    """Numerical integrator using RK2."""
    k1_v = f.subs(s_sym, s0).subs(v_sym, v0) * dt
    k1_s = v0 * dt

    k2_v = f.subs(s_sym, s0 + k1_s/2).subs(v_sym, v0 + k1_v/2) *dt
    k2_s = (v0 + k1_v/2) * dt

    s = s0 + k2_s + dt**3
    v = v0 + k2_v + dt**3
    t = t0 + dt

    return s, v, t

def RK4(f, s0, v0, t0, s_sym, v_sym, dt):
    """Numerical integrator using RK4."""
    k1_v = f.subs(s_sym, s0).subs(v_sym, v0) * dt
    k1_s = v0 * dt

    k2_v = f.subs(s_sym, s0 + k1_s/2).subs(v_sym, v0 + k1_v/2) * dt
    k2_s = (v0 + k1_v/2) * dt

    k3_v = f.subs(s_sym, s0 + k2_s/2).subs(v_sym, v0 + k2_v/2) * dt
    k3_s = (v0 + k2_v/2) * dt

    k4_v = f.subs(s_sym, s0 + k3_s).subs(v_sym, v0 + k3_v) * dt
    k4_s = (v0 + k3_v) * dt

    s = s0 + (k1_s + 2*k2_s + 2*k3_s + k4_s)/6 + dt**5
    v = v0 + (k1_v + 2*k2_v + 2*k3_v + k4_v)/6 + dt**5
    t = t0 + dt

    return s, v, t
