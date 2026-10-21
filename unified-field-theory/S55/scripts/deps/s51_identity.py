#!/usr/bin/env python3
"""UFT S51 (WF32 run #1061): test the S50 small-theta identity LUmin M2 = 2 I(R:A) and the S51 derivation.
For each (code, deformation G, tripartition R|A|B):
  M2full/th^2 vs Lemma-1 prediction 4 Var(G)/ln2
  LU_tan  = 4/ln2 * dist^2_R( (1-P0)G psi0 , span_R{(1-P0) P psi0 : P single-party Pauli} )   [exact O(th^2) LU-min, Lemma 2]
  LU_opt  = numerical LU-minimized M2 at th (s50_lumin), divided by th^2        [optimizer, only for subset]
  IvN, I2 = I(R:A) von Neumann / Renyi-2 at th, /th^2
  defA2   = |A| - S2(rho_A(th)), defRA2 = |RA| - S2(rho_RA(th))  (/th^2)
  base flags: rho_R, rho_A, rho_RA maximally mixed at th=0
"""
import json, sys, itertools, time
import numpy as np
from scipy.linalg import expm
import s50_choi_nonlocal_magic as m
import s50_lumin as L
LN2 = np.log(2)
P1 = {'I': m.I2, 'X': m.PX, 'Y': m.PY, 'Z': m.PZ}

# ---------------- codes ----------------
def random_clifford_encoder(n, k, rng, depth=None):
    depth = depth or 20 * n
    Hd = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2); Sg = np.diag([1, 1j])
    U = np.eye(2 ** n, dtype=complex)
    for _ in range(depth):
        r = rng.integers(3)
        if r == 0: U = m.op_on(n, {int(rng.integers(n)): Hd}) @ U
        elif r == 1: U = m.op_on(n, {int(rng.integers(n)): Sg}) @ U
        else:
            a, b = rng.choice(n, 2, replace=False)
            C = m.op_on(n, {a: np.diag([1, 0]).astype(complex)}) + m.op_on(n, {a: np.diag([0, 1]).astype(complex), b: m.PX})
            U = C @ U
    # V|i> = U (|i> (x) |0^{n-k}>)
    cols = []
    for i in range(2 ** k):
        e = np.zeros(2 ** n, complex); e[i << (n - k)] = 1; cols.append(U @ e)
    return np.array(cols).T

def steane():
    Hs = ["IIIXXXX", "IXXIIXX", "XIXIXIX"]
    st = Hs + [h.replace('X', 'Z') for h in Hs]
    return m.stab_code(7, st, ["XXXXXXX"], ["ZZZZZZZ"])

def get_codes(rng):
    C = {"513": (5, 1, m.CODES["513"]["V"]), "422": (4, 2, m.CODES["422"]["V"]), "713": (7, 1, steane())}
    C["rnd61"] = (6, 1, random_clifford_encoder(6, 1, rng))
    return C

def is_stab_state(psi):
    return abs(m.M2_pure(psi)) < 1e-9

# ---------------- helpers ----------------
def perm_state(psi, N, order):
    return psi.reshape([2] * N).transpose(order).reshape(-1)

def S2(rho): return float(-np.log2(np.real(np.trace(rho @ rho))))

def party_paulis(N, qubits):
    for labels in itertools.product('IXYZ', repeat=len(qubits)):
        if all(c == 'I' for c in labels): continue
        yield m.op_on(N, {q: P1[c] for q, c in zip(qubits, labels)})

def lu_tan(psi0, Gfull, N, parties):
    """exact O(th^2) coefficient of LU-min M2 (per th^2)"""
    Pi = lambda x: x - psi0 * np.vdot(psi0, x)
    v = Pi(Gfull @ psi0)
    cols = []
    for Q in parties:
        for P in party_paulis(N, Q):
            cols.append(Pi(P @ psi0))
    Mx = np.array(cols).T
    Mr = np.vstack([Mx.real, Mx.imag]); vr = np.concatenate([v.real, v.imag])
    a, *_ = np.linalg.lstsq(Mr, vr, rcond=None)
    res = vr - Mr @ a
    return 4 * float(res @ res) / LN2, 4 * float(np.real(np.vdot(v, v))) / LN2

def mi(psi, N, R, A):
    rR, rA, rRA = m.reduced(psi, N, R), m.reduced(psi, N, A), m.reduced(psi, N, R + A)
    IvN = m.entropy(rR) + m.entropy(rA) - m.entropy(rRA)
    I2 = S2(rR) + S2(rA) - S2(rRA)
    return IvN, I2, len(A) - S2(rA), len(R + A) - S2(rRA), len(A) - m.entropy(rA)

def gen_G(Nphys, qubits, rng, k):
    H = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)); H = (H + H.conj().T) / 2
    H /= np.linalg.norm(H, 2)
    # embed on physical qubits (global index k+q); build via Pauli expansion
    N = Nphys + k
    G = np.zeros((2 ** N, 2 ** N), complex)
    for a, b in itertools.product('IXYZ', repeat=2):
        Pab = np.kron(P1[a], P1[b]); c = np.trace(Pab @ H) / 4
        if abs(c) > 0: G += c * m.op_on(N, {k + qubits[0]: P1[a], k + qubits[1]: P1[b]})
    return G

def run_case(code, n, k, V, G, A_phys, th, do_opt, rng):
    N = n + k; R = list(range(k)); A = [k + q for q in A_phys]; B = [q for q in range(N) if q not in R + A]
    psi0 = m.choi(V, k)
    out = dict(code=code, A=A_phys, B=[q - k for q in B])
    out["base_maxmixed"] = dict(R=bool(abs(S2(m.reduced(psi0, N, R)) - len(R)) < 1e-9),
                                A=bool(abs(S2(m.reduced(psi0, N, A)) - len(A)) < 1e-9),
                                RA=bool(abs(S2(m.reduced(psi0, N, R + A)) - len(R + A)) < 1e-9),
                                B=bool(abs(S2(m.reduced(psi0, N, B)) - len(B)) < 1e-9))
    out["LU_tan"], out["M2pred"] = lu_tan(psi0, G, N, [R, A, B])
    psi = expm(-1j * th * G) @ psi0
    out["M2full"] = m.M2_pure(psi) / th ** 2
    b = mi(psi0, N, R, A); out["base_IvN"], out["base_I2"] = b[0], b[1]
    IvN, I2, dA2, dRA2, dAvN = [x - y for x, y in zip(mi(psi, N, R, A), b)]   # changes from theta=0
    out.update(IvN=IvN / th ** 2, I2=I2 / th ** 2, defA2=dA2 / th ** 2, defRA2=dRA2 / th ** 2, defAvN=dAvN / th ** 2)
    if do_opt:
        order = R + A + B
        ps = perm_state(psi, N, order)
        t0 = time.time()
        out["LU_opt"] = L.lu_min(ps, (2 ** len(R), 2 ** len(A), 2 ** len(B)), restarts=3, rng=rng, iters=4000) / th ** 2
        out["opt_sec"] = round(time.time() - t0, 1)
    return out

if __name__ == "__main__":
    pass
