import unittest
from tcxparser import TCXParser


class TestParseTCX(unittest.TestCase):

    def setUp(self):
        tcx_file = 'test.tcx'
        self.tcx = TCXParser(tcx_file)

    def test_latitude_is_correct(self):
        self.assertEquals(self.tcx.latitude, 35.951880198)

    def test_longitude_is_correct(self):
        self.assertEquals(self.tcx.longitude, -79.0931872185)

    def test_activity_type_is_correct(self):
        self.assertEquals(self.tcx.activity_type, 'running')

    def test_completion_time_is_correct(self):
        self.assertEquals(self.tcx.completed_at, '2012-12-26T22:03:05Z')

    def test_distance_is_correct(self):
        self.assertEquals(self.tcx.distance, 4686.31103516)

    def test_distance_units_is_correct(self):
        self.assertEquals(self.tcx.distance_units, 'meters')

    def test_duration_is_correct(self):
        self.assertEquals(self.tcx.duration, 1992.78)

    def test_calories_is_correct(self):
        self.assertEquals(self.tcx.calories, 379)
        
    def test_hr_max(self):
        self.assertEquals(self.tcx.hr_max, 189)

    def test_hr_min(self):
        self.assertEquals(self.tcx.hr_min, 60)

    def test_hr_avg(self):
        self.assertEquals(self.tcx.hr_avg, 156)
        
    def test_pace(self):
        self.assertEquals(self.tcx.pace, '07:05')
    
    def test_altitude_avg_is_correct(self):
        self.assertAlmostEqual(self.tcx.altitude_avg, 172.020056184)

if __name__ == '__main__':
    unittest.main()
