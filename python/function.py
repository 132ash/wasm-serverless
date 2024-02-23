import logging
from gevent import event
from gevent.lock import BoundedSemaphore
from functionWorker import FunctionWorker

# data structure for request info
class RequestInfo:
    def __init__(self, data):
        self.data = data
        self.result = event.AsyncResult()

    def constructParam(self):
        argc = len(self.data)
        argv = str(argc) + " " + ' '.join(map(str, self.data)) + '\n'
        return argc, argv
    

class FunctionInfo:
    def __init__(self, funcName, wasmCodePath, maxWorkers = 10):
        self.funcName = funcName
        self.wasmCodePath = wasmCodePath
        self.maxWorkers = maxWorkers


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
            print("no req to be processed.")
            return 
        self.numOfProcessingReq += 1
        worker = self.acquireWorker()
        while worker is None:
            worker = self.createWorker()
        if worker is None:
            self.numOfProcessingReq -= 1
            return None
        req = self.requestQueue.pop(0)
        self.numOfProcessingReq -= 1
        # 2. send request to the container
        argc, argv = req.constructParam()
        logging.info('run code in worker.')
        res = worker.run(argc, argv)
        req.result.set(res)
        print("[function] set result in Request.")
        
        # 3. put the worker back into pool
        self.returnWorker(worker)

    def acquireWorker(self):
        res = None
        self.workerLock.acquire()
        if len(self.workerPool) != 0:
            logging.info('get worker from pool of function %s. pool size %d.', self.info.funcName, len(self.workerPool))
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
            logging.info('hit worker limit, function: %s', self.info.funcName)
            return None
        self.numOfWorkingWorkers += 1
        self.workerLock.release()

        logging.info('create worker of function: %s', self.info.funcName)
        try:
            # worker = FunctionWorker(self.info.funcName, self.info.wasmCodePath)
            worker = tmpWorker(self.info.funcName, self.info.wasmCodePath)
        except Exception as e:
            print(e)
            self.numOfWorkingWorkers -= 1
            return None
        worker.startWorker()
        return worker

    def removeWorker(self):
        pass

class tmpWorker:
    def __init__(self, funcName, wasmCodePath):
        self.funcName = funcName
        self.wasmCodePath = wasmCodePath
    def startWorker(self):
        print("loaded wasm code at {}.".format(self.wasmCodePath))
    def run(self, argc, argv):
        print("run function {}. argc: {}, argv:{}".format(self.funcName, argc, argv))
        return 1
    def __del__(self):
        print("worker deleted.")
     
def waitEventRes(funcName, manager):
    req = RequestInfo([1,2])
    manager[funcName].requestQueue.append(req)
    res = req.result.get()
    print("[client] get function res:{}, type:{}".format(res, type(res)))


if __name__ == "__main__":
    funcName = "funcTest"
    wasmCodePath = "/test.wasm"
    maxWorkers = 10
    req = RequestInfo([1,2])

    easyManager = {}

    info = FunctionInfo(funcName, wasmCodePath, maxWorkers)
    easyManager[funcName] = Function(info)

    waitEventRes(funcName, easyManager)

    easyManager[funcName].dispatchRequest()



