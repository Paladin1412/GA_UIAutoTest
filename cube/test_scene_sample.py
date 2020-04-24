# -*- coding: UTF-8 -*-
"""
    GAutomator与Cube结合脚本示例，本示例为单个场景测试内容，需要在main_perform.py中的 cube_run()函数中增加执行调用。

    自动化测试与原GAutomator完全一致，主要变化在流程控制上。

    示例中，仅需要修改   scene_name、run()函数的执行内容。

    @:param scene_name: 当前测试场景名称
    @:param runner.run(): 自动化测试内容，根据场景不同使用不同的自动化脚本。
"""

__author__ = 'guoruihe'

from main_perform import *


scene_name = "test_scene_sample" # 当次测试场景名称


def _native_prepare():
    # 本地环境准备，清楚数据，拉起游戏
    device = manager.get_device()
    device._clear_qq_account()
    device._clear_user_info(local_package)
    time.sleep(10)
    return True


def _cube_prepare(comment=""):

    result = start_service("com.tencent.cubex/com.tencent.cubex.service.CubeService")
    # print(result)
    if result == -1:
        raise WeTestRuntimeError("No service to start!")

    cube_client.connect_cube(user_name)

    ret = cube_client.begin_cube_test(local_package, scene_name, CubeTestLevel.LIGHT, CubeSnapshots.OPEN)
    if ret is None:
        return False
    else:
        return True


def _cube_finish_test():
    cube_client.stop_cube_test()
    cube_client.upload_record()


def _prepare():
    # 准备工作
    # 清理QQ、微信账号，清理游戏数据确保每次启动的逻辑是一样的。然后，拉起游戏
    env = os.environ.get("PLATFORM_IP")
    logger = manager.get_logger()
    lanuch_result =  _native_prepare()
    lanuch_result = lanuch_result and _cube_prepare() # cube性能测试服务拉起、准备阶段

    if lanuch_result:
        # 拉起成功，通常游戏会有一段过场动画，这时候并不一定会启动我们这边的sdk，我们需要不断的尝试连接SDK。如果,连接成功获取sdk版本号则游戏已经启动
        logger.debug("Launch package {0} SUCCESS,try to connect U3DAutomation SDK".format(os.environ["PKGNAME"]))
        global engine
        engine = manager.get_engine()
        version = None
        for i in range(30):
            try:
                version = engine.get_sdk_version()
                if version:
                    logger.debug(version)
                    manager.save_sdk_version(version)
                    return True
            except:
                time.sleep(2)
    return False


def run():
    prepare = _prepare()
    logger = manager.get_logger()
    reporter = manager.get_reporter()
    if not prepare:
        reporter.screenshot()
        logger.error("Connect to sdk fail,please config your game contain sdk or not in the first scene")
        return
    try:
        """此处添加当次测试的内容"""
        import testcase.runner as runner
        runner.run()  # 根据不同测试场景需求，修改该部分内容。

        import testcase.MyTestAPI as nsstest
        # 1. 登录游戏，选服，进入游戏大厅
        nsstest.login()
        nsstest.select_section(34)
        nsstest.enter_gamecenter()

        #2. 开始单局，打桩标记
        nsstest.random_start("ECGMT_PROP_SINGLE_GAME")
        cube_client.mark_tag()

        # 3.等待单局结束，打桩标记
        nsstest.wait_until_end()
        cube_client.mark_tag()

        # 4.退出游戏
        nsstest.exit_game()

        time.sleep(10)

    except WeTestRuntimeError as e:
        stack = traceback.format_exc()
        logger.exception(stack)
    finally:
        _cube_finish_test()
