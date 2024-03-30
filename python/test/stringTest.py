import requests

ip = "http://192.168.35.132:7000/"

requestAddr = ip + "request"
createAddr = ip + 'create'
deleteAddr = ip + 'delete'
funcName = "string_fetch"
funcName2 = "cal"
funcName3 = "simple_func"
funcName4 = "wasm_sleep"
triggerData =[{"funcName":"string_fetch", "parameters":{"size_DB":"100MB"}},
              {"funcName":"cal", "parameters":{"arg1":6, "arg2":3}},
              {"funcName":"simple_func", "parameters":{"arg1":6, "arg2":3}},
              {"funcName":"wasm_sleep", "parameters":{"sleepTime":1}}]


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
        req = triggerData[-1]
        res = requests.post(requestAddr, json=req)
        print(f"func {func} run result:{res.json()}")

funcNames = [funcName4]
testCreateAllFunc(funcNames)
testRunAllFunc(funcNames)
testRunAllFunc(funcNames)
testDeleteAllFunc(funcNames)
# testRunAllFunc(funcNames)