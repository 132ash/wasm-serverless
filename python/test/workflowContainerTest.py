import requests
import time
import yaml

ip = "http://192.168.35.132:8000/"
workflowCreateAddr = ip + "workflow/create"
workflowDeleteAddr = ip + "workflow/delete"
workflowRunAddr = ip + "workflow/run"
yamlDirPath  = "/home/ash/wasm/wasm-serverless/python/yaml/workflow"

FILE_NAME = "pg-being_ernest.txt"
FILE_NAME_TEST = "test.txt"
mode = ["wasm", 'docker']
workflowName = 'workflow'
parameters = {"cal":{"arg1":2, "arg2":4},  "divide2":{"div":2.5}}

# workflowName = 'wordcount'
# parameters = {"cut":{"text_DB":FILE_NAME, "sliceNum":10}}

def changeWorkerType(workflowName, workerType):
    filename = '/'.join([yamlDirPath, f'{workflowName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
    for i in range(len(yamlData["functions"])):
        yamlData['functions'][i]["container"] = workerType
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)

def workflowCreate(name):
    data = {"workflowName": name}
    res = requests.post(workflowCreateAddr, json=data)
    print(f"workflow {name} create res:{res.text}")

def workflowRun(name):
    data = {"workflowName":name, "parameters":parameters}
    res = requests.post(workflowRunAddr, json=data).json()
    print(f"workflow {name} run res:{res['result']['workflowResult']}")
    print(f"workflow {name} run latency:{res['result']['e2elatency']}")
    print(f"function run latency:{res['result']['funcLatency']}")

def workflowDelete(name):
    data = {"workflowName": name}
    res = requests.post(workflowDeleteAddr, json=data)
    print(f"workflow {name} delete res:{res.text}")

for worker in mode:
    changeWorkerType(workflowName, worker)
    workflowCreate(workflowName)
    workflowRun(workflowName)
    time.sleep(1)
    workflowRun(workflowName)
    time.sleep(1)
    workflowRun(workflowName)
    time.sleep(1)
    workflowDelete(workflowName)