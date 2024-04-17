from container import Container
import subprocess
import os
import info
import ast
import sys
import signal
import docker

client = docker.from_env()
containerList = {func_name:[] for func_name in info.funcNames}
port = 30000

def killProcessesOnPort(port):
    command = "lsof -i :" + str(port) + " | grep LISTEN | awk '{print $2}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

# 如果有找到进程ID，尝试杀死这些进程
    if stdout:
        for pid in stdout.decode().splitlines():
            try:
                os.kill(int(pid), signal.SIGKILL)
                print(f"kill process {pid}.")
            except Exception as e:
                pass
    else:
        pass

def flush():
    os.system('docker rm -f $(docker ps -aq --filter label=dockerContainer)')
    killProcessesOnPort(port)

def createContainer(funcName, type,wasmMode):
    container = Container(funcName, port, type, client,wasmMode)
    container.startWorker()
    containerList[funcName].append(container)

def runFunction(funcName, param, runtimes, type):
    container = containerList[funcName][0]
    for _ in range(runtimes):
        print(container.run(param))
    container.writeMaxMem()

if __name__ == "__main__":
    print("running.")
    funcName = sys.argv[1]
    container = sys.argv[2]
    wasmMode =  sys.argv[3]
    runtimes = int(sys.argv[4])
    param = ast.literal_eval(sys.argv[5])
    flush()
    createContainer(funcName, container,wasmMode)
    runFunction(funcName, param, runtimes,container)
    print("finished.")
