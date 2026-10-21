"""Fast LU minimization of pure-state SRE M2 over U_R (x) U_A (x) U_B via Riemannian
gradient ascent on S4 = sum_P |<P>|^4 (M2 = -log2(S4/N)). Analytic gradient."""
import numpy as np
from scipy.linalg import expm
import s50_choi_nonlocal_magic as m

def S4_and_grad(psi):
    N = psi.size; n = int(np.log2(N)); idx = np.arange(N); H = m.hadamard(n)
    X = idx[:, None] ^ idx[None, :]                     # X[x,b] = b^x
    F = np.conj(psi[X]) * psi[None, :]
    E = F @ H                                           # E[x,z]
    a2 = np.abs(E) ** 2
    S4 = np.sum(a2 ** 2)
    A = (2 * a2 * np.conj(E)) @ H                       # A[x,c'] = sum_z 2|E|^2 E* (-1)^{z.c'}
    B = (2 * a2 * E) @ H
    # g[c] = sum_x psi[c^x] (A[x, c^x] + B[x, c])
    cx = X.T                                            # cx[c,x] = c^x
    xs = idx[None, :]
    g = np.sum(psi[cx] * (A[xs, cx] + B[xs, idx[:, None]]), axis=1)
    return S4, g                                        # g = dS4/dpsi*

def lu_min(psi, dims, iters=3000, restarts=3, rng=None, init_scale=0.8, tol=1e-12):
    rng = rng or np.random.default_rng(0)
    N = psi.size; best = m.M2_pure(psi); T0 = psi.reshape(dims)
    for r in range(restarts):
        Us = [np.eye(d, dtype=complex) if r == 0 else
              expm(1j * m.herm_from(rng.normal(scale=init_scale, size=d * d), d)) for d in dims]
        def state(Us):
            return np.einsum('ai,bj,ck,ijk->abc', Us[0], Us[1], Us[2], T0).reshape(-1)
        p = state(Us); S, g = S4_and_grad(p); eta = 0.5
        for it in range(iters):
            P = p.reshape(dims); G = g.reshape(dims); Ds = []
            for ax, d in enumerate(dims):
                Pm = np.moveaxis(P, ax, 0).reshape(d, -1); Gm = np.moveaxis(G, ax, 0).reshape(d, -1)
                C = Pm @ Gm.conj().T
                Ds.append(1j * (C - C.conj().T))       # dS4 = Tr(H D) for psi -> (1+iH)psi
            gn = sum(np.real(np.trace(D @ D)) for D in Ds)
            if gn < tol: break
            while True:                                 # ascent with backtracking
                Un = [expm(1j * eta * D) @ U for D, U in zip(Ds, Us)]
                pn = state(Un); Sn, gnw = S4_and_grad(pn)
                if Sn >= S + 1e-4 * eta * gn or eta < 1e-10:
                    break
                eta *= 0.5
            if Sn < S: break
            Us, p, S, g = Un, pn, Sn, gnw; eta = min(eta * 1.5, 5.0)
        best = min(best, float(-np.log2(S / N)))
    return best

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    psi = rng.normal(size=16) + 1j * rng.normal(size=16); psi /= np.linalg.norm(psi)
    S, g = S4_and_grad(psi)
    d = rng.normal(size=16) + 1j * rng.normal(size=16); e = 1e-6
    num = (S4_and_grad(psi + e * d)[0] - S4_and_grad(psi - e * d)[0]) / (2 * e)
    print("grad check", num, 2 * np.real(np.vdot(g, d)))
