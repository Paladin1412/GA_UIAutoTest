#-*- coding: UTF-8 -*-
import os

from wpyscripts.tools.baisc_operater import engine, device

__author__ = 'alexkan,minhuaxu,guoruihe'

import json, socket, time
import logging
from wpyscripts.common.wetest_exceptions import *

logger = logging.getLogger("wetest")


class SocketClient(object):

    def __init__(self, _host='localhost', _port=53003):
        self.host = _host
        self.port = _port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((self.host, self.port))

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def _send_cube_data(self, data):
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError) as e:
            raise WeTestInvaildArg('You can only send JSON-serializable data')
        logger.debug ('[_send_cube_data]: ' + serialized)
        self.socket.sendall(serialized)
        self.socket.send("\n")

    def _recv_cube_data(self):
        total = 4096
        view = memoryview(bytearray(total))

        recv_size = self.socket.recv_into(view, total)

        logger.debug( '[_recv_cube_data]: ' + str(view.tobytes()))
        try:
            deserialized = json.loads(view[0:recv_size-1].tobytes())
        except (TypeError, ValueError) as e:
            raise WeTestInvaildArg('Data received was not in JSON format')
        return deserialized

    def send_message(self, msg_list, timeout=20):
        """

        :param msg_list: 参数列表，dict类型
        :param timeout:  连接超时
        :return:  返回cubex的应答数据，dict类型
        """
        for retry in range(0, 2):
            try:
                self.socket.settimeout(timeout)
                self._send_cube_data(msg_list)
                ret = self._recv_cube_data()
                return ret
            except WeTestRuntimeError as e:
                raise e
            except socket.timeout:
                self.socket.close()
                self._connect()
                raise WeTestSDKError("Recv Data From SDK timeout")
            except socket.error as e:
                time.sleep(1)
                logger.error("Retry...{0}".format(e.errno))
                # Retry 的时候点击屏幕:
                # device.excute_adb("shell input tap 20 20")
                self.socket.close()
                self._connect()
                continue
        raise Exception('Socket Error')

host = 'localhost'
port = 59999


def get_socket_client():
    if get_socket_client.instance:
        return get_socket_client.instance
    else:
        get_socket_client.instance = SocketClient(host, port)
        return get_socket_client.instance

get_socket_client.instance = None
