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

What follows below is intended to help people working on athlib.

# Python documentation

We require a modern python>=3.8.0 some functions already have typing information and it will be applied later to others.

## Installation
    pip install athlib

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

# Javascript documentation & development

see the [documentation](js/README.md) in folder js 

# Documentation itself

The docs are written using reStructured Text, the Python standard.  There is an environment
in `docs`.  
  
    cd docs
    make html
    
