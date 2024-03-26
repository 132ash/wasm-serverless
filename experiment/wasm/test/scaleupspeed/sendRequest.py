import asyncio
import aiohttp
import sys
import requests
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config

dockerProxyAddr = ':'.join([config.HOST_IP, config.DOCKER_PROXY_PORT])
wasmProxyAddr = ':'.join([config.HOST_IP, config.WASM_PROXY_PORT])
FUNC_NAME = "wasm_sleep"

async def invokeFunction(session, url, data):
    async with session.post(url, json=data) as response:
        # 这里假设你不需要处理响应
        pass


async def sendRequests(funcName, param, containerType, times=50, interval=0.002):
    req = {"funcName": funcName, "parameters":param}
    tasks = []
    if containerType == 'wasm':
        reqAddr = '/'.join([wasmProxyAddr, 'request'])
    else:
        reqAddr = '/'.join([dockerProxyAddr, 'request'])
    async with aiohttp.ClientSession() as session:
        for _ in range(times):
            # 创建任务但不立即等待
            task = asyncio.create_task(invokeFunction(session, reqAddr, req))
            tasks.append(task)
            
            # 等待2毫秒再启动下一个请求
            await asyncio.sleep(interval)

        # 等待所有任务完成
        await asyncio.gather(*tasks)

def getContainerNum(funcName, containerType):
    req = {"funcName":funcName}
    if containerType == 'wasm':
        infoAddr = '/'.join([wasmProxyAddr, 'info'])
    else:
        infoAddr = '/'.join([dockerProxyAddr, 'info'])
    res = requests.post(infoAddr, json=req)
    return res.json()['containerNum']

