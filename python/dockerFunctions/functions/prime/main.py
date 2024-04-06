import json

def main():
    prime = [True for _ in range(maxNum+1)]
    p = 2
    while (p * p <= maxNum):
        if (prime[p] == True):
            for i in range(p * p, maxNum+1, p):
                prime[i] = False
        p += 1
    return {"count": sum(1 for p in range(2, maxNum) if prime[p])}
