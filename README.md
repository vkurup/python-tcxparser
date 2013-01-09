# python-tcxparser

python-tcxparser is a minimal parser for Garmin's TCX file format. It
is not in any way exhaustive. It extracts just enough data to allow me
to post data from my Garmin ForeRunner 410 watch to
[DailyMile's](http://dailymile.com) API.

Data extracted:
 - latitude & longitude of start point of workout
 - type of workout (running, walking, etc)
 - time of completion of workout (in ISO UTC)
 - distance of workout (in meters)
 - duration of workout (in seconds)
 - calories burned during workout (as estimated by device)

## Installation

    pip install python-tcxparser

## Usage

    >>> import tcxparser
    >>> tcx = tcxparser.TcxParser('/home/vinod/Downloads/20121226-212953.tcx')
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

## Contact
Please contact me with any questions: Vinod Kurup (vinod@kurup.com)
