#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import time
import os
import logging
from libs.uiauto.uiautomator import AutomatorDevice
from wpyscripts.common.adb_process import AdbTool

logger=logging.getLogger("wetest")

_device_port=9008
_uiautomator_port = os.environ.get("UIAUTOMATOR_PORT","19008")

def _init_uiautomator():
    """
        初始化uiautomator
    :return:
    """
    file_path = os.path.split(os.path.realpath(__file__))[0]
    uiautomator_stub_path = os.path.abspath(
        os.path.join(file_path, "..\\third\\libs\\uiAutomator\\uiautomator-stub.jar"))
    adb=AdbTool()
    print(adb.cmd_wait("push",uiautomator_stub_path,"/data/local/tmp"))

    logger.debug("Start UIAutomator")
    uiautomator_process=adb.cmd("shell","uiautomator","runtest","uiautomator-stub.jar","-c","com.github.uiautomatorstub.Stub")
    time.sleep(3)
    logger.debug("Exit uiautomator")
    adb.forward(_uiautomator_port,_device_port)


def _init():
    port = os.environ.get("UIAUTOMATORPORT")
    if port:
        return int(port)
    else:
        """
            本地，初始化UiAutomator
        """
        _init_uiautomator()
        return int(_uiautomator_port)


def get_uiautomator():
    if get_uiautomator.instance:
        return get_uiautomator.instance
    else:
        port=_init()
        get_uiautomator.instance = AutomatorDevice(None, port, os.environ.get("PLATFORM_IP", "127.0.0.1"), None)
        return get_uiautomator.instance

get_uiautomator.instance=None
