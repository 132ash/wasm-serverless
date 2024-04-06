import os
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import sys
sys.path.append('./config')
import config
import base64

workerPath = config.WORKERPATH
PIPE_WRITE_FD = config.PIPE_WRITE_FD
STATE_WRITE_FD = config.STATE_WRITE_FD 
# db_server = couchdb.Server(couchdb_url)

class Runner:
    def __init__(self):
        self.wasmCodePath = ""
        self.funcName = ""
        self.outputSize = 0
        self.in_fd = 0
        self.out_fd = 1
        self.state_fd = 2
        self.inputPipe = []
        self.outputPipe = []
        self.statePipe = []
        self.message = b'ready\n'

    def init(self, wasmCodePath, funcName, outputSize, heapSize):
        self.wasmCodePath = wasmCodePath
        self.funcName = funcName
        self.outputSize = outputSize
        self.heapSize = heapSize
        p1 = os.pipe()
        p2 = os.pipe()
        p3 = os.pipe()
        self.workerPid = os.fork()
        if self.workerPid > 0:
            self.in_fd = p1[1]
            self.out_fd = p2[0]
            self.state_fd = p3[0]
            os.close(p1[0]) 
            os.close(p2[1]) 
            os.close(p3[1]) 
            os.write(self.in_fd, (self.wasmCodePath+'\n').encode()) 
            os.write(self.in_fd, (self.funcName+'\n').encode()) 
            os.write(self.in_fd, (str(self.outputSize)+'\n').encode()) 
            os.write(self.in_fd, (str(self.heapSize)+'\n').encode()) 
            return 
        else:
            os.dup2(p1[0], 0)
            os.dup2(p2[1], PIPE_WRITE_FD)
            os.dup2(p3[1], STATE_WRITE_FD)
            os.close(p1[1]) 
            os.close(p2[0]) 
            os.close(p3[0])
            os.execvp(workerPath, [workerPath])
            print("error occured.")
            exit()

    def getState(self):
        message = os.read(self.state_fd, len(self.message))
        return message

    def getResultFromPipe(self, expected_size):
        data_received = b''
        while len(data_received) < expected_size:
            # 这里的读操作会阻塞，直到有数据可读
            data = os.read(self.out_fd, 4096)  # 尝试读取4KB
            if not data:
                # 如果没有读到数据，表示管道已经关闭
                break
            data_received += data
        return data_received

    def run(self,param):
        msg = self.getState()
        print(msg)
        if msg == self.message:
            data = param.encode()
            print(len(data))
            os.write(self.in_fd, data) 
            res = self.getResultFromPipe(self.outputSize+16)    
            # os.read(self.out_fd, self.outputSize+16)
            return base64.b64encode(res).decode('ascii')
        else:
            return base64.b64encode(b'').decode('ascii')


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
    heapSize = inp.get("heapSize", 1024 * 1024 * 10)
    runner.init(inp["wasmCodePath"], inp['funcName'], inp['outputSize'], heapSize)

    proxy.status = 'ok'
    return {'status': proxy.status}


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
