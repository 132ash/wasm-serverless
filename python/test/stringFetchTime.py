import time
ip = 'http://192.168.35.132:7000/'

requestAddr = ip + "request"
createAddr = ip + 'create'
deleteAddr = ip + 'delete'
infoAddr = ip + 'info'
FILE_NAME = "pg-being_ernest.txt"
FILE_NAME_TEST = "test.txt"
funcNames = ['binarytree']
triggerData = {'cal': {"funcName":"cal", "parameters":{"arg1":1, 'arg2':2}},
               'cut':  {"funcName":"cut", "parameters":{"text_DB":FILE_NAME, 'sliceNum':3}},
               'merge':  {"funcName":"merge", "parameters":{"countRes":[{'hello':1, 'world':1}, {'the':1}, {'world':1}]}},
               'spectral_norm': {"funcName":"spectral_norm", "parameters":{"number":200}},
               'binarytree': {"funcName":"binarytree", "parameters":{"number":10}}
               }

# 'binarytree': {"funcName":"binarytree", "parameters":{"number":10}}

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
        start = time.time()
        res=  requests.post(requestAddr, json=req).json()
        end = time.time()
        return res, end - start
    
def getInfo(funcName):
    req = {"funcName":funcName}
    res = requests.post(infoAddr, json=req)
    print(res.json())

testDeleteAllFunc(funcNames)
testCreateAllFunc(funcNames)
res, time1 = testRunAllFunc(funcNames)
print(res)
print(time1)

# 8591.747946