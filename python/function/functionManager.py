import gevent
import time
import json
import struct

from functionWorker import FunctionWorker
from function import Function, FunctionInfo, RequestInfo
from typing import Any, Dict, List

dispatch_interval = 0.005
repack_clean_interval = 5.000

class FunctionManager:
    def __init__(self):
        self.functions: Dict[str, Function] = {} 
        gevent.spawn_later(repack_clean_interval, self._clean_loop)
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)

    def createFunction(self,funcName):
        info = FunctionInfo(funcName)
        function = Function(info)
        self.functions[funcName] = function

    def runFunction(self, funcName:str, data:dict):
        if funcName not in self.functions:
            raise Exception("No such function!")
        func = self.functions[funcName]
        print(f"[funcManager] run function {funcName} with param {data}.")
        param = self.constructInput(data, func.info)
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
        for _, function in self.functions.items():
            # print("[manager] cleaning function {}'s workers.".format(name))
            gevent.spawn(function.cleanWorker)

    def constructInput(self, data, info):
        param = {}
        for name, _ in info.input.items():
            param[name] = data[name]
        return json.dumps(param) + '\n'
        
    def constructOutput(self, uintBits, info):
        res = {}
        bitsIdx = 0
        for name, type in info.output.items():
            chunk = uintBits[bitsIdx:bitsIdx+4]
            if type == 'int':
                res[name] = struct.unpack('<i', chunk)[0]
            elif type == 'float':
                res[name] = struct.unpack('<f', chunk)[0]
            else:
                raise Exception("Invalid parameter type.")
            bitsIdx += 4 
        return res
