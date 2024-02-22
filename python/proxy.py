from functionManager import FunctionManager


manager = FunctionManager()

def createFunction(funcName, wasmCodePath):
    flag = manager.createFunction(funcName, wasmCodePath)
    if flag:
        print("func {} created.".format(funcName))

def runFunction(funcname, argc, argv):
    res = manager.runFunction(funcname, argc, argv)
    print("run result:")
    print(int(res))

def deleteFunction(funcname):
    manager.deleteFunction(funcname)


wasmPath = "./wasmFunctions/sum.wasm"

createFunction("sum", wasmPath)
runFunction("sum", 2, [1, 2])
runFunction("sum", 2, [2, 3])
deleteFunction("sum")


