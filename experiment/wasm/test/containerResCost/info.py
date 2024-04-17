wasmPath = {
            "binarytree":"/home/ash/wasm/wasm-serverless/python/wasmFunctions/binarytree.wasm",
            "spectral_norm":"/home/ash/wasm/wasm-serverless/python/wasmFunctions/spectral_norm.wasm"
}

input = {
        "binarytree":{"number":"int"},
        "spectral_norm":{"number":"int"}
}

output = {
        "binarytree":{"res":"long long", "runtime":"double"},
        "spectral_norm":{"res":"double", "runtime":"double"}
}

dockerFunctype = "c" # c python

wasmMode = {
            "binarytree":"JIT",
            "spectral_norm":"JIT"
}

imageName = {
            "binarytree":"binarytree",
            "spectral_norm":"spectral_norm"
}

imageName_py = {
            "binarytree":"binarytree_py",
            "spectral_norm":"spectral_norm_py"
}

param = {
        "binarytree":{"number":10},
        "spectral_norm":{"number":200}
}

resFiles = {
    "docker":"/home/ash/wasm/wasm-serverless/experiment/wasm/test/containerResCost/dockerMemUsage.txt",
    "wasm interpreter" : "/home/ash/wasm/wasm-serverless/experiment/wasm/test/containerResCost/wasmINTERPmem.txt",
    "wasm jit" : "/home/ash/wasm/wasm-serverless/experiment/wasm/test/containerResCost/wasmJITmem.txt"

}


#         "binarytree":{"number":5},
#         "spectral_norm":{"number":50}
# }

funcNames = ["binarytree", "spectral_norm"]


outPutSize = 16

runFuncPath = "/home/ash/wasm/wasm-serverless/experiment/wasm/test/containerResCost/run.py"