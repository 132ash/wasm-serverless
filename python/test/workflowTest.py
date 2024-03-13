import requests

ip = "http://192.168.35.132:8000/"
workflowCreateAddr = ip + "workflow/create"
workflowDeleteAddr = ip + "workflow/delete"
workflowRunAddr = ip + "workflow/run"
workflowName = 'workflow'
parameters = {"cal":{"arg1":2, "arg2":4},  "divide2":{"div":2.5}}

def workflowCreate(name):
    data = {"workflowName": name}
    res = requests.post(workflowCreateAddr, json=data)
    print(f"workflow {name} create res:{res.text}")

def workflowRun(name):
    data = {"workflowName":name, "parameters":parameters}
    res = requests.post(workflowRunAddr, json=data)
    print(f"workflow {name} run res:{res.text}")

def workflowDelete(name):
    data = {"workflowName": name}
    res = requests.post(workflowDeleteAddr, json=data)
    print(f"workflow {name} delete res:{res.text}")

workflowCreate(workflowName)
workflowRun(workflowName)
workflowDelete(workflowName)