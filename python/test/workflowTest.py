import requests
import time

ip = "http://192.168.35.132:8000/"
workflowCreateAddr = ip + "workflow/create"
workflowDeleteAddr = ip + "workflow/delete"
workflowRunAddr = ip + "workflow/run"
FILE_NAME = "pg-being_ernest.txt"
FILE_NAME_TEST = "test.txt"
# workflowName = 'workflow'
# parameters = {"cal":{"arg1":2, "arg2":4},  "divide2":{"div":2.5}}

workflowName = 'wordcount'
parameters = {"cut":{"text_DB":FILE_NAME, "sliceNum":10}}

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

workflowCreate(workflowName)
workflowRun(workflowName)
time.sleep(1)
workflowRun(workflowName)
time.sleep(1)
workflowRun(workflowName)
time.sleep(1)
workflowDelete(workflowName)