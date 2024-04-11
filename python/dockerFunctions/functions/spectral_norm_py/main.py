import numpy as np
import time

def A(i, j):
    return ((i + j) * (i + j + 1) // 2 + i + 1)

def dot(v, u):
    return np.dot(v, u)

def mult_Av(v, n):
    out = np.zeros(n)
    for i in range(n):
        for j in range(n):
            out[i] += v[j] / A(i, j)
    return out

def mult_Atv(v, n):
    out = np.zeros(n)
    for i in range(n):
        for j in range(n):
            out[i] += v[j] / A(j, i)
    return out

def mult_AtAv(v, n):
    tmp = mult_Av(v, n)
    return mult_Atv(tmp, n)

def main():
    n=number
    startTime = time.time()
    
    u = np.ones(n)
    v = np.zeros(n)
    
    for i in range(10):
        v = mult_AtAv(u, n)
        u = mult_AtAv(v, n)
    
    res = np.sqrt(dot(u, v) / dot(v, v))
    runtime = time.time() - startTime
    return {"res":res, "runtime":runtime}