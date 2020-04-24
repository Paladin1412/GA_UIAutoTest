# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'

import os
import traceback
import time
import logging
import wpyscripts.manager as manager
from wpyscripts.common.wetest_exceptions import *

logger = logging.getLogger("wetest")

print(os.environ)

local_package = "com.tencent.tmgp.apollo"  # 你需要测试的包名
user_name = '13124'

import cube_manager as manager

def _prepare():
    global cube_client
    result = manager.start_service("com.tencent.cubex/com.tencent.cubex.service.CubeService")
    # print(result)
    if result == -1:
        raise WeTestRuntimeError("No service to start!")

    cube_client = manager.get_cube_client()

    cube_client.connect_cube(user_name)


def _begin_test():
    cube_client.begin_cube_test(local_package)
    time.sleep(10)
    cube_client.stop_cube_test()
    time.sleep(5)
    cube_client.delete_record()
    time.sleep(5)


def _mark_scene():
    cube_client.begin_cube_test(local_package)
    time.sleep(10)
    cube_client.scene_tag()
    time.sleep(5)
    cube_client.scene_tag()
    time.sleep(5)
    cube_client.scene_tag()
    time.sleep(5)
    cube_client.scene_tag()
    time.sleep(5)
    cube_client.stop_cube_test()
    time.sleep(5)
    cube_client.delete_record()
    time.sleep(5)


def _upload_record():
    cube_client.begin_cube_test(local_package)
    time.sleep(20)
    cube_client.scene_tag()
    time.sleep(5)
    cube_client.scene_tag()
    time.sleep(5)
    cube_client.stop_cube_test()
    time.sleep(5)
    cube_client.upload_record()
    time.sleep(5)


def _recover_data():
    cube_client.begin_cube_test(local_package)
    time.sleep(20)
    cube_client.stop_cube_test()
    time.sleep(5)
    cube_client.recover_data()
    time.sleep(1)
    cube_client.begin_cube_test(local_package)
    time.sleep(20)
    cube_client.stop_cube_test()
    time.sleep(5)
    cube_client.upload_record()
    time.sleep(5)


def _finish():
    pass

def main():
    try:
        _prepare()
        # _begin_test()

        _mark_scene()

    except Exception as e:
        traceback.print_exc()
        stack = traceback.format_exc()
        logger.error(stack)
    finally:
        _finish()

main()