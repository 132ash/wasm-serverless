import pandas as pd
import sys
import yaml
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
from repository import Repository
import requests

resdir = config.RESULT_DIR
FUNCYAMLPATH = config.FUNCYAMLPATH
proxyAddr = ':'.join([config.HOST_IP, config.WASM_PROXY_PORT])
FUNC_NAME = "string_fetch"
PARAMS = [{'size_DB':x} for x in ['1KB', '10KB', '100KB', '500KB', '1MB', '10MB', '100MB']]
testTime = 5


def flushFunction(funcName):
    req = {"funcNames": [funcName]}
    deleteAddr = '/'.join([proxyAddr, 'delete'])
    createAddr = '/'.join([proxyAddr, 'create'])
    # 200MB heap
    requests.post(deleteAddr, json=req)
    requests.post(createAddr, json=req)

def invokeFunction(funcName, param):
    req = {"funcName": funcName, "parameters":param}
    reqAddr = '/'.join([proxyAddr, 'request'])
    res = requests.post(reqAddr, json=req)
    return res.json()

def changeWorkerType(funcName, workerType):
    filename = '/'.join([FUNCYAMLPATH, f'{funcName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
    yamlData['containerType'] = workerType
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)

def testDataTransfer(testTime):
    wasmStartLatencies = {}
    dockerStartLatencies = {}
    print("---------------------DATA TRANSFER-----------------------------")
    print(f"test string sizes: {PARAMS}")
    print("TESTING WASM CONTAINER.")
    mode = 'wasm'
    changeWorkerType(FUNC_NAME, mode)
    # prewarm.
    flushFunction(FUNC_NAME)
    for param in PARAMS:
        for size in param.values():
            print(f"testing data size {size}.")
            wasmStartLatencies[size] = []
            for i in range(testTime):
                if (i+1) % max((testTime) // 10, 1) == 0:
                    print(f"Test Step:{(i+1)}/{testTime}")
                rawResult = invokeFunction(FUNC_NAME, param)
                postProxyTIme = rawResult['timeStamps'][-1]
                stringReadyTime = (rawResult['res']['startTime'] * 1e-6 - postProxyTIme)
                wasmStartLatencies[size].append(stringReadyTime*1000)
    print("TESTING DOCKER CONTAINER.")
    mode = 'docker'
    # prewarm.
    changeWorkerType(FUNC_NAME, mode)
    flushFunction(FUNC_NAME)
    for param in PARAMS:
        for size in param.values():
            print(f"testing data size {size}.")
            dockerStartLatencies[size] = []
            for i in range(testTime):
                if (i+1) % max((testTime) // 10, 1) == 0:
                    print(f"Test Step:{(i+1)}/{testTime}")
                rawResult = invokeFunction(FUNC_NAME, param)
                postProxyTIme = rawResult['timeStamps'][-1]
                readyTIme = rawResult['res']['readyTime'] - postProxyTIme
                dockerStartLatencies[size].append(readyTIme*1000)
        
    df1 = pd.DataFrame(wasmStartLatencies)
    df2 = pd.DataFrame(dockerStartLatencies)
    df1["Source"] = "wasm"
    df2["Source"] = "docker"
    df_combined = pd.concat([df1, df2], ignore_index=True)
    df_combined.to_csv('/'.join([resdir,'data_transfer_new(ms).csv']),  index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    # repo = Repository.makeAndStoreStrings()
    testDataTransfer(testTime)
