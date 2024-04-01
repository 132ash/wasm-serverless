import time
import numpy as np


def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    C = np.matmul(A, B)

def main():
    start = time.time()
    matmul(1000)
    end = time.time()
    return {"exec_latency": end - start}
