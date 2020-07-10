from urllib import request
from html.parser import HTMLParser
import datetime
from openpyxl import load_workbook
import json

MONTH_LIST = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

class MyHTMLParser(HTMLParser):
    trFlag = False
    spanFlag = False
    datas = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            for att in attrs:
                if att == ("class", "breakRowClass0 breakRowClass0Top"):
                    self.trFlag = True
        if tag == 'span':
            self.spanFlag = True

    def handle_endtag(self, tag):
        if tag == "tr":
            self.trFlag = False
        if tag == 'span':
            self.spanFlag = False

    def handle_data(self, data):
        if self.trFlag and self.spanFlag:
            self.datas.append(data)


# parse data from URL
url = "https://emcservice.my.salesforce.com/00O3a000005B0oo?cancelURL=%2F00O3a000005B0oo&retURL=%2F00O3a000005B0oo&isdtp=vw&sfdcIFrameOrigin=https%3A%2F%2Femcservice.my.salesforce.com%22&isWsVw=true&nonce=6d43313f749341440d61b4f61b94ed76f2e8c05d09ae72a0d0f217d8616b2e13"

# set Headers
myheaders = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'sid=00Dj0000000HyWJ!ARMAQPn0FE3H.Ie2uoyJ0FEHS9vkXH63DsvW0jhuep31e_EHbAHeFeaEQHk49bfu5VVVVi.L5G_uas_H3a19Nz9aRgJXj1UC',
    'Host': 'emcservice.my.salesforce.com',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36}'}

req = request.Request(url, headers=myheaders)
response = request.urlopen(req)

parser = MyHTMLParser()
parser.feed(response.read().decode())

# parse data and store deta in Dict
myDict = {}
n = len(parser.datas)
for i in range(0, n, 2):
    numStr = ([x for x in parser.datas[i + 1] if x.isdigit()])
    num = int("".join(numStr))

    myDict[parser.datas[i]] = num

print(myDict)
if not myDict:
    print("Cookie is old, please refresh the cookie")
# check with Excel
today = datetime.date.today()
month = today.month
day = today.day

filePath = "./shift.xlsx"
morningQueue = dict()
lateQueue = dict()

xls_read = load_workbook(filePath)
monthStr = MONTH_LIST[month - 1]
sheet = xls_read.__getitem__(monthStr)

targetColumn = 2 + day
rowNum = 0

for row in sheet.rows:
    columnNum = 0
    tmpName = ""

    for cell in row:
        if columnNum == 2:
            # update name
            if cell.value == "Owen Zhang":
                cell.value = "Owen, Zhang"
            tmpName = cell.value
        if columnNum == targetColumn:
            if cell.value == "M":
                morningQueue[tmpName] = 0
            if cell.value == "L":
                lateQueue[tmpName] = 0
        columnNum += 1
        # last line
    if rowNum == 19:
        break
    rowNum += 1

#add parsed data into dict
## update in 2019/11/25
## the return fomrat in myDict from SalesForce always change, so split the Name, just judge by the firstName
## if the firstName contains, we think it's the same user.

for queueKey in morningQueue.keys():
    firstName = queueKey.split(",")[0]
    for key in myDict.keys():
        if key.__contains__(firstName):
            morningQueue[queueKey] = myDict[key]
        else:
            pass

for queueKey in lateQueue.keys():
    firstName = queueKey.split(",")[0]
    for key in myDict.keys():
        if key.__contains__(firstName):
            lateQueue[queueKey] = myDict[key]
        else:
            pass


def sort_dict(dict):
    keys = dict.keys()
    values = dict.values()

    list1 = [(key, val) for key, val in zip(keys, values)]
    list_sorted = sorted(list1, key=lambda x: x[1], reverse=False)

    return list_sorted

resultStr = ""
resultStr += str(today) + "\n"
# print(today)
print(morningQueue)
import re
for value in sort_dict(morningQueue):
    valueString = str(value)
    # print("M:", valueString[0], valueString.split('\'')[1], ",", valueString.split(',')[1], "\n")
    resultStr += "M:" + valueString[0] + valueString.split('\'')[1] + "," + valueString.split(',')[2] + "\n"

# print(sort_dict(morningQueue))
for value in sort_dict(lateQueue):
    valueString = str(value)
    # print("M:", valueString[0], valueString.split('\'')[1], ",", valueString.split(',')[1], "\n")
    resultStr += "M:" + valueString[0] + valueString.split('\'')[1] + "," + valueString.split(',')[2] + "\n"

# print(sort_dict(lateQueue))

# resultStr += "\""
print(resultStr)

import pymsteams
myTeamsMessage = pymsteams.connectorcard("https://outlook.office.com/webhook/51d4b15a-257f-4cea-a185-eb104f507789@945c199a-83a2-4e80-9f8c-5a91be5752dd/IncomingWebhook/a5e632ea5cb5461eb21a45dc52fb3d17/9822a7b5-811b-43ac-9d57-663c320acd99")
myTeamsMessage.text(resultStr)
myTeamsMessage.send()


