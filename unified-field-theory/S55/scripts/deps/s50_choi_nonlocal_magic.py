#!/usr/bin/env python3
"""UFT Session 50 (ATTEMPT, WF32 run #1023): tripartite Choi-state non-local magic
of small deformed / approximate QECCs vs a non-Clifford angle theta.

Choi state |Phi> = (1/sqrt(d)) sum_i |i>_R (x) V_theta|i>,  V_theta = U_theta V_0,
V_0 = exact stabilizer encoder ([[5,1,3]] or [[4,2,2]]).  Parties: R, A, B.

Quantities (all computed exactly on <=6 qubits, 64-dim state):
  M2_full      pure-state stabilizer 2-Renyi entropy of the Choi state (includes LOCAL magic)
  M2_LUmin     min over U_R (x) U_A (x) U_B of M2  -> numerical UPPER bound on the
               local-unitary non-local SRE (optimizer may miss the global min)
  antiflat[X]  Tr rho_X^3 - (Tr rho_X^2)^2 for X in {R, A, B}.  LU-invariant; exactly 0 for
               any state LU-equivalent to a stabilizer state (flat spectra on every cut).
               => antiflat>0 on any cut is a RIGOROUS certificate of non-local magic > 0.
  M2mix[X]     mixed-state SRE  -log2( sum_P tr(rho P)^4 / sum_P tr(rho P)^2 ) of reduced
               states; 0 on reduced stabilizer states (not an LU invariant, not a monotone).
  I_max        max_{|E|<=e} I(R:E) over physical erasures E the exact code corrects
               (e=2 for [[5,1,3]], e=1 for [[4,2,2]]): 0 iff still an exact erasure code for
               those E; the "approximateness" of the deformed code.
Deformations:
  D1 cross-cut   U = exp(-i theta Z_a Z_b / 2), a in A, b in B   (Clifford at theta = pi/2)
  D2 local       U = exp(-i theta Z_a / 2) on ONE physical qubit (NEGATIVE CONTROL: full magic
                 grows, but non-local magic must stay 0; tests the minimizer can actually
                 remove local magic, i.e. the LUmin number is not trivially 0)
  D3 random      U = exp(-i theta H), H a fixed random 2-qubit Hermitian (||H||_op = 1) on (a,b)
"""
import json, sys, time
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

rng = np.random.default_rng(20260925)

# ---------- Pauli utilities (qubit k <-> bit n-1-k) ----------
PX = np.array([[0, 1], [1, 0]], complex); PZ = np.diag([1., -1.]).astype(complex)
PY = 1j * PX @ PZ; I2 = np.eye(2, dtype=complex)

def op_on(n, ops):
    """ops: dict qubit->2x2"""
    M = np.array([[1.]], complex)
    for k in range(n):
        M = np.kron(M, ops.get(k, I2))
    return M

def pauli_string(s):
    d = {'I': I2, 'X': PX, 'Y': PY, 'Z': PZ}
    return op_on(len(s), {k: d[c] for k, c in enumerate(s)})

_H = {}
def hadamard(n):
    if n not in _H:
        H = np.array([[1.]])
        for _ in range(n):
            H = np.kron(H, np.array([[1., 1.], [1., -1.]]))
        _H[n] = H
    return _H[n]

def pauli_expvals_pure(psi):
    """all |<P>| for P = X^x Z^z (phase irrelevant for 4th/2nd moments)"""
    N = psi.size; n = int(np.log2(N)); idx = np.arange(N)
    F = np.conj(psi[idx[None, :] ^ idx[:, None]]) * psi[None, :]   # F[x,b]
    return F @ hadamard(n)                                          # E[x,z]

def pauli_expvals_mixed(rho):
    N = rho.shape[0]; n = int(np.log2(N)); idx = np.arange(N)
    F = rho[idx[None, :], idx[None, :] ^ idx[:, None]]              # F[x,b] = rho[b, b^x]
    return F @ hadamard(n)

def M2_pure(psi):
    E = np.abs(pauli_expvals_pure(psi)); N = psi.size
    return -np.log2(np.sum(E ** 4) / N)

def M2_mixed(rho):
    E = np.abs(pauli_expvals_mixed(rho))
    return -np.log2(np.sum(E ** 4) / np.sum(E ** 2))

# ---------- reduced states ----------
def reduced(psi, n, keep):
    keep = sorted(keep); rest = [k for k in range(n) if k not in keep]
    T = psi.reshape([2] * n).transpose(keep + rest).reshape(2 ** len(keep), -1)
    return T @ T.conj().T

def entropy(rho):
    w = np.linalg.eigvalsh(rho); w = w[w > 1e-14]
    return float(-np.sum(w * np.log2(w)))

def antiflat(rho):
    return float(np.real(np.trace(rho @ rho @ rho) - np.trace(rho @ rho) ** 2))

# ---------- codes ----------
def stab_code(n, stabs, xlogs, zlogs):
    P = np.eye(2 ** n, dtype=complex)
    for s in stabs:
        P = P @ (np.eye(2 ** n) + pauli_string(s)) / 2
    for z in zlogs:                      # fix |0...0>_L
        P = P @ (np.eye(2 ** n) + pauli_string(z)) / 2
    v = P[:, 0].copy()                   # P|0...0>
    if np.linalg.norm(v) < 1e-9:
        raise RuntimeError("bad seed")
    v /= np.linalg.norm(v)
    k = len(xlogs); cols = []
    for i in range(2 ** k):
        w = v.copy()
        for j in range(k):
            if (i >> (k - 1 - j)) & 1:
                w = pauli_string(xlogs[j]) @ w
        cols.append(w)
    V = np.array(cols).T                 # 2^n x 2^k isometry
    assert np.allclose(V.conj().T @ V, np.eye(2 ** k), atol=1e-10)
    return V

CODES = {
    "513": dict(n=5, k=1, V=stab_code(5, ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"], ["XXXXX"], ["ZZZZZ"]),
                A=[0, 1], B=[2, 3, 4], cut=(1, 2), erasure=2),
    "422": dict(n=4, k=2, V=stab_code(4, ["XXXX", "ZZZZ"], ["XXII", "XIXI"], ["ZIZI", "ZZII"]),
                A=[0, 1], B=[2, 3], cut=(1, 2), erasure=1),
}

def choi(V, k):
    dR = 2 ** k
    psi = np.zeros(dR * V.shape[0], complex)
    for i in range(dR):
        e = np.zeros(dR); e[i] = 1
        psi += np.kron(e, V[:, i])
    return psi / np.sqrt(dR)

def deform_unitary(code, kind, theta, Hrand):
    n = code["n"]; a, b = code["cut"]
    if kind == "D1":
        G = op_on(n, {a: PZ, b: PZ}) / 2
    elif kind == "D2":
        G = op_on(n, {a: PZ}) / 2
    elif kind == "D3":
        # embed 4x4 Hrand on qubits (a,b) (adjacent, a<b)
        assert b == a + 1
        G = np.kron(np.kron(np.eye(2 ** a), Hrand), np.eye(2 ** (n - b - 1)))
    return expm(-1j * theta * G)

# ---------- LU minimization over U_R (x) U_A (x) U_B ----------
def herm_from(p, d):
    H = np.zeros((d, d), complex); iu = np.triu_indices(d, 1)
    m = len(iu[0])
    H[iu] = p[:m] + 1j * p[m:2 * m]
    H = H + H.conj().T
    H[np.diag_indices(d)] = p[2 * m:2 * m + d]
    return H

def nparams(d): return d * d

def lu_min(psi, dims, restarts=4, maxiter=400):
    """dims = (dR, dA, dB) consistent with psi ordering R,A,B"""
    sizes = [nparams(d) for d in dims]
    T = psi.reshape(dims)
    def apply(p):
        off = 0; Us = []
        for d, s in zip(dims, sizes):
            Us.append(expm(1j * herm_from(p[off:off + s], d))); off += s
        X = np.einsum('ai,bj,ck,ijk->abc', Us[0], Us[1], Us[2], T, optimize=True)
        return X.reshape(-1)
    f = lambda p: M2_pure(apply(p))
    best = (M2_pure(psi), None)
    for r in range(restarts):
        p0 = rng.normal(scale=(0.0 if r == 0 else 0.6), size=sum(sizes))
        if r == 0: p0 += 1e-3 * rng.normal(size=sum(sizes))
        res = minimize(f, p0, method="L-BFGS-B", options=dict(maxiter=maxiter))
        if res.fun < best[0]:
            best = (float(res.fun), res.x)
    return best[0]

def mutual_info_max(psi, code):
    n = code["n"]; k = code["k"]; ntot = k + n
    R = list(range(k)); best = 0.0
    from itertools import combinations
    SR = entropy(reduced(psi, ntot, R))
    for e in range(1, code["erasure"] + 1):
        for E in combinations(range(n), e):
            Eg = [k + q for q in E]
            I = SR + entropy(reduced(psi, ntot, Eg)) - entropy(reduced(psi, ntot, R + Eg))
            best = max(best, I)
    return best

def analyze(code, psi):
    k = code["k"]; n = code["n"]; ntot = k + n
    R = list(range(k)); A = [k + q for q in code["A"]]; B = [k + q for q in code["B"]]
    out = dict(M2_full=float(M2_pure(psi)))
    for name, X in (("R", R), ("A", A), ("B", B)):
        rho = reduced(psi, ntot, X)
        out["antiflat_" + name] = antiflat(rho)
        out["M2mix_" + name] = float(M2_mixed(rho))
    out["I_max"] = float(mutual_info_max(psi, code))
    return out

def main(fast=False):
    thetas = [0.0, 0.025, 0.05, 0.1, 0.2, 0.4, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2]
    Hr = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)); Hr = (Hr + Hr.conj().T) / 2
    Hr /= np.linalg.norm(Hr, 2)
    results = []
    for cname, code in CODES.items():
        k, n = code["k"], code["n"]
        dims = (2 ** k, 2 ** len(code["A"]), 2 ** len(code["B"]))
        for kind in ("D1", "D2", "D3"):
            for th in thetas:
                t0 = time.time()
                V = deform_unitary(code, kind, th, Hr) @ code["V"]
                psi = choi(V, k)
                r = dict(code=cname, deform=kind, theta=float(th))
                r.update(analyze(code, psi))
                import s50_lumin as L
                r["M2_LUmin"] = float(L.lu_min(psi, dims, restarts=(2 if fast else 5), rng=rng))
                r["sec"] = round(time.time() - t0, 1)
                results.append(r)
                print(json.dumps(r), flush=True)
    return results

if __name__ == "__main__":
    res = main(fast="--fast" in sys.argv)
    json.dump(res, open(sys.argv[-1] if sys.argv[-1].endswith(".json") else "s50_results.json", "w"), indent=1)
