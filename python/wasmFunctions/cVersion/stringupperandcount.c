#include "wasmUtils.h"

int stringupperandcount(int resultSize, uint64_t buffer, int times) {

    char* input = (char*) buffer;
    int len = strlen(input);
    int i;
    int upperCount = 0;

    for (i = 0; i < len; ++i) {
        // 只处理ASCII范围的小写字母
        if (input[i] >= 'a' && input[i] <= 'z') {
            input[i] = toupper(input[i]);
        } else {
            upperCount++;
        }
    }
    input[i] = '\0';
    int timeres = times * upperCount;
    int flag = setFlagForStringOutput(1,0);
    setOutput(resultSize, flag,  2, input, &timeres);
    // setOutput(newResultSize, newResultSize/sizeof(uint32_t), &res);
    return 1;
}