from gevent import monkey
monkey.patch_all()

import sys
sys.path.append('./function')
sys.path.append('./test')
import json
from functionManager import FunctionManager
from workflowManager import WorkflowManager
from flask import Flask, request
app = Flask(__name__)

class Dispatcher:
    def __init__(self) -> None:
        self.managers = {}
       
    def createManager(self, workflowName, functionManager):
        self.managers[workflowName] = WorkflowManager(sys.argv[1] + ':' + sys.argv[2], workflowName, functionManager)

    def getState(self, workflowName: str, requestId: str):
        return self.managers[workflowName].getState(requestId)

    def triggerFunction(self, workflowName, state, functionName, noParentExecution):
        self.managers[workflowName].triggerFunction(state, functionName, noParentExecution)

    def delState(self, workflowName, requestId, master):
        self.managers[workflowName].delState(requestId, master)



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
    funcName = data["funcName"]
    status = 'ok'
    try:
        functionManager.deleteFunction(funcName)
    except BaseException as e:
        status = str(e)
    return json.dumps({'status': status})

@app.route('/create', methods = ['POST'])
def create():
    data = request.get_json(force=True, silent=True)
    funcNames = data["funcNames"]
    if 'workflowName' in data:
        dispatcher.createManager(data['workflowName'])
    for funcName in funcNames:
        functionManager.createFunction(funcName)
    return json.dumps({'status': 'ok'})


   

@app.route('/info', methods = ['GET'])
def info():
    funcNames = list(functionManager.functions.keys())
    return json.dumps(funcNames)

from gevent.pywsgi import WSGIServer
import logging
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S', level='INFO')
    # server = WSGIServer((sys.argv[1], int(sys.argv[2])), app)
    server = WSGIServer(('0.0.0.0', 5000), app)
    print("server started.")
    server.serve_forever()
    # gevent.spawn_later(GET_NODE_INFO_INTERVAL)