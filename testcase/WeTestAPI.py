#coding:utf-8
import hmac,time,random,base64
import hashlib
import requests
# import requests_toolbelt as rt
import urllib
class WeTestApi():
    def __init__(self, auth, host, expiretime = 0):
        self.__secretid = auth['secretid']
        self.__secretkey = auth['secretkey']
        self.__expiretime = expiretime
        self.__host = host
    def _get_signature_params(self, requesturi, querydata, method):
        timestamp = int(time.time())
        nonce = random.randint(0,9999)
        data = {
            "timestamp":str(timestamp),
            "nonce":str(nonce),
            "signaturemethod":"HmacSHA256",
            "expire":str(self.__expiretime),
            "secretid":str(self.__secretid)
        }
        finaldata = dict(data, **querydata)
        querypair = []
        for key in sorted(finaldata.keys()):
            querypair.append("%s=%s" %(str(key), str(finaldata[key])))
        querystr = "&".join(querypair)
        source_str = method + requesturi + "?" + querystr
        encode_str = hmac.new(self.__secretkey, source_str, hashlib.sha256).digest()
        signature = base64.b64encode(encode_str)
        finaldata["signature"] = signature
        return finaldata
    def _get_request_uri(self, route):
        return self.__host + route
    '''
    获取测试进度
    '''
    def get_test_status(self,testid):
        url = "/cloudapi/api_v4/private_test_status"
        params = {
            "testid":testid
        }
        params = self._get_signature_params(url, params, "GET")
        response = requests.get(self._get_request_uri(url), params)
        return response.json()
    '''
    获取测试信息
    '''
    def get_test_info(self, testid):
        url = "/cloudapi/api_v4/private_test_info"
        params = {
            "testid":testid
        }
        params = self._get_signature_params(url, params, "GET")
        response = requests.get(self._get_request_uri(url), params)
        return response.json()
    '''
    获取测试截图和日志
    '''
    def get_test_image_log(self,testid, needimage = 1, needlog = 1):
        url = "/cloudapi/api_v4/private_test_image_log"
        params = {}
        params['testid'] = testid
        params["needimage"] = needimage
        params["needlog"] = needlog
        params = self._get_signature_params(url, params, "GET")
        response = requests.get(self._get_request_uri(url), params=params)
        return response.json()
    '''
    获取单个设备的测试截图和日志
    '''
    def get_test_device_image_log(self, testid, deviceid, needimage = 1, needlog = 1):
        url = "/cloudapi/api_v4/private_test_device_image_log"
        params = {}
        params['testid'] = testid
        params["deviceid"] = deviceid
        params["needimage"] = needimage
        params["needlog"] = needlog
        params = self._get_signature_params(url, params, "GET")
        response = requests.get(self._get_request_uri(url), params=params)
        return response.json()
    '''
    获取测试错误日志和性能数据
    '''
    def get_test_perf_error(self, testid, needperf = 1, neederror= 1):
        url = "/cloudapi/api_v4/private_test_perf_error"
        params = {}
        params["testid"] = testid
        params["needperf"] = needperf
        params["neederror"] = neederror
        params = self._get_signature_params(url, params, "GET")
        response = requests.get(self._get_request_uri(url), params)
        return response.json()
    '''
    获取单个设备测试错误日志和性能数据
    '''
    def get_test_device_perf_error(self, testid, deviceid, needperf = 1, neederror= 1):
        url = "/cloudapi/api_v4/private_test_device_perf_error"
        params = {}
        params["testid"] = testid
        params["deviceid"] = deviceid
        params["needperf"] = needperf
        params["neederror"] = neederror
        params, headers = self._get_signature_params(url, params, "GET")
        response = requests.get(self._get_request_uri(url), params)
        return response.json()
    '''
    获取指定日期范围内的测试列表
    '''
    def get_test_list(self,startdate=False,enddate=False,projectid=0):
        url = "/cloudapi/api_v4/private_test_list"
        params = {}
        if startdate:
            params["startdate"] = startdate
        if enddate:
            params["enddate"] = enddate
        params['projectid'] = projectid
        params = self._get_signature_params(url, params, "GET")
        response = requests.get(self._get_request_uri(url), params)
        return response.json()
    # def _upload_resource(self, filepath, uptype):
    #     url = "/cloudapi/api_v4/fileupload"
    #     params = {
    #         "type":uptype
    #     }
    #     params = self._get_signature_params(url, params, "POST")
    #     url = self._get_request_uri(url)+ "?" + urllib.urlencode(params)
    #     m = rt.MultipartEncoder(
    #         fields =  {
    #             "file":(filepath,open(filepath,"rb").read())
    #         }
    #     )
    #     response = requests.post(url, data = m, headers = {"Content-Type":m.content_type})
    #     return response.json()
    '''
    上传APK
    '''
    def upload_apk(self, apkpath):
       return self._upload_resource(apkpath, "apk")
    '''
    上传script
    '''
    def upload_script(self, scriptpath):
        return self._upload_resource(scriptpath, "script")
    '''
    提交测试, testparams是提测参数。apk和script是测试apk路径和script路径。也可以直接传递apkid和scriptid参数
    '''
    def start_test(self, testparams):
        url = "/cloudapi/api_v4/private_user_autotest"
        if "apk" in testparams:
            testparams["apkid"] = self.upload_apk(testparams["apk"])['apkid']
        if "script" in testparams:
            testparams["scriptid"] = self.upload_script(testparams["script"])['scriptid']
        params = self._get_signature_params(url, {}, "POST")
        url = self._get_request_uri(url) + "?" + urllib.urlencode(params)
        response = requests.post(url, json = testparams)
        return response.json()
    '''
    下载，简单的封装
    '''
    def download_file(self, url, saveto):
        r = requests.get(url)
        with open(saveto,"wb") as f:
            f.write(r.content)
if __name__ == '__main__':
    authparams = {
        "secretid":"VW44hkA8Py8cW9mU",
        "secretkey":"TH2WlPtJS8abhX4S",
    }
    client = WeTestApi(authparams, "http://api.wetest.qq.com")
    print client.get_test_info(3287706)
    print client.get_test_device_image_log(3287706,32410)