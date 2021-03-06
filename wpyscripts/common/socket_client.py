#-*- coding: UTF-8 -*-
import os

__author__ = 'alexkan,minhuaxu'

import json, socket, struct, time
from wpyscripts.common.wetest_exceptions import *


class SocketClient(object):

    def __init__(self, _host='localhost', _port=27018):
        self.host = _host
        self.port = _port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((self.host, self.port))

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def _send_data(self, data):
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError) as e:
            raise WeTestInvaildArg('You can only send JSON-serializable data')
        length = len(serialized)
        buff = struct.pack("i", length)
        self.socket.send(buff)
        self.socket.sendall(serialized)


    def _recv_data(self):
        length_buffer = self.socket.recv(4)
        if length_buffer:
            total = struct.unpack_from("i", length_buffer)[0]
        else:
            raise WeTestSDKError('recv length is None?')
        view = memoryview(bytearray(total))
        next_offset = 0
        while total - next_offset > 0:
            recv_size = self.socket.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
        #print str(view.tobytes())
        try:
            deserialized = json.loads(view.tobytes())
        except (TypeError, ValueError) as e:
            raise WeTestInvaildArg('Data received was not in JSON format')
        if deserialized['status']!=0:
            message="Error code: "+str(deserialized['status'])+" msg: "+deserialized['data']
            raise WeTestSDKError(message)
        return deserialized['data']

    def send_command(self, cmd, params=None, timeout=100):
        # if params != None and not isinstance(params, dict):
        #     raise Exception('Params should be dict')
        if not params:
            params = ""
        command={}
        command["cmd"] = cmd
        command["value"] = params
        for retry in range(0,2):
            try:
                self.socket.settimeout(timeout)
                self._send_data(command)
                ret = self._recv_data()
                return ret
            except WeTestRuntimeError as e:
                raise e
            except socket.timeout:
                self.socket.close()
                self._connect()
                raise WeTestSDKError("Recv Data From SDK timeout")
            except socket.error as e:
                time.sleep(1)
                os.system("adb shell input keyevent 100 100")
                print("Retry...{0}".format(e.errno))
                self.socket.close()
                self._connect()
                continue
        raise Exception('Socket Error')

host = 'localhost'
port = 27018


def get_socket_client():
    if get_socket_client.instance:
        return get_socket_client.instance
    else:
        get_socket_client.instance = SocketClient(host, port)
        return get_socket_client.instance

get_socket_client.instance = None
