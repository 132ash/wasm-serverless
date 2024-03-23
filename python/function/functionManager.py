import gevent
import json
import couchdb
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
        res = func.sendRequest(data)
        return self.constructOutput(res, func.info)
    
    def deleteFunction(self, funcName):
        if funcName in self.functions:
            self.functions.pop(funcName)

    def _dispatch_loop(self):
        # print("[manager] new dispatch loop.")
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)
        for function in self.functions.values():
            # print("[manager] dispatch function {}'s request.".format(name))
            gevent.spawn(function.dispatchRequest)

    def _clean_loop(self):
        # print("[manager] new clean loop.")
        gevent.spawn_later(repack_clean_interval, self._clean_loop)
        for function in self.functions.values():
            # print("[manager] cleaning function {}'s workers.".format(name))
            gevent.spawn(function.cleanWorker)
        
    def constructOutput(self, funcRes, info):
        res = {}
        timeStamps = funcRes['timeStamps']
        bitsIdx = 0
        uintBits = funcRes['res']
        for name, type in info.output.items():
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
        return res, timeStamps
