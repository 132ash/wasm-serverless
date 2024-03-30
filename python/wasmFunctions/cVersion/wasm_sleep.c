#include "wasmUtils.h"
#include <time.h>

int wasm_sleep(int resultSize, int duration) {
    struct timeval tv;
    long long startTime, endTime;
    gettimeofday(&tv, NULL);
    startTime = 
        (long long)tv.tv_sec;

    sleep(duration);
    gettimeofday(&tv, NULL);
    endTime = 
        (long long)tv.tv_sec;
    int res = endTime - startTime;
    setOutput(resultSize, 0 , 0, 1, &res);
    return 1;
}
