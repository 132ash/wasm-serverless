import requests

# docker run -p 6000:5000 --name spectral_norm -l dockerContainer -d spectral_norm

# docker remove --force 87776b4880d546be6fa4b896e659eaea2399facd63a4d92cd0308f417c0db4c9

# docker rm $(docker ps -aq) --force

ip = "http://0.0.0.0:6000/"

initAddr = ip + "init"
statusAddr = ip + "status"
runAddr = ip + "run"


def testInit(funcName):
    req = {"function":funcName}
    res = requests.post(initAddr, json=req)
    print(res.text)

def testStatus():
    res = requests.get(statusAddr)
    print(res)


def testInvoke(param):
    res = requests.post(runAddr, json=param)
    print(res.text)



funcName = 'spectral_norm'
param = {'number':50}


testInit(funcName)
testStatus()
testInvoke(param)