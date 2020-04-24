#-*- coding: UTF-8 -*-
__author__ = 'guoruihe'

from exceptions import RuntimeError


class CubeServiceError(RuntimeError):
    """
        CubeX服务异常
    """
    pass


class CubeConnectError(RuntimeError):
    """
        与CubeX建立连接出现错误时抛出
    """
    pass


class CubeRuntimeError(RuntimeError):
    """
        与CubeX进行场景标记时出现错误抛出
    """
    pass


class CubeRecoverError(RuntimeError):
    """
        恢复cubex数据时，出现错误
    """
    pass


class DeviceNotRootError(RuntimeError):
    """
    手机未ROOT
    """
    pass

class CubeServiceStartError(RuntimeError):
    """
    cube启动异常，需要人工检查介入
    """
    pass


class GetMonitorFileError(RuntimeError):
    """
    测试结束停止游戏时，无法获取到Monitor文件，则无法继续完成本次测试，需重新测试。
    """
    pass