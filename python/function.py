import logging
import time
import yaml
import sys
sys.path.append('./config')
sys.path.append('./storage')
import config
from gevent import event
from gevent.lock import BoundedSemaphore
from functionWorker import FunctionWorker

SINGLEFUNCYAMLPATH = config.SINGLEFUNCYAMLPATH

# data structure for request info
class RequestInfo:
    def __init__(self, data):
        self.data = data
        self.result = event.AsyncResult()

class FunctionInfo:
    def __init__(self, funcName):
        funcYamlData = yaml.load(open(SINGLEFUNCYAMLPATH+'/'+funcName+'.yaml'), Loader=yaml.FullLoader)
        self.name = funcYamlData['name']
        self.wasmCodePath = funcYamlData['wasmCodePath']
        self.maxWorkers = funcYamlData['maxWorkers']
        self.expireTime = funcYamlData['expireTime']
        self.input = {}
        self.output = {}
        for param in funcYamlData['input']:
            self.input[param['name']] = param['type']
        self.output['name'] = funcYamlData['output']['name']
        self.output['type'] = funcYamlData['output']['type']



class Function:
    def __init__(self, functionInfo:FunctionInfo):
        self.requestQueue = []
        self.info = functionInfo
        self.numOfProcessingReq = 0
        self.workerLock = BoundedSemaphore()
        self.workerPool = []
        self.numOfWorkingWorkers = 0

    def sendRequest(self, data):
        req = RequestInfo(data)
        self.requestQueue.append(req)
        res = req.result.get()
        return res

    def dispatchRequest(self):
        # no req to be processed.
        if len(self.requestQueue) - self.numOfProcessingReq == 0:
            # print("no req to be processed.")
            return 
        self.numOfProcessingReq += 1
        # print("processing request num:{}".format(self.numOfProcessingReq))
        worker = self.acquireWorker()
        while worker is None:
            worker = self.createWorker()
        if worker is None:
            self.numOfProcessingReq -= 1
            return
        req = self.requestQueue.pop(0)
        self.numOfProcessingReq -= 1
        # 2. send request to the container
        # print("request data:{}".format(req.data))
        res = worker.run(req.data)
        # print("[function] set result in Request.res:{}".format(res))
        req.result.set(res)
        # 3. put the worker back into pool
        self.returnWorker(worker)

    def cleanWorker(self):
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
            logging.info('get worker from pool of function %s. pool size %d.', self.info.name, len(self.workerPool))
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
        self.numOfWorkingWorkers += 1
        self.workerLock.release()

        logging.info('create worker of function: %s', self.info.name)
        try:
            worker = FunctionWorker(self.info.name, self.info.wasmCodePath)
            # worker = tmpWorker(self.info.funcName, self.info.wasmCodePath)
        except Exception as e:
            print(e)
            self.numOfWorkingWorkers -= 1
            return None
        worker.startWorker()
        return worker

    def removeWorker(self, worker):
        del worker

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



