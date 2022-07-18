import os
from unittest import TestCase

from tcxparser import TCXParser


class TestSupTCX(TestCase):
    def setUp(self):
        """
        TCX file sup_activity_1.tcx was taken from the following repository:
        https://github.com/firefly-cpp/tcx-test-files
        """
        tcx_file = "sup_activity_1.tcx"
        path = os.path.join(os.path.dirname(__file__), "files", tcx_file)
        self.tcx = TCXParser(path)

    def test_total_steps(self):
        self.assertEqual(self.tcx.total_steps, 491)
