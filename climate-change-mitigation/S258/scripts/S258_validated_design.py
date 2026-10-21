#!/usr/bin/env python3
"""S258 (UPR run #1026): re-run the S257 paired-disc composite model on registry parameters
VALIDATED against primary documents, compare to the correct Puro Table 11.2 per-plot benchmarks,
quantify the R/a and h/a design rule, and evaluate Cascade's suggested 50% site-reuse cap.
Model identical to S257_registry_design.py (spherical covariance, nugget fraction f, range a,
destructive coring => distinct cores never share nugget). n = NU0 * V/sigma^2, NU0 = 107.2
(x=0.05, SD 0.00094, target relSD 0.15)."""
import math
import numpy as np
rng = np.random.default_rng(258)
B, S = 0.7035, 0.7150; SB = S-B; SIG = 0.00094; X = 0.05; T = 0.15
NU0 = (1-X)**2*SIG**2/(SB**2*X**2*T**2)

def c_rel(d, f, a):
    r = np.minimum(d/a, 1.0)
    return np.where(d == 0, 1.0, (1-f)*(1-(1.5*r-0.5*r**3)))

def disc(k, R, c):
    if R == 0: return np.tile(c, (k, 1))
    rr = R*np.sqrt(rng.uniform(size=k)); th = rng.uniform(0, 2*np.pi, k)
    return np.c_[rr*np.cos(th), rr*np.sin(th)] + c

def cbar(P, Q, f, a, same):
    d = np.sqrt(((P[:, None, :]-Q[None, :, :])**2).sum(-1)); c = c_rel(d, f, a)
    if not same: c = np.where(d == 0, 1-f, c)
    return c.mean()

def vrel(k, R, h, f, a, paired=True, reps=1500):
    acc = 0.0
    for _ in range(reps):
        P = disc(k, R, np.zeros(2))
        if paired:
            th = rng.uniform(0, 2*np.pi); ctr = h*np.array([np.cos(th), np.sin(th)])
        else:
            ctr = np.array([1e6, 0.0])
        Q = disc(k, R, ctr)
        acc += 0.5*(cbar(P, P, f, a, True)+cbar(Q, Q, f, a, True)) - cbar(P, Q, f, a, False)
    return 2*acc/reps

def ceil3(x): return 3*math.ceil(x/3 - 1e-12)
print("== Puro Eq 11.4 check: N_min = max(9, ceil(3*sqrt(A),3)); 2-plot app = 2/3, 3-plot eval = 1/3")
for A in [10, 50, 100, 500, 1000, 5000]:
    N = max(9, ceil3(3*math.sqrt(A)))
    print(f"  A={A:5d} ha: N_min={N:4d}  2-plot application={2*N//3:4d}  3-plot evaluation={N//3:4d}")
print(f"NU0 = {NU0:.1f}\n")

proxies = [('ExCa', 0.408, 20.5), ('ExMg', 0.452, 28.4), ('TotSr f=.25', 0.25, 30.0)]
designs = [('Puro literal min k=5 R=5', 5, 5.0), ('Puro k=15 R=5 (R floor)', 15, 5.0),
           ('Puro k=15 R=15', 15, 15.0), ('Isometric PDD Darjeeling k=15 R=4.6', 15, 4.6),
           ('Isometric PDD Mombak k=10 R=1', 10, 1.0), ('tight k=15 R=1', 15, 1.0)]
H = [0.02, 1.0, 2.5, 5.0, 10.0]
print("== Required n per stratum-plot per campaign (x=0.05); benchmark: Puro 10 ha treated plot = 8 (2-plot) / 4 (3-plot)")
res = {}
for pn, f, a in proxies:
    print(f"-- proxy {pn} f={f} a={a} m")
    print(f"{'design':38s} {'unpaired':>8s} " + " ".join(f"h={h:>5}" for h in H))
    for dn, k, R in designs:
        vu = vrel(k, R, 0, f, a, paired=False, reps=500)
        vs = [vrel(k, R, h, f, a) for h in H]
        res[(pn, dn)] = (vu, vs)
        print(f"{dn:38s} {math.ceil(NU0*vu):8d} " + " ".join(f"{math.ceil(NU0*v):7d}" for v in vs))

print("\n== R/a x h/a rule (k=15): n / n(R=0,h=0) inflation, ExCa f=0.408 and TotSr f=0.25 (a fixed, scale-free in R/a, h/a)")
for pn, f, a in [proxies[0], proxies[2]]:
    base = vrel(15, 0.0, 0.0, f, a, reps=200)
    ratios = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]
    print(f"-- {pn}: n at R=0,h=0 = {math.ceil(NU0*base)} (k=15 composites of coincident cores: nugget/15)")
    print(f"{'R/a \\ h/a':>10s} " + " ".join(f"{r:>6}" for r in ratios))
    for rR in ratios:
        row = [vrel(15, rR*a, rh*a, f, a, reps=800)/base for rh in ratios]
        print(f"{rR:>10} " + " ".join(f"{v:6.2f}" for v in row))

print("\n== Cascade 50% site-reuse cap (anti-gaming): inverse-variance mix of paired (Vp) and unpaired (Vu) sites")
print("   1/V_eff = q/Vp + (1-q)/Vu ; n = NU0*V_eff")
for pn, dn in [('ExCa', 'Isometric PDD Darjeeling k=15 R=4.6'), ('ExCa', 'Isometric PDD Mombak k=10 R=1'), ('TotSr f=.25', 'tight k=15 R=1')]:
    vu, vs = res[(pn, dn)]
    for hi, h in enumerate(H):
        if h not in (1.0, 5.0): continue
        vp = vs[hi]
        line = []
        for q in [1.0, 0.75, 0.5, 0.0]:
            veff = 1/(q/vp + (1-q)/vu)
            line.append(f"q={q}:{math.ceil(NU0*veff)}")
        print(f"  {pn:12s} {dn:36s} h={h:>4}m  " + "  ".join(line))
