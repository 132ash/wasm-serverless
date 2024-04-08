#include "../utils/wasmUtils.h"

int binarytree(int resultSize, int N)
{
       struct timeval tv;
   long long startTime;
   gettimeofday(&tv, NULL); 
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
    unsigned  depth, minDepth, maxDepth, stretchDepth;
    treeNode   *stretchTree, *longLivedTree, *tempTree;
    long long finalItem=0;

    minDepth = 4;

    if ((minDepth + 2) > N)
        maxDepth = minDepth + 2;
    else
        maxDepth = N;

    stretchDepth = maxDepth + 1;

    stretchTree = BottomUpTree(stretchDepth);
    DeleteTree(stretchTree);

    longLivedTree = BottomUpTree(maxDepth);

    for (depth = minDepth; depth <= maxDepth; depth += 2)
    {
        long  long  i, iterations, check;

        iterations = pow(2, maxDepth - depth + minDepth);

        check = 0;

        for (i = 1; i <= iterations; i++)
        {
            tempTree = BottomUpTree(depth);
            check += ItemCheck(tempTree);
            DeleteTree(tempTree);
        } /* for(i = 1...) */
    } /* for(depth = minDepth...) */

    finalItem = ItemCheck(longLivedTree);
    gettimeofday(&tv, NULL); 
   long long endTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
   double runtime = (endTime - startTime) / 1000000.0;
    int flag = setFlagForDoubleOutput(2,0,1);
   setOutput(resultSize,0, flag, 2, &finalItem, &runtime);

    return 0;
} /* main() */
    
