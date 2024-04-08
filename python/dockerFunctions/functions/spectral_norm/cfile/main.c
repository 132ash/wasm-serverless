#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>

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
#   pragma omp parallel for private(sum,j)
   for (i = 0; i < n; i++) {
      for (sum = j = 0; j < n; j++)
         sum += v[j] / A(i,j);
      out[i] = sum;
   }
}

void mult_Atv(double * v, double * out, const int n) {
   int i, j;
   double sum;
#   pragma omp parallel for private(sum,j)
   for (i = 0; i < n; i++) {
      for (sum = j = 0; j < n; j++)
         sum += v[j] / A(j,i);
      out[i] = sum;
   }
}

double *tmp;
void mult_AtAv(double *v, double *out, const int n) {
   mult_Av(v, tmp, n);
   mult_Atv(tmp, out, n);
}

int main(int argc, char**argv) {
   struct timeval tv;
   long long startTime;
   gettimeofday(&tv, NULL); 
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
   int n = atoi(argv[1]);
   if (n <= 0) n = 2000;

   double *u, *v;
   u = malloc(n * sizeof(double));
   v = malloc(n * sizeof(double));
   tmp = malloc(n * sizeof(double));

   int i;
   for (i = 0; i < n; i++) u[i] = 1;
   for (i = 0; i < 10; i++) {
      mult_AtAv(u, v, n);
      mult_AtAv(v, u, n);
   }
   double res = sqrt(dot(u,v, n) / dot(v,v,n));
   gettimeofday(&tv, NULL); 
    startTime = 
        (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec - startTime;
   double runtime = startTime / 1000000.0; 
   printf("%.9f %.9f\n", res, runtime);
   return 0;
}

// gcc -o main main.c -lm