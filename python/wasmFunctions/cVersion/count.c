#include "./utils/wasmUtils.h"

int count(int resultSize, uint64_t buffer)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    long long startTime;
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;

    char* text = (char*) buffer;

    cJSON *root = cJSON_CreateObject();
    char *word = strtok((char*)text, " ");
    while (word != NULL) {
        if (cJSON_HasObjectItem(root, word)) {
            cJSON *item = cJSON_GetObjectItem(root, word);
            cJSON_SetNumberValue(item, item->valuedouble + 1);
        } else {
            cJSON_AddNumberToObject(root, word, 1);
        }
        word = strtok(NULL, " ");
    }

    char *json_str = cJSON_Print(root);
    cJSON_Delete(root);
    int flag = setFlagForStringOutput(1,0);
    setOutput(resultSize, flag,  0, 1, json_str);
    return 1;
}
