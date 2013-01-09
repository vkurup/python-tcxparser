import unittest
from tcxparser import TcxParser


class TestParseTcx(unittest.TestCase):

    def setUp(self):
        tcx_file = 'test.tcx'
        self.tcx = TcxParser(tcx_file)

    def test_latitude_is_correct(self):
        self.assertEquals(self.tcx.latitude(), 35.951880198)

    def test_longitude_is_correct(self):
        self.assertEquals(self.tcx.longitude(), -79.0931872185)

    def test_activity_type_is_correct(self):
        self.assertEquals(self.tcx.activity_type(), 'running')

    def test_completion_time_is_correct(self):
        self.assertEquals(self.tcx.completed_at(), '2012-12-26T22:03:05Z')

    def test_distance_is_correct(self):
        self.assertEquals(self.tcx.distance(), 4686.31103516)

    def test_distance_units_is_correct(self):
        self.assertEquals(self.tcx.distance_units(), 'meters')

    def test_duration_is_correct(self):
        self.assertEquals(self.tcx.duration(), 1992.78)

    def test_calories_is_correct(self):
        self.assertEquals(self.tcx.calories(), 379)

if __name__ == '__main__':
    unittest.main()
