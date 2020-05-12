"""
Unit test for base.py.
"""

from unittest import TestCase
from unittest.mock import Mock

from dynamics.base import Simulation
from utils import DynamicsError, SimulationParametersNotDefinedError

class TestSimulation(TestCase):
    """Unit test for class Simulation."""

    def setUp(self):
        self.simulation = Simulation()

    def test_register_func(self):
        """Test method register by registering a function."""
        func = lambda x, y: x + y
        self.simulation.register('addition', func)
        test = self.simulation.addition(1, 9)

        self.assertEqual(test, 10)

    def test_register_obj(self):
        """Test method register by registering a function."""
        test_mock = Mock(test='pass')
        self.simulation.register('object', test_mock)
        test = self.simulation.object.test

        self.assertEqual(test, 'pass')

    def test_unregister(self):
        """Test method unregister for attribute."""
        test_mock = Mock()
        self.simulation.register('object', test_mock)
        self.simulation.unregister('object')

        with  self.assertRaises(AttributeError): self.simulation.object

    def test_run_1(self):
        """Test method run for the running the simulation, without setting
        the parameters."""
        with self.assertRaises(SimulationParametersNotDefinedError): \
            self.simulation.run()
    
    def test_run_2(self):
        """Test method run for simulation error handling, without model."""
        self.simulation.set_paramters(
            time_step=1e-3, time_start=0.0, time_end=1.0
        )
        with self.assertRaises(DynamicsError): self.simulation.run()

    def test_run_3(self):
        """Test method run for simulation error handling, without solver."""
        self.simulation.set_paramters(
            time_step=1e-3, time_start=0.0, time_end=1.0
        )
        with self.assertRaises(DynamicsError): self.simulation.run()

    def test_set_parameters(self):
        """Test method set_parameters for setting up simulation parameters."""
        self.simulation.set_paramters(
            time_step=1e-3, time_start=0.0, time_end=1.0
        )

        self.assertEqual(self.simulation.n_iter, 1000)
        self.assertEqual(self.simulation._parameters, True)


if __name__ == '__main__':
    from utils.test_utils import run_test
    TEST_CLASSES = [TestSimulation]
    run_test(TEST_CLASSES)