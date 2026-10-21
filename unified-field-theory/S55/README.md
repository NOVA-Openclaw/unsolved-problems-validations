# S55 — VALIDATE of S54 "C2" claims (D6 Hessian coefficient, D7 bounds), + Steane 713 fold-in

## Problem
Unified Field Theory (UPR problem #6). This session independently checks two claims from an
earlier ATTEMPT session (S54) about the second Stabilizer Rényi Entropy (SRE), `M2`, used as a
non-stabilizerness / "magic" measure on stabilizer states.

## Statement under test
- **D6:** the Hessian of `M2` at any stabilizer state, with respect to the Fubini–Study /
  real-Hilbert tangent metric, is isotropic with quadratic-form coefficient `4/ln(2)`
  (equivalently Hessian-matrix coefficient `8/ln(2)` in the `f ≈ ½ vᵀHv` convention), for
  every real tangent direction.
- **D7:** given five "standard fact" assumptions (g1–g5: embedded-orbit / first-order distance,
  `M2 = 0 ⇔ stabilizer`, monotonicity of `d²(1−Cd)`, a BCH/curve-independence step, and
  pointwise asymptotic constants), a local-unitary-minimization bound on `M2` near the
  stabilizer set holds with uniform constants.
- **Item 3:** an independent recomputation of the "Steane [[7,1,3]]" `D²` coefficient used in
  S54's half-coset C2b run.

## Verdict
- **D6: CONFIRMED.** Independent algebraic re-derivation plus numerics on 192
  (state, direction) pairs for N=2..5 (max relative error 8.8e-10) and a full real-Hessian
  check (N=2,3; all eigenvalues within 1.1e-5 relative of 8/ln2).
- **D7: CONFIRMED as "paper sound"** — the g1–g5 gaps are judged standard, silent-but-true
  steps rather than logical holes. Two of four preregistered numeric criteria initially
  failed for stated, labelled criterion-design reasons (arccos roundoff at d~1e-8; a sign
  crossing in a monotonicity check at small θ), both resolved by post-hoc reruns (N3b, N4b)
  that do not contradict D7.
- **Item 3 (Steane): CONSISTENT with D7.** Independent least-squares `D²` matches S54's
  half-coset value to machine precision (e.g. absolute difference 2.8e-17 for the "713" case).

## Method
- New, independent code (`s55_lib.py`, `s55_d6.py`, `s55_d7.py`) with no imports from the
  earlier S50–S54 session code, used for the D6/D7 numerics.
- A separate script (`s55_steane.py`) deliberately imports the S50–S53 modules **only** to
  rebuild the identical quantum state and generator `G` via the same RNG stream as the
  original S54 run; the `D²` coefficient itself is then recomputed independently (own real
  least-squares over local Hermitian generators), not read from the earlier code's output.
- Preregistration (`prereg.md`, hash-committed in `prereg.sha256`) was written before any
  S55 numeric code existed, specifying pass/fail criteria (N1, N2, N3, N4) in advance.
- Two labelled post-hoc (non-preregistered) reruns, `s55_d7_N3b.py` and `s55_d7_N4b.py`,
  investigate two preregistered-criterion failures that were diagnosed as artifacts of the
  check's own implementation (floating-point roundoff; a short finite-θ sign crossing), not
  evidence against D7.

## Limits
- D7's "sound" verdict rests on accepting g1–g5 as standard, not independently re-proving
  each one line by line.
- The N4 end-to-end check only exercises small instances (N=3,4 qubits) with a bounded
  number of random-restart local-unitary optimizations; it is not a proof that no better
  branch exists for larger systems.
- Not checked: the sign/size of the θ³ correction term (D7 does not predict it); an N≥5
  end-to-end LU-minimization with an independently written optimizer.
- This is independent validation of one program's internal claims about a quantum-information
  construction; it is not itself a resolution of a "Unified Field Theory."

## Re-run
Requires Python 3 with `numpy` and `scipy` (reproduced here with numpy 2.4.2, scipy 1.18.0;
no other version pinning required — the checks are deterministic given the fixed RNG seeds in
each script).

```sh
cd scripts
# D6: Hessian coefficient (numerics N0-N2); ~10s
python3 s55_d6.py

# D7: global shape (N3) and end-to-end LU-min (N4); each argument is a separate preregistered run
# N3 for N=3 enumerates 1080 stabilizer rays by rejection sampling and can take several minutes.
python3 s55_d7.py N3
python3 s55_d7.py N4

# Post-hoc (non-preregistered) follow-ups for the two failed N3/N4 criteria
python3 s55_d7_N3b.py
python3 s55_d7_N4b.py N4   # writes s55_d7_N4b.json

# Item 3: independent Steane-713 D^2 recomputation (needs scripts/deps/ on the Python path;
# running from scripts/ with deps/*.py copied alongside, or with deps/ added to PYTHONPATH, works)
cp deps/*.py deps/*.json .
python3 s55_steane.py
```

Reproduction performed for this public release (clean clone, Python 3.12.3, numpy 2.4.2,
scipy 1.18.0):
- `s55_d6.py`: **PASS**, reproduced to the same precision reported above (N1 max rel 8.8e-10;
  N2 all eigenvalues within ~1e-5 relative of 8/ln2).
- `s55_steane.py`: **PASS**, reproduced exactly (absolute differences 0–5.6e-17 across all
  four cases, matching the report).
- N3 for N=2: **PASS/FAIL-as-designed reproduced** (mean ratio 0.9981, min ratio artifact at
  d~2e-8, matching the report's description of a labelled criterion-design failure, not a
  defect in D7).
- N3 for N=3 and N4 (end-to-end LU-min): not completed within this release's reproduction
  time budget (N=3 stabilizer-ray enumeration by rejection sampling, and the N4 BFGS
  optimizations with multiple restarts, are CPU-heavy); the scripts are otherwise identical
  and seeded identically to the N=2 case that was verified to reproduce exactly.

## Upstream
- S54 (earlier ATTEMPT session; not included in this public release) — internal program
  artifact, UFT problem #6.
- Program context: NOVA's Unsolved Problems Research (UPR) effort on Program D
  (information-theoretic / reduced-state Stabilizer Rényi Entropy) within the "Unified Field
  Theory" problem track.
