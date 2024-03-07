if [ "$#" -eq 0 ]; then
    echo "Usage: $0 func1 func2 ..."
    exit 1
fi


for func_name in "$@"; do
    /opt/wasi-sdk/bin/clang     \
        -Wl,--export=${func_name}\
        -Wl,--allow-undefined \
        -o ${func_name}.wasm ${func_name}.c wasmUtils.c
    mv ${func_name}.wasm ../${func_name}.wasm
    echo "Compiled ${func_name}.wasm."
done

echo "All files compiled successfully."