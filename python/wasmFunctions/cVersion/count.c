#include "../utils/wasmUtils.h"


int count(int resultSize, uint64_t buffer)
{

    char* str = (char*) buffer;
    int inWord = 0; // 当前是否在单词中
    int wordCount = 0; // 单词计数

    // 遍历字符串
    for (; *str != '\0'; str++) {
        if (isalpha((unsigned char)*str)) {
            // 当前字符是字母
            if (!inWord) {
                // 这标志着一个新单词的开始
                inWord = 1;
                wordCount++; // 增加单词计数
            }
        } else {
            // 当前字符不是字母
            if (inWord) {
                // 这标志着一个单词的结束
                inWord = 0;
            }
        }
    }
    setOutput(resultSize, 0,  0, 1, &wordCount);
    return 1;
}
