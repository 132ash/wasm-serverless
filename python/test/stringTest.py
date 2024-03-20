import requests

ip = "http://192.168.35.132:7000/"

requestAddr = ip + "request"
createAddr = ip + 'create'
funcName = "stringupperandcount"
funcName2 = "cal"
triggerData = [{"funcName":funcName, "parameters":{"lowerstr":"HelloWorld", "counttimes":2}}]
triggerData2 = [{"funcName":"cal", "parameters":{"arg1":6, "arg2":3}}]


def testCreateAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(createAddr, json=req)
    print(res.text)

def testRunAllFunc(funcNames):
    for i, func in enumerate(funcNames):
        req = triggerData[i]
        res = requests.post(requestAddr, json=req)
        print(f"func {func} run result:{res.json()}")

funcNames = [funcName]
testCreateAllFunc(funcNames)
testRunAllFunc(funcNames)