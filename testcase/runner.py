# -*- coding: UTF-8 -*-
from testcase.client_autotest import client_test, relax_profile, delte_account
from testcase.MyTestAPI import team_prop_join_player, join_team_player, stealpig_join_player, join_team_nplayer, stealpig_joinout_player, join_team_3droom_run, join_team_3droom
from testcase.NewbieTest import newbie_lead
__author__ = 'minhuaxu'

from wpyscripts.tools.baisc_operater import *
import wpyscripts.tools.traverse.travel as travel

logger = manager.get_testcase_logger()


# 帮助文档及内容
# ==========================QQ登陆过程示例================================================
# def login_qq():
#     """
#         腾讯系游戏，通过QQ登陆
#
#         从拉起游戏出现QQ和微信登陆按钮--->QQ账号密码输入登陆-->登陆完成
#     :return:
#     """
#     tencent_login(scene_name="EmptyScene",login_button="/BootObj/CUIManager/Form_Login/LoginContainer/pnlMobileLogin/btnGroup/btnQQ",sleeptime=3)


# ==========================随机遍历过程================================================
# forbid_names = ["/ViewUIDepth_2/Canvas/ManagerInformation/Panel/JumpWindow/RightPanel/Wanjiaxinxi/ChangeServerButton",
#                 "/ViewUIDepth_2/Canvas/ManagerInformation/Panel/JumpWindow/RightPanel/Wanjiaxinxi/LoginOutButton"]
def random_search_test():
    log_dir = os.environ.get("UPLOADDIR")
    if log_dir:
        log_dir = os.path.join(log_dir, "policy.log")
    else:
        log_dir = "policy.log"
    logger.info("run random search in testcase runner")
    travel.explore(log_dir, [], mode=0, max_num=3000)


def run():
    """
        业务逻辑的起点
    """
    try:
        # 新手引导---自动化
        newbie_lead()

        # 偷猪
        # stealpig_join_player()

        # 进出偷猪休闲区
        # stealpig_joinout_player()

        # 房间加入车队 6人1组进行添加
        # join_team_player()
        # 房间加入车队 无等待添加
        # join_team_nplayer()

        # 进入车队3d房间 等待开始比赛
        # join_team_3droom()
        # 进入车队3d房间 在房间内乱跑
        # join_team_3droom_run()

        # 单局冒烟
        # team_prop_join_player()

        # 删除账号
        # delte_account()

        # client_test()
        # relax_profile()



    except Exception as e:
        traceback.print_exc()
        stack = traceback.format_exc()
        logger.error(stack)
        report.report_error("script_error")
    finally:
        report.screenshot()
