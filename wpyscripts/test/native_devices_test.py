#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import unittest

from wpyscripts.manager import *

logger=logging.getLogger("wetest")

class DeviceTest(unittest.TestCase):

    def setUp(self):
        self.device=get_device()


    def test_get_display_size(self):
        size=self.device.get_display_size()
        if size:
            logger.debug("width : {0},height : {1}".format(size.width,size.height))

    def test_get_top_package_activity(self):
        top_activity=self.device.get_top_package_activity()
        if top_activity:
            logger.debug(top_activity)

    # def test_back(self):
    #     self.device.back()

    # def test_login_qq(self):
    #     self.device._clear_qq_account()
    #     result=self.device.login_qq_wechat_wait()
    #     if result:
    #         logger.debug("Login OK")
    #     else:
    #         logger.debug("Login error")


    # def test_launch_app(self):
    #     pid,launchtime=self.device._launch_app("com.tencent.buggame")
    #     logger.debug("pid = {0},launchtime = {1}".format(pid,launchtime))
