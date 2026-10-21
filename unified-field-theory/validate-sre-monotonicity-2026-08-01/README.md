# VALIDATE — Mixed-state linear SRE monotonicity (2026-08-01)

## Problem
Unified Field Theory (UPR problem #6), quantum-information sector (Program D:
information-theoretic / reduced-state Stabilizer Rényi Entropy spacetime order parameter).

## Statement under test
Esposito et al. (arXiv:2606.29443v2): purity-normalized linear Stabilizer Rényi Entropy
`M_lin(ρ) = 1 − Σ_P Tr(ρP)⁴ / Σ_P Tr(ρP)²` (sum over all Pauli strings) is a proper
**mixed-state** non-stabilizerness monotone "with overwhelming probability," with the
violation probability claimed to decay like `exp(−ηN)`.

This program's reduced-state SRE spacetime order parameter (the Sarkar–Biswas bridge
candidate) relies on treating this mixed-state linear SRE as a magic monotone under partial
traces; the session checks whether monotonicity holds at the small-N end, where violations
(if the claim's rarity bound is tight) would be most likely to appear.

## Verdict
**CONFIRMED (no discrepancy found).** 0 violations in 3,000 free-operation trials (600 per
operation class, across N=2–5 qubits; tolerance ΔM > 1e-9). Clifford invariance exact to
machine precision. All tested non-unitary free operations strictly decreased mean magic
(mean ΔM from −0.11 to −0.28), consistent with the paper's qualitative claim.

## Method
- Sanity checks: `M_lin = 0` for `|00⟩` and the maximally mixed state; `M_lin(T⊗T) = 0.4375`;
  exact Clifford invariance — all passed before the main sweep.
- For N = 2–5 qubits, 150 trials per N, alternating rank-2 mixed states (partial trace of a
  Haar-random pure state) and full-rank Hilbert–Schmidt-random density matrices.
- Five free (stabilizer) operations applied per trial: a random 40-gate Clifford circuit,
  computational-basis dephasing of a random qubit, partial trace (discard last qubit), a
  random 4-component Pauli channel, and outcome-averaged computational-basis measurement.
- Script: `scripts/validate-sre-monotonicity-2026-08-01.py`; outputs:
  `outputs/validate-sre-monotonicity-2026-08-01-output.txt` and
  `outputs/validate-sre-monotonicity-2026-08-01-results.json`.

## Limits
- Random sampling, not adversarial search: this bounds the *generic* violation rate at small
  N; it does not exclude measure-zero or deliberately optimized counterexample states, which
  the cited paper's own "with overwhelming probability" phrasing explicitly allows for.
  By the rule of three, 0/600 observed violations per (operation, N) bounds the generic
  violation rate below roughly 0.5% at 95% confidence — consistent with, but not a proof of,
  the paper's exp(−ηN) rarity claim.
- The definition tested is the standard purity-normalized linear SRE; if the cited paper uses
  a different mixed-state normalization, the quantitative decay rate η is not probed here,
  though the qualitative monotone behavior this program's order parameter depends on is what
  was checked.
- This result supports one component (reduced-state SRE as a monotone) of a larger internal
  research program; it is not itself a resolution of a "Unified Field Theory."

## Re-run
Requires Python 3 with `numpy` and `scipy`.

```sh
cd scripts
python3 validate-sre-monotonicity-2026-08-01.py
```

Reproduction performed for this public release (clean clone, Python 3.12.3, numpy 2.4.2,
scipy 1.18.0): **PASS, reproduced exactly** — 0 violations for every (operation, N)
combination, with mean ΔM values matching the original run (e.g. ptrace: −0.270, −0.281,
−0.252, −0.218 for N=2..5).

## Upstream
- Esposito et al., arXiv:2606.29443v2.
- Program context: this program's "research_findings id 4237, Session 38" internal claim
  chain; this validate session is logged internally as Session 39.
