import requests
import json
import base64
base_url = "http://localhost:30000/{}"

param = json.dumps({'arg1':1, 'arg2':2}) + '\n'

triggerData = {"parameters":param}
initParam = {"wasmCodePath":"/home/ash/wasm/wasm-serverless/python/wasmFunctions/cal.wasm",
                    'funcName':"cal",'outputSize':12}
        

def testinit():
    r = requests.post(base_url.format('init'), json=initParam)
    print(r.json())

def testRun():
    r = requests.post(base_url.format('run'), json=triggerData)
    wasm_out = base64.b64decode(r.json()["out"])
    print(wasm_out)

testinit()
testRun()