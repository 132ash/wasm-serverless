import sys
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
from repository import Repository
import requests
import yaml

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


def timeTick():
    print("TESTING WASM CONTAINER.")
    for param in PARAMS:
        print(f"testing data {param}.")
        mode = 'wasm'
        changeWorkerType(FUNC_NAME, mode)
        print(f"-----------------------------{mode}-----------------------------------")
        flushFunction(FUNC_NAME)
        for size in param.values():
            rawResult = invokeFunction(FUNC_NAME, param)
            print(rawResult)
            wasmTimeStamp = rawResult['res']['wasmTimeStamp']
            postProxyTIme = rawResult['timeStamps'][-1]
            getParamTime = (wasmTimeStamp[0] * 1e-6 - postProxyTIme) * 1000
            paramReadyTime = (wasmTimeStamp[1] * 1e-6 - postProxyTIme) * 1000
            stringReadyTime = (rawResult['res']['startTime'] * 1e-6 - postProxyTIme) * 1000
            getStringTime = (wasmTimeStamp[3] * 1e-6) * 1000
            wrapStringTime = (wasmTimeStamp[2] * 1e-6) * 1000
            print(f"wrapper get param {getParamTime}\nwasm param ready {paramReadyTime}\nwasm string ready {stringReadyTime}\nget string latency {getStringTime}\nwrap string latency {wrapStringTime}")
        mode = 'docker'
        print(f"-----------------------------{mode}-----------------------------------")
        changeWorkerType(FUNC_NAME, mode)
        flushFunction(FUNC_NAME)
        for size in param.values():
            rawResult = invokeFunction(FUNC_NAME, param)
            # wasmTimeStamp = rawResult['res']['wasmTimeStamp']
            postProxyTIme = rawResult['timeStamps'][-1]
            inFuncTIme = (rawResult['res']['inFuncTIme'] - postProxyTIme)* 1000
            readyTIme = (rawResult['res']['readyTime'] - postProxyTIme)* 1000
            getStringTime = (readyTIme - inFuncTIme)
            print(f"in function {inFuncTIme}\ndocker string ready {readyTIme}\nget string latency {getStringTime}")
        # getParamTime = wasmTimeStamp[0] * 1e-6 - postProxyTIme
        # paramReadyTime = wasmTimeStamp[1] * 1e-6 - postProxyTIme
        # getStringTime = wasmTimeStamp[2] * 1e-6
        # print(f"get param {getParamTime}\nparam ready {paramReadyTime}\nget string {getStringTime}")
    #         timeStamps = rawResult['timeStamps'] 
    #             readyTime = timeStamps[1] * 1e3
    #             getStrTime = timeStamps[2] * 1e-3
    #             funcStartTime = rawResult['res']['startTime'] * 1e-3
    #             wasmStartLatencies[size].append(funcStartTime - readyTime)
    # print("TESTING DOCKER CONTAINER.")
    # mode = 'docker'
    # # prewarm.
    # flushFunction(FUNC_NAME, mode)
    # for param in PARAMS:
    #     for size in param.values():
    #         print(f"testing data size {size}.")
    #         dockerStartLatencies[size] = []
    #         for i in range(testTime):
    #             if (i+1) % max((testTime) // 10, 1) == 0:
    #                 print(f"Test Step:{(i+1)}/{testTime}")
    #             rawResult = invokeFunction(FUNC_NAME, param, mode)
    #             readyTime = rawResult['readyTime']
    #             funcStartTime = rawResult['res']['out']['startTime']
    #             dockerStartLatencies[size].append((funcStartTime - readyTime)*1000)
        


if __name__ == "__main__":
    timeTick()