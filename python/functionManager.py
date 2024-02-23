import gevent
import time

from functionWorker import FunctionWorker
from function import Function, FunctionInfo, RequestInfo

dispatch_interval = 0.005
repack_clean_interval = 5.000

class FunctionManager:
    def __init__(self):
        self.functions = {}
        gevent.spawn_later(repack_clean_interval, self._clean_loop)
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)

    def createFunction(self, funcName, wasmCodePath, maxWorkers=10, expireTime=600):
        info = FunctionInfo(funcName, wasmCodePath, maxWorkers, expireTime)
        function = Function(info)
        self.functions[funcName] = function

    def runFunction(self, funcName, data:list):
        if funcName not in self.functions:
            raise Exception("No such function!")
        res = self.functions[funcName].sendRequest(data)
        return res
    
    def deleteFunction(self, funcName):
        self.functions.pop(funcName)

    def _dispatch_loop(self):
        # print("[manager] new dispatch loop.")
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)
        for name, function in self.functions.items():
            # print("[manager] dispatch function {}'s request.".format(name))
            gevent.spawn(function.dispatchRequest)

    def _clean_loop(self):
        # print("[manager] new clean loop.")
        gevent.spawn_later(repack_clean_interval, self._clean_loop)
        for name, function in self.functions.items():
            # print("[manager] cleaning function {}'s workers.".format(name))
            gevent.spawn(function.cleanWorker)
