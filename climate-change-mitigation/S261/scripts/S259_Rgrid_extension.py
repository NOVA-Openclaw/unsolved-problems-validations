#!/usr/bin/env python3
"""S259 (UPR run #1031): extend the S258 optimal-R scan past R=30 m and quantify the flatness of the
minimum. Model identical to S258_validated_design.py / S258_optimal_R.py (spherical covariance,
nugget fraction f, range a; destructive coring so distinct cores never share nugget;
n = NU0 * V/sigma^2, NU0 = 107.2 at x=0.05, SD 0.00094, target relSD 0.15).

Change vs S258: COMMON RANDOM NUMBERS. For each replicate we draw k unit-disc points for the pre and
post composites and one offset direction ONCE, then scale by R and h. The whole n(R) curve is therefore
evaluated on the same random geometry, so argmin_R is not driven by independent MC noise per cell
(S258 drew fresh geometry per cell). We report the continuous n (NU0*V), its ceil, R* (argmin of the
continuous curve), the MC standard error at R*, and the near-optimal band {R : n(R) <= n* + 1}.
"""
import math, sys
import numpy as np

SEED = 259
B, S = 0.7035, 0.7150; SB = S - B; SIG = 0.00094; X = 0.05; T = 0.15
NU0 = (1 - X)**2 * SIG**2 / (SB**2 * X**2 * T**2)

def c_rel(d, f, a):
    r = np.minimum(d / a, 1.0)
    return np.where(d == 0, 1.0, (1 - f) * (1 - (1.5 * r - 0.5 * r**3)))

def geometry(k, reps, rng):
    def unit(n):
        rr = np.sqrt(rng.uniform(size=(reps, n))); th = rng.uniform(0, 2*np.pi, (reps, n))
        return np.stack([rr*np.cos(th), rr*np.sin(th)], -1)
    U, W = unit(k), unit(k)
    ph = rng.uniform(0, 2*np.pi, reps)
    D = np.stack([np.cos(ph), np.sin(ph)], -1)
    return U, W, D

def vrel_curve(U, W, D, Rs, h, f, a):
    """Per-replicate V/sigma^2 for each R (common geometry). Returns array (len(Rs), reps)."""
    out = []
    for R in Rs:
        P = R * U
        Q = R * W + h * D[:, None, :]
        def cb(A, Bm, same):
            d = np.sqrt(((A[:, :, None, :] - Bm[:, None, :, :])**2).sum(-1))
            c = c_rel(d, f, a)
            if not same: c = np.where(d == 0, 1 - f, c)
            return c.mean(axis=(1, 2))
        out.append(2 * (0.5 * (cb(P, P, True) + cb(Q, Q, True)) - cb(P, Q, False)))
    return np.array(out)

def main():
    rng = np.random.default_rng(SEED)
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    Rs = [0.5, 1, 2, 3, 5, 7.5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100, 150]
    proxies = [('ExCa', 0.408, 20.5), ('ExMg', 0.452, 28.4), ('TotSr f=.25', 0.25, 30.0)]
    H = [0.5, 1.0, 2.5, 5.0, 10.0, 15.0]
    print(f"NU0 = {NU0:.2f}   reps = {reps}   seed = {SEED}")
    print("Asymptote check: as R -> inf all cores decorrelate: V/sig^2 -> 2/k (paired == unpaired), n_inf = ceil(NU0*2/k)")
    for k in (15, 30):
        print(f"   k={k}: n_inf = {math.ceil(NU0*2/k)}  (NU0*2/k = {NU0*2/k:.2f})")
    summary = []
    for pn, f, a in proxies:
        for k in (15, 30):
            U, W, D = geometry(k, reps, rng)
            print(f"\n-- {pn} (f={f}, a={a} m), k={k}: continuous n(R) = NU0*V/sig^2")
            print(f"{'h':>5s} " + " ".join(f"{R:>6}" for R in Rs) + " |   R*   n*  se  R*/h  band(n<=n*+1)       R15 n")
            for h in H:
                V = vrel_curve(U, W, D, Rs, h, f, a)
                n = NU0 * V.mean(1)
                i = int(np.argmin(n)); nstar = n[i]
                se = NU0 * V[i].std(ddof=1) / math.sqrt(reps)
                band = [R for R, v in zip(Rs, n) if v <= nstar + 1.0]
                edge = ' EDGE' if i == len(Rs) - 1 else ''
                n15 = n[Rs.index(15)]
                print(f"{h:5.1f} " + " ".join(f"{v:6.2f}" for v in n) +
                      f" | {Rs[i]:>5} {nstar:5.2f} {se:4.2f} {Rs[i]/h:5.1f}  [{min(band)}-{max(band)}]{edge}  {n15:6.2f}")
                summary.append((pn, k, h, Rs[i], nstar, Rs[i]/h, min(band), max(band), n15, math.ceil(nstar), math.ceil(n15)))
    print("\n== SUMMARY (R* on continuous n; band = R with n <= n*+1; ceil for sample counts)")
    print(f"{'proxy':12s} {'k':>3s} {'h':>5s} {'R*':>5s} {'n*':>6s} {'ceil':>4s} {'R*/h':>5s} {'band':>11s} {'bandlo/h':>8s} {'n@R15':>6s} {'ceil':>4s}")
    for pn, k, h, R, ns, rh, lo, hi, n15, cs, c15 in summary:
        print(f"{pn:12s} {k:3d} {h:5.1f} {R:5} {ns:6.2f} {cs:4d} {rh:5.1f} {f'[{lo}-{hi}]':>11s} {lo/h:8.1f} {n15:6.2f} {c15:4d}")

if __name__ == '__main__':
    main()
