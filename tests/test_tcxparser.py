import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from unittest import TestCase

from tcxparser import TCXParser


class TestParseTCX(TestCase):

    def setUp(self):
        tcx_file = 'test.tcx'
        path = os.path.join(os.path.dirname(__file__), 'files', tcx_file)
        self.tcx = TCXParser(path)

    def test_hr_values_are_correct(self):
        self.assertEqual(self.tcx.hr_values()[0], 62)
        self.assertEqual(self.tcx.hr_values()[-1], 180)

    def test_altitude_points_are_correct(self):
        self.assertEqual(self.tcx.altitude_points()[0], 178.942626953)
        self.assertEqual(self.tcx.altitude_points()[-1], 166.4453125)

    def test_time_values_are_correct(self):
        self.assertEqual(self.tcx.time_values()[0], '2012-12-26T21:29:53Z')
        self.assertEqual(self.tcx.time_values()[-1], '2012-12-26T22:03:05Z')

    def test_latitude_is_correct(self):
        self.assertEqual(self.tcx.latitude, 35.951880198)

    def test_longitude_is_correct(self):
        self.assertEqual(self.tcx.longitude, -79.0931872185)

    def test_activity_type_is_correct(self):
        self.assertEqual(self.tcx.activity_type, 'running')

    def test_started_at_is_correct(self):
        self.assertEqual(self.tcx.started_at, '2012-12-26T21:29:53Z')

    def test_completion_time_is_correct(self):
        self.assertEqual(self.tcx.completed_at, '2012-12-26T22:03:05Z')

    def test_distance_is_correct(self):
        self.assertEqual(self.tcx.distance, 4686.31103516)

    def test_distance_units_is_correct(self):
        self.assertEqual(self.tcx.distance_units, 'meters')

    def test_duration_is_correct(self):
        self.assertEqual(self.tcx.duration, 1992.78)

    def test_calories_is_correct(self):
        self.assertEqual(self.tcx.calories, 379)

    def test_hr_max(self):
        self.assertEqual(self.tcx.hr_max, 189)

    def test_hr_min(self):
        self.assertEqual(self.tcx.hr_min, 60)

    def test_hr_avg(self):
        self.assertEqual(self.tcx.hr_avg, 156)

    def test_pace(self):
        self.assertEqual(self.tcx.pace, '07:05')

    def test_altitude_avg_is_correct(self):
        self.assertAlmostEqual(self.tcx.altitude_avg, 172.020056184)

    def test_altitude_max_is_correct(self):
        self.assertAlmostEqual(self.tcx.altitude_max, 215.95324707)

    def test_altitude_min_is_correct(self):
        self.assertAlmostEqual(self.tcx.altitude_min, 157.793579102)

    def test_ascent_is_correct(self):
        self.assertAlmostEqual(self.tcx.ascent, 153.80981445)

    def test_descent_is_correct(self):
        self.assertAlmostEqual(self.tcx.descent, 166.307128903)

    def test_activity_notes_is_correct(self):
        self.assertEqual(self.tcx.activity_notes, 'Aerobics')

    def test_position_values_are_correct(self):
        values = self.tcx.position_values()
        self.assertAlmostEqual(values[-1][0], 35.9519544616)
        self.assertAlmostEqual(values[-1][1], -79.0930143837)

    def test_distance_values_are_correct(self):
        self.assertAlmostEqual(self.tcx.distance_values()[0], 0.0)
        self.assertAlmostEqual(self.tcx.distance_values()[-1], 4686.31103516)


class BugTest(TestCase):

    def test_single_trackpoint_in_track_is_ok(self):
        "https://github.com/vkurup/python-tcxparser/issues/9"
        xml = """
        <TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2">
          <Activities>
            <Activity>
              <Lap>
                <Track>
                  <Trackpoint>
                    <DistanceMeters>5</DistanceMeters>
                  </Trackpoint>
                </Track>
              </Lap>
            </Activity>
          </Activities>
        </TrainingCenterDatabase>
        """
        tcx_file = StringIO(xml)
        tcx = TCXParser(tcx_file)
        self.assertEqual(tcx.distance, 5)

    def test_no_error_if_no_position(self):
        "https://github.com/vkurup/python-tcxparser/issues/11"
        xml = """
        <TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2">
          <Activities>
            <Activity>
              <Lap>
                <Track>
                  <Trackpoint>
                    <DistanceMeters>5</DistanceMeters>
                  </Trackpoint>
                </Track>
              </Lap>
            </Activity>
          </Activities>
        </TrainingCenterDatabase>
        """
        tcx_file = StringIO(xml)
        tcx = TCXParser(tcx_file)
        self.assertEqual(tcx.latitude, None)
        self.assertEqual(tcx.longitude, None)
