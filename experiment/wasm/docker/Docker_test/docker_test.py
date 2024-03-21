import requests

ip = "http://localhost:8000/"

requestAddr = ip + "request"
infoAddr = ip + "info"
triggerData = {"funcName":"compute", "parameters":{"arg1":1, "arg2":2}}


def testRun():
    res = requests.post(requestAddr, json=triggerData)
    print(res.text)

testRun()