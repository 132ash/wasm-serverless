#include "wasmUtils.h"

int sum(int resultSize, float divres, int time2res, int subres) {
    float res = (divres + time2res) + subres;
    setOutput(resultSize, resultSize/sizeof(uint32_t), &res);
    return 1;
}