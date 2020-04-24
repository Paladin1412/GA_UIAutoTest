# -*- coding: UTF-8 -*-
import datetime
import sys
import os
from WeTestAPI import WeTestApi
reload(sys)
sys.setdefaultencoding("utf-8")

authparams = {
    "secretid": "VW44hkA8Py8cW9mU",
    "secretkey": "TH2WlPtJS8abhX4S",
}
wetestClient = WeTestApi(authparams, "http://api.wetest.qq.com")

from wpyscripts.wetest.element import Element
from wpyscripts.wetest.engine import ElementBound

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from testcase.tools import *
from wpyscripts.common.utils import *
from Confunc import *
report = manager.get_reporter()
END_GAME = 0
NEW_PLAYER = 0

ROOM_NAME = 'auto'
MAX_ROOM_PLAYER = 5
WAIT_MINUTE = 30
FIRST_PLAYER = "666"
SECTION = 31
SECTION_DICT = {31: 1, 30: 2, 34: 3, 33: 4, 35: 5, 37: 6, 40: 7, 41: 8}
PLAYER_LIST = ["2085", "2910", "1041", "3525", "3242"]
GAME_TYPE = "ECGMT_PROP_TEAM_GAME"
"""gametype:
       ECGMT_SPEED_SINGLE_GAME  #个人竞速
       ECGMT_SPEED_TEAM_GAME    #组队竞速
       ECGMT_PROP_SINGLE_GAME   #个人道具
       ECGMT_PROP_TEAM_GAME     #组队道具
     """


def filepath(file):
    log_dir = os.environ.get("UPLOADDIR")
    file_path = os.path.split(os.path.realpath(__file__))[0]
    if log_dir:
        file_path = os.path.abspath(os.path.join(log_dir, file))
    else:
        file_path = os.path.abspath(os.path.join(os.path.dirname(file_path), file))
    return file_path

def getDeviceImageLink():
    img_url = ''
    screen_shot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot")
    img_path = find_new_file(screen_shot_path)
    img_url = post_file_to_svr(img_path, "http://10.125.32.148/upload.php")
    logger.debug('img_url: ' + img_url)
    return img_url


def reportr_write(clicktime,reporter,testScence,case,element,test_result,failed_reason,screenshot_link):
    clicktime = time.time()
    report.screenshot()
    reporter.write("{0},{1},{2},{3},{4},{5},{6}\n".format(testScence, case, element, test_result, failed_reason,screenshot_link,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    reporter.flush()



# 加等级后 通过进出背包触发新手引导
def InAndOut():
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToKnapsack"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_BackpackView/AnchorLeftTop/Back"))
    time.sleep(3)


def login_qq(test_type=0):
    wait_for_scene("Update", 200)

    qq_button = find_elment_wait("/UIRoot/OG_FL_AccountLoginView/Login/AnchorCenter/LoginField/Buttons/QQLoginBtn",
                                 1000)
    screen_shot_click(qq_button, 10)

    # 测试解锁用
    if test_type == 3:
        time.sleep(2)
        os.system("adb shell input keyevent 26")
        os.system("adb shell input swipe 300 1000 300 500")
        # end
    wait_for_package("com.tencent.mobileqq")
    device.login_qq_wechat_wait(120)
    time.sleep(10)

    wait_for_scene("Update", 1000)


def login_wechat():
    wait_for_scene("Update", 200)

    wechat_btn = find_elment_wait(
        "/UIRoot/OG_FL_AccountLoginView/Login/AnchorCenter/LoginField/Buttons/WxLoginBtn",
        1000)
    screen_shot_click(wechat_btn, 10)

    wait_for_package("com.tencent.mm")
    device.login_qq_wechat_wait(120)
    time.sleep(10)

    wait_for_scene("Update", 1000)


def select_section(section):
    # 如果服务器拉取失败
    # screen_shot_click(find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Yellow)"))
    # 同意用户协议
    screen_shot_click(find_elment_wait("/UIRoot/OG_FL_UserAgreementDlg/AnchorCenter/Btns/Confirm", 5))
    # 关服公告
    screen_shot_click(find_elment_wait("/UIRoot/C_Com_DialogNoticeView/Anchor/Button_Mid_Name", 5))
    time.sleep(3)

    select_btn = find_elment_wait("/UIRoot/OG_FL_ServerChoseView/Start/AnchorBottom/PopuPanel/PlatformChoicesList")
    screen_shot_click(select_btn)

    server = find_elment_wait(
        "/UIRoot/OG_FL_ServerChoseView/Start/AnchorBottom/PopuPanel/SeverList/ScrollView/Grid/Label(Clone) " + "(" + str(
            section) + ")")
    screen_shot_click(server)

    section = find_elment_wait(
        "/UIRoot/OG_FL_ServerListView/AnchorCenter/ServerItemList/ServerItemScrollView/ServerItemCycleGrid/0", 1)
    screen_shot_click(section, 1)


def create_player():
    random_name_btn = find_elment_wait(
        "/UIRoot/OG_FL_CreateRoleView/DressUpPanel/AnchorBottom/AnchorBottom_Root/CreateRolePanel/RandomNameBtn")
    ensure_btn = find_elment_wait(
        "/UIRoot/OG_FL_CreateRoleView/DressUpPanel/AnchorBottom/AnchorBottom_Root/CreateRolePanel/EnsureBtn")
    while True:
        cu_scene = engine.get_scene()
        if cu_scene != "Login":
            break
        screen_shot_click(random_name_btn)
        player_name = ""
        try:
            player_name = engine.get_element_text(engine.find_element(
                "/UIRoot/OG_FL_CreateRoleView/DressUpPanel/AnchorBottom/AnchorBottom_Root/CreateRolePanel/InputFrame"))
        except WeTestRuntimeError as e:
            print e
        if player_name != "":
            screen_shot_click(ensure_btn)
            time.sleep(3)
            scene = engine.get_scene()
            if scene == "Login":
                cancel_jmp = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Blue)", 2)
                if cancel_jmp:
                    engine.click(cancel_jmp)
                global NEW_PLAYER
                NEW_PLAYER = 1
                time.sleep(3)
                # break
                # pass
            else:
                break


def my_wait_button(name, max_count=30, sleeptime=2):
    debug = None
    for i in range(max_count):
        elemens = engine.get_touchable_elements()
        for element in elemens:
            element = element[0]
            if get_element_name(element) == name:
                return True
        report.capture_and_mark(0, 0)
        time.sleep(sleeptime)


def skip_newer_tech():
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)

    # 大厅-新手引导-关闭所有新手引导
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/大厅/BG"))
    # 点击跳过新手引导
    new_tech_btn = find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/新手引导/BG", 5)
    if new_tech_btn:
        screen_shot_click(new_tech_btn)

    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/CloseAllTutorial/BG", 5))
    time.sleep(2)
    # 回退
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"), 5)
    time.sleep(2)
    # 回退到debug主界面
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"), 5)

    # GM
    console_btn = find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleBtn")
    screen_shot_click(console_btn)
    GMInput = find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleContainer/GMInput")
    # 输入GM指令发送
    # 增加所有物品1
    engine.input(GMInput, "svr addallthing 1")
    screen_shot_click("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleContainer/SubmitBtn")
    time.sleep(10)
    screen_shot_click(console_btn)
    # 增加所有物品2
    engine.input(GMInput, "svr addallthing 2")
    screen_shot_click("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleContainer/SubmitBtn")
    time.sleep(10)
    screen_shot_click(console_btn)
    # 加经验
    engine.input(GMInput, "svr addexp 100000")
    screen_shot_click("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleContainer/SubmitBtn")
    time.sleep(8)
    # 驾照
    engine.input(GMInput, "svr setlicenselevel 4")
    screen_shot_click("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleContainer/SubmitBtn")
    time.sleep(8)

    # 皇冠
    engine.input(GMInput, "svr privilege crown 300")
    screen_shot_click("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleContainer/SubmitBtn")
    time.sleep(8)

    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsBtn"))
    time.sleep(2)

    screen_shot_click(debug_btn)


def gm_input(strs):
    gm_num = len(strs)
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)
    # GM
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleBtn"))
    GMInput = find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleContainer/GMInput")
    # 输入GM指令发送
    # 循环输入各条指令
    for i in range(gm_num):
        engine.input(GMInput, strs[i])
        screen_shot_click("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ConsoleContainer/SubmitBtn")
        time.sleep(10)
    # 返回
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsBtn"))
    time.sleep(2)

    screen_shot_click(debug_btn)



def enter_gamecenter():
    # 进入游戏
    screen_shot_click(find_elment_wait(
        "/UIRoot/OG_FL_ServerChoseView/Start/AnchorBottom/Button_Big_Name(Yellow)"))

    time.sleep(30)
    current_scene = engine.get_scene()
    # 创建角色
    if current_scene == "CreateRole":
        screen_shot_click(find_elment_wait(
            "/UIRoot/OG_FL_CreateRoleView/DressUpPanel/AnchorBottom/AnchorBottom_Root/CreateRolePanel/EnsureBtn"))
        # create_player()
        screen_shot_click(find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Blue)", 3))
        wait_for_scene("Level_TrainTrack_A", 100)
        my_wait_button("FullMask", 50)
        # 新账号，构造流程
        return 1

    elif current_scene == "Level_TrainTrack_A":
        # 跳过新手引导
        my_wait_button("FullMask", 50)
        skip_newer_tech()
        exit_server()
    elif current_scene == "Update":
        print current_scene
        common_label = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Label")
        if common_label is not None:
            common_text = engine.get_element_text(common_label)
            print common_text
            ensure_btn = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Yellow)")
            screen_shot_click(ensure_btn)

        return 2

    time.sleep(30)

    close_activity()


def enter_newplayer(EVENTCLICKTIME,reporter):
    # 进入游戏
    dl_btn = find_elment_wait("/UIRoot/OG_FL_ServerChoseView/Start/AnchorBottom/Button_Big_Name(Yellow)")
    if(dl_btn):
        screen_shot_click(dl_btn)
        reportr_write(EVENTCLICKTIME, reporter, "登录游戏", "点击登录", dl_btn.object_name, "Success", "", "xxx.png")
    else:
        reportr_write(EVENTCLICKTIME, reporter, "登录游戏", "点击登录", dl_btn.object_name, "Failed", "TIMEOUT", "xxx.png")
    time.sleep(30)
    current_scene = engine.get_scene()
    # 创建角色
    if current_scene == "CreateRole":
        ensure_btn = find_elment_wait("/UIRoot/OG_FL_CreateRoleView/DressUpPanel/AnchorBottom/AnchorBottom_Root/CreateRolePanel/EnsureBtn")
        if(ensure_btn):
            screen_shot_click(ensure_btn)
            reportr_write(EVENTCLICKTIME, reporter, "创建角色", "点击创建", ensure_btn.object_name, "Success", "", "xxx.png")
        else:
            reportr_write(EVENTCLICKTIME, reporter, "创建角色", "点击创建", ensure_btn.object_name, "Failed", "TIMEOUT", "xxx.png")
        # create_player()
        qx_btn = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Blue)", 3)
        if(qx_btn):
            screen_shot_click(qx_btn)
            reportr_write(EVENTCLICKTIME, reporter, "创建角色", "取消跳过基础引导", qx_btn.object_name, "Success", "", "xxx.png")
        else:
            reportr_write(EVENTCLICKTIME, reporter, "创建角色", "直接进入引导", "Enter_Game", "Success", "", "xxx.png")
        time.sleep(10)
        wait_for_scene("Level_TrainTrack_A")
        my_wait_button("FullMask", 50)
        # 新账号，构造流程
        return 1
    elif current_scene == "Level_TrainTrack_A":
        return 1


def enter_gamecenter_wait(times):

    for i in range(times):
        ret = enter_gamecenter()
        if ret != 2:
            break


def full_avatar():
    # debug-快捷入口-
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)

    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride"
                                "/快捷入口/BG"))
    # 全满装avatar
    engine.swipe_position(950, 600, 950, 300, 50, 1000)
    time.sleep(2)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/UseTemplatePlayerStartGameDataQuick/BG"))
    engine.swipe_position(950, 300, 950, 600, 50, 1000)
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))

    screen_shot_click(debug_btn)


def exit_server():
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/工具/BG"))
    engine.swipe_position(650, 610, 650, 50, 50, 1000)
    time.sleep(2)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/退出/BG"))
    time.sleep(2)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/SwitchToServerChoseSimple/BG"))

    # 回退
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))
    time.sleep(2)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button"))


def close_new_tech():
    wait_for_scene("Level_TrainTrack_A")
    time.sleep(10)
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)

    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/大厅/BG"))
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/新手引导/BG"))
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/CloseAllTutorial/BG"))

    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))

    screen_shot_click(debug_btn)
    time.sleep(2)


def check_room():
    pvp_btn = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/Button_PVP")
    screen_shot_click(pvp_btn)

    for i in range(4):
        room = find_elment_wait(
            "/UIRoot/OG_RoomListView/AnchorCenter/RoomListPanel/UIScrollView/GridPriv/Grid/" + str(i))
        room_name = engine.get_element_text(find_elment_wait(
            "/UIRoot/OG_RoomListView/AnchorCenter/RoomListPanel/UIScrollView/GridPriv/Grid/" + str(i) + "/RoomName"))
        if room_name == ROOM_NAME:
            # in_game = find_elment_wait(
            #     "/UIRoot/OG_RoomListView/AnchorCenter/RoomListPanel/UIScrollView/GridPriv/Grid/1/InGame", 1)
            in_game = None
            try:
                in_game = engine.find_element(
                    "/UIRoot/OG_RoomListView/AnchorCenter/RoomListPanel/UIScrollView/GridPriv/Grid/" + str(
                        i) + "/InGame")
            except WeTestSDKError as e:
                logger.warn(e)

            if in_game:
                print '2'
                exit_game()
            else:
                screen_shot_click(room)

    create_game_room(GAME_TYPE)



# 创建房间
def create_game_room(game_type, map_no):
    # wait_for_scene("")
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/ModeRoot/Button_PVP"))
    screen_shot_click(find_elment_wait("/UIRoot/OG_RoomListView/AnchorBottom/Down_all/CreateRoomBtn"))

    single_speed_btn = find_elment_wait("/UIRoot/OG_SelectGameModelDialog/Anchor/UIGrid/" + game_type)
    screen_shot_click(single_speed_btn)

    # 修改房间名字,手动开局
    change_room_name("auto", 1)



    while True:
        seats = engine.find_elements_path("/UIRoot/OG_LB_RoomView/AnchorLeft/Seats/Grids/*/PlayerInfo")
        seats_num = len(seats)
        print 'room player = ' + str(seats_num)
        # 房间人满
        if seats_num == 5:
            time.sleep(10)
            change_room_name("auto_smoke", 1)

            #  选择地图
            screen_shot_click(find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorLeft/Seats/Grids/Map"))

            # 普通赛道页签
            maps = engine.find_elements_path("/UIRoot/OG_LB_MapIdentifyView/View/StaticUI/Anchor/Grid/*")
            if len(maps) > 0:
                screen_shot_click(maps[4])
            time.sleep(5)
            # 向地图下方滑动，选择地图no
            engine.swipe_position(500, 580, 500, 150, 50, 1000)
            time.sleep(3)
            engine.swipe_position(500, 580, 500, 150, 50, 1000)
            time.sleep(3)
            screen_shot_click(
                find_elment_wait(
                    "/UIRoot/OG_LB_MapIdentifyView/View/DynamicUI/Group02/MapScrollView/Grid/" + str(map_no)))

            time.sleep(2)

            time.sleep(40)
            # 开局
            screen_shot_click(find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorButtom/Offset/VisableGroup/StartBtn"))
            return
        else:
            time.sleep(3)


# 加房間
def join_room():
    flag_join = 0
    while True:
        if flag_join == 0:
            screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/ModeRoot/Button_PVP"))
            for i in range(4):
                room_name_e = find_elment_wait("/UIRoot/OG_RoomListView/AnchorCenter/RoomListPanel/UIScrollView/GridPriv/Grid/" + str(i) + "/RoomName")
                room_name = engine.get_element_text(room_name_e)
                if room_name == "auto":
                    player_num = engine.get_element_text(find_elment_wait(
                        "/UIRoot/OG_RoomListView/AnchorCenter/RoomListPanel/UIScrollView/GridPriv/Grid/" + str(i) + "/PlayerNum/NumLabel"))
                    print int(player_num)
                    if int(player_num) < 6:
                        print 'join auto test room'
                        screen_shot_click(room_name_e)
                        flag_join = 1
                        break
            if flag_join == 0:
                screen_shot_click(find_elment_wait("/UIRoot/OG_RoomListView/AnchorTopLeft/Top_all/ReturnBack"))
        else:
            report.capture_and_mark(0, 0)
            return


def return_home():
    wait_for_scene("lobby")
    find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorButtom/Offset/VisableGroup/PrepareBtn", 50)
    # 等待return按钮
    # time.sleep(8)
    time.sleep(2)
    # 检测是否有画质弹框:
    down_hz = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Yellow)", 2)
    if down_hz is not None:
        screen_shot_click(down_hz)
    # 返回大厅
    room_bakc_btn = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorTopLeft/Back")
    if room_bakc_btn:
        screen_shot_click(room_bakc_btn)
    time.sleep(1)

    # room_bakc_btn = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorTopLeft/Back")
    # if room_bakc_btn:
    #     screen_shot_click(room_bakc_btn)
    # time.sleep(1)

    screen_shot_click(find_elment_wait("/UIRoot/OG_RoomListView/AnchorTopLeft/Top_all/ReturnBack"))
    time.sleep(1)

    # close_activity()


# 随机一把竞速
def random_start(game_no=0):
    # ECGMT_SPEED_SINGLE_GAME,ECGMT_SPEED_TEAM_GAME,ECGMT_PROP_SINGLE_GAME,ECGMT_PROP_TEAM_GAME
    game_type = ""
    if game_no == 0:
        game_type = "ECGMT_SPEED_SINGLE_GAME"
    elif game_no == 1:
        game_type = "ECGMT_SPEED_TEAM_GAME"
    elif game_no == 2:
        game_type = "ECGMT_PROP_SINGLE_GAME"
    elif game_no == 3:
        game_type = "ECGMT_PROP_TEAM_GAME"

    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/ModeRoot/Button_PVP"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/OG_RoomListView/AnchorBottom/Down_all/MatchBtn"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/OG_SelectGameModelDialog/Anchor/UIGrid/" + game_type))
    start_btn = find_elment_wait("/UIRoot/OG_LB_RoomTeamView/AnchorButtom/Offset/StartBtn")
    screen_shot_click(start_btn)
    time.sleep(5)


def relax_land_run(range_times):
    # relax 入口
    relax_in = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/ModeRoot/Button_Leisure")
    screen_shot_click(relax_in)
    # 等待进入
    wait_for_scene("LeisureArea", 30)
    find_elment_wait("/UIRoot/IG_RelaxationLobbyView/StaticUI/AnchorLeftTop/SearchPlayer")
    # 循环跳动
    jump_btn = find_elment_wait("/UIRoot/IG_RelaxationLobbyView/DynamicUI/AnchorRightBottom/JumpBtn")
    for i in range(range_times):
        screen_shot_click(jump_btn)
        time.sleep(2)

    screen_shot_click(find_elment_wait("/UIRoot/IG_RelaxationLobbyView/StaticUI/AnchorLeftTop/CallBackBtn"))


# 修改房间名字
def change_room_name(name, auto_start=0):
    room_name = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorTopLeft/RoomInfo/Title/RoomName")
    if room_name is not None:

        screen_shot_click(room_name)
    input_frame = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorLeft/SettingPanel/Anchor/Name/InputFrame")
    if input_frame is not None:
        engine.input(input_frame, name)
    if auto_start == 1:
        # 添加手动开局
        time.sleep(3)
        screen_shot_click(
            find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorLeft/SettingPanel/Anchor/AutoStart/Toggle/Off"))
    time.sleep(3)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorLeft/SettingPanel/Anchor/EnsureBtn"))


def wait_for_start():
    # wait_for_scene_level("Level_Madagascar")
    # while True:
    #     elements = engine.get_touchable_elements()
    #     for element in elements:
    #         element = element[0]
    #         if get_element_name(element) == "DriftBtn":
    #             return
    find_elment_wait("/UIRoot/IG_MatchInputDlg/Root/OperatingMode/KeysRoot/AnchorRightDown/DriftBtn", 500)
    time.sleep(1)


def get_element_name(element):
    # list_element = str(element).split(' ')
    # return list_element[1]
    element = str(element)
    # print type(element)
    name_list = element.split('/')
    names = name_list[len(name_list) - 1]
    return names.split(' ')[0]


def wait_until_end():
    for i in range(100):
        scene = engine.get_scene()
        if scene == "Lobby":
            # report.report_error("success end")
            elements = engine.get_touchable_elements()
            for element in elements:
                element = element[0]
                if get_element_name(element) == "Confirm":
                    screen_shot_click(element)
                if get_element_name(element) == "OG_LB_PlayerLevelUpDialog":
                    screen_shot_click(element)
                if get_element_name(element) == "StartBtn":
                    report.capture_and_mark(0, 0)
                    return
            time.sleep(3)
        else:
            elements = engine.get_touchable_elements()
            for element in elements:
                element = element[0]
                # print element
                if get_element_name(element) == "Button_Mid_Name(Yellow)":
                    screen_shot_click(element)
                    sys.exit(4)
                    # exit_game()
                # elif get_element_name(element) == "BackButton":
                #     screen_shot_click(element)
                elif get_element_name(element) == "FastMsgButton":
                    print 'end mark'
                    return
            time.sleep(3)
            report.capture_and_mark(1000, 500)


def wait_room():
    wait_for_scene_game("Lobby", 100)
    # 使用debug返回大厅
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView"
                                       "/Gride/快捷入口/BG"))

    engine.swipe_position(1500, 500, 1500, 100, 50, 1000)
    time.sleep(2)
    engine.swipe_position(1500, 500, 1500, 100, 50, 1000)
    time.sleep(1)
    # back to lobby
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/ForceBackLobby/BG"))

    time.sleep(8)
    # 滑最上
    engine.swipe_position(1500, 200, 1500, 700, 20, 1000)
    time.sleep(2)
    engine.swipe_position(1500, 200, 1500, 700, 20, 1000)
    time.sleep(2)

    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button"))


def high_debug():
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)
    time.sleep(1)
    screen_shot_click(
        find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/快捷入口/BG"))
    time.sleep(1)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/SwitchPerformanceBuild/BG"))

    time.sleep(2)

    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/TrunOnSmokeUp/BG"))

    re_btn = find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG")
    screen_shot_click(re_btn)
    time.sleep(1)
    screen_shot_click(debug_btn)


def auto_tuoguan():
    # 开启自动托管游戏
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)

    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/单局/BG"))

    engine.swipe_position(1000, 610, 1000, 350, 50, 1000)
    time.sleep(2)
    au_tg_btn = engine.find_element(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/OpenAutoAI/BG")
    screen_shot_click(au_tg_btn)
    engine.swipe_position(1000, 350, 1000, 610, 50, 1000)
    time.sleep(2)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))
    # screen_shot_click_pos(1760, 250)
    # screen_shot_click(find_elment_wait(
    #     "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))

    screen_shot_click(debug_btn, 2)

def tuoguan():
    # 开启托管游戏
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)

    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/单局/BG"))
    time.sleep(2)
    tg_btn = engine.find_element(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/OpenTrusteeship/BG")
    screen_shot_click(tg_btn)
    time.sleep(2)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))
    # 关闭debug
    screen_shot_click(debug_btn, 2)
    time.sleep(2)
def close_activity():
    # 手游回归奖励
    speedback_page = find_elment_wait("/UIRoot/OG_LB_RefluxWelcomeLetterDlg/LetterCover/Button3_Small(Yellow)", 2)
    if speedback_page:
        screen_shot_click(speedback_page)
        time.sleep(5)
        receive_btn = find_elment_wait("/UIRoot/OG_LB_RefluxWelcomeLetterDlg/LetterContent/ReceiveBtn", 2)
        if receive_btn:
            screen_shot_click(receive_btn)
        time.sleep(5)
        mid_btn1 = find_elment_wait("/UIRoot/OG_ReceiveRewardDialog/Container/Button_Mid_Name(Blue)", 2)
        if mid_btn1:
            screen_shot_click(mid_btn1)
        close_btn = find_elment_wait("/UIRoot/OG_LB_RefluxWelcomeNotifyDlg/LetterNotifyFriend/CloseBtn", 2)
        if close_btn:
            screen_shot_click(close_btn)
        time.sleep(2)
        mid_btn2 = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Yellow)", 2)
        if mid_btn2:
            screen_shot_click(mid_btn2)
    time.sleep(5)

    # V7任务弹框
    task_back_btn = find_elment_wait("/UIRoot/OG_LB_TaskScreen/AnchorTopLeft/Public/BackBtn", 20)
    if task_back_btn:
        screen_shot_click(task_back_btn)


    # 活动
    close_activity_dia = find_elment_wait("/UIRoot/OG_LB_ActivityDlg/AnchorCenter/Content/Button_Mid_CloseBtn", 5)
    if close_activity_dia:
        screen_shot_click(close_activity_dia)

    fuli_close_btn = find_elment_wait("/UIRoot/OG_ContinuationEnterRewardDlg/AnchorCenter/Button_Mid_Name", 5)
    if fuli_close_btn:
        screen_shot_click(fuli_close_btn)

    # 七日累登
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_PandoraDlg/LoginIn2/closebtn"))
    # 处理tga弹框
    time.sleep(5)
    device.excute_adb("shell input keyevent 4")

    # 判断是否有退出游戏
    back = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Blue)", 5)
    time.sleep(2)
    if back is not None:
        screen_shot_click(back)
    # 异形弹框
    # # 新活动
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_PandoraDlg/Pop/Container_content/unRegularObject/Button_close"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_PandoraDlg/Pop/Container_content/unRegularObject/Button_close"))

    # 拍脸广告
    screen_shot_click(find_elment_wait(
        "/UIRoot/OG_LB_PandoraDlg/Pop/Container_content/regularObject/Button_close"))
    time.sleep(2)
    screen_shot_click(find_elment_wait(
        "/UIRoot/OG_LB_PandoraDlg/Pop/Container_content/regularObject/Button_close"))

    # 首充
    close_first_charge = find_elment_wait("/UIRoot/OG_FirstRechargeView/Anchor/CloseBtn", 5)
    if close_first_charge:
        screen_shot_click(close_first_charge)



    time.sleep(3)


def dress():
    while True:
        # 打开背包
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToKnapsack"))
        time.sleep(4)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_BackpackView/AnchorLeft/Offset/TitlePanel/Table/-2_1"))
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_BackpackView/AnchorLeft/Offset/TitlePanel/Table/-2_1/PullDown/Grid/1_18"))
        full_clo = find_elment_wait("/UIRoot/OG_LB_BackpackView/AnchorLeft/Items/ItemPanel/Grid/0", 2)
        if full_clo:
            break
        else:
            # 1.跳过新手引导
            skip_newer_tech()
            # 2.退回选服界面
            exit_server()
            # 3.重登构造条件
            enter_gamecenter()
    # 选中全部页签
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_BackpackView/AnchorLeft/Offset/TitlePanel/Table/-2_1/PullDown/Grid/1_0"))
    # 套装
    cloths = engine.find_elements_path("/UIRoot/OG_LB_BackpackView/AnchorLeft/Offset/TitlePanel/Table/-2_1/PullDown/Grid/*")
    len_cloths = len(cloths)
    for i in range(len_cloths / 2):
        screen_shot_click(cloths[i])
        rand_grid()
        time.sleep(2)
    engine.swipe_position(70, 750, 70, 350, 50, 1000)
    for i in range(len_cloths / 2, len_cloths):
        screen_shot_click(cloths[i])
        rand_grid()
        time.sleep(2)
    # 回大厅
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_BackpackView/AnchorLeftTop/Back"))
    time.sleep(10)
    close_activity()


    # 进入车库 跳过车库新手引导
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToGargeScreenBtn"))
    time.sleep(10)
    engine.click_position(93, 940)
    time.sleep(10)
    i = 0
    while True:
        # 选中刺客
        # car_chike = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/0/VehicleInfo/Name", 5)
        # 选中南瓜车
        car_chike = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/75", 5)
        if car_chike:
            screen_shot_click(car_chike)
            time.sleep(5)
            # 点击改装
            refit_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/BtnRefit", 2)
            if refit_btn:
                screen_shot_click(refit_btn)
            time.sleep(10)
            # 点击屏幕 跳过改装介绍
            engine.click_position(890, 630)
            time.sleep(5)
            # 点击传动
            cd_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/1", 2)
            if cd_btn:
                screen_shot_click(cd_btn)
            time.sleep(3)
            # 点击传动改装按钮
            refit_cd_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/RefitBtn", 2)
            if refit_cd_btn:
                screen_shot_click(refit_cd_btn)
            time.sleep(8)
            # 跳过传动改装介绍
            engine.click_position(890, 630)
            time.sleep(5)
            # 返回刺客改装
            back_ck = find_elment_wait("/UIRoot/OG_LB_VehicleCptRefitView/AnchorLeftTop/AnimRoot/Back", 2)
            if back_ck:
                screen_shot_click(back_ck)
            time.sleep(3)
            # 返回赛车界面
            back_carview = find_elment_wait("/UIRoot/OG_LB_GarageView/AnchorLeftTop/AnimRoot/Back", 2)
            if back_carview:
                screen_shot_click(back_carview)
            print "成功跳过车库新手引导..."
            time.sleep(2)
            break
        else:
            i = i + 1
            print "第"+ str(i) + "次检查车库新手引导"
            if i == 5:
                print "未检查到新手引导"
                # 点击刺客坐标位
                engine.click_position(445, 845)
                time.sleep(10)
                # 点击改装
                refit_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/BtnRefit", 2)
                if refit_btn:
                    screen_shot_click(refit_btn)
                time.sleep(10)
                # 点击屏幕 跳过改装介绍
                engine.click_position(890, 630)
                time.sleep(5)
                # 点击传动
                cd_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/1", 2)
                if cd_btn:
                    screen_shot_click(cd_btn)
                time.sleep(3)
                # 点击传动改装按钮
                refit_cd_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/RefitBtn", 2)
                if refit_cd_btn:
                    screen_shot_click(refit_cd_btn)
                time.sleep(8)
                # 跳过传动改装介绍
                engine.click_position(890, 630)
                time.sleep(5)
                # 返回刺客改装
                back_ck = find_elment_wait("/UIRoot/OG_LB_VehicleCptRefitView/AnchorLeftTop/AnimRoot/Back", 2)
                if back_ck:
                    screen_shot_click(back_ck)
                time.sleep(3)
                # 返回赛车界面
                back_carview = find_elment_wait("/UIRoot/OG_LB_GarageView/AnchorLeftTop/AnimRoot/Back", 2)
                if back_carview:
                    screen_shot_click(back_carview)
                print "成功跳过车库新手引导..."
                time.sleep(2)
                break

    while True:
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_GarageListView/AnchorLeft/AnchorLeft_root/TitlePanel/Table/-2_0/PullDown/Grid/0_103"))
        a_car = find_elment_wait("/UIRoot/OG_LB_GarageListView/AnchorCenter/AnimaRoot/Items/ItemPanel/Grid/0", 5)
        if a_car:
            break
        else:
            # 1.跳过新手引导
            skip_newer_tech()
            # 2.退回选服界面
            exit_server()
            # 3.重登构造条件
            enter_gamecenter()
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToGargeScreenBtn"))
        time.sleep(5)

    # 随机选一辆驾驶
    screen_shot_click(find_elment_wait(
        "/UIRoot/OG_LB_GarageListView/AnchorCenter/AnimaRoot/Items/ItemPanel/Grid/" + str(random.randint(0, 10))), 5)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_GarageView/AnchorButtomRight/AnimRoot/Btns/BtnDirve"))
    # 返回大厅
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_GarageView/AnchorLeftTop/AnimRoot/Back"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_GarageListView/AnchorTopLeft/Back"))

    # 带宠物
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoTPetScreenBtn"))
    time.sleep(3)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_GetNewPetView/AnchorButtom/AnimRoot/Offset/Btn/ActiveBtn"))
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_GetNewPetView/AnchorButtom/AnimRoot/Offset/Btn/TweenScale/Grid/2All"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_GetNewPetView/AnchorButtom/AnimRoot/Offset/Btn/BackBtn"))


def rand_grid():
    grid = random.randint(0, 5)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_BackpackView/AnchorLeft/Items/ItemPanel/Grid/" + str(grid)))


def tuoguan():
    # 托管游戏
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    screen_shot_click(debug_btn)
    time.sleep(1)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/单局/BG"))
    tg_btn = engine.find_element(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/OpenTrusteeship/BG")
    screen_shot_click(tg_btn)
    screen_shot_click(find_elment_wait(
        "/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/ToolsContainer/ScrollView/Gride/Btn(Clone)/BG"))

    screen_shot_click(debug_btn, 2)


def re_lobby():
    # 返回大厅
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorTopLeft/Back", 3))
    time.sleep(1)
    screen_shot_click(find_elment_wait("/UIRoot/OG_RoomListView/AnchorTopLeft/Top_all/ReturnBack", 3))
    time.sleep(1)


def exit_game():
    wait_for_scene("Lobby")
    set_btn = find_elment_wait("/UIRoot/OG_TopNavStlyView/Anchor/AnimatRoot/RightBtnRoot/Btn_Setting")
    screen_shot_click(set_btn)

    exit_btn = find_elment_wait(
        "/UIRoot/OG_LB_SettingView/AnchorCenter/BasicSetPanel/BasicScrollViewSet/AnchorBottom/PrivacySet/ServiceInfo/Btn_ExitLogin")
    screen_shot_click(exit_btn)
    # report.report(False, u"异常退出", "功能测试test")


def team_prop_join_player():
    login_qq()

    # 31每日构建
    select_section(2)
    # high_debug()
    enter_result = enter_gamecenter()

    # 新手
    if enter_result == 1:
        # 1.跳过新手引导
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()
        # relogin
        gm_input(["svr setlicenselevel 4", "svr addexp 500000"])
        exit_server()

        enter_gamecenter()
        # 4. 穿上衣服和车等
        dress()
    # # 服务器连接失败，停留在登陆界面
    # elif enter_result == 2:
    #     # 30 稳定体验
    #     select_section(1)
    #     enter_gamecenter()

    # 再次跳过引导和穿装备
    # ==================
    skip_newer_tech()
    # 2.退回选服界面
    exit_server()
    # 3.重登构造条件
    enter_gamecenter()
    # relogin
    gm_input(["svr setlicenselevel 4", "svr addexp 500000"])
    exit_server()

    enter_gamecenter()
    # 4. 穿上衣服和车等
    dress()
    # ==================

    # 自动托管
    auto_tuoguan()
    while True:
        join_room()
        wait_for_start()
        time.sleep(130)
        return_home()






def test_run():
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_RoomTeamView/AnchorButtom/Offset/StartBtn"))
    time.sleep(20)


# 申请加入车队 --- 6人1组
def join_team_player():
    login_qq()

    # 34-手Q测试
    select_section(4)
    # high_debug()
    enter_result = enter_gamecenter()

    # 新手
    if enter_result == 1:
        # 1.跳过新手引导
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()
        # relogin
        gm_input(["svr setlicenselevel 4", "svr addexp 500000"])
        exit_server()

        enter_gamecenter()


        # 4. 穿上衣服和车等
        dress()

        # 第二次跳过新手引导，添加所有物品
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()

    # 进入车队界面 检查是否已加入车队
    enter_team_btn = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToMotorcadeScreenBtn")
    if enter_team_btn:
        screen_shot_click(enter_team_btn)
    time.sleep(5)
    create_carteam_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/TitlePanel/Tab/Table/Tab_RacingTeamCreate", 5)
    if create_carteam_btn:
        # 返回大厅
        team_back_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorTopLeft/Public/BackBtn")
        if team_back_btn:
            screen_shot_click(team_back_btn)
        time.sleep(5)
        # 进入auto房间 每次房间加慢后 记得修改房间名
        join_room()
        while True:
            seats = engine.find_elements_path("/UIRoot/OG_LB_RoomView/AnchorLeft/Seats/Grids/*/PlayerInfo")
            seats_num = len(seats)
            print 'room player = ' + str(seats_num)
            # 房间人满
            if seats_num == 5:
                break
            else:
                time.sleep(3)
        # 申请加入车队
        room_apply_jointeam()
    else:
        exit_server()


# 申请加入车队 --- 连续加人
def join_team_nplayer():
    login_qq()

    # 34-手Q测试
    select_section(4)
    # high_debug()
    enter_result = enter_gamecenter()

    # 新手
    if enter_result == 1:
        # 1.跳过新手引导
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()
        # relogin
        gm_input(["svr setlicenselevel 4", "svr addexp 500000"])
        exit_server()

        enter_gamecenter()


        # 4. 穿上衣服和车等
        dress()

        # 第二次跳过新手引导，添加所有物品
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()

    # 进入车队界面 检查是否已加入车队
    enter_team_btn = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToMotorcadeScreenBtn")
    if enter_team_btn:
        screen_shot_click(enter_team_btn)
    time.sleep(5)
    create_carteam_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/TitlePanel/Tab/Table/Tab_RacingTeamCreate", 5)
    if create_carteam_btn:
        # 返回大厅
        team_back_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorTopLeft/Public/BackBtn")
        if team_back_btn:
            screen_shot_click(team_back_btn)
        time.sleep(5)
        # 进入auto房间 每次房间加慢后 记得修改房间名
        join_room()
        while True:
            seats = engine.find_elements_path("/UIRoot/OG_LB_RoomView/AnchorLeft/Seats/Grids/*/PlayerInfo")
            seats_num = len(seats)
            print 'room player = ' + str(seats_num)
            # 房间里有其他人
            if seats_num >= 1:
                break
            else:
                time.sleep(3)
        # 申请加入车队
        room_apply_jointeam()
    else:
        exit_server()


# 进入车队3d房间 等待开始比赛
def join_team_3droom():
    login_qq()

    # 31每日构建
    select_section(4)
    # high_debug()
    enter_result = enter_gamecenter()

    # 新手
    if enter_result == 1:
        # 1.跳过新手引导
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()
        # relogin
        gm_input(["svr setlicenselevel 4", "svr addexp 500000"])
        exit_server()

        enter_gamecenter()
        # 4. 穿上衣服和车等
        dress()
    # 进入车队3d房间
    join_team3droom_autorun()


# 进入车队3d房间 房间内瞎跑
def join_team_3droom_run():
    login_qq()

    # 31每日构建
    select_section(4)
    # high_debug()
    enter_result = enter_gamecenter()

    # 新手
    if enter_result == 1:
        # 1.跳过新手引导
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()
        # relogin
        gm_input(["svr setlicenselevel 4", "svr addexp 500000"])
        exit_server()

        enter_gamecenter()
        # 4. 穿上衣服和车等
        dress()
    # 进入车队3d房间
    join_team3droom()


# 拉起游戏 进入偷猪休闲区 开始偷猪-跑到偷猪休闲区，开始移动抓猪，放猪
def stealpig_join_player():
    login_qq()

    # 31每日构建
    select_section(4)
    # high_debug()
    enter_result = enter_gamecenter()

    # 新手
    if enter_result == 1:
        # 1.跳过新手引导
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()
        # relogin
        gm_input(["svr setlicenselevel 4", "svr addexp 500000"])
        exit_server()

        enter_gamecenter()
        # 4. 穿上衣服和车等
        dress()

        # 第二次跳过新手引导，添加所有物品
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()

    # 创建车队
    # create_motorcade()
    # 进入偷猪休闲区 开始自动偷猪
    steal_pig()

def stealpig_joinout_player():
    login_qq()

    # 31每日构建
    select_section(4)
    # high_debug()
    enter_result = enter_gamecenter()

    # 新手
    if enter_result == 1:
        # 1.跳过新手引导
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()
        # relogin
        gm_input(["svr setlicenselevel 4", "svr addexp 500000"])
        exit_server()

        enter_gamecenter()
        # 4. 穿上衣服和车等
        dress()

        # 第二次跳过新手引导，添加所有物品
        skip_newer_tech()
        # 2.退回选服界面
        exit_server()
        # 3.重登构造条件
        enter_gamecenter()

    # 创建车队
    # create_motorcade()
    # 进入偷猪休闲区 反复进出
    joinout_steal_pig()


# 房间申请加入车队
def room_apply_jointeam():
    # 查找房主位置
    for i in range(1, 7):
        room_master = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorLeft/Seats/Grids/Seat"+ str(i) +"/PlayerInfo/Grid/Host",2)
        if room_master:
            print(i)
            captain_position = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorLeft/Seats/Grids/Seat"+ str(i) +"/PlayerInfo/"+ str(i), 2)
            if captain_position:
                screen_shot_click(captain_position)
            break
        else:
            time.sleep(2)
    time.sleep(2)
    infor_btn = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorLeft/PopupPlayer/Grid/BtnInfo", 2)
    if infor_btn:
        screen_shot_click(infor_btn)
    time.sleep(10)
    view_btn = find_elment_wait("/UIRoot/OG_LB_PlayerSpaceDlg/AnchorLeft/PagesRoot/HomePage/Animation_Open/GuildInfo/GameObject/Btn_Check", 2)
    if view_btn:
        screen_shot_click(view_btn)
    time.sleep(4)
    # 个人空间申请加入车队
    join_team_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamBrowsingDialog/Center/Button_Mid_Confirm", 2)
    if join_team_btn:
        screen_shot_click(join_team_btn)
    time.sleep(2)
    engine.click_position(50, 58)
    time.sleep(4)
    return_room = find_elment_wait("/UIRoot/OG_LB_RoomView/AnchorTopLeft/Back")
    if return_room:
        screen_shot_click(return_room)
    time.sleep(5)
    return_hall = find_elment_wait("/UIRoot/OG_RoomListView/AnchorTopLeft/Top_all/ReturnBack", 2)
    if return_hall:
        screen_shot_click(return_hall)
    # exit_server()

# 进入车队赛3D房间 打开自动托管 等待开局
def join_team3droom_autorun():
    # 进入车队界面
    goto_motorcade_btn = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToMotorcadeScreenBtn")
    if goto_motorcade_btn:
        screen_shot_click(goto_motorcade_btn)
    time.sleep(10)
    team_match_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/AnchorBottomRight/Content/Buttons/TeamMatchBtn", 2)
    if team_match_btn:
        print("aleady skip team view")
    else:
        # 通过车队创建后第1个弹窗
        engine.click_position(950, 620)
        time.sleep(10)
        # 通过车队创建后第2个弹窗
        engine.click_position(950, 620)
    time.sleep(5)
    # 检查是否有车队 有则进入车队3d房间 没有则退出游戏
    team_match_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/AnchorBottomRight/Content/Buttons/TeamMatchBtn", 2)
    if team_match_btn:
        screen_shot_click(team_match_btn)
        time.sleep(5)
        # 进入3D房间
        enter_match_btn = find_elment_wait("/UIRoot/OG_IntroduceDlg/BtnEnter")
        if enter_match_btn:
            screen_shot_click(enter_match_btn)
            time.sleep(10)
            # 自动托管
            auto_tuoguan()
            # 进入后移动到随机位置
            engine.swipe_and_press(220, 857, random.randint(70, 362), random.randint(726, 1015), 50, 2000)
            # 循环等待
            while True:
                time.sleep(30)
                report.capture_and_mark(0, 0)
                time.sleep(10)
    else:
        exit_server()



# 进入车队3d房间瞎跑
def join_team3droom():
    # 进入车队界面
    goto_motorcade_btn = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToMotorcadeScreenBtn")
    if goto_motorcade_btn:
        screen_shot_click(goto_motorcade_btn)
    time.sleep(10)
    team_match_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/AnchorBottomRight/Content/Buttons/TeamMatchBtn", 2)
    if team_match_btn:
        print("aleady skip team view")
    else:
        # 通过车队创建后第1个弹窗
        engine.click_position(950, 620)
        time.sleep(10)
        # 通过车队创建后第2个弹窗
        engine.click_position(950, 620)
    time.sleep(5)
    # 检查是否有车队 有则进入车队3d房间 没有则退出游戏
    team_match_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/AnchorBottomRight/Content/Buttons/TeamMatchBtn", 2)
    if team_match_btn:
        screen_shot_click(team_match_btn)
        time.sleep(5)
        # 进入3D房间
        enter_match_btn = find_elment_wait("/UIRoot/OG_IntroduceDlg/BtnEnter")
        if enter_match_btn:
            screen_shot_click(enter_match_btn)
            time.sleep(30)
            # 在3d房间瞎跑
            while True:
                engine.swipe_and_press(220, 857, random.randint(70, 362), random.randint(726, 1015), 50, 3000)
                time.sleep(3)
                report.capture_and_mark(0, 0)
                time.sleep(3)
    else:
        exit_server()

# 创建车队
def create_motorcade():
    # 加砖石
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    if debug_btn:
        screen_shot_click(debug_btn)
    time.sleep(2)

    gm_btn = find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/GMBtnsBtn")
    if gm_btn:
        screen_shot_click(gm_btn)
    time.sleep(2)
    add_diamond = find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/GMBtnsContainer/ScrollView/Grid/加钻石1000/BG")
    if add_diamond:
        screen_shot_click(add_diamond)
    time.sleep(1)
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button"))
    time.sleep(1)
    # 进入车队界面
    goto_motorcade_btn = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToMotorcadeScreenBtn")
    if goto_motorcade_btn:
        screen_shot_click(goto_motorcade_btn)
    time.sleep(5)
    # 进入创建车队界面
    team_create_tab = find_elment_wait("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/TitlePanel/Tab/Table/Tab_RacingTeamCreate", 1)
    if team_create_tab:
        screen_shot_click(team_create_tab)
    time.sleep(5)
    # 输入车队名
    team_name = engine.find_element("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/RacingTeamCreate/details/Left/TeamName")
    if team_name:
        engine.input(team_name,"秋名山" + str(random.randint(0,1000)) + "队")
    time.sleep(2)
    team_decla = engine.find_element("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/RacingTeamCreate/details/Left/TeamDeclaration")
    if team_decla:
        engine.input(team_decla,"我们是秋名山第" + str(random.randint(0,1000)) + "强战队")
    time.sleep(2)
    # 创建车队
    create_team_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/RacingTeamCreate/details/Right/CreateBtn", 1)
    if create_team_btn:
        screen_shot_click(create_team_btn)
    time.sleep(10)

    enter_steal = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/Content/Buttons/LeisureFuncBtn/Button2_Mid_Name(Yellow)", 1)
    if enter_steal:
        print("aleady create team")
    else:
        # 通过车队创建后第1个弹窗
        engine.click_position(950, 620)
        time.sleep(10)
        # 通过车队创建后第2个弹窗
        engine.click_position(950, 620)
    time.sleep(5)

def create_xxnum_motorcade():
    # 加砖石
    debug_btn = find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button")
    if debug_btn:
        screen_shot_click(debug_btn)
    time.sleep(2)

    gm_btn = find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/GMBtnsBtn")
    if gm_btn:
        screen_shot_click(gm_btn)
    time.sleep(2)
    add_diamond = find_elment_wait("/UIRoot/ViewProfiler/ConsoleDlg/AnchorCenter/Root/GMBtnsContainer/ScrollView/Grid/加钻石1000/BG")
    if add_diamond:
        screen_shot_click(add_diamond)
    time.sleep(1)
    screen_shot_click(find_elment_wait("/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button"))
    time.sleep(1)
    # 进入车队界面
    goto_motorcade_btn = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToMotorcadeScreenBtn")
    if goto_motorcade_btn:
        screen_shot_click(goto_motorcade_btn)
    time.sleep(5)
    # 进入创建车队界面
    team_create_tab = find_elment_wait("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/TitlePanel/Tab/Table/Tab_RacingTeamCreate", 2)
    if team_create_tab:
        screen_shot_click(team_create_tab)
        time.sleep(5)
        for i in range(1, 7):
            # 输入车队名
            team_name = engine.find_element("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/RacingTeamCreate/details/Left/TeamName")
            if team_name:
                engine.input(team_name,"auto" + str(i) + "team")
            time.sleep(2)
            team_decla = engine.find_element("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/RacingTeamCreate/details/Left/TeamDeclaration")
            if team_decla:
                engine.input(team_decla,"我们是秋名山第" + str(i) + "强战队")
            time.sleep(2)
            # 创建车队
            create_team_btn = find_elment_wait("/UIRoot/OG_LB_RacingTeamFreeScreen/AnchorLeft/RacingTeamCreate/details/Right/CreateBtn", 1)
            if create_team_btn:
                screen_shot_click(create_team_btn)
            # 判断是否存在车队
            if i == 1 :
                print("已存在这个车队")
            else:
                break
        time.sleep(10)
        # 通过车队创建后第1个弹窗
        engine.click_position(950, 620)
        time.sleep(10)
        # 通过车队创建后第2个弹窗
        engine.click_position(950, 620)
    else:
        print("aleady create team")
    time.sleep(5)


# 进出偷猪休闲区
def joinout_steal_pig():
    # 进入车队界面
    goto_motorcade_btn = find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToMotorcadeScreenBtn")
    if goto_motorcade_btn:
        screen_shot_click(goto_motorcade_btn)
    time.sleep(10)
    enter_steal = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/AnchorBottomRight/Content/Buttons/LeisureFuncBtn", 2)
    if enter_steal:
        print("aleady skip team view")
    else:
        # 通过车队创建后第1个弹窗
        engine.click_position(950, 620)
        time.sleep(10)
        # 通过车队创建后第2个弹窗
        engine.click_position(950, 620)
    time.sleep(5)
    # 进入偷猪房间
    enter_steal = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/AnchorBottomRight/Content/Buttons/LeisureFuncBtn")
    if enter_steal:
        screen_shot_click(enter_steal)
    time.sleep(4)
    while True:
        # 进入偷猪休闲区
        join_steal = find_elment_wait("/UIRoot/OG_LB_PigPartyDialog/AnchorRightBottom/AnchorRightBottom_Root/JoinParrtyBtn")
        if join_steal:
            screen_shot_click(join_steal)
        time.sleep(30)
        # 退出偷猪休闲区
        out_steal = find_elment_wait("/UIRoot/IG_RelaxationLobbyView/StaticUI/AnchorLeftTop/Back")
        if out_steal:
            screen_shot_click(out_steal)
        time.sleep(30)



# 休闲区偷猪
def steal_pig():
    # 进入车队界面
    goto_motorcade_btn = find_elment_wait(
        "/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToMotorcadeScreenBtn")
    if goto_motorcade_btn:
        screen_shot_click(goto_motorcade_btn)
    time.sleep(10)
    enter_steal = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/AnchorBottomRight/Content/Buttons/LeisureFuncBtn", 1)
    if enter_steal:
        print("aleady skip team view")
    else:
        # 通过车队创建后第1个弹窗
        engine.click_position(950, 620)
        time.sleep(10)
        # 通过车队创建后第2个弹窗
        engine.click_position(950, 620)
    time.sleep(5)
    # 进入偷猪房间
    enter_steal = find_elment_wait("/UIRoot/OG_LB_RacingTeamNewScreen/AnchorBottomRight/Content/Buttons/LeisureFuncBtn")
    if enter_steal:
        screen_shot_click(enter_steal)
    time.sleep(1)
    join_steal = find_elment_wait("/UIRoot/OG_LB_PigPartyDialog/AnchorRightBottom/AnchorRightBottom_Root/JoinParrtyBtn")
    if join_steal:
        screen_shot_click(join_steal)
    time.sleep(20)
    # 开始移动
    # for i in range(6):
    #     engine.swipe_position(210, 857, 210, 160, 500, 5000)
    # for i in range(2):
    #     engine.swipe_position(210, 857, 160, 160, 500, 5000)
    # 跑到猪圈门口
    engine.swipe_and_press(220, 857, 220, 716, 50, 33000)
    time.sleep(2)
    # 调整进入猪圈的方向
    engine.swipe_and_press(220, 857, 180, 716, 50, 4000)
    time.sleep(1)
    # 随机移动到猪圈某个位置
    engine.swipe_and_press(220, 857, random.randint(70, 362), random.randint(726, 1015), 50, 1000)
    time.sleep(1)
    position = find_elment_wait("/UIRoot/IG_RelaxationLobbyView/DynamicUI/AnchorRightBottom/JumpBtn", 2)
    if position:
        screen_shot_click(position)
    time.sleep(5)
    while True:
        # 连续尝试抓小猪5次
        for i in range(5):
            # 抓小猪
            steal_littlepig = find_elment_wait("/UIRoot/OG_LB_PigPartyLeisureMain/PigBtn/Btn_PigSteal", 1)
            # 检测放小猪
            drop_littlepig = find_elment_wait("/UIRoot/OG_LB_PigPartyLeisureMain/PigBtn/Btn_PigGiveUpSteal", 1)
            if steal_littlepig:
                screen_shot_click(steal_littlepig)
            if drop_littlepig:
                screen_shot_click(drop_littlepig)
            time.sleep(10)
            engine.swipe_and_press(220, 857, random.randint(70, 362), random.randint(726, 1015), 50, 2000)
            time.sleep(2)
        # 连续尝试抓猪王5次
        for i in range(5):
            # 抓猪王
            steal_pigking = find_elment_wait("/UIRoot/OG_LB_PigPartyLeisureMain/PigBtn/Btn_PigHelp", 1)
            # 检测放猪王
            drop_pigking = find_elment_wait("/UIRoot/OG_LB_PigPartyLeisureMain/PigBtn/Btn_PigGiveUpHelp", 1)
            if steal_pigking:
                screen_shot_click(steal_pigking)
            if drop_pigking:
                screen_shot_click(drop_pigking)
            time.sleep(10)
            engine.swipe_and_press(220, 857, random.randint(70, 362), random.randint(726, 1015), 50, 2000)
            time.sleep(2)

def main():
    team_prop_join_player()


if __name__ == '__main__':
    main()
