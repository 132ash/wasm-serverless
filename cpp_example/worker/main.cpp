#include "worker.hpp"
#include <time.h>

#define PIPE_WRITE_FD  10713

int main() {
    int argc, param;
    uint32 argv[256];
    char buffer[50];

    std::string wasmCodePath, funcName;
	wasmCodePath.resize(100); 
    funcName.resize(100);
	scanf("%s", &wasmCodePath[0]);
    scanf("%s", &funcName[0]);
    // printf("path: %s\n",wasmCodePath.c_str());
    // printf("funcName: %s\n",funcName.c_str());

    wasrModule wasmRuntime(wasmCodePath, funcName);
    
    while(true) {
 
        scanf("%d",&argc);
        for(int i = 0; i < argc; ++i) {
            scanf("%d", &param);
            argv[i] = param;
        }
        // std::cout << sum << std::endl;
        wasmRuntime.runWasmCode(2, argv);
        int bytes = snprintf(buffer, sizeof(buffer), "%d\n", argv[0]);
        write(PIPE_WRITE_FD, buffer, bytes);

    }
    return 0;
}