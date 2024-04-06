import requests

ip = 'http://127.0.0.1:7000/'

requestAddr = ip + "request"
createAddr = ip + 'create'
deleteAddr = ip + 'delete'
infoAddr = ip + 'info'
FILE_NAME = "pg-being_ernest.txt"
FILE_NAME_TEST = "test.txt"
funcNames = ['cal']
triggerData = {'cal': {"funcName":"cal", "parameters":{"arg1":1, 'arg2':2}},
               'cut':  {"funcName":"cut", "parameters":{"text_DB":FILE_NAME, 'sliceNum':3}},
               'merge':  {"funcName":"merge", "parameters":{"countRes":[{'hello':1, 'world':1}, {'the':1}, {'world':1}]}}
               }

def testCreateAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(createAddr, json=req)
    print(res.text)

def testDeleteAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(deleteAddr, json=req)
    print(res.text)


def testRunAllFunc(funcNames):
    for func in funcNames:
        req = triggerData[func]
        return requests.post(requestAddr, json=req).json()
    
def getInfo(funcName):
    req = {"funcName":funcName}
    res = requests.post(infoAddr, json=req)
    print(res.json())

testCreateAllFunc(['merge'])
res = testRunAllFunc(['merge'])
print(res)