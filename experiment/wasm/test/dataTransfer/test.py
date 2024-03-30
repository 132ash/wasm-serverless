import pandas as pd
import sys
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
from repository import Repository
import requests

resdir = config.RESULT_DIR
dockerProxyAddr = ':'.join([config.HOST_IP, config.DOCKER_PROXY_PORT])
wasmProxyAddr = ':'.join([config.HOST_IP, config.WASM_PROXY_PORT])
FUNC_NAME = "string_fetch"
PARAMS = [{'size_DB':x} for x in ['1KB', '10KB', '100KB', '500KB', '1MB', '10MB', '100MB']]
testTime = 5


def flushFunction(funcName, containerType):
    req = {"funcNames": [funcName]}
    if containerType == 'wasm':
        deleteAddr = '/'.join([wasmProxyAddr, 'delete'])
        createAddr = '/'.join([wasmProxyAddr, 'create'])
        # 200MB heap
        req.update({"heapSize":104857600*2})
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


def testDataTransfer(testTime):
    wasmStartLatencies = {}
    dockerStartLatencies = {}
    print("---------------------DATA TRANSFER-----------------------------")
    print(f"test string sizes: {PARAMS}")
    print("TESTING WASM CONTAINER.")
    mode = 'wasm'
    # prewarm.
    flushFunction(FUNC_NAME, mode)
    for param in PARAMS:
        for size in param.values():
            print(f"testing data size {size}.")
            wasmStartLatencies[size] = []
            for i in range(testTime):
                if (i+1) % max((testTime) // 10, 1) == 0:
                    print(f"Test Step:{(i+1)}/{testTime}")
                rawResult = invokeFunction(FUNC_NAME, param, mode)
                timeStamps = rawResult['timeStamps'] 
                readyTime = timeStamps[1] * 1e3
                getStrTime = timeStamps[2] * 1e-3
                funcStartTime = rawResult['res']['startTime'] * 1e-3
                wasmStartLatencies[size].append(funcStartTime - readyTime)
    print("TESTING DOCKER CONTAINER.")
    mode = 'docker'
    # prewarm.
    flushFunction(FUNC_NAME, mode)
    for param in PARAMS:
        for size in param.values():
            print(f"testing data size {size}.")
            dockerStartLatencies[size] = []
            for i in range(testTime):
                if (i+1) % max((testTime) // 10, 1) == 0:
                    print(f"Test Step:{(i+1)}/{testTime}")
                rawResult = invokeFunction(FUNC_NAME, param, mode)
                readyTime = rawResult['readyTime']
                funcStartTime = rawResult['res']['out']['startTime']
                dockerStartLatencies[size].append((funcStartTime - readyTime)*1000)
        
    df1 = pd.DataFrame(wasmStartLatencies)
    df2 = pd.DataFrame(dockerStartLatencies)
    df1["Source"] = "wasm"
    df2["Source"] = "docker"
    df_combined = pd.concat([df1, df2], ignore_index=True)
    df_combined.to_csv('/'.join([resdir,'data_transfer(ms).csv']),  index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    # repo = Repository.makeAndStoreStrings()
    testDataTransfer(testTime)
