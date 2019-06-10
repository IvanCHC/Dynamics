"""
Unit test for base.py.
"""

from unittest import TestCase

from dynamics.base import Simulation

class TestSimulation(TestCase):
    """Unit test for class Simulation."""

    def setUp(self):
        self.simulation = Simulation()
        self.func = lambda x, y: x + y

    def test_register(self):
        """Test method register by registering a function."""
        self.simulation.register('addition', self.func)
        test = self.simulation.addition(1, 9)
        
        self.assertEqual(test, 10)
        

if __name__ == '__main__':
    from utils.test_utils import run_test
    TEST_CLASSES = [TestSimulation]
    run_test(TEST_CLASSES)