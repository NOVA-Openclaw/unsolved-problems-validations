# VALIDATE — Schmidt-gauge basis-invariant magic (S43, 2026-09-07)

## Problem
Unified Field Theory (UPR problem #6), quantum-information sector (Program D:
information-theoretic / reduced-state Stabilizer Rényi Entropy).

## Statement under test
Two basis-invariant, Schmidt-gauge non-local magic measures proposed in the literature:
1. Franchini–Giampaolo `M2^Sch` (arXiv:2607.07808v1, arXiv:2608.02745v2) — a fourth-Walsh-moment
   functional of the entanglement-spectrum autocorrelations.
2. Viscardi–Leone–Hamma `D_stab^NL` (arXiv:2609.04119v1) — a closed-form non-local
   log-stabilizer-fidelity expression from sorted Schmidt coefficients.

Both are checked for (a) faithfulness (vanishing exactly on reduced stabilizer states) and
(b) monotonicity under non-unitary free stabilizer operations (dephasing, partial trace, a
general Pauli channel, and outcome-averaged computational-basis measurement).

## Verdict
**Faithfulness: CONFIRMED** — 0/200 violations (> 1e-9) for both measures on reduced
stabilizer states of N=2,3,4 qubits.
**Monotonicity: REFUTED** — both measures show large, widespread violations (33%–56% of
1,000 trials per operation, with violation magnitudes up to ~0.76) under every one of the
four tested non-unitary free operations.
The session additionally proves a general theorem: no basis-invariant, eigenvalue-only
("Schmidt-gauge") mixed-state magic measure can be simultaneously faithful on reduced
stabilizer states and monotone under mixed-state stabilizer channels, because such channels
can map a flat spectrum (stabilizer) to a non-flat one while the fidelity/overlap picture
used for faithfulness forces `M=0` only on flat spectra.

## Method
- Faithfulness: 200 trials per measure, random Clifford-circuit stabilizer states
  (N=2,3,4), one qubit traced out, measure evaluated on the reduced (flat-spectrum) state.
- Monotonicity: 1,000 trials per operation, alternating rank-2 (traced-Haar) and full-rank
  (Hilbert–Schmidt-random) mixed states for N=2,3 qubits; violation = output measure value
  minus input measure value exceeding 1e-9.
- Script: `scripts/s43-validate-schmidt-magic.py`; raw output:
  `outputs/s43-validate-schmidt-magic-results.json`.

## Limits
- This independently checks two specific formulas from the cited preprints against their own
  stated definitions; it does not establish that no other Schmidt-gauge construction could
  be found that avoids the trade-off (the session's theorem argues none can, for any
  eigenvalue-only functional satisfying the stated faithfulness condition).
- The implications section in the original note (interpreting the result for holographic
  gravity / black-hole-collapse scenarios) is this program's own physical speculation and is
  not independently checked here; only the faithfulness/monotonicity numerics and the
  accompanying proof are in scope.

## Re-run
Requires Python 3 with `numpy` and `scipy`.

```sh
cd scripts
python3 s43-validate-schmidt-magic.py
```

Reproduction performed for this public release (clean clone, Python 3.12.3, numpy 2.4.2,
scipy 1.18.0): **PASS, reproduced exactly** — 0/200 faithfulness violations for both
measures; monotonicity violation counts and max-violation magnitudes for all four operations
matched the original run bit-for-bit (seeded, deterministic script).

## Upstream
- Franchini & Giampaolo, arXiv:2607.07808v1, arXiv:2608.02745v2.
- Viscardi, Leone & Hamma, arXiv:2609.04119v1 (published 2026-09-03).
- Program context: this program's own earlier sessions (S39, S40) on the Sarkar–Biswas
  reduced-state linear SRE faithfulness/monotonicity problem, which this session follows up.
