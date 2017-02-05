"Execute all the Python tests"
import unittest
import doctest


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')

    from athlib.wma import agegrader
    test_suite.addTests(doctest.DocTestSuite(agegrader))

    from athlib import utils
    test_suite.addTests(doctest.DocTestSuite(utils))

    from athlib import codes
    test_suite.addTests(doctest.DocTestSuite(codes))

    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner().run(my_test_suite())
