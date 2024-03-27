#include "worker.hpp"

using json = nlohmann::json;

#define PIPE_WRITE_FD  10713

int main() {
    int argc, param;
    uint32 argv[256];

    char buffer[50];
    auto returnBuffer = resultBuffer;
    int returnSize;

    std::string wasmCodePath, funcName, jsonParamStr;
	wasmCodePath.resize(100); 
    funcName.resize(100);
	scanf("%s", &wasmCodePath[0]);
    scanf("%s", &funcName[0]);
    scanf("%d", &returnSize);

    wasrModule wasmRuntime(wasmCodePath, funcName, returnSize);

    const char* message = "ready\n"; 
    write(PIPE_WRITE_FD, message, strlen(message));
    long long getStringTime=0;

    
    while(true) {
        jsonParamStr.clear();
        while (jsonParamStr.empty()) {
            std::getline(std::cin, jsonParamStr);
        }
        auto jsonObject = json::parse(jsonParamStr);
        std::memcpy(&argv[0], &returnSize, sizeof(returnSize));
        int argc = 1; // num of params. default: returnSize.
        for (auto it = jsonObject.begin(); it != jsonObject.end(); ++it) {
            std::string key = it.key();
            const auto& element = it.value();
            uint32_t param;
            if (element.is_number_integer()) {
                // If the element is an unsigned number, directly save it
                uint32 arg = element.get<uint32_t>();
                argv[argc] = arg;
                argc += 1;
            } else if (element.is_number_float()) {
                // For floating-point numbers, we need to store their binary representation
                float number = element.get<float>();
                // Copy the bits of the float into a uint32_t variable
                uint32 binaryRepresentation;
                std::memcpy(&binaryRepresentation, &number, sizeof(float));
                argv[argc] = binaryRepresentation;
                argc += 1;   
            } else if (element.is_string()) {
              // read the string from json, create a buffer to save it, and create che corresponding buffer in wasm world.
                std::string strValue;
                if (EndsWith(key, "_DB")){
                    std::string strKey = element.get<std::string>();
                    strValue = GetDocumentContent(strKey, &getStringTime);
                } else {
                    strValue = element.get<std::string>();
                }
                int strSize = strValue.size() + 1;
                char * buffer = NULL;
                uint64_t buffer_for_wasm;
                buffer_for_wasm = wasmRuntime.mallocWasmBuffer(strValue.c_str(), strSize);
                if (buffer_for_wasm != 0) { 
                    // // copy str content, save wasm buffer address and str size in argv.
                    argv[argc] = buffer_for_wasm;
                    argc += 2;
                } else {
                    printf("error: wasm buffer allocation failed.\n");
                }
            }   
        }
        wasmRuntime.runWasmCode(argc, argv);
        memcpy(resultBuffer+returnSize, &getStringTime, sizeof(long long));
        write(PIPE_WRITE_FD, resultBuffer, returnSize+sizeof(long long));
        wasmRuntime.freeAllBuffer();
    }
    return 0;
}