import os
import signal
import sys
import time
import psutil
import chardet
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

# def preexec_function():
#     # 将子进程的进程组 ID 设置为其自身的 PID
#     os.setpgrp()



class FunctionWorker:
    def __init__(self, info:FunctionInfo, port, type, wasmParam, dockerParam):
        self.type = type
        self.info = info
        self.funcName = info.name
        self.port = port
        if self.type == 'wasm':
            self.worker = wasmWorker(info.name, info, port, wasmParam['wasmCodePath'],  wasmParam['outputSize'],  wasmParam['heapSize'])
        elif self.type == 'docker':
            self.worker = dockerWorker(info.name, dockerParam['client'], dockerParam['imageName'], port)
        self.lastTriggeredTime = time.time()
        
    def startWorker(self):
        self.lastTriggeredTime = time.time()
        self.worker.startWorker()
        
    def run(self,param):
        start = time.time()
        res = self.worker.run(param)
        end = time.time()
        self.lastTriggeredTime = time.time()
        return res
        # print("run function {}. param:{}".format(self.funcName, param))
    
    def destroy(self):
        # print(f"{self.funcName}'s worker delete. pid:{self.workerProcess}")
        self.worker.destroy()


class wasmWorker:
    def __init__(self, funcName, info:FunctionInfo, port, wasmCodePath='', outputSize=0, heapSize=1024*1024*10):
        self.workerProcess = None
        self.info = info
        self.funcName = funcName
        self.wasmCodePath = wasmCodePath
        self.outputSize = outputSize
        self.heapSize = heapSize
        self.lastTriggeredTime = 0
        self.port = port

    def startWorker(self):
        self.workerProcess = subprocess.Popen(["python", proxyPath, str(self.port)],stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, start_new_session=True)
        self.waitStart()
        initParam = {"wasmCodePath":self.wasmCodePath,'funcName':self.funcName,'outputSize':self.outputSize, "heapSize":self.heapSize}
        r = requests.post(base_url.format(self.port, 'init'), json=initParam)
        # print(f"{self.funcName}'s worker {self.workerProcess.pid} start on port {self.port}.")
        # # print(r.json())
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
        data = self.constructInput(param)
        postProxyTime = time.time()
        r = requests.post(base_url.format(self.port, 'run'), json={"parameters":data})
        res, wasmTimeStamp = self.constructOutput(base64.b64decode(r.json()["out"]))
        res["postProxyTime"] = postProxyTime
        res["wasmTimeStamp"] = wasmTimeStamp
        # print(f"{self.funcName}'s worker {self.workerProcess.pid} exists: {psutil.pid_exists(self.workerProcess.pid)}.")
        return res
        
        # print("run function {}. param:{}".format(self.funcName, param))
    
    def destroy(self):
        # print(f"delete {self.funcName}'s worker. pid:{self.workerProcess.pid}")
        pid = self.workerProcess.pid
        if psutil.pid_exists(pid):
            os.killpg(pid, signal.SIGKILL)
        else:
            print(f"{self.funcName}'s worker {self.workerProcess.pid} doesn't exist.")


    def constructInput(self, data):
        param = {}
        prefix = 1
        for name, _ in self.info.input.items():
            param[str(prefix)+name] = data[name]
            prefix += 1
        return json.dumps(param) + '\n'
    
    def constructOutput(self, uintBits):
        res = {}
        wasmTimeStamps = []
        bitsIdx = 0
        for name, type in self.info.output.items():
            if type == 'string':
                start = bitsIdx 
                while uintBits[bitsIdx] != 0:
                    bitsIdx += 1
                # encoding = chardet.detect(uintBits[start:bitsIdx])['encoding']
                # print(f"encoding: {encoding}")
                res[name] = uintBits[start:bitsIdx].decode("ISO-8859-1")
                # except:
                #     print(uintBits[18780:18798])
                #     print(uintBits[18799:18810])
                #     input("wrong decode.")
                bitsIdx += 1
            elif type == 'long long':
                chunk = uintBits[bitsIdx:bitsIdx+8]
                res[name] = int.from_bytes(chunk, 'little')
                bitsIdx += 8
            elif type == 'double':
                chunk = uintBits[bitsIdx:bitsIdx+8]
                res[name] = struct.unpack('<d', chunk)[0]
                bitsIdx += 8
            else:
                chunk = uintBits[bitsIdx:bitsIdx+4]
                if type == 'int':
                    res[name] = struct.unpack('<i', chunk)[0]
                elif type == 'float':
                    res[name] = struct.unpack('<f', chunk)[0]
                bitsIdx += 4 
        bitsIdx = self.outputSize
        for _ in range(4):
            chunk = uintBits[bitsIdx:bitsIdx+8]
            wasmTimeStamps.append(int.from_bytes(chunk, 'little'))
            bitsIdx += 8
        return res, wasmTimeStamps


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
        postProxyTime = time.time()
        r = requests.post(base_url.format(self.port, 'run'), json=data)
        self.lasttime = time.time()
        res = r.json()
        res['postProxyTime'] = postProxyTime
        return res

    # initialize the container
    def init(self):
        data = {'function': self.funcName }
        r = requests.post(base_url.format(self.port, 'init'), json=data)
        self.lasttime = time.time()
        return r.status_code == 200

    # kill and remove the container
    def destroy(self):
        self.container.remove(force=True)
