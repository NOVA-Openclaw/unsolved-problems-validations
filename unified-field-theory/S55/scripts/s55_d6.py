"""S55 N0 (lib cross-check) + N1 + N2 (prereg s55_prereg.md)."""
import numpy as np, json, itertools, functools
import s55_lib as L
rng = np.random.default_rng(55055); out = {}
# N0: brute-force M2 with explicit Pauli matrices vs FWHT
P1 = [np.eye(2), np.array([[0,1],[1,0]]), np.array([[0,-1j],[1j,0]]), np.diag([1,-1])]
def M2_brute(psi):
    N = int(np.log2(psi.size)); s = 0
    for t in itertools.product(range(4), repeat=N):
        P = functools.reduce(np.kron, [P1[i] for i in t]); s += np.real(np.vdot(psi, P @ psi)) ** 4
    return -np.log2(s / psi.size)
e = 0
for N in (2, 3):
    for _ in range(3):
        v = rng.normal(size=2**N) + 1j*rng.normal(size=2**N); v /= np.linalg.norm(v); e = max(e, abs(M2_brute(v) - L.M2(v)))
out['N0_maxerr_fwht_vs_brute'] = e; print('N0', e, flush=True)
c0 = 4 / L.LN2
def horiz(phi, D):
    w = rng.normal(size=D) + 1j * rng.normal(size=D); w -= np.vdot(phi, w) * phi; return w / np.linalg.norm(w)
# N1
n1 = []
for N in (2, 3, 4, 5):
    D = 2 ** N
    for s in range(6):
        phi = L.rand_clifford_state(N, rng); assert L.M2(phi) < 1e-10
        for d in range(8):
            w = horiz(phi, D)
            f = lambda t: L.M2(np.cos(t) * phi + np.sin(t) * w)
            sd = lambda h: (f(h) + f(-h) - 2 * f(0)) / h**2  # = 2a + O(h^2)
            a1, a2, a3 = sd(2e-3) / 2, sd(1e-3) / 2, sd(1e-2) / 2
            aR = (4 * a2 - a1) / 3
            n1.append(dict(N=N, s=s, d=d, a_rich=aR, a_h1e2=a3, rel=abs(aR - c0) / c0, rel_h1e2=abs(a3 - c0) / c0))
    mx = max(r['rel'] for r in n1 if r['N'] == N); print('N1 N=%d max rel %.3e' % (N, mx), flush=True)
out['N1_max_rel'] = max(r['rel'] for r in n1); out['N1_max_rel_h1e-2'] = max(r['rel_h1e2'] for r in n1)
out['N1_count'] = len(n1); out['N1_PASS'] = out['N1_max_rel'] < 1e-4
# N2 full Hessian
n2 = []
for N in (2, 3):
    D = 2 ** N
    for s in range(2):
        phi = L.rand_clifford_state(N, rng)
        # real orthonormal basis of horizontal space: complex ONB of phi-perp, times {1, i}
        Q, _ = np.linalg.qr(np.column_stack([phi] + [rng.normal(size=D) + 1j*rng.normal(size=D) for _ in range(D - 1)]))
        B = [Q[:, k] for k in range(1, D)]; B = B + [1j * b for b in B]; m = len(B)
        f = lambda v: L.M2(phi + sum(vk * bk for vk, bk in zip(v, B)))
        h = 1e-3; Hm = np.zeros((m, m)); f0 = f(np.zeros(m))
        for i in range(m):
            for j in range(i, m):
                ei = np.zeros(m); ej = np.zeros(m); ei[i] = h; ej[j] = h
                Hm[i, j] = Hm[j, i] = (f(ei + ej) - f(ei - ej) - f(-ei + ej) + f(-ei - ej)) / (4 * h * h)
        ev = np.linalg.eigvalsh(Hm); off = np.max(np.abs(Hm - np.diag(np.diag(Hm))))
        n2.append(dict(N=N, s=s, dim=m, eig_min=ev.min(), eig_max=ev.max(), eig_relmax=float(np.max(np.abs(ev - 2 * c0)) / (2 * c0)), offdiag=off))
        print('N2', n2[-1], flush=True)
out['N2'] = n2; out['N2_PASS'] = all(r['eig_relmax'] < 1e-3 and r['offdiag'] < 1e-3 * 2 * c0 for r in n2)
out['target_quadform'] = c0; out['target_hessian'] = 2 * c0
json.dump(dict(out, N1=n1), open('s55_d6.json', 'w'), indent=1, default=float)
print('SUMMARY', {k: v for k, v in out.items() if k != 'N2'}, flush=True)
