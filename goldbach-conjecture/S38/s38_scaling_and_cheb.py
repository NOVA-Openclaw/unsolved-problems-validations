#!/usr/bin/env python3
"""S38 VALIDATE, claims (c) and (d). This is an independent implementation.
(c) CoV of y = r_un/(S*I) on [1000,50000] and on sliding windows. Test the
    ~1/sqrt(r) and ~1/sqrt(X) scaling hypotheses. Separate the within-window
    trend (drift) from the local scatter.
(d) S35/S36 partitioned Chebyshev correction. Implemented from the written
    definition (P_actual = sum_{a+b=n mod q} fL(a) fU(b), L=(q,n/2], U=(n/2,n])
    with (i) the correct denominator and (ii) the S35 denominator total_L - 1.
"""
import numpy as np
from scipy.integrate import quad
C2 = 0.66016181584686957

def sieve(N):
    s = np.ones(N + 1, dtype=bool); s[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if s[i]: s[i*i::i] = False
    return s

N = 200000
isp = sieve(N)
L = 1 << int(np.ceil(np.log2(2 * N + 2)))
f = np.fft.rfft(isp.astype(float), L)
r_ord = np.rint(np.fft.irfft(f * f, L)[:N + 1]).astype(np.int64)
sq = np.zeros(N + 1, dtype=np.int64); ps = np.nonzero(isp)[0]; sq[2 * ps[2 * ps <= N]] = 1
r_un = (r_ord + sq) // 2
S = np.full(N + 1, 2 * C2)
for p in ps[1:]: S[p::p] *= (p - 1) / (p - 2)

def Ihalf(n): return quad(lambda t: 1 / (np.log(t) * np.log(n - t)), 2, n / 2, limit=200)[0]
def Is37(n):
    ts = np.linspace(2, n / 2, 500); dt = ts[1] - ts[0]
    return np.sum(1 / (np.log(ts) * np.log(n - ts))) * dt

def cov(y): return y.std() / y.mean()

print("=== (c) [1000,50000] CoV under same conventions ===")
ev = np.arange(1000, 50001, 2)
Ia = np.array([Ihalf(n) for n in ev]); I37 = np.array([Is37(n) for n in ev])
y37 = r_un[ev] / (S[ev] * I37); ya = r_un[ev] / (S[ev] * Ia)
print(f"S37/S35 convention (500-pt Riemann I): mean {y37.mean():.6f}  var(y/mean) {np.var(y37/y37.mean()):.8f}  CoV {cov(y37)*100:.4f}%")
print(f"accurate I:                             mean {ya.mean():.6f}  var(y/mean) {np.var(ya/ya.mean()):.8f}  CoV {cov(ya)*100:.4f}%")
# drift: linear fit of y vs log n, residual CoV
for lab, y in (("S37 conv", y37), ("accurate", ya)):
    X = np.vstack([np.ones_like(ev, float), np.log(ev)]).T
    b = np.linalg.lstsq(X, y, rcond=None)[0]; res = y - X @ b
    print(f"  [{lab}] detrended (y - a - b log n) CoV {res.std()/y.mean()*100:.4f}%  slope b={b[1]:.5f}")

print("\n=== (c) window scan, width 5000 evens-span, y accurate; local-detrended scatter ===")
print(f"{'window':>18s} {'mean r':>9s} {'CoV%':>8s} {'CoVdetr%':>9s} {'1/sqrt(mean r)%':>16s} {'ratio':>7s}")
rows = []
for a in [2000, 5000, 10000, 20000, 40000, 80000, 100000, 140000, 190000]:
    b = a + 10000
    if b > N: b = N
    e = np.arange(a, b + 1, 2)
    I = np.array([Ihalf(n) for n in e]); y = r_un[e] / (S[e] * I)
    X = np.vstack([np.ones_like(e, float), np.log(e)]).T
    res = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
    mr = r_un[e].mean(); cv = cov(y); cvd = res.std() / y.mean(); pr = 1 / np.sqrt(mr)
    rows.append((np.mean(e), mr, cvd))
    print(f"[{a:6d},{b:6d}] {mr:9.1f} {cv*100:8.4f} {cvd*100:9.4f} {pr*100:16.4f} {cvd/pr:7.3f}")
rows = np.array(rows)
sl_X = np.polyfit(np.log(rows[:, 0]), np.log(rows[:, 2]), 1)[0]
sl_r = np.polyfit(np.log(rows[:, 1]), np.log(rows[:, 2]), 1)[0]
print(f"log-log slope of detrended CoV vs X: {sl_X:.3f}   (1/sqrt(X) predicts -0.5)")
print(f"log-log slope of detrended CoV vs mean r: {sl_r:.3f}   (1/sqrt(r) predicts -0.5)")
m1 = r_un[np.arange(1000, 50001, 2)].mean(); m2 = r_un[np.arange(100000, 120001, 2)].mean()
print(f"naive 1/sqrt(r) prediction for S37 CoV from 3.5484%: {3.5484*np.sqrt(m1/m2):.4f}%  (mean r {m1:.1f} -> {m2:.1f})")
print(f"naive 1/sqrt(Xmid) prediction: {3.5484*np.sqrt(25500/110000):.4f}%")

print("\n=== (d) partitioned Chebyshev correction, independent implementation ===")
qs_all = [3, 5, 7, 11, 13, 17]
# cumulative counts of primes > q in residue a mod q, indexed by x
cum = {}
for q in qs_all:
    arr = np.zeros((q, N + 1), dtype=np.int32)
    for a in range(1, q):
        m = isp.copy(); m[:q + 1] = False
        m &= (np.arange(N + 1) % q == a)
        arr[a] = np.cumsum(m)
    cum[q] = arr

def factor(n_arr, qlist, bug):
    F = np.ones(len(n_arr))
    h = n_arr // 2
    for q in qlist:
        cL = cum[q][:, h].astype(float); cT = cum[q][:, n_arr].astype(float); cU = cT - cL
        TL = cL.sum(0) - (1 if bug else 0); TU = cU.sum(0)
        fL = cL / TL; fU = cU / TU
        P = np.zeros(len(n_arr))
        for a in range(1, q):
            b = (n_arr - a) % q
            ok = b != 0
            P += np.where(ok, fL[a] * fU[b, np.arange(len(n_arr))], 0)
        nsol = np.where(n_arr % q == 0, q - 1, q - 2)
        F *= P / (nsol / (q - 1) ** 2)
    return F

base = y37
vb = np.var(base / base.mean())
print(f"baseline (S35 conv) var(y/mean) = {vb:.8f}  CoV {np.sqrt(vb)*100:.4f}%  [S35 claimed 0.00125912, 3.5484%]")
subsets = [qs_all[:k] for k in range(1, 7)]
for bug in (True, False):
    print(f"-- denominator {'total_L - 1 (S35 bug)' if bug else 'correct sum(counts_L) (S36 fix)'}")
    for qsub in subsets:
        C = factor(ev, qsub, bug); y = base / C; v = np.var(y / y.mean())
        print(f"   q<= {qsub[-1]:2d}: var {v:.8f}  red {100*(vb-v)/vb:8.4f}%  CoV {np.sqrt(v)*100:.4f}%")
# same with accurate I baseline (robustness)
vb2 = np.var(ya / ya.mean())
print(f"-- robustness: accurate-I baseline var {vb2:.8f}, fixed denominator")
for qsub in subsets:
    C = factor(ev, qsub, False); y = ya / C; v = np.var(y / y.mean())
    print(f"   q<= {qsub[-1]:2d}: var {v:.8f}  red {100*(vb2-v)/vb2:8.4f}%")
# how big is the bug factor's n-trend
Cb = factor(ev, qs_all, True) / factor(ev, qs_all, False)
print(f"bug factor prod_q TL/(TL-1) over q<=17: n=1000 -> {Cb[0]:.5f}, n=50000 -> {Cb[-1]:.5f}; its CoV {cov(Cb)*100:.4f}% (compare baseline CoV)")
