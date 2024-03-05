import gevent
import time
import json
import struct

from python.function.functionWorker import FunctionWorker
from python.function.function import Function, FunctionInfo, RequestInfo

dispatch_interval = 0.005
repack_clean_interval = 5.000

class FunctionManager:
    def __init__(self):
        self.functions = {}
        gevent.spawn_later(repack_clean_interval, self._clean_loop)
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)

    def createFunction(self,funcName):
        info = FunctionInfo(funcName)
        function = Function(info)
        self.functions[funcName] = function

    def runFunction(self, funcName, data:list):
        if funcName not in self.functions:
            raise Exception("No such function!")
        func = self.functions[funcName]
        param = self.constructInput(data)
        res = func.sendRequest(param)
        return self.constructOutput(res, func.info)
    
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

    def constructInput(self, param):
        return json.dumps(param) + '\n'
        
    def constructOutput(self, uintBits, info):
        resType = info.output['type']
        resName = info.output['name']
        res = {}
        if resType == 'int':
            res[resName] = struct.unpack('<i', uintBits)[0]
        else:
            if resType == 'float':
                res[resName] = struct.unpack('<f', uintBits)[0]
            else:
                raise Exception("Invalid parameter type.")
        return res
