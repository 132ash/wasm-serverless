from gevent import monkey
monkey.patch_all()

import sys
sys.path.append('./function')
sys.path.append('./test')
sys.path.append('./config')
import json
import signal
from typing import Dict
from functionManager import FunctionManager
from workersp import WorkerSPManager
from mastersp import MasterSPManager
from flask import Flask, request
app = Flask(__name__)

import config
CONTROL_MODE = config.CONTROL_MODE

class Dispatcher:
    def __init__(self) -> None:
        self.managers = {}
       
    def createManager(self, control_mode, workflowName, functionManager):
        if control_mode == 'WorkerSP':
            self.managers[workflowName] = WorkerSPManager(sys.argv[1] + ':' + sys.argv[2], workflowName, functionManager)
        elif control_mode == 'MasterSP':
            self.managers[workflowName] = MasterSPManager(sys.argv[1] + ':' + sys.argv[2], workflowName, functionManager)

    def deleteManager(self, workflowName):
        self.managers.pop(workflowName)
      
    def getState(self, workflowName: str, requestId: str):
        return self.managers[workflowName].getState(requestId)

    def triggerFunction(self, workflowName:str, state, functionName, parameters,  noParentExecution):
        return self.managers[workflowName].triggerFunction(state, functionName, parameters, noParentExecution)

    def clearDB(self, workflowName:str, reqID):
        self.managers[workflowName].clearDB(reqID)

    def delStateAndParam(self, workflowName, requestId, master):
        self.managers[workflowName].delStateAndParam(requestId, master)

functionManager = FunctionManager(watch_container_num=False)
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
    res = dispatcher.triggerFunction(workflowName, state, functionName, parameters, noParentExecution)
    return json.dumps({'status': 'ok', 'res':res})

@app.route('/request', methods = ['POST'])
def req():
    data = request.get_json(force=True, silent=True)
    funcName = data["funcName"]
    parameters = data["parameters"]
    status = 'ok'
    res, timeStamps = functionManager.runFunction(funcName, parameters)
    return json.dumps({'status': status, 'res':res, 'timeStamps':timeStamps})

@app.route('/delete', methods = ['POST'])
def delete():
    data = request.get_json(force=True, silent=True)
    funcNames = data["funcNames"]
    if 'workflowName' in data:
        dispatcher.deleteManager(data['workflowName'])
    for funcName in funcNames:
        functionManager.deleteFunction(funcName)
    return json.dumps({'status': 'ok'})

@app.route('/create', methods = ['POST'])
def create():
    data = request.get_json(force=True, silent=True)
    master = data.get('master', False)
    workerTypes = []
    msgs = {}
    workerType = ''
    if 'workflowName' in data:
        dispatcher.createManager(CONTROL_MODE, data['workflowName'], functionManager)
    if not master: # not create functon on master in mastersp.
        funcNames = data["funcNames"]
        workerTypes = data["workerTypes"]
        heapSize = data.get("heapSize", 1024 * 1024 * 10)
        for i, funcName in enumerate(funcNames):
            if len(workerTypes) != 0:
                workerType = workerTypes[i]
            msgs[funcName]=functionManager.createFunction(funcName, workerType, heapSize)
    return json.dumps({'status': 'ok', 'msg':msgs})

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


@app.route('/info', methods = ['POST'])
def info():
    data = request.get_json(force=True, silent=True)
    funcName = data['funcName']
    container_num = functionManager.functions[funcName].numOfContainer
    return json.dumps({"containerNum":container_num})

from gevent.pywsgi import WSGIServer
import logging
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S', level='INFO')
    server = WSGIServer((sys.argv[1], int(sys.argv[2])), app)
    # server = WSGIServer(('0.0.0.0', 7000), app)

    
    def signal_handler(sig, frame):
        print('收到停止信号，正在关闭所有子进程...')
        for funcName in functionManager.functions:
            functionManager.deleteFunction(funcName)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)


    # run on 7000.
    print(f"proxy started on {sys.argv[1]+ ':'+ sys.argv[2]}.")
    server.serve_forever()
    # gevent.spawn_later(GET_NODE_INFO_INTERVAL)