# athlib
A library of functions, data and schema for Athletics (i.e. Track and Field)

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

## Next steps - 11th June
Currently we have just the IAAF scores in Javascript.

 - Add some tested Python code (e.g. UKA age group calculations)
 - Publish on PyPI
 - Work out a testing approach for the Javascript
 - Work out the best way to package and ship, and have on a CDN, for the javascript portions