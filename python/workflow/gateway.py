import gevent
from gevent import monkey
monkey.patch_all()
import sys
import json
import requests
import uuid
import time

sys.path.append('./storage')
sys.path.append('./config')
import config

from python.grouping.grouping import groupAndSave
from repository import Repository
from flask import Flask, request
app = Flask(__name__)

repo = Repository()


def createOnWorker(workflowName):
    workerAddrs = repo.getAllWorkerAddrs(workflowName)
    functions = repo.getWorkflowFunctions(workflowName)
    for workerIP in workerAddrs:
        createUrl = 'http://{}/create'.format(workerIP)
        data = {"funcNames" : functions, 'workflowName':workflowName}
        requests.post(createUrl, json=data)
    return json.dumps({'status': 'ok'})

def triggerFunction(workflowName, request_id, function_name, param):
    info = repo.getFunctionInfo(function_name, workflowName)
    ip = info['ip']
    url = 'http://{}/workflow/request'.format(ip)
    data = {
        'requestId': request_id,
        'workflowName': workflowName,
        'funcName': function_name,
        'noParentExecution': True,
        'parameters': param
    }
    requests.post(url, json=data)

def runWorkflow(workflowName, requestId, parameters):
    repo.createRequestDoc(requestId)
    # allocate works
    startFunctions = repo.getStartFunctions(workflowName)
    start = time.time()
    jobs = []
    for func in startFunctions:
        jobs.append(gevent.spawn(triggerFunction, workflowName, requestId, func, parameters[func]))
    gevent.joinall(jobs)
    end = time.time()
    res = repo.getWorkflowRes(requestId)
    return {'latency':end - start, 'workflowResult': res}

@app.route('/workflow/create', methods = ['POST'])
def workflowCreate():
    data = request.get_json(force=True, silent=True)
    workflowName = data["workflowName"]
    groupAndSave(workflowName)
    createOnWorker(workflowName)
    return json.dumps({'status': 'ok'})

@app.route('/workflow/run', methods = ['POST'])
def workflowRun():
    id = str(uuid.uuid4())
    data = request.get_json(force=True, silent=True)
    workflowName = data["workflowName"]
    parameters = data["parameters"]
    res = runWorkflow(workflowName, id, parameters)
    print("workflow result:{}".format(res))
    return json.dumps({'status': 'ok', 'result':res})

# @app.route('/workflow/delete', methods = ['POST'])
# def workflowDelete():
#     data = request.get_json(force=True, silent=True)
#     workflowName = data["workflowName"]
#     status = 'ok'
#     manager = WorkflowManager(workflowName, functionManager)
#     try:
#         manager.deleteWorkflow(workflowName)
#     except BaseException as e:
#         status = str(e)
#     return json.dumps({'status': status})