#!/usr/bin/env python3
"""S37 VALIDATE — scaling sanity checks for arXiv 2511.09556 (Cheskidov–Dai–Palasek).

This does NOT re-prove the paper. It checks that the *leading-order ansatz* of
Sec. 2.6 / 4.1 is dimensionally consistent with the claimed properties of Thm 1.1:

  v(x,t) ~ sum_k N_k exp(-N_k^2 t) * O(1) profile supported on Omega_k, |Omega_k| <= 2^-k
  N_k = A^(b^k)  (double exponential, eq. 4.1 with d>=3, m*=1)

Checks:
 (1) eq. (2.5) time integral, symbolically.
 (2) Duhamel impulse: a mode at frequency N_k forced by N_{k+1}^2 exp(-2 N_{k+1}^2 s)
     becomes (F/2) exp(-N_k^2 t) for t >> N_{k+1}^-2 — i.e. the injection is effectively
     instantaneous, relative error ~ N_k^2 / N_{k+1}^2. Amplitude recursion is scale-free.
 (3) Type I upper bound sup_t sqrt(t) ||v(t)||_inf < inf, and lower bound at t_k = N_k^-2.
 (4) ||v||_{L^2_t L^inf} diverges (~1/2 per scale) — required by Thm 2.1 (else uniqueness).
 (5) Orlicz-weakened LPS (1.4) with weight 1/(1+(loglog N)^c): converges iff c > 1.
 (6) L^2_t L^p converges for p < inf via |Omega_k|^(2/p) = 2^(-2k/p)   (eq. 1.6).
 (7) Energy at t = N_k^-2 ~ N_k^2 2^-k -> inf  (Thm 2.4 / Remark 1.4 necessity).
Uses the model ||v(t)||_inf ~ sum_k N_k e^{-N_k^2 t} (ignores O(1) profile constants).
Everything in log-space / mpmath to avoid overflow.
"""
import math
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
print("=" * 70)
print("(1) eq. (2.5): I(j,j') = int_0^inf N N' exp(-(N^2+N'^2) s) ds")
N, Np, s, t = sp.symbols("N Np s t", positive=True)
I = sp.integrate(N * Np * sp.exp(-(N**2 + Np**2) * s), (s, 0, sp.oo))
print("   closed form:", sp.simplify(I))
print("   j=j' :", sp.simplify(I.subs(Np, N)), "  (paper: ~1)")
print("   N' << N limit, leading term:", sp.series(I.subs(Np, N * sp.Symbol('r', positive=True)),
      sp.Symbol('r', positive=True), 0, 2).removeO(), " = N'/N  (paper eq 2.5 writes N_{j,k}^-1 N_{j',k} for j>j' -> same thing)")

print("=" * 70)
print("(2) Duhamel impulse on a single Fourier mode")
Nk, Nk1, F = sp.symbols("N_k N_k1 F", positive=True)
vhat = sp.integrate(sp.exp(-Nk**2 * (t - s)) * F * Nk1**2 * sp.exp(-2 * Nk1**2 * s), (s, 0, t))
vhat = sp.simplify(vhat)
print("   vhat(t) =", vhat)
target = F / 2 * sp.exp(-Nk**2 * t)
for (nk, nk1) in [(4, 16), (16, 256), (256, 65536)]:
    tt = mp.mpf(10) / nk1**2  # t = 10 N_{k+1}^-2 (well after the injection window)
    tt2 = mp.mpf(1) / nk**2   # t = N_k^-2 (natural time of shell k)
    for lab, T in [("t=10/N_{k+1}^2", tt), ("t=1/N_k^2", tt2)]:
        val = mp.mpf(F.subs(F, 1)) * nk1**2 * (mp.e**(-nk**2 * T) - mp.e**(-2 * nk1**2 * T)) / (2 * nk1**2 - nk**2)
        tgt = mp.e**(-nk**2 * T) / 2
        print(f"   N_k={nk:>6}, N_k+1={nk1:>6}, {lab:>15}: rel.err = {mp.nstr(abs(val/tgt-1), 4)}"
              f"   (N_k^2/(2N_k+1^2) = {mp.nstr(mp.mpf(nk)**2/(2*mp.mpf(nk1)**2),4)})")
print("   => output amplitude at shell k = (1/2) * [O(1) low-freq part of a_{k+1}^2], no N-dependence:")
print("      the amplitude recursion a_{k+1}^2 -> a_k is scale-invariant exactly at Type I scaling.")

print("=" * 70)
A, b, K = 2, 2, 7   # N_k = 2^(2^k): 2,4,16,256,65536,2^32,2^64,...
Ns = [mp.mpf(A) ** (b ** k) for k in range(1, K + 1)]
print(f"(3)-(7) model with N_k = {A}^({b}^k), k=1..{K}:", [mp.nstr(x, 3) for x in Ns])

def vinf(T):
    return mp.fsum(n * mp.e ** (-n * n * T) for n in Ns)

# (3) sup sqrt(t)||v||  over a log grid spanning all scales
lo, hi = -2 * mp.log(Ns[-1]) - 5, 2
grid = [mp.e ** (lo + (hi - lo) * i / 4000) for i in range(4001)]
vals = [mp.sqrt(T) * vinf(T) for T in grid]
print(f"(3) sup_t sqrt(t)||v(t)||_inf = {mp.nstr(max(vals), 6)}  (single-mode max = (2e)^-1/2 = {mp.nstr(1/mp.sqrt(2*mp.e),6)})")
print("    lower bound at t_k = N_k^-2 : sqrt(t_k)||v(t_k)|| =",
      [mp.nstr(mp.sqrt(1 / n**2) * vinf(1 / n**2), 4) for n in Ns], " (>= e^-1 = 0.3679)")

# (4) int_0^1 ||v||^2 dt per scale — diagonal terms: int N^2 e^{-2N^2 t} = 1/2 (1-e^{-2N^2})
diag = [mp.mpf(1) / 2 * (1 - mp.e ** (-2 * n * n)) for n in Ns]
cross = mp.fsum(2 * Ns[i] * Ns[j] / (Ns[i] ** 2 + Ns[j] ** 2) for i in range(K) for j in range(i + 1, K))
print(f"(4) int ||v||_inf^2 dt: diagonal per scale = {[mp.nstr(x,4) for x in diag]}; cross terms total = {mp.nstr(cross,4)}")
print("    partial sums grow linearly in K  => v not in L^2_t L^inf_x (log-divergent at borderline)  ✔ consistent with Thm 2.1")

# (5) Orlicz weight — contribution of scale k ≈ (1/2)/(1+(loglog N_k)^c); loglog N_k = k log b + loglog A
def orlicz_partial(c, Kmax):
    return sum(0.5 / (1 + (k * math.log(b) + math.log(math.log(A))) ** c) if (k*math.log(b)+math.log(math.log(A)))>0
               else 0.5 for k in range(1, Kmax + 1))
for c in (0.5, 1.0, 1.5, 2.0):
    print(f"(5) c={c}: partial sums K=1e2,1e4,1e6 ->",
          [round(orlicz_partial(c, Km), 4) for Km in (100, 10_000, 1_000_000)])
print("    => (1.4) holds only for c > 1 with double-exponential N_k (paper says 'for some c>0'; any c>1 works).")

# (6) L^2_t L^p : scale k contributes ||v_k||_p^2 * (1/(2N_k^2)) with ||v_k||_p ~ N_k 2^{-k/p}
for p in (2, 4, 10, 100):
    ks = range(1, 60)
    tot = sum(0.5 * 2 ** (-2 * k / p) for k in ks)
    print(f"(6) p={p:>3}: sum_k (1/2) 2^(-2k/p) (k<60) = {tot:.4f}  (limit {0.5*2**(-2/p)/(1-2**(-2/p)):.4f}; finite for every p<inf)")

# (7) energy at t_k
print("(7) log10 energy at t_k=N_k^-2 ~ log10(N_k^2 2^-k e^-2):",
      [mp.nstr(mp.log10(n**2 * mp.mpf(2) ** (-(k + 1)) * mp.e ** -2), 4) for k, n in enumerate(Ns)])
print("    -> diverges: energy blows up as t->T*+, so the branch is NOT Leray–Hopf (as the paper states).")
