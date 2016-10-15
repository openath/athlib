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

If you want to hack on athlib, look there too.  We'll move some things from below shortly, and try to keep this README very short.

## Age Groups
The first Python function included has been in use in our entry system for 2 years, and has a reasonable number of tests.  It just works out age groups from a competition date and birth date.   There are three supported categories: XC, ROAD and TF.

    >>> from athlib.uka.agegroups import calc_age_group
    >>> from datetime import date
    >>> calc_age_group(date(1966,3,21), date(2015,1,3), "XC", vets=False)
    'SEN'
    >>> calc_age_group(date(2000,1,1), date(2015,1,3), "XC", vets=False)
    'U15'
    >>> 

The optional vets argument says whether those over 35 should return a WMA age grade (V45 etc), or just "SEN" for senior

## IAAF scores

These are available in Javascript, as well as Python.

## Next steps - update the documentation, so that it's auto-generated from the code

 - Publish on PyPI
 - Work out a testing approach for the Javascript
 - Work out the best way to package and ship, and have on a CDN, for the javascript portions
