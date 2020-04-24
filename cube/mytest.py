import time
# -*- coding: UTF-8 -*-
# -*-coding:utf-8 -*-
from testcase.tools import *
from wpyscripts.common.utils import *
import testcase.MyTestAPI as nsss


reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    import testcase.MyTestAPI as nsss

    # nsss.login_qq()
    #
    # time.sleep(5)
    # nsss.high_debug()
    #
    # nsss.select_section(4)
    # new_player = nsss.enter_gamecenter()
    # if new_player == 0:
    #     nsss.skip_newer_tech()
    #     nsss.exit_server()
    #     nsss.enter_gamecenter()
    #     nsss.dress()

    nsss.enter_gamecenter()
    nsss.dress()
    # nsstest.random_start("ECGMT_PROP_SINGLE_GAME")

    for i in range(2):
        nsss.create_game_room("ECGMT_PROP_TEAM_GAME", 11)
        print "create room ok"
        nsss.wait_for_start()
        print "wait_for_start ok"

        nsss.tuoguan()


        time.sleep(150)
        print 'stop mark1'


        nsss.wait_room()
        time.sleep(20)


if __name__ == '__main__':
    input_frame = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorLeft/SettingPanel/Anchor/Name/InputFrame", 2)
    if input_frame is not None:
        print '11'
        engine.input(input_frame, "11")
