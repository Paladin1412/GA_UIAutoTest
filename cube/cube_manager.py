# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'

import os
import logging
import wpyscripts.common.adb_process as adb
from cube_client import *
import wpyscripts.common.platform_helper as platform

_local_client_port=53003
_cube_port=59999


env = os.environ.get("PLATFORM_IP")
hostip = os.environ.get("PLATFORM_IP", "127.0.0.1")
platform_port = os.environ.get("PLATFORM_PORT")
logger = logging.getLogger("wetest")

def _platform_forward(remote_port):
    """
        在wetest平台运行时，forward映射的端口交由平台分配并且实现映射
    :param remote_port:
    :return:
    """
    platform_client = platform.get_platform_client()
    response = platform_client.platform_forward(remote_port)
    return response["localPort"]

def start_service(service_name):
    for retry in range(0, 2):
        file = os.popen("adb shell am startservice {0}".format(service_name)) #  com.tencent.cubex/com.tencent.cubex.service.CubeService
        file.readline()
        result = 0
        while 1:
            line = file.readline()
            logger.debug(line)
            if not line:
                result = 1
                break
            else :
                if "Error" in line:
                    result = -1
        if result == 1:
            break
    return result


def get_cube_client():
    if get_cube_client.instance:
        return get_cube_client.instance

    global _local_client_port

    if not env:
        adb.forward(_local_client_port, _cube_port)
    else:
        _local_client_port = _platform_forward(_cube_port)
    local_port = int(_local_client_port)

    get_cube_client.instance = CubeClient(hostip, local_port)
    return get_cube_client.instance

get_cube_client.instance = None

cube_client = get_cube_client()