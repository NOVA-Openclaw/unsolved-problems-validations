#!/usr/bin/env python3
"""UFT S52 (WF32 run #1079): coset-support decomposition of the O(theta^2) LU-min coefficient D^2 (Lemma A).
Library: stabilizer group of a pure stabilizer state via Pauli masks, coset labelling, rep-type (L/Bi/Tri),
D^2 parts, and O(theta^2) marginal features (dS2, mixed M2, Haug-Tarabunga W2) by Richardson finite differences.
Qubit q <-> bit (N-1-q) (matches s50 op_on kron ordering: qubit 0 most significant)."""
import itertools, numpy as np
from scipy.linalg import expm
import s50_choi_nonlocal_magic as m
import s51_identity as S51
LN2 = np.log(2)

def pop(a): return np.array([bin(int(v)).count('1') for v in np.atleast_1d(a)])

class Stab:
    def __init__(self, psi, N, tol=1e-9):
        self.N, self.psi = N, psi
        d = 2 ** N; self.idx = np.arange(d)
        self.popz = {}
        M2 = m.M2_pure(psi)
        if abs(M2) > tol: raise ValueError(f"base not a stabilizer state (M2={M2:.3g})")
        E = np.abs(m.pauli_expvals_pure(psi))
        self.S = [(int(x), int(z)) for x, z in zip(*np.nonzero(np.abs(E - 1) < 1e-8))]
        assert len(self.S) == d, len(self.S)
        # generators for syndromes: pick independent set greedily (symplectic)
        self.gens = self._indep(self.S)
        assert len(self.gens) == N

    def apply(self, x, z, v):
        ph = (1j) ** (bin(x & z).count('1')) * (-1.0) ** pop_arr(self.idx & z)
        out = np.empty_like(v); out[self.idx ^ x] = ph * v
        return out

    def expval(self, x, z): return np.vdot(self.psi, self.apply(x, z, self.psi))

    def _indep(self, L):
        basis, rows = [], []
        for (x, z) in L:
            vec = (x << self.N) | z
            r = vec
            for b in rows:
                r = min(r, r ^ b)
            if r:
                rows.append(r); rows.sort(reverse=True); basis.append((x, z))
        return basis

    def syndrome(self, x, z):
        s = 0
        for i, (gx, gz) in enumerate(self.gens):
            c = (bin(x & gz).count('1') + bin(z & gx).count('1')) & 1
            s |= c << i
        return s

_POPC = None
def pop_arr(a):
    global _POPC
    mx = int(a.max()) + 1 if np.size(a) else 1
    if _POPC is None or len(_POPC) < mx:
        n = max(mx, 1 << 12); _POPC = np.array([bin(i).count('1') for i in range(n)])
    return _POPC[a]

def support_parties(x, z, N, parties):
    mask = x | z; out = set()
    for pi, P in enumerate(parties):
        for q in P:
            if mask >> (N - 1 - q) & 1: out.add(pi); break
    return out

def coset_table(st, parties):
    """returns dict syn -> dict(rep=(x,z), type, singles=[(x,z)]) for all 4^N Paulis"""
    N = st.N; d = 2 ** N; T = {}
    for x in range(d):
        for z in range(d):
            s = st.syndrome(x, z)
            if s == 0: continue
            e = T.setdefault(s, dict(rep=(x, z), minparties=4, singles=[]))
            k = len(support_parties(x, z, N, parties))
            e["minparties"] = min(e["minparties"], k)
            if k == 1: e["singles"].append((x, z))
    for e in T.values():
        e["type"] = {1: "L", 2: "Bi", 3: "Tri"}[max(e["minparties"], 1)]
    return T

def decompose(st, T, G):
    """D^2 parts for generator G (full matrix on N qubits). Also returns T_s dimension check."""
    psi = st.psi; Gp = G @ psi
    parts = dict(L=0.0, Bi=0.0, Tri=0.0); maxdim = 0; nT = dict(L=0, Bi=0, Tri=0)
    for s, e in T.items():
        qv = st.apply(*e["rep"], psi)
        c = np.vdot(qv, Gp)
        nT[e["type"]] += 1
        if e["type"] == "L":
            # real span of lambda_P over single reps
            lams = np.array([np.vdot(qv, st.apply(x, z, psi)) for (x, z) in e["singles"]])
            M = np.vstack([lams.real, lams.imag])
            dim = np.linalg.matrix_rank(M, tol=1e-8); maxdim = max(maxdim, dim)
            a, *_ = np.linalg.lstsq(M, np.array([c.real, c.imag]), rcond=None)
            r = np.array([c.real, c.imag]) - M @ a
            parts["L"] += float(r @ r)
        else:
            parts[e["type"]] += abs(c) ** 2
    return parts, maxdim, nT

# ---- marginal features ----
def S2b(rho): return float(-np.log2(np.real(np.trace(rho @ rho))))
def M2mixed_bits(rho):
    return float(m.M2_mixed(rho))   # = -log2 A_2 - S_2 (bits), Haug-Tarabunga eq.(3) mixed SRE

def features(psi, N, parties):
    R, A, B = parties; f = {}
    for name, Q in [("R", R), ("A", A), ("B", B), ("RA", R + A), ("RB", R + B), ("AB", A + B)]:
        rho = m.reduced(psi, N, sorted(Q))
        s2 = S2b(rho); m2 = M2mixed_bits(rho)
        f["S2_" + name] = s2; f["M2_" + name] = m2; f["W2_" + name] = m2 - 2 * s2
    f["I3_2"] = f["S2_R"] + f["S2_A"] + f["S2_B"] - f["S2_RA"] - f["S2_RB"] - f["S2_AB"]  # + S2(RAB)=0
    return f

def feat_theta2(psi0, G, N, parties, th=2e-3):
    f0 = features(psi0, N, parties)
    fa = features(expm(-1j * th * G) @ psi0, N, parties)
    fb = features(expm(-2j * th * G) @ psi0, N, parties)
    out = {}
    for k in f0:
        a = (fa[k] - f0[k]) / th ** 2; b = (fb[k] - f0[k]) / (2 * th) ** 2
        out[k] = 2 * a - b  # Richardson: removes O(theta) term
    return out
