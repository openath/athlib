import unittest
from setuptools import setup, find_packages

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    name = "athlib",
    version = "0.0.1",
    packages = find_packages(),
    test_suite="setup.my_test_suite",

    # metadata for upload to PyPI
    author = "Andy Robinson and others",
    author_email = "andy@reportlab.com",
    description = "Utilities for track and field athletics",
    license = "Apache",
    keywords = "athletics track field",
    url = "https://github.com/openath/athlib",   # project home page, if any    
)