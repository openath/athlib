# athlib

Athlib is a library of functions, data and schema for Athletics (i.e. Track and Field)

We're building lots of sites for the sport of athletics.  When we find something common and testable, we aim to place it here.   This library should contain

 - static reference data, provided it's not huge nor available elsewhere
 - Python code implementing functions of general interest
 - Javascript code implementing functions of general interest

 
It is NOT intended to contain 
 - web applications, view code or database code.
 - competition management software

Things we hope to put in here:

 - standard event codes and their English names
 - UKA and other age group calculators
 - WMA age grade calculations
 - utilities for parsing and formatting performances as commonly input in athletics
 - standardised scoring functions
 - sample JSON files in line with our schemas
 - schemas to validate 

# Installation

For the Python version, it should be just

    pip install athlib

If working on this source, you'll need to ensure the inner package (./athlib) is on your path, so that you can execute "import athlib"

# Documentation
...can be found at http://athlib.readthedocs.org/

# Contributing

## Python development

For Python developers, please install the extra development requirements with
```
pip install -r dev_requirements.txt
```
Run tests with...

```
python setup.py test
```

Check style with 
```
pycodestyle --exclude=bin,lib,include,sampledata
```

You can also copy the file `pre-commit.sample` to `.git/hooks/pre-commit`, and the two above checks will be run before any commit, and block it if they return issues.

## Javascript development

We're discussing the Javascript toolchain.  

## Next steps - update the documentation, so that it's auto-generated from the code

 - Fix up JSON directory structure and schemata
 - Publish on PyPI
 - Work out a testing approach for the Javascript
 - Work out the best way to package and ship, and have on a CDN, for the javascript portions
