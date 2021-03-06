#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from exceptions import RuntimeError

class WeTestRuntimeError(RuntimeError):
    """
        与引擎、平台设备交互过程中遇到不可忽略的错误时抛出
    """
    pass


class WeTestEnvironmentError(WeTestRuntimeError):
    """
        环境变量设置有问题
    """
    pass

class WeTestPlatormError(WeTestRuntimeError):
    """
        平台连接错误
    """
    pass

class NetError(WeTestRuntimeError):
    """
        网络相关错误，初始化失败、网络断开连接
    """
    pass

class WeTestInvaildArg(WeTestRuntimeError):
    """
        错误的输入接口
    """
    pass

class WeTestSDKError(WeTestRuntimeError):
    """
        SDK错误
    """
    pass

class WeTestSDKTimeOut(WeTestRuntimeError):
    """
        SDK超时错误
    """
    pass

class WeTestInvaildSdkVersion(WeTestRuntimeError):
    """
        当前wpyscripts不支持对应的SDK
    """

class SceneTagError(WeTestRuntimeError):
    """
        性能数据设置标签错误
    """

class LoginError(WeTestRuntimeError):
    """
        登陆出错，比如QQ或微信没有账号密码等
    """

class UIAutomatorError(WeTestRuntimeError):
    """
        调用UIAutomator时错误
    """

class UIAutomatorLoginError(WeTestRuntimeError):
    """
        登录时出错
    """