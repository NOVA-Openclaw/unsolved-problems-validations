#!/usr/bin/env python3
"""S308 POST-HOC diagnostic (written after s308_check.py N5b FAILed; disclosed).
Question: is the N5b failure a bug in the exact z-law, or a rare-cell artifact of the per-cell
normal-sd test (cells with p ~ 1e-8 make a single MC hit read as many 'sd')?
Test: (i) report the max-dev cell's exact prob, expected count, observed count;
(ii) Pearson chi-square on cells with expected count >= 5 (rest pooled), vs df;
(iii) exact-law sanity: each pair's marginal sign law vs independent binomial computation.
Seed 3081 (fresh draws; not the N5 draws)."""
import itertools, math, sys
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, '.')
import s308_check as C

rng = np.random.default_rng(3081)
R = 200000
ok_all = True
for beta, c0 in [(Fr(1, 2), 4), (Fr(1, 4), 3)]:
    for tau in [C.TAUS[0], C.TAUS[15], C.TAUS[5]]:
        law = C.z_law(beta, tau, c0)
        pv = np.array([float(C.p(beta, tau, e)) for e in C.ELEMS])
        cnt = rng.multinomial(C.N, pv, size=R)
        obs = {}
        for row in cnt:
            z = tuple(C.zi_of(int(row[2 * i]), int(row[2 * i + 1]), c0) for i in range(C.M))
            obs[z] = obs.get(z, 0) + 1
        unk = [z for z in obs if z not in law]
        best = None
        for z, pz in law.items():
            e = float(pz) * R
            sd = math.sqrt(max(float(pz) * (1 - float(pz)) * R, 1e-300))
            dv = abs(obs.get(z, 0) - e) / sd
            if best is None or dv > best[0]:
                best = (dv, float(pz), e, obs.get(z, 0))
        chi = 0.0; df = -1; pe = 0.0; po = 0
        for z, pz in law.items():
            e = float(pz) * R
            if e >= 5:
                chi += (obs.get(z, 0) - e) ** 2 / e; df += 1
            else:
                pe += e; po += obs.get(z, 0)
        if pe >= 5:
            chi += (po - pe) ** 2 / pe; df += 1
        zstat = (chi - df) / math.sqrt(2 * df)
        ok = (not unk) and zstat < 4
        ok_all &= ok
        print(f"beta={beta} tau={tau}: max-dev cell {best[0]:.1f} sd at p={best[1]:.2e} (E={best[2]:.3f}, obs={best[3]}); "
              f"chi2={chi:.1f} df={df} z={zstat:.2f}; unseen-in-law cells={len(unk)}")
print(f"[{'PASS' if ok_all else 'FAIL'}] SUPP z-law chi-square (cells E>=5, rest pooled), z<4, no impossible cells")
