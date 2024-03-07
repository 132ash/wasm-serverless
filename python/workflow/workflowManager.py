import sys

sys.path.append('./config')
sys.path.append('./storage')
import config
import requests
import gevent
import gevent.lock
from typing import Any, Dict, List
from repository import Repository

repo = Repository()

def condExec(cond: str, param: dict) -> Any:
    if cond.startswith('default'):
        return True    
    return eval(cond, param)    

class WorkflowState:
    def __init__(self, requestId: str, all_func: List[str]):
        self.request_id = requestId
        self.lock = gevent.lock.BoundedSemaphore() # guard the whole state
        self.funcRes = {}

        self.executed: Dict[str, bool] = {}
        self.parentExecuted: Dict[str, int] = {}
        for f in all_func:
            self.funcRes[f] = {}
            self.executed[f] = False
            self.parentExecuted[f] = 0


class WorkflowManager:
    def __init__(self, hostAddr, workflowName, functionManager):
        self.hostAddr = hostAddr
        self.lock = gevent.lock.BoundedSemaphore() # guard self.states
        self.workflowName = workflowName
        self.functionManager = functionManager
        self.infoDB = workflowName + '_function_info'
        self.functionInfo: Dict[str, dict] = {}
        self.states: Dict[str, WorkflowState] = {}
        self.funcNames = repo.getWorkflowFunctions(workflowName)
        

    def getState(self, request_id: str) -> WorkflowState:
        self.lock.acquire()
        if request_id not in self.states:
            self.states[request_id] = WorkflowState(request_id, self.func)
        state = self.states[request_id]
        self.lock.release()
        return state
    
    def getFunctionInfo(self, functionName: str) -> Any:
        if functionName not in self.functionInfo:
            self.functionInfo[functionName] = repo.getFunctionInfo(functionName, self.workflowName)
        return self.functionInfo[functionName]

    # def runWorkflow(self, parameters):
    #     startFunction = self.workflowInfo['startFunction']['name']
    #     res = self.runFunction(startFunction, parameters)
    #     return res
        
    # def deleteWorkflow(self, workflowName):
    #     repo = Repository()
    #     repo.deleteWorkflowInfo(workflowName)

    def triggerFunction(self, state: WorkflowState, functionName: str, parameters:dict, noParentExecution = False) -> None:
        funcInfo = self.getFunctionInfo(functionName)
        if funcInfo['ip'] == self.hostAddr:
            # function runs on local
            self.triggerFunctionLocal(state, functionName, parameters, noParentExecution)
        else:
            # function runs on remote machine
            self.triggerFunctionRemote(state, functionName, funcInfo['ip'], parameters, noParentExecution)


    def triggerFunctionLocal(self, state: WorkflowState, function_name: str, parameters:dict, noParentExecution = False) -> None:
        state.lock.acquire()
        if not noParentExecution:
            state.parentExecuted[function_name] += 1
        runnable = self.checkRunnable(state, function_name)
        # remember to release state.lock
        if runnable:
            state.executed[function_name] = True
            state.lock.release()
            self.runFunction(state, function_name, parameters)
        else:
            state.lock.release()

    # trigger a function that runs on remote machine
    def triggerFunctionRemote(self, state: WorkflowState, function_name: str, remote_addr: str, parameters:dict, no_parent_execution = False) -> None:
        remote_url = 'http://{}/workflow/request'.format(remote_addr)
        data = {
            'requestId': state.request_id,
            'workflowName': self.workflowName,
            'funcName': function_name,
            'noParentExecution': no_parent_execution,
            'parameters': parameters
        }
        response = requests.post(remote_url, json=data)
        response.close()

    def checkRunnable(self, state: WorkflowState, function_name: str) -> bool:
        info = self.getFunctionInfo(function_name)
        return state.parentExecuted[function_name] == info['parent_cnt'] and not state.executed[function_name]


    def runFunction(self, state:WorkflowState, funcName, parameters):
        info = self.getFunctionInfo(funcName)
        source = info['source']
        if source == 'VIRTUAL':
            self.runSwitchFunction(info, state, parameters)
            return
        if source == 'END':
            self.runEndFunction(info, state, parameters) 
            return 
        self.runNormalFunction(state, funcName, parameters)
        jobs = [
            gevent.spawn(self.triggerFunction, state, func, state.funcRes[funcName])
            for func in info['next']
        ]
        gevent.joinall(jobs)
    
    def runNormalFunction(self, state:WorkflowState, funcName, parameters):
        res = self.functionManager.runFunction(funcName, parameters)
        state.funcRes[funcName] = res
    
    def runSwitchFunction(self, info, state:WorkflowState, parameters):
        for i, next_func in enumerate(info['next']):
            cond = info['conditions'][i]
            if condExec(cond, parameters):
                self.triggerFunction(state, next_func, parameters)
                break
    
    def runEndFunction(self, info, state:WorkflowState, parameters):
        output = info[output]
        reqID = state.request_id
        res = {}
        for param in output:
            res[param] = parameters[param]
        repo.saveWorkflowRes(reqID, res)
        print("end function result: {}".format(res))

       

        


