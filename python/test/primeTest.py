import requests
import time
import json

ip = 'http://192.168.35.132:7000/'

requestAddr = ip + "request"
createAddr = ip + 'create'
deleteAddr = ip + 'delete'
infoAddr = ip + 'info'
param = {'maxNum':1000000}

# param = {"text_DB":FILE_NAME}
funcNames = ['prime']
triggerData = [{"funcName":"prime", "parameters":param}]

# funcNames = ['cal']
# triggerData = [{"funcName":"cal", "parameters":{"arg1":1, 'arg2':2}}]

def testDeleteAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(deleteAddr, json=req)
    print(res.text)


def testCreateAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(createAddr, json=req)
    print(res.text)

def testRunAllFunc(funcNames):
    for i, func in enumerate(funcNames):
        req = triggerData[i]
        startTime = time.time()
        res = requests.post(requestAddr, json=req).json()
        endTime = time.time()
        print(res['res']['count'])
        print(f'e2e latency:{endTime-startTime}')

def getInfo(funcName):
    req = {"funcName":funcName}
    res = requests.post(infoAddr, json=req)
    print(res.json())


testCreateAllFunc(funcNames)
testRunAllFunc(funcNames)
testRunAllFunc(funcNames)
testRunAllFunc(funcNames)
testDeleteAllFunc(funcNames)