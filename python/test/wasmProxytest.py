import requests
import json
import time
import base64
import yaml
import struct
base_url = "http://localhost:30000/{}"


FILE_NAME = "pg-being_ernest.txt"
FILE_NAME_TEST = "test.txt"
slice = ""
with open(f"/home/ash/wasm/wasm-serverless/python/setupScripts/text/{FILE_NAME}", 'r') as f:
    slice = f.read()

# slice = "hello the world\nhello the world\nhello the world"

funcNames = ['count']
param = json.dumps({'slice':slice}) + '\n'
# param = json.dumps({'slice':"world"}) + '\n'
outputSize = 500000
initParam = {"wasmCodePath":"/home/ash/wasm/wasm-serverless/python/wasmFunctions/count.wasm",
                    'funcName':"count",'outputSize':outputSize}

info = yaml.load(open("/home/ash/wasm/wasm-serverless/python/yaml/singleFunction/count.yaml"), Loader=yaml.FullLoader)
        
triggerData = {"parameters":param}

def testinit():
    r = requests.post(base_url.format('init'), json=initParam)

def testRun(n):
    t1 = time.time()
    r = requests.post(base_url.format('run'), json=triggerData)
    wasm_out = base64.b64decode(r.json()["out"])
    res, timeStamps = constructOutput(wasm_out)
    t2 = time.time()
    with open(f"/home/ash/wasm/wasm-serverless/python/wrongByte{n}.txt", 'w') as f:
        f.write(json.dumps(res))
    # print(res)[:50]
    print(t2-t1)
    print(timeStamps)

def constructOutput(uintBits):
        res = {}
        bitsIdx = 0
        timeStamps = []
        for i in info["output"]:
                name = i['name']
                type = i['type']
                if type == 'string':
                    start = bitsIdx 
                    while uintBits[bitsIdx] != 0:
                        bitsIdx += 1
                # encoding = chardet.detect(uintBits[start:bitsIdx])['encoding']
                # print(f"encoding: {encoding}")
                    res[name] = uintBits[start:bitsIdx].decode("ISO-8859-1")
                # except:
                #     print(uintBits[18780:18798])
                #     print(uintBits[18799:18810])
                #     input("wrong decode.")
                    bitsIdx += 1
                elif type == 'double':
                    chunk = uintBits[bitsIdx:bitsIdx+8]
                    res[name] = int.from_bytes(chunk, 'little')
                    bitsIdx += 8
                else:
                    chunk = uintBits[bitsIdx:bitsIdx+4]
                    if type == 'int':
                        res[name] = struct.unpack('<i', chunk)[0]
                    elif type == 'float':
                        res[name] = struct.unpack('<f', chunk)[0]
                    bitsIdx += 4 
        bitsIdx = outputSize
        for _ in range(2):
            chunk = uintBits[bitsIdx:bitsIdx+8]
            timeStamps.append(int.from_bytes(chunk, 'little'))
            bitsIdx += 8
        return res, timeStamps



testinit()
testRun(1)
time.sleep(1)
testRun(2)
time.sleep(1)
testRun(3)