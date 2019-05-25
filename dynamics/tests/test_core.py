"""
Unit test for core.py.
"""

from unittest import TestCase
from dynamics.core import Model
from utils.test_utils import run_test

class TestModel(TestCase):
    "Unit test for the Model."

    def setUp(self):
        "Methdo to setup the model unit test."
        components = "alpha"
        self.model = Model(components=components)

    def test_list_conversion(self):
        "Method to test list conversion."
        # Initialise test components
        components = "alpha"
        model = Model(components=components)

        self.assertEqual(model.components, [components])

    def test_list_conversion_2(self):
        "Method to test list conversion."
        # Initialise test components
        components = ["alpha"]
        model = Model(components=components)

        self.assertEqual(model.components, components)


if __name__ == '__main__':
    TEST_CLASSES = [TestModel]
    run_test(TEST_CLASSES)
