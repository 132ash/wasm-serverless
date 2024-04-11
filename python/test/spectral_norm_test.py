import requests

ip = 'http://192.168.35.132:7000/'

requestAddr = ip + "request"
createAddr = ip + 'create'
deleteAddr = ip + 'delete'
infoAddr = ip + 'info'
funcNames = ['spectral_norm']
triggerData = {'spectral_norm': {"funcName":"spectral_norm", "parameters":{"number":10}},
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

testCreateAllFunc(funcNames)
res = testRunAllFunc(funcNames)
print(res)