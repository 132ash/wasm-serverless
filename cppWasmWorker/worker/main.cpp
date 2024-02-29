#include "worker.hpp"
#include "../include/json.hpp"
#include <time.h>

using json = nlohmann::json;

#define PIPE_WRITE_FD  10713

int main() {
    int argc, param;
    uint32 argv[256];
    char buffer[50];

    std::string wasmCodePath, funcName, jsonParamStr;
	wasmCodePath.resize(100); 
    funcName.resize(100);
	scanf("%s", &wasmCodePath[0]);
    scanf("%s", &funcName[0]);

    wasrModule wasmRuntime(wasmCodePath, funcName);
    
    while(true) {
        // std::string jsonParamStr;
        std::getline(std::cin, jsonParamStr);
        if(jsonParamStr.empty()) {
            std::getline(std::cin, jsonParamStr);
        }
        // scanf("%s", &jsonParamStr[0]);
        auto jsonObject = json::parse(jsonParamStr);
        int argc = 0;
        for (auto& element : jsonObject.items()) {
            argv[argc] = element.value();
            argc += 1;
        }
        // std::cout << sum << std::endl;
        wasmRuntime.runWasmCode(argc, argv);
        write(PIPE_WRITE_FD, &argv[0], sizeof(argv[0]));
    }
    return 0;
}