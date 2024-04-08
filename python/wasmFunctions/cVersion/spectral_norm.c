// #include "../utils/spectral_norm_util.h"
#include "../utils/wasmUtils.h"


int spectral_norm(int resultSize, int n)
{

   struct timeval tv;
   long long startTime;
   gettimeofday(&tv, NULL); 
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
   if (n <= 0) n = 2000;

   double *u, *v;
   u = malloc(n * sizeof(double));
   v = malloc(n * sizeof(double));
   double* tmp = malloc(n * sizeof(double));

   int i;
   for (i = 0; i < n; i++) u[i] = 1;
   for (i = 0; i < 10; i++) {
      mult_AtAv(tmp, u, v, n);
      mult_AtAv(tmp, v, u, n);
   }

   double res = sqrt(dot(u,v, n) / dot(v,v,n));

   gettimeofday(&tv, NULL); 
   long long endTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
   double runtime = (endTime - startTime) / 1000000.0;
   int flag = setFlagForDoubleOutput(2,0,1);
   setOutput(resultSize,0, flag, 2, &res, &runtime);

   return 1;
}
