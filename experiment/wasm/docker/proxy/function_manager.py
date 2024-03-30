import gevent
import docker
import os
from function_info import parse
from port_controller import PortController
from function import Function
import requests 

min_port = 20000
repack_clean_interval = 5.000 # repack and clean every 5 seconds
watch_interval = 0.004
dispatch_interval = 0.005 # 200 qps at most

# the class for scheduling functions' inter-operations
class FunctionManager:
    def __init__(self, watch_container_num=False):
        self.watch_container_num = watch_container_num
        self.function_info = parse()

        self.port_controller = PortController(min_port, min_port + 4999)
        self.client = docker.from_env()
        self.functions = {
            x.function_name: Function(self.client, x, self.port_controller)
            for x in self.function_info
        }

        self.init()
       
    def init(self):
        print("Clearing previous containers.")
        os.system('docker rm -f $(docker ps -aq --filter label=dockerContainer)')

        gevent.spawn_later(repack_clean_interval, self._clean_loop)
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)
        if self.watch_container_num:
            gevent.spawn_later(watch_interval, self._watch_loop)
            
    def _watch_loop(self):
        gevent.spawn_later(watch_interval, self._watch_loop)
        for function in self.functions.values():
            # print("[manager] cleaning function {}'s workers.".format(name))
            gevent.spawn(function.watchContainer)
    
    def _clean_loop(self):
        gevent.spawn_later(repack_clean_interval, self._clean_loop)
        for function in self.functions.values():
            gevent.spawn(function.cleanWorker)

    def _dispatch_loop(self):
        gevent.spawn_later(dispatch_interval, self._dispatch_loop)
        for function in self.functions.values():
            gevent.spawn(function.dispatchRequest)

    def clear_containers(self, funcNames):
        for name in funcNames:
           gevent.spawn(self.functions[name].cleanWorker, True)
    
    def run(self, function_name, parameter):
        # print('run', function_name, request_id, runtime, input, output, to, keys)
        if function_name not in self.functions:
            raise Exception("No such function!")
        res = self.functions[function_name].sendRequest(parameter)
        return res['res'], res['timeStamps']
