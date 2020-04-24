# -*- coding: UTF-8 -*-
"""
    GAutomator与Cube结合脚本示例，本示例为单个场景测试内容，需要在main_perform.py中的 cube_run()函数中增加执行调用。

    自动化测试与原GAutomator完全一致，主要变化在流程控制上。

    示例中，仅需要修改   scene_name、run()函数的执行内容。

    @:param scene_name: 当前测试场景名称
    @:param runner.run(): 自动化测试内容，根据场景不同使用不同的自动化脚本。
"""
from testcase import MyTestAPI, runner

__author__ = 'guoruihe'

from main_perform import *


scene_name = "team_prop_game"  # 当次测试场景名称


def _native_prepare():
    # 本地环境准备，清楚数据，拉起游戏
    device = manager.get_device()
    # device._clear_cubex_data()
    device._clear_qq_account()
    device._clear_user_info(local_package)
    time.sleep(10)
    return True


def _cube_prepare(testtype, comment=""):

    result = start_service("com.tencent.cubex/com.tencent.cubex.service.CubeService")
    # print(result)
    if result == -1:
        raise WeTestRuntimeError("No service to start!")

    cube_client.connect_cube(user_name)

    # ret = cube_client.begin_cube_test(local_package, scene_name, testtype, CubeSnapshots.OPEN)
    if testtype == 5:
        ret = cube_client.begin_unity_test(local_package, scene_name, testtype, CubeSnapshots.CLOSE, Before5and6.BEFORE)
    else:
        ret = cube_client.begin_cube_test(local_package, scene_name, testtype, CubeSnapshots.OPEN)

    if ret is None:
        return False
    else:
        return True


def _cube_finish_test():
    cube_client.stop_cube_test()
    cube_client.upload_record()


def _prepare(test_type):
    # 准备工作
    # 清理QQ、微信账号，清理游戏数据确保每次启动的逻辑是一样的。然后，拉起游戏
    # 每次启动的时候杀掉cubex
    os.system("adb shell am force-stop com.tencent.cubex")
    env = os.environ.get("PLATFORM_IP")
    logger = manager.get_logger()
    lanuch_result =  _native_prepare()
    lanuch_result = lanuch_result and _cube_prepare(test_type)
    # cube性能测试服务拉起、准备阶段

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


def run(test_type):
    prepare = _prepare(test_type)
    logger = manager.get_logger()
    reporter = manager.get_reporter()
    if not prepare:
        reporter.screenshot()
        logger.error("Connect to sdk fail,please config your game contain sdk or not in the first scene")
        return
    try:
        """此处添加当次测试的内容"""
        # runner.run()  # 根据不同测试场景需求，修改该部分内容。

        import testcase.MyTestAPI as nsss
        # 1. 登录游戏，选服，进入游戏大厅
        nsss.login_qq(test_type)

        time.sleep(5)
        nsss.high_debug()

        nsss.select_section(2)
        new_player = nsss.enter_gamecenter()
        if new_player == 0:
            nsss.skip_newer_tech()
            nsss.exit_server()
            nsss.enter_gamecenter()
            nsss.dress()
        # 全不同装扮宠物设置

        # 2. 开始单局，打桩标记
        # nsstest.random_start("ECGMT_PROP_SINGLE_GAME")

        # 临时
        for i in range(2):
            nsss.create_game_room("ECGMT_PROP_TEAM_GAME", 11)
            print "create room ok"
            nsss.wait_for_start()
            print "wait_for_start ok"
            # 单局开始托管并标记
            nsss.tuoguan()
            # 起始点打标记
            cube_client.mark_tag()

            # 结束标记
            time.sleep(150)
            print 'stop mark1'
            cube_client.mark_tag()

            # 回到房间
            nsss.wait_room()
            time.sleep(20)

    except WeTestRuntimeError as e:
        stack = traceback.format_exc()
        logger.exception(stack)
    finally:
        logger.debug("stop cube...")
        _cube_finish_test()
