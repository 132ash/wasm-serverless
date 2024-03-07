#include "wasmUtils.h"


void setOutput(int resultSize, size_t numOfOutput,...){
    uint8_t* resultArray = (uint8_t*)malloc(resultSize);
    void * output;
    va_list valist;
    va_start(valist, numOfOutput);
    for (size_t i = 0, offset=0; i < numOfOutput; i++) {
        output = va_arg(valist, void*);
        memcpy(resultArray+offset, output, sizeof(uint32_t)); 
        offset += sizeof(uint32_t);
    }
    _Z10set_outputPhi(resultArray, resultSize);
    va_end(valist);
    free(resultArray);
}