#!/usr/bin/env python3
"""
S43 VALIDATE — Numerical evaluation of Schmidt-gauge basis-invariant magic
on reduced stabilizer states and random states to verify monotonicity and faithfulness.

This script implements:
1. Schmidt-gauge Stabilizer Rényi Entropy formulation of Franchini-Giampaolo (arXiv:2607.07808v1, arXiv:2608.02745v2):
   M2_Sch(lambdas) = -log2( 2^-m * sum_{s, k in F_2^m} A_s(k)^4 )
   where A_s(k) = sum_x sqrt(lambda_x * lambda_{x ^ s}) * (-1)^{k . x}
2. Viscardi-Leone-Hamma closed-form log-stabilizer fidelity formulation (arXiv:2609.04119v1, Sep 3, 2026):
   D_stab_NL(lambdas) = -log2( max_{k <= m} 2^-k * (sum_{i=1}^{2^k} theta_i^\downarrow)^2 )
   where theta_i^\downarrow = sqrt(lambda_i^\downarrow) are the descending Schmidt coefficients.

It validates:
- FAITHFULNESS: Both measures must be exactly 0 (within TOL) on any reduced stabilizer state.
- MONOTONICITY: For any mixed state rho, any stabilizer free operation E (dephasing, partial trace, General Pauli Channel, selective average) must satisfy:
  M(E(rho)) <= M(rho) + TOL
"""

import numpy as np
import scipy.linalg as la
import json, sys, time

# Seed for reproducible results
rng = np.random.default_rng(20260907)
TOL = 1e-9

# Standard 1-qubit gates
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS1 = [I2, X, Y, Z]

H_gate = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S_gate = np.array([[1, 0], [0, 1j]], dtype=complex)

# Stacked Pauli strings helper
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

# 1. Franchini-Giampaolo Schmidt-gauge Stabilizer Rényi Entropy M2_Sch
def compute_M2_Sch(lambdas):
    lambdas = np.array(lambdas, dtype=float)
    # Filter out extremely small values and normalize
    lambdas[lambdas < 1e-15] = 0.0
    if np.sum(lambdas) == 0:
        return 0.0
    lambdas = lambdas / np.sum(lambdas)
    
    d = len(lambdas)
    m = int(np.round(np.log2(d)))
    assert 2**m == d, f"Dimension {d} must be a power of 2"
    
    theta = np.sqrt(lambdas)
    
    # Generate Walsh-Hadamard matrix of size d x d without 1/sqrt(d) factor
    W = np.array([[1, 1], [1, -1]], dtype=float)
    for _ in range(m - 1):
        W = np.kron(W, np.array([[1, 1], [1, -1]], dtype=float))
        
    total_sum = 0.0
    for s in range(d):
        f_s = np.zeros(d, dtype=float)
        for x in range(d):
            f_s[x] = theta[x] * theta[x ^ s]
        A_s = W @ f_s
        total_sum += np.sum(A_s**4)
        
    val = 2**(-m) * total_sum
    # Avoid log of zero or negative numbers due to numerical noise
    if val <= 1e-15:
        return 0.0
    return -np.log2(val)

# 2. Viscardi-Leone-Hamma closed-form log-stabilizer fidelity D_stab_NL
def compute_D_stab_NL(lambdas):
    lambdas = np.array(lambdas, dtype=float)
    lambdas[lambdas < 1e-15] = 0.0
    if np.sum(lambdas) == 0:
        return 0.0
    lambdas = lambdas / np.sum(lambdas)
    
    d = len(lambdas)
    m = int(np.round(np.log2(d)))
    assert 2**m == d, f"Dimension {d} must be a power of 2"
    
    # Sorted in descending order
    lambdas_sorted = np.sort(lambdas)[::-1]
    theta_sorted = np.sqrt(lambdas_sorted)
    
    max_val = -np.inf
    for k in range(m + 1):
        idx_limit = 2**k
        sum_theta = np.sum(theta_sorted[:idx_limit])
        val = 2**(-k) * (sum_theta**2)
        if val > max_val:
            max_val = val
            
    if max_val <= 1e-15:
        return 0.0
    return -np.log2(max_val)

# Clifford operations helper
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
        if bits[c] == 1:
            bits[t] ^= 1
        new_b = 0
        for q in range(n):
            new_b = (new_b << 1) | bits[q]
        U[new_b, b] = 1.0
    return U

# Generate a random stabilizer state of n qubits
def random_stabilizer_state(n):
    # Start with |0>^n
    v = np.zeros(2**n, dtype=complex)
    v[0] = 1.0
    
    # Apply random Clifford gates to generate a random stabilizer state
    num_gates = n * 5 + 5
    for _ in range(num_gates):
        gtype = rng.choice(["H", "S", "CNOT"])
        if gtype == "H":
            q = rng.integers(n)
            v = op_on(q, n, H_gate) @ v
        elif gtype == "S":
            q = rng.integers(n)
            v = op_on(q, n, S_gate) @ v
        elif gtype == "CNOT" and n > 1:
            c, t = rng.choice(n, size=2, replace=False)
            v = cnot(c, t, n) @ v
    return v

# Tracing out last qubit (partial trace)
def ptrace_last(rho, n):
    r = rho.reshape(2**(n - 1), 2, 2**(n - 1), 2)
    return np.trace(r, axis1=1, axis2=3)

# Comp-basis dephasing on a qubit
P0_1 = np.array([[1, 0], [0, 0]], dtype=complex)
P1_1 = np.array([[0, 0], [0, 1]], dtype=complex)

def dephase(rho, q, n):
    P0 = op_on(q, n, P0_1)
    P1 = op_on(q, n, P1_1)
    return P0 @ rho @ P0 + P1 @ rho @ P1

# General Pauli channel on a qubit
def pauli_channel_on_qubit(rho, q, n, weights=None):
    if weights is None:
        # random probability distribution on I, X, Y, Z
        weights = rng.dirichlet(np.ones(4))
    
    out = np.zeros_like(rho)
    for w, P in zip(weights, PAULIS1):
        cop = op_on(q, n, P)
        out += w * (cop @ rho @ cop)
    return out

# Selective average (on average, selective computational basis measurement on a qubit q)
def selective_avg(rho, q, n, magic_func):
    P0 = op_on(q, n, P0_1)
    P1 = op_on(q, n, P1_1)
    
    m0 = magic_func(la.eigvalsh(rho))
    
    acc = 0.0
    for P in (P0, P1):
        s = P @ rho @ P
        p = np.trace(s).real
        if p > 1e-12:
            eigs = la.eigvalsh(s / p)
            acc += p * magic_func(eigs)
    return acc - m0

# Random general mixed states for testing
def random_mixed_state(n):
    # Trace one env qubit off a Haar-random pure state on n+1 qubits
    d = 2**(n+1)
    v = rng.normal(size=d) + 1j * rng.normal(size=d)
    v /= np.linalg.norm(v)
    v = v.reshape(2**n, 2)
    rho = v @ v.conj().T
    return rho / np.trace(rho).real

def random_hs_mixed_state(n):
    d = 2**n
    G = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    rho = G @ G.conj().T
    return rho / np.trace(rho).real

def main():
    print("="*60)
    print("S43 VALIDATION RUN — SCHMIDT-GAUGE BASIS-INVARIANT MAGIC")
    print("="*60)
    
    # ---------------- TEST 1: FAITHFULNESS ON REDUCED STABILIZER STATES ----------------
    print("\n--- TEST 1: FAITHFULNESS ON REDUCED STABILIZER STATES ---")
    faithfulness_errors_m2 = 0
    faithfulness_errors_dstab = 0
    num_stabilizer_trials = 200
    
    for trial in range(num_stabilizer_trials):
        n = rng.choice([2, 3, 4])
        # Generate random pure stabilizer state
        v = random_stabilizer_state(n)
        rho_pure = np.outer(v, v.conj())
        
        # Take partial trace over last qubit to get a reduced stabilizer state
        rho_reduced = ptrace_last(rho_pure, n)
        eigs = la.eigvalsh(rho_reduced)
        
        # Since it is a reduced stabilizer state, its eigenvalues must be flat on its support
        # We compute both Schmidt-gauge magic formulations
        m2_sch_val = compute_M2_Sch(eigs)
        dstab_nl_val = compute_D_stab_NL(eigs)
        
        if m2_sch_val > TOL:
            print(f"[Trial {trial}] Faithfulness violation M2_Sch = {m2_sch_val:.3e} for reduced stabilizer state of size {n-1}")
            faithfulness_errors_m2 += 1
        if dstab_nl_val > TOL:
            print(f"[Trial {trial}] Faithfulness violation D_stab_NL = {dstab_nl_val:.3e} for reduced stabilizer state of size {n-1}")
            faithfulness_errors_dstab += 1
            
    print(f"Stabilizer Trials: {num_stabilizer_trials}")
    print(f"M2_Sch Faithfulness Violations (> {TOL}): {faithfulness_errors_m2}")
    print(f"D_stab_NL Faithfulness Violations (> {TOL}): {faithfulness_errors_dstab}")
    
    # ---------------- TEST 2: MONOTONICITY UNDER FREE OPERATIONS ----------------
    print("\n--- TEST 2: MONOTONICITY UNDER FREE OPERATIONS ON RANDOM STATES ---")
    num_mono_trials = 1000
    ops = ["dephase", "ptrace", "pauli_ch", "selective_avg"]
    
    mono_violations = {op: {"M2_Sch": 0, "D_stab_NL": 0, "max_viol_M2": -np.inf, "max_viol_D": -np.inf} for op in ops}
    
    for trial in range(num_mono_trials):
        n = rng.choice([2, 3])  # test 2 and 3 qubits
        
        # 50% Haar-reduced rank-2 mixed state, 50% Hilbert-Schmidt full rank
        if trial % 2 == 0:
            rho = random_mixed_state(n)
        else:
            rho = random_hs_mixed_state(n)
            
        eigs_before = la.eigvalsh(rho)
        m2_before = compute_M2_Sch(eigs_before)
        dstab_before = compute_D_stab_NL(eigs_before)
        
        # Random qubit index
        q = int(rng.integers(n))
        
        # 1. Comp-basis dephasing
        rho_dephase = dephase(rho, q, n)
        m2_dephase = compute_M2_Sch(la.eigvalsh(rho_dephase))
        dstab_dephase = compute_D_stab_NL(la.eigvalsh(rho_dephase))
        
        d_m2_dephase = m2_dephase - m2_before
        d_dstab_dephase = dstab_dephase - dstab_before
        
        if d_m2_dephase > TOL:
            mono_violations["dephase"]["M2_Sch"] += 1
            mono_violations["dephase"]["max_viol_M2"] = max(mono_violations["dephase"]["max_viol_M2"], d_m2_dephase)
        if d_dstab_dephase > TOL:
            mono_violations["dephase"]["D_stab_NL"] += 1
            mono_violations["dephase"]["max_viol_D"] = max(mono_violations["dephase"]["max_viol_D"], d_dstab_dephase)
            
        # 2. Partial trace (discard last qubit)
        rho_trace = ptrace_last(rho, n)
        m2_trace = compute_M2_Sch(la.eigvalsh(rho_trace))
        dstab_trace = compute_D_stab_NL(la.eigvalsh(rho_trace))
        
        d_m2_trace = m2_trace - m2_before
        d_dstab_trace = dstab_trace - dstab_before
        
        if d_m2_trace > TOL:
            mono_violations["ptrace"]["M2_Sch"] += 1
            mono_violations["ptrace"]["max_viol_M2"] = max(mono_violations["ptrace"]["max_viol_M2"], d_m2_trace)
        if d_dstab_trace > TOL:
            mono_violations["ptrace"]["D_stab_NL"] += 1
            mono_violations["ptrace"]["max_viol_D"] = max(mono_violations["ptrace"]["max_viol_D"], d_dstab_trace)
            
        # 3. General Pauli channel
        rho_pauli = pauli_channel_on_qubit(rho, q, n)
        m2_pauli = compute_M2_Sch(la.eigvalsh(rho_pauli))
        dstab_pauli = compute_D_stab_NL(la.eigvalsh(rho_pauli))
        
        d_m2_pauli = m2_pauli - m2_before
        d_dstab_pauli = dstab_pauli - dstab_before
        
        if d_m2_pauli > TOL:
            mono_violations["pauli_ch"]["M2_Sch"] += 1
            mono_violations["pauli_ch"]["max_viol_M2"] = max(mono_violations["pauli_ch"]["max_viol_M2"], d_m2_pauli)
        if d_dstab_pauli > TOL:
            mono_violations["pauli_ch"]["D_stab_NL"] += 1
            mono_violations["pauli_ch"]["max_viol_D"] = max(mono_violations["pauli_ch"]["max_viol_D"], d_dstab_pauli)
            
        # 4. Selective Average
        avg_d_m2 = selective_avg(rho, q, n, compute_M2_Sch)
        avg_d_dstab = selective_avg(rho, q, n, compute_D_stab_NL)
        
        if avg_d_m2 > TOL:
            mono_violations["selective_avg"]["M2_Sch"] += 1
            mono_violations["selective_avg"]["max_viol_M2"] = max(mono_violations["selective_avg"]["max_viol_M2"], avg_d_m2)
        if avg_d_dstab > TOL:
            mono_violations["selective_avg"]["D_stab_NL"] += 1
            mono_violations["selective_avg"]["max_viol_D"] = max(mono_violations["selective_avg"]["max_viol_D"], avg_d_dstab)
            
    # Print results
    print(f"Monotonicity Trials: {num_mono_trials}")
    for op in ops:
        mv = mono_violations[op]
        print(f"\nOperation: {op}")
        print(f"  M2_Sch violations:    {mv['M2_Sch']} (max violation: {mv['max_viol_M2'] if mv['M2_Sch'] > 0 else 'N/A'})")
        print(f"  D_stab_NL violations: {mv['D_stab_NL']} (max violation: {mv['max_viol_D'] if mv['D_stab_NL'] > 0 else 'N/A'})")
        
    # Write results to JSON
    results = {
        "meta": {
            "date": "2026-09-07",
            "session": 43,
            "tol": TOL,
            "seed": 20260907,
            "num_stabilizer_trials": num_stabilizer_trials,
            "num_mono_trials": num_mono_trials
        },
        "faithfulness": {
            "stabilizer_trials": num_stabilizer_trials,
            "m2_sch_violations": faithfulness_errors_m2,
            "dstab_nl_violations": faithfulness_errors_dstab
        },
        "monotonicity": {
            "mono_trials": num_mono_trials,
            "results": {op: {
                "M2_Sch_violations": mv["M2_Sch"],
                "D_stab_NL_violations": mv["D_stab_NL"],
                "max_viol_M2": float(mv["max_viol_M2"]) if mv["M2_Sch"] > 0 else 0.0,
                "max_viol_D": float(mv["max_viol_D"]) if mv["D_stab_NL"] > 0 else 0.0
            } for op, mv in mono_violations.items()}
        }
    }
    
    with open("research/unsolved/unified-field-theory/s43-validate-schmidt-magic-results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults successfully written to s43-validate-schmidt-magic-results.json")

if __name__ == "__main__":
    main()
