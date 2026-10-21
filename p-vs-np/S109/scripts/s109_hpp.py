"""S109 part C: is the corrector-LP feasibility governed by H++ of the g1 witness?
H++ (S84/S86): M >= 0 on Neg, M <= 0 on Pos\\{0}, M(0) <= 2.  Sample random vertices of the H++-restricted
witness polytope for g1 and of the normalized-but-NOT-H++ complement; exact min lam0 vs g2 = H1 and g2 = H5b."""
import sys
sys.path.insert(0, 'pyc_restore')
import numpy as np
import s109_lib as S
from s109_pairs import exact_min_lam0, MEM
out = open('s109_hpp_output.txt', 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n'); out.flush()
rng = np.random.default_rng(1090)

def hpp_rows(n, g):
    N = 1 << n; rows = []
    for v in range(1, N):
        if g[v] == 1:
            r = np.zeros(2 * N); r[v] = 1; r[N + v] = 1; rows.append((r, 0.0))
    r = np.zeros(2 * N); r[0] = 1; r[N] = 1; rows.append((r, 2.0))
    return rows

def is_hpp(n, g, M):
    N = 1 << n
    return all(M[v] >= 0 for v in range(N) if g[v] == -1) and all(M[v] <= 0 for v in range(1, N) if g[v] == 1) and M[0] <= 2

g2s = [MEM[0], MEM[3]]
for name, n, g, A, M in MEM:
    N = 1 << n; z = N - 1
    stats = {}
    for tag, extra in (('H++', hpp_rows(n, g)), ('norm', [])):
        for _ in range(10):
            r = S.h_lp(n, g, rng.standard_normal(2 * N), extra_ub=extra)
            if r.status != 0: raise RuntimeError(r.message)
            Aw = [S.rat(x, 1000) for x in r.x[:N]]; Bw = [S.rat(x, 1000) for x in r.x[N:]]
            Mw = [a + b for a, b in zip(Aw, Bw)]
            if not S.h_check_exact(n, g, Aw, Bw): stats.setdefault((tag, 'WNE'), 0); continue
            hp = is_hpp(n, g, Mw)
            for g2 in g2s:
                res = exact_min_lam0(n, g, Aw, g2[1], g2[2], g2[4])
                key = (tag, 'wit_is_H++' if hp else 'wit_not_H++', g2[0], str(res.get('primal_val')), f'A(z*)={Aw[z]}')
                stats[key] = stats.get(key, 0) + 1
    P(f'{name}:')
    for k in sorted(stats, key=str): P('   ', k, stats[k])
