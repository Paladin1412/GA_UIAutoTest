# -*- coding: UTF-8 -*-
"""
main.py

main是自动化测试的起点，最大限度的对用户透明。

GAutomator最大的一个特点是，在本地运行与在wetest平台运行测试逻辑代码一致，对用户透明。通过环境变量“PLATFORM_IP”来判定在本地运行还是在wetest平台运行。
在wetest平台上运行的逻辑与本地运行的逻辑不相同。

main.py主要完成包括，清楚QQ、微信、游戏数据，拉起游戏，等待wetest sdk启动等工作。准备工作完成后，会调用testcase.runner.run函数，测试逻辑的起点

本地启动，只运行一台手机的:
usage:
    设置游戏包名，main.py往下，找到找到local_package = os.environ.get("PKGNAME", ""),设置包名，如找到local_package=com.tencent.wetest.demo
     python main.py

运行多台手机:
usage:
    "python main.py --qqname=2952020110 --qqpwd=wetestpwd --engineport=50031 --uiport=19000 --serial=saaaweadf"
    "python main.py --qqname=2952020111 --qqpwd=wetestpwd --engineport=50032 --uiport=19001 --serial=asdfadfadf"

    这两个命令会分别启动在序列号(adb devices查看)的手机上运行自动化.参数详见main()

"""
__author__ = 'minhuaxu,guoruihe'

import os
import traceback
import time
import getopt
import sys
import optparse
import wpyscripts.manager as manager
from wpyscripts.common.wetest_exceptions import *

from cube_manager import *
from cube_protocol import CubeTestLevel, CubeSnapshots

print(os.environ)

local_package = os.environ.get("PKGNAME", "com.tencent.tmgp.speedmobile")  # 你需要测试的包名,可以设置默认值
user_name = os.environ.get("USER_NAME", "23087")  # WeTest平台用户id，请联系相关人员查询


def _prepare_environ():
    if os.environ.get("PLATFORM_IP", None) is None:
        """
            如果本地运行，需要设置登录的账户名和密码
        """
        if os.environ.get("QQNAME", None) is None:
            os.environ["QQNAME"] = "2630319119"
            os.environ["QQPWD"] = "test001"

        if os.environ.get("WECHATNAME", None) is None:
            os.environ["WECHATNAME"] = "qfsycs_001"
            os.environ["WECHATPWD"] = "Test*002"

        env = os.environ.get("PLATFORM_IP")

        if not env:
            # 本地环境
            if not local_package:
                raise WeTestRuntimeError("You must set your game package name,at the top of the file")
            else:
                os.environ["PKGNAME"] = local_package


import team_prop_game as team_prop_game


def _cube_run():
    """
    将所有的测试添加到此处执行，通过脚本进行分场景拉起测试、上传报告。
    每个场景测试，将会进行如下流程操作：
        准备阶段： 清理、拉起
        测试阶段
        结束阶段：结束游戏、上传报告、清理现场
    :return:
    """


    # 1.root通用   sony
    # team_prop_game.run(4)
    # 2.资源测试   s6
    # team_prop_game.run(2)
    # 3.mono内存   s6
    # team_prop_game.run(3)






    # # 3.非root通用
    # team_prop_game.run(6)

    # #1.Unity深度测试
    # team_prop_game.run(5)




    # 标准测试
    # team_prop_game.run(0)

    # 偷猪测试
    team_prop_game.start_steal_pig(4)

def main():
    """
        在自己的pc上运行时，如果需要操控多台手机，可以通过命令行的方式启动
        关于账号或者密码，只需要设置一种账号类型即可。在有第三方账号的话，会优先使用第三方账号
        --qqname:qq账号，每部手机应该都不一样
        --qqpwd:qq密码
        --wechataccount:微信账号
        --wechatpwd:微信密码
        --othername:其他任何账号
        --otherpwd:其他任何账号的密码

        --engineport:与手机端的sdk服务建立网络映射，填入的为本地的网络端口号（如,50031），不同手机之间要确保不同
        --uiport:与手机端的UIAutomator服务建立网络映射，填入的为本地的网络端口号（如,19008），不同手机之间要确保不同
        --serial:adb devcies能够查看手机的序列号，不同的序列号代表不同的手机

    :return:
    """
    usage = "usage:%prog [options] --qqname= --qqpwd= --engineport= --uiport= --serial="
    parser = optparse.OptionParser(usage)
    parser.add_option("-q", "--qqname", dest="QQNAME", help="QQ Account")
    parser.add_option("-p", "--qqpwd", dest="QQPWD", help="QQ Password")
    parser.add_option("-b", "--wechataccount", dest="WECHATNAME", help="wechat Account")
    parser.add_option("-c", "--wechatpwd", dest="WECHATPWD", help="wechat Password")
    parser.add_option("-e", "--engineport", dest="LOCAL_ENGINE_PORT", help="network port forward engine sdk")
    parser.add_option("-u", "--uiport", dest="UIAUTOMATOR_PORT", help="network port forward uiautomator server")
    parser.add_option("-s", "--serial", dest="ANDROID_SERIAL", help="adb devices android mobile serial")
    parser.add_option("-g", "--othername", dest="OTHERNAME", help="upload account")
    parser.add_option("-f", "--otherpwd", dest="OTHERPWD", help="upload password")
    (options, args) = parser.parse_args()
    try:
        if options.QQNAME:
            os.environ["QQNAME"] = options.QQNAME
        if options.QQPWD:
            os.environ["QQPWD"] = options.QQPWD
        if options.LOCAL_ENGINE_PORT:
            os.environ["LOCAL_ENGINE_PORT"] = options.LOCAL_ENGINE_PORT
        if options.UIAUTOMATOR_PORT:
            os.environ["UIAUTOMATOR_PORT"] = options.UIAUTOMATOR_PORT
        if options.ANDROID_SERIAL:
            os.environ["ANDROID_SERIAL"] = options.ANDROID_SERIAL
        if options.OTHERNAME:
            os.environ["OTHERNAME"] = options.OTHERNAME
        if options.OTHERPWD:
            os.environ["OTHERPWD"] = options.OTHERPWD
        if options.WECHATNAME:
            os.environ["WECHATNAME"] = options.WECHATNAME
        if options.WECHATPWD:
            os.environ["WECHATPWD"] = options.WECHATPWD
        _prepare_environ()
    except getopt.error, msg:
        print("for help use --help")
        return 2

    logger = manager.get_logger()
    try:
        _cube_run()
    except:
        stack = traceback.format_exc()
        logger.exception(stack)
    finally:
        logger.debug("GAutomator End")


if __name__ == "__main__":
    sys.exit(main())
