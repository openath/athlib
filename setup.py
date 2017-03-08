import os, re, shutil, unittest, doctest
from setuptools import setup, find_packages

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

def find_schemas(top,drop=1):
    for p,D,F in os.walk(top):
        if p==top and 'samples' in D:
            D.remove('samples')
        for f in F:
            fn = os.path.join(p,f)
            with open(fn,'rb') as j:
                json = j.read()
            if schema_marker_re.search(json):
                if drop:
                    fn = os.sep.join(fn.split(os.sep)[drop:])
                yield fn

here = os.getcwd()
base = os.path.dirname(os.path.abspath(__file__))
schema_marker_re = re.compile(r'''(?P<q>["'])\$schema(?P=q)\s*:''',re.M)

os.chdir(base)
jschdir = os.path.join('athlib','json-schemas')
try:
    if os.path.isdir(jschdir):
        shutil.rmtree(jschdir)
    shutil.copytree('json',jschdir)
    setup(
        name="athlib",
        version="0.0.2",
        packages=find_packages(),
        package_data={'athlib':list(find_schemas(os.path.join('athlib','json-schemas')))},
        test_suite="setup.my_test_suite",

        # metadata for upload to PyPI
        author="Andy Robinson and others",
        author_email="andy@reportlab.com",
        description="Utilities for track and field athletics",
        license="Apache",
        keywords="athletics track field",
        url="https://github.com/openath/athlib",   # project home page, if any
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache',
            'Topic :: Athletics',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            ],
        )
finally:
    if os.path.isdir(jschdir):
        shutil.rmtree(jschdir)
    os.chdir(here)
