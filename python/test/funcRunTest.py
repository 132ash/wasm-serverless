from functionManager import FunctionManager
import time

def sendReq(funcName, manager:FunctionManager, data):
    print("new request. data:{}".format(data))
    res = manager.runFunction(funcName, data)
    print("[client] get function res:{}, type:{}".format(res, type(res)))
    print("send over.\n")

if __name__ == "__main__":
    funcName = "sum"
    wasmPath = "./wasmFunctions/sum.wasm"
    maxWorkers = 10
    manager = FunctionManager()
    data1 = [1,2]
    data2 = [3,4]
    data3 = [5,6]

    manager.createFunction(funcName, wasmPath)
    while(True):
        sendReq(funcName, manager, data1)
        sendReq(funcName, manager, data2)
        sendReq(funcName, manager, data3)
        time.sleep(1)



