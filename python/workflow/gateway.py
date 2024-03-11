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
sys.path.append('./grouping')
import config

from grouping import groupAndSave, deleteWorkflowDB
from repository import Repository
from flask import Flask, request
app = Flask(__name__)

repo = Repository()

def getWorkflowRealFunctions(workflowName):
    allFunctions, sources = repo.getWorkflowFunctions(workflowName)
    trueFunctions = []
    for func in  allFunctions:
        if sources[func] != 'VIRTUAL' and sources[func] != 'END':
            trueFunctions.append(func)
    return trueFunctions


def createOnWorker(workflowName):
    trueFunctions = getWorkflowRealFunctions(workflowName)
    workerAddrs = repo.getAllWorkerAddrs(workflowName)
    for workerIP in workerAddrs:
        createUrl = 'http://{}/create'.format(workerIP)
        data = {"funcNames" : trueFunctions, 'workflowName':workflowName}
        requests.post(createUrl, json=data)
    return json.dumps({'status': 'ok'})

def deleteOnWorker(workflowName):
    trueFunctions = getWorkflowRealFunctions(workflowName)
    workerAddrs = repo.getAllWorkerAddrs(workflowName)
    for workerIP in workerAddrs:
        deleteUrl = 'http://{}/delete'.format(workerIP)
        data = {"funcNames" : trueFunctions, 'workflowName':workflowName}
        requests.post(deleteUrl, json=data)
    return json.dumps({'status': 'ok'})

def triggerFunction(workflowName, request_id, function_name, param):
    info = repo.getFunctionInfo(function_name, workflowName)
    ip = info['ip']
    url = 'http://{}/workflow/request'.format(ip)
    data = {
        'requestId': request_id,
        'workflowName': workflowName,
        'functionName': function_name,
        'noParentExecution': True,
        'parameters': param
    }
    requests.post(url, json=data)

def runWorkflow(workflowName, requestId, parameters):
    # allocate works
    startFunctions = repo.getStartFunctions(workflowName)
    start = time.time()
    jobs = []
    for func in startFunctions:
        jobs.append(gevent.spawn(triggerFunction, workflowName, requestId, func, parameters[func]))
    gevent.joinall(jobs)
    end = time.time()
    print("[GATEWAY] workflow finished.")
    res = repo.getWorkflowRes(requestId)

    # clear memory and other stuff
    if config.CLEAR_DB_AND_MEM:
        masterAddr = repo.getAllWorkerAddrs(workflowName + '_workflow_metadata')[0]
        clear_url = 'http://{}/clear'.format(masterAddr)
        requests.post(clear_url, json={'requestID': requestId, 
                                       'master': True, 'workflowName': workflowName})
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

@app.route('/workflow/delete', methods = ['POST'])
def workflowDeeate():
    data = request.get_json(force=True, silent=True)
    workflowName = data["workflowName"]
    deleteWorkflowDB(workflowName)
    deleteOnWorker(workflowName)
    return json.dumps({'status': 'ok'})

from gevent.pywsgi import WSGIServer
import logging
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S', level='INFO')
    server = WSGIServer((sys.argv[1], int(sys.argv[2])), app)
    # server = WSGIServer(('0.0.0.0', 8000), app)
    print(f"gateway started on {sys.argv[1]+ ':'+ sys.argv[2]}.")
    server.serve_forever()
    # gevent.spawn_later(GET_NODE_INFO_INTERVAL)