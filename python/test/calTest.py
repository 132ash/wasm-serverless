import requests

ip = 'http://127.0.0.1:7000/'

requestAddr = ip + "request"
createAddr = ip + 'create'
deleteAddr = ip + 'delete'
infoAddr = ip + 'info'
funcNames = ['cal']
triggerData = [{"funcName":"cal", "parameters":{"arg1":1, 'arg2':2}}]

def testCreateAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(createAddr, json=req)
    print(res.text)

def testDeleteAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(deleteAddr, json=req)
    print(res.text)


def testRunAllFunc(funcNames):
    for i, func in enumerate(funcNames):
        req = triggerData[i]
        res = requests.post(requestAddr, json=req)
        print(f"func {func} run result:{res.json()}")

def getInfo(funcName):
    req = {"funcName":funcName}
    res = requests.post(infoAddr, json=req)
    print(res.json())

testCreateAllFunc(funcNames)
testRunAllFunc(funcNames)
testDeleteAllFunc(funcNames)