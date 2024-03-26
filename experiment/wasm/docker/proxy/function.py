import logging
import time
import math
from gevent import event
from gevent.lock import BoundedSemaphore
from container import Container
from function_info import FunctionInfo

# data structure for request info
class RequestInfo:
    def __init__(self, request_id, data):
        self.data = data
        self.result = event.AsyncResult()

# manage a function's container poolimport logging
import time
import yaml
import sys
from gevent import event
from gevent.lock import BoundedSemaphore
from container import Container

# data structure for request info
class RequestInfo:
    def __init__(self, data):
        self.data = data
        self.result = event.AsyncResult()

class Function:
    def __init__(self, client, functionInfo:FunctionInfo, port_controller):
        self.client = client
        self.requestQueue = []
        self.numOfContainer = []
        self.info = functionInfo
        self.numOfProcessingReq = 0
        self.workerLock = BoundedSemaphore()
        self.workerPool = []
        self.numOfWorkingWorkers = 0
        self.port_controller = port_controller

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
        req = self.requestQueue.pop(0)
        self.numOfProcessingReq -= 1
     
        # reqtime after container is ready.
        timeStamps.append(time.time())
        res = worker.send_request(req.data)
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
            logging.info('get worker from pool of function %s. pool size %d.', self.info.function_name, len(self.workerPool))
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
        if self.numOfWorkingWorkers + len(self.workerPool) > self.info.max_workers:
            logging.info('hit worker limit, function: %s', self.info.function_name)
            return None
        self.workerLock.release()

        # logging.info('create worker of function: %s', self.info.name)
        try:
             worker = Container.create(self.client, self.info.img_name, self.port_controller.get(), 'exec')
            # worker = tmpWorker(self.info.funcName, self.info.wasmCodePath)
        except Exception as e:
            print(e)
            return None
        self.init_worker(worker)
        print(f"create a container of funcion {self.info.function_name}.")
        self.numOfWorkingWorkers += 1
        return worker

    def removeWorker(self, worker):
        logging.info('remove worker: %s, pool size: %d', self.info.function_name, len(self.workerPool))
        worker.destroy()
        self.port_controller.put(worker.port)

    def init_worker(self, container):
        container.init(self.info.function_name)

def cleanPool(workerPool, expireTime, expiredWorkers):
    curTime = time.time()
    idx = -1
    for i, worker in enumerate(workerPool):
        if curTime - worker.lasttime < expireTime:
            idx = i
            break
    if idx < 0:
        idx = len(workerPool)
    expiredWorkers.extend(workerPool[:idx])
    return workerPool[idx:]