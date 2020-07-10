import json
from urllib import request
from html.parser import HTMLParser
import re
import time
import pygame


def listenQueue():
    # parse data from URL
    url = "https://emcservice.my.salesforce.com/500?fcf=00B3a000004YQRP&rolodexIndex=-1&page=1&isdtp=nv&nonce=9ba10f9fa8f29354d1e1a6831fa8d165a38c75ecf8dbfc439a8fab3b870d47de&sfdcIFrameOrigin=https%3A%2F%2Femcservice.my.salesforce.com"

    # set Headers
    myHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=31536002',
        'Connection': 'keep-alive',
        'Cookie': 'sid=00Dj0000000HyWJ!ARMAQMZOksgIiopFIN9xIZ9m_WgTUah2.cSnEJrSnKo2HLol_.0dwjRMtrSNgKZ.GTZTQVYWX6KhyErRVfzWKyJLIT4Xx3ke',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36}'}

    req = request.Request(url, headers=myHeaders,method="POST")
    response = request.urlopen(req)
    responseStr = response.read().decode()
    # print(responseStr)
    if not responseStr:
        print("cookie is old,please update Cookie")
        return -1

    #parse data with Re
    patt = "CASES\.PRIORITY\"\:\[(\"S[0-9]\",?)*"
    pattern = re.compile(patt)

    result = pattern.search(responseStr).group()
    res = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+ result
    print(res)
    currentS2count = result.count("S3")
    currentS1Count = result.count("S1")
    # print(currentS1Count, s1Counts)
    # print(currentS2count, s2Counts)
    if result.__contains__("S3") or result.__contains__("S1"):
        if currentS2count > 0 or currentS1Count > 0:
            print("case!!!")
            url = "https://slack.com/api/chat.postMessage"
            myHeaders = {
                "Content-type": "application/json",
                "Authorization": "Bearer xoxb-322570874211-878348890663-0YhrgSLknij4cAacN0WJxzRD"
            }
            mydata = {
                "channel": "GRULJEK1C",
                "text": res
            }
            req = request.Request(url, headers=myHeaders, method="POST")
            response = request.urlopen(req, data=bytes(json.dumps(mydata), encoding="utf-8"))
            responseStr = response.read().decode()
            print(responseStr)


while(1):
    listenQueue()
    time.sleep(600)