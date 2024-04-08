import pandas as pd
import sys
import yaml
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
import requests

ip = 'http://192.168.35.132:7000/'
resdir = config.RESULT_DIR
FUNCFLOWYAMLPATH = config.FUNCFLOWYAMLPATH

requestAddr = ip + "request"
createAddr = ip + 'create'
deleteAddr = ip + 'delete'
infoAddr = ip + 'info'
funcNames = ['spectral_norm', 'binarytree']
triggerData = {
               'spectral_norm': {"funcName":"spectral_norm", "parameters":{"number":200}},
               'binarytree': {"funcName":"binarytree", "parameters":{"number":10}}
               }
paramList = {
               'spectral_norm':[10 * i for i in range(1,21)],
               'binarytree': [i for i in range(1,11)]
            }

def CreateAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(createAddr, json=req)
    print(res.text)

def DeleteAllFunc(funcNames):
    req = {"funcNames":funcNames}
    res = requests.post(deleteAddr, json=req)
    print(res.text)

def RunFunc(funcName, number):
    data = triggerData[funcName]
    data["parameters"]['number'] = number
    res=  requests.post(requestAddr, json=data).json()
    return res

def flushAndPreWarm(funcName):
    funcNames=  [funcName]
    DeleteAllFunc(funcNames)
    CreateAllFunc(funcNames)
    RunFunc(funcName, 1)

def changeWorkerType(funcName, workerType):
    filename = '/'.join([FUNCFLOWYAMLPATH, f'{funcName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
    yamlData['containerType'] = workerType
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)

def getRunTime(data, mode):
    if mode == 'docker':
        dataLis = data['result'].split()
        return float(dataLis[1])
    else:
        return data['runtime']

    
def testCompute(testTime):
    ComputeLatencies = {func:{mode:[]for mode in ['wasm', 'docker'] } for func in funcNames}
    print("---------------------COMPLEX COMPUTE-----------------------------")
    print("TESTING WASM CONTAINER.")
    mode = 'wasm'
    for func in funcNames:
        changeWorkerType(func, mode)
        flushAndPreWarm(func)
        for param in paramList[func]:
            totalLatency = 0
            for i in range(testTime):
                if (i+1) % max((testTime) // 10, 1) == 0:
                    print(f"{mode} {func} with param {param} Test Step:{(i+1)}/{testTime}")
                rawResult = RunFunc(func, param)['res']
                runtime = getRunTime(rawResult, mode)
                totalLatency += runtime
            ComputeLatencies[func][mode].append(totalLatency/testTime)
    print("TESTING DOCKER CONTAINER.")
    mode = 'docker'
    for func in funcNames:
        changeWorkerType(func, mode)
        flushAndPreWarm(func)
        for param in paramList[func]:
            totalLatency = 0
            for i in range(testTime):
                if (i+1) % max((testTime) // 10, 1) == 0:
                    print(f"{mode} {func} with param {param} Test Step:{(i+1)}/{testTime}")
                rawResult = RunFunc(func, param)['res']
                runtime = getRunTime(rawResult, mode)
                totalLatency += runtime
            ComputeLatencies[func][mode].append(totalLatency/testTime)
    print(ComputeLatencies)
    for func, platforms in ComputeLatencies.items():
        df = pd.DataFrame({
            'Input': paramList[func],
            'WASM': platforms['wasm'],
            'Docker': platforms['docker']
        })
        df.to_csv('/'.join([resdir,"complexCompute",f'{func}_performance.csv']), index=False)
# 画图
    # df = pd.DataFrame({'wasm': wasmStartLatencies, 'docker': dockerStartLatencies})
    # df.to_csv('/'.join([resdir,'coldstart(ms).csv']),  index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    testCompute(testTime)
