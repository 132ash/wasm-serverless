#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <string>

#define PIPE_WRITE_FD  10713

int main() {
    int argc;
    int argv[128];
    char buffer[50];

    int sum = 0;

    std::string wasmCodePath;
	wasmCodePath.resize(100); 
	scanf("%s", &wasmCodePath[0]);
    printf("path: %s\n",wasmCodePath.c_str());
    
    while(true) {
 
        scanf("%d",&argc);
        for(int i = 0; i < argc; ++i) {
            scanf("%d", &argv[i]);
        }
        for(int i = 0; i < argc; ++i) {
            sum += argv[i];
        }
        argv[0] = sum;
        std::cout << "inside c++: " << sum << std::endl;
        sum = 0;
        int bytes = snprintf(buffer, sizeof(buffer), "%d\n", argv[0]);
        write(PIPE_WRITE_FD, buffer, bytes);

    }
    return 0;
}