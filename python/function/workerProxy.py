import os
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import sys
sys.path.append('./config')
import config
import base64

workerPath = config.WORKERPATH
PIPE_WRITE_FD = config.PIPE_WRITE_FD
# db_server = couchdb.Server(couchdb_url)

class Runner:
    def __init__(self):
        self.wasmCodePath = ""
        self.funcName = ""
        self.outputSize = 0
        self.in_fd = 0
        self.out_fd = 1
        self.inputPipe = []
        self.outputPipe = []
        self.message = "ready\n"

    def init(self, wasmCodePath, funcName, outputSize):
        self.wasmCodePath = wasmCodePath
        self.funcName = funcName
        self.outputSize = outputSize
        p1 = os.pipe()
        p2 = os.pipe()
        self.workerPid = os.fork()
        if self.workerPid > 0:
            self.in_fd = p1[1]
            self.out_fd = p2[0]
            os.close(p1[0]) 
            os.close(p2[1]) 
            os.write(self.in_fd, (self.wasmCodePath+'\n').encode()) 
            os.write(self.in_fd, (self.funcName+'\n').encode()) 
            os.write(self.in_fd, (str(self.outputSize)+'\n').encode()) 
            message = os.read(self.out_fd, len(self.message))
            return str(message, encoding='utf-8')
        else:
            os.dup2(p1[0], 0)
            os.dup2(p2[1], PIPE_WRITE_FD)
            os.close(p1[1]) 
            os.close(p2[0]) 
            os.execvp(workerPath, [workerPath])
            print("error occured.")
            exit()

    def run(self,param):
        os.write(self.in_fd, param.encode()) 
        res = os.read(self.out_fd, self.outputSize)
        return base64.b64encode(res).decode('ascii')


proxy = Flask(__name__)
proxy.status = 'new'
runner = Runner()


@proxy.route('/status', methods=['GET'])
def status():
    res = {}
    res['status'] = proxy.status
    if runner.funcName:
        res['function'] = runner.funcName
    return res


@proxy.route('/init', methods=['POST'])
def init():
    proxy.status = 'init'
    inp = request.get_json(force=True, silent=True)
    message = runner.init(inp["wasmCodePath"], inp['funcName'], inp['outputSize'])

    proxy.status = 'ok'
    return {'status': proxy.status, "message":message}


@proxy.route('/run', methods=['POST'])
def run():
    proxy.status = 'run'

    inp = request.get_json(force=True, silent=True)
    # record the execution time
    out = runner.run(inp["parameters"])

    res = {
        "out": out
    }

    proxy.status = 'ok'
    return res


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python proxy.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    print(f"wasm proxy started on {port}.")
    proxy.run(debug=False, port=port)
