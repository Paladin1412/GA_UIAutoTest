#!usr/bin/python
# -*- coding=utf-8 -*-

import os
import urllib2
import urllib
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import zipfile



#上传文件到服务器，并返回生成的URL
def post_file_to_svr(file_path, url):
    tmp_url = ''
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
    except urllib2.URLError, e:
        print e.reason
        # print e.code
    f.close()
    return tmp_url


# 输入目录路径，输出最新文件完整路径
def find_new_file(dir_in):
    # 查找目录下最新的文件
    file_lists = os.listdir(dir_in)
    file_lists.sort(key=lambda fn: os.path.getmtime(dir_in + "//" + fn)
                    if not os.path.isdir(dir_in + "//" + fn) else 0)
    file_path = os.path.abspath(os.path.join(dir_in, file_lists[-1]))
    print('the newest file path：' + file_path)
    return file_path