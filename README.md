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

# Documentation

The main documentation is [over here](http://opentrack.run/athlib/build/html/index.html).   What follows below is intended to help people working on athlib; if you are not an experience Python or Javascript developer,
please head over there.




# Python documentation

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

# Javascript documentation

    npm install athlib

Browser links coming soon

## Javascript development

We have a complete Javascript environment in the "js/" subdirectory.  This is lifted from someone else's library boilerplate.  

    npm run build    # build for node
    npm run build-web  # build for browser
    npm run test   # tests running in console.

We'd welcome help modernising this.  It uses Webpack 1 and gulp.  The authors are a bit out of their depth here a.

# Documentation itself

The docs are written using reStructured Text, the Python standard.  There is an environment
in `docs`.  
  
    cd docs
    make html
    
