"""
Utils for Unit test.
"""
import unittest

def run_test(test_classes):
    " Method to run many test classes."
    # Initialise loader and suite list
    loader = unittest.TestLoader()
    suites_list = []
    
    # Run tests
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    runner.run(big_suite)