import subprocess
import sys
import psutil
import info
import pandas as pd
import json
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config

resdir = config.RESULT_DIR
DOCKER_FILE_PATH = info.DOCKER_FILE_PATH
WASM_FILE_PATH = info.WASM_FILE_PATH
if info.dockerFunctype == "python":
    memCost_dir = "memCost_py"
else:
    memCost_dir = "memCost_C"


runtimes = 3
mode = ['wasm', 'docker']
funcNames = ["binarytree", "spectral_norm"]

mem = {funcName:{type:[] for type in mode}for funcName in funcNames}

def get_total_memory_percent(process):
    """
    计算指定进程及其所有子进程的总内存占用百分比。
    """
    total_memory = 0
    if process.is_running():
        # 获取目标进程的内存占用百分比
        total_memory += process.memory_info().rss / (1024 * 1024)
        # 遍历子进程
        for child in process.children(recursive=True):
            try:
                total_memory += child.memory_info().rss / (1024 * 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return total_memory
    else:
        return 0



if __name__ == '__main__':
    with open(DOCKER_FILE_PATH, 'w') as f:
        f.truncate(0)
    with open(WASM_FILE_PATH, 'w') as f:
        f.truncate(0)
    for funcName in funcNames:
        for type in mode:
            print(f"-------------------------{funcName}--------------{type}-----------------------------------")
            param = info.param[funcName]
            ret = subprocess.Popen(['python', info.runFuncPath, funcName , type, str(runtimes), json.dumps(param)])
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
        df.to_csv('/'.join([resdir,memCost_dir,f'{func}_memcost.csv']), index=False)
        
    # pd.DataFrame({'node': nodes, 'core x second': cpu, 'mem_usage': mem}).to_csv(config.RESULT_DIR+'/groupingCost.csv')