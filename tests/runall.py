'''utilities to assist running the tests'''
import os
_rootdir = os.path.dirname(os.path.abspath(__file__))
_rootdir = os.path.normpath(os.path.join(_rootdir,'..'))

def localpath(relpath):
    return os.path.join(_rootdir,relpath)

def main():
    was_here = os.getcwd()
    try:
        os.chdir(_rootdir)
        import unittest, doctest, sys
        sys.path.insert(0,_rootdir)
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

if __name__=='__main__':
    main()
