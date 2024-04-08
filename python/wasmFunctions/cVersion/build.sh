if [ "$#" -eq 0 ]; then
    echo "Usage: $0 func1 func2 ..."
    exit 1
fi


for func_name in "$@"; do
    /opt/wasi-sdk/bin/clang     \
        -Wl,--export=${func_name}\
        -z stack-size=52428800 -Wl,--initial-memory=131072000,--max-memory=1310720000 \
        -Wl,--export=malloc -Wl,--export=free\
        -Wl,--allow-undefined \
        -o ${func_name}.wasm ${func_name}.c ../utils/cJSON.c ../utils/wasmUtils.c
    mv ${func_name}.wasm ../${func_name}.wasm
    echo "Compiled ${func_name}.wasm."
done

echo "All files compiled successfully." 