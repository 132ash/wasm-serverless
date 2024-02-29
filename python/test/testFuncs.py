import struct
import json

def sub(arg1:int, arg2:int):
    return arg1 - arg2

def reverse(arg:int):
    return -1 * arg

def times2(arg:int):
    return 2 * arg


class Runner:
    def __init__(self):
        self.functions = {"sub":sub, "reverse":reverse, "times2":times2}
    
    def run(self, funcName, param):
        param = tuple(json.loads(param).values())
        res = self.functions[funcName](*param)
        return struct.pack('<i', res)
    

if __name__ == "__main__":
    runner = Runner()
    param = '{"sub1":2, "sub2":3}'
    print(runner.run("sub", param))
    # print(runner.run("reverse", (-5,)))
    # print(runner.run("times2", (-1,)))