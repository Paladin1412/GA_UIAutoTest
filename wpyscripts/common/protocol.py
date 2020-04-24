# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu alexkan'


class Commands(object):
    GET_VERSION = 100  # 获取版本号
    FIND_ELEMENTS = 101  # 查找节点
    FIND_ELEMENT_PATH = 102  # 模糊查找
    GET_ELEMENTS_BOUND = 103  # 获取节点的位置信息
    GET_ELEMENT_WORLD_BOUND = 104  # 获取节点的世界坐标
    GET_UI_INTERACT_STATUS = 105  # 获取游戏的可点击信息，包括scene、可点击节点，及位置信息
    GET_CURRENT_SCENE = 106  # 获取Unity的Scene名称
    GET_ELEMENT_TEXT = 107  # 获取节点的文字内容
    GET_ELEMENT_IMAGE = 108  # 获取节点的图片名称
    GET_REGISTERED_HANDLERS = 109  # 获取注册的函数的名称
    CALL_REGISTER_HANDLER = 110  # 调用注册的函数
    SET_INPUT_TEXT = 111  # input控件更换文字信息
    GET_OBJECT_FIELD=112 # 通过反射获取gameobject中component的属性值

    #######################/
    HANDLE_TOUCH_EVENTS = 200  # 发送down move up

    DUMP_TREE = 300

class TouchEvent(object):
    ACTION_DOWN = 0
    ACTION_UP = 1
    ACTION_MOVE = 2

    def __init__(self, x, y, sleeptime, type):
        self.x = x
        self.y = y
        self.sleeptime = sleeptime
        self.type = type
