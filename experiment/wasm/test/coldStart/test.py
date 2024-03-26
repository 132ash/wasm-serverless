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


    
def testColdStart(testTime):
    wasmStartLatencies = []
    dockerStartLatencies = []
    print("---------------------COLD START-----------------------------")
    print("TESTING WASM CONTAINER.")
    mode = 'wasm'
    for i in range(testTime):
        if (i+1) % max((testTime) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{testTime}")
        flushFunction(FUNC_NAME, mode)
        rawResult = invokeFunction(FUNC_NAME, PARAM, mode)
        invokeTime = rawResult['reqTime']   
        readyTime = rawResult['readyTime']
        wasmStartLatencies.append((readyTime - invokeTime)*1000)
    print("TESTING DOCKER CONTAINER.")
    mode = 'docker'
    for i in range(testTime):
        if (i+1) % max((testTime) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{testTime}")
        flushFunction(FUNC_NAME, mode)
        rawResult = invokeFunction(FUNC_NAME, PARAM, mode)
        invokeTime = rawResult['reqTime']   
        readyTime = rawResult['readyTime']
        dockerStartLatencies.append((readyTime - invokeTime)*1000)
    df = pd.DataFrame({'wasm': wasmStartLatencies, 'docker': dockerStartLatencies})
    df.to_csv('/'.join([resdir,'coldstart(ms).csv']),  index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    testColdStart(testTime)
