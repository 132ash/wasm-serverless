from gevent import monkey
monkey.patch_all()

import sys
import json
from typing import Dict
from flask import Flask, request
app = Flask(__name__)
from function_manager import FunctionManager

# create all fucntions when initialized.
functionManager = FunctionManager(watch_container_num=True)

@app.route('/request', methods = ['POST'])
def req():
    data = request.get_json(force=True, silent=True)
    funcName = data["funcName"]
    parameters = data["parameters"]
    status = 'ok'
    res, timeStamps = functionManager.run(funcName, parameters)
    return json.dumps({'status': status, 'res':res, 'reqTime':timeStamps[0], 'readyTime':timeStamps[1]})

# delete a fucntion's containers.
@app.route('/delete', methods = ['POST'])
def clear():
    data = request.get_json(force=True, silent=True)
    funcNames = data["funcNames"]
    functionManager.clear_containers(funcNames)
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
    # server = WSGIServer(('0.0.0.0', 8000), app)
    print(f"Docker proxy started on {sys.argv[1]+ ':'+ sys.argv[2]}.")
    server.serve_forever()
    # gevent.spawn_later(GET_NODE_INFO_INTERVAL)