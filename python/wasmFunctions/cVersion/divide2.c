#include "../utils/wasmUtils.h"

int divide2(int resultSize, float arg1) {
    float res = arg1 / 2;
    setOutput(resultSize, 0,0, resultSize/sizeof(uint32_t), &res);
    return 1;
}