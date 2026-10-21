#!/usr/bin/env python3
"""
VALIDATE session 2026-08-01 — Unified Field Theory (unsolved_problems id=6)

Claim under test (Esposito et al., arXiv:2606.29443v2, per research_findings
id 4237 / session 38 synthesis):

    Linear Stabilizer Entropy (purity-normalized) acts as a proper mixed-state
    non-stabilizerness (magic) monotone "with overwhelming probability", with
    violation probabilities decaying as exp(-eta * N) in system size N.

Why it matters here: NOVA's reduced-state SRE (Sarkar-Biswas) spacetime order
parameter takes partial traces of a global state and treats the resulting
mixed-state linear SRE as a magic monotone. If monotonicity fails badly at
small N, the order parameter's interpretation is unsafe.

Independent numerical test:
  Definition (standard purity-normalized linear SRE for mixed states):
      M_lin(rho) = 1 - sum_P Tr(rho P)^4 / sum_P Tr(rho P)^2
  where the sum runs over all 4^N Pauli strings. Properties expected of a
  monotone: M_lin = 0 on stabilizer pure states and the maximally mixed state,
  invariance under Clifford unitaries, and non-increase under free (stabilizer)
  operations: computational-basis dephasing, discarding a qubit (partial
  trace), Pauli channels, and (on average) selective computational-basis
  measurement.

  Protocol: for N = 2..5 qubits, draw random magic-rich states (rank-2 mixed
  states from tracing one env qubit off a Haar-random pure state, and
  full-rank Hilbert-Schmidt random density matrices), apply each free
  operation, and record Delta M = M_after - M_before. A violation is
  Delta M > TOL. Track violation frequency and magnitude per N.

Outcome categories: confirmed / discrepancy / inconclusive (recorded in
progress_notes by the orchestrating session).
"""
import numpy as np
import json, sys, time

rng = np.random.default_rng(20260801)
TOL = 1e-9

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS1 = [I2, X, Y, Z]

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.array([[1, 0], [0, 1j]], dtype=complex)

# ---------- Pauli basis (precomputed, stacked) ----------
_basis_cache = {}
def pauli_basis(n):
    if n in _basis_cache:
        return _basis_cache[n]
    mats = [np.array([[1]], dtype=complex)]
    for _ in range(n):
        mats = [np.kron(m, p) for m in mats for p in PAULIS1]
    B = np.stack(mats)  # shape (4^n, 2^n, 2^n)
    _basis_cache[n] = B
    return B

def m_lin(rho):
    n = int(np.log2(rho.shape[0]))
    B = pauli_basis(n)
    c = np.einsum('kij,ji->k', B, rho).real  # Tr(rho P) real for Hermitian rho
    s2 = np.sum(c**2)
    s4 = np.sum(c**4)
    return 1.0 - s4 / s2

# ---------- random states ----------
def haar_pure(n):
    d = 2**n
    v = rng.normal(size=d) + 1j * rng.normal(size=d)
    v /= np.linalg.norm(v)
    return v

def rank2_mixed(n):
    """Trace one env qubit off a Haar pure state on n+1 qubits."""
    v = haar_pure(n + 1).reshape(2**n, 2)
    return v @ v.conj().T

def hs_random(n):
    d = 2**n
    G = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    rho = G @ G.conj().T
    return rho / np.trace(rho).real

# ---------- operators on n qubits ----------
def op_on(qubit, n, gate):
    m = np.array([[1]], dtype=complex)
    for q in range(n):
        m = np.kron(m, gate if q == qubit else I2)
    return m

def cnot(c, t, n):
    d = 2**n
    U = np.zeros((d, d), dtype=complex)
    for b in range(d):
        bits = [(b >> (n - 1 - q)) & 1 for q in range(n)]
        if bits[c]:
            bits[t] ^= 1
        b2 = 0
        for q in range(n):
            b2 = (b2 << 1) | bits[q]
        U[b2, b] = 1
    return U

def random_clifford(n, depth=40):
    d = 2**n
    U = np.eye(d, dtype=complex)
    for _ in range(depth):
        kind = rng.integers(3)
        if kind == 0:
            U = op_on(rng.integers(n), n, H) @ U
        elif kind == 1:
            U = op_on(rng.integers(n), n, S) @ U
        elif n >= 2:
            c, t = rng.choice(n, size=2, replace=False)
            U = cnot(c, t, n) @ U
    return U

# ---------- free operations ----------
def dephase_qubit(rho, q, n):
    """Computational-basis measurement on qubit q, outcome forgotten."""
    P0 = op_on(q, n, np.array([[1, 0], [0, 0]], dtype=complex))
    P1 = op_on(q, n, np.array([[0, 0], [0, 1]], dtype=complex))
    return P0 @ rho @ P0 + P1 @ rho @ P1

def ptrace_last(rho, n):
    """Discard the last qubit."""
    r = rho.reshape(2**(n-1), 2, 2**(n-1), 2)
    return np.einsum('iajb->ij', r[:, :, :, :][:, np.arange(2), :, np.arange(2)].transpose(1, 0, 2)) \
        if False else np.trace(r, axis1=1, axis2=3)

def pauli_channel(rho, n, k=4):
    B = pauli_basis(n)
    idx = rng.choice(len(B), size=k, replace=False)
    p = rng.dirichlet(np.ones(k))
    out = np.zeros_like(rho)
    for w, i in zip(p, idx):
        out += w * (B[i] @ rho @ B[i])
    return out

def selective_measure_avg(rho, q, n):
    """Selective comp-basis measurement: return (probs, post-states)."""
    P0 = op_on(q, n, np.array([[1, 0], [0, 0]], dtype=complex))
    P1 = op_on(q, n, np.array([[0, 0], [0, 1]], dtype=complex))
    out = []
    for P in (P0, P1):
        s = P @ rho @ P
        p = np.trace(s).real
        if p > 1e-12:
            out.append((p, s / p))
    return out

# ---------- experiment ----------
def run():
    results = {}
    NS = [2, 3, 4, 5]
    TRIALS = 150
    t0 = time.time()

    # sanity checks
    assert abs(m_lin(np.eye(4) / 4)) < 1e-12, "maximally mixed must be free"
    zz = np.zeros((4, 4), dtype=complex); zz[0, 0] = 1
    assert abs(m_lin(zz)) < 1e-12, "|00> must be free"
    tstate = np.array([1, np.exp(1j*np.pi/4)], dtype=complex) / np.sqrt(2)
    tt = np.outer(tstate, tstate.conj())
    m_t = m_lin(np.kron(tt, tt))
    assert m_t > 0.1, "T-state tensor product must have magic"
    print(f"sanity OK  (M_lin(T⊗T) = {m_t:.6f})")

    for N in NS:
        stats = {op: {"trials": 0, "violations": 0, "max_viol": 0.0,
                      "mean_delta": 0.0}
                 for op in ("clifford", "dephase", "ptrace", "pauli_ch",
                            "selective_avg")}
        for trial in range(TRIALS):
            rho = rank2_mixed(N) if trial % 2 == 0 else hs_random(N)
            m0 = m_lin(rho)

            # 1. Clifford invariance
            U = random_clifford(N)
            d = m_lin(U @ rho @ U.conj().T) - m0
            _rec(stats["clifford"], d)

            # 2. dephasing
            d = m_lin(dephase_qubit(rho, rng.integers(N), N)) - m0
            _rec(stats["dephase"], d)

            # 3. partial trace (discard last qubit)
            d = m_lin(ptrace_last(rho, N)) - m0
            _rec(stats["ptrace"], d)

            # 4. Pauli channel
            d = m_lin(pauli_channel(rho, N)) - m0
            _rec(stats["pauli_ch"], d)

            # 5. selective measurement, outcome-averaged monotonicity
            branches = selective_measure_avg(rho, rng.integers(N), N)
            avg = sum(p * m_lin(s) for p, s in branches)
            _rec(stats["selective_avg"], avg - m0)

        for op in stats:
            st = stats[op]
            st["mean_delta"] /= max(st["trials"], 1)
            st["violation_rate"] = st["violations"] / max(st["trials"], 1)
        results[N] = stats
        print(f"N={N} done ({time.time()-t0:.1f}s)")

    return results

def _rec(st, d):
    st["trials"] += 1
    st["mean_delta"] += d
    if d > TOL:
        st["violations"] += 1
        st["max_viol"] = max(st["max_viol"], d)

if __name__ == "__main__":
    res = run()
    print("\n=== RESULTS: violation rate (Delta M_lin > 1e-9) by op and N ===")
    hdr = f"{'op':14s}" + "".join(f"  N={n}: rate / max_viol      " for n in res)
    print(hdr)
    ops = list(next(iter(res.values())).keys())
    for op in ops:
        row = f"{op:14s}"
        for n in res:
            st = res[n][op]
            row += f"  {st['violation_rate']:.3f} / {st['max_viol']:.2e}   "
        print(row)
    print("\nmean Delta M_lin by op and N (negative = magic decreased):")
    for op in ops:
        row = f"{op:14s}"
        for n in res:
            row += f"  {res[n][op]['mean_delta']:+.5f}   "
        print(row)
    with open(__file__.replace(".py", "-results.json"), "w") as f:
        json.dump({str(k): v for k, v in res.items()}, f, indent=2)
    print("\nresults JSON written.")
