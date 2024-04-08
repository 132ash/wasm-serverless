#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <malloc.h> 
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/time.h>
#include "cJSON.h"
#include <math.h>

void _Z10set_outputPhi(uint8_t* inBuffer, int32_t inLength);

void setOutput(int resultSize, int stringFlag, int doubleFlag, size_t numOfOutput,...);
void copyStrInOutput(uint8_t* resArray, void* buffer, int* offset);

int setFlagForStringOutput(int numOfString,...);
int setFlagForDoubleOutput(int numOfDouble,...);

int isStringAt(int flag, int pos);
int isDoubleAt(int flag, int pos);

int A(int i, int j);

double dot(double * v, double * u, int n);

void mult_Av(double * v, double * out, const int n);

void mult_Atv(double * v, double * out, const int n);

void mult_AtAv(double *tmp, double *v, double *out, const int n);

typedef struct tn {
    struct tn*    left;
    struct tn*    right;
} treeNode;


treeNode* NewTreeNode(treeNode* left, treeNode* right);



long long ItemCheck(treeNode* tree);


treeNode* BottomUpTree(unsigned depth);


void DeleteTree(treeNode* tree);
