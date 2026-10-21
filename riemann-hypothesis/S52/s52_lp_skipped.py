#!/usr/bin/env python3
"""S52: re-solve the data points s52_lp_stress.py dropped (SLSQP constraint violation > 1e-7) with an
EXACT closed-form KKT solve. Block-constant optimum; SW=0 is optimal when unconstrained optimum has SW>0
(cost increases in |SW|, SW<=0 only pushes mass elsewhere). Enumerate active sets exactly with Fractions."""
import itertools
from fractions import Fraction as F
from mpmath import mp, mpf, sqrt
mp.dps=40; r2=sqrt(2); Astar=mpf(5)/2+r2; A1=2+r2
fE=lambda A:(5+2*r2-2*A)/(3+2*r2); fEp=lambda A:(4-A)/A
exec(open('s52_lp_stress.py').read().split('worstE =')[0])  # reuse minq definition only
def exact(n,r,p,q,N):
    DU,k,LU=r+p+q,p+q,2*r+2*p+4*q
    best=None
    # candidate: weights w=(DU,n,k); minimise sum S_i^2/w_i s.t. sum=N, SU>=LU, SM<=n, SW<=0
    blocks=[(DU,'U'),(n,'M'),(k,'W')]
    for fix in itertools.product([None,'lo'],[None,'hi'],[None,'hi']):
        fixed={}
        if fix[0]: fixed['U']=F(LU)
        if fix[1]: fixed['M']=F(n)
        if fix[2]: fixed['W']=F(0)
        for w,nm in blocks:
            if w==0: fixed[nm]=F(0)
        free=[(w,nm) for w,nm in blocks if nm not in fixed]
        rest=F(N)-sum(fixed.values()); W=sum(w for w,_ in free)
        S=dict(fixed)
        if free:
            if W==0: continue
            for w,nm in free: S[nm]=rest*w/W
        elif rest!=0: continue
        if S['U']<LU or S['M']>n or S['W']>0: continue
        Q=sum(S[nm]**2/w for w,nm in blocks if w)
        if best is None or Q<best: best=Q
    return best
bad=[]
R=range(0,9)
for n,r,p,q in itertools.product(R,R,R,R):
    if n+r+p+q==0: continue
    for e in (0,1,2,5,10,25):
        if e and r+q==0: continue
        N=n+2*r+2*p+4*q+e
        Q,viol=minq(n,r,p,q,N)
        if viol>1e-7: bad.append((n,r,p,q,N,float(viol)))
print("dropped by SLSQP:",len(bad))
for n,r,p,q,N,v in bad:
    Q=exact(n,r,p,q,N); A=mpf(Q.numerator)/Q.denominator/N; ratio=mpf(n+2*r+2*p)/N
    s1=ratio-fE(A) if A<Astar else None; s2=ratio-fEp(A) if A1<=A<4 else None
    print(f"  {(n,r,p,q,N)} viol={v:.2e} exact A_min={Q/N} ={mp.nstr(A,10)} slackE={mp.nstr(s1,8) if s1 is not None else 'n/a'} slackE'={mp.nstr(s2,8) if s2 is not None else 'n/a'}")
