import os
import signal
import sys
import logging
import time
from variables import *
from gevent import event
from gevent.lock import BoundedSemaphore


workerPath = "/home/ash/wasm/wasm-serverless/cpp_example/worker/build/worker"

class FunctionWorker:
    def __init__(self, funcName, wasmCodePath):
        self.workerPid = 1
        self.funcName = funcName
        self.inputPipe = []
        self.outputPipe = []
        self.wasmCodePath = wasmCodePath
        self.in_fd = 0
        self.out_fd = 1
        self.lastTriggeredTime = 0
        
    def startWorker(self):
        print("loaded data at {}.".format(self.wasmCodePath))
        self.lastTriggeredTime = time.time()
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
            return True
        else:
            os.dup2(p1[0], 0)
            os.dup2(p2[1], PIPE_WRITE_FD)
            os.close(p1[1]) 
            os.close(p2[0]) 
            os.execvp(workerPath, [workerPath])
            print("error occured.")
            exit()
    def run(self,param):
        res = 0
        self.lastTriggeredTime = time.time()
        # print("run function {}. param:{}".format(self.funcName, param))
        os.write(self.in_fd, param.encode()) 
        res = os.read(self.out_fd, sys.getsizeof(res))
        return res
    def __del__(self):
        os.close(self.in_fd)
        os.close(self.out_fd)
        if self.workerPid > 0:
            os.kill(self.workerPid, signal.SIGKILL)
        print("worker deleted.")


