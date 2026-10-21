#!/usr/bin/env python3
"""S308 r2 — POST-HOC diagnostics (written 2026-10-14 by the finishing executor, AFTER s308_check.py
reported N4b/N4c/N5b FAIL). Disclosed as post-hoc in S308-validate.md §6. Does not overwrite or alter
s308_check.py / s308_output.txt; preregistered scoring of those items is unchanged.

(A) N4c adjudication: reproduce the identical 12 beta=1/2 schemes (random.seed(308) is set at import of
    s308_check; make_scheme is the only consumer of `random`, called in the same order) and decompose each
    scheme's worst-tau bound 1-delta-a2-a3 into (delta=1-Et, a2=Ef2, a3=EF) and compare with the exact
    decoder success. Question: is vacuity a theorem defect (success < bound would be; N4a already says
    no) or a generator-power issue (the schemes are simply bad estimators / carry too much lie mass)?
(B) N5b adjudication: reproduce the IDENTICAL N5 Monte Carlo draws (NPR = default_rng(308) at import,
    same call sequence) and re-test the z-law with valid small-count statistics:
      - per-cell exact two-sided binomial tail p-values, Bonferroni over all cells x 9 cases at family
        level 1e-3 (the original per-cell bar 4.5 sd x 256 cells x 9 cases ~ 1.6e-2 family nominal, but its
        normal approximation is invalid for cells with R*p << 1);
      - Pearson chi-square on cells with E >= 5 (rest pooled), z = (chi2-df)/sqrt(2df) < 4;
      - for the original max-dev cell: exact p, E, observed count.
"""
import math, sys, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy import stats

sys.path.insert(0, '.')
import s308_check as C  # seeds random(308) and NPR(308) at import

configs = [(Fr(1, 2), 4), (Fr(1, 4), 3)]
laws = {}
for beta, c0 in configs:
    for tau in C.TAUS:
        laws[(beta, tau)] = C.z_law(beta, tau, c0)
print("z-laws computed", flush=True)

schemes = []
for beta, c0 in configs:
    for sidx in range(12):
        schemes.append(C.make_scheme(beta, c0, C.random))

# ---------------- (A) ----------------
print("== (A) N4c decomposition, beta=1/2 schemes (worst tau by bound) ==", flush=True)
a_rows = []
for sidx, S in enumerate(schemes[:12]):
    beta = S['beta']
    worst = None
    minsucc = Fr(2)
    for tau in C.TAUS:
        Eg = EF = Et = Ef2 = succ = Fr(0)
        for z, pz in laws[(beta, tau)].items():
            H, f, t, f2 = C.coin_measures(S, z, tau)
            F = max(f.values())
            ok = 1 if C.decode(H) == tau else 0
            Eg += pz * H[tau]; EF += pz * F; Et += pz * t; Ef2 += pz * f2; succ += pz * ok
        bound = Et - Ef2 - EF
        minsucc = min(minsucc, succ)
        if worst is None or bound < worst[0]:
            worst = (bound, 1 - Et, Ef2, EF, succ, Eg - EF, tau)
    b, dl, a2, a3, sc, gm, tau = worst
    a_rows.append((sidx, worst, minsucc))
    print(f" #{sidx:2d} bound={float(b):+.4f} delta={float(dl):.4f} a2={float(a2):.4f} a3={float(a3):.4f} "
          f"Eg-EF={float(gm):+.4f} succ@tau={float(sc):.4f} min_tau succ={float(minsucc):.4f} "
          f"{'VACUOUS(<0.3)' if b < Fr(3,10) else 'ok'}", flush=True)
vac = [r for r in a_rows if r[1][0] < Fr(3, 10)]
nonvac = [r for r in a_rows if r[1][0] >= Fr(3, 10)]
def mean(xs):
    xs = [float(x) for x in xs]
    return sum(xs) / max(len(xs), 1)
print(f" vacuous n={len(vac)}: mean delta={mean(r[1][1] for r in vac):.4f} a2={mean(r[1][2] for r in vac):.4f} a3={mean(r[1][3] for r in vac):.4f}")
print(f" non-vac n={len(nonvac)}: mean delta={mean(r[1][1] for r in nonvac):.4f} a2={mean(r[1][2] for r in nonvac):.4f} a3={mean(r[1][3] for r in nonvac):.4f}")
violations = sum(1 for r in a_rows if r[1][4] < r[1][0])
print(f"[{'PASS' if violations == 0 else 'FAIL'}] R2-A success >= bound at worst tau for all 12 beta=1/2 schemes (violations={violations})")

# ---------------- (B) ----------------
print("== (B) N5b re-test on identical N5 draws ==", flush=True)
R = 20000
cases = []
for S in schemes[:3]:
    beta = S['beta']
    for tau in [C.TAUS[0], C.TAUS[5], C.TAUS[15]]:
        law = laws[(beta, tau)]
        pv = np.array([float(C.p(beta, tau, e)) for e in C.ELEMS])
        counts = C.NPR.multinomial(C.N, pv, size=R)
        zc = {}
        for row in counts:
            z = tuple(C.zi_of(int(row[2 * i]), int(row[2 * i + 1]), S['c0']) for i in range(C.M))
            zc[z] = zc.get(z, 0) + 1
            C.NPR.random()  # consume the coin draw exactly as N5 did (one per row)
        cases.append((beta, tau, law, zc))
ncells = sum(len(c[2]) for c in cases)
thr = 1e-3 / ncells
ok_binom = True
ok_chi = True
impossible = 0
for beta, tau, law, zc in cases:
    impossible += sum(1 for z in zc if z not in law)
    worst = None
    minp = 1.0
    for z, pz in law.items():
        pf = float(pz); k = zc.get(z, 0)
        sd = math.sqrt(max(pf * (1 - pf), 1e-12) / R)
        dv = abs(k / R - pf) / sd
        if worst is None or dv > worst[0]:
            worst = (dv, pf, pf * R, k)
        lo = stats.binom.cdf(k, R, pf); hi = stats.binom.sf(k - 1, R, pf)
        pv2 = min(1.0, 2 * min(lo, hi))
        minp = min(minp, pv2)
    if minp < thr:
        ok_binom = False
    chi = 0.0; df = -1; pe = 0.0; po = 0
    for z, pz in law.items():
        e = float(pz) * R
        if e >= 5:
            chi += (zc.get(z, 0) - e) ** 2 / e; df += 1
        else:
            pe += e; po += zc.get(z, 0)
    if pe >= 5:
        chi += (po - pe) ** 2 / pe; df += 1
    zst = (chi - df) / math.sqrt(2 * df)
    if zst >= 4:
        ok_chi = False
    print(f"   beta={beta} tau={tau}: orig max-dev {worst[0]:.2f} sd at p={worst[1]:.2e} (E={worst[2]:.4f}, obs={worst[3]}); "
          f"min exact binom p={minp:.2e} (Bonf thr {thr:.1e}); chi2={chi:.1f} df={df} z={zst:+.2f}", flush=True)
print(f"[{'PASS' if ok_binom and impossible == 0 else 'FAIL'}] R2-B1 exact binomial per-cell, Bonferroni family 1e-3, no impossible cells (impossible={impossible})")
print(f"[{'PASS' if ok_chi else 'FAIL'}] R2-B2 pooled chi-square z<4 on identical N5 draws")
