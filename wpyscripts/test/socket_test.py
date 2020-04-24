#-*- coding: UTF-8 -*-
__author__ = 'alexkan'

from wpyscripts.common import socket_client as client
from wpyscripts.common.protocol import *

socket = client.get_socket_client()


def send_cmd_test():
    ret = socket.send_command(Commands.GET_VERSION)
    print(ret)

send_cmd_test()
# send_cmd_test()
# send_cmd_test()
# send_cmd_test()
