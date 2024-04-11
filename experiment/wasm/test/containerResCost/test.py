import subprocess
import sys
import psutil
import info
import pandas as pd
import json
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config

resdir = config.RESULT_DIR
DOCKER_FILE_PATH = "/home/ash/wasm/wasm-serverless/experiment/wasm/test/containerResCost/dockerMemusage.txt"

runtimes = 3
mode = ['wasm', 'docker']
funcNames = ["binarytree", "spectral_norm"]

mem = {funcName:{type:[] for type in mode}for funcName in funcNames}

def get_total_memory_percent(process):
    """
    计算指定进程及其所有子进程的总内存占用百分比。
    """
    if process.is_running():
        # 获取目标进程的内存占用百分比
        total_memory_percent = process.memory_percent()
        # 遍历子进程
        for child in process.children(recursive=True):
            if child.is_running():
                # 累加子进程的内存占用百分比
                total_memory_percent += child.memory_percent()
        return total_memory_percent
    else:
        return 0



if __name__ == '__main__':
    with open(DOCKER_FILE_PATH, 'w') as f:
        f.truncate(0)
    for funcName in funcNames:
        for type in mode:
            print(f"-------------------------{funcName}--------------{type}-----------------------------------")
            param = info.param[funcName]
            ret = subprocess.Popen(['python', info.runFuncPath, funcName , type, str(runtimes), json.dumps(param)])
            # , stdout=subprocess.DEVNULL
            manager = psutil.Process(ret.pid)
            mem_percent = 0
            cpu_percent = 0
            cnt = 0
            while ret.poll() is None:
                c = manager.cpu_percent(interval=0.01)
                mem_percent = max(mem_percent, get_total_memory_percent(manager))
                cpu_percent = cpu_percent + c
                cnt = cnt + 1
            # output = ret.communicate()[0]
            # print(output)
            mem_mb = mem_percent * 7.71725 * 1024 * 0.01
            mem[funcName][type].append(mem_mb)
    print(mem)
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
            mem[lis[0]]['docker'][0] += m
    print(mem)
    for func, platforms in mem.items():
        df = pd.DataFrame({
            'WASM': platforms['wasm'],
            'Docker': platforms['docker']
        })
        df.to_csv('/'.join([resdir,"memCost",f'{func}_memcost.csv']), index=False)
        
    # pd.DataFrame({'node': nodes, 'core x second': cpu, 'mem_usage': mem}).to_csv(config.RESULT_DIR+'/groupingCost.csv')