"""
Unit test for creator.py.
"""

from nose import with_setup
from unittest import TestCase

from dynamics import creator

CNAME = "CLASS_NAME"

def teardown_func():
    creator.__dict__.pop(CNAME)

class TestCreator(TestCase):
    """Unit test for module Creator."""
    
    @with_setup(None, teardown_func)
    def test_create(self):
        "Method to test create method."
        creator.create(CNAME, list)
        l = creator.__dict__[CNAME]([0,1,2,3])

        self.assertEqual(l, [0,1,2,3])
        teardown_func()

    @with_setup(None, teardown_func)
    def test_attribute(self):
        "Method to test create method with attribute."
        creator.create(CNAME, list, a=1)
        l = creator.__dict__[CNAME]([0,1,2,3])

        self.assertEqual(l.a, 1)
        teardown_func()

if __name__ == '__main__':
    from utils.test_utils import run_test
    TEST_CLASSES = [TestCreator]
    run_test(TEST_CLASSES)
