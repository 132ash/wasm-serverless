PIPE_WRITE_FD  = 10713
COUCH_DB_URL = 'http://132ash:ash020620@192.168.35.132:5984'
WORKERPATH = "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker/build/worker"
WORKFLOWYAMLPATH = "/home/ash/wasm/wasm-serverless/python/yaml/workflow"
SINGLEFUNCYAMLPATH = "/home/ash/wasm/wasm-serverless/python/yaml/singleFunction"
WASMFUNCTIONPATH = "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker/wasmFunctions"
WORKERNODEPATH = "/home/ash/wasm/wasm-serverless/python/config/workerNodeInfo.yaml"
NETWORK_BANDWIDTH = 25 * 1024 * 1024 / 4
NET_MEM_BANDWIDTH_RATIO = 15 # mem_time = net_time / 15
GROUP_LIMIT = 3
GATEWAY_ADDR =  '192.168.35.132:8000'
MASTER_HOST = '192.168.35.132:7000'
CLEAR_DB_AND_MEM = True
CONTROL_MODE = 'WorkerSP' #WorkerSP
DATA_TRANSFER_DB = "strings_for_data_transfer"