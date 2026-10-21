#!/usr/bin/env python3
"""S261 (UPR run #1042) VALIDATE: does within-composite mixing / subsampling error change the S260
recommendation (unpaired wide composites, k=27 floor-8 / k=54 floor-4)?

S259/S260 model: composite = exact equal-weight mean of its k cores, so V_B/sigma^2 = 2/k exactly.
S261 adds three per-composite error terms (all DERIVED from standard sampling theory; magnitudes ASSUMED
over a grid, then anchored in the artifact with Gy/TOS numbers):

 (1) phi   : fraction of the single-sample point variance sigma^2 that is PER-ANALYSIS (lab subsample
             fundamental sampling error FSE + instrument error). It does NOT average down with k.
 (2) CV_w  : coefficient of variation of core masses in the composite (unequal core volumes / bulk
             density). Weighted mean of k cores with weights w_i: Var = s_w^2 * sum w_i^2
             ~= s_w^2 (1+CV_w^2)/k  -> extra s_w^2 CV_w^2 / k.
 (3) N_c   : effective number of independent "mixing units" (clods / aggregates / unmixed pockets, each
             carrying one core's identity) that reach the analysed subsample. Multinomial draw of N_c
             units from k cores: E[sum w^2] = 1/N_c + (1-1/N_c)/k  -> extra ~ s_w^2 / N_c.
             This is the grouping-segregation (GSE) term of Gy/TOS expressed in core units.
 s_w^2 = within-composite between-core variance (relative to sigma^2): 1 for regime B (cores spread
 over the stratum, a << stratum), 1 - mean off-diagonal correlation for tight regime-A discs.

 V'/sigma^2 = (1-phi) * V_model + 2 (1-phi) s_w (CV_w^2/k + 1/N_c) + 2 phi       (pair of composites)
 n_stat = ceil(NU0 * V'),   design n = max(n_stat, floor).

Cost model imported unchanged from S260 (assumed inputs). Seed 261.
"""
import math, sys
import numpy as np
sys.path.insert(0, '.')
from S259_Rgrid_extension import NU0, geometry, vrel_curve, c_rel
from S260_cost_optimisation import cost, LABS, PROXIES

SEED = 261
reps = int(sys.argv[1]) if len(sys.argv) > 1 else 400
rng = np.random.default_rng(SEED)
KA = [5, 8, 10, 12, 15, 20, 30, 40, 54, 80]
RS = [0.5, 1, 2, 3, 5]
HS = (0.5, 1.0)

def sw_rel(U, R, f, a):
    """within-composite between-core variance / sigma^2 = 1 - mean off-diagonal correlation."""
    P = R * U
    d = np.sqrt(((P[:, :, None, :] - P[:, None, :, :])**2).sum(-1))
    c = c_rel(d, f, a)
    k = U.shape[1]
    off = (c.sum(axis=(1, 2)) - k) / (k * (k - 1))
    return float(1 - off.mean())

# ---- regime A tables (V_model and s_w) --------------------------------------------------------
VP, SW = {}, {}
for pn, f, a in PROXIES:
    for k in KA:
        U, W, D = geometry(k, reps, rng)
        for h in HS:
            V = vrel_curve(U, W, D, RS, h, f, a).mean(1)
            for R, v in zip(RS, V):
                VP[(pn, k, h, R)] = v
        for R in RS:
            SW[(pn, k, R)] = sw_rel(U, R, f, a)

def vprime(Vm, sw, k, phi, cvw, Nc):
    inv = 0.0 if Nc is None else 1.0 / Nc
    return (1 - phi) * Vm + 2 * (1 - phi) * sw * (cvw**2 / k + inv) + 2 * phi

def best_B(floor, c_lab, phi, cvw, Nc, kmax=2000):
    best = None
    for k in range(2, kmax + 1):
        ns = NU0 * vprime(2.0 / k, 1.0, k, phi, cvw, Nc)
        n = max(math.ceil(ns - 1e-9), floor, 1)
        c = cost(n, k, 'B', c_lab)[0]
        if best is None or c < best[0]:
            best = (c, k, n)
    # smallest k that reaches the floor (the S260 "design k")
    kfloor = next((k for k in range(2, kmax + 1)
                   if NU0 * vprime(2.0 / k, 1.0, k, phi, cvw, Nc) <= floor + 1e-9), None)
    return best, kfloor

def best_A(pn, floor, c_lab, phi, cvw, Nc):
    best = None
    for k in KA:
        for h in HS:
            for R in RS:
                ns = NU0 * vprime(VP[(pn, k, h, R)], SW[(pn, k, R)], k, phi, cvw, Nc)
                n = max(math.ceil(ns - 1e-9), floor, 1)
                c = cost(n, k, 'A', c_lab, R)[0]
                if best is None or c < best[0]:
                    best = (c, k, h, R, n)
    return best

def floor_infeasible(phi, Nc, floor):
    """Additive per-composite terms alone: NU0*2*(phi + (1-phi)/Nc) must be < floor for ANY k to work."""
    inv = 0.0 if Nc is None else 1.0 / Nc
    return NU0 * 2 * (phi + (1 - phi) * inv)

print(f"S261 composite-error model  NU0={NU0:.2f}  reps(A)={reps}  seed={SEED}")
print("\n[0] Reproduction check (phi=0, CV_w=0, N_c=inf must reproduce S260 floor addendum)")
for floor in (4, 8):
    for c_lab in LABS:
        (cB, kB, nB), kf = best_B(floor, c_lab, 0, 0, None)
        line = f"  floor {floor} lab ${c_lab:3.0f}: B ${cB:6.0f} (k={kB},n={nB}) kfloor={kf}"
        for pn, *_ in PROXIES:
            bA = best_A(pn, floor, c_lab, 0, 0, None)
            line += f" | {pn} A/B={bA[0]/cB:.2f}"
        print(line)

print("\n[1] Additive floor: NU0*2*(phi+(1-phi)/N_c) = n reachable only as k->inf (must be < floor)")
PHIS = [0, 1e-4, 1e-3, 3e-3, 1e-2, 3e-2]
NCS = [None, 10000, 1000, 300, 100, 30]
print("   phi \\ N_c " + " ".join(f"{('inf' if N is None else N):>7}" for N in NCS))
for phi in PHIS:
    print(f"   {phi:8.4f}  " + " ".join(f"{floor_infeasible(phi, N, 0):7.2f}" for N in NCS))

print("\n[2] Regime B: smallest k reaching the floor (kfloor), vs S260 (27 / 54). CV_w in {0,0.2,0.4}")
for floor in (8, 4):
    print(f"  floor {floor}:")
    for cvw in (0.0, 0.2, 0.4):
        print(f"   CV_w={cvw}: phi \\ N_c " + " ".join(f"{('inf' if N is None else N):>6}" for N in NCS))
        for phi in PHIS:
            row = []
            for N in NCS:
                _, kf = best_B(floor, 300, phi, cvw, N)
                row.append(f"{(kf if kf is not None else '  --'):>6}")
            print(f"      {phi:8.4f}          " + " ".join(row))

print("\n[3] Cost + A/B under realistic scenarios (lab $116/$300/$500)")
SCEN = [
    ("S260 ideal", 0, 0, None),
    ("good prep (split>=20g, pulverise): phi=1e-3 CV_w=0.2 N_c=1e4", 1e-3, 0.2, 10000),
    ("typical: phi=3e-3 CV_w=0.2 N_c=1000", 3e-3, 0.2, 1000),
    ("poor field mixing: phi=3e-3 CV_w=0.3 N_c=300", 3e-3, 0.3, 300),
    ("bad: 0.1-0.25 g unground total digest, bucket mix: phi=1e-2 CV_w=0.4 N_c=100", 1e-2, 0.4, 100),
    ("very bad: phi=3e-2 CV_w=0.4 N_c=30", 3e-2, 0.4, 30),
]
for name, phi, cvw, Nc in SCEN:
    print(f"\n  -- {name}   additive-floor n = {floor_infeasible(phi, Nc, 0):.2f}")
    for floor in (8, 4):
        for c_lab in LABS:
            (cB, kB, nB), kf = best_B(floor, c_lab, phi, cvw, Nc)
            ideal = best_B(floor, c_lab, 0, 0, None)[0][0]
            line = f"    floor {floor} lab ${c_lab:3.0f}: B ${cB:6.0f} (k={kB},n={nB},kfloor={kf}) x{cB/ideal:.2f} vs ideal"
            for pn, *_ in PROXIES:
                bA = best_A(pn, floor, c_lab, phi, cvw, Nc)
                line += f" | {pn} A ${bA[0]:6.0f} (k={bA[1]},h={bA[2]},R={bA[3]},n={bA[4]}) A/B={bA[0]/cB:.2f}"
            print(line)

print("\n[4] Within-composite s_w (regime A, tight discs) - why A is LESS exposed to CV_w/N_c terms")
for pn, f, a in PROXIES:
    print(f"  {pn}: " + "  ".join(f"k={k},R={R}:{SW[(pn,k,R)]:.2f}" for k in (15, 30) for R in (0.5, 2, 5)))
