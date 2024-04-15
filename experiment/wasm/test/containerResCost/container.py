import os
import signal
import sys
import time
import psutil
import json
import gevent
import struct
import requests
import threading
import base64
import info
import subprocess

DOCKER_FILE_PATH = info.DOCKER_FILE_PATH
WASM_FILE_PATH = info.WASM_FILE_PATH

base_url = 'http://127.0.0.1:{}/{}'

proxyPath = "/home/ash/wasm/wasm-serverless/experiment/wasm/test/containerResCost/wasmProxy.py"

# def preexec_function():
#     # 将子进程的进程组 ID 设置为其自身的 PID
#     os.setpgrp()



class Container:
    def __init__(self, funcName, port, type, client):
        self.type = type
        self.funcName = funcName
        self.port = port
        self.client = client
        if self.type == 'wasm':
            self.worker = wasmWorker(funcName, port, info.wasmPath[funcName], info.outPutSize)
        elif self.type == 'docker':
            if info.dockerFunctype != 'python':
                self.worker = dockerWorker(funcName, client, info.imageName[funcName], port)
            else:
                self.worker = dockerWorker(funcName, client, info.imageName_py[funcName], port)
        
    def startWorker(self):
        self.worker.startWorker()
        
    def run(self,param):
        res = self.worker.run(param)
        self.lastTriggeredTime = time.time()
        return res
        # print("run function {}. param:{}".format(self.funcName, param))
    
    def destroy(self):
        # print(f"{self.funcName}'s worker delete. pid:{self.workerProcess}")
        self.worker.destroy()

    def writeMaxMem(self):
        self.worker.writeMaxMem()


class wasmWorker:
    def __init__(self, funcName, port, wasmCodePath='', outputSize=0, heapSize = 1024*1024*10):
        self.workerProcess = None
        self.funcName = funcName
        self.wasmCodePath = wasmCodePath
        self.heapSize = heapSize
        self.outputSize = outputSize
        self.lastTriggeredTime = 0
        self.port = port
        self.maxMem = 0

    def startWorker(self):
        self.workerProcess = subprocess.Popen(["python", proxyPath, str(self.port)],stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, start_new_session=True)
        self.waitStart()
        initParam = {"wasmCodePath":self.wasmCodePath,'funcName':self.funcName,'outputSize':self.outputSize, "heapSize":self.heapSize}
        r = requests.post(base_url.format(self.port, 'init'), json=initParam)
        # print(f"{self.funcName}'s worker {self.workerProcess.pid} start on port {self.port}.")
        # # print(r.json())
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

    def monitor_container_memory(self):
        """
        监控Wasm容器的最大内存使用量。
        """
        max_memory_usage = 0
        start = time.time()
        while True:  
            total_memory = 0     
            try:
                p = psutil.Process(self.workerProcess.pid)
                # 计算主进程的内存使用
                # total_memory += p.memory_info().rss / (1024 * 1024)
                # print(total_memory)
                for child in p.children(recursive=True):
                    print(p)
                    try:
                        total_memory += child.memory_info().rss / (1024 * 1024)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                max_memory_usage = max(max_memory_usage, total_memory)
                print("all process.")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
            if time.time() - start >= 6:
                break
            time.sleep(0.01)  # 短暂休眠以减少CPU占用
        self.maxMem = max(self.maxMem, max_memory_usage)
        # return max_memory_usage

    # send a request to container and wait for result
    def run(self, data = {}):
        response_list = []
        request_thread = threading.Thread(target=self.send_request, args=(data, response_list))
        request_thread.start() 
        self.monitor_container_memory()
        return response_list[0]
    
    def writeMaxMem(self):
        with open(WASM_FILE_PATH, 'a') as f:
            f.write(self.funcName+":"+str(self.maxMem)+'\n')

    def send_request(self, param, response_list):
        data = self.constructInput(param)
        postProxyTime = time.time()
        r = requests.post(base_url.format(self.port, 'run'), json={"parameters":data})
        res, wasmTimeStamp = self.constructOutput(base64.b64decode(r.json()["out"]))
        res["postProxyTime"] = postProxyTime
        res["wasmTimeStamp"] = wasmTimeStamp
        response_list.append(res)
 
    def destroy(self):
        # print(f"delete {self.funcName}'s worker. pid:{self.workerProcess.pid}")
        pid = self.workerProcess.pid
        if psutil.pid_exists(pid):
            os.killpg(pid, signal.SIGKILL)
        else:
            print(f"{self.funcName}'s worker {self.workerProcess.pid} doesn't exist.")


    def constructInput(self, data):
        param = {}
        prefix = 1
        for name, _ in info.input[self.funcName].items():
            param[str(prefix)+name] = data[name]
            prefix += 1
        return json.dumps(param) + '\n'
    
    def constructOutput(self, uintBits):
        res = {}
        wasmTimeStamps = []
        bitsIdx = 0
        for name, type in info.output[self.funcName].items():
            if type == 'string':
                start = bitsIdx 
                while uintBits[bitsIdx] != 0:
                    bitsIdx += 1
                res[name] = uintBits[start:bitsIdx].decode("ISO-8859-1")
                bitsIdx += 1
            elif type == 'long long':
                chunk = uintBits[bitsIdx:bitsIdx+8]
                res[name] = int.from_bytes(chunk, 'little')
                bitsIdx += 8
            elif type == 'double':
                chunk = uintBits[bitsIdx:bitsIdx+8]
                res[name] = struct.unpack('<d', chunk)[0]
                bitsIdx += 8
            else:
                chunk = uintBits[bitsIdx:bitsIdx+4]
                if type == 'int':
                    res[name] = struct.unpack('<i', chunk)[0]
                elif type == 'float':
                    res[name] = struct.unpack('<f', chunk)[0]
                bitsIdx += 4 
        bitsIdx = self.outputSize
        for _ in range(4):
            chunk = uintBits[bitsIdx:bitsIdx+8]
            wasmTimeStamps.append(int.from_bytes(chunk, 'little'))
            bitsIdx += 8
        return res, wasmTimeStamps


class dockerWorker:

    def __init__(self, funcName, client, image_name, port):
        self.client = client
        self.funcName = funcName
        self.image_name = image_name
        self.port = port
        self.attr = 'exec'
        self.funcName = funcName
        self.maxMem = 0
        self.lasttime = -1

    def startWorker(self):
        self.lasttime = time.time()
        self.container  = self.client.containers.run(self.image_name,
                                                    detach=True,
                                                    ports={'5000/tcp': str(self.port)},
                                                    labels=['dockerContainer'])
        self.waitStart()
        self.init()

    # wait for the container cold start
    def waitStart(self):
        while True:
            try:
                r = requests.get(base_url.format(self.port, 'status'))
                if r.status_code == 200:
                    break
            except Exception:
                pass
            gevent.sleep(0.005)

    def send_request(self, data, response_list):
        """
        发送POST请求的线程函数。
        """
        response = requests.post(base_url.format(self.port, 'run'), json=data)
        response_list.append(response.json())  # 存储响应数据供主线程访问

    def monitor_container_memory(self, request_thread):
        """
        监控Docker容器的最大内存使用量。
        """
        max_memory_usage = 0
        start = time.time()
        while True:
            stats = self.container.stats(stream=False)
            current_memory_usage = stats['memory_stats']['usage']
            max_memory_usage = max(max_memory_usage, current_memory_usage)
            
            self.container.reload()  # 刷新容器状态
            if not request_thread.is_alive():
                break  # 如果容器不再运行，终止监控
            
            time.sleep(0.01)  # 短暂休眠以减少CPU占用
            if time.time() - start >= 6:
                break
        self.maxMem = max(self.maxMem, max_memory_usage)
        # return max_memory_usage

    # send a request to container and wait for result
    def run(self, data = {}):
        response_list = []
        request_thread = threading.Thread(target=self.send_request, args=(data, response_list))
        request_thread.start() 
        self.monitor_container_memory(request_thread)
        return response_list[0]
    
    def writeMaxMem(self):
        with open(DOCKER_FILE_PATH, 'a') as f:
            f.write(self.funcName+":"+str(self.maxMem)+'\n')

    # initialize the container
    def init(self):
        data = {'function': self.funcName }
        r = requests.post(base_url.format(self.port, 'init'), json=data)
        self.lasttime = time.time()
        return r.status_code == 200

    # kill and remove the container
    def destroy(self):
        self.container.remove(force=True)
