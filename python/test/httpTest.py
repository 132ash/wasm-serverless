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

createReq = {"funcName":"sub"}
triggerReq = {"funcName":"sub", "parameters":{"sub1":1, "sub2":2}}
deleteReq = {"funcName": "sum"}

def testCreate(funcName):
    req = {"funcName":funcName}
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
    req = {"workflowName":"workflow", "parameters": {"sub1":3, "sub2":1}}
    res = requests.post(workflowrequestAddr, json=req)
    print(res.text)




testWorkflowCreate()
testWorkflowTrigger()