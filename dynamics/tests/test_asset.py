"""
Unit test for model.py.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

from dynamics.asset import Asset

class TestAsset(TestCase):
    """Unit test for class Asset."""

    def setUp(self):
        self.name = 'test'
        self.var_name = 'test_var'
        self.component = Mock(length=1)
        self.solution = Mock()
        self.motion_func = Mock()

    def test_motion(self):
        func = lambda x, y: x + y
        asset = Asset(self.name, 1, self.component, self.solution, func)

        self.assertEqual(asset.motion, 2)


if __name__ == '__main__':
    from utils.test_utils import run_test
    TEST_CLASSES = [TestAsset]
    run_test(TEST_CLASSES)