#!/usr/bin/env python3
"""
ATTEMPT session 2026-08-14 — UFT Session 40 (unsolved_problems id=6)

Adversarial search for mixed-state monotonicity violations of the
purity-normalized linear Stabilizer Entropy:

    M_lin(rho) = 1 - sum_P Tr(rho P)^4 / sum_P Tr(rho P)^2   (all 4^N Paulis)

For each non-unitary free operation E (comp-basis dephasing, general Pauli
channel, outcome-averaged selective measurement, partial trace), maximize

    f(rho[, channel params]) = M_lin(E(rho)) - M_lin(rho)

via L-BFGS-B (finite-difference gradients) from many random starts,
rho = A A^dag / Tr(A A^dag), alternating rank-2 and full-rank ansatz.

Also: large random-sampling run to bound the rarity exponent eta in
P(violation) ~ exp(-eta N) (Esposito et al., arXiv:2606.29443v2).

Companion to validate-sre-monotonicity-2026-08-01.py (Session 39).
"""
import numpy as np
import json, sys, time
from scipy.optimize import minimize

rng = np.random.default_rng(20260814)
TOL = 1e-9

# ---------------- section 1: Pauli basis + fast M_lin ----------------
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS1 = [I2, X, Y, Z]

_basis_cache = {}
def pauli_basis(n):
    """Stacked Pauli strings, shape (4^n, 2^n, 2^n)."""
    if n in _basis_cache:
        return _basis_cache[n]
    mats = [np.array([[1]], dtype=complex)]
    for _ in range(n):
        mats = [np.kron(m, p) for m in mats for p in PAULIS1]
    B = np.stack(mats)
    _basis_cache[n] = B
    return B

_flat_cache = {}
def pauli_flat(n):
    """(4^n, 4^n) real-friendly matrix F with c_k = Tr(rho P_k) = F_k . vec(rho^T).
    Since Tr(rho P) = sum_ij rho_ij P_ji = vec(P^T) . vec(rho) elementwise sum,
    we store F[k] = vec(P_k) so c = (F @ vec(rho.T)) -- implemented directly."""
    if n in _flat_cache:
        return _flat_cache[n]
    B = pauli_basis(n)
    d = 2**n
    F = B.transpose(0, 2, 1).reshape(4**n, d * d)  # vec of P^T row-major
    _flat_cache[n] = F
    return F

def m_lin(rho):
    n = int(np.log2(rho.shape[0]))
    F = pauli_flat(n)
    c = (F @ rho.reshape(-1)).real
    s2 = np.sum(c * c)
    s4 = np.sum(c**4)
    return 1.0 - s4 / s2

def m_lin_check(rho):
    """Independent slow recomputation (explicit loop) for verification."""
    n = int(np.log2(rho.shape[0]))
    B = pauli_basis(n)
    s2 = s4 = 0.0
    for P in B:
        c = np.trace(rho @ P).real
        s2 += c**2
        s4 += c**4
    return 1.0 - s4 / s2

# ---------------- section 2: parameterization & free operations ------
def rho_from_x(x, d, r):
    """x: real vector length 2*d*r -> rho = A A^dag / Tr."""
    A = (x[:d * r] + 1j * x[d * r:]).reshape(d, r)
    rho = A @ A.conj().T
    tr = np.trace(rho).real
    return rho / tr

def op_on(qubit, n, gate):
    m = np.array([[1]], dtype=complex)
    for q in range(n):
        m = np.kron(m, gate if q == qubit else I2)
    return m

P0_1 = np.array([[1, 0], [0, 0]], dtype=complex)
P1_1 = np.array([[0, 0], [0, 1]], dtype=complex)

_proj_cache = {}
def projectors(q, n):
    if (q, n) not in _proj_cache:
        _proj_cache[(q, n)] = (op_on(q, n, P0_1), op_on(q, n, P1_1))
    return _proj_cache[(q, n)]

def dephase(rho, q, n):
    P0, P1 = projectors(q, n)
    return P0 @ rho @ P0 + P1 @ rho @ P1

def ptrace_last(rho, n):
    r = rho.reshape(2**(n - 1), 2, 2**(n - 1), 2)
    return np.trace(r, axis1=1, axis2=3)

def pauli_channel_soft(rho, n, logits):
    """General Pauli channel with softmax(logits) weights over all 4^n Paulis."""
    B = pauli_basis(n)
    w = np.exp(logits - logits.max())
    w /= w.sum()
    out = np.zeros_like(rho)
    for wi, P in zip(w, B):
        if wi > 1e-14:
            out += wi * (P @ rho @ P)
    return out

def selective_avg_delta(rho, q, n, mfun=m_lin):
    """sum_i p_i M(rho_i) - M(rho) for comp-basis measurement on qubit q."""
    P0, P1 = projectors(q, n)
    m0 = mfun(rho)
    acc = 0.0
    for P in (P0, P1):
        s = P @ rho @ P
        p = np.trace(s).real
        if p > 1e-12:
            acc += p * mfun(s / p)
    return acc - m0

# ---------------- section 3: adversarial optimizer -------------------
def make_objective(op, n, q, r):
    """Return (neg_objective(x), nparams, f_of_x(x)) for the given free op."""
    d = 2**n
    ns = 2 * d * r  # state params
    if op == "pauli_ch":
        npar = ns + 4**n
    else:
        npar = ns

    def f(x):
        rho = rho_from_x(x[:ns], d, r)
        if op == "dephase":
            return m_lin(dephase(rho, q, n)) - m_lin(rho)
        elif op == "ptrace":
            return m_lin(ptrace_last(rho, n)) - m_lin(rho)
        elif op == "pauli_ch":
            return m_lin(pauli_channel_soft(rho, n, x[ns:])) - m_lin(rho)
        elif op == "selective_avg":
            return selective_avg_delta(rho, q, n)
        raise ValueError(op)

    return (lambda x: -f(x)), npar, f

def adversarial_search(n, ops, restarts=50, maxiter=150, verbose=True):
    """Maximize violation objective per op. Returns per-op best record."""
    d = 2**n
    results = {}
    for op in ops:
        best = {"f": -np.inf, "x": None, "q": None, "r": None}
        t0 = time.time()
        for k in range(restarts):
            r = 2 if k % 2 == 0 else d          # alternate rank-2 / full rank
            q = k % n                            # cycle measured/dephased qubit
            negf, npar, fx = make_objective(op, n, q, r)
            x0 = rng.normal(size=npar) * 0.7
            try:
                res = minimize(negf, x0, method="L-BFGS-B",
                               options={"maxiter": maxiter, "eps": 1e-7})
                val = -res.fun
                xbest = res.x
            except Exception as e:
                print(f"  [{op} N={n} restart {k}] optimizer error: {e}")
                continue
            if val > best["f"]:
                best = {"f": float(val), "x": xbest.copy(), "q": q, "r": r}
        best["seconds"] = round(time.time() - t0, 1)
        results[op] = best
        if verbose:
            print(f"N={n} {op:14s} max f = {best['f']:+.3e}  "
                  f"(q={best['q']}, rank={best['r']}, {best['seconds']}s)",
                  flush=True)
    return results

def verify_candidate(op, n, best):
    """Independent recomputation of the best objective with the slow m_lin."""
    d = 2**n
    r = best["r"]; q = best["q"]; x = best["x"]
    ns = 2 * d * r
    rho = rho_from_x(x[:ns], d, r)
    if op == "dephase":
        f = m_lin_check(dephase(rho, q, n)) - m_lin_check(rho)
    elif op == "ptrace":
        f = m_lin_check(ptrace_last(rho, n)) - m_lin_check(rho)
    elif op == "pauli_ch":
        f = m_lin_check(pauli_channel_soft(rho, n, x[ns:])) - m_lin_check(rho)
    elif op == "selective_avg":
        f = selective_avg_delta(rho, q, n, mfun=m_lin_check)
    return float(f), rho

# ---------------- section 4: random-sampling rarity bound ------------
def haar_pure(n):
    d = 2**n
    v = rng.normal(size=d) + 1j * rng.normal(size=d)
    return v / np.linalg.norm(v)

def rank2_mixed(n):
    v = haar_pure(n + 1).reshape(2**n, 2)
    return v @ v.conj().T

def hs_random(n):
    d = 2**n
    G = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    rho = G @ G.conj().T
    return rho / np.trace(rho).real

def random_pauli_channel(rho, n, k=4):
    B = pauli_basis(n)
    idx = rng.choice(len(B), size=k, replace=False)
    p = rng.dirichlet(np.ones(k))
    out = np.zeros_like(rho)
    for w, i in zip(p, idx):
        out += w * (B[i] @ rho @ B[i])
    return out

def sampling_bound(n, samples):
    """Count violations over `samples` random states x 4 free ops."""
    stats = {op: {"violations": 0, "max_delta": -np.inf}
             for op in ("dephase", "ptrace", "pauli_ch", "selective_avg")}
    for i in range(samples):
        rho = rank2_mixed(n) if i % 2 == 0 else hs_random(n)
        m0 = m_lin(rho)
        q = int(rng.integers(n))
        deltas = {
            "dephase": m_lin(dephase(rho, q, n)) - m0,
            "ptrace": m_lin(ptrace_last(rho, n)) - m0,
            "pauli_ch": m_lin(random_pauli_channel(rho, n)) - m0,
            "selective_avg": selective_avg_delta(rho, q, n),
        }
        for op, dlt in deltas.items():
            st = stats[op]
            st["max_delta"] = max(st["max_delta"], dlt)
            if dlt > TOL:
                st["violations"] += 1
    for op in stats:
        st = stats[op]
        st["samples"] = samples
        st["rate"] = st["violations"] / samples
        st["rate_95_upper"] = (3.0 / samples if st["violations"] == 0
                               else None)  # rule of three
    return stats

# ---------------- section 5: main driver -----------------------------
def sanity():
    assert abs(m_lin(np.eye(4) / 4)) < 1e-12
    zz = np.zeros((4, 4), dtype=complex); zz[0, 0] = 1
    assert abs(m_lin(zz)) < 1e-12
    t = np.array([1, np.exp(1j * np.pi / 4)], dtype=complex) / np.sqrt(2)
    tt = np.outer(t, t.conj())
    mt = m_lin(np.kron(tt, tt))
    assert abs(mt - 0.4375) < 1e-9, mt
    # Clifford invariance spot check (fast/slow agreement too)
    rho = hs_random(2)
    assert abs(m_lin(rho) - m_lin_check(rho)) < 1e-12
    print(f"sanity OK (M_lin(T(x)T) = {mt:.6f})", flush=True)

def main():
    sanity()
    out = {"meta": {"date": "2026-08-14", "session": 40, "tol": TOL,
                    "seed": 20260814,
                    "restarts_per_op": 50, "maxiter": 150}}
    ops = ["dephase", "ptrace", "pauli_ch", "selective_avg"]

    # --- adversarial search ---
    out["adversarial"] = {}
    for n in (2, 3):
        res = adversarial_search(n, ops, restarts=50, maxiter=150)
        rec = {}
        for op, best in res.items():
            vf, rho = verify_candidate(op, n, best)
            entry = {"max_f": best["f"], "verified_f": vf,
                     "qubit": best["q"], "rank": best["r"],
                     "seconds": best["seconds"],
                     "violation": bool(vf > TOL)}
            if vf > TOL:
                entry["rho_real"] = rho.real.tolist()
                entry["rho_imag"] = rho.imag.tolist()
                ns = 2 * (2**n) * best["r"]
                if op == "pauli_ch":
                    entry["channel_logits"] = best["x"][ns:].tolist()
                print(f"*** COUNTEREXAMPLE N={n} {op}: f={vf:.3e} ***",
                      flush=True)
            rec[op] = entry
        out["adversarial"][str(n)] = rec
        _dump(out)

    # --- random-sampling rarity bounds ---
    out["sampling"] = {}
    for n, samples in ((2, 20000), (3, 8000)):
        t0 = time.time()
        st = sampling_bound(n, samples)
        for op in st:
            st[op]["max_delta"] = float(st[op]["max_delta"])
        out["sampling"][str(n)] = st
        print(f"sampling N={n}: {samples} states done "
              f"({time.time()-t0:.0f}s)", flush=True)
        _dump(out)

    # --- eta estimate/bound ---
    out["eta"] = eta_report(out)
    _dump(out)
    print(json.dumps(out["eta"], indent=2))

def eta_report(out):
    """Estimate eta if violations found; otherwise produce bounds."""
    rep = {}
    any_viol = False
    rates = {}
    for n in ("2", "3"):
        for op, st in out["sampling"][n].items():
            if st["violations"] > 0:
                any_viol = True
                rates.setdefault(op, {})[n] = st["rate"]
    adv_viol = any(e["violation"]
                   for n in out["adversarial"].values() for e in n.values())
    rep["adversarial_counterexample_found"] = adv_viol
    rep["random_sampling_violations_found"] = any_viol
    if any_viol:
        # eta from rate ratio where both N have nonzero rates
        est = {}
        for op, r in rates.items():
            if "2" in r and "3" in r and r["3"] > 0:
                est[op] = float(np.log(r["2"] / r["3"]))
        rep["eta_estimates_from_rates"] = est
    else:
        # zero-count bounds: rate_N < 3/M at 95% => if rate = C exp(-eta N)
        # with C <= 1, then eta > -ln(3/M)/N
        bounds = {}
        for n_str, samples in (("2", out["sampling"]["2"]["dephase"]["samples"]),
                               ("3", out["sampling"]["3"]["dephase"]["samples"])):
            nn = int(n_str)
            bounds[n_str] = {"rate_upper_95": 3.0 / samples,
                             "eta_lower_if_C_le_1": float(-np.log(3.0 / samples) / nn)}
        rep["zero_count_bounds"] = bounds
        rep["note"] = ("No violations found; eta cannot be point-estimated. "
                       "Bounds assume rate(N) = C*exp(-eta*N) with C<=1.")
    return rep

def _dump(out):
    with open(__file__.replace(".py", "-results.json"), "w") as f:
        def clean(o):
            if isinstance(o, dict):
                return {k: clean(v) for k, v in o.items() if k != "x"}
            if isinstance(o, np.ndarray):
                return o.tolist()
            if isinstance(o, (np.floating, np.integer)):
                return o.item()
            return o
        json.dump(clean(out), f, indent=2)

if __name__ == "__main__":
    main()
