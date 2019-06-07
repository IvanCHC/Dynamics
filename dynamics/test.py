"""The module `dynamics.test` contains unittest runner for dynamics. It is
used to run all tests.
"""

import unittest


def create_suite():
    test_suite = unittest.TestLoader().discover('.', pattern="test_*.py")
    return test_suite

if __name__ == '__main__':

    suite = create_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
