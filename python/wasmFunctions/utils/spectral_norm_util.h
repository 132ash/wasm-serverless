#include <stdio.h>
#include <stdlib.h>
#include <math.h>

inline int A(int i, int j);

double dot(double * v, double * u, int n);

void mult_Av(double * v, double * out, const int n);

void mult_Atv(double * v, double * out, const int n);

void mult_AtAv(double *tmp, double *v, double *out, const int n);