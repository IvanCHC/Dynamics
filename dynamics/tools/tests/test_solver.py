"""
Unit test for solver.py.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

import numpy as np
from sympy.physics.vector import dynamicsymbols

from dynamics.tools import solver

class TestSolver(TestCase):
    """Unit test for class solver."""

    def setUp(self):
        self.s_sym = dynamicsymbols('x')
        self.v_sym = dynamicsymbols('xdot')
        self.f = self.v_sym**2 + self.s_sym
        self.s0 = 2
        self.v0 = 2
        self.t0 = 0
        self.dt = 1

    def test_euler(self):
        solution = solver.euler(
            self.f, self.s0, self.v0, self.t0, self.s_sym, self.v_sym, self.dt
        )
        self.assertTupleEqual(solution, (4, 8, 1))

    def test_improved_euler(self):
        solution = solver.improved_euler(
            self.f, self.s0, self.v0, self.t0, self.s_sym, self.v_sym, self.dt
        )
        self.assertTupleEqual(solution, (7, 39, 1))

    def test_RK2(self):
        solution = solver.RK2(
            self.f, self.s0, self.v0, self.t0, self.s_sym, self.v_sym, self.dt
        )
        self.assertTupleEqual(solution, (8, 31, 1))

    def test_RK4(self):
        solution = solver.RK4(
            self.f, self.s0, self.v0, self.t0, self.s_sym, self.v_sym, self.dt
        )
        np.testing.assert_array_almost_equal(solution, (54.083, 11587.542, 1), 3)

if __name__ == '__main__':
    from utils.test_utils import run_test
    TEST_CLASSES = [TestSolver]
    run_test(TEST_CLASSES)