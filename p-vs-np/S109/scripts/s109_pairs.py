"""S109 part A: exact min-lam0 on all 49 member pairs with the S95 (S85 get_Hpp_M) witnesses,
using the independent s109_lib instrument. Per pair: exact primal attainment (assembled mu passes exact
Lemma-1 on the TENSOR kernel) + exact dual certificate => exact optimum.  Plus controls."""
import sys, json
from fractions import Fraction as F
sys.path.insert(0, 'pyc_restore')
import numpy as np
import s83_witness_norm as W
import s85_lambda_boxes as L85
import s109_lib as S

import os
out = open("s109_pairs_output.txt" if __name__ == "__main__" else os.devnull, "w")
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n'); out.flush()

MEM = []
for name, n, Sup in W.MEMBERS:
    g = S.g_from_support(n, Sup)
    A, M = L85.get_Hpp_M(n, np.array(g, dtype=float))
    A = [S.rat(x, 1000) for x in A]; M = [S.rat(x, 1000) for x in M]
    B = [m - a for m, a in zip(M, A)]
    ok_h = S.h_check_exact(n, g, A, B)
    negok = all(M[v] >= 0 for v in range(1 << n) if g[v] == -1)
    zstar = (1 << n) - 1
    P(f'witness {name}: exact H={ok_h}  M>=0 on Neg={negok}  A(z*)={A[zstar]}  sum(A)={sum(A)}  A(0)={A[0]}  M(0)={M[0]}')
    assert ok_h and negok
    MEM.append((name, n, g, A, M))


def exact_min_lam0(n1, g1, A1, n2, g2, M2):
    Lp = S.build_lp(n1, g1, A1, n2, g2, M2)
    col = Lp['li'][0]
    res = S.solve(Lp, col)
    if res.status == 2:
        return dict(status='INFEASIBLE')
    if res.status != 0:
        raise RuntimeError(f'LP status {res.status}: {res.message}')
    # exact primal
    x = [S.rat(v) for v in res.x]
    pok = S.exact_primal_check(Lp, x)
    mu_ok = None
    if pok:
        mu = S.assemble_mu(Lp, n1, A1, n2, M2, x)
        mu_ok, bad = S.lemma1_exact(n1 + n2, S.tensor(n1, g1, n2, g2), mu)
    # exact dual
    y = [S.rat(v) for v in res.eqlin.marginals]
    w = [S.rat(v) for v in res.ineqlin.marginals]
    bnd = S.exact_dual_bound(Lp, col, y, w)
    return dict(status='OPT', float=res.fun, primal_val=x[col] if pok else None, primal_exact=pok,
                mu_lemma1_exact=mu_ok, dual_bound=bnd,
                exact_opt=(pok and bnd is not None and bnd == x[col]))


def main():
    # ---- controls ----
    P('\n== CONTROLS ==')
    # Positive control A: the NOT1 Lemma-1 certificate is (0,1) by hand; instrument must accept it and reject (0,-1).
    g_not1 = [1, -1]
    P('  POS-CONTROL NOT1 (0,1):', S.lemma1_exact(1, g_not1, [F(0), F(1)])[0], ' (expected True)')
    P('  NEG-CONTROL NOT1 (0,-1):', S.lemma1_exact(1, g_not1, [F(0), F(-1)])[0], ' (expected False)')
    # Negative control B: H_A-only g1 x member must be INFEASIBLE (S84 6/6 on H_A-only x member).
    import common as C
    for Sup in [(3, 13, 14), (7, 11, 12), (7, 10, 13)]:
        gA = S.g_from_support(4, Sup)
        okA, A_A, _ = C.condition_H(4, np.array(gA, dtype=float), A_only=True, return_witness=True)
        A_A = [S.rat(x, 1000) for x in A_A]
        P(f'  H_A-only {Sup}: exact H_A witness={S.ha_check_exact(4, gA, A_A)}')
        for name, n, g, A, M in MEM[:3]:
            r = exact_min_lam0(4, gA, A_A, n, g, M)
            P(f'  NEG-CONTROL HA{Sup} x {name}: {r["status"]}  (expected INFEASIBLE)')

    # ---- all 49 ----
    P('\n== 49 PAIRS (S95 witnesses) ==')
    rows = []
    for (n1a, n1, g1, A1, M1) in MEM:
        for (n2a, n2, g2, A2, M2) in MEM:
            r = exact_min_lam0(n1, g1, A1, n2, g2, M2)
            rows.append(dict(g1=n1a, g2=n2a, **{k: (str(v) if isinstance(v, F) else v) for k, v in r.items()}))
            P(f'  {n1a:9s} x {n2a:9s}: {r["status"]} lam0*={r.get("primal_val")} dual={r.get("dual_bound")} '
              f'primal_exact={r.get("primal_exact")} mu_Lemma1={r.get("mu_lemma1_exact")} EXACT_OPT={r.get("exact_opt")}')
    json.dump(rows, open('s109_pairs_results.json', 'w'), indent=1)
    ne = sum(1 for r in rows if r.get('exact_opt'))
    P(f'\nexact-certified optima: {ne}/49')
    vals = {}
    for r in rows:
        vals.setdefault(r['g1'], set()).add(r.get('primal_val'))
    for k, v in vals.items():
        P(f'  g1={k}: distinct lam0* over g2 = {sorted(v)}')


if __name__ == '__main__':
    main()
