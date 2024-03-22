#include "wasmUtils.h"

int simple_func(int resultSize, int arg1, int arg2)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    long long startTime;
    int res = arg1 + arg2;
         
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;


    int flag = setFlagForDoubleOutput(1,0);
    setOutput(resultSize,0, flag, 2, &startTime, &res);
    return 1;
}