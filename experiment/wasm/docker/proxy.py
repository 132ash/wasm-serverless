from gevent import monkey
monkey.patch_all()

import sys
import json
from typing import Dict
from flask import Flask, request
app = Flask(__name__)
from function_manager import FunctionManager

# create all fucntions when initialized.
functionManager = FunctionManager()

@app.route('/request', methods = ['POST'])
def req():
    data = request.get_json(force=True, silent=True)
    funcName = data["funcName"]
    parameters = data["parameters"]
    status = 'ok'
    res = functionManager.run(funcName, parameters)
    return json.dumps({'status': status, 'res':res})

# delete all fucntions' containers.
@app.route('/delete', methods = ['GET'])
def clear():
    functionManager.clear_containers()
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
    # server = WSGIServer(('0.0.0.0', 8000), app)
    print(f"Docker proxy started on {sys.argv[1]+ ':'+ sys.argv[2]}.")
    server.serve_forever()
    # gevent.spawn_later(GET_NODE_INFO_INTERVAL)