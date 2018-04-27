import os
from unittest import TestCase

from tcxparser import TCXParser


class TestParseCyclingTCX(TestCase):

    def setUp(self):
        tcx_file = 'test2.tcx'
        path = os.path.join(os.path.dirname(__file__), 'files', tcx_file)
        self.tcx = TCXParser(path)

    def test_cadence_max_is_correct(self):
        self.assertEqual(self.tcx.cadence_max, 115)

    def test_cadence_avg_is_correct(self):
        self.assertEqual(self.tcx.cadence_avg, 82)
