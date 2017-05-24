import sys, os, re, shutil, unittest, doctest
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

def get_version():
    if os.path.isdir('docs'):
        NS = {}
        version_re = re.compile(r'^version\s*=.*$',re.M)
        with open(os.path.join('docs','source','conf.py'),'r') as f:
            txt = f.read()
        m = version_re.search(txt)
        if not m:
            raise ValueError('Cannot find version in docs/source/conf.py')
        sv = m.group()
        exec m.group() in NS
        docs_version = NS['version']
    else:
        docs_version = 'unknown'
    if os.path.isdir('athlib'):
        NS = {}
        version_re = re.compile(r'^__version__\s*=.*$',re.M)
        with open(os.path.join('athlib','__init__.py'),'rb') as f:
            txt = f.read()
        m = version_re.search(txt)
        if not m:
            raise ValueError('Cannot find version in docs/source/conf.py')
        sv = m.group()
        exec m.group() in NS
        athlib_version = NS['__version__']
        if docs_version!='unknown' and athlib_version!=docs_version:
            i0 = m.start()
            i1 = m.end()
            txt = txt[:i0]+('__version__ = %r' % docs_version)+txt[i1:]
            with open(os.path.join('athlib','__init__.py'),'wb') as f:
                f.write(txt)
        else:
            docs_version = athlib_version
    return docs_version

def find_json(top,drop=1,force=False):
    for p,D,F in os.walk(top):
        for f in F:
            fn = os.path.join(p,f)
            with open(fn,'rb') as j:
                json = j.read()
            if force or schema_marker_re.search(json):
                if drop:
                    fn = os.sep.join(fn.split(os.sep)[drop:])
                yield fn

here = os.getcwd()
base = os.path.dirname(os.path.abspath(__file__))
schema_marker_re = re.compile(r'''(?P<q>["'])\$schema(?P=q)\s*:''',re.M)

os.chdir(base)
jschdir = os.path.join('athlib','json-schemas')
try:
    if 'sdist' in sys.argv:
        if os.path.isdir(jschdir):
            shutil.rmtree(jschdir)
        shutil.copytree('json',jschdir)
        shutil.copyfile('README.md','README.rst')
    setup(
        name="athlib",
        version=get_version(),
        packages=find_packages(),
        package_data={'athlib':(list(find_json(os.path.join('athlib','json-schemas')))
                                +list(find_json(os.path.join('athlib','wma'),force=True)))},
        test_suite="setup.my_test_suite",

        # metadata for upload to PyPI
        author="Andy Robinson and others",
        author_email="andy@reportlab.com",
        description="Utilities for track and field athletics",
        license="Apache",
        keywords="athletics track field",
        url="https://github.com/openath/athlib",   # project home page, if any
        install_requires=[
                'jsonschema>=2.6.0',
                'python-dateutil',
                ],
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Utilities',
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
    try:
        os.remove('README.rst')
    except:
        pass
    os.chdir(here)
