#!/usr/bin/env python3
"""S52 fresh harness part 1: exact/high-precision algebra of L4, L6, L7, E, E' (mpmath, 60 digits).
Independent of S51 scripts."""
from mpmath import mp, mpf, sqrt, diff, findroot
mp.dps = 60
r2 = sqrt(2); Astar = mpf(5)/2 + r2; A1 = 2 + r2
fE  = lambda A: (5 + 2*r2 - 2*A)/(3 + 2*r2)
fEp = lambda A: (4 - A)/A
def scheme(A, t, b2):
    """L6 constant from raw definitions: b1+b2=2t-A, b1-b3=2-A. Returns (b1,b3,c,phi) or None if infeasible."""
    b1 = 2*t - A - b2; b3 = b1 - 2 + A
    if b2 < t**2/4 or b3 < 0: return None
    c = max((t**2 - 2*b2)/2, 1 + b3)
    return b1, b3, c, b1/c
print("L4: t=2+sqrt2 root of t^2-4t+2:", mp.nstr(A1**2-4*A1+2, 5))
for A in [mpf(1), mpf(2), mpf('3.5'), Astar - mpf(10)**-40]:
    b1,b3,c,phi = scheme(A, A1, A1**2/4)
    print(f"L4 A={mp.nstr(A,12)}: b1={mp.nstr(b1,15)} (5/2+r2-A={mp.nstr(Astar-A,15)}) b3={mp.nstr(b3,15)} c={mp.nstr(c,15)} (3/2+r2={mp.nstr(mpf(3)/2+r2,15)}) phi-fE={mp.nstr(phi-fE(A),5)}")
# E' construction
for A in [A1, mpf('3.5'), mpf('3.9'), Astar, 4 - mpf(10)**-40]:
    b1,b3,c,phi = scheme(A, A, A**2/4)
    print(f"E' A={mp.nstr(A,15)}: b1={mp.nstr(b1,12)} A(4-A)/4={mp.nstr(A*(4-A)/4,12)} b3={mp.nstr(b3,12)} c={mp.nstr(c,12)} A^2/4={mp.nstr(A**2/4,12)} phi-(4-A)/A={mp.nstr(phi-fEp(A),5)}")
print("boundary A=2+sqrt2 exactly: fE =", mp.nstr(fE(A1),40))
print("                            fE'=", mp.nstr(fEp(A1),40))
print("                          3-2r2=", mp.nstr(3-2*r2,40))
print("slopes at 2+sqrt2: fE' =", mp.nstr(diff(fE,A1),30), " (4-A)/A' =", mp.nstr(diff(fEp,A1),30))
print("A->4-: fEp(4-1e-40)=", mp.nstr(fEp(4-mpf(10)**-40),5), " fE(4)=", mp.nstr(fE(4),10), "(negative => E trivial there)")
print("A=Astar: fE=", mp.nstr(fE(Astar),5), " fEp(Astar)=", mp.nstr(fEp(Astar),20))
# fEp - fE on (A1,4): must be >0
import itertools
worst = min(fEp(A1 + (4-A1)*mpf(i)/2000) - fE(A1 + (4-A1)*mpf(i)/2000) for i in range(1,2000))
print("min_{A in (A1,4)} (fEp - fE) on 1999-pt grid:", mp.nstr(worst,10))
# L7 optimality: brute force the L6 scheme over (t,b2) on a fine grid, compare with claimed optimum
def claimed(A): return fE(A) if A <= A1 else fEp(A)
mp.dps = 30
print("\nL7 brute force (grid t in [0.5,8], b2 in [t^2/4, 2t-2]; 400x400 then local refine):")
for A in [mpf(1), mpf('1.5'), mpf(2), mpf(3), A1, mpf('3.5'), mpf('3.8'), mpf('3.9'), Astar, mpf('3.95'), mpf('3.99')]:
    best = (-mpf(10), None)
    for i in range(401):
        t = mpf('0.5') + mpf('7.5')*i/400
        lo, hi = t**2/4, 2*t-2
        if hi < lo: continue
        for j in range(41):
            b2 = lo + (hi-lo)*j/40
            s = scheme(A, t, b2)
            if s and s[3] > best[0]: best = (s[3], (t, b2))
    # refine
    t0, b0 = best[1]; step = mpf('0.02')
    for _ in range(60):
        imp = False
        for dt in (-step, 0, step):
            for db in (-step, 0, step):
                s = scheme(A, t0+dt, b0+db)
                if s and s[3] > best[0] + mpf(10)**-25:
                    best = (s[3], (t0+dt, b0+db)); imp = True
        t0, b0 = best[1]
        if not imp: step /= 2
    print(f"  A={mp.nstr(A,8):>10}: brute={mp.nstr(best[0],12):>16} at t={mp.nstr(t0,8)} b2={mp.nstr(b0,8)} | claimed={mp.nstr(claimed(A),12):>16} | brute-claimed={mp.nstr(best[0]-claimed(A),3)}")
