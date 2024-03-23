#include "native.hpp"
#include <string>
#include <cstring>
#include <stdexcept>
#include <iostream>

// std::string wasmTestFilePath = "/home/ash/wasm/wasm-serverless/worker/wasmFunctions/sum.wasm";

int stackSize = 1024 * 1024 * 10; //10MB
int heapSize = 1024 * 1024 * 10; //10MB

void readBytes(int fd, unsigned char* buffer, int bufferLength){
    int cpos = 0;
    while (cpos < bufferLength) {
        int rc = read(fd, buffer + cpos, bufferLength - cpos);
        if (rc < 0) {
            perror("[Host Worker Read] Couldn't Read from worker.");
            throw "[Host Worker Read] Couldn't Read from worker.";
        } else {
            cpos += rc;
        }
    }
}


void readFileToBytes(const std::string& path, std::vector<uint8_t>& codeBytes){
    int fd = open(path.c_str(), O_RDONLY);
    if (fd < 0) throw std::runtime_error("Couldn't open file " + path);
    struct stat statbuf;
    int staterr = fstat(fd, &statbuf);
    if (staterr < 0) throw std::runtime_error("Couldn't stat file " + path);
    size_t fsize = statbuf.st_size;
    posix_fadvise(fd, 0, 0, POSIX_FADV_SEQUENTIAL);
    codeBytes.resize(fsize);
    readBytes(fd, codeBytes.data(), fsize);
    close(fd);
    return;
}

class wasrModule{
  private:
    char error_buf[128];
    wasm_module_t module;
    wasm_module_inst_t module_inst;
    wasm_function_inst_t func;
    wasm_exec_env_t exec_env;
    std::vector<uint8_t> codeBytes;
    std::vector<uint64_t> buffers;

  public:

    wasrModule(std::string wasmFilePath, std::string funcName, int return_size){
      resultBuffer = new uint8_t[return_size];
      memset(resultBuffer, 1, return_size);
      readFileToBytes(wasmFilePath, codeBytes);
      this->constructRuntime(funcName);
    }

    ~wasrModule(){
      this->deconstructRuntime();
      delete [] resultBuffer;
    }

    void constructRuntime(std::string funcName){
      wasm_runtime_init();
      if(!wasm_runtime_register_natives("env", ns, sizeof(ns) / sizeof(NativeSymbol))) 
        throw "[Runtime] Fail to register the native fucntion.";
      module = wasm_runtime_load(codeBytes.data(), codeBytes.size(), error_buf, sizeof(error_buf));
      module_inst = wasm_runtime_instantiate(module, stackSize, heapSize, error_buf, sizeof(error_buf));
      func = wasm_runtime_lookup_function(module_inst, funcName.c_str());
      exec_env = wasm_runtime_create_exec_env(module_inst, stackSize);
    }

    void deconstructRuntime(){
      this->freeAllBuffer();
      wasm_runtime_destroy_exec_env(exec_env);
      wasm_runtime_deinstantiate(module_inst);
      wasm_runtime_unload(module);
      wasm_runtime_destroy();
    }

    void runWasmCode(int argc, uint32 argv[]){
      // Call the wasm code and the argument get from native function
      
      if (!wasm_runtime_call_wasm(exec_env, func, argc, argv) ) {
        printf("error: %s\n", wasm_runtime_get_exception(module_inst));
      }
    }

    uint64_t mallocWasmBuffer(const char *src, uint64_t size){
      uint64_t wasm_buffer_addr = wasm_runtime_module_dup_data(module_inst, src, size);
      buffers.push_back(wasm_buffer_addr);
      return wasm_buffer_addr;
    }

    void freeWasmBuffer(uint64_t wasm_buffer_addr){
      wasm_runtime_module_free(module_inst, wasm_buffer_addr);
    }

    void freeAllBuffer(){
      for (auto addr:buffers) {
        this->freeWasmBuffer(addr);
      }
    }
};