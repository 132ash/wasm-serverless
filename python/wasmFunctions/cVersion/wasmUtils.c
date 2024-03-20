#include "wasmUtils.h"

void setOutput(int resultSize, int flag, size_t numOfOutput,...){
    uint8_t* resultArray = (uint8_t*)malloc(resultSize);
    void * output;
    va_list valist;
    va_start(valist, numOfOutput);
    int offset = 0;
    for (int i = 0; i < numOfOutput; i++) {
        output = va_arg(valist, void*);
        if (isStringAt(flag, i)){
            copyStrInOutput(resultArray, output, &offset);
        } else {
            memcpy(resultArray+offset, output, sizeof(uint32_t)); 
            offset += sizeof(uint32_t);
        }
    }
    _Z10set_outputPhi(resultArray, resultSize);
    va_end(valist);
    free(resultArray);
}


void copyStrInOutput(uint8_t* resArray, void* buffer, int* offset){
    int strLen = strlen((char*)buffer);
    memcpy(resArray+*offset, buffer, strLen); 
    resArray[*offset+strLen] = 0;
    *offset += (strLen+1);
}

int setFlagForStringOutput(int numOfString,...) {
    int flag = 0;
    va_list valist;
    va_start(valist, numOfString);
    for (int i = 0; i < numOfString; i++) {
        int pos = va_arg(valist, int);
        flag |= (1U << pos);
    }
    return flag;
}

int isStringAt(int flag, int pos) {
    return (flag & (1U << pos)) != 0;
}