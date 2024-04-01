#include "wasmUtils.h"

void setOutput(int resultSize, int stringFlag, int doubleFlag, size_t numOfOutput,...){
    uint8_t* resultArray = (uint8_t*)malloc(resultSize);
    void * output;
    va_list valist;
    va_start(valist, numOfOutput);
    int offset = 0;
    for (int i = 0; i < numOfOutput; i++) {
        output = va_arg(valist, void*);
        if (isStringAt(stringFlag, i)){
            copyStrInOutput(resultArray, output, &offset);
        } else if (isDoubleAt(doubleFlag, i)) {
            memcpy(resultArray+offset, output, sizeof(uint64_t)); 
            offset += sizeof(uint64_t);
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

int setFlagForDoubleOutput(int numOfDouble,...) {
    int flag = 0;
    va_list valist;
    va_start(valist, numOfDouble);
    for (int i = 0; i < numOfDouble; i++) {
        int pos = va_arg(valist, int);
        flag |= (1U << pos);
    }
    return flag;
}

int isStringAt(int stringFlag, int pos) {
    return (stringFlag & (1U << pos)) != 0;
}

int isDoubleAt(int doubleFlag, int pos) {
    return (doubleFlag & (1U << pos)) != 0;
}