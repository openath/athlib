# Welcome to AthLib's documentation

Currently this is placeholder text.

AthLib is a library of functions for athletics - that's "track and field" to Americans.  It's part of the [OpenTrack](http://opentrack.run) project.

## Contributors

There's very little here yet but we are trying to set this up to be a model library in modern Python.    The author is a dinosaur doing Python since about 1994, who has at times tired of trying to follow all the latest and greatest
in Python deployment.   Feel free to point out things that are not as they should be.

To WORK on athlib, we suggest starting with

    pip install -r reqs_dev.txt

which will install the documentation, testing and packaging tools.  We're using mkdocs for documentation, and trying to follow the latest Python packaging guidelines from setuptools.

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
