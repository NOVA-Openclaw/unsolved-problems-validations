#!/usr/bin/env python3
"""UPR #1057 S36 VALIDATE (Twin Prime, id=10): bounds on Maynard's M_k.
LOWER bound: Rayleigh quotient M_k >= k*J(F)/I(F) maximized over symmetric
polynomials F = sum c_{a,b} (1-P1)^a P2^b on the simplex (Maynard 2015 Sec.7
basis), P1=sum t_i, P2=sum t_i^2, a+2b <= D.
  simplex integral: int (1-P1)^A prod t_i^{e_i} = A! prod e_i! / (k+A+sum e)!
  int_0^{s} F dt_k = sum_j C(b,j) a!(2j)!/(a+2j+1)! s^{a+2j+1} P2'^{b-j}
UPPER bound: M_k <= k/(k-1) * log k (Polymath8b, CITED theorem) -- arithmetic only.
Unconditional bounded gaps via BV (theta=1/2) need M_k > 4; level theta
needs M_k > 2/theta (m=1).
"""
import sys, math
from functools import lru_cache
from mpmath import mp, mpf, factorial, binomial, matrix, eig, log, eigsy
mp.dps = 200

def partitions(n, maxp=None):
    if maxp is None: maxp = n
    if n == 0: yield (); return
    for p in range(min(n, maxp), 0, -1):
        for rest in partitions(n-p, p): yield (p,)+rest

@lru_cache(None)
def simplex_int(k, A, B):
    """int over {t_i>=0, sum<=1} in k vars of (1-P1)^A P2^B."""
    tot = mpf(0)
    for lam in partitions(B):
        l = len(lam)
        if l > k: continue
        # number of ways to assign parts to distinct variables
        mult = {}
        for p in lam: mult[p] = mult.get(p, 0)+1
        ways = factorial(k)/factorial(k-l)
        for m in mult.values(): ways /= factorial(m)
        coef = factorial(B)
        for p in lam: coef /= factorial(p)
        prod = mpf(1)
        for p in lam: prod *= factorial(2*p)
        tot += ways*coef*prod
    return tot*factorial(A)/factorial(k+A+2*B)

def basis(D):
    return [(a, b) for b in range(D//2+1) for a in range(D-2*b+1)]

def Mk_lower(k, D):
    bs = basis(D); n = len(bs)
    I = matrix(n, n); J = matrix(n, n)
    # integrated forms: list of (coef, exponent of (1-P1'), exponent of P2')
    def integ(a, b):
        return [(binomial(b, j)*factorial(a)*factorial(2*j)/factorial(a+2*j+1), a+2*j+1, b-j) for j in range(b+1)]
    G = [integ(a, b) for (a, b) in bs]
    for i, (a1, b1) in enumerate(bs):
        for j, (a2, b2) in enumerate(bs):
            I[i, j] = simplex_int(k, a1+a2, b1+b2)
            s = mpf(0)
            for c1, x1, y1 in G[i]:
                for c2, x2, y2 in G[j]:
                    s += c1*c2*simplex_int(k-1, x1+x2, y1+y2)
            J[i, j] = k*s
    # generalized eigenproblem J c = lam I c via Cholesky of I
    from mpmath import cholesky, inverse
    # diagonal scaling for conditioning
    from mpmath import sqrt
    dsc = [1/sqrt(I[i, i]) for i in range(n)]
    for i in range(n):
        for j in range(n):
            I[i, j] *= dsc[i]*dsc[j]; J[i, j] *= dsc[i]*dsc[j]
    L = cholesky(I); Li = inverse(L)
    Mmat = Li*J*Li.T
    Mmat = (Mmat+Mmat.T)/2
    ev = eigsy(Mmat, eigvals_only=True)
    return max(ev), n

if __name__ == "__main__":
    ks = [int(a) for a in sys.argv[1:]] or [40, 50, 54]
    for k in ks:
        ub = mpf(k)/(k-1)*log(k)
        print(f"k={k} UPPER k/(k-1)log k = {mp.nstr(ub, 10)}  (needs >4 unconditional: {'possible' if ub > 4 else 'IMPOSSIBLE'})")
        for D in range(2, 13, 2):
            try:
                lb, n = Mk_lower(k, D)
            except ValueError as e:
                print(f"  k={k} D={D} FAILED: {e}"); break
            print(f"  k={k} D={D} basis={n} M_k >= {mp.nstr(lb, 12)}  -> implied min level theta > 2/M = {mp.nstr(2/lb, 8)}")
            sys.stdout.flush()
