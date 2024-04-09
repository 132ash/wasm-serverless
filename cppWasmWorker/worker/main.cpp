#include "worker.hpp"
#include <exception>
using json = nlohmann::json;

#define PIPE_WRITE_FD  10713
#define STATE_WRITE_FD  10714

int main() {
    int argc, param;
    uint32 argv[256];

    char buffer[50];
    auto returnBuffer = resultBuffer;
    int returnSize, heapSize;
    struct timeval tv;

    std::string wasmCodePath, funcName, jsonParamStr;
	wasmCodePath.resize(100); 
    funcName.resize(100);
	scanf("%s", &wasmCodePath[0]);
    scanf("%s", &funcName[0]);
    scanf("%d", &returnSize);
    scanf("%d", &heapSize);
    long long getStringTime=2;
    long long getParamTime=2, analyzedParamTime=2;
    long long inWasmTime=2;
    long long wrapStringTime=2;
    const char* message = "ready\n"; 
    wasrModule wasmRuntime(wasmCodePath, funcName, returnSize, heapSize);
    while(true) {
        jsonParamStr.clear();
        write(STATE_WRITE_FD, message, strlen(message));
        // new round ready. waiting for input parameter.
        while (jsonParamStr.empty()) {
            std::getline(std::cin, jsonParamStr);
        }
        gettimeofday(&tv, NULL);
        getParamTime = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
        std::cout << "json input length: " << jsonParamStr.length() << std::endl;
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
                gettimeofday(&tv, NULL);
                wrapStringTime = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
                uint64_t buffer_for_wasm;
                uint64_t strSize;
                std::string strValue;
              // read the string from json, create a buffer to save it, and create che corresponding buffer in wasm world.
                if (EndsWith(key, "_DB")){
                    std::string strKey = element.get<std::string>();
                    // strValue = "testString";
                    strValue = GetDocumentContent(strKey, &getStringTime);
                } else {
                    strValue = element.get<std::string>();
                }
                strSize = strValue.size() + 1;
                std::cout << "length of str: " << strSize << std::endl;
                char * nativeBuffer = NULL;
                buffer_for_wasm = wasmRuntime.mallocWasmBuffer(nativeBuffer, strValue.c_str(), strSize);
                if (buffer_for_wasm != 0) { 
                    std::cout << "wasm buffer addr: " << buffer_for_wasm << std::endl;
                    // // copy str content, save wasm buffer address and str size in argv.
                    argv[argc] = buffer_for_wasm;
                    argc += 2;
                } else {
                    printf("error: wasm buffer allocation failed.\n");
                }
                gettimeofday(&tv, NULL);
                wrapStringTime = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec - wrapStringTime;
            }   
        }
        gettimeofday(&tv, NULL);
        analyzedParamTime = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
        // gettimeofday(&tv, NULL);
        // inWasmTime = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
        wasmRuntime.runWasmCode(argc, argv);
        // gettimeofday(&tv, NULL);
        // inWasmTime = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec - inWasmTime;
        wrapStringTime = wrapStringTime - getStringTime;
        memcpy(resultBuffer+returnSize, &getParamTime, sizeof(long long));
        memcpy(resultBuffer+returnSize+sizeof(long long), &analyzedParamTime, sizeof(long long));
        memcpy(resultBuffer+returnSize+2*sizeof(long long), &wrapStringTime, sizeof(long long));
        memcpy(resultBuffer+returnSize+3*sizeof(long long), &getStringTime, sizeof(long long));
        writeResultToPipe(PIPE_WRITE_FD, resultBuffer, returnSize+4*sizeof(long long));
        // write(PIPE_WRITE_FD, resultBuffer, returnSize+2*sizeof(long long));
        wasmRuntime.freeAllBuffer();
    }
    return 0;
}