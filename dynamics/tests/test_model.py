"""
Unit test for model.py.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

import sympy as sp
from sympy.physics.vector import dynamicsymbols

from dynamics.model import Model

class TestModel(TestCase):
    """Unit test for class Model."""

    def test_initialise(self):
        """Test method initialise."""
        asset = Mock()
        model = Model(asset)

        model.initialise(direction_grav=(1, 0), time_step=5e-3,
                         n_iter=200, time_start=10.0)
        self.assertEqual(model.direction_grav, (1, 0))
        self.assertEqual(model.time_step, 5e-3)
        self.assertEqual(model.n_iter, 200)
        self.assertEqual(model.time_start, 10.0)

    @patch('dynamics.model.Model._time_derivative', return_value=0)
    @patch('dynamics.model.kinectic')
    def test_kinectic_energy(self, mock_kinetic, mock_time_der):
        """Test method kinectic energy."""
        mock_kinetic.return_value = dynamicsymbols('xdot')**2

        asset = Mock(var_name='x', motion=[1], connection=None)
        model = Model([asset, asset])
        self.assertEqual(model._kinectic_energy(), 2*dynamicsymbols('xdot')**2)
        
    @patch('dynamics.model.potentialGrav')
    def test_potential_energy(self, mock_potentialGrav):
        """Test method potential energy."""
        mock_potentialGrav.return_value = dynamicsymbols('x')

        asset = Mock(var_name='x', motion=[1], connection=None)
        model = Model([asset, asset])
        self.assertEqual(model._potential_energy(), 2*dynamicsymbols('x'))


if __name__ == '__main__':
    from utils.test_utils import run_test
    TEST_CLASSES = [TestModel]
    run_test(TEST_CLASSES)