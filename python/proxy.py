from gevent import monkey
monkey.patch_all()

import sys
sys.path.append('./workflow')
sys.path.append('./test')
import json
from workflowParser import Parser
from testFuncManager import FunctionManager
from workflowManager import WorkflowManager
from flask import Flask, request
app = Flask(__name__)

functionManager = FunctionManager()


@app.route('/request', methods = ['POST'])
def req():
    data = request.get_json(force=True, silent=True)
    funcName = data["funcName"]
    parameters = data["parameters"]
    status = 'ok'
    try:
        res = functionManager.runFunction(funcName, parameters)
        print("function result:{}".format(res))
        return json.dumps({'status': status, 'res':res})
    except BaseException as e:
        status = str(e)
        return json.dumps({'status': status})

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
    print("create a function.")
    data = request.get_json(force=True, silent=True)
    print(data)
    funcName = data["funcName"]
    status = 'ok'
    try:
        functionManager.createFunction(funcName)
    except BaseException as e:
        status = str(e)
    return json.dumps({'status': status})
   

@app.route('/info', methods = ['GET'])
def info():
    funcNames = list(functionManager.functions.keys())
    return json.dumps(funcNames)


@app.route('/workflow/create', methods = ['POST'])
def workflowCreate():
    data = request.get_json(force=True, silent=True)
    workflowName = data["workflowName"]
    parser = Parser(workflowName)
    status = 'ok'
    parser.parse()
    parser.saveWorkflowData()
    # except BaseException as e:
    #     status = str(e)
    return json.dumps({'status': status})

@app.route('/workflow/run', methods = ['POST'])
def workflowRun():
    data = request.get_json(force=True, silent=True)
    workflowName = data["workflowName"]
    parameters = data["parameters"]
    status = 'ok'
    manager = WorkflowManager(workflowName, functionManager)
    res = manager.runWorkflow(parameters)
    print("workflow result:{}".format(res))
    return json.dumps({'status': status, 'res':res})

@app.route('/workflow/delete', methods = ['POST'])
def workflowDelete():
    data = request.get_json(force=True, silent=True)
    workflowName = data["workflowName"]
    status = 'ok'
    manager = WorkflowManager(workflowName, functionManager)
    try:
        manager.deleteWorkflow(workflowName)
    except BaseException as e:
        status = str(e)
    return json.dumps({'status': status})
    


from gevent.pywsgi import WSGIServer
import logging
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S', level='INFO')
    # server = WSGIServer((sys.argv[1], int(sys.argv[2])), app)
    server = WSGIServer(('0.0.0.0', 5000), app)
    print("server started.")
    server.serve_forever()
    # gevent.spawn_later(GET_NODE_INFO_INTERVAL)