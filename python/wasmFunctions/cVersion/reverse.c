#include "wasmUtils.h"

int reverse(int resultSize, int arg1) {
    int res = -1 * arg1;
    setOutput(resultSize, resultSize/sizeof(uint32_t), &res);
    return 1;
}