#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <malloc.h> 
#include <stdio.h>
#include <ctype.h>

void _Z10set_outputPhi(uint8_t* inBuffer, int32_t inLength);

void setOutput(int resultSize, int flag, size_t numOfOutput,...);
void copyStrInOutput(uint8_t* resArray, void* buffer, int* offset);

int setFlagForStringOutput(int numOfString,...);

int isStringAt(int flag, int pos);