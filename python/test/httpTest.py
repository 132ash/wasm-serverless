import json
import requests

ip = "http://localhost:5000/"

requestAddr = ip + "request"
deleteAddr = ip + 'delete'
createAddr = ip + 'create'
infoAddr = ip + 'info'

createReq = {"funcName":"sum", "wasmCodePath":".//wasmFunctions//sum.wasm", 'maxWorkers':10, 'expireTime':2}
triggerReq = {"funcName":"sum", "parameters":[1,2]}
deleteReq = {"funcName": "sum"}

def testCreate():
    res = requests.post(createAddr, json=createReq)
    print(res.text)

def testInfo():
    res = requests.get(infoAddr)
    print(res.json())

def testTrigger():
    res = requests.post(requestAddr, json=triggerReq)
    print(res.json())

def testDelete():
    res = requests.post(deleteAddr, json=deleteReq)
    print(res.json())


testCreate()
testInfo()
testTrigger()
testInfo()
testDelete()
testInfo()
testTrigger()