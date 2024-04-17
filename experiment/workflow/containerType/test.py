import pandas as pd
import sys
import uuid
import yaml
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")

import config
import requests
yamlDirPath = config.WORKFLOWYAMLPATH
resdir = config.RESULT_DIR
gatewayAddr = ':'.join([config.HOST_IP, config.GATEWAY_PORT])
workflowCreateAddr = '/'.join([gatewayAddr, "workflow/create"])
workflowDeleteAddr = '/'.join([gatewayAddr, "workflow/delete"])
workflowRunAddr = '/'.join([gatewayAddr, "workflow/run"])
FORKFLOW_LIST = ["workflow"]
FILE_NAME = "pg-being_ernest.txt"
FILE_NAME_TEST = "test.txt"
parameters = {
    "wordcount":{"workflowName":"wordcount", "parameters":{"cut":{"text_DB":FILE_NAME, "sliceNum":10}}},
    "workflow": {"workflowName":"workflow", "parameters":{"cal":{"arg1":2, "arg2":4},  "divide2":{"div":2.5}}}                       
            }


    
def workflowCreate(name):
    data = {"workflowName": name}
    res = requests.post(workflowCreateAddr, json=data)

def workflowDelete(name):
    data = {"workflowName": name}
    res = requests.post(workflowDeleteAddr, json=data)

def runWorkflow(workflowName):
    data = parameters[workflowName]
    result = requests.post(workflowRunAddr, json=data).json()["result"]
    return result['e2elatency']

def changeWorkerType(workflowName, funcName, workerType):
    filename = '/'.join([yamlDirPath, f'{workflowName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
    for i in range(len(yamlData["functions"])):
        func = yamlData['functions'][i]
        if funcName:
            if func['name'] == funcName:
                yamlData['functions'][i]["container"] = workerType
                with open(filename, 'w') as f:
                    yaml.dump(stream=f, data=yamlData)
                break
        else:
            yamlData['functions'][i]["container"] = workerType
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)

def changeWasmMode(workflowName, wasmMode):
    filename = '/'.join([yamlDirPath, f'{workflowName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
   
    yamlData['wasmMode'] = wasmMode
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)

def colde2eTime(workflowName, testTime):
    colde2etimes = []
    for i in range(testTime):
        if (i+1) % max((testTime) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{testTime}")
        workflowDelete(workflowName)
        workflowCreate(workflowName)
        result = runWorkflow(workflowName)
        colde2etimes.append(result)
    return colde2etimes

def warme2eTime(workflowName, testTime):
    warme2etimes = []
    workflowDelete(workflowName)
    workflowCreate(workflowName)
    runWorkflow(workflowName)
    for i in range(testTime):
        if (i+1) % max((testTime) // 10, 1) == 0:
            print(f"Test Step:{(i+1)}/{testTime}")
        result = runWorkflow(workflowName)
        warme2etimes.append(result)
    return warme2etimes


def testContainerType(testTime):
    e2eTime = {workflow:{} for workflow in FORKFLOW_LIST}
    containers = [ 'docker', 'wasm']
    timeFunc = {"cold":colde2eTime, "warm":warme2eTime}
    print("---------------------CONTAINER TYPE COST-----------------------------")
    for container in containers:
        for workflow in FORKFLOW_LIST:
            if workflow == "wordcount":
                changeWorkerType(workflow, 'count', container)
            else:
                changeWorkerType(workflow, '', container)
            e2eTime[workflow][container] = {}
            for startType in timeFunc.keys():
                print(f"Testing {container} {startType}.")
                e2eTime[workflow][container][startType] = timeFunc[startType](workflow, testTime)
    for workflow in FORKFLOW_LIST:
        workflow_df = []
        for container, startmode in e2eTime[workflow].items():
            tmp_df = {startType:times for startType, times in startmode.items()}
            tmp_df["container"] = container
            workflow_df.append(pd.DataFrame(tmp_df))
        workflow_df_combined = pd.concat(workflow_df, ignore_index=True)
        workflow_df_combined.to_csv('/'.join([resdir,"containerType",f'{workflow}_result.csv']), index=False)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    testContainerType(testTime)
