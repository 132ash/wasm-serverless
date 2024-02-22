from functionWorker import FunctionWorker

class FunctionManager:
    def __init__(self):
        self.functions = {}
    def createFunction(self, funcName, wasmCodePath):
        worker = FunctionWorker(funcName, wasmCodePath)
        worker.startWorker()
        self.functions[funcName] = worker
    def runFunction(self, functionName, argc, argv):
        worker = self.functions[functionName]
        res = worker.run(argc, argv)
        return res
    def deleteFunction(self, funcName):
        self.functions.pop(funcName)
