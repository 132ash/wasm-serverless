import gevent
from gevent import monkey
monkey.patch_all()
import sys
import json
import requests
import uuid
import time

from datetime import datetime

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
    allFunctions, sources, containers = repo.getWorkflowFunctions(workflowName)
    trueFunctions = []
    workerTypes = []
    for func in  allFunctions:
        if sources[func] != 'SWITCH' and sources[func] != 'END':
            trueFunctions.append(func)
            workerTypes.append(containers[func])
    return trueFunctions, workerTypes


def createOnWorker(workflowName):
    trueFunctions, workerTypes = getWorkflowRealFunctions(workflowName)
    workerAddrs = repo.getAllWorkerAddrs(workflowName)
    for workerIP in workerAddrs:
        createUrl = 'http://{}/create'.format(workerIP)
        data = {"funcNames" : trueFunctions, 'workflowName':workflowName, 'workerTypes':workerTypes}
        requests.post(createUrl, json=data)
    if config.CONTROL_MODE == 'MasterSP': #Create workflowManager on master.
        createUrl = 'http://{}/create'.format(config.MASTER_HOST)
        data = {'workflowName':workflowName, 'master':True}
        requests.post(createUrl, json=data)
    return json.dumps({'status': 'ok'})

def deleteOnWorker(workflowName):
    trueFunctions = getWorkflowRealFunctions(workflowName)[0]
    workerAddrs = repo.getAllWorkerAddrs(workflowName)
    for workerIP in workerAddrs:
        deleteUrl = 'http://{}/delete'.format(workerIP)
        data = {"funcNames" : trueFunctions, 'workflowName':workflowName}
        requests.post(deleteUrl, json=data)
    return json.dumps({'status': 'ok'})

def triggerFunction(workflowName, request_id, function_name, param):
    info = repo.getFunctionInfo(function_name, workflowName)
    ip = ''
    if config.CONTROL_MODE == 'WorkerSP':
        ip = info['ip']
    elif config.CONTROL_MODE == 'MasterSP':
        ip = config.MASTER_HOST
    url = 'http://{}/workflow/request'.format(ip)
    data = {
        'requestId': request_id,
        'workflowName': workflowName,
        'functionName': function_name,
        'noParentExecution': True,
        'parameters': param
    }
    response = requests.post(url, json=data)
    response.close()

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
    funcLatency = repo.getLatency(requestId)

    # clear memory and other stuff
    if config.CLEAR_DB_AND_MEM:
        masterAddr  = ''
        if config.CONTROL_MODE == 'WorkerSP':
            masterAddr = repo.getAllWorkerAddrs(workflowName)[0]
        elif config.CONTROL_MODE == 'MasterSP':
            masterAddr = config.MASTER_HOST
        clear_url = 'http://{}/clear'.format(masterAddr)
        requests.post(clear_url, json={'requestID': requestId, 
                                       'master': True, 'workflowName': workflowName})
    return {'e2elatency':end - start, 'workflowResult': res, 'funcLatency':funcLatency}

@app.route('/workflow/create', methods = ['POST'])
def workflowCreate():
    data = request.get_json(force=True, silent=True)
    workflowName = data["workflowName"]
    groupAndSave(workflowName)
    createOnWorker(workflowName)
    return json.dumps({'status': 'ok'})

@app.route('/workflow/run', methods = ['POST'])
def workflowRun():
    data = request.get_json(force=True, silent=True)
    if 'requestID' not in data:
        id = str(uuid.uuid4())
    else:
        id = data["requestID"]
    workflowName = data["workflowName"]
    parameters = data["parameters"]
    res = runWorkflow(workflowName, id, parameters)
    # print("workflow result:{}".format(res))
    return json.dumps({'status': 'ok', 'result':res})

@app.route('/workflow/delete', methods = ['POST'])
def workflowDelete():
    data = request.get_json(force=True, silent=True)
    workflowName = data["workflowName"]
    deleteOnWorker(workflowName)
    deleteWorkflowDB(workflowName)
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