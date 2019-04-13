"""
Unit test for pendulum.py.
"""

import numpy as np
from unittest import TestCase
from dynamics.pendulum.pendulum import Pendulum

class TestPendulum(TestCase):

    def setUp(self):
        self.dummy_pendulum = Pendulum(mu=0.1, time_step=1)

    def test_constractor(self):
        # Evaluate and set the parameters
        expected_mu = 0.1
        test_mu = self.dummy_pendulum.mu
        expected_result = {}
        test_result = self.dummy_pendulum.result

        # Run tests
        np.testing.assert_equal(expected_mu, test_mu)
        np.testing.assert_equal(expected_result, test_result)

    def test_setup(self):
        # Run set up method
        self.dummy_pendulum.setup(mu=0.2)
        
        # Evaluate and set the parameters
        expected_mu = 0.2
        test_mu = self.dummy_pendulum.mu
        
        # Run test
        np.testing.assert_equal(expected_mu, test_mu)

    def test_run(self):
        # Run run method
        self.dummy_pendulum.run()
        theta = self.dummy_pendulum.result['theta']

        # Evaluate the size of theta array
        expected_theta_size = (100,)
        test_theta_size = np.shape(theta)

        # Run test
        np.testing.assert_equal(test_theta_size, expected_theta_size)
        np.testing.assert_equal(theta[-1], 0)
    
    def test_get_phase_portait(self):
        # Run run method
        self.dummy_pendulum.get_phase_portait()
        omega = self.dummy_pendulum.result_phase['omega']
        
        # Evaluate the size of theta array
        expected_omega_size = (200, 300)
        test_omega_size = np.shape(omega)

        # Run test
        np.testing.assert_equal(test_omega_size, expected_omega_size)

if __name__ == '__main__':
    from utils.test_utils import run_test
    test_classes_to_run = [TestPendulum]
    run_test(test_classes_to_run)
    
