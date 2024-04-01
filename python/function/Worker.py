import os
import signal
import sys
import time
import json
import gevent
import struct
from functionInfo import FunctionInfo
from requests.adapters import HTTPAdapter
import requests
import base64


sys.path.append('./config')
sys.path.append('./workflow')
import config
import subprocess

base_url = 'http://127.0.0.1:{}/{}'
connection_pool_size = 500
proxyPath = config.WASMPROXYPATH

def preexec_function():
    # 将子进程的进程组 ID 设置为其自身的 PID
    os.setpgrp()



class FunctionWorker:
    def __init__(self, info:FunctionInfo, port, type, wasmParam, dockerParam):
        self.type = type
        self.info = info
        self.funcName = info.name
        if self.type == 'wasm':
            self.worker = wasmWorker(info.name, info, port, wasmParam['wasmCodePath'],  wasmParam['outputSize'],  wasmParam['heapSize'])
        elif self.type == 'docker':
            self.worker = dockerWorker(info.name, dockerParam['client'], dockerParam['imageName'], port)
        self.lastTriggeredTime = -1
        
    def startWorker(self):
        self.lastTriggeredTime = time.time()
        self.worker.startWorker()
        
    def run(self,param):
        res = self.worker.run(param)
        self.lastTriggeredTime = time.time()
        # print(f"{self.funcName}'s worker run. pid:{self.workerProcess}")
        return res
        # print("run function {}. param:{}".format(self.funcName, param))
    
    def destroy(self):
        # print(f"{self.funcName}'s worker delete. pid:{self.workerProcess}")
        self.worker.destroy()


class wasmWorker:
    def __init__(self, funcName, info:FunctionInfo, port, wasmCodePath='', outputSize=0, heapSize=1024*10):
        self.workerProcess = None
        self.info = info
        self.funcName = funcName
        self.wasmCodePath = wasmCodePath
        self.outputSize = outputSize
        self.heapSize = heapSize
        self.lastTriggeredTime = 0
        self.message = "ready\n"
        self.port = port

    def startWorker(self):
        self.workerProcess = subprocess.Popen(["python", proxyPath, str(self.port)],stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, preexec_fn=preexec_function)
        self.waitStart()
        # print(f"{self.funcName}'s worker start. pid:{self.workerProcess}")
        initParam = {"wasmCodePath":self.wasmCodePath,'funcName':self.funcName,'outputSize':self.outputSize, "heapSize":self.heapSize}
        r = requests.post(base_url.format(self.port, 'init'), json=initParam)
        # print(r.json())
        # return 

    def waitStart(self):
        while True:
            try:
                r = requests.get(base_url.format(self.port, 'status'))
                if r.status_code == 200:
                    break
            except Exception:
                pass
            gevent.sleep(0.005)
        
    def run(self,param):
        r = requests.post(base_url.format(self.port, 'run'), json={"parameters":self.constructInput(param)})
        # print(f"{self.funcName}'s worker run. pid:{self.workerProcess}")
        print(base64.b64decode(r.json()["out"]))
        return self.constructOutput(base64.b64decode(r.json()["out"]))
        
        # print("run function {}. param:{}".format(self.funcName, param))
    
    def destroy(self):
        print(f"{self.funcName}'s worker delete. pid:{self.workerProcess}")
        pid = self.workerProcess.pid
        os.killpg(pid, signal.SIGKILL)


    def constructInput(self, data):
        param = {}
        prefix = 1
        for name, _ in self.info.input.items():
            param[str(prefix)+name] = data[name]
            prefix += 1
        return json.dumps(param) + '\n'
    
    def constructOutput(self, uintBits):
        res = {}
        bitsIdx = 0
        for name, type in self.info.output.items():
            if type == 'string':
                start = bitsIdx 
                while uintBits[bitsIdx] != 0:
                    bitsIdx += 1
                res[name] = uintBits[start:bitsIdx].decode('ascii')
                bitsIdx += 1
            elif type == 'double':
                chunk = uintBits[bitsIdx:bitsIdx+8]
                res[name] = int.from_bytes(chunk, 'little')
                bitsIdx += 8
            else:
                chunk = uintBits[bitsIdx:bitsIdx+4]
                if type == 'int':
                    res[name] = struct.unpack('<i', chunk)[0]
                elif type == 'float':
                    res[name] = struct.unpack('<f', chunk)[0]
                bitsIdx += 4 
        # for _ in range(2):
        #     chunk = uintBits[bitsIdx:bitsIdx+8]
        #     timeStamps.append(int.from_bytes(chunk, 'little'))
        #     bitsIdx += 8
        return res


class dockerWorker:

    def __init__(self, funcName, client, image_name, port):
        self.client = client
        self.funcName = funcName
        self.image_name = image_name
        self.port = port
        self.attr = 'exec'
        self.funcName = funcName
        self.lasttime = -1

    def startWorker(self):
        self.lasttime = time.time()
        self.container  = self.client.containers.run(self.image_name,
                                                    detach=True,
                                                    ports={'5000/tcp': str(self.port)},
                                                    labels=['dockerContainer'])
        self.waitStart()
        self.init()

    # wait for the container cold start
    def waitStart(self):
        while True:
            try:
                r = requests.get(base_url.format(self.port, 'status'))
                if r.status_code == 200:
                    break
            except Exception:
                pass
            gevent.sleep(0.005)

    # send a request to container and wait for result
    def run(self, data = {}):
        r = requests.post(base_url.format(self.port, 'run'), json=data)
        self.lasttime = time.time()
        return r.json()

    # initialize the container
    def init(self):
        data = {'function': self.funcName }
        r = requests.post(base_url.format(self.port, 'init'), json=data)
        self.lasttime = time.time()
        return r.status_code == 200

    # kill and remove the container
    def destroy(self):
        self.container.remove(force=True)
