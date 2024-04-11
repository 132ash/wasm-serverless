import time

class TreeNode:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

def NewTreeNode(left=None, right=None):
    return TreeNode(left, right)

def ItemCheck(tree):
    if tree.left is None:
        return 1
    else:
        return 1 + ItemCheck(tree.left) + ItemCheck(tree.right)

def BottomUpTree(depth):
    if depth > 0:
        return NewTreeNode(BottomUpTree(depth - 1), BottomUpTree(depth - 1))
    else:
        return NewTreeNode()

def DeleteTree(tree):
    if tree.left is not None:
        DeleteTree(tree.left)
        DeleteTree(tree.right)
    del tree

def main():
    startTime = time.time()
    N = number
    minDepth = 4
    maxDepth = max(minDepth + 2, N)
    stretchDepth = maxDepth + 1
    
    stretchTree = BottomUpTree(stretchDepth)
    ItemCheck(stretchTree)
    DeleteTree(stretchTree)
    
    longLivedTree = BottomUpTree(maxDepth)
    
    for depth in range(minDepth, maxDepth + 1, 2):
        iterations = 2**(maxDepth - depth + minDepth)
        check = 0
        
        for i in range(1, iterations + 1):
            tempTree = BottomUpTree(depth)
            check += ItemCheck(tempTree)
            DeleteTree(tempTree)
    
    finalItem = ItemCheck(longLivedTree)
    runtime = time.time() - startTime
    return {"res":finalItem, "runtime":runtime}