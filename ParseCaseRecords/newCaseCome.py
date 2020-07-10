from urllib import request
from html.parser import HTMLParser
import re
import time
import pygame
import logging


filepath = r"./乃木坂の詩.mp3"
s1Counts, s2Counts = 0, 0
def listenQueue():
    # parse data from URL
    url = "https://emcservice.my.salesforce.com/500?fcf=00B3a000004YQRP&rolodexIndex=-1&page=1&isdtp=nv&nonce=9ba10f9fa8f29354d1e1a6831fa8d165a38c75ecf8dbfc439a8fab3b870d47de&sfdcIFrameOrigin=https%3A%2F%2Femcservice.my.salesforce.com"

    # set Headers
    myHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=31536002',
        'Connection': 'keep-alive',
        'Cookie': 'sid=00Dj0000000HyWJ!ARMAQEGBRtSzY27XcESQxjDl1WDcFu6g4s7fh5VBMhEvlpNAXIfdc_vaDUEI.ck_bFry8iJdo2Dc5yWyyV60ka9LYktb4A74',
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
    (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), result)
    currentS2count = result.count("S2")
    currentS1Count = result.count("S1")
    # print(currentS1Count, s1Counts)
    # print(currentS2count, s2Counts)
    if result.__contains__("S2") or result.__contains__("S1"):
        if currentS2count > int(s2Counts) or currentS1Count > int(s1Counts):
            logging.log("case!!!")
            pygame.mixer.init()
            track = pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()


s2Counts = input("how many S2 cases in current queue:")
s1Counts = input("how many S1 cases in current queue:")


while(1):
    listenQueue()
    time.sleep(120)