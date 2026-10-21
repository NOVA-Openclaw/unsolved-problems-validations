
# S49 toy checks for Fu 2610.16445 Lemma 5.2.1 (twisted Lang isogeny) and the implicit steps.
from fractions import Fraction
from itertools import permutations
import math
def det(M):
    M=[[Fraction(x) for x in r] for r in M]; n=len(M); d=Fraction(1)
    for c in range(n):
        p=next((r for r in range(c,n) if M[r][c]!=0),None)
        if p is None: return Fraction(0)
        if p!=c: M[c],M[p]=M[p],M[c]; d=-d
        d*=M[c][c]
        for r in range(c+1,n):
            f=M[r][c]/M[c][c]
            for k in range(c,n): M[r][k]-=f*M[c][k]
    return d
print("Check A: theta = Coxeter n-cycle on X_*(T_der) for Ghat_der=SL_n; |ker L_theta| = |det(theta-1)|, finite <=> elliptic")
for n in range(2,8):
    # basis of sum-zero lattice e_i - e_{i+1}, i=0..n-2 ; theta permutes coords cyclically
    B=[[1 if j==i else (-1 if j==i+1 else 0) for j in range(n)] for i in range(n-1)]
    def coords(v):  # express sum-zero v in basis B: c_i = v_0+...+v_i
        out=[];s=0
        for i in range(n-1): s+=v[i]; out.append(s)
        return out
    cyc=lambda v:[v[-1]]+v[:-1]
    Th=[coords(cyc(b)) for b in B]  # rows = images
    M=[[Th[i][j]-(1 if i==j else 0) for j in range(n-1)] for i in range(n-1)]
    d=det(M); print(f"  n={n}: det(theta-1)={d}  ->  |(T_der)^theta| = {abs(d)} (expected n={n}, = |Z(SL_n)| ) ok={abs(d)==n}")
print("Check B: non-elliptic theta (identity) gives det 0 -> L_theta not an isogeny (ellipticity is needed)")
print("  det(0 matrix)=",det([[0,0],[0,0]]))
print("Check C: s of order m with gcd(m,q)=1 => s is a power of s^q, so Z(s^q)=Z(s) (used implicitly for x = t n)")
bad=0
for m in range(2,60):
    for q in [2,3,4,5,7,8,9,11,25,27,49]:
        if math.gcd(m,q)!=1: continue
        if not any(pow(q,k,m)==1 for k in range(1,m+1)): bad+=1
print("  counterexamples:",bad)
print("  |T(F_q)| for split rank-r torus = (q-1)^r, nonsplit rank-1 = q+1: both prime to p ->", all(math.gcd((q-1)*(q+1),q)==1 for q in [2,3,4,5,7,8,9,11,25,27,49]))
print("Check D: 'regular semisimple => centralizer is a torus' fails without connectedness when Ghat_der not simply connected")
# PGL2: s=diag(1,-1); w=[[0,1],[1,0]]; w s w^-1 = diag(-1,1) = -s, equal to s in PGL2
s=[[1,0],[0,-1]]; w=[[0,1],[1,0]]
mul=lambda A,B:[[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
wsw=mul(mul(w,s),w)
print("  w s w^-1 =",wsw,"= -s:",wsw==[[-x for x in r] for r in s],"-> in PGL2 the centralizer of s is T u wT (disconnected).")
print("  => Fu's 'T_s := Z(s) is a maximal torus' relies on DR09's regularity definition (centralizer of phi(I) a torus), not plain regular semisimplicity.")

