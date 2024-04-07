#include "../utils/wasmUtils.h"

int reverse(int resultSize, int arg1) {
    int res = -1 * arg1;
    setOutput(resultSize, 0,0,resultSize/sizeof(uint32_t), &res);
    return 1;
}