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

imageName = {
            "binarytree":"binarytree_py",
            "spectral_norm":"spectral_norm_py"
}

# param = {
#         "binarytree":{"number":5},
#         "spectral_norm":{"number":100}
# }

param = {
        "binarytree":{"number":14},
        "spectral_norm":{"number":200}
}

funcNames = ["binarytree", "spectral_norm"]


outPutSize = 16

runFuncPath = "/home/ash/wasm/wasm-serverless/experiment/wasm/test/containerResCost/run.py"