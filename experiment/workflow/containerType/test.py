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
FORKFLOW_LIST = ["wordcount"]
parameters = {"wordcount":{"workflowName":"wordcount", "parameters":{"cal":{"arg1":2, "arg2":4},  "divide2":{"div":2.5}}}}

def workflowCreate(name):
    data = {"workflowName": name}
    res = requests.post(workflowCreateAddr, json=data)
    print(f"workflow {name} create res:{res.text}")

def workflowDelete(name):
    data = {"workflowName": name}
    res = requests.post(workflowDeleteAddr, json=data)
    print(f"workflow {name} delete res:{res.text}")

def runWorkflow(workflowName, reqID):
    data = parameters[workflowName]
    data.update({"requestID":reqID})
    result = requests.post(workflowRunAddr, json=data).json()["result"]
    return result['e2elatency']

def changeWorkerType(workflowName, funcName):
    yamlData = yaml.load(open('/'.join[yamlDirPath, f'{workflowName}.yaml']), Loader=yaml.FullLoader)
    for i in range(len(yamlData["functions"])):
        func = yamlData[i]
        if func['name'] == funcName:
            yamlData[i]["container"] = 


def testScheduleCost(testTime):
    scheduleTime = {}
    print("---------------------SCHEDULE COST-----------------------------")
    for workflow in FORKFLOW_LIST:
        scheduleTime[workflow] = []
        reqID  = str(uuid.uuid4())
        workflowCreate(workflow)
        runWorkflow(workflow, reqID)
        for _ in range(testTime):
            reqID  = str(uuid.uuid4())
            e2elatency, funcLatency = runWorkflow(workflow, reqID)
            scheduleTime[workflow].append(getScheduleCost(e2elatency,funcLatency,workflow))
        workflowDelete(workflow)
    print(scheduleTime)
    df = pd.DataFrame(scheduleTime)
    df.to_csv('/'.join([resdir,"scheduleCost",mode+'_scheduleCost.csv']),  index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    testScheduleCost(testTime)
