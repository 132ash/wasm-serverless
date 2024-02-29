FUNC_NAME=$1

/opt/wasi-sdk/bin/clang     \
        -Wl,--export=${FUNC_NAME}\
        -Wl,--allow-undefined \
        -o ${FUNC_NAME}.wasm ${FUNC_NAME}.c