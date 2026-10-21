#!/usr/bin/env python3
"""S52 independent threshold recomputation (mpmath 50 digits, findroot + bisection cross-check).
C_theta = theta/2 + cot(theta/sqrt2)/sqrt2  (Wang arXiv:2609.07918 (4.2), re-read S52 from the text).
Theorem E threshold: C_theta = 5/2+sqrt2.  Theorem E' threshold: C_theta = 4.  E'/E switch: C_theta = 2+sqrt2."""
from mpmath import mp, mpf, sqrt, cot, findroot, diff
mp.dps = 50
r2 = sqrt(2)
C = lambda th: th/2 + cot(th/r2)/r2
def bisect(f, a, b, it=200):
    fa = f(a)
    for _ in range(it):
        m = (a+b)/2; fm = f(m)
        if (fm > 0) == (fa > 0): a, fa = m, fm
        else: b = m
    return (a+b)/2
print("monotone check: C'(theta) sign on (0.2,0.6) at 9 pts:", [mp.nstr(diff(C, mpf(x)/100),4) for x in range(20,61,5)])
for name, target, guess in [("E  (A*=5/2+sqrt2)", mpf(5)/2+r2, 0.26), ("E' (A=4)", mpf(4), 0.255),
                            ("switch (A=2+sqrt2)", 2+r2, 0.30), ("Lamzouri stated (A=2)", mpf(2), 0.55)]:
    f = lambda th: C(th) - target
    x1 = findroot(f, mpf(guess)); x2 = bisect(f, mpf('0.1'), mpf('0.9'))
    print(f"{name:24s}: findroot={mp.nstr(x1,20)} bisect={mp.nstr(x2,20)} |diff|={mp.nstr(abs(x1-x2),3)} C(root)-target={mp.nstr(f(x1),3)}")
fE  = lambda A: (5 + 2*r2 - 2*A)/(3 + 2*r2)
fEp = lambda A: (4 - A)/A
for th in ['0.2613','0.27','0.30177','0.3293','0.5502','1']:
    A = C(mpf(th))
    print(f"theta={th:8s} C={mp.nstr(A,12)} c2_E={mp.nstr(fE(A),8)} c2_E'={mp.nstr(fEp(A),8) if A>=2+r2 else '(n/a, A<2+r2)'}")
