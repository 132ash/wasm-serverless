import os
import signal
import sys
import time
import gevent
from requests.adapters import HTTPAdapter
import requests
import base64


sys.path.append('./config')
import config
import subprocess

base_url = 'http://127.0.0.1:{}/{}'
connection_pool_size = 500
proxyPath = config.WASMPROXYPATH

def preexec_function():
    # 将子进程的进程组 ID 设置为其自身的 PID
    os.setpgrp()



class FunctionWorker:
    def __init__(self, funcName, wasmCodePath, outputSize, port, heapSize):
        self.workerProcess = None
        self.funcName = funcName
        self.wasmCodePath = wasmCodePath
        self.outputSize = outputSize
        self.heapSize = heapSize
        self.lastTriggeredTime = 0
        self.message = "ready\n"
        self.port = port
        
    def startWorker(self):
        self.lastTriggeredTime = time.time()
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
        r = requests.post(base_url.format(self.port, 'run'), json={"parameters":param})
        self.lastTriggeredTime = time.time()
        # print(f"{self.funcName}'s worker run. pid:{self.workerProcess}")
        return base64.b64decode(r.json()["out"])
        
        # print("run function {}. param:{}".format(self.funcName, param))
    
    def destroy(self):
        # print(f"{self.funcName}'s worker delete. pid:{self.workerProcess}")
        os.killpg(self.workerProcess.pid, signal.SIGKILL)


