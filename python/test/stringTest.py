import requests

ip = "http://192.168.35.132:7000/"

requestAddr = ip + "request"
createAddr = ip + 'create'
funcName = "stringupperandcount"
funcName2 = "cal"
funcName3 = "simple_func"
triggerData =[{"funcName":"simple_func", "parameters":{"arg1":6, "arg2":3}}]
triggerData2 = [{"funcName":"cal", "parameters":{"arg1":6, "arg2":3}}]
triggerData3 = [{"funcName":"simple_func", "parameters":{"arg1":6, "arg2":3}}]


def testCreateAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(createAddr, json=req)
    print(res.text)

def testRunAllFunc(funcNames):
    for i, func in enumerate(funcNames):
        req = triggerData[i]
        res = requests.post(requestAddr, json=req)
        print(f"func {func} run result:{res.json()}")

funcNames = [funcName3]
testCreateAllFunc(funcNames)
testRunAllFunc(funcNames)