# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'

import os
import json
import random
import sys
import logging
import time
import traceback

from socket_client import SocketClient
from cube_exceptions import *

from cube_protocol import *

logger = logging.getLogger("wetest")


class CubeClient(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.seq = 0
        self.session_id = random.randint(0, sys.maxint)
        self.socket = SocketClient(self.address, self.port)
        self.status = CubeStatus.UNKNOW

    def __get_session_id(self):
        return self.session_id

    def __get_seq(self):
        self.seq += 1
        return self.seq

    def __dec_seq(self):
        self.seq -= 1
        return self.seq

    def __get_user_name(self):
        return self.user_name

    def __get_msg_list(self, _server_type):
        msg_list = {}
        msg_list['session_id'] = self.__get_session_id()
        msg_list['serve_type'] = _server_type
        return msg_list

    def __send_command(self, _msg_list):
        for retry in range(0, 2):
            try:
                while True:
                    _msg_list["seq"] = self.__get_seq()
                    ret = self.socket.send_message(_msg_list, 100)
                    if ret['reply_type'] == CubeReplyCode.EXECUTING:
                        time.sleep(1)
                    else:
                        break
                if ret['reply_type'] != CubeReplyCode.SUCCESS:
                    self.__dec_seq()
                    message = "Error code: " + str(ret['reply_type']) + " msg: " + ret['error_msg']
                    logger.error(message)
                    if ret['reply_type'] == CubeRunErrorCode.DEVICE_NEED_ROOT:
                        raise DeviceNotRootError("手机未ROOT，无法使用CUBE服务")
                    elif ret['reply_type'] == CubeRunErrorCode.GET_MONITOR_FILE_ERROR:
                        raise GetMonitorFileError("由于游戏崩溃或其他原因，导致本次测试失败，需重新测试。")
                else:
                    return ret, CubeRunErrorCode.SUCCESS
            except DeviceNotRootError:
                stack = traceback.format_exc()
                logger.exception(stack)
                raise DeviceNotRootError("手机未ROOT，无法使用CUBE服务")
            except GetMonitorFileError:
                stack = traceback.format_exc()
                logger.exception(stack)
                return None, CubeRunErrorCode.CUBE_STOP_APP_ERROR
            except:
                stack = traceback.format_exc()
                logger.exception(stack)
                # os.system("adb shell ps")
                ret = self.recover_data()
                if ret is True:
                    return json.loads("{}"), CubeRunErrorCode.SUCCESS
        return None, CubeRunErrorCode.CUBE_ERROR

    def __detect_status(self):
        pass

    def connect_cube(self, _user_name):
        """
        连接cubex，与之沟通sessionid、seq、username
        :param _user_name:   wetest用户id，用于上传报告
        :return:  成功：cubex返回数据，失败：None
        """
        logger.debug("connect cube server.")
        msg_list = self.__get_msg_list(CubeServerType.CONNECTION_BUILD)
        self.user_name = _user_name # '133870'
        msg_list['user_name'] = self.user_name
        return self.__send_command(msg_list)

    def begin_cube_test(self, _game_name, _comment="", _test_type=CubeTestLevel.LIGHT, _snapshots=CubeSnapshots.OPEN):
        """
        开始测试，提供游戏包名、测试场景名，以及其他测试参数等，完成测试。
        :param _game_name:  待测游戏包名
        :param _comment: 测试场景名称
        :param _test_type:  测试类型（整形）。0：表示轻度性能，1：表示重度性能，2：表示资源测试，3：表示mono内存
        :param _snapshots:  截图功能（整形）。0：表示关闭截图，1：表示开启截图（截图暂时功能未开放）；
        :param _
        :return: 成功：cubex返回数据，失败：None
        """
        logger.debug("begin cube test.")
        msg_list = self.__get_msg_list(CubeServerType.BEGIN_TEST)
        msg_list['comment'] = _comment
        msg_list['target_name'] = _game_name
        msg_list['test_type'] = _test_type
        msg_list['snapshots'] = _snapshots
        ret, status = self.__send_command(msg_list)
        if ret is None :
            raise CubeRuntimeError("Can not launch the app!")
        else:
            return status

    def begin_unity_test(self, _game_name, _comment="", _test_type=CubeTestLevel.UNITY_PROFILE, _snapshots=CubeSnapshots.OPEN, _before5d6=0):
        """
        开始测试，提供游戏包名、测试场景名，以及其他测试参数等，完成测试。
        :param _game_name:  待测游戏包名
        :param _comment: 测试场景名称
        :param _test_type:  测试类型（整形）。0：表示轻度性能，1：表示重度性能，2：表示资源测试，3：表示mono内存
        :param _snapshots:  截图功能（整形）。0：表示关闭截图，1：表示开启截图（截图暂时功能未开放）；
        :param _before5d6:  unity版本是否高于5.6
        :return: 成功：cubex返回数据，失败：None
        """
        logger.debug("begin cube test.")
        msg_list = self.__get_msg_list(CubeServerType.BEGIN_TEST)
        msg_list['comment'] = _comment
        msg_list['target_name'] = _game_name
        msg_list['test_type'] = _test_type
        msg_list['snapshots'] = _snapshots
        msg_list['before5d6'] = _before5d6
        ret, status = self.__send_command(msg_list)
        if ret is None :
            raise CubeRuntimeError("Can not launch the app!")
        else:
            return status

    def mark_tag(self):
        """
        打标记
        :return:  成功：cubex返回数据，失败：None
        """
        logger.debug("cube scene tag.")
        msg_list = self.__get_msg_list(CubeServerType.SCENE_TAG)
        ret, status = self.__send_command(msg_list)
        if ret is None:
            raise CubeRuntimeError("Can not mark scene tag!")
        else:
            return status

    def scene_tag(self):
        """
        Deprecated function. 兼容老版本保留。
        打标记，请使用mark_tag()函数。
        :return:
        """
        self.mark_tag()

    def stop_cube_test(self):
        """
        停止测试
        :return:  成功：cubex返回数据，失败：None
        """
        logger.debug("stop cube test.")
        msg_list = self.__get_msg_list(CubeServerType.STOP_TEST)
        # print "msg_list=" + msg_list
        ret, status = self.__send_command(msg_list)
        if ret is None:
            raise CubeRuntimeError("Can not stop test!")
        else:
            return status

    def upload_record(self):
        """
        上传报告
        :return:  成功：cubex返回数据，失败：None
        """
        logger.debug("upload record.")
        msg_list = self.__get_msg_list(CubeServerType.UPLOAD_OR_DELETE_RECORD)
        msg_list['dealt_type'] = CubeUploadDelete.UPLOAD
        ret, status = self.__send_command(msg_list)
        if ret is None:
            raise CubeRuntimeError("Can not upload record. Please check your username or network!")
        else:
            return status

    def delete_record(self):
        """
        删除报告
        :return:  成功：cubex返回数据，失败：None
        """
        logger.debug("delete cube.")
        msg_list = self.__get_msg_list(CubeServerType.UPLOAD_OR_DELETE_RECORD)
        msg_list['dealt_type'] = CubeUploadDelete.DELETE
        ret, status = self.__send_command(msg_list)
        if ret is None:
            raise CubeRuntimeError("Can not delete record!")
        else:
            return status

    def _restart_cube_service(self):
        logger.debug("restart cube service..")
        for retry in range(0, 2):
            file = os.popen("adb shell am startservice " +
                            "com.tencent.cubex/com.tencent.cubex.service.CubeService")
            file.readline()
            result = 0
            while True:
                line = file.readline()
                logger.debug(line)
                if not line:
                    result = 1
                    break
                else:
                    if "Error" in line:
                        result = -1
            if result == 1:
                break
        return result

    def recover_data(self):
        """
        恢复数据
        :return:  成功恢复：cubex返回数据，失败：None
        """
        logger.debug("revocer cube data.")
        result = self._restart_cube_service()
        if result != 1:
            raise CubeServiceStartError("Cube服务无法启动，请检查是否正确安装Cube服务并使能相关权限。")
        for retry in range(0, 2):
            try:
                msg_list = self.__get_msg_list(CubeServerType.RECOVER_DATA)
                while True:
                    msg_list["seq"] = self.__get_seq()
                    ret = self.socket.send_message(msg_list)
                    if ret['reply_type'] == CubeReplyCode.EXECUTING:
                        time.sleep(1)
                    else:
                        break
                if ret['reply_type'] != CubeReplyCode.RESEND_CMD and ret['reply_type'] != CubeReplyCode.CONTINUE_CMD:
                    message = "Error code: " + str(ret['reply_type']) # + " msg: " + ret['error_msg']
                    logger.error(message)
                    self.session_id = ret['session_id']
                    self.seq = ret['seq'] - 1
                    raise CubeServiceError("Can not recover the data, please check your phone or restart the test to try!")
                elif ret['reply_type'] == CubeReplyCode.RESEND_CMD:
                    # 最近操作未完成，需重新操作
                    self.session_id = ret['session_id']
                    self.seq = ret['seq'] - 1
                    return False
                elif ret['reply_type'] == CubeReplyCode.CONTINUE_CMD:
                    # 最近操作已完成，进入下一步操作
                    self.session_id = ret['session_id']
                    self.seq = ret['seq']
                    return True
            except:
                stack = traceback.format_exc()
                logger.exception(stack)
                self._restart_cube_service()
        raise CubeRecoverError("Can not recover data! Please check your phone!")




