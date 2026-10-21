#!/usr/bin/env python3
"""S260 (UPR run #1038): cost optimisation of Sr-tracer ERW MRV sampling designs.

Regime A: RTK-grade paired composites (h = 0.5 or 1 m), tight disc radius R, k cores per composite.
Regime H: handheld-GPS paired composites (h = 5 or 10 m) -- reference; S259 showed ~ unpaired.
Regime B: unpaired composites whose k cores are spread at random over the stratum (V/sig^2 = 2/k).
Hybrid (Cascade q cap): fraction q of sites RTK-paired tight, (1-q) fresh WIDE unpaired composites.

Variance model: identical to S259_Rgrid_extension.py (imported), common random numbers, seed 260.
n (sites per campaign, each site = 1 baseline + 1 post composite) = ceil(NU0 * V/sig^2), NU0=107.2.

COST INPUTS ARE ASSUMPTIONS (not measured; flagged in the artifact). Per stratum-plot (10 ha),
per baseline+post campaign pair:
  lab      c_lab per composite analysed (2n composites): 116 / 300 / 500 USD (S255 range)
  coring   t_core min per core, all regimes (auger, bag, log)          : 3 min
  labour   L USD/h field tech all-in                                    : 60
  walking  TSP tour 0.7124*sqrt(N*A) (Beardwood-Halton-Hammersley), v = 0.8 m/s, A = 1e5 m^2
           A/H: tour over n site centres (intra-disc walking ~2R per core, added)
           B  : tour over all n*k core locations
  RTK      stake-out/relocation t_rtk min per site per visit          : 3 min
           RTK rover rental c_rtk per field day (8 h), per visit        : 250 USD
Mobilisation/travel is common to all regimes and excluded.
"""
import math, sys
import numpy as np
sys.path.insert(0, '.')
from S259_Rgrid_extension import NU0, geometry, vrel_curve

SEED = 260
A = 1e5; V_WALK = 0.8; T_CORE = 3.0; L = 60.0; T_RTK = 3.0; C_RTK = 250.0
LABS = [116.0, 300.0, 500.0]
PROXIES = [('ExCa', 0.408, 20.5), ('ExMg', 0.452, 28.4), ('TotSr', 0.25, 30.0)]
KS = [5, 10, 15, 20, 30, 40, 54, 60, 80]
RS = [0.5, 1, 2, 3, 5, 7.5, 10, 15]
BENCH = {'2-plot': 8, '3-plot': 4}

def tsp(N):
    return 0.7124 * math.sqrt(N * A)

def field_hours(n, k, regime, R=0.0):
    """Field hours for ONE visit (baseline OR post)."""
    cores = n * k
    if regime == 'B':
        walk_m = tsp(cores)
        extra_min = 0.0
    else:
        walk_m = tsp(n) + cores * 2 * R          # tour of sites + intra-disc
        extra_min = n * T_RTK if regime == 'A' else 0.0
    return (cores * T_CORE + extra_min) / 60.0 + walk_m / V_WALK / 3600.0

def cost(n, k, regime, c_lab, R=0.0):
    hrs = field_hours(n, k, regime, R)
    c = 2 * n * c_lab + 2 * hrs * L
    if regime == 'A':
        c += 2 * math.ceil(hrs / 8.0) * C_RTK
    return c, 2 * hrs

def main():
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    rng = np.random.default_rng(SEED)
    print(f"NU0={NU0:.2f} reps={reps} seed={SEED}  A={A/1e4:.0f} ha  t_core={T_CORE} min  L=${L}/h  "
          f"t_rtk={T_RTK} min  RTK=${C_RTK}/day  v={V_WALK} m/s")
    # 1. paired V/sig^2 tables (continuous) for each proxy, k, h, best R
    VP = {}
    for pn, f, a in PROXIES:
        for k in KS:
            U, W, D = geometry(k, reps, rng)
            for h in (0.5, 1.0, 5.0, 10.0):
                V = vrel_curve(U, W, D, RS, h, f, a).mean(1)
                for R, v in zip(RS, V):
                    VP[(pn, k, h, R)] = v
    # 2. per-design cost and minimum-cost design by regime
    rows = []
    for pn, f, a in PROXIES:
        for c_lab in LABS:
            best = {}
            for k in KS:
                nB = math.ceil(NU0 * 2.0 / k)
                cB, hB = cost(nB, k, 'B', c_lab)
                rows.append((pn, c_lab, 'B', k, None, None, nB, cB, hB))
                for h in (0.5, 1.0, 5.0, 10.0):
                    reg = 'A' if h <= 1.0 else 'H'
                    for R in RS:
                        n = math.ceil(NU0 * VP[(pn, k, h, R)])
                        c, hh = cost(n, k, reg, c_lab, R)
                        rows.append((pn, c_lab, f'{reg}{h:g}', k, h, R, n, c, hh))
    import collections
    print("\n== MIN-COST design per regime (unconstrained n), per 10 ha plot, baseline+post")
    print(f"{'proxy':6s} {'lab$':>5s} {'reg':>5s} {'k':>3s} {'R':>5s} {'n':>4s} {'cost$':>8s} {'fieldh':>7s}")
    grp = collections.defaultdict(list)
    for r in rows: grp[(r[0], r[1], r[2])].append(r)
    mins = {}
    for key in sorted(grp, key=lambda x: (x[0], x[1], x[2])):
        r = min(grp[key], key=lambda t: t[7]); mins[key] = r
        print(f"{r[0]:6s} {r[1]:5.0f} {r[2]:>5s} {r[3]:3d} {str(r[5]):>5s} {r[6]:4d} {r[7]:8.0f} {r[8]:7.1f}")
    print("\n== MIN-COST design meeting a registry count (n <= 8 '2-plot', n <= 4 '3-plot')")
    for bname, bn in BENCH.items():
        print(f"-- {bname} (n <= {bn})")
        for key in sorted(grp, key=lambda x: (x[0], x[1], x[2])):
            ok = [t for t in grp[key] if t[6] <= bn]
            if not ok:
                print(f"{key[0]:6s} {key[1]:5.0f} {key[2]:>5s}  infeasible in grid (k<=80)"); continue
            r = min(ok, key=lambda t: t[7])
            print(f"{r[0]:6s} {r[1]:5.0f} {r[2]:>5s} k={r[3]:3d} R={str(r[5]):>5s} n={r[6]:3d} cost=${r[7]:7.0f} fieldh={r[8]:5.1f}")
    # 3. cost ratio A(best of h=0.5/1)/B at the unconstrained optimum
    print("\n== Ratio best-A / best-B (unconstrained)")
    for pn, *_ in PROXIES:
        for c_lab in LABS:
            a_ = min(mins[(pn, c_lab, 'A0.5')][7], mins[(pn, c_lab, 'A1')][7])
            b_ = mins[(pn, c_lab, 'B')][7]
            print(f"{pn:6s} lab ${c_lab:3.0f}: A=${a_:6.0f} B=${b_:6.0f} ratio={a_/b_:4.2f}")
    # 4. Cascade q cap: hybrid of paired tight (RTK) and fresh WIDE unpaired vs fresh TIGHT unpaired
    print("\n== Cascade q-cap penalty: n(q) / n(q=1) for best RTK design, fresh sites TIGHT vs WIDE")
    for pn, f, a in PROXIES:
        for k in (15, 30):
            for h in (0.5, 1.0):
                # best R at this k,h
                R = min(RS, key=lambda R: VP[(pn, k, h, R)])
                vp = VP[(pn, k, h, R)]
                # tight unpaired: pre and post composites at independent locations -> V = 2*var(mean of tight disc)
                # var(mean)/sig^2 = within-disc mean covariance = 0.5*V(h=inf) ; approximate via h=10 at R (a>=20)? compute exactly:
                rng2 = np.random.default_rng(SEED + k)
                U, W, D = geometry(k, reps, rng2)
                vt = vrel_curve(U, W, D, [R], 1e6, f, a).mean()     # h -> inf: independent tight discs
                vw = 2.0 / k
                out = []
                for q in (1.0, 0.75, 0.5):
                    nt = NU0 / (q / vp + (1 - q) / vt)
                    nw = NU0 / (q / vp + (1 - q) / vw)
                    out.append(f"q={q}: tight {math.ceil(nt):3d} wide {math.ceil(nw):3d}")
                print(f"{pn:6s} k={k:2d} h={h:3.1f} R*={R:>4}  vp={vp:.4f} vt={vt:.4f} vw={vw:.4f} | " + " | ".join(out))

if __name__ == '__main__':
    main()
