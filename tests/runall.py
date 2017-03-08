'''utilities to assist running the tests'''
import sys, os
from unittest import TestCase
from athlib.utils import _rootdir

class AthlibTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        me = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.__sys_path__ = sys.path[:]
        sys.path.insert(0, _rootdir)
        cls.__here__ = os.getcwd()
        os.chdir(me)

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.__here__)
        sys.path[:] = cls.__sys_path__

def main():
    was_here = os.getcwd()
    try:
        import unittest
        import doctest
        import sys
        sys.path.insert(0, _rootdir)
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover('tests', pattern='test_*.py')

        from athlib.wma import agegrader
        test_suite.addTests(doctest.DocTestSuite(agegrader))

        from athlib import utils
        test_suite.addTests(doctest.DocTestSuite(utils))

        from athlib import codes
        test_suite.addTests(doctest.DocTestSuite(codes))
        unittest.TextTestRunner().run(test_suite)
    finally:
        os.chdir(was_here)

if __name__ == '__main__':
    main()
