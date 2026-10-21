#!/usr/bin/env python3
"""S52 fresh harness part 2: adversarial stress of E and E' in the ABSTRACT model used by the proof.
Only the facts the proof uses are imposed on alpha (dims DU=r+p+q, DM=n, DW-DV=k=p+q):
  S_U >= 2r+2p+4q, S_M <= n, alpha_W <= 0, sum alpha = N, N >= n+2r+2p+4q (multiplicities).
Adversary: for each integer data (n,r,p,q,N) find MIN sum alpha^2 (convex QP; by convexity the optimum
is block-constant, so we optimise block sums S_U,S_M,S_W exactly with scipy then re-evaluate in mpmath).
That gives the smallest admissible A = A_min = min sum alpha^2 / N. E holds for this data iff
  (n+2r+2p)/N >= fE(A)  for every A >= A_min, i.e. iff it holds at A_min (fE decreasing).
We report the minimum slack (n+2r+2p)/N - f(A_min) over the sweep, for f=fE (A_min<A*) and f=fE' (A_min in [2+r2,4))."""
import itertools, numpy as np
from scipy.optimize import minimize
from mpmath import mp, mpf, sqrt
mp.dps = 50
r2 = sqrt(2); Astar = mpf(5)/2 + r2; A1 = 2 + r2
fE  = lambda A: (5 + 2*r2 - 2*A)/(3 + 2*r2)
fEp = lambda A: (4 - A)/A
def minq(n, r, p, q, N):
    DU, k = r+p+q, p+q
    LU = 2*r+2*p+4*q
    # variables SU, SM, SW ; cost SU^2/DU + SM^2/n + SW^2/k ; handle empty blocks
    def cost(x):
        SU, SM, SW = x
        c = 0.0
        c += SU**2/DU if DU else (0 if abs(SU)<1e-12 else 1e9)
        c += SM**2/n  if n  else (0 if abs(SM)<1e-12 else 1e9)
        c += SW**2/k  if k  else (0 if abs(SW)<1e-12 else 1e9)
        return c
    cons = [{'type':'eq','fun':lambda x: x[0]+x[1]+x[2]-N},
            {'type':'ineq','fun':lambda x: x[0]-LU},
            {'type':'ineq','fun':lambda x: n - x[1]},
            {'type':'ineq','fun':lambda x: -x[2]}]
    if not n: cons.append({'type':'eq','fun':lambda x: x[1]})
    if not k: cons.append({'type':'eq','fun':lambda x: x[2]})
    if not DU: cons.append({'type':'eq','fun':lambda x: x[0]})
    x0 = [max(LU, N-n), min(n, N-LU) if n else 0, 0]
    res = minimize(cost, x0, constraints=cons, method='SLSQP', options={'ftol':1e-15,'maxiter':500})
    SU, SM, SW = res.x
    # exact re-evaluation in mpmath with constraint check
    SU, SM, SW = mpf(SU), mpf(SM), mpf(SW)
    viol = max(LU-SU, SM-n, SW, abs(SU+SM+SW-N))
    Q = (SU**2/DU if DU else 0) + (SM**2/n if n else 0) + (SW**2/k if k else 0)
    return Q, viol
worstE = (mpf(10), None); worstEp = (mpf(10), None); cnt = {'E':0,'Ep':0,'all':0}; maxviol = 0
rng = np.random.default_rng(52)
datas = []
R = range(0, 9)
for n, r, p, q in itertools.product(R, R, R, R):
    if n+r+p+q == 0: continue
    Nmin = n + 2*r + 2*p + 4*q
    for extra in (0, 1, 2, 5, 10, 25):
        # extra multiplicity only possible if r+q>0 (multiple elements)
        if extra and r+q == 0: continue
        datas.append((n, r, p, q, Nmin+extra))
for n,r,p,q,N in datas:
    Q, viol = minq(n,r,p,q,N)
    maxviol = max(maxviol, float(viol))
    if viol > 1e-7: continue
    cnt['all'] += 1
    A = Q/N; ratio = mpf(n+2*r+2*p)/N
    if A < Astar:
        cnt['E'] += 1; s = ratio - fE(A)
        if s < worstE[0]: worstE = (s, (n,r,p,q,N, A))
    if A1 <= A < 4:
        cnt['Ep'] += 1; s = ratio - fEp(A)
        if s < worstEp[0]: worstEp = (s, (n,r,p,q,N, A))
print("data points solved:", cnt['all'], " max constraint violation:", maxviol)
print("E  : cases with A_min < 5/2+sqrt2:", cnt['E'], " min slack:", mp.nstr(worstE[0],12), " at (n,r,p,q,N,A)=", worstE[1][:5], mp.nstr(worstE[1][5],12))
print("E' : cases with A_min in [2+sqrt2,4):", cnt['Ep'], " min slack:", mp.nstr(worstEp[0],12), " at", worstEp[1][:5] if worstEp[1] else None, mp.nstr(worstEp[1][5],12) if worstEp[1] else '')
# Tightness probe (derived): family r=p=0, n and q chosen to push A into [2+sqrt2,4)
print("\nTightness family (only simple reals n and multiple non-real q, N=n+4q):")
for n, q in [(1,1),(1,2),(2,3),(3,5),(1,3),(5,8),(10,17),(1,10)]:
    Q, viol = minq(n,0,0,q,n+4*q); A = Q/(n+4*q); ratio = mpf(n)/(n+4*q)
    tag = 'E-range' if A < Astar else 'beyond A*'
    extra = f" fE'={mp.nstr(fEp(A),10)} slackE'={mp.nstr(ratio-fEp(A),6)}" if A1 <= A < 4 else ''
    print(f"  n={n:2d} q={q:2d} A_min={mp.nstr(A,12)} ratio={mp.nstr(ratio,10)} fE={mp.nstr(fE(A),10)} slackE={mp.nstr(ratio-fE(A),6)}{extra} [{tag}]")
