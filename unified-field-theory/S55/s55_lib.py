"""S55 independent library (no s50-s54 imports)."""
import numpy as np
LN2 = np.log(2)
def fwht(a):
    a = a.copy(); h = 1; n = a.shape[0]
    while h < n:
        a = a.reshape(-1, 2, h, *a.shape[1:]) if False else a
        for i in range(0, n, 2 * h):
            x = a[i:i + h].copy(); y = a[i + h:i + 2 * h].copy(); a[i:i + h] = x + y; a[i + h:i + 2 * h] = x - y
        h *= 2
    return a
def pauli_expect_abs(psi):
    """|<X^x Z^z>| for all x,z (array [x,z]); equals |<P>| for the Hermitian Pauli with that symplectic label."""
    D = psi.size; idx = np.arange(D)
    M = np.array([np.conj(psi) * psi[idx ^ x] for x in range(D)]).T  # rows i, cols x
    return np.abs(fwht(M)).T  # [x,z]
def M2(psi):
    psi = psi / np.linalg.norm(psi); D = psi.size
    return -np.log2(np.sum(pauli_expect_abs(psi) ** 4) / D)
H1 = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2); S1 = np.diag([1, 1j])
def apply1(psi, U, q, N):
    t = psi.reshape([2] * N); t = np.moveaxis(np.tensordot(U, t, axes=([1], [q])), 0, q); return t.reshape(-1)
def cnot(psi, c, t, N):
    T = psi.reshape([2] * N).copy(); sl = [slice(None)] * N; sl[c] = 1; sub = T[tuple(sl)]
    ax = t if t < c else t - 1; T[tuple(sl)] = np.flip(sub, axis=ax); return T.reshape(-1)
def rand_clifford_state(N, rng, ngates=None):
    psi = np.zeros(2 ** N, complex); psi[0] = 1
    for _ in range(ngates or 20 * N + 10):
        r = rng.integers(3)
        if r == 0: psi = apply1(psi, H1, rng.integers(N), N)
        elif r == 1: psi = apply1(psi, S1, rng.integers(N), N)
        elif N > 1:
            c, t = rng.choice(N, 2, replace=False); psi = cnot(psi, c, t, N)
    return psi
def canon(psi):
    k = np.argmax(np.abs(psi) > 1e-9); return psi * np.conj(psi[k]) / abs(psi[k])
def enumerate_stab(N, rng, target):
    seen = {}
    while len(seen) < target:
        p = canon(rand_clifford_state(N, rng, ngates=rng.integers(1, 40 * N)))
        seen.setdefault(tuple(np.round(p, 6)), p)
    return np.array(list(seen.values()))
def fs(a, b): return float(np.arccos(min(1.0, abs(np.vdot(a, b)))))
