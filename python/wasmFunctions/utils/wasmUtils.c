#include "wasmUtils.h"

void setOutput(int resultSize, int stringFlag, int doubleFlag, size_t numOfOutput,...){
    uint8_t* resultArray = (uint8_t*)malloc(resultSize);
    void * output;
    va_list valist;
    va_start(valist, numOfOutput);
    int offset = 0;
    for (int i = 0; i < numOfOutput; i++) {
        output = va_arg(valist, void*);
        if (isStringAt(stringFlag, i)){
            copyStrInOutput(resultArray, output, &offset);
        } else if (isDoubleAt(doubleFlag, i)) {
            memcpy(resultArray+offset, output, sizeof(uint64_t)); 
            offset += sizeof(uint64_t);
        } else {
            memcpy(resultArray+offset, output, sizeof(uint32_t)); 
            offset += sizeof(uint32_t);
        }
    }
    _Z10set_outputPhi(resultArray, resultSize);
    va_end(valist);
    free(resultArray);
}


void copyStrInOutput(uint8_t* resArray, void* buffer, int* offset){
    int strLen = strlen((char*)buffer);
    memcpy(resArray+*offset, buffer, strLen); 
    resArray[*offset+strLen] = 0;
    *offset += (strLen+1);
}

int setFlagForStringOutput(int numOfString,...) {
    int flag = 0;
    va_list valist;
    va_start(valist, numOfString);
    for (int i = 0; i < numOfString; i++) {
        int pos = va_arg(valist, int);
        flag |= (1U << pos);
    }
    return flag;
}

int setFlagForDoubleOutput(int numOfDouble,...) {
    int flag = 0;
    va_list valist;
    va_start(valist, numOfDouble);
    for (int i = 0; i < numOfDouble; i++) {
        int pos = va_arg(valist, int);
        flag |= (1U << pos);
    }
    return flag;
}

int isStringAt(int stringFlag, int pos) {
    return (stringFlag & (1U << pos)) != 0;
}

int isDoubleAt(int doubleFlag, int pos) {
    return (doubleFlag & (1U << pos)) != 0;
}

void mult_AtAv(double *tmp, double *v, double *out, const int n) {
   mult_Av(v, tmp, n);
   mult_Atv(tmp, out, n);
}

int A(int i, int j) {
   return ((i+j) * (i+j+1) / 2 + i + 1);
}

double dot(double * v, double * u, int n) {
   int i;
   double sum = 0;
   for (i = 0; i < n; i++)
      sum += v[i] * u[i];
   return sum;
}

void mult_Av(double * v, double * out, const int n) {
   int i, j;
   double sum;
   for (i = 0; i < n; i++) {
      for (sum = j = 0; j < n; j++)
         sum += v[j] / A(i,j);
      out[i] = sum;
   }
}

void mult_Atv(double * v, double * out, const int n) {
   int i, j;
   double sum;
   for (i = 0; i < n; i++) {
      for (sum = j = 0; j < n; j++)
         sum += v[j] / A(j,i);
      out[i] = sum;
   }
}


treeNode* NewTreeNode(treeNode* left, treeNode* right)
{
    treeNode*    new;

    new = (treeNode*)malloc(sizeof(treeNode));

    new->left = left;
    new->right = right;

    return new;
} /* NewTreeNode() */


long long ItemCheck(treeNode* tree)
{
    if (tree->left == NULL)
        return 1;
    else
        return 1 + ItemCheck(tree->left) + ItemCheck(tree->right);
} /* ItemCheck() */


treeNode* BottomUpTree(unsigned depth)
{
    if (depth > 0)
        return NewTreeNode
        (
            BottomUpTree(depth - 1),
            BottomUpTree(depth - 1)
        );
    else
        return NewTreeNode(NULL, NULL);
} /* BottomUpTree() */


void DeleteTree(treeNode* tree)
{
    if (tree->left != NULL)
    {
        DeleteTree(tree->left);
        DeleteTree(tree->right);
    }

    free(tree);
} /* DeleteTree() */
