PIPE_WRITE_FD  = 10713
STATE_WRITE_FD = 10714
COUCH_DB_URL = 'http://132ash:ash020620@192.168.35.132:5984'
INTERPWORKERPATH = "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_INTERP/build/worker"
JITPWORKERPATH = "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/worker"
WORKFLOWYAMLPATH = "/home/ash/wasm/wasm-serverless/python/yaml/workflow"
SINGLEFUNCYAMLPATH = "/home/ash/wasm/wasm-serverless/python/yaml/singleFunction"
WASMFUNCTIONPATH = "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker/wasmFunctions"
WORKERNODEPATH = "/home/ash/wasm/wasm-serverless/python/config/workerNodeInfo.yaml"
NETWORK_BANDWIDTH = 1000 * 1024 * 1024 / 8  #1000/8 MB/s
NET_MEM_BANDWIDTH_RATIO = 15 # mem_time = net_time / 15
GROUP_LIMIT = 3
GATEWAY_ADDR =  '192.168.35.132:8000'
MASTER_HOST = '192.168.35.132:7000'
CLEAR_DB_AND_MEM = True
CONTROL_MODE = 'WorkerSP' # WorkerSP MasterSP
DATA_TRANSFER_DB = "strings_for_data_transfer"
WASMPROXYPATH = "/home/ash/wasm/wasm-serverless/python/function/wasmProxy.py"


# master
# python /home/ash/wasm/wasm-serverless/python/workflow/gateway.py 192.168.35.132 8000
# python /home/ash/wasm/wasm-serverless/python/workflow/proxy.py 192.168.35.132 7000

# worker1
# python /home/ash/wasm/wasm-serverless/python/workflow/proxy.py 192.168.35.133 7000


#worker2
# python /home/ash/wasm/wasm-serverless/python/workflow/proxy.py 192.168.35.134 7000
