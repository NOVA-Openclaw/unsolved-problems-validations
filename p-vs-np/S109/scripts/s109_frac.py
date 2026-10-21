"""S109 part D: fractional A(z*). For the members where A(z*) ranges over [0,1] (H5a,H5d,H5e), pin A(z*)=t,
sample normalized witnesses (random objectives) and compute exact min lam0 vs g2=H1. Does lam0 interpolate?"""
import sys
from fractions import Fraction as F
sys.path.insert(0, 'pyc_restore')
import numpy as np
import s109_lib as S
from s109_pairs import exact_min_lam0, MEM
out = open('s109_frac_output.txt', 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n'); out.flush()
rng = np.random.default_rng(7)
H1 = MEM[0]
for name, n, g, A, M in [m for m in MEM if m[0][:3] == 'H5a' or m[0][:3] == 'H5d' or m[0][:3] == 'H5e']:
    N = 1 << n; z = N - 1
    for t in [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]:
        r1 = np.zeros(2 * N); r1[z] = 1
        extra = [(r1, float(t)), (-r1, -float(t))]
        seen = {}
        for _ in range(6):
            r = S.h_lp(n, g, rng.standard_normal(2 * N), extra_ub=extra)
            if r.status != 0: seen['LPFAIL'] = seen.get('LPFAIL', 0) + 1; continue
            Aw = [S.rat(x, 1000) for x in r.x[:N]]; Bw = [S.rat(x, 1000) for x in r.x[N:]]
            if not S.h_check_exact(n, g, Aw, Bw) or Aw[z] != t: seen['WNE'] = seen.get('WNE', 0) + 1; continue
            res = exact_min_lam0(n, g, Aw, H1[1], H1[2], H1[4])
            k = str(res.get('primal_val')) + ('' if res.get('exact_opt') in (True, None) else ' (NOT EXACT)')
            seen[k] = seen.get(k, 0) + 1
        P(f'  {name} A(z*)={t}: {seen}')
