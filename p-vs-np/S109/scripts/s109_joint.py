"""S109 part E: GLOBAL min lam0 over all normalized g1-witnesses (joint LP, exact primal+dual), per pair with
the S95 g2 witnesses. Also max lam0 over H++ witnesses isn't needed. Also exact recheck of the H5d -1/2 outlier."""
import sys, json
from fractions import Fraction as F
sys.path.insert(0, 'pyc_restore')
import numpy as np
import s109_lib as S
from s109_pairs import MEM
out = open('s109_joint_output.txt', 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n'); out.flush()

def joint(n1, g1, n2, g2, M2, hpp=False, sense=1):
    L = S.build_joint_lp(n1, g1, n2, g2, M2, hpp=hpp)
    col = L['li'][0]
    res = S.solve(L, col, sense)
    if res.status == 2: return 'INFEASIBLE', None, None
    if res.status != 0: raise RuntimeError(res.message)
    x = [S.rat(v) for v in res.x]
    pok = S.exact_primal_check(L, x)
    if pok:
        N1 = 1 << n1; A1 = x[L['off']:L['off'] + N1]; B1 = x[L['off'] + N1:L['off'] + 2 * N1]
        wok = S.h_check_exact(n1, g1, A1, B1)
        mu = S.assemble_mu(L, n1, A1, n2, M2, x)
        mok = S.lemma1_exact(n1 + n2, S.tensor(n1, g1, n2, g2), mu)[0]
        pok = pok and wok and mok
    y = [S.rat(v) for v in res.eqlin.marginals]; w = [S.rat(v) for v in res.ineqlin.marginals]
    if sense == 1:
        bnd = S.exact_dual_bound(L, col, y, w)
    else:
        bnd = None
    return ('OPT', x[col], (pok, bnd, pok and bnd == x[col]))

# positive control: joint LP min must be <= the fixed-witness min (S95 witness is one feasible A1)
P('== joint min lam0 over ALL normalized g1-witnesses (g2 = S95 witness) ==')
rows = []
for (a, n1, g1, A1, M1) in MEM:
    for (b, n2, g2, A2, M2) in MEM:
        st, val, cert = joint(n1, g1, n2, g2, M2)
        rows.append((a, b, st, str(val), cert))
        P(f'  {a:9s} x {b:9s}: {st} global_min_lam0={val} (primal+witness+Lemma1 exact, dual bound, EXACT) = {cert}')
json.dump(rows, open('s109_joint_results.json', 'w'), indent=1, default=str)
