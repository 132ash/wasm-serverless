import pandas as pd
import sys
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
import requests

resdir = config.RESULT_DIR
dockerProxyAddr = ':'.join([config.HOST_IP, config.DOCKER_PROXY_PORT])
wasmProxyAddr = ':'.join([config.HOST_IP, config.WASM_PROXY_PORT])
FUNC_NAME = "simple_func"
PARAM = {'arg1':1212, 'arg2':23132}

TEST_TIME = 1000

def flushFunction(funcName, containerType):
    req = {"funcNames": [funcName]}
    if containerType == 'wasm':
        deleteAddr = '/'.join([wasmProxyAddr, 'delete'])
        createAddr = '/'.join([wasmProxyAddr, 'create'])
        requests.post(deleteAddr, json=req)
        requests.post(createAddr, json=req)
    else:
        clearAddr = '/'.join([dockerProxyAddr, 'delete'])
        requests.post(clearAddr, json=req)

def invokeFunction(funcName, param, containerType):
    req = {"funcName": funcName, "parameters":param}
    if containerType == 'wasm':
        reqAddr = '/'.join([wasmProxyAddr, 'request'])
    else:
        reqAddr = '/'.join([dockerProxyAddr, 'request'])
    res = requests.post(reqAddr, json=req)
    return res.json()


    
def testColdStart():
    wasmStartLatencies = []
    dockerStartLatencies = []
    print("---------------------COLD START-----------------------------")
    print("TESTING WASM CONTAINER.")
    mode = 'wasm'
    for i in range(TEST_TIME):
        if (i+1) % max((TEST_TIME) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{TEST_TIME}")
        flushFunction(FUNC_NAME, mode)
        rawResult = invokeFunction(FUNC_NAME, PARAM, mode)
        invokeTime = rawResult['reqTime']   
        funcStartTime = rawResult['res']['startTime'] * 1e-6
        wasmStartLatencies.append(funcStartTime - invokeTime)
    print("TESTING DOCKER CONTAINER.")
    mode = 'docker'
    for i in range(TEST_TIME):
        if (i+1) % max((TEST_TIME) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{TEST_TIME}")
        flushFunction(FUNC_NAME, mode)
        rawResult = invokeFunction(FUNC_NAME, PARAM, mode)
        invokeTime = rawResult['reqTime']   
        funcStartTime = rawResult['res']['startTime']
        dockerStartLatencies.append(funcStartTime - invokeTime)
    df = pd.DataFrame({'wasm': wasmStartLatencies, 'docker': dockerStartLatencies})
    df.to_csv('/'.join([resdir,'coldstart.csv']))

if __name__ == "__main__":
    testColdStart()
