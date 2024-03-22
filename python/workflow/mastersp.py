import sys
import logging
sys.path.append('./config')
sys.path.append('./storage')
import config
import requests
from datetime import datetime
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
    def __init__(self, requestId: str, functions: List[str]):
        self.request_id = requestId
        self.lock = gevent.lock.BoundedSemaphore() # guard the whole state
        self.funcRes = {}

        self.executed: Dict[str, bool] = {}
        self.parentExecuted: Dict[str, int] = {}
        for f in functions:
            self.funcRes[f] = {}
            self.executed[f] = False
            self.parentExecuted[f] = 0

class FunctionParameters:
    def __init__(self, requestId: str, functions: List[str]):
        self.request_id = requestId
        self.lock = gevent.lock.BoundedSemaphore() # guard the whole state
        self.funcParameters: Dict[str, dict]= {}
        for f in functions:
            self.funcParameters[f] = {}

    def setParam(self, funcName, param):
        self.lock.acquire()
        self.funcParameters[funcName].update(param)
        self.lock.release()

    def getParam(self, funcName):
        self.lock.acquire()
        param = self.funcParameters[funcName]
        self.lock.release()
        return param

class MasterSPManager:
    def __init__(self, hostAddr, workflowName, functionManager):
        self.hostAddr = hostAddr
        self.stateLock = gevent.lock.BoundedSemaphore() # guard self.states
        self.paramLock = gevent.lock.BoundedSemaphore() # guard self.funcParameters
        self.workflowName = workflowName
        self.functionManager = functionManager
        self.infoDB = workflowName + '_function_info'
        self.functionInfo: Dict[str, dict] = {}
        self.states: Dict[str, WorkflowState] = {} #{id: state}
        self.funcParameters: Dict[str, FunctionParameters] = {} #{id: param}
        self.funcNames = repo.getWorkflowFunctions(workflowName)[0]

    def setFunctionParam(self, request_id: str, funcName:str, param:dict):
        self.paramLock.acquire()
        if request_id not in self.funcParameters:
            self.funcParameters[request_id] =FunctionParameters(request_id, self.funcNames)
        self.paramLock.release()
        self.funcParameters[request_id].setParam(funcName, param)

    def getFunctionParam(self, request_id: str, funcName:str):
        return self.funcParameters[request_id].getParam(funcName)

    def getState(self, request_id: str) -> WorkflowState:
        self.stateLock.acquire()
        if request_id not in self.states:
            self.states[request_id] = WorkflowState(request_id, self.funcNames)
        state = self.states[request_id]
        self.stateLock.release()
        return state
    
    def getFunctionInfo(self, functionName: str) -> Any:
        if functionName not in self.functionInfo:
            self.functionInfo[functionName] = repo.getFunctionInfo(functionName, self.workflowName)
        return self.functionInfo[functionName]
    
    def delStateAndParamRemote(self, requestID: str, remoteAddr: str):
        url = 'http://{}/clear'.format(remoteAddr)
        requests.post(url, json={'requestID': requestID, 'workflowName': self.workflowName})

    # delete state
    def delStateAndParam(self, requestID: str, master: bool):
        logging.info('delete state and param of: %s', requestID)
        self.stateLock.acquire()
        if requestID in self.states:
            del self.states[requestID]
        self.stateLock.release()
        self.paramLock.acquire()
        if requestID in self.funcParameters:
            del self.funcParameters[requestID]
        self.paramLock.release()
        if master:
            jobs = []
            addrs = repo.getAllWorkerAddrs(self.workflowName)
            for addr in addrs:
                if addr != self.hostAddr:
                    jobs.append(gevent.spawn(self.delStateAndParamRemote, requestID, addr))
            gevent.joinall(jobs)

    def get_node_status(self, addr: str, status: Dict):
        url = f'http://{addr}/info'
        result = requests.get(url)
        status[addr] = result.json()

    # simulate dynamic node selecting
    def node_select(self):
        addrs = repo.getAllWorkerAddrs(self.workflowName)
        jobs = []
        status = {}
        for addr in addrs:
            jobs.append(gevent.spawn(self.get_node_status, addr, status))
        gevent.joinall(jobs)
        selected_addr = ''
        return selected_addr

    def triggerFunction(self, state: WorkflowState, functionName: str, parameters:dict, noParentExecution = False) -> None:
        funcInfo = self.getFunctionInfo(functionName)
        if funcInfo['ip'] == self.hostAddr:
            # function runs on local
            return self.triggerFunctionLocal(functionName, parameters)
        else:
            # function runs on remote machine
            self.triggerFunctionRemote(state, functionName, funcInfo['ip'], parameters, noParentExecution)
            return {}


    def triggerFunctionLocal(self, function_name: str, parameters:dict) -> None:
        print(f"[Workflow Manager] run local func {function_name} with param {parameters}.]")
        return self.runFunction(function_name, parameters)

    # trigger a function that runs on remote machine
    def triggerFunctionRemote(self, state: WorkflowState, function_name: str, remote_addr: str, parameters:dict, noParentExecution = False) -> None:
        print(f"[Workflow Manager] run remote func {function_name} on IP {remote_addr} with param {parameters}.]")
        state.lock.acquire()
        if not noParentExecution:
            state.parentExecuted[function_name] += 1
        runnable = self.checkRunnable(state, function_name)
        self.setFunctionParam(state.request_id, function_name, parameters)
        if runnable:
            state.executed[function_name] = True
            state.lock.release()
            self.node_select() #simulate node selection process.
            info = self.getFunctionInfo(function_name)
            source = info['source']
            if source == 'VIRTUAL':
                self.runSwitchFunction(info, state, parameters)
                return
            if source == 'END':
                self.runEndFunction(info, state, parameters) 
                return 
            remoteUrl = 'http://{}/workflow/request'.format(remote_addr)  
            data = {
                'requestId': state.request_id,
                'workflowName': self.workflowName,
                'functionName': function_name,
                'noParentExecution': noParentExecution,
                'parameters': self.getFunctionParam(state.request_id, function_name)
            }  
            response = requests.post(remoteUrl, json=data)
            res = response.json()['res']
            response.close()
            jobs = [
                    gevent.spawn(self.triggerFunction, state, func, res)
                    for func in info['next']
                ]
            gevent.joinall(jobs)
        else:
            state.lock.release()

    def checkRunnable(self, state: WorkflowState, function_name: str) -> bool:
        info = self.getFunctionInfo(function_name)
        return state.parentExecuted[function_name] == info['parent_cnt'] and not state.executed[function_name]


    def runFunction(self, funcName, parameters:dict):
        return self.runNormalFunction(funcName, parameters)
    
    def runNormalFunction(self, funcName, parameters):
        return self.functionManager.runFunction(funcName, parameters)[0]
       
    def runSwitchFunction(self, info, state:WorkflowState, parameters):
        output = info['output']
        selectedParam ={}
        for name in output:
            selectedParam[name] = parameters[name]
        for i, next_func in enumerate(info['next']):
            cond = info['conditions'][i]
            ctx = parameters.copy()
            if condExec(cond, ctx):
                self.triggerFunction(state, next_func, selectedParam)
                break
    
    # choose multiple(or single) params in parameters and construct output dict.
    def runEndFunction(self, info, state:WorkflowState, parameters:dict):
        output = info['output']
        reqID = state.request_id
        res = {}
        if len(output) == 1:
            for name, value in parameters.items():
                res[name] = value
                break
        else:
            for item in output:
                res[item['input']] = parameters[item['input']]
        print("end function result: {}".format(res))
        repo.saveWorkflowRes(reqID, res)

    def clearDB(self, requestID):
        repo.clearDB(requestID)

       

        


