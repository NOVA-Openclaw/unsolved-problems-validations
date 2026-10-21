"""S109 part B: witness dependence of min lam0.
(1) range of A(z*) over normalized H-witnesses per member (exact-verified endpoints).
(2) for g1 fixed, sample K vertex witnesses A1 (random objectives over the normalized H-polytope), exact-verify
    each is an H-witness, compute exact min lam0 against g2 = H1 (S95 witness) -> is lam0 a function of g1 alone?
(3) for g1 = H1 fixed, vary M2 over sampled normalized witnesses of g2 -> g2-independence under witness change."""
import sys, json
from fractions import Fraction as F
sys.path.insert(0, 'pyc_restore')
import numpy as np
import s83_witness_norm as W, s85_lambda_boxes as L85
import s109_lib as S
from s109_pairs import exact_min_lam0, MEM   # re-runs part A header (witness checks) only if imported fresh

out = open('s109_witness_output.txt', 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n'); out.flush()

rng = np.random.default_rng(109)
def exact_wit(n, g, res):
    N = 1 << n
    A = [S.rat(x, 1000) for x in res.x[:N]]; B = [S.rat(x, 1000) for x in res.x[N:]]
    M = [a + b for a, b in zip(A, B)]
    ok = S.h_check_exact(n, g, A, B) and all(M[v] >= 0 for v in range(N) if g[v] == -1)
    return ok, A, B, M

P('== (1) A(z*) range over normalized H-witnesses ==')
for name, n, g, A, M in MEM:
    N = 1 << n; z = N - 1
    c = np.zeros(2 * N); c[z] = 1
    lo = S.solve if False else None
    rlo = S.h_lp(n, g, c); rhi = S.h_lp(n, g, -c)
    oklo, Alo, _, _ = exact_wit(n, g, rlo); okhi, Ahi, _, _ = exact_wit(n, g, rhi)
    P(f'  {name}: A(z*) in [{Alo[z]}, {Ahi[z]}]  (endpoint witnesses exact-verified: {oklo}, {okhi})')

K = 12
H1 = MEM[0]
P(f'\n== (2) vary g1 witness (K={K} random-objective vertices + A(z*) extremes), g2 = H1 S95 witness ==')
summary = {}
for name, n, g, A, M in MEM:
    N = 1 << n; z = N - 1
    objs = [np.eye(2 * N)[z], -np.eye(2 * N)[z]] + [rng.standard_normal(2 * N) for _ in range(K)]
    vals = []
    for c in objs:
        r = S.h_lp(n, g, c)
        if r.status != 0: raise RuntimeError(r.message)
        ok, Aw, Bw, Mw = exact_wit(n, g, r)
        if not ok:
            vals.append(('WITNESS_NOT_EXACT', None)); continue
        res = exact_min_lam0(n, g, Aw, H1[1], H1[2], H1[4])
        vals.append((res['status'], res.get('primal_val'), res.get('exact_opt'), Aw[z], sum(Aw)))
    summary[name] = vals
    dist = sorted({str(v[1]) for v in vals})
    P(f'  {name}: distinct lam0* = {dist}')
    for v in vals:
        P(f'      status={v[0]} lam0*={v[1]} exact={v[2] if len(v)>2 else None} A(z*)={v[3] if len(v)>3 else None} sumA={v[4] if len(v)>4 else None}')

P('\n== (3) g1 = H1 (S95 witness) fixed; vary g2 witness M2 (K random vertices) ==')
g1 = MEM[0]
for name, n, g, A, M in MEM:
    N = 1 << n
    vals = set(); infe = 0
    for _ in range(8):
        r = S.h_lp(n, g, rng.standard_normal(2 * N))
        ok, Aw, Bw, Mw = exact_wit(n, g, r)
        if not ok: vals.add('WNE'); continue
        res = exact_min_lam0(g1[1], g1[2], g1[3], n, g, Mw)
        if res['status'] != 'OPT': infe += 1; continue
        vals.add(str(res['primal_val']) + ('' if res['exact_opt'] else '(not exact)'))
    P(f'  H1 x {name}: distinct lam0* over 8 g2-witnesses = {sorted(vals)}  infeasible={infe}')
