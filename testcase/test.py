# -*- coding: UTF-8 -*-
import datetime
import sys
import os
from cube.cube_manager import get_cube_client
# from testcase.MyTestAPI import enter_gamecenter_wait, exit_server, return_home, close_activity, team_prop_join_player, \
#     auto_tuoguan, create_motorcade, steal_pig, skip_newer_tech, join_team_player, room_apply_jointeam,  dress, joinout_steal_pig, join_team3droom,test_run
from testcase.NewbieTest import newbie_lead
reload(sys)
sys.setdefaultencoding("utf-8")
from wpyscripts.wetest.element import Element
from wpyscripts.wetest.engine import ElementBound
from WeTestAPI import WeTestApi
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from testcase.tools import *
from wpyscripts.common.utils import *

# from poster.encode import multipart_encode
import urllib2
import urllib
import json
# from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers
authparams = {
    "secretid": "VW44hkA8Py8cW9mU",
    "secretkey": "TH2WlPtJS8abhX4S",
}
wetestClient = WeTestApi(authparams, "http://api.wetest.qq.com")
report = manager.get_reporter()

def main():
    common_label = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Label")
    common_text = engine.get_element_text(common_label)
    print common_text
    if common_text == u'服务器连接失败，请您检查一下网络再试试':
        ensure_btn = find_elment_wait("/UIRoot/C_Com_DialogCommon1/Anchor/Button_Mid_Name(Yellow)")
        screen_shot_click(ensure_btn)
        print 1
    else:
        print 2



def filepath(file):
    log_dir = os.environ.get("UPLOADDIR")
    file_path = os.path.split(os.path.realpath(__file__))[0]
    if log_dir:
        file_path = os.path.abspath(os.path.join(log_dir, file))
    else:
        file_path = os.path.abspath(os.path.join(os.path.dirname(file_path), file))
    return file_path

#上传文件到服务器，并返回生成的URL
def postFileToSvr(file_path, url):
    tmp_url =''
    register_openers()
    f = open(file_path.decode('utf-8'), 'rb')
    datagen, headers = multipart_encode({"fileToUpload": f})
    request = urllib2.Request(url, datagen, headers)
    try:
        response = urllib2.urlopen(request)
        tmp_res = response.read()
        if 'Sorry' in tmp_res:
            print tmp_res
        else:
            res = json.loads(tmp_res)
            tmp_url = urllib.unquote(res['url'])
        return tmp_url
    except urllib2.URLError, e:
        print e.reason
        print e.code
    f.close()


def getDeviceImageLink():
    global EVENTCLICKTIME
    logLinkList = {}
    testid = os.environ.get("TESTID")
    deviceid = os.environ.get("DEVICEID")
    testLog = wetestClient.get_test_device_image_log(testid,deviceid)
    # testLog = wetestClient.get_test_device_image_log("616236a643e007b2e7da1b4810773005", "b4dff4a8747f92ced2cb424e8b57d8ea")
    #根据时间获取对应的截图链接
    # logger.debug("====testid = {}".format(testid))
    # logger.debug("====deviceid = {}".format(deviceid))
    logger.debug("====testLog = {}".format(testLog))
    logLinkList["url"] = " "
    if testLog is None:
        return logLinkList
    imageLog = testLog[u'images']
    # 设置3s延迟时间，找3s内的截图，增加截图获取成功率
    delayTimeStamp = EVENTCLICKTIME + 3
    beforeTimeStamp = EVENTCLICKTIME - 3
    for singleImageLog in imageLog:
        imageLogTime = time.mktime(time.strptime(singleImageLog[u'date'], '%Y-%m-%d %H:%M:%S'))
        # logger.debug(">>>>>>>>>>>>>jietushijian:%s>>>>>>>>jilushijian:%s>>>>>"%(imageLogTime, EVENTCLICKTIME))
        if(beforeTimeStamp <= imageLogTime and delayTimeStamp >= imageLogTime):
            # print(EVENTCLICKTIME)
            logLinkList["url"] = singleImageLog[u'url']
            break
    logLinkList["mmlog"] = testLog[u'mmlog']
    logLinkList["log"] = testLog[u'log']
    # logLinkList["url"] = "http://wetest.oa.com"
    return logLinkList




def log_test():
    file_path = filepath("NssGame_BVT.log")
    if os.path.exists(file_path):
        os.remove(file_path)
    reporter = open(file_path, "w")


    global EVENTCLICKTIME
    import  parseConfigDist as parseConfigDist
    filedir = os.path.split(os.path.realpath(__file__))[0]
    filepaths = os.path.join(os.path.dirname(filedir), "data/elements.txt")
    configDist = parseConfigDist.MainPathConfigParser(filepaths)
    configDist.parse()
    MainPathCoverCheckList = configDist.MainPathCoverCheckList

    EVENTCLICKTIME = time.time()
    report.screenshot()
    reporter.write("{0},{1},{2},{3},{4},{5},{6}\n".format("登录游戏", "进入大厅", "LoginFailed", False, "LoginFailed",
                                                          "http//www.baidu.com",
                                                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    reporter.flush()
    reporter.close()


# # 单局内---滑板引导通用程序
# def skateInGame():
#     driftBtn_bound = None
#     while True:
#         rt_btn = find_elment_wait("/UIRoot/IG_LicenseSettleView/SucceededRoot/Right/ReturnBtn", 1)
#         if rt_btn:
#             screen_shot_click(rt_btn)
#             break
#         elements = engine.get_touchable_elements()
#         for element in elements:
#             element_path = element[0].object_name
#             if "/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/ErrorBtn" in element_path or "/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/HUDBtn" in element_path or "/UIRoot/ViewProfiler/StaiticUI/Anchor/BtnRoot/Button" in element_path:
#                 print "useless"
#             elif "/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/DriftBtn" in element_path:
#                 print 'drift'
#                 driftBtn_bound = engine.get_element_bound(element[0])
#                 engine.press(element[0], 3000)
#                 time.sleep(1)
#
#             elif "/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/RSteerButton" in element_path or "/UIRoot/IG_TutorialDialog/Anchor/Tutorial/ForwardPanel/LSteerButton" in element_path:
#                 cu_bound = engine.get_element_bound(element[0])
#                 if driftBtn_bound is not None:
#                     print 'multi click'
#                     engine.multi_press_position(cu_bound.x + cu_bound.width / 2, cu_bound.y + cu_bound.height / 2,
#                                                 driftBtn_bound.x + driftBtn_bound.width / 2,
#                                                 driftBtn_bound.y + driftBtn_bound.height / 2)
#                     time.sleep(1)
#
#                 else:
#                     print 'single touch'
#                     screen_shot_click(element[0])
#             else:
#                 screen_shot_click(element[0])
#
#         time.sleep(2)

if __name__ == '__main__':
    newbie_lead()
    # skateInGame()
    # engine.click_position(50,30)
    # engine.click_position()
    # log_test()
    # btn = find_elment_wait("/UIRoot/OG_LB_MarriageNoLoverMainPageDlg/AnchorLeftTop/Back",5)
    # print(btn)
    # screen_shot_click(btn)
