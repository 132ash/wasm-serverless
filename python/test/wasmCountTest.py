import requests
import time

ip = 'http://192.168.35.132:7000/'

requestAddr = ip + "request"
createAddr = ip + 'create'
deleteAddr = ip + 'delete'
infoAddr = ip + 'info'
FILE_NAME = "pg-being_ernest.txt"
FILE_NAME_TEST = "test.txt"
slice = ""
with open(f"/home/ash/wasm/wasm-serverless/python/setupScripts/text/{FILE_NAME}", 'r') as f:
    slice = f.read()

param = {'slice':slice[:int(len(slice)/10)]}
# param = {"text_DB":FILE_NAME}
funcNames = ['wordcount']
triggerData = [{"funcName":"wordcount", "parameters":param}]

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

def testRunAllFunc(funcNames, mode, i):
    for i, func in enumerate(funcNames):
        req = triggerData[i]
        startTime = time.time()
        res = requests.post(requestAddr, json=req).json()
        endTime = time.time()
        with open(f"countRes_{mode}_{i}.txt", 'w') as f:
            f.write(res['res']['countRes'])
        print(f'e2e latency:{endTime-startTime}')

def getInfo(funcName):
    req = {"funcName":funcName}
    res = requests.post(infoAddr, json=req)
    print(res.json())
mode = 'docker'
print(len(slice))
testCreateAllFunc(funcNames)
testRunAllFunc(funcNames, mode ,1)
testRunAllFunc(funcNames, mode ,2)
testRunAllFunc(funcNames, mode ,3)
testDeleteAllFunc(funcNames)