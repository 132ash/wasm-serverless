import sys
import logging
sys.path.append('./config')
sys.path.append('./storage')
import config
import requests
import time
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

class WorkerSPManager:
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
        info = self.getFunctionInfo(funcName)
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

    def triggerFunction(self, state: WorkflowState, functionName: str, parameters:dict, noParentExecution = False) -> None:
        funcInfo = self.getFunctionInfo(functionName)
        if funcInfo['ip'] == self.hostAddr:
            # function runs on local
            self.triggerFunctionLocal(state, functionName, parameters, noParentExecution)
        else:
            # function runs on remote machine
            self.triggerFunctionRemote(state, functionName, funcInfo['ip'], parameters, noParentExecution)
        return {}


    def triggerFunctionLocal(self, state: WorkflowState, function_name: str, parameters:dict, noParentExecution = False) -> None:
        # print(f"[Workflow Manager] run func {function_name} with param {parameters}.]")
        state.lock.acquire()
        if not noParentExecution:
            state.parentExecuted[function_name] += 1
        runnable = self.checkRunnable(state, function_name)
        self.setFunctionParam(state.request_id, function_name, parameters)
        # remember to release state.lock
        if runnable:
            state.executed[function_name] = True
            state.lock.release()
            self.runFunction(state, function_name, self.getFunctionParam(state.request_id, function_name))
        else:
            state.lock.release()

    # trigger a function that runs on remote machine
    def triggerFunctionRemote(self, state: WorkflowState, function_name: str, remote_addr: str, parameters:dict, no_parent_execution = False) -> None:
        remote_url = 'http://{}/workflow/request'.format(remote_addr)
        data = {
            'requestId': state.request_id,
            'workflowName': self.workflowName,
            'functionName': function_name,
            'noParentExecution': no_parent_execution,
            'parameters': parameters
        }
        response = requests.post(remote_url, json=data)
        response.close()

    def checkRunnable(self, state: WorkflowState, function_name: str) -> bool:
        info = self.getFunctionInfo(function_name)
        print(f"check func {function_name}. exec parent {state.parentExecuted[function_name]} with total {info['parent_cnt']}.")
        return state.parentExecuted[function_name] == info['parent_cnt'] and not state.executed[function_name]


    def runFunction(self, state:WorkflowState, funcName, parameters:dict):
        info = self.getFunctionInfo(funcName)
        source = info['source']
        if source == 'SWITCH':
            self.runSwitchFunction(info, state, parameters)
            return
        if source == 'END':
            self.runEndFunction(info, state, parameters) 
            return 
        if source == 'FOREACH':
            res = self.runForeachFunction(state, info, funcName, parameters) 
        else:
            res = self.runNormalFunction(state, funcName, parameters)
        jobs = [
            gevent.spawn(self.triggerFunction, state, func, res)
            for func in info['next']
        ]
        gevent.joinall(jobs)
    
    def runNormalFunction(self, state:WorkflowState, funcName, parameters, collectedRes = [], foreach=False):
        if foreach:
            collectedRes.append(self.functionManager.runFunction(funcName, parameters)[0])
            return
        else:
            reqID = state.request_id
            start = time.time()
            res = self.functionManager.runFunction(funcName, parameters)[0]
            end = time.time()
            print(f"func {funcName} update latency.")
            repo.saveLatency(reqID, funcName, end-start)
            return res
       
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

    def runForeachFunction(self, state:WorkflowState, info, funcName, parameters):
        reqID = state.request_id
        start = time.time()
        traverse = info['traverse']
        selectedParam = []
        splitedRes = []
        
        for i in range(len(parameters[traverse[0]])):
            sub_param = {}
            for param in parameters:
                if param in traverse:
                    sub_param[param] = parameters[param][i]
                else:
                    sub_param[param] = parameters[param]
            selectedParam.append(sub_param)
        jobs = [
            gevent.spawn(self.runNormalFunction, state, funcName, param, splitedRes, True)
            for param in selectedParam
        ]
        gevent.joinall(jobs)
        end = time.time()
        collectedRes = {key:[] for key in splitedRes[0].keys()}
        for key in collectedRes:
            for foreachRes in splitedRes:
                collectedRes[key].append(foreachRes[key])
        repo.saveLatency(reqID, funcName, end-start)
        return collectedRes
        
    
    # choose multiple(or single) params in parameters and construct output dict.
    def runEndFunction(self, info, state:WorkflowState, parameters:dict):
        start = time.time()
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
        end = time.time()
        # print("end function result: {}".format(res))
        repo.saveLatency(reqID, 'end', end-start)
        repo.saveWorkflowRes(reqID, res)

    def clearDB(self, requestID):
        repo.clearDB(requestID)

       

        


