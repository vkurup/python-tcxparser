from StringIO import StringIO
import unittest

from tcxparser import TCXParser


class TestParseTCX(unittest.TestCase):

    def setUp(self):
        tcx_file = 'test2.tcx'
        self.tcx = TCXParser(tcx_file)

    def test_cadence_max_is_correct(self):
        self.assertEquals(self.tcx.cadence_max, 115)

    def test_cadence_avg_is_correct(self):
        self.assertEquals(self.tcx.cadence_avg, 82)

if __name__ == '__main__':
    unittest.main()
