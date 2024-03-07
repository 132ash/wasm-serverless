#include "wasmUtils.h"

int cal(int resultSize, int arg1, int arg2) {
    int addres = arg1 + arg2;
    int subres = arg1 - arg2;
    float divres = ((float)arg1 / arg2);
    setOutput(resultSize, resultSize/sizeof(uint32_t), &addres, &subres, &divres);
    return 1;
}




