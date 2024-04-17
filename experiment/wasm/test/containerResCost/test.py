import subprocess
import sys
import psutil
import info
import pandas as pd
import json
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
import yaml

resdir = config.RESULT_DIR
DOCKER_FILE_PATH = info.DOCKER_FILE_PATH
WASM_INTERP_PATH = info.WASM_INTERP_PATH
WASM_JIT_PATH = info.WASM_JIT_PATH

runtimes = 3
container = ['wasm', 'wasm', 'docker']
wasmModes = ['INTERP', 'JIT', 'JIT']
testMode = ["wasm interpreter",  "wasm jit",  "docker"]
funcNames = ["binarytree", "spectral_norm"]

mem = {funcName:{type:[] for type in testMode}for funcName in funcNames}

def get_total_memory_percent(process):
    """
    计算指定进程及其所有子进程的总内存占用百分比。
    """
    total_memory = 0
    if process.is_running():
        # 获取目标进程的内存占用百分比
        # total_memory += process.memory_info().rss / (1024 * 1024)
        # 遍历子进程
        for child in process.children(recursive=True):
            try:
                total_memory += child.memory_info().rss / (1024 * 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        print(total_memory)
        return total_memory
    else:
        return 0
    
def changeWorkerType(funcName, workerType):
    filename = '/'.join([config.FUNCYAMLPATH, f'{funcName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
    yamlData['containerType'] = workerType
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)

def changeWasmMode(funcName, mode):
    filename = '/'.join([config.FUNCYAMLPATH, f'{funcName}.yaml'])
    with open(filename, 'r') as f:
        yamlData = yaml.load(f.read(), Loader=yaml.FullLoader)
    yamlData['wasmMode'] = mode
    with open(filename, 'w') as f:
        yaml.dump(stream=f, data=yamlData)


if __name__ == '__main__':

    for fileName in [DOCKER_FILE_PATH, WASM_INTERP_PATH, WASM_JIT_PATH]:
        with open(fileName, 'w') as f:
            f.truncate(0)

    for funcName in funcNames:
        for i, type in enumerate(testMode):
            wasmMode = wasmModes[i]
            containerType = container[i]
            print(f"----------------------{funcName}-------{containerType}------{wasmMode}-----------------------------")
            param = info.param[funcName]
            ret = subprocess.Popen(['python', info.runFuncPath, funcName , type, wasmMode, str(runtimes), json.dumps(param)])
            ret.wait()
         
    with open(DOCKER_FILE_PATH, "r") as f:
        content = f.read()
        dockerMems = content.split('\n')
        for funcAndmem in dockerMems:
            if len(funcAndmem) == 0:
                continue
            lis = funcAndmem.split(':')
            print(lis)
            m = float(lis[1]) / (1024 * 1024)
            print(m)
            mem[lis[0]]['docker'].append(m)

    with open(WASM_FILE_PATH, "r") as f:
        content = f.read()
        wasmMems = content.split('\n')
        for funcAndmem in wasmMems:
            if len(funcAndmem) == 0:
                continue
            lis = funcAndmem.split(':')
            print(m)
            mem[lis[0]]['wasm'].append(float(lis[1]))
    print(mem)
    for func, platforms in mem.items():
        df = pd.DataFrame({
            'WASM': platforms['wasm'],
            'Docker': platforms['docker']
        })
        df.to_csv('/'.join([resdir,"memCost",f'{func}_memcost.csv']), index=False)
        
    # pd.DataFrame({'node': nodes, 'core x second': cpu, 'mem_usage': mem}).to_csv(config.RESULT_DIR+'/groupingCost.csv')