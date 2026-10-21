#!/usr/bin/env python3
"""S49 VALIDATE: falsification test of Lamzouri Prop 2.1 ineq (2.7) OUTSIDE its stated hypothesis
(1<=A<2), i.e. with A := sum K(z-s)^2 / |Z| in [2, 5/2+sqrt2). S47's c2(theta) for theta<0.5502
needs exactly this regime. Our re-read of the proof says only 0<=A<5/2+sqrt2 is used (b1>0).
Also tests (2.6). K(xi) = int eta(u)^2 exp(-2 pi i xi u) du, eta^2 = normalized smooth bump on (-lam,lam).
Random conjugation-invariant multisets with multiplicities; counts computed exactly."""
import numpy as np
rng = np.random.default_rng(4949)
r2 = np.sqrt(2)

def make_K(lam, m=1201):
    u = np.linspace(-lam, lam, m)[1:-1]
    f = np.exp(-1/(1-(u/lam)**2))            # smooth bump; any even f>=0 with int f=1 qualifies (f=eta^2)
    f *= rng.uniform(0.5, 1.5)**0            # (keep deterministic shape)
    du = u[1]-u[0]; f /= f.sum()*du
    def K(xi):
        return (f[None, :]*np.exp(-2j*np.pi*np.asarray(xi)[:, None]*u[None, :])).sum(axis=1)*du
    return K

def random_multiset():
    pts = []
    nreal = rng.integers(0, 6); npair = rng.integers(0, 5)
    for _ in range(nreal):
        pts.append((complex(rng.normal(0, 1.0), 0.0), int(rng.choice([1, 1, 2, 3]))))
    for _ in range(npair):
        z = complex(rng.normal(0, 1.0), rng.normal(0, 0.5)*rng.choice([0.05, 0.3, 1.0]))
        m = int(rng.choice([1, 1, 2, 3]))
        pts.append((z, m)); pts.append((z.conjugate(), m))
    if not pts:
        pts = [(0j, 1)]
    return pts

worst27 = np.inf; worst26 = np.inf; worst24 = np.inf; nA2 = 0; ntot = 0; Amax = 0
for trial in range(20000):
    lam = rng.choice([0.05, 0.1, 0.2, 0.4, 0.8])
    K = make_K(lam) if trial % 50 == 0 or trial == 0 else K
    Z = random_multiset()
    elems = np.array([z for z, m in Z for _ in range(m)])
    N = len(elems)
    diffs = (elems[:, None]-elems[None, :]).ravel()
    S = np.sum(K(diffs)**2)
    assert abs(S.imag) < 1e-8*max(1, abs(S)), S
    S = S.real; A = S/N
    simple = sum(m for z, m in Z if m == 1)
    real = sum(m for z, m in Z if abs(z.imag) == 0)
    simple_real = sum(m for z, m in Z if m == 1 and abs(z.imag) == 0)
    s_or_r = sum(m for z, m in Z if m == 1 or abs(z.imag) == 0)
    worst24 = min(worst24, simple_real - (2*N - S))
    worst26 = min(worst26, simple + real - (3*N - S))
    if A < 2.5 + r2:
        ntot += 1
        if A >= 2: nA2 += 1; Amax = max(Amax, A)
        slack = s_or_r - (5+2*r2-2*A)/(3+2*r2)*N
        if A >= 2: worst27 = min(worst27, slack)
print(f"(2.4) min slack over all trials: {worst24:.4e}  (>= -1e-9 means holds)")
print(f"(2.6) min slack over all trials: {worst26:.4e}")
print(f"(2.7) trials with A<5/2+sqrt2: {ntot}; of which A in [2, 3.914): {nA2}; max A seen there {Amax:.3f}")
print(f"(2.7) min slack in the EXTENDED regime A>=2: {worst27:.4e}")
