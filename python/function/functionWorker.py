import os
import signal
import sys
import time
import gevent
import requests
import base64


sys.path.append('./config')
import config
import subprocess

base_url = 'http://127.0.0.1:{}/{}'
proxyPath = config.WASMPROXYPATH


class FunctionWorker:
    def __init__(self, funcName, wasmCodePath, outputSize, port):
        self.workerProcess = None
        self.funcName = funcName
        self.wasmCodePath = wasmCodePath
        self.outputSize = outputSize
        self.lastTriggeredTime = 0
        self.message = "ready\n"
        self.port = port
        
    def startWorker(self):
        self.lastTriggeredTime = time.time()
        self.workerProcess = subprocess.Popen(["python", proxyPath, str(self.port)],stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        self.waitStart()
        initParam = {"wasmCodePath":self.wasmCodePath,'funcName':self.funcName,'outputSize':self.outputSize}
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
        return base64.b64decode(r.json()["out"])
        # print("run function {}. param:{}".format(self.funcName, param))
    
    def __del__(self):
        self.workerProcess.send_signal(signal.SIGINT)
        print(f"{self.funcName}'s worker deleted.")


