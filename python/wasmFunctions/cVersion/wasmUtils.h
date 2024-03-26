#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <malloc.h> 
#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/time.h>

void _Z10set_outputPhi(uint8_t* inBuffer, int32_t inLength);

void setOutput(int resultSize, int stringFlag, int doubleFlag, size_t numOfOutput,...);
void copyStrInOutput(uint8_t* resArray, void* buffer, int* offset);

int setFlagForStringOutput(int numOfString,...);
int setFlagForDoubleOutput(int numOfDouble,...);

int isStringAt(int flag, int pos);
int isDoubleAt(int flag, int pos);