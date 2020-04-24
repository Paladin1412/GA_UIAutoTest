# -*- coding: UTF-8 -*-
import datetime
import sys
import os
# from cube.cube_manager import get_cube_client
# from testcase.nsstest import enter_gamecenter_wait, exit_server, return_home, close_activity, team_prop_join_player, \
#     auto_tuoguan, create_motorcade, steal_pig, skip_newer_tech, join_team_player, room_apply_jointeam,  dress, joinout_steal_pig, join_team3droom,Novice_Guidance,test_run,GameOutGuidance

reload(sys)
sys.setdefaultencoding("utf-8")
from wpyscripts.wetest.element import Element
from wpyscripts.wetest.engine import ElementBound

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from testcase.tools import *
from wpyscripts.common.utils import *

# from poster.encode import multipart_encode
import urllib2
import urllib
import json
# from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers

def filepath(file):
    log_dir = os.environ.get("UPLOADDIR")
    file_path = os.path.split(os.path.realpath(__file__))[0]
    if log_dir:
        file_path = os.path.abspath(os.path.join(log_dir, file))
    else:
        file_path = os.path.abspath(os.path.join(os.path.dirname(file_path), file))
    return file_path

#上传文件到服务器，并返回生成的URL
# def postFileToSvr(file_path, url):
#     tmp_url =''
#     register_openers()
#     f = open(file_path.decode('utf-8'), 'rb')
#     datagen, headers = multipart_encode({"fileToUpload": f})
#     request = urllib2.Request(url, datagen, headers)
#     try:
#         response = urllib2.urlopen(request)
#         tmp_res = response.read()
#         if 'Sorry' in tmp_res:
#             print tmp_res
#         else:
#             res = json.loads(tmp_res)
#             tmp_url = urllib.unquote(res['url'])
#         return tmp_url
#     except urllib2.URLError, e:
#         print e.reason
#         print e.code
#     f.close()


# def getDeviceImageLink():
#     global EVENTCLICKTIME
#     logLinkList = {}
#     imagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot")
#     os.system("dir %s\\*.png /b > images.txt"%imagePath)
#     testLog = []
#     f = open("images.txt")
#     for line in f.readlines():
#         testLog.append(line)
#     f.close()
#     #根据时间获取对应的截图路径
#     logLinkList = "NOIMAGELOG"
#     # 设置3s延迟时间，找3s内的截图，增加截图获取成功率
#     delayTimeStamp = EVENTCLICKTIME + 2
#     beforeTimeStamp = EVENTCLICKTIME - 2
#     for singleImageLog in testLog:
#         imageLogTime = time.mktime(time.strptime(singleImageLog.split(".")[0], '%Y%m%d%H%M%S'))
#         # logger.debug(">>>>>>>>>>>>>jietushijian:%s>>>>>>>>jilushijian:%s>>>>>"%(imageLogTime, EVENTCLICKTIME))
#         if(beforeTimeStamp <= imageLogTime and delayTimeStamp >= imageLogTime):
#             # print(EVENTCLICKTIME)
#             logLinkList = "%s\\%s"%(imagePath, singleImageLog.strip('\n') )
#             img_url = postFileToSvr(logLinkList, "http://10.125.32.148/upload.php")
#             # print(">>>%s>>>"%logLinkList)
#             break
#     return img_url