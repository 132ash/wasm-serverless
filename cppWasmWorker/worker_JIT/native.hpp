/*
    This file used to define the native function hooked by host_interface.h .
*/
#include "../include/utils.hpp"

uint8_t* resultBuffer;

static void set_output_native(wasm_exec_env_t exec_env, uint8_t* inBuffer, int32_t inLength){
   std::copy(inBuffer, inBuffer+inLength, resultBuffer);
}

static NativeSymbol ns[] = {
    {
        "_Z10set_outputPhi",
        (void *)set_output_native,
        "(*~)"
    },
};
