#include "../utils/wasmUtils.h"

int times2(int resultSize, int arg1) {
    int res = 2 * arg1;
    setOutput(resultSize, 0,0,resultSize/sizeof(uint32_t), &res);
    return 1;
}