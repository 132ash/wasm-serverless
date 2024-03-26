import requests

ip = 'http://127.0.0.1:7000/'

requestAddr = ip + "request"
createAddr = ip + 'create'
infoAddr = ip + 'info'
# triggerData = [{"funcName":"cal", "parameters":{"arg1":1, "arg2":2}}]

triggerData = [{"funcName":"wasm_sleep", "parameters":{"sleepTime":1}}]


def testCreateAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(createAddr, json=req)
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

getInfo("wasm_sleep")