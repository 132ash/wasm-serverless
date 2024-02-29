import yaml
import sys
sys.path.append('../config')
sys.path.append('../storage')
sys.path.append('..')
import config
from testFuncs import Runner
SINGLEFUNCYAMLPATH = config.SINGLEFUNCYAMLPATH

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
    def __init__(self, info):
        self.info = info
        self.runner = Runner()

    def sendRequest(self, param):
        return self.runner.run(self.info.name, param)


