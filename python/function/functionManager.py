import gevent
from portController import PortController
import struct
import docker
import os

from function import Function, FunctionInfo, RequestInfo
from typing import Any, Dict, List

dispatch_interval = 0.005
watch_interval = 0.004
repack_clean_interval = 5.000
min_port = 30000

class FunctionManager:
    def __init__(self, watch_container_num=False):
        print("Clearing previous docker containers.")
        os.system('docker rm -f $(docker ps -aq --filter label=dockerContainer)')
        self.functions: Dict[str, Function] = {} 
        self.portController = PortController(min_port, min_port+4999, min_port+5000, min_port+10000)
        self.client = docker.from_env()
        gevent.spawn_later(repack_clean_interval, self._clean_loop)
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)
        if watch_container_num:
            gevent.spawn_later(watch_interval, self._watch_loop)

    def createFunction(self,funcName,heapSize=1024 * 1024 * 10):
        info = FunctionInfo(funcName)
        function = Function(info, self.client, self.portController, heapSize)
        self.functions[funcName] = function

    def runFunction(self, funcName:str, data:dict):
        if funcName not in self.functions:
            raise Exception(f"No such function: {funcName}, function list:{list(self.functions.keys())}!")
        func = self.functions[funcName]
        rawRes = func.sendRequest(data)
        return rawRes['res'], rawRes['timeStamps']
    
    def deleteFunction(self, funcName):
        if funcName in self.functions:
            function = self.functions[funcName]
            function.cleanWorker(force=True)
            self.functions.pop(funcName)

    def _watch_loop(self):
        gevent.spawn_later(watch_interval, self._watch_loop)
        for function in self.functions.values():
            # print("[manager] cleaning function {}'s workers.".format(name))
            gevent.spawn(function.watchContainer)

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
 
