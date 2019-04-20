"""
Unit test for pendulum.py.
"""

import numpy as np
from unittest import TestCase
from unittest.mock import MagicMock
from dynamics.core import Problem, DynamicModel

class TestProblem(TestCase):

    def setUp(self):
        # Set up the test
        self.problem = Problem(dof=1)
        self.problem.setup = MagicMock(return_value=1)

    def test_constructor(self):
        # Evaluate and set the test parameters
        expected_dof = 1
        test_dof = self.problem.dof

        # Run tests
        np.testing.assert_equal(expected_dof, test_dof)

    def test_initialise(self):
        # Evaluate and set the test parameters
        expected_time_step = 1e-5
        self.problem.initialise(time_step=1e-5)
        test_time_step = self.problem.time_step

        # Run tests
        np.testing.assert_equal(expected_time_step, test_time_step)

    def test_setup(self):
        # Evaluate and set the test parameters
        expected_return = 1
        test_return = self.problem.setup()

        # Run tests
        np.testing.assert_equal(expected_return, test_return)

if __name__ == '__main__':
    from utils.test_utils import run_test
    test_classes_to_run = [TestProblem]
    run_test(test_classes_to_run)