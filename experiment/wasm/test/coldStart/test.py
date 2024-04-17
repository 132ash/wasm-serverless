import pandas as pd
import sys
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
import yaml
import requests

resdir = config.RESULT_DIR
proxyAddr = ':'.join([config.HOST_IP, config.PROXY_PORT])
FUNC_NAME = "simple_func"
PARAM = {'arg1':1212, 'arg2':23132}

def changeWorkerType(funcName, workerType):
    filename = '/'.join([config.FUNCYAMLPATH, f'{funcName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
    yamlData['containerType'] = workerType
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)

def changeWasmMode(funcName, mode):
    filename = '/'.join([config.FUNCYAMLPATH, f'{funcName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
    yamlData['wasmMode'] = mode
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)

def flushFunction(funcName, containerType):
    req = {"funcNames": [funcName]}
    deleteAddr = '/'.join([proxyAddr, 'delete'])
    createAddr = '/'.join([proxyAddr, 'create'])
    requests.post(deleteAddr, json=req)
    requests.post(createAddr, json=req)

def invokeFunction(funcName, param, containerType):
    req = {"funcName": funcName, "parameters":param}
    reqAddr = '/'.join([proxyAddr, 'request'])
    res = requests.post(reqAddr, json=req)
    return res.json()


    
def testColdStart(testTime):
    wasmINTERPStartLatencies = []
    wasmJITStartLatencies = []
    dockerStartLatencies = []
    print("---------------------COLD START-----------------------------")
    print("TESTING WASM CONTAINER INTERP.")
    mode = 'wasm INTERP'
    changeWorkerType(FUNC_NAME, "wasm")
    changeWasmMode(FUNC_NAME, "INTERP")
    for i in range(testTime):
        if (i+1) % max((testTime) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{testTime}")
        flushFunction(FUNC_NAME, mode)
        rawResult = invokeFunction(FUNC_NAME, PARAM, mode)
        timeStamps = rawResult['timeStamps']
        invokeTime = timeStamps[0]   
        readyTime = timeStamps[1]
        wasmINTERPStartLatencies.append((readyTime - invokeTime)*1000)
    print("TESTING WASM CONTAINER JIT.")
    mode = 'wasm JIT'
    changeWasmMode(FUNC_NAME, "JIT")
    for i in range(testTime):
        if (i+1) % max((testTime) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{testTime}")
        flushFunction(FUNC_NAME, mode)
        rawResult = invokeFunction(FUNC_NAME, PARAM, mode)
        timeStamps = rawResult['timeStamps']
        invokeTime = timeStamps[0]   
        readyTime = timeStamps[1]
        wasmJITStartLatencies.append((readyTime - invokeTime)*1000)
    print("TESTING DOCKER CONTAINER.")
    mode = 'docker'
    changeWorkerType(FUNC_NAME, "docker")
    for i in range(testTime):
        if (i+1) % max((testTime) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{testTime}")
        flushFunction(FUNC_NAME, mode)
        rawResult = invokeFunction(FUNC_NAME, PARAM, mode)
        timeStamps = rawResult['timeStamps']
        invokeTime = timeStamps[0]   
        readyTime = timeStamps[1]
        dockerStartLatencies.append((readyTime - invokeTime)*1000)
    df = pd.DataFrame({'wasm interpreter': wasmINTERPStartLatencies,'wasm jit':wasmJITStartLatencies, 'docker': dockerStartLatencies})
    df.to_csv('/'.join([resdir,'coldstart(ms).csv']),  index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    testColdStart(testTime)
