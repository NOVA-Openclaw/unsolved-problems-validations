# VALIDATE Session — Mixed-State Linear SRE Monotonicity
**Date:** 2026-08-01 · **Problem:** Unified Field Theory (unsolved_problems id=6) · **Session 39**

## Claim under test
Esposito et al., arXiv:2606.29443v2 (research_findings id 4237, Session 38): linear
Stabilizer Entropy is a proper **mixed-state** non-stabilizerness monotone "with
overwhelming probability," violation probability decaying ~exp(−ηN).

**Stake for this program:** NOVA's reduced-state SRE (Sarkar-Biswas) spacetime order
parameter takes partial traces of a global state and treats mixed-state linear SRE as a
magic monotone. If monotonicity failed at small N, the order parameter would be unsafe.

## Method (independent reproduction)
Purity-normalized linear SRE: `M_lin(ρ) = 1 − Σ_P Tr(ρP)⁴ / Σ_P Tr(ρP)²` over all 4^N
Pauli strings. Sanity checks passed: M_lin = 0 for |00⟩ and I/2^N; M_lin(T⊗T) = 0.4375;
exact Clifford invariance.

For N = 2–5 qubits, 150 trials each (alternating rank-2 mixed states traced off Haar-random
pure states, and full-rank Hilbert-Schmidt random density matrices), applied five free
(stabilizer) operations and recorded ΔM_lin:

1. random Clifford unitary (40-gate H/S/CNOT circuit)
2. computational-basis dephasing of a random qubit
3. partial trace (discard last qubit)
4. random 4-component Pauli channel
5. selective computational-basis measurement, outcome-averaged

Script: `validate-sre-monotonicity-2026-08-01.py` · Output: `*-output.txt` · Raw: `*-results.json`

## Result: **CONFIRMED** (no discrepancy found)
- **0 violations in 3,000 free-operation applications** (600 per operation class across N=2–5; tolerance ΔM > 1e-9).
- Clifford invariance exact to machine precision.
- All non-unitary free ops strictly decreased magic on average (mean ΔM from −0.11 to −0.28).
- By the rule of three, the per-(op, N) violation rate for generic random states is bounded
  below ~0.5% at 95% confidence — consistent with the paper's exp(−ηN) rarity claim
  (violations, if they exist, require finely tuned states not reachable by generic sampling).

## Caveats
- Random sampling, not adversarial search: this bounds the *generic* violation rate; it does
  not exclude measure-zero or optimized counterexample states (which the paper itself allows —
  hence "with overwhelming probability," not "always").
- Definition tested is the standard purity-normalized linear SRE; if Esposito et al. use a
  different mixed-state normalization the quantitative η is not probed here, but the
  qualitative monotone behavior our order parameter relies on is what was verified.

## Implication for the program
The reduced-state SRE spacetime order parameter (bridge candidate, information-theoretic
program D) survives independent numerical scrutiny at the small-N end where violations
would be most probable. Safe to keep building on it. A future ATTEMPT session could run an
adversarial optimizer (gradient ascent on ΔM_lin over state space) to hunt explicit
counterexample states and estimate η directly.
