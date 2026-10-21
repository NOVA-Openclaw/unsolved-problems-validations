# POST-HOC N4b (NOT preregistered): identical to s55_d7.py N4 (same rng stream) but rndstab4_1 additionally at theta=0.01,0.005 to test whether its non-monotone |r-1| is a sign crossing of an O(theta) term.
"""S55 N3 (global M2 vs distance to stabilizer set, N=2,3) and N4 (end-to-end LU-min vs own D^2). Prereg s55_prereg.md."""
import numpy as np, json, sys, itertools, functools
from scipy.linalg import expm
from scipy.optimize import minimize
import s55_lib as L
part = sys.argv[1]; rng = np.random.default_rng(55707 if part == 'N3' else 55708); out = {}
c0 = 4 / L.LN2
if part == 'N3':
    for N in (2, 3):
        D = 2 ** N; st = L.enumerate_stab(N, rng, 60 if N == 2 else 1080); rows = []
        for k in range(20000):
            if k % 2 == 0:
                v = rng.normal(size=D) + 1j * rng.normal(size=D)
            else:
                phi = st[rng.integers(len(st))]; w = rng.normal(size=D) + 1j * rng.normal(size=D); w -= np.vdot(phi, w) * phi; w /= np.linalg.norm(w)
                t = rng.uniform(0, 0.5) * (rng.uniform() ** 2 if k % 4 == 1 else 1); v = np.cos(t) * phi + np.sin(t) * w
            v /= np.linalg.norm(v); d = float(np.arccos(min(1, np.max(np.abs(st.conj() @ v))))); m = L.M2(v); rows.append((d, m))
        a = np.array(rows); d, m = a[:, 0], a[:, 1]; rat = m / (c0 * d ** 2)
        small = d < 0.02; bins = [(0, .01), (.01, .02), (.02, .05), (.05, .1), (.1, .2), (.2, .4), (.4, 2)]
        res = dict(nstab=len(st), n=len(a), mean_ratio_d_lt_0p02=float(rat[small].mean()), n_small=int(small.sum()),
                   min_M2_over_d2=float(np.min(m / d ** 2)), min_ratio=float(rat.min()), argmin_d=float(d[np.argmin(m / d ** 2)]),
                   n_bad=int(np.sum((m < 1e-6) & (d > 0.05))), max_d=float(d.max()),
                   bins={f'{lo}-{hi}': [float(rat[(d >= lo) & (d < hi)].min()) if np.any((d >= lo) & (d < hi)) else None,
                                         float(rat[(d >= lo) & (d < hi)].mean()) if np.any((d >= lo) & (d < hi)) else None] for lo, hi in bins})
        res['PASS'] = abs(res['mean_ratio_d_lt_0p02'] - 1) < 2e-2 and res['min_M2_over_d2'] > 0 and res['n_bad'] == 0
        out[f'N={N}'] = res; print('N3', N, res, flush=True)
else:
    P = [np.eye(2), np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1., -1]).astype(complex)]
    def herm_basis(d):
        B = []
        for i in range(d):
            for j in range(i, d):
                E = np.zeros((d, d), complex)
                if i == j: E[i, i] = 1; B.append(E)
                else:
                    E[i, j] = E[j, i] = 1; B.append(E.copy() / np.sqrt(2)); F = np.zeros((d, d), complex); F[i, j] = -1j; F[j, i] = 1j; B.append(F / np.sqrt(2))
        return B
    def local_ops(dims):
        ops = []
        for ax, d in enumerate(dims):
            for h in herm_basis(d):
                mats = [np.eye(dd) for dd in dims]; mats[ax] = h; ops.append(functools.reduce(np.kron, mats))
        return ops
    def D2_own(psi0, G, dims):
        Pi = np.outer(psi0, psi0.conj()); Q = np.eye(psi0.size) - Pi
        A = np.array([Q @ h @ psi0 for h in local_ops(dims)]).T; b = -(Q @ G @ psi0)
        Ar = np.vstack([A.real, A.imag]); br = np.concatenate([b.real, b.imag]); x, *_ = np.linalg.lstsq(Ar, br, rcond=None)
        return float(np.linalg.norm(Ar @ x - br) ** 2)
    def lu_min(psi, dims, restarts, rng):
        bases = [herm_basis(d) for d in dims]; npar = [len(b) for b in bases]; T = psi.reshape(dims); best = []
        def state(p, U0s):
            Us = []; o = 0
            for b, n, U0 in zip(bases, npar, U0s):
                Us.append(expm(1j * sum(pk * bk for pk, bk in zip(p[o:o + n], b))) @ U0); o += n
            return np.einsum('ai,bj,ck,ijk->abc', *Us, T).reshape(-1)
        for r in range(restarts):
            U0s = [np.eye(d) if r == 0 else np.linalg.qr(rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)))[0] for d in dims]
            val = None
            for rnd in range(4):   # re-centre the chart a few times
                res = minimize(lambda p: L.M2(state(p, U0s)), np.zeros(sum(npar)), method='BFGS', options=dict(gtol=1e-11, maxiter=2000))
                o = 0; newU = []
                for b, n, U0 in zip(bases, npar, U0s):
                    newU.append(expm(1j * sum(pk * bk for pk, bk in zip(res.x[o:o + n], b))) @ U0); o += n
                U0s = newU
                if val is not None and abs(val - res.fun) < 1e-14: val = res.fun; break
                val = res.fun
            best.append(float(val))
        return best
    def ghz():
        v = np.zeros(8, complex); v[0] = v[7] = 1 / np.sqrt(2); return v
    def zbell():
        v = np.zeros(8, complex); v[0] = v[3] = 1 / np.sqrt(2); return v   # |0>_R |Phi+>_AB
    cases = [('GHZ', 3, (2, 2, 2), ghz(), (1, 2)), ('0xBell', 3, (2, 2, 2), zbell(), (1, 2))]
    for i in range(2):
        cases.append((f'rndstab4_{i}', 4, (2, 4, 2), L.rand_clifford_state(4, rng), (rng.integers(1, 3), 3)))
    for name, N, dims, psi0, (qa, qb) in cases:
        assert L.M2(psi0) < 1e-10
        Hm = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)); Hm = (Hm + Hm.conj().T) / 2
        # embed 2-qubit H on qubits qa,qb (qubit order = kron order, R first)
        G = np.zeros((2 ** N, 2 ** N), complex)
        for a, b in itertools.product(range(4), repeat=2):
            c = np.real(np.trace(np.kron(P[a], P[b]).conj().T @ Hm)) / 4
            mats = [P[0]] * N; mats[qa] = P[a]; mats[qb] = P[b]; G += c * functools.reduce(np.kron, mats)
        D2 = D2_own(psi0, G, dims); coef = c0 * D2; rows = []
        for th in ((0.08, 0.04, 0.02, 0.01, 0.005) if name == "rndstab4_1" else (0.08, 0.04, 0.02)):
            psi = expm(-1j * th * G) @ psi0; vals = lu_min(psi, dims, 10, rng)
            rows.append(dict(th=th, r_ident=vals[0] / (coef * th ** 2) if D2 > 1e-6 else vals[0], r_global=min(vals) / (coef * th ** 2) if D2 > 1e-6 else min(vals),
                             r_restarts=[v / (coef * th ** 2) for v in vals] if D2 > 1e-6 else vals, M2_unopt=L.M2(psi)))
            print(name, rows[-1], flush=True)
        e = [abs(r['r_global'] - 1) for r in rows]
        ok = D2 > 1e-6 and e[0] <= 0.1 and e[0] >= e[1] >= e[2] and e[2] <= 0.5 * e[0] and all(r['r_global'] >= r['r_ident'] * (1 - 5 * r['th']) for r in rows)
        out[name] = dict(D2=D2, coef=coef, qa=int(qa), qb=int(qb), rows=rows, PASS=bool(ok)); print('RESULT', name, D2, ok, flush=True)
json.dump(out, open(f's55_d7_{part}b.json', 'w'), indent=1, default=float)
