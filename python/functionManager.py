import gevent
import time

from functionWorker import FunctionWorker
from function import Function, FunctionInfo, RequestInfo

dispatch_interval = 0.5

class FunctionManager:
    def __init__(self):
        self.functions = {}
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)

    def createFunction(self, funcName, wasmCodePath, maxWorkers=10):
        info = FunctionInfo(funcName, wasmCodePath, maxWorkers)
        function = Function(info)
        # worker = FunctionWorker(funcName, wasmCodePath)
        # worker.startWorker()
        self.functions[funcName] = function

    def runFunction(self, funcName, data:list):
        # worker = self.functions[functionName]
        # res = worker.run(argc, argv)
        if funcName not in self.functions:
            raise Exception("No such function!")
        res = self.functions[funcName].sendRequest(data)
        return res
    
    def deleteFunction(self, funcName):
        self.functions.pop(funcName)

    def _dispatch_loop(self):
        print("[manager] new dispatch loop.")
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)
        for name, function in self.functions.items():
            print("[manager] dispatch function {}'s request.".format(name))
            gevent.spawn(function.dispatchRequest)


def sendReq(funcName, manager:FunctionManager, data):
    print("new request. data:{}".format(data))
    res = manager.runFunction(funcName, data)
    print("[client] get function res:{}, type:{}".format(res, type(res)))
    print("send over.\n")


if __name__ == "__main__":
    funcName = "funcTest"
    wasmCodePath = "/test.wasm"
    maxWorkers = 10
    manager = FunctionManager()
    data = [1,2]

    manager.createFunction(funcName, wasmCodePath, maxWorkers)

    while(True):
        sendReq(funcName, manager, data)
        time.sleep(1)
