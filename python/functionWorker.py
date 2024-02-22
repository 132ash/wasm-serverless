import os
import signal
import sys
from variables import *


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
    def startWorker(self):
        print("loaded data at {}.".format(self.wasmCodePath))
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
    def run(self, argc, argv):
        res = 0
        print("run function {}. argc: {}, argv:{}".format(self.funcName, argc, argv))
        parameters = str(argc) + " " + ' '.join(map(str, argv)) + '\n'
        os.write(self.in_fd, parameters.encode()) 
        res = os.read(self.out_fd, sys.getsizeof(res))
        return res
    def __del__(self):
        os.close(self.in_fd)
        os.close(self.out_fd)
        if self.workerPid > 0:
            os.kill(self.workerPid, signal.SIGKILL)
        print("worker deleted.")


