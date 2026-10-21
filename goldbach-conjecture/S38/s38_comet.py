#!/usr/bin/env python3
"""S38 VALIDATE: independent reproduction of the S37 Goldbach-comet statistics.

Written without reusing the S37 code. r(n) is computed for every even n at once
by an FFT autocorrelation of the prime indicator.
Conventions:
  r_ord(n)   = #{(p,q) ordered : p+q=n}          (p=q counted once)
  r_un(n)    = #{p<=q : p+q=n}                     (p=q counted once)
  S(n)       = 2*C2*prod_{p|n,p>2} (p-1)/(p-2)
  G_simple   = S(n) * n / log^2 n
  I_full(n)  = int_2^{n-2} dt / (log t log(n-t))   (accurate quadrature)
  I_half(n)  = int_2^{n/2} ...                     (accurate)
  I_s37(n)   = S37's 500-point left Riemann sum over [2, n/2] (reproduced to check the quadrature error)
"""
import numpy as np, sys
from scipy.integrate import quad

C2 = 0.66016181584686957

def sieve(N):
    s = np.ones(N + 1, dtype=bool); s[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if s[i]: s[i*i::i] = False
    return s

def r_counts(N):
    isp = sieve(N).astype(np.float64)
    L = 1 << int(np.ceil(np.log2(2 * N + 2)))
    f = np.fft.rfft(isp, L)
    r_ord = np.rint(np.fft.irfft(f * f, L)[:N + 1]).astype(np.int64)
    sq = np.zeros(N + 1, dtype=np.int64)
    ps = np.nonzero(isp)[0]
    ps2 = 2 * ps[2 * ps <= N]; sq[ps2] = 1          # p=q cases
    r_un = (r_ord + sq) // 2
    return isp.astype(bool), r_ord, r_un

def sing(N, isp):
    S = np.full(N + 1, 2 * C2)
    for p in np.nonzero(isp)[0]:
        if p == 2: continue
        S[p::p] *= (p - 1) / (p - 2)
    return S

def I_quad(n, hi):
    f = lambda t: 1.0 / (np.log(t) * np.log(n - t))
    return quad(f, 2, hi, limit=200)[0]

def I_s37(n):
    ts = np.linspace(2, n / 2, 500); dt = ts[1] - ts[0]
    return np.sum(1.0 / (np.log(ts) * np.log(n - ts))) * dt

def stats(y):
    m = y.mean(); v = y.var(); sd = y.std()
    return m, v, sd, sd / m, np.var(y / m)

def window(a, b, r_ord, r_un, S, tag, do_s37=True, out=print):
    ev = np.arange(a, b + 1, 2)
    Ih = np.array([I_quad(n, n / 2) for n in ev])
    If = 2 * Ih  # symmetric integrand: I_full = 2*I_half up to the n-2 endpoint (negligible)
    Gs = S[ev] * ev / np.log(ev) ** 2
    rows = {
        'r_ord / (S*I_full)': r_ord[ev] / (S[ev] * If),
        'r_un  / (S*I_half)': r_un[ev] / (S[ev] * Ih),
        'r_ord / G_simple   ': r_ord[ev] / Gs,
        'r_un  / G_simple   ': r_un[ev] / Gs,
    }
    if do_s37:
        I37 = np.array([I_s37(n) for n in ev])
        rows['r_un  / (S*I_s37) ['+'S37 exact convention]'] = r_un[ev] / (S[ev] * I37)
    out(f"\n=== {tag}: evens in [{a},{b}], N={len(ev)} ===")
    out(f"{'convention':45s} {'mean':>11s} {'rawvar':>11s} {'sd':>10s} {'CoV%':>8s} {'var(y/mean)':>12s}")
    res = {}
    for k, y in rows.items():
        m, v, sd, cv, nv = stats(y)
        res[k] = (m, v, sd, cv, nv)
        out(f"{k:45s} {m:11.8f} {v:11.8f} {sd:10.8f} {cv*100:8.4f} {nv:12.8f}")
    return ev, rows, res

def main():
    N = 120002
    isp, r_ord, r_un = r_counts(N)
    # sanity: brute force a few
    for n in (100, 1000, 100000, 120000):
        bf = sum(1 for p in range(2, n // 2 + 1) if isp[p] and isp[n - p])
        assert bf == r_un[n], (n, bf, r_un[n])
    print("sanity r_un brute-force OK at 100,1000,1e5,1.2e5; r_un(100000) =", r_un[100000])
    S = sing(N, isp)

    ev, rows, res = window(100000, 120000, r_ord, r_un, S, "Claim (a) window")

    # Claim (b): mod-6 branching of r/I (no singular series)
    print("\n=== Claim (b): mod 6 branching, y = r/I (no singular series) ===")
    Ih = np.array([I_quad(n, n / 2) for n in ev]); I37 = np.array([I_s37(n) for n in ev])
    for lab, I in (("I_half accurate", Ih), ("I_s37 (500-pt Riemann)", I37)):
        y = r_un[ev] / I
        ms = {}
        for c in (0, 2, 4):
            mk = ev % 6 == c
            ms[c] = y[mk].mean()
            print(f"  [{lab}] n={c} mod 6 (N={mk.sum()}): mean r/I = {ms[c]:.6f}, mean S = {S[ev][mk].mean():.6f}, "
                  f"mean S excl p=3 factor = {(S[ev][mk] / np.where(ev[mk]%3==0,2.0,1.0)).mean():.6f}")
        ratio = ms[0] / ((ms[2] + ms[4]) / 2)
        print(f"  [{lab}] band ratio mean0 / mean(mean2,mean4) = {ratio:.6f}")
        # decomposition: ratio = 2 * (E[S'|0]/E[S'|2,4]) * (E[rho|0]/E[rho|2,4]) roughly
    Sp = S[ev] / np.where(ev % 3 == 0, 2.0, 1.0)
    m0 = ev % 6 == 0; m24 = ~m0
    print(f"  S' (singular series without p=3 factor): E[S'|0 mod 6]={Sp[m0].mean():.6f}  E[S'|2,4]={Sp[m24].mean():.6f}  ratio={Sp[m0].mean()/Sp[m24].mean():.6f}")
    rho = r_un[ev] / (S[ev] * Ih)
    print(f"  rho=r/(S I): E[rho|0]={rho[m0].mean():.6f} E[rho|2]={rho[ev%6==2].mean():.6f} E[rho|4]={rho[ev%6==4].mean():.6f}")
    print(f"  => predicted band ratio 2 * S'ratio * rho-ratio = {2*Sp[m0].mean()/Sp[m24].mean()*rho[m0].mean()/rho[m24].mean():.6f}")
    # Null test: how much does the ratio fluctuate over disjoint 20k windows?
    print("  Band ratio across other 20000-wide windows (I accurate, r_un):")
    for a in (20000, 40000, 60000, 80000, 100000):
        e = np.arange(a, a + 20001, 2)
        I = np.array([I_quad(n, n / 2) for n in e]); y = r_un[e] / I
        r0 = y[e % 6 == 0].mean(); r24 = (y[e % 6 == 2].mean() + y[e % 6 == 4].mean()) / 2
        print(f"    [{a},{a+20000}] ratio = {r0/r24:.6f}")

if __name__ == "__main__":
    main()
