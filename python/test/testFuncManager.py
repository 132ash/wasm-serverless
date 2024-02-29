import sys
import yaml
import json
import struct
sys.path.append('./config')
sys.path.append('./storage')
import config
from repository import Repository
from functionTest import FunctionInfo, Function

SINGLEFUNCYAMLPATH = config.SINGLEFUNCYAMLPATH

class FunctionManager:
    def __init__(self):
        self.functions = {}
        # self.repo = Repository()

    def createFunction(self, funcName):
        info = FunctionInfo(funcName)
        function = Function(info)
        self.functions[funcName] = function
        
        # self.repo.saveFunctionInfo(info.funcName, info)

    # param: in dict
    def runFunction(self, funcName, data:dict):
        if funcName not in self.functions:
            raise Exception("No such function!")
        func = self.functions[funcName]
        param = self.constructInput(data)
        # transform parameter
        res = func.sendRequest(param)
        return self.constructOutput(res, func.info)
    
    def deleteFunction(self, funcName):
        self.functions.pop(funcName)
        # self.repo.deleteFunctionInfo(funcName)

    def constructInput(self, param):
        return json.dumps(param) + '\n'
        
    def constructOutput(self, uintBits, info):
        resType = info.output['type']
        resName = info.output['name']
        res = {}
        if resType == 'int':
            res[resName] = struct.unpack('<i', uintBits)[0]
        else:
            if resType == 'float':
                res[resName] = struct.unpack('<f', uintBits)[0]
            else:
                raise Exception("Invalid parameter type.")
        return res
    
if __name__ == "__main__":
    manager = FunctionManager()
    param = {"sub1":2, "sub2":3}
    manager.createFunction('sub')
    print(manager.runFunction('sub', param))
        