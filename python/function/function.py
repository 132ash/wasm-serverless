import logging
import time
import yaml
import signal
import couchdb
import sys
sys.path.append('./config')
sys.path.append('./storage')
sys.path.append('./workflow')
import config
from gevent import event
from gevent.lock import BoundedSemaphore
from Worker import FunctionWorker
from functionInfo import FunctionInfo

COUCH_URL = config.COUCH_DB_URL
DATA_TRANSFER_DB = config.DATA_TRANSFER_DB

# data structure for request info
class RequestInfo:
    def __init__(self, data):
        self.data = data
        self.result = event.AsyncResult()

class stringRepo:
    def __init__(self):
        self.couch = couchdb.Server(COUCH_URL)

    def fetchString(self, size):
        sizes =  ['1KB', '10KB', '1MB']
        if size not in sizes:
            raise ValueError("size must be one of {sizes}.")
        doc = self.couch[DATA_TRANSFER_DB][size]
        if 'content' in doc:
            return doc['content']
        
class Function:
    def __init__(self, functionInfo:FunctionInfo, client, port_controller, heapSize=1024 * 1024 * 10):
        self.requestQueue = []
        self.numOfContainer = []
        self.info = functionInfo
        self.numOfProcessingReq = 0
        self.workerLock = BoundedSemaphore()
        self.workerPool = []
        self.heapSize = heapSize
        self.numOfWorkingWorkers = 0
        self.port_controller = port_controller
        self.wasmParam = self.info.wasmParam
        self.dockerParam = self.info.dockerParam
        self.wasmParam['heapSize'] = heapSize
        self.dockerParam['client'] = client

    def sendRequest(self, data):
        req = RequestInfo(data)
        self.requestQueue.append(req)
        res = req.result.get()
        return res
    
    def watchContainer(self):
        if self.numOfWorkingWorkers == 0:
            return
        self.numOfContainer.append((time.time(), self.numOfWorkingWorkers))

    def dispatchRequest(self):
        timeStamps = []
        # no req to be processed.
        if len(self.requestQueue) - self.numOfProcessingReq == 0:
            # print("no req to be processed.")
            return 
        self.numOfProcessingReq += 1
        # reqtime before container is ready.
        timeStamps.append(time.time())
        worker = self.acquireWorker()
        while worker is None:
            worker = self.createWorker()
        if worker is None:
            self.numOfProcessingReq -= 1
            return
        print(f'get worker. working worker: {self.numOfWorkingWorkers}.')
        req = self.requestQueue.pop(0)
        self.numOfProcessingReq -= 1
        
        # reqtime after container is ready.
        timeStamps.append(time.time())
        res = worker.run(req.data)
        # print("[function] set result in Request.res:{}".format(res))
        req.result.set({'res':res, 'timeStamps':timeStamps})
        # 3. put the worker back into pool
        self.returnWorker(worker)

    def cleanWorker(self, force=False):
        if force:
            self.workerLock.acquire()
            for worker in self.workerPool:
                self.removeWorker(worker)
            self.workerPool = []
            self.workerLock.release()
            return
        # print("[before cleaning]: num of workers:{}".format(len(self.workerPool)))
        expiredWorkers = []
        self.workerLock.acquire()
        self.workerPool = cleanPool(self.workerPool, self.info.expireTime, expiredWorkers)
        self.workerLock.release()

        for worker in expiredWorkers:
            self.removeWorker(worker)
        # print("[after cleaning]: num of workers:{}".format(len(self.workerPool)))

    def acquireWorker(self):
        res = None
        self.workerLock.acquire()
        if len(self.workerPool) != 0:
            res = self.workerPool.pop(-1)
            self.numOfWorkingWorkers += 1 
        self.workerLock.release()
        return res

    def returnWorker(self, worker):
        self.workerLock.acquire()
        self.workerPool.append(worker)
        self.numOfWorkingWorkers -= 1
        self.workerLock.release()

    ''' 
    create a worker and make it run, return the worker.
    '''
    def createWorker(self):
        self.workerLock.acquire()
        if self.numOfWorkingWorkers + len(self.workerPool) > self.info.maxWorkers:
            logging.info('hit worker limit, function: %s', self.info.name)
            return None
        self.workerLock.release()

        # logging.info('create worker of function: %s', self.info.name)
        try:
            worker = FunctionWorker(self.info, self.port_controller.get(self.info.containerType), self.info.containerType, self.wasmParam, self.dockerParam)
            # worker = tmpWorker(self.info.funcName, self.info.wasmCodePath)
        except Exception as e:
            print(e)
            return None
        worker.startWorker()
        self.numOfWorkingWorkers += 1
        return worker

    def removeWorker(self, worker:FunctionWorker):
        worker.destroy()
        self.port_controller.put(worker.port, self.info.containerType)

def cleanPool(workerPool, expireTime, expiredWorkers):
    curTime = time.time()
    idx = -1
    for i, worker in enumerate(workerPool):
        if curTime - worker.lastTriggeredTime < expireTime:
            idx = i
            break
    if idx < 0:
        idx = len(workerPool)
    expiredWorkers.extend(workerPool[:idx])
    return workerPool[idx:]


# class tmpWorker:
#     def __init__(self, funcName, wasmCodePath):
#         self.funcName = funcName
#         self.wasmCodePath = wasmCodePath
#     def startWorker(self):
#         print("loaded wasm code at {}.".format(self.wasmCodePath))
#     def run(self, argc, argv):
#         print("run function {}. argc: {}, argv:{}".format(self.funcName, argc, argv))
#         return 1
#     def __del__(self):
#         print("worker deleted.")
     
# def waitEventRes(funcName, manager):
#     req = RequestInfo([1,2])
#     manager[funcName].requestQueue.append(req)
#     res = req.result.get()
#     print("[client] get function res:{}, type:{}".format(res, type(res)))


# if __name__ == "__main__":
#     funcName = "funcTest"
#     wasmCodePath = "/test.wasm"
#     maxWorkers = 10
#     req = RequestInfo([1,2])

#     easyManager = {}

#     info = FunctionInfo(funcName, wasmCodePath, maxWorkers)
#     easyManager[funcName] = Function(info)

#     waitEventRes(funcName, easyManager)

#     easyManager[funcName].dispatchRequest()



