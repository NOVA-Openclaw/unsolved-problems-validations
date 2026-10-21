"""S55 item 3: independent D^2 for the S54 C2b Steane case. S54 modules imported ONLY to rebuild the identical psi0 and G
(rng stream replicated as in s54_c2.py mode b); D^2 is then computed by my own real least squares (no HalfCosets/lu_tan)."""
import sys, json, itertools, numpy as np
sys.path.insert(0, '..')
import s50_choi_nonlocal_magic as m, s51_identity as S51, s52_coset as C, s53_halfcoset as H
codes = S51.get_codes(np.random.default_rng(5151)); rng = np.random.default_rng(5454)
cases = [("513", [0, 1]), ("422", [0, 1]), ("rnd61", [0, 1, 2]), ("713", [3, 4, 5])]
res = {}
def herm_basis(d):
    B = []
    for i in range(d):
        for j in range(i, d):
            if i == j: E = np.zeros((d, d), complex); E[i, i] = 1; B.append(E)
            else:
                E = np.zeros((d, d), complex); E[i, j] = E[j, i] = 1 / np.sqrt(2); B.append(E)
                F = np.zeros((d, d), complex); F[i, j] = -1j / np.sqrt(2); F[j, i] = 1j / np.sqrt(2); B.append(F)
    return B
for code, Ap in cases:
    n, k, V = codes[code]; N = n + k; R = list(range(k)); A = [k + q for q in Ap]; B = [q for q in range(N) if q not in R + A]
    psi0 = m.choi(V, k); st = C.Stab(psi0, N); hc = H.HalfCosets(st, [R, A, B])
    for q1, q2 in itertools.product(Ap, [q - k for q in B]):
        G, g = H.gen_G_multi(n, k, [q1, q2], rng); D = hc.D2(G)
        if D > 1e-3: break
    order = R + A + B; dims = (2 ** len(R), 2 ** len(A), 2 ** len(B))
    Pm = np.transpose(np.eye(2 ** N).reshape([2] * N + [2 ** N]), order + [N]).reshape(2 ** N, 2 ** N)  # permutation matrix
    p0 = Pm @ psi0; Gp = Pm @ G @ Pm.T
    Q = np.eye(2 ** N) - np.outer(p0, p0.conj()); cols = []
    T = p0.reshape(dims)
    for ax, d in enumerate(dims):
        for h in herm_basis(d):
            cols.append((Q @ np.moveaxis(np.tensordot(h, T, axes=([1], [ax])), 0, ax).reshape(-1)))
    Am = np.array(cols).T; b = -(Q @ Gp @ p0)
    Ar = np.vstack([Am.real, Am.imag]); br = np.concatenate([b.real, b.imag]); x, *_ = np.linalg.lstsq(Ar, br, rcond=None)
    D2own = float(np.linalg.norm(Ar @ x - br) ** 2)
    res[code] = dict(pair=[q1, q2], D2_halfcoset=float(D), D2_own=D2own, coef_own=4 * D2own / np.log(2), coef_s54=4 * float(D) / np.log(2), absdiff=abs(D2own - D))
    print(code, res[code], flush=True)
s = json.load(open('../s54_c2b713.json'))[0]; th = np.array([r['th'] for r in s['rows']]); r = np.array([r['r_global'] for r in s['rows']])
ri = np.array([x['r_ident'] for x in s['rows']]); e = r - 1
fit = np.polyfit(th, r, 2)   # r = c2 th^2 + c1 th + c0 through 3 points (exact)
res['steane_fit'] = dict(r_minus_1=e.tolist(), halving_ratios=(e[1:] / e[:-1]).tolist(), quad_fit_c0_c1_c2=fit[::-1].tolist(),
                         lin_extrap_from_last_two=float(2 * r[2] - r[1]), max_abs_global_minus_ident=float(np.max(np.abs(r - ri))))
print(res['steane_fit']); json.dump(res, open('s55_steane.json', 'w'), indent=1)
