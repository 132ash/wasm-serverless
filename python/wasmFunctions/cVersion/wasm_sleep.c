#include "wasmUtils.h"
#include <time.h>

int wasm_sleep(int resultSize, int duration) {
    sleep(duration);
    int res = 4;
    setOutput(resultSize, 0 , 0, 1, &res);
    return 1;
}
