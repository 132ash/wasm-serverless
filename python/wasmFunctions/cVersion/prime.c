#include "../utils/wasmUtils.h"

int prime(int resultSize, int n) {
    int count = 0;
    char *prime = (char *)malloc((n+1) * sizeof(char));
    memset(prime, 1, n+1);

    for (int p = 2; p*p <= n; p++) {
        // 如果prime[p]没有被改变，那么它是一个素数
        if (prime[p]) {
            // 更新所有p的倍数为非素数
            for (int i = p*p; i <= n; i += p) {
                prime[i] = 0;
            }
        }
    }

    // 计数素数数量
    for (int p = 2; p <= n; p++) {
        if (prime[p]) count++;
    }

    free(prime);
    setOutput(resultSize, 0,  0, 1, &count);
    return 1;
}
