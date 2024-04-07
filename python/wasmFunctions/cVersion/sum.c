#include "../utils/wasmUtils.h"

int sum(int resultSize, float divres, int time2res, int subres) {
    float res = (divres + time2res) + subres;
    setOutput(resultSize, 0,0,resultSize/sizeof(uint32_t), &res);
    return 1;
}