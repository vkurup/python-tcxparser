import os
from unittest import TestCase

from tcxparser import TCXParser


class TestParseCyclingTCX(TestCase):
    def setUp(self):
        """
        TCX file test2.tcx was taken from the following dataset:
        S. Rauter, I. Jr. Fister, I. Fister. A collection of sport activity files
        for data analysis and data mining.
        Technical report 0201, University of Ljubljana and University of Maribor, 2015.
        """
        tcx_file = "test2.tcx"
        path = os.path.join(os.path.dirname(__file__), "files", tcx_file)
        self.tcx = TCXParser(path)

    def test_cadence_max_is_correct(self):
        self.assertEqual(self.tcx.cadence_max, 115)

    def test_cadence_avg_is_correct(self):
        self.assertEqual(self.tcx.cadence_avg, 82)

    def test_power_avg_is_correct(self):
        self.assertEqual(self.tcx.power_avg, 146)

    def test_power_max_is_correct(self):
        self.assertEqual(self.tcx.power_max, 419)
