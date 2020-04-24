#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'


import unittest

from wpyscripts.manager import *

logger=logging.getLogger("wetest")

class ReportTest(unittest.TestCase):
    def setUp(self):
        self.report=get_reporter()

    def test_add_tag(self):
        self.report.add_start_scene_tag("GameStart")
        self.report.add_end_scene_tag("GameStart")

    def test_capture_and_mark(self):
        self.report.capture_and_mark(1416.97973633,830.564605713)


    def test_screen_shot(self):
        logger.debug("test_screen_shot")
        self.report.screenshot()
