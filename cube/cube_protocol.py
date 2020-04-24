# -*- coding: UTF-8 -*-
__author__ = 'guoruihe'


class CubeServerType(object):
    CONNECTION_BUILD = 1  # 建立连接
    BEGIN_TEST = 2  # 开始测试，拉起游戏
    SCENE_TAG = 4  # 场景标记
    STOP_TEST = 8  # 停止测试
    UPLOAD_OR_DELETE_RECORD = 16  # 上传或删除测试记录

    RECOVER_DATA = 101  # 恢复数据


class CubeUploadDelete(object):
    UPLOAD = 0  # 上传测试记录
    DELETE = 1  # 删除测试记录


class CubeTestLevel(object):
    LIGHT = 0
    SEVERE = 1
    RESOURCES = 2
    MONO_MEMORY = 3
    LIGHT_ROOT = 4
    UNITY_PROFILE = 5
    LIGHT_UNROOT = 6


class CubeSnapshots(object):
    CLOSE = 0
    OPEN = 1


class Before5and6(object):
    BEFORE = 1
    AFTER = 0


class CubeReplyCode(object):
    SUCCESS = 0
    ERROR = 1
    EXECUTING = 3
    RESEND_CMD = 4
    CONTINUE_CMD = 5


class CubeRunErrorCode(object):
        SUCCESS = 0
        CUBE_ERROR = -1
        CUBE_STARTED_ERROR = -2  # cube服务启动失败，无法进行测试，需手动检查服务启动问题
        CUBE_CONNECT_ERROR = -3  # cube通信连接建立失败，无法进行测试，需手动检查服务通信：1、 端口号；2、服务是否正确启动
        CUBE_STOP_APP_ERROR = -4  # 测试中，APP因某些原因崩溃，cube未获取到正确信息，无法完成测试。需要重测！
        CUBE_UPLOAD_ERRROR = -5  # cube上传数据错误（无数据、步骤错误等）。需重测！

        DOWNLOAD_SO_FAIL = 1
        APP_EXCEPTION_STOP = 2
        GET_MONITOR_FILE_ERROR = 3
        UPLOAD_FAILURE = 4
        MSG_FORMAT_ERROR = 5
        SESSION_CONFIG_EXCEPTION = 6
        DEVICE_NEED_ROOT = 7
        ILLEGAL_STATUS_TRANSITION = 8
        DELETE_DATA_ERROR = 9
        CONNECT_CONFIG_ERROR = 10
        MSG_SEQ_ILLEGAL = 11
        DATA_COMPRESS_FAILURE = 12
        NO_DATA_FILE = 13
        GAME_NOT_IN_FRONT = 14
        STOP_GAME_ERROR = 15
        GAME_INTENT_CREATE_ERROR = 16
        COPY_RESOURCE_FAILURE = 17
        RECORD_DATA_FAILURE = 18


class CubeStatus(object):
    """
    Cube服务的状态，用于状态转移判断，对于非法状态转移进行正确控制
    """
    UNKNOW = -1
    START_SERVICE = 0
    CONNECT = 1
    LANUCH_TEST = 2
    MARK = 3
    STOP_TEST = 4
    DELETE = 5
    UPLOAD = 6

