#!/usr/bin/env python3
"""UFT S53 (WF32 run #1108): half-coset theorem (D1), code-only cross-cut criterion (D2), Renyi-2 marginal formula (D3), S51(iii) (D4).
Builds on s52_coset.Stab (qubit q <-> bit N-1-q). Everything combinatorial except a_s = <Q_s psi0 | G psi0>."""
import itertools, numpy as np
import s50_choi_nonlocal_magic as m, s51_identity as S51, s52_coset as C
LN2 = np.log(2)

def symp(x1, z1, x2, z2): return (bin(x1 & z2).count('1') + bin(z1 & x2).count('1')) & 1

def party_mask(N, P):
    mk = 0
    for q in P: mk |= 1 << (N - 1 - q)
    return mk

class HalfCosets:
    """For each nontrivial coset s: rep Q_s, flags goodH (half commuting with Q_s has a single-party Pauli), goodHb (anticommuting half has one)."""
    def __init__(self, st, parties):
        self.st, self.parties = st, parties; N = st.N; d = 2 ** N
        masks = [party_mask(N, P) for P in parties]
        self.rep = {}; self.good = {}
        allm = d - 1
        for x in range(d):
            for z in range(d):
                s = st.syndrome(x, z)
                if s == 0: continue
                if s not in self.rep: self.rep[s] = (x, z); self.good[s] = [False, False]
                sup = x | z
                single = any((sup & ~mk & allm) == 0 for mk in masks)
                if single:
                    qx, qz = self.rep[s]; self.good[s][symp(x, z, qx, qz)] = True
        self.masks = masks

    def a_s(self, G):
        psi = self.st.psi; Gp = G @ psi
        return {s: np.vdot(self.st.apply(*q, psi), Gp) for s, q in self.rep.items()}

    def D2(self, G, a=None):
        a = a or self.a_s(G); tot = 0.0
        for s, (gh, ghb) in self.good.items():
            if not gh: tot += a[s].real ** 2
            if not ghb: tot += a[s].imag ** 2
        return tot

    def is_bad_pauli(self, x, z):
        s = self.st.syndrome(x, z)
        if s == 0: return False
        qx, qz = self.rep[s]; return not self.good[s][symp(x, z, qx, qz)]

    def marginal_formula(self, G, X, a=None):
        """D3: Delta S2(X)/theta^2 = (2F'-4E)/ln2 ; X = list of qubits"""
        st = self.st; N = st.N; mk = party_mask(N, X); allm = 2 ** N - 1
        SX = [(x, z) for (x, z) in st.S if ((x | z) & ~mk & allm) == 0 and (x | z) != 0]
        a = a or self.a_s(G)
        # X-rep existence per coset
        hasrep = {}
        sub = [b for b in range(N) if mk >> b & 1]
        for bits in itertools.product(range(4), repeat=len(sub)):
            x = z = 0
            for b, v in zip(sub, bits):
                x |= (v & 1) << b; z |= (v >> 1) << b
            s = st.syndrome(x, z)
            if s and s not in hasrep: hasrep[s] = (x, z)
        Fp = E = 0.0
        for s, (qx, qz) in self.rep.items():
            flipped = any(symp(qx, qz, tx, tz) for (tx, tz) in SX)
            if flipped and s not in hasrep: Fp += abs(a[s]) ** 2
            if (not flipped) and s in hasrep:
                rx, rz = hasrep[s]
                r = a[s] if symp(rx, rz, qx, qz) == 0 else a[s] * (-1j)  # rotate into rep's half (sign irrelevant, squared)
                E += r.imag ** 2
        return (2 * Fp - 4 * E) / LN2, Fp, E

def S2X(psi, N, X): return C.S2b(m.reduced(psi, N, sorted(X)))

def fd_dS2(psi0, G, N, X, th=2e-3):
    from scipy.linalg import expm
    f0 = S2X(psi0, N, X); fa = S2X(expm(-1j * th * G) @ psi0, N, X); fb = S2X(expm(-2j * th * G) @ psi0, N, X)
    return 2 * (fa - f0) / th ** 2 - (fb - f0) / (2 * th) ** 2

def gen_G_multi(n, k, qubits, rng):
    N = n + k; L = len(qubits); dd = 2 ** L
    H = rng.normal(size=(dd, dd)) + 1j * rng.normal(size=(dd, dd)); H = (H + H.conj().T) / 2; H /= np.linalg.norm(H, 2)
    G = np.zeros((2 ** N, 2 ** N), complex); g = {}
    for labs in itertools.product('IXYZ', repeat=L):
        P = S51.P1[labs[0]]
        for c in labs[1:]: P = np.kron(P, S51.P1[c])
        c = float(np.real(np.trace(P @ H) / dd)); g[''.join(labs)] = c
        G += c * m.op_on(N, {k + q: S51.P1[l] for q, l in zip(qubits, labs)})
    return G, g

def code_criterion(st, k, n, Aphys, Bphys, x, z):
    """D2: bad iff P not in N(H) and no h in H with (h|B ~ P_B and [h|A,P_A]=0) or (h|A ~ P_A and [h|B,P_B]=0). P physical (x,z masks on N bits)."""
    N = st.N; Rm = party_mask(N, range(k)); Am = party_mask(N, [k + q for q in Aphys]); Bm = party_mask(N, [k + q for q in Bphys])
    Hs = [(hx, hz) for (hx, hz) in st.S if ((hx | hz) & Rm) == 0]
    if st.syndrome(x, z) == 0: return False   # in +-H (stabilizer) -> trivial
    if all(symp(x, z, hx, hz) == 0 for hx, hz in Hs): return False  # normalizer (logical) -> removable
    for hx, hz in Hs:
        for M1, M2 in ((Am, Bm), (Bm, Am)):
            if (hx & M2) == (x & M2) and (hz & M2) == (z & M2) and symp(hx & M1, hz & M1, x & M1, z & M1) == 0:
                return False
    return True
