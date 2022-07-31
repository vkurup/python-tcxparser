python-tcxparser
================

.. sidebar:: Build Status

   :master: |master-status|

.. image:: https://pyup.io/repos/github/vkurup/python-tcxparser/shield.svg
   :target: https://pyup.io/repos/github/vkurup/python-tcxparser/
   :alt: Requirement Updates

.. image:: https://img.shields.io/fedora/v/python3-tcxparser?color=blue&label=Fedora%20Linux&logo=fedora
   :target: https://src.fedoraproject.org/rpms/python-tcxparser
   :alt: Fedora package

.. |master-status| image::
    https://github.com/vkurup/python-tcxparser/workflows/lint-test/badge.svg?branch=master
    :alt: Build Status
    :target: https://github.com/vkurup/python-tcxparser/actions?query=branch%3Amaster

python-tcxparser is a minimal parser for Garmin's TCX file format. It
is not in any way exhaustive.

Data extracted:
 - latitude & longitude of start point of workout
 - type of workout (running, walking, etc)
 - time of completion of workout (in ISO UTC)
 - distance of workout (in meters)
 - duration of workout (in seconds)
 - calories burned during workout (as estimated by device)
 - average, max and min heart rate during workout
 - average pace during workout
 - average altitude during workout
 - ascent and descent of workout
 - max and min altitude
 - time stamp of each data point (in ISO UTC)
 - average and max cadence (cycling activities)
 - percentage and time spent in heart rate zone
 - average and max power
 - total steps (also strokes)

Installation
------------

Install it from PyPI::

   pip install python-tcxparser

Usage
-----

Basic usage example::

    >>> import tcxparser
    >>> tcx = tcxparser.TCXParser('/home/vinod/Downloads/20121226-212953.tcx')
    >>> # Duration of workout in seconds
    ... tcx.duration
    1992.78
    >>> # latitude/longitude at start of workout
    ... tcx.latitude
    35.951880198
    >>> tcx.longitude
    -79.0931872185
    >>> tcx.activity_type
    'running'
    >>> # ISO UTC timestamp when workout completed
    ... tcx.completed_at
    '2012-12-26T22:03:05Z'
    >>> # distance of workout in meters
    ... tcx.distance
    4686.31103516
    >>> tcx.distance_units
    'meters'
    >>> # calories burned (as reported by device)
    ... tcx.calories
    379
    >>> # percentage of workout spent in each user-defined heart rate zone
    ... tcx.hr_percent_in_zones({"Z0": (0, 99), "Z1": (100, 129), "Z2": (130, 200)})
    {"Z0": 14, "Z1": 36, "Z2": 50}

Compatibility
-------------

* Python 3.7+, see `tox.ini`_.

.. _tox.ini: tox.ini

License
-------

* BSD


Maintainer Information
----------------------

We use Github Actions to lint (using pre-commit, black, isort, and flake8),
test (using tox and tox-gh-actions), and calculate coverage (using coverage).

We have a local script to do these actions locally, named ``maintain.sh``::

  $ ./maintain.sh

A Github Action workflow also builds and pushes a new package to PyPI whenever a new
Release is created in Github. This uses a project-specific PyPI token, as described in
the `PyPI documentation here <https://pypi.org/help/#apitoken>`_. That token has been
saved in the ``PYPI_PASSWORD`` settings for this repo, but has not been saved anywhere
else so if it is needed for any reason, the current one should be deleted and a new one
generated.

As always, be sure to bump the version in ``setup.py`` before creating a Release, so
that the proper version gets pushed to PyPI.


Contact
-------

Please contact me with any questions: Vinod Kurup (vinod@kurup.com)
