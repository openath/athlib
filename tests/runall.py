'''utilities to assist running the tests'''
import sys
import os
from unittest import TestCase
isPy3 = sys.version_info[0] == 3
_rootdir = os.path.dirname(os.path.abspath(__file__))
_rootdir = os.path.normpath(os.path.join(_rootdir, '..'))

if isPy3:
    import builtins
    lexec = getattr(builtins, 'exec')
else:
    def lexec(obj, G=None, L=None):
        if G is None:
            frame = sys._getframe(1)
            G = frame.f_globals
            if L is None:
                L = frame.f_locals
            del frame
        elif L is None:
            L = G
        exec("""exec obj in G, L""")


def localpath(relpath):
    return os.path.join(_rootdir, relpath)


class AthlibTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__sys_path__ = sys.path[:]
        sys.path.insert(0, _rootdir)
        cls.__here__ = os.getcwd()
        os.chdir(_rootdir)

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.__here__)
        sys.path[:] = cls.__sys_path__


def main():
    was_here = os.getcwd()
    try:
        os.chdir(_rootdir)
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
