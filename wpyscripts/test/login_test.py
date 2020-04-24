#-*- coding: UTF-8 -*-
__author__ = 'alexkan'


import unittest

from wpyscripts.manager import *

logger=logging.getLogger("wetest")

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.device = get_device()

    def test_login(self):
        self.device.login_qq_wechat_wait(120)