# -*- coding: UTF-8 -*-
import datetime
import sys
import os
from testcase.MyTestAPI import enter_newplayer,gm_input,auto_tuoguan,getDeviceImageLink,filepath,login_qq,select_section,high_debug
reload(sys)
sys.setdefaultencoding("utf-8")
from wpyscripts.wetest.element import Element
from wpyscripts.wetest.engine import ElementBound

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from testcase.tools import *
from wpyscripts.common.utils import *
report = manager.get_reporter()


# 新手引导---自动化
def newbie_lead():
    file_path = filepath("NssGame_BVT.log")
    if os.path.exists(file_path):
        os.remove(file_path)
    reporter = open(file_path, "w")
    import  parseConfigDist as parseConfigDist
    global EVENTCLICKTIME
    EVENTCLICKTIME = time.time()
    try:
        login_qq()
        scene = engine.get_scene()
        if (scene == "Update"):
            reportr_write(EVENTCLICKTIME, reporter, "拉起游戏", "进入登录界面", "StartGame", "Success", "", getDeviceImageLink())
        # 34-手Q测试服
        select_section(5)
        high_debug()
        enter_result = enter_newplayer(EVENTCLICKTIME,reporter)
    except:
        reportr_write(EVENTCLICKTIME, reporter, "拉起游戏", "进入登录界面", "StartGame", "Failed", "", getDeviceImageLink())
        return

    # 新手
    if enter_result == 1:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导", "进入引导", "BeginLead", "Success", "", getDeviceImageLink())
        # newbieInGame_1-5是1-3级的新手引导的不同阶段程序
        newbieInGame_1(reporter)
        newbieInGame_2(reporter)
        newbieInGame_3(reporter)
        newbieInGame_4(reporter)
        newbieInGame_5(reporter)
        # 升级到4级,获得成就 触发成就引导
        gm_input(["svr addexp 575","svr addthing 10001 10000"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-成就", "升到4级", "Upgrade->4", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_AchievementArriveDlg/Root/Confirm"))
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到5级，领取刺客赛车，触发改装引导
        gm_input(["svr addexp 750"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-改装", "升到5级", "Upgrade->5", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToTask"))
        time.sleep(5)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_TaskScreen/AnchorLeft/TaskTab/ChannelTable/NewBieTarget/PullDown/Grid/LevelTasks"))
        time.sleep(5)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_NewbieTasks/AnchorCenter/TaskView/ListOffset/ScrollView/FashionGrid/1/CanOpen"))
        time.sleep(5)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_AchievementArriveDlg/Root/Confirm"))
        time.sleep(5)
        newbieOutGame(reporter)
        # 升级到6级，触发技巧教学引导
        gm_input(["svr addexp 850"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-技巧教学", "升到6级", "Upgrade->6", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到7级，触发邂逅引导
        gm_input(["svr addexp 950"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-邂逅", "升到7级", "Upgrade->7", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到8级，触发赛道教学引导
        gm_input(["svr addexp 1000"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-赛到教学", "升到8级", "Upgrade->8", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到9级，触发休闲区引导
        gm_input(["svr addexp 1050"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-休闲区", "升到9级", "Upgrade->9", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到10级，触发天赋引导
        gm_input(["svr addexp 1150","svr setlicenselevel 2"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-天赋", "升到10级", "Upgrade->10", "Success", "", getDeviceImageLink())
        # 确定获得成就
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_AchievementArriveDlg/Root/Confirm"))
        time.sleep(5)
        engine.click_position(400, 300)
        time.sleep(5)
        # 退出游戏重进 使驾照gm指令生效
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_TopNavView/Anchor/AnimatRoot/RightBtnRoot/Btn_Setting"))
        time.sleep(5)
        screen_shot_click(find_elment_wait(
            "/UIRoot/OG_LB_SettingView/AnchorCenter/BasicSetPanel/BasicScrollViewSet/AnchorBottom/PrivacySet/ServiceInfo/Btn_ExitLogin"))
        time.sleep(30)
        screen_shot_click(find_elment_wait("/UIRoot/OG_FL_ServerChoseView/Start/AnchorBottom/Button_Big_Name(Yellow)"))
        time.sleep(50)
        newbieOutGame(reporter)
        # 升级到11级，触发情侣引导---当前测试包程序无法点击返回按钮
        gm_input(["svr addexp 1200"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-情侣", "升到11级", "Upgrade->11", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到12级，触发超能引导
        gm_input(["svr addexp 1250"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-超能", "升到12级", "Upgrade->12", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        # 进入对战房间
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/ModeRoot/Button_PVP"))
        time.sleep(3)
        # 触发超能引导
        screen_shot_click(find_elment_wait("/UIRoot/OG_RoomListView/AnchorLeft/TitlePanel/ChannelTable/ActionSpeed"))
        newbieOutGame(reporter)
        # 升级到13级，触发图鉴引导
        gm_input(["svr addexp 1250"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-图鉴", "升到13级", "Upgrade->13", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 触发滑板引导
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/ModeRoot/Button_PVP"))
        time.sleep(3)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_EntertainmentScreen/AnchorLeft/TitlePanel/Table/Classical"))
        time.sleep(3)
        screen_shot_click(find_elment_wait("/UIRoot/OG_RoomListView/AnchorLeft/TitlePanel/ChannelTable/SkateBoard"))
        time.sleep(5)
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
        time.sleep(3)
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/TeachBtn"))
        time.sleep(15)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-滑板", "滑板引导", "SkateBord", "Success", "", getDeviceImageLink())
        skateInGame(reporter)
        time.sleep(8)
        newbieOutGame(reporter)
        # 升级到14级，触发车队引导
        gm_input(["svr addexp 1300"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-车队", "升到14级", "Upgrade->14", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到15级，触发排位赛引导
        gm_input(["svr addexp 1350"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-排位赛", "升到15级", "Upgrade->15", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 触发超时空引导
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/ModeRoot/Button_PVP"))
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-超时空", "超时空引导", "Upgrade->15", "Success", "", getDeviceImageLink())
        time.sleep(3)
        screen_shot_click(find_elment_wait("/UIRoot/OG_RoomListView/AnchorLeft/TitlePanel/ChannelTable/HyperSpace"))
        time.sleep(3)
        newbieOutGame(reporter)
        # 升级到16级，触发新剧情模式引导
        gm_input(["svr addexp 1350"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-新剧情模式（失落的手稿）", "升到16级", "Upgrade->17", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRight/AnimatRoot/ModeRoot/Button_StoryLine"))
        time.sleep(5)
        newbieOutGame(reporter)
        # 升级到17级，触发赛道之王引导
        gm_input(["svr addexp 1400"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-赛道之王", "升到17级", "Upgrade->17", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到18级，触发街区车王引导
        gm_input(["svr addexp 1450"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-街区车王", "升到18级", "Upgrade->18", "Success", "", getDeviceImageLink())
        engine.click_position(400, 300)
        time.sleep(5)
        KnapsackInAndOut()
        newbieOutGame(reporter)
        # 升级到50级，触发职业驾照引导
        gm_input(["svr addexp 387915", "svr setlicenselevel 4"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-职业驾照", "升到50级", "Upgrade->50", "Success", "", getDeviceImageLink())
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_AchievementArriveDlg/Root/Confirm"))
        time.sleep(5)
        engine.click_position(400, 300)
        time.sleep(5)
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_AchievementArriveDlg/Root/Confirm"))
        time.sleep(5)
        newbieOutGame(reporter)
        # 触发职业挑战引导
        gm_input(["svr setlicenselevel 5"])
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-职业挑战", "职业挑战引导", "Upgrade->50", "Success", "", getDeviceImageLink())
        # 退出游戏重进 使驾照gm指令生效
        screen_shot_click(find_elment_wait("/UIRoot/OG_LB_TopNavView/Anchor/AnimatRoot/RightBtnRoot/Btn_Setting"))
        time.sleep(5)
        screen_shot_click(find_elment_wait(
            "/UIRoot/OG_LB_SettingView/AnchorCenter/BasicSetPanel/BasicScrollViewSet/AnchorBottom/PrivacySet/ServiceInfo/Btn_ExitLogin"))
        time.sleep(30)
        screen_shot_click(find_elment_wait("/UIRoot/OG_FL_ServerChoseView/Start/AnchorBottom/Button_Big_Name(Yellow)"))
        time.sleep(40)
        newbieOutGame(reporter)
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导", "进入引导", "BeginLead", "Failed", "TimeOut", getDeviceImageLink())
    reporter.close()


def reportr_write(clicktime,reporter,testScence,case,element,test_result,failed_reason,screenshot_link):
    clicktime = time.time()
    report.screenshot()
    reporter.write("{0},{1},{2},{3},{4},{5},{6}\n".format(testScence, case, element, test_result, failed_reason,screenshot_link,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    reporter.flush()

# 加等级后 通过进出背包触发新手引导
def KnapsackInAndOut():
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_LobbyView/AnchorRightBottom/AnimaRoot/Grid/GoToKnapsack"))
    time.sleep(2)
    screen_shot_click(find_elment_wait("/UIRoot/OG_LB_BackpackView/AnchorLeftTop/Back"))
    time.sleep(3)


# 单局外---自动引导通用程序
def newbieOutGame(reporter):
    # 开始扫描单局外引导过程，检测并触发单局外引导
    while(True):
        # fullmask=屏幕有遮罩层的场景，为空代表没有遮罩层
        fullmask = None
        # 检查界面是否有遮罩层
        fullmask = engine.find_elements_path("FullMask")
        # print(fullmask)
        # 有遮罩层
        if(fullmask):
            # 需要点击的位置
            btn = None
            # 获取整个界面可点击的控件
            elements = engine.get_touchable_elements()
            # 获取每个控件
            for element in elements:
                print element[0]
                # 获取控件的路径名称
                element_val = element[0].object_name
                # 已/为分隔符，拆分控件路径
                element_vals = element_val.split('/')
                # 遍历并判断每个名称
                for val in element_vals:
                    # 如果是强引导按钮 则将路径赋值给点击位
                    if(val == "ForwardPanel"):
                        btn = element_val
                        break
                    # 如果是领奖控件 则将路径赋值给点击位
                    elif(val == "Button_Mid_Name(Blue)"):
                        btn = element_val
                        break
                    # 如果是返回控件 则将路径赋值给点击位
                    elif(val == "Back"):
                        btn = element_val
                        break
            # 没有找到控件 点击屏幕通过指引型引导
            if(btn == None):
                time.sleep(2)
                screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
                # screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
                reportr_write(EVENTCLICKTIME, reporter, "新手引导-通用引导", "点击屏幕，通过引导提示", "ClickScreen", "Success", "", getDeviceImageLink())
                time.sleep(1)
            # 点击相应控件
            else:
                print(btn)
                btnclick = find_elment_wait(btn)
                if(btnclick):
                    screen_shot_click(btnclick)
                    reportr_write(EVENTCLICKTIME, reporter, "新手引导-通用引导", "点击按钮", btnclick.object_name, "Success", "", getDeviceImageLink())
                else:
                    reportr_write(EVENTCLICKTIME, reporter, "新手引导-通用引导", "点击按钮", btnclick.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
                time.sleep(5)
            time.sleep(1)
        # 没有遮罩层
        else:
            btn = None
            elements = engine.get_touchable_elements()
            for element in elements:
                print element[0]
                element_val = element[0].object_name
                element_vals = element_val.split('/')
                # 遍历并判断每个名称，如果有返回按钮，则将路径赋值给点击位
                for val in element_vals:
                    if (val == "Back"):
                        btn = element_val
                        break
                    elif(val == "ReturnBack"):
                        btn = element_val
                        break
                    elif(val == "CallBackBtn"):
                        btn = element_val
                        break
                    elif(val == "Button_close"):
                        btn = element_val
                        break
                    elif (val == "CloseBtn"):
                        btn = element_val
                        break
                    elif (val == "Button_Mid_CloseBtn"):
                        btn = element_val
                        break
                    elif (val == "BackBtn"):
                        btn = element_val
                        break
                    elif (val == "ButtonClose"):
                        btn = element_val
                        break
                    elif (val == "Button_Mid_Name"):
                        btn = element_val
                        break
            print(btn)
            # 检查是否是情侣界面
            ql_back = find_elment_wait("/UIRoot/OG_LB_MarriageNoLoverMainPageDlg/AnchorRight/OpenWeddingHallListDlgBtn", 1)
            # 找到相应返回控件，点击返回
            if(btn != None):
                btnback = find_elment_wait(btn)
                if(btnback):
                    screen_shot_click(btnback)
                    reportr_write(EVENTCLICKTIME, reporter, "新手引导-通用引导", "点击返回", btnback.object_name, "Success", "", getDeviceImageLink())
                    if(ql_back):
                        engine.click_position(50, 30)
                else:
                    reportr_write(EVENTCLICKTIME, reporter, "新手引导-通用引导", "点击返回", btnback.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
                time.sleep(5)
            elif(ql_back):
                engine.click_position(50, 30)
            # 没有找到返回控件，代表引导结束
            else:
                print("该阶段引导结束")
                break


# 单局内---滑板引导通用程序
def skateInGame(reporter):
    driftBtn_bound = None
    while True:
        rt_btn = find_elment_wait("/UIRoot/IG_LicenseSettleView/SucceededRoot/Right/ReturnBtn", 1)
        if rt_btn:
            screen_shot_click(rt_btn)
            break
        elements = engine.get_touchable_elements()
        for element in elements:
            element_path = element[0].object_name
            if "/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/ErrorBtn" in element_path or "/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/HUDBtn" in element_path or "/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button" in element_path:
                print "useless"
            elif "/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/DriftBtn" in element_path:
                print 'drift'
                driftBtn_bound = engine.get_element_bound(element[0])
                engine.press(element[0], 3000)
                time.sleep(1)
                reportr_write(EVENTCLICKTIME, reporter, "新手引导-滑板引导", "长按压板", "PressSkate", "Success", "",getDeviceImageLink())
            elif "/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/RSteerButton" in element_path or "/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/LSteerButton" in element_path:
                cu_bound = engine.get_element_bound(element[0])
                if driftBtn_bound is not None:
                    print 'multi click'
                    engine.multi_press_position(cu_bound.x + cu_bound.width / 2, cu_bound.y + cu_bound.height / 2,
                                                driftBtn_bound.x + driftBtn_bound.width / 2,
                                                driftBtn_bound.y + driftBtn_bound.height / 2)
                    time.sleep(1)
                    reportr_write(EVENTCLICKTIME, reporter, "新手引导-滑板引导", "转向+漂移-通过碗道", "BankDash", "Success", "", getDeviceImageLink())
                else:
                    print 'single touch'
                    screen_shot_click(element[0])
            else:
                screen_shot_click(element[0])
                reportr_write(EVENTCLICKTIME, reporter, "新手引导-滑板引导", "点击屏幕-通过介绍", "ClickScreen", "Success", "", getDeviceImageLink())
        time.sleep(2)


# 1级新手引导
def newbieInGame_1(reporter):
    # 等待进入开场介绍
    current_scene = engine.get_scene()
    if(current_scene == "Level_TrainTrack_A_Art"):
        sign = 1
    wait_sign = wait_for_scene("Level_TrainTrack_A_Art")
    if(wait_sign == True):
        # 通过开场介绍
        time.sleep(5)
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
        time.sleep(20)
        # 跳过介绍
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
        time.sleep(2)
        xiaopen_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/QTEView/QteEff/Lighrt", 5)
        if(xiaopen_btn):
            screen_shot_click(xiaopen_btn)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "点击小喷", xiaopen_btn.object_name, "Success", "", getDeviceImageLink())
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "点击小喷", xiaopen_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(10)
        # 右转弯
        right = engine.find_element("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/RSteerButton")
        if(right):
            engine.press(right, 2000)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "右转弯", right.object_name, "Success", "", getDeviceImageLink())
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "右转弯", right.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(10)
        # 左转弯
        left = engine.find_element("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/LSteerButton")
        if(left):
            engine.press(left, 2000)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "左转弯", left.object_name, "Success", "", getDeviceImageLink())
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "左转弯", left.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(10)
        # 通过漂移演示
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
        time.sleep(20)
        # 通过漂移操作演示1
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
        time.sleep(15)
        # 通过漂移操作演示2
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
        time.sleep(15)
        # 通过漂移操作演示3
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "漂移演示", "Drift_demon", "Success", "", getDeviceImageLink())
        time.sleep(15)
        # 通过漂移尝试的介绍
        screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "漂移介绍", "Drift_intruduce", "Success", "", getDeviceImageLink())
        time.sleep(10)
        # 使用右漂移 通过引导
        right = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/RSteerButton", 5)
        drift = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/DriftBtn", 5)
        if(right):
            engine.double_click(right, drift)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "向右漂移", right.object_name + " + " + drift.object_name, "Success", "", getDeviceImageLink())
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "向右漂移", "RightDrift", "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(1)
        # 触发小喷
        xiaopen_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/SmallBoostButton/BG", 5)
        if(xiaopen_btn):
            screen_shot_click(xiaopen_btn)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "点击小喷", xiaopen_btn.object_name, "Success", "", "xxx.pgn")
            time.sleep(10)
        # 使用左漂移 通过引导
        left = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/LSteerButton")
        drift = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/DriftBtn", 5)
        if(left):
            engine.double_click(left, drift)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "向左漂移", left.object_name + " + " + drift.object_name, "Success", "", getDeviceImageLink())
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "向右漂移", "LeftDrift", "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(1)
        # 触发小喷
        xiaopen_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/SmallBoostButton/BG", 5)
        if(xiaopen_btn):
            screen_shot_click(xiaopen_btn)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "点击小喷", xiaopen_btn.object_name, "Success", "", getDeviceImageLink())
            time.sleep(5)
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "点击小喷", xiaopen_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
        # 开启托管
        # tuoguan()
        # 往前行驶
        time.sleep(30)
        # 使用氮气
        danqi = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/PropsSlot_0", 10)
        if(danqi):
            screen_shot_click(danqi)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "使用氮气", danqi.object_name, "Success", "", getDeviceImageLink())
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "使用氮气", danqi.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(10)
        # 使用小喷
        xiaopen_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/SmallBoostButton", 5)
        if(xiaopen_btn):
            screen_shot_click(xiaopen_btn)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "点击小喷", xiaopen_btn.object_name, "Success", "", getDeviceImageLink())
            time.sleep(5)
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "点击小喷", xiaopen_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(10)
        # 点击返回 进入游戏大厅
        back_btn = find_elment_wait("/UIRoot/IG_LicenseSettleView/SucceededRoot/Right/ReturnBtn")
        if(back_btn):
            screen_shot_click(back_btn)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "返回大厅", back_btn.object_name, "Success", "", getDeviceImageLink())
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "返回大厅", back_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(50)
        # 驾驶新手赛车
        drive_btn = find_elment_wait("/UIRoot/OG_LB_GetNewVehicleView/AnchorButtom/AnimRoot/Offset/Btn/DriveBtn")
        if(drive_btn):
            screen_shot_click(drive_btn)
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "驾驶新手赛车", drive_btn.object_name, "Success", "", getDeviceImageLink())
        else:
            reportr_write(EVENTCLICKTIME, reporter, "新手引导-基础操作", "驾驶新手赛车", drive_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
        time.sleep(20)

# 匹配竞速单局引导
def newbieInGame_2(reporter):
    # 跳过实战比赛的介绍
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(10)
    # 进入对战房间
    pvproom = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/Button_PVP")
    if(pvproom):
        screen_shot_click(pvproom)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "进入对战房间", pvproom.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "进入对战房间", pvproom.object_name, "Failed", "CRASH", getDeviceImageLink())
    time.sleep(5)
    # 进入匹配房间
    matchroom = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/MatchBtn")
    if(matchroom):
        screen_shot_click(matchroom)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "进入匹配房间", matchroom.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "进入匹配房间", matchroom.object_name, "Failed", "CRASH", getDeviceImageLink())
    time.sleep(5)
    # 进入个人竞速房间
    spdroom = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/ECGMT_SPEED_SINGLE_GAME")
    if(spdroom):
        screen_shot_click(spdroom)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "进入个人匹配房间", spdroom.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "进入个人匹配房间", spdroom.object_name, "Failed", "CRASH", getDeviceImageLink())
    time.sleep(10)
    # 开始匹配
    start_match = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/StartBtn")
    if(start_match):
        screen_shot_click(start_match)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "开始匹配", start_match.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "开始匹配", start_match.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    # 等待进入单局
    time.sleep(20)
    wait_sign = wait_for_scene_danju("LevelArt")
    if(wait_sign == True):
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "单局开始", "Game_Start", "Success", "", getDeviceImageLink())
        # 开启托管
        auto_tuoguan()
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "开启托管", "Game_Host", "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "单局开始", "Game_Start", "Failed", "TIMEOUT/CRASH", getDeviceImageLink())
    time.sleep(200)
    # 通过结算页签
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "单局结束", "EndMatch", "Success", "", getDeviceImageLink())
    time.sleep(10)
    # 退出单局
    backgame = find_elment_wait("/UIRoot/IG_SettleView/AnchorBottom/BottomOffset/BackButton")
    if(backgame):
        screen_shot_click(backgame)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "退出单局", backgame.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "退出单局", backgame.object_name, "Failed", "CRASH", getDeviceImageLink())
    time.sleep(30)
    # 升级弹窗
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(5)
    # 返回对战房间
    backroom = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/Back")
    if(backroom):
        screen_shot_click(backroom)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "返回房间", backroom.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "返回房间", backroom.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
    # 返回大厅
    backhall = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/ReturnBack")
    if(backhall):
        screen_shot_click(backhall)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "返回大厅", backhall.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-个人竞速", "返回大厅", backhall.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(20)

# 道具赛教学引导
def newbieInGame_3(reporter):
    # 通过道具赛的介绍
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    # 等待进入道具赛单局
    time.sleep(40)
    # 通过道具赛介绍1
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(10)
    # 通过道具赛介绍2
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(10)
    qte_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/QTEView")
    if(qte_btn):
        screen_shot_click(qte_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "触发QTE", qte_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "触发QTE", qte_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    # 通过导弹引导1
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(10)
    # 通过导弹引导2
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(15)
    # 通过导弹引导3
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(15)
    reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "导弹介绍", "missile_introduce", "Success", "", getDeviceImageLink())
    # 点击导弹
    slot_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/PropsSlot_0")
    if(slot_btn):
        screen_shot_click(slot_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "导弹瞄准", slot_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "导弹瞄准", slot_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(20)
    # 点击释放导弹
    slot_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/PropsSlot_0")
    if(slot_btn):
        screen_shot_click(slot_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "导弹发射", slot_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "导弹发射", slot_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(10)
    # 通过防御介绍1
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(10)
    # 通过防御介绍2
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(10)
    reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "防御介绍", "defense_introduce", "Success", "", getDeviceImageLink())
    # 点击释放护盾
    slot_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/PropsSlot_0")
    if(slot_btn):
        screen_shot_click(slot_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "使用护盾", slot_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "使用护盾", slot_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(20)
    # 通过传递道具的介绍
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(10)
    # 通过传递道具的演示
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "道具传递介绍", "transmit_introduce", "Success", "", getDeviceImageLink())
    time.sleep(15)
    btn1 = engine.find_element("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/PropsSlot_0")
    btn2 = engine.find_element("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/TeammateHead_1")
    b1 = engine.get_element_bound(btn1)
    b2 = engine.get_element_bound(btn2)
    trans_result = engine.swipe_and_press(b1.x + b1.width / 2, b1.y + b1.height / 2, b2.x + b2.width / 2, b2.y + b2.height / 2, 50, 1000)
    if(trans_result):
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "传递道具", btn1.object_name + "--->" + btn2.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "传递道具", btn1.object_name + "--->" + btn2.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(10)
    # 使用氮气
    dq_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/PropsSlot_0")
    if(dq_btn):
        screen_shot_click(dq_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "使用氮气", dq_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "使用氮气", dq_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(20)
    # 返回大厅
    return_btn = find_elment_wait("/UIRoot/IG_LicenseSettleView/SucceededRoot/Right/ReturnBtn")
    if(return_btn):
        screen_shot_click(return_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "返回大厅", return_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "返回大厅", return_btn.object_name, "Failed", "CRASH", getDeviceImageLink())
    time.sleep(30)
    # 确认获得新手驾照
    close_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/CloseBtn")
    if(close_btn):
        screen_shot_click(close_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "领取新手驾照", close_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "领取新手驾照", close_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
    # 返回大厅
    back_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/Back")
    if(back_btn):
        screen_shot_click(back_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "返回大厅", back_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-道具教学", "返回大厅", back_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(20)

# 组队道具赛引导
def newbieInGame_4(reporter):
    # 通过组队道具赛介绍
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(15)
    # 进入对战房间
    pvp_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/Button_PVP")
    if(pvp_btn):
        screen_shot_click(pvp_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "进入对战房间", pvp_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "进入对战房间", pvp_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
    # 进入匹配房间
    match_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/MatchBtn")
    if(match_btn):
        screen_shot_click(match_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "进入匹配房间", match_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "进入匹配房间", match_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
    # 进入组队道具赛房间
    team_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/ECGMT_PROP_TEAM_GAME")
    if(team_btn):
        screen_shot_click(match_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "进入组队道具房间", team_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "进入组队道具房间", team_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/ECGMT_PROP_TEAM_GAME"))
    # 开始匹配
    start_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/StartBtn")
    if(start_btn):
        screen_shot_click(start_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "开始匹配", start_btn.object_name, "Success", "", getDeviceImageLink())
        time.sleep(5)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "单局开始", "Game_Start", "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "开始匹配", start_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(220)
    # 通过结算页签
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "单局结束", "Game_End", "Success", "", getDeviceImageLink())
    time.sleep(10)
    # 退出单局
    back_btn = find_elment_wait("/UIRoot/IG_SettleView/AnchorBottom/BottomOffset/BackButton")
    if(back_btn):
        screen_shot_click(back_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "退出单局", back_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "退出单局", back_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(30)
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(3)
    # 返回对战房间
    back_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/Back")
    if(back_btn):
        screen_shot_click(back_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回对战房间", back_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回对战房间", back_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
    # 返回大厅
    return_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/ReturnBack")
    if(return_btn):
        screen_shot_click(return_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回大厅", return_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回大厅", return_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(20)

# 萌新任务引导
def newbieInGame_5(reporter):
    # 进入任务入口
    go_task = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/GoToTask")
    if(go_task):
        screen_shot_click(go_task)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "点击任务入口", go_task.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "点击任务入口", go_task.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(20)
    # 通过萌新介绍
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    # 领取萌新奖励
    get_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/GetRewardBtn")
    if(get_btn):
        screen_shot_click(get_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "领取萌新奖励", get_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "领取萌新奖励", get_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(15)
    # 通过奖励介绍1
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(15)
    # 通过奖励介绍2
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(15)
    # 进入开局送炫装
    task_btn = find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/GameTasks")
    if(task_btn):
        screen_shot_click(task_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "点击炫装任务", task_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "点击炫装任务", task_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
    # 前往任务完成比赛
    goto_btn =find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/Goto")
    if(goto_btn):
        screen_shot_click(goto_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "点击前往任务", goto_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "点击前往任务", goto_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(15)
    # 通过任务介绍
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    time.sleep(10)
    # 进入个人竞速匹配房间
    screen_shot_click(find_elment_wait("/UIRoot/OG_SelectGameModelDialog/Anchor/UIGrid/ECGMT_SPEED_SINGLE_GAME"))
    time.sleep(10)
    # 开始匹配
    start_btn = find_elment_wait("/UIRoot/OG_LB_RoomTeamView/AnchorButtom/Offset/StartBtn")
    if(start_btn):
        screen_shot_click(start_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "开始匹配", start_btn.object_name, "Success", "", getDeviceImageLink())
        time.sleep(5)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "单局开始", "Game_Start", "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "开始匹配", start_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(220)
    # 通过结算页签
    screen_shot_click(find_elment_wait("/UIRoot/IG_TutorialDialog/Anchor/Tutorial/FullMask"))
    reportr_write(EVENTCLICKTIME, reporter, "新手引导-萌新任务", "单局结束", "Game_End", "Success", "", getDeviceImageLink())
    time.sleep(10)
    # 退出单局
    back_btn = find_elment_wait("/UIRoot/IG_SettleView/AnchorBottom/BottomOffset/BackButton")
    if (back_btn):
        screen_shot_click(back_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "退出单局", back_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "退出单局", back_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(30)
    # 返回对战房间
    # 返回对战房间
    back_btn = find_elment_wait("/UIRoot/OG_LB_RoomTeamView/AnchorTopLeft/Back")
    if (back_btn):
        screen_shot_click(back_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回对战房间", back_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回对战房间", back_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
    # 返回任务界面
    return_back = find_elment_wait("/UIRoot/OG_RoomListView/AnchorTopLeft/Top_all/ReturnBack")
    if (return_back):
        screen_shot_click(return_back)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回任务界面", return_back.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回任务界面", return_back.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(20)
    # 返回大厅
    back_btn = find_elment_wait("/UIRoot/OG_LB_TaskScreen/AnchorTopLeft/Public/BackBtn")
    if (back_btn):
        screen_shot_click(back_btn)
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回大厅", back_btn.object_name, "Success", "", getDeviceImageLink())
    else:
        reportr_write(EVENTCLICKTIME, reporter, "新手引导-组队道具", "返回大厅", back_btn.object_name, "Failed", "TIMEOUT", getDeviceImageLink())
    time.sleep(5)
