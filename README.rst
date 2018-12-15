python-tcxparser
================

.. image:: https://img.shields.io/pypi/v/python-tcxparser.svg
    :target: https://pypi.python.org/pypi/python-tcxparser
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/vkurup/python-tcxparser.svg?branch=master
   :target: https://travis-ci.org/vkurup/python-tcxparser
   :alt: Latest Travis CI build status

.. image:: https://pyup.io/repos/github/vkurup/python-tcxparser/shield.svg
   :target: https://pyup.io/repos/github/vkurup/python-tcxparser/
   :alt: Requirement Updates

.. image:: https://codecov.io/gh/vkurup/python-tcxparser/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/vkurup/python-tcxparser
   :alt: Code Coverage


python-tcxparser is a minimal parser for Garmin's TCX file format. It
is not in any way exhaustive. It extracts just enough data to allow me
to post data from my Garmin ForeRunner 410 watch to
`DailyMile's <http://dailymile.com>`_ API.

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

Compatibility
-------------

* Python 2.7 or 3.6+

License
-------

* BSD

Contact
-------

Please contact me with any questions: Vinod Kurup (vinod@kurup.com)
