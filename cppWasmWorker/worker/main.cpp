#include "worker.hpp"
#include "../include/json.hpp"
#include <time.h>

using json = nlohmann::json;

#define PIPE_WRITE_FD  10713

int main() {
    int argc, param;
    // first two positions are for resurnSize and argc.
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
    
    while(true) {
        jsonParamStr.clear();
        while (jsonParamStr.empty()) {
            std::getline(std::cin, jsonParamStr);
        }
        auto jsonObject = json::parse(jsonParamStr);
        int argc = 0; // num of input params.
        for (const auto& element : jsonObject) {
            uint32_t param;
            if (element.is_number_integer()) {
                param = element.get<uint32_t>();
            } else if (element.is_number_float()) {   
                float f = element.get<float>();
                std::memcpy(&param, &f, sizeof(f));
            }
            argv[argc + 1] = param;
            argc += 1;
        }
        argv[0] = returnSize;
        wasmRuntime.runWasmCode(argc+2, argv);
        write(PIPE_WRITE_FD, resultBuffer, returnSize);
    }
    return 0;
}