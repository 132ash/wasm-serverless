#include "wasmUtils.h"

int string_fetch(int resultSize, uint64_t buffer)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    long long startTime;
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;

    char* input = (char*) buffer;
    int len = strlen(input);


    int flag = setFlagForDoubleOutput(1,0);
    setOutput(resultSize,0, flag, 2, &startTime, &len);
    return 1;
}