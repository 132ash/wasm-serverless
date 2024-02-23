from gevent import monkey
monkey.patch_all()

import json
from functionManager import FunctionManager
from flask import Flask, request
app = Flask(__name__)
import sys

manager = FunctionManager()

@app.route('/request', methods = ['POST'])
def req():
    data = request.get_json(force=True, silent=True)
    funcName = data["funcName"]
    parameters = data["parameters"]
    status = 'ok'
    try:
        res = manager.runFunction(funcName, parameters)
        print("function result:{}".format(str(res)[0]))
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
        manager.deleteFunction(funcName)
    except BaseException as e:
        status = str(e)
    return json.dumps({'status': status})

@app.route('/create', methods = ['POST'])
def create():
    print("create a function.")
    data = request.get_json(force=True, silent=True)
    print(data)
    funcName = data["funcName"]
    wasmCodePath = data["wasmCodePath"]
    maxWorkers = data['maxWorkers']
    expireTime = data['expireTime']
    status = 'ok'
    try:
        manager.createFunction(funcName, wasmCodePath, maxWorkers, expireTime)
    except BaseException as e:
        status = str(e)
    return json.dumps({'status': status})
   

@app.route('/info', methods = ['GET'])
def info():
    funcNames = list(manager.functions.keys())
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