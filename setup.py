from setuptools import setup, find_packages
setup(
    name = "athlib",
    version = "0.0.1",
    packages = find_packages(),
    test_suite="athlib",

    # metadata for upload to PyPI
    author = "Andy Robinson and others",
    author_email = "andy@reportlab.com",
    description = "Utilities for track and field athletics",
    license = "Apache",
    keywords = "athletics track field",
    url = "https://github.com/openath/athlib",   # project home page, if any    
)