#include <malloc.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

typedef struct tn {
    struct tn*    left;
    struct tn*    right;
} treeNode;


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


int main(int argc, char* argv[])
{
    struct timeval tv;
   long long startTime;
   gettimeofday(&tv, NULL); 
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
    unsigned   N, depth, minDepth, maxDepth, stretchDepth;
    treeNode   *stretchTree, *longLivedTree, *tempTree;

    N = atol(argv[1]);

    minDepth = 4;

    if ((minDepth + 2) > N)
        maxDepth = minDepth + 2;
    else
        maxDepth = N;

    stretchDepth = maxDepth + 1;
    long long finalItem;

    stretchTree = BottomUpTree(stretchDepth);
    ItemCheck(stretchTree);

    DeleteTree(stretchTree);

    longLivedTree = BottomUpTree(maxDepth);

    for (depth = minDepth; depth <= maxDepth; depth += 2)
    {
        long    i, iterations, check;

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
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec - startTime;
    double runtime = startTime / 1000000.0; 
    printf("%lld %.9f", finalItem, runtime);
    return 0;
} /* main() */

// gcc -o main main.c -lm