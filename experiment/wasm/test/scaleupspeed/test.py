import sys
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
import requests
import time
import pandas as pd
import asyncio
from sendRequest import sendRequests, getContainerNum
import matplotlib.pyplot as plt

resdir = config.RESULT_DIR
dockerProxyAddr = ':'.join([config.HOST_IP, config.DOCKER_PROXY_PORT])
wasmProxyAddr = ':'.join([config.HOST_IP, config.WASM_PROXY_PORT])
FUNC_NAME = "wasm_sleep"
param = {"sleepTime": 10}
time_duration_ms = 100

# ab -n 100 -c 100 -T application/json -p /home/ash/wasm/wasm-serverless/python/test/postData.json http://127.0.0.1:7000/request

def flushFunction(funcName, containerType):
    req = {"funcNames": [funcName]}
    if containerType == 'wasm':
        deleteAddr = '/'.join([wasmProxyAddr, 'delete'])
        createAddr = '/'.join([wasmProxyAddr, 'create'])
        requests.post(deleteAddr, json=req)
        requests.post(createAddr, json=req)
    else:
        clearAddr = '/'.join([dockerProxyAddr, 'delete'])
        requests.post(clearAddr, json=req)

def testScaleUpSpeed(testTime):
    wasmTimes = []
    dockerTimes = []
    wasmContainerNum = []
    dockerContainerNum = []
    print("---------------------SCALE UP SPEED-----------------------------")
    print("TESTING WASM CONTAINER.")
    mode = 'wasm'
    flushFunction(FUNC_NAME, mode)
    startTime = time.time()
    asyncio.run(sendRequests(FUNC_NAME, {"sleepTime":5}, mode))
    timeAndContianerNum = getContainerNum(FUNC_NAME, mode)
    for pair in timeAndContianerNum:
        wasmTimes.append(pair[0] - startTime)
        wasmContainerNum.append(pair[1])

    print("TESTING DOCKER CONTAINER.")
    mode = 'docker'
    flushFunction(FUNC_NAME, mode)
    startTime = time.time()
    asyncio.run(sendRequests(FUNC_NAME, {"sleepTime":5}, mode))
    timeAndContianerNum = getContainerNum(FUNC_NAME, mode)
    for pair in timeAndContianerNum:
        dockerTimes.append(pair[0] - startTime)
        dockerContainerNum.append(pair[1])

    df_wasm = pd.DataFrame({'Time': wasmTimes, 'Containers': wasmContainerNum, 'Platform': 'WASM'})
    df_docker = pd.DataFrame({'Time': dockerTimes, 'Containers': dockerContainerNum, 'Platform': 'Docker'})


    df = pd.concat([df_wasm, df_docker], ignore_index=True)
    df.to_csv('/'.join([resdir,'scaleupspeed.csv']), index=False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py testTime")
        sys.exit(1)

    # 获取命令行参数
    testTime = int(sys.argv[1])
    testScaleUpSpeed(testTime)
