import json
import requests

ip = "http://localhost:5000/"

requestAddr = ip + "request"
deleteAddr = ip + 'delete'
createAddr = ip + 'create'
infoAddr = ip + 'info'
workflowrequestAddr = ip + "workflow/run"
workflowdeleteAddr = ip + 'workflow/delete'
workflowcreateAddr = ip + 'workflow/create'

createReq = {"funcName":["sub"]}
triggerReq = {"funcName":"cal", "parameters":{"arg1":1, "arg2":2}}
deleteReq = {"funcName": "sum"}

def testCreate(funcName):
    req = {"funcNames":[funcName]}
    res = requests.post(createAddr, json=req)
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

def testWorkflowCreate():
    req = {"workflowName":"workflow"}
    testCreate("sub")
    testCreate("reverse")
    testCreate("times2")
    res = requests.post(workflowcreateAddr, json=req)
    print(res.text)

def testWorkflowTrigger():
    req = {"workflowName":"workflow", "parameters": {"sub1":1, "sub2":2}}
    res = requests.post(workflowrequestAddr, json=req)
    print(res.text)

def testWasmFunc():
    funcName = "times2"
    createReq = {"funcName":funcName}
    param1 = {"arg1":1}
    param2 = {"arg1":5}
    param3 = {"arg1":2}
    runReq1 = {"funcName":funcName, "parameters":param1}
    runReq2 = {"funcName":funcName, "parameters":param2}
    runReq3 = {"funcName":funcName, "parameters":param3}
    res = requests.post(createAddr, json=createReq) 
    print("create {} res:{}".format(funcName, res.text))
    res = requests.post(requestAddr, json=runReq1) 
    print("run {} res:{}".format(funcName, res.text))
    res = requests.post(requestAddr, json=runReq2) 
    print("run {} res:{}".format(funcName, res.text))
    res = requests.post(requestAddr, json=runReq3) 
    print("run {} res:{}".format(funcName, res.text))


testCreate("cal")
testTrigger()