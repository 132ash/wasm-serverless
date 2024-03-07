import requests

ip = "http://localhost:5000/"

requestAddr = ip + "request"
createAddr = ip + 'create'
triggerData = [{"funcName":"cal", "parameters":{"arg1":1, "arg2":2}},
 {"funcName":"divide2", "parameters":{"div":2.5}},
{"funcName":"reverse", "parameters":{"subres":-6}},
 {"funcName":"times2", "parameters":{"subres":-5}},
 {"funcName":"sum", "parameters":{"divres":0.75, "time2res":6, "subres":-4}}]


def testCreateAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(createAddr, json=req)
    print(res.text)

def testRunAllFunc(funcNames):
    for i, func in enumerate(funcNames):
        req = triggerData[i]
        res = requests.post(requestAddr, json=req)
        print(f"func {func} run result:{res.json()}")

funcNames = ["cal", "divide2", "reverse", "times2", "sum"]
testCreateAllFunc(funcNames)
testRunAllFunc(funcNames)