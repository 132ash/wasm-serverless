from gevent import monkey
monkey.patch_all()

import sys
sys.path.append('./function')
sys.path.append('./test')
import json
from typing import Dict
from functionManager import FunctionManager
from workflowManager import WorkflowManager
from flask import Flask, request
app = Flask(__name__)

class Dispatcher:
    def __init__(self) -> None:
        self.managers:Dict[str, WorkflowManager] = {}
       
    def createManager(self, workflowName, functionManager):
        self.managers[workflowName] = WorkflowManager(sys.argv[1] + ':' + sys.argv[2], workflowName, functionManager)

    def deleteManager(self, workflowName):
        self.managers.pop(workflowName)
      
    def getState(self, workflowName: str, requestId: str):
        return self.managers[workflowName].getState(requestId)

    def triggerFunction(self, workflowName:str, state, functionName, parameters,  noParentExecution):
        self.managers[workflowName].triggerFunction(state, functionName, parameters, noParentExecution)

    def clearDB(self, workflowName:str, reqID):
        self.managers[workflowName].clearDB(reqID)

    def delStateAndParam(self, workflowName, requestId, master):
        self.managers[workflowName].delStateAndParam(requestId, master)

functionManager = FunctionManager()
dispatcher = Dispatcher()


@app.route('/workflow/request', methods = ['POST'])
def workflowReq():
    data = request.get_json(force=True, silent=True)
    requestId = data['requestId']
    workflowName = data['workflowName']
    functionName = data['functionName']
    noParentExecution = data['noParentExecution']
    parameters = data['parameters']
    # get the corresponding workflow state and trigger the function
    state = dispatcher.getState(workflowName, requestId)
    dispatcher.triggerFunction(workflowName, state, functionName, parameters, noParentExecution)
    return json.dumps({'status': 'ok'})

@app.route('/request', methods = ['POST'])
def req():
    data = request.get_json(force=True, silent=True)
    funcName = data["funcName"]
    parameters = data["parameters"]
    status = 'ok'
    res = functionManager.runFunction(funcName, parameters)
    return json.dumps({'status': status, 'res':res})

@app.route('/delete', methods = ['POST'])
def delete():
    data = request.get_json(force=True, silent=True)
    funcNames = data["funcNames"]
    if 'workflowName' in data:
        dispatcher.deleteManager(data['workflowName'], functionManager)
    for funcName in funcNames:
        functionManager.deleteFunction(funcName)
    return json.dumps({'status': 'ok'})

@app.route('/create', methods = ['POST'])
def create():
    data = request.get_json(force=True, silent=True)
    funcNames = data["funcNames"]
    if 'workflowName' in data:
        dispatcher.createManager(data['workflowName'], functionManager)
    for funcName in funcNames:
        functionManager.createFunction(funcName)
    return json.dumps({'status': 'ok'})

@app.route('/clear', methods = ['GET'])
def clear():
    data = request.get_json(force=True, silent=True)
    workflow_name = data['workflowName']
    request_id = data['requestID']
    master = False
    if 'master' in data:
        master = True
        dispatcher.clearDB(workflow_name, request_id) # optional: clear results in center db
    dispatcher.delStateAndParam(workflow_name, request_id, master) # and remove state for every node
    return json.dumps({'status': 'ok'})


@app.route('/info', methods = ['GET'])
def info():
    funcNames = list(functionManager.functions.keys())
    return json.dumps(funcNames)

from gevent.pywsgi import WSGIServer
import logging
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S', level='INFO')
    server = WSGIServer((sys.argv[1], int(sys.argv[2])), app)
    # server = WSGIServer(('0.0.0.0', 7000), app)
    print(f"proxy started on {sys.argv[1]+ ':'+ sys.argv[2]}.")
    server.serve_forever()
    # gevent.spawn_later(GET_NODE_INFO_INTERVAL)