import sys

sys.path.append('./config')
sys.path.append('./storage')
import config
from repository import Repository


class WorkflowManager:
    def __init__(self, workflowName, functionManager):
        self.workflowName = workflowName
        self.functionManager = functionManager
        repo = Repository()
        self.workflowInfo = repo.getWorkflowInfo(workflowName)

    def runWorkflow(self, parameters):
        startFunction = self.workflowInfo['startFunction']['name']
        res = self.runFunction(startFunction, parameters)
        return res
        
    def deleteWorkflow(self, workflowName):
        repo = Repository()
        repo.deleteWorkflowInfo(workflowName)

    def runFunction(self, funcName, parameters):
        funcType = self.workflowInfo['type'][funcName]
        if funcType == 'NORMAL':
            res = self.runNormalFunction(funcName, parameters)
        if funcType == 'SWITCH':
            res = self.runSwitchFunction(funcName, parameters)
        if funcType == 'END':
            res = self.runEndFunction(parameters)
        return res
    
    def runNormalFunction(self, funcName, parameters):
        res = self.functionManager.runFunction(funcName, parameters)
        next = self.workflowInfo['next'][funcName][0]
        print("normal function {} result: {}".format(funcName, res))
        return self.runFunction(next, res)
    
    def runSwitchFunction(self, funcName, input):
        output = self.workflowInfo['switchFunction'][funcName]['output']
        condition = self.workflowInfo['switchFunction'][funcName]['condition']
        if eval(condition):
            next = self.workflowInfo['next'][funcName][0]
        else:
            next = self.workflowInfo['next'][funcName][1]
        paramOut = {}
        for param in output:
            paramOut[param] = input[param]
        return self.runFunction(next, paramOut)
    
    def runEndFunction(self, parameters):
        output = self.workflowInfo['endFunction']['output']
        res = {}
        for param in output:
            res[param] = parameters[param]
        print("end function result: {}".format(res))
        return res

       

        


