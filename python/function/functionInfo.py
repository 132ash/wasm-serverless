import sys
sys.path.append('./config')
sys.path.append('./storage')
import config
import yaml

SINGLEFUNCYAMLPATH = config.SINGLEFUNCYAMLPATH

class FunctionInfo:
    def __init__(self, funcName):
        funcYamlData = yaml.load(open(SINGLEFUNCYAMLPATH+'/'+funcName+'.yaml'), Loader=yaml.FullLoader)
        self.name = funcYamlData['name']
        self.wasmCodePath = funcYamlData.get('wasmCodePath', '') 
        self.maxWorkers = funcYamlData['maxWorkers']
        self.expireTime = funcYamlData['expireTime']
        self.imageName = funcYamlData.get('imageName', '')
        self.containerType = funcYamlData['containerType']
        self.input = {}
        self.output = {}
        self.outputSize = 0
        self.maxOutputStrSize = funcYamlData.get("maxStringSize", 0)
        outputStrNum = 0
        for param in funcYamlData['input']:
            self.input[param['name']] = param['type']
        for param in funcYamlData['output']:
            if param['type'] == 'string':
                outputStrNum += 1
            elif param['type'] == 'double':
                self.outputSize += 8
            else:
                self.outputSize += 4
            self.output[param['name']] = param['type']
        self.outputSize += self.maxOutputStrSize * outputStrNum
        self.wasmParam = {"wasmCodePath":self.wasmCodePath, 'outputSize':self.outputSize}
        self.dockerParam = {'imageName': self.imageName}
