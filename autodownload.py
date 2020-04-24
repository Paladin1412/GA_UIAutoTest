import ast
import json
import os

import time
g_params = {
    "jobId": "",
    "buildId": "",
    "shell": "",
    "before": "",
    "type": ""
}

accessKey = "aL9eVe3j"
secretKey = "So3rfM2Rl3W7VWfJ"


def getJobs():
    cmd = "sodaDemo --accessKey=" + accessKey + " --secretKey=" + secretKey + " --jobId=" + str(g_params['jobId']) + " --func=getJobs"
    # print cmd
    result = os.popen(cmd)
    result = result.read()
    # print result
    result = ast.literal_eval(result)
    result = result[0]
    print result
    return result['status'], result['buildId']


def params_init():
    with open("download.json", 'r') as soda_file:
        params = json.load(soda_file)
        global g_params
        g_params = params
        # g_params['jobId'] = params['jobId']
        # g_params['buildId'] = params['buildId']
        # g_params['shell'] = params['shell']
        # g_params['before'] = params['before']


def params_update():
    with open("download.json", 'w') as soda_file:
        global g_params
        json.dump(g_params, soda_file)


def download_artiface(buildId):
    cmd = "sodaDemo --accessKey=" + accessKey + " --secretKey=" + secretKey + " --jobId=" + str(g_params['jobId']) + " --buildId=" + buildId + " --func=downloadArtifact" + " --downloadFolder=temp"
    os.system("mkdir temp")
    result = os.popen(cmd)
    print result.read()


def download_apk(buildId):
    cmd = "sodaDemo --accessKey=" + accessKey + " --secretKey=" + secretKey + " --jobId=" + str(
        g_params['jobId']) + " --buildId=" + str(buildId) + " --func=downloadApk" + " --shell=" + g_params[
        'shell'] + " --downloadFolder=" + str(g_params['jobId']) + "-" + str(buildId)
    # print cmd
    print "strart download"
    os.popen(cmd).read()
    print "download finish"


def download_ipa(buildId):
    cmd = "sodaDemo --accessKey=" + accessKey + " --secretKey=" + secretKey + " --jobId=" + str(
        g_params['jobId']) + " --buildId=" + str(buildId) + " --func=downloadIpa" + " --downloadFolder=" + str(g_params['jobId']) + "-" + str(g_params['buildId'])
    print "start download"
    os.system(cmd)
    print "download finish"


def main():
    params_init()

    if g_params['type'] == "ipa":
        download_ipa(g_params['buildId'])

    else:
        if g_params['before'] == "y":
            download_apk(g_params['buildId'])
        else:
            status, buildId = getJobs()
            if buildId == g_params['buildId']:
                print 'no new'
            else:
                if status == 3:
                    download_apk(buildId)
                    g_params['buildId'] = buildId
                    params_update()


if __name__ == '__main__':
    main()
    # getJobs()
