import pandas as pd
import sys
import uuid
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
import requests
from criticalFunc import analyze
FILE_NAME = "pg-being_ernest.txt"
resdir = config.RESULT_DIR
gatewayAddr = ':'.join([config.HOST_IP, config.GATEWAY_PORT])
mode = config.CONTROL_MODE
workflowCreateAddr = '/'.join([gatewayAddr, "workflow/create"])
workflowDeleteAddr = '/'.join([gatewayAddr, "workflow/delete"])
workflowRunAddr = '/'.join([gatewayAddr, "workflow/run"])
FORKFLOW_LIST = ["workflow", "wordcount"]
parameters = {"workflow":{"workflowName":"workflow", "parameters":{"cal":{"arg1":2, "arg2":4},  "divide2":{"div":2.5}}},
              "wordcount":{"workflowName":"wordcount", "parameters":{"cut":{"text_DB":FILE_NAME, "sliceNum":10}}}
              }

def workflowCreate(name):
    data = {"workflowName": name}
    res = requests.post(workflowCreateAddr, json=data)

def workflowDelete(name):
    data = {"workflowName": name}
    res = requests.post(workflowDeleteAddr, json=data)

def runWorkflow(workflowName, reqID):
    data = parameters[workflowName]
    data.update({"requestID":reqID})
    result = requests.post(workflowRunAddr, json=data).json()["result"]
    return result['e2elatency'], result['funcLatency']

def getScheduleCost(e2elatency, funcLatency, workflowName):
    max_critical_time = {}
    criticalFuncs = analyze(workflowName, funcLatency)
    for func in criticalFuncs:
        if func not in max_critical_time:
            max_critical_time[func] = funcLatency[func]
        else:
            max_critical_time[func] = max(funcLatency[func], max_critical_time[func])
    # print(criticalFuncs)
    # print(funcLatency)
    return e2elatency - sum(max_critical_time.values())

def testScheduleCost(testTime):
    scheduleTime = {}
    print("---------------------SCHEDULE COST-----------------------------")
    for workflow in FORKFLOW_LIST:
        print(f"Testing workflow {workflow}.")
        scheduleTime[workflow] = []
        reqID  = str(uuid.uuid4())
        workflowCreate(workflow)
        runWorkflow(workflow, reqID)
        for i in range(testTime):
            if (i+1) % max((testTime) // 10, 1) == 0:
                print(f"Test Step:{(i+1)}/{testTime}")
            reqID  = str(uuid.uuid4())
            e2elatency, funcLatency = runWorkflow(workflow, reqID)
            scheduleTime[workflow].append(getScheduleCost(e2elatency,funcLatency,workflow))
        workflowDelete(workflow)
    # print(scheduleTime)
    df = pd.DataFrame(scheduleTime)
    df.to_csv('/'.join([resdir,"scheduleCost_test",mode+'_scheduleCost.csv']),  index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    testScheduleCost(testTime)
