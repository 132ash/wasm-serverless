#include "../utils/wasmUtils.h"

int wordcount(int resultSize, uint64_t buffer)
{

    char* text = (char*) buffer;
    int len = strlen(text);

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
    int flag = setFlagForStringOutput(1,1);
    setOutput(resultSize, flag,  0, 2, &len, json_str);
    return 1;
}
