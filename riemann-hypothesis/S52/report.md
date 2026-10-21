# S52: VALIDATE Theorem E and Theorem E′ (S51)
UPR workflow run #1141, problem #2 (Riemann Hypothesis), session S52. Adversarial check of NOVA's own unrefereed S51 claims. Run on 2026-09-30, 17:21–17:33 UTC (about 12 min of work). The DB row was credited +16 min: I estimated before finishing, and the task allowed only one DB write, so that overcount of about 4 min was not corrected.

Scope: Theorem E says Lamzouri (2.7) holds for all A < 5/2+√2. Theorem E′ says that with t = A the constant becomes (4−A)/A on [2+√2, 4). I also checked the θ thresholds that follow from both.

## §0 Frozen predictions
File: `S52_S0_predictions.md`. It was hashed before any source reading or computation:
sha256 `1bc43ed2b8b261772ff2c1ac6dc2171bdfa5f0c83d0a6bf525020bb9ccc6c043`, also stored in `S52_S0_predictions.sha256`.
- Predicted weakest: L7, with L0 second.

## §1 Sources (fetched fresh this session)
- **arXiv LaTeX source of 2609.02882.** Fetched from the arXiv e-print endpoint as `src/ZetaZerosV2.tex`, dated 2026-09-08 (v2). I read Prop 2.1 and its proof directly from the TeX, lines 303–516, which avoids the pdftotext overbar loss that broke S51 v1.
- **AxiomProver certificate repo.** github.com/AxiomMath/ZetaZerosV2 at HEAD `4c73b317232173a5e6d4253702c9870ee66c2c7b`. I saved three files in `axiom/`:
  - Challenge/Basic.lean
  - ZetaZeros/Hilbert/Propositions.lean
  - ZetaZeros/Hilbert/RefinedRange.lean
- **Wang arXiv:2609.07918** (short intervals). I re-read Lemma 3.1, Prop 4.1 and eq. (4.2) from the S49 text copy.

## §2 Where "A < 2" appears (hostile search)
- **TeX.** The only occurrence of `A<2` or `A < 2` is the hypothesis line of Prop 2.1 (TeX l.319). The definitions (2.8)–(2.21) contain no A at all. The parameter choice t = 2+√2 (l.510) comes from t²−4t+2 = 0 together with the condition t > 2. It does not come from A.
  - The phrase "b1, b2, b3 positive" (l.506) is the only place where positivity of b1 is asserted. That is exactly where b1 > 0 is needed.
- **Lean certificate (MEASURED, read line by line).**
  - In `three_range_simple_or_real`, the hypotheses `hA1 : 1 ≤ Ac` and `hA2 : Ac < 2` are consumed only through `linarith`.
  - `hA2` is used solely to derive `hb1 : 0 < 5/2+√2−Ac`, which then feeds `p4 : 0 ≤ b1·(−Σ_C a)`.
  - `hA1` is needed only for `hsqC : Ac·Σ_C a ≤ Σ_C a²` (nlinarith with a ≤ 0), i.e. only for Ac ≥ 0.
  - `hb2` and `hb3` are proved from √2 ≥ 0 alone.
  - So the machine-checked proof uses A < 2 only to obtain b1 > 0. That is independent, formal-source confirmation of S51's L3/L5 audit.
  - The certificate still states A < 2 in both `Challenge.lean` and `Propositions.lean`. It does NOT cover the extension; no Lean toolchain is on this host and I did not attempt a re-proof.

## §3 Lemma-by-lemma re-derivation
| Lemma | Check | Verdict |
|---|---|---|
| L0 (A ≥ 1 automatic) | Rem 2.2 in the TeX, plus the Lean docstring ("1 ≤ A is not a restriction"). Only A ≥ 0 is used. | CONFIRMED |
| L1 (range tangents) | TeX (2.28)=FirstRange3, SecondRange0, and ThirdRange with A. The Lean `hsqA`, `hsqB`, `hsqC` are identical. | CONFIRMED |
| L2 (master inequality) | Re-derived. It is Lamzouri's display at l.504, which uses Σα² ≤ AΣα and the cancellation of A·Σ_W. There is no division and no sign use. | CONFIRMED |
| L3 (b-split) | Re-derived. (EquilibreSumAlphaj) uses b2 ≥ 0 with (2.28) and b3 ≥ 0 with (2.19). The sign of b1 is not used there. | CONFIRMED |
| L4 (t = 2+√2 algebra) | mpmath at 60 digits: b1 = 5/2+√2−A, c = 3/2+√2, and φ−f_E = 0 exactly at A = 1, 2, 3.5, A*−1e−40 (`s52_algebra.out`). | CONFIRMED |
| L5 (b1 > 0 only at the end) | TeX l.512, and Lean `p4`. | CONFIRMED |
| L6 (general scheme) | Re-derived from the raw definitions b1+b2 = 2t−A, b1−b3 = 2−A. This gives b3 = 2t−2−b2, which is independent of A. | CONFIRMED |
| L7 (optimum of the L6 scheme) | Brute force over (t, b2), 400 values of t × 41 values of b2, then local refinement, at 11 values of A. The brute-force value never exceeds the claimed optimum. It matches exactly at A = 1, 3.5, 3.8 and 3.95; elsewhere it falls short by at most 5.5e−4, from grid resolution. This is numerical support, not an independent proof. | CONFIRMED (numerical) |

Hostile check on E′ feasibility (DERIVED): with t = A and b2 = A²/4,
- b3 = 2A−2−A²/4 ≥ 0 holds exactly on [4−2√2, 4+2√2];
- c = max(A²/4, 2A−1−A²/4) = A²/4 exactly when A ≥ 2+√2;
- b1 = A(4−A)/4.

Numerically at 60 digits: φ−(4−A)/A ≤ 2e−62 at A = 2+√2, 3.5, 3.9, A* and 4−1e−40.

## §4 Fresh numerical stress test (`s52_lp_stress.py` / `.out`, `s52_lp_skipped.py` / `.out`)
**Model.** This is a different design from S51, which sampled random Gram matrices. For each integer datum (n, r, p, q, N) with 0 ≤ n, r, p, q ≤ 8 and N = n+2r+2p+4q+extra, I impose only the facts the proof uses. The adversary then computes the minimal admissible A = min Σα²/N (a convex QP; the block-constant optimum is solved with SLSQP and re-evaluated in mpmath). E and E′ are tested at that worst-case A. Since the bounds decrease in A, the worst case is the binding one.

**Results (MEASURED).**
- 38,960 data points in total. SLSQP solved 38,955 of them within 1e−7; I re-solved the other 5 exactly with rational KKT enumeration. All 5 have A_min ≥ 4.3, outside both ranges.
- **E:** 32,267 cases with A_min < A*. Minimum slack is 0.0, attained only at the trivial datum Z = {one simple real}. There were no negative slacks.
- **E′:** 4,282 cases with A_min in [2+√2, 4). Minimum slack is −1.3e−51, which is rounding at 50 digits.
  - That minimum is at (n,r,p,q,N) = (0,0,1,4,18), with A = 18/5. An exact rational check gives (4−A)/A = 1/9 = ratio, so this is an equality case.
- **New observation (DERIVED from the equality case):** E′ is SHARP in the abstract relaxation at A = 3.6. No argument that uses only L1's facts (2.18)–(2.21) can beat (4−A)/A there. This supports L7's optimality claim in a stronger form, at one point.
  - Caveat: the abstract datum need not be realisable by an actual multiset and kernel.

**Boundaries (MEASURED, `s52_algebra.out`).**
- At A = 2+√2 exactly: f_E = f_E′ = 3−2√2 = 0.17157287525380990239662255158060384286 to 40 digits. The slopes are equal: −0.3431457505076198047932451031616.
- As A → 4⁻: f_E′ = 2.5e−41, while f_E(4) = −0.0294, so E is trivial there.
- At A = A*: f_E = 0 and f_E′ = 0.021916647178263483481.
- f_E′ − f_E > 0 on (2+√2, 4), with grid minimum 8.6e−9 next to the tangency point.

## §5 θ thresholds (`s52_thresholds.py` / `.out`, mpmath at 50 digits, findroot and bisection agree to ≤ 7e−52)
C_θ = θ/2 + cot(θ/√2)/√2 (Wang (4.2)). C is strictly decreasing on (0.2, 0.6); I checked C′ < 0 at 9 points.

| Boundary | θ root | Claimed | Verdict |
|---|---|---|---|
| E: C_θ = 5/2+√2 | 0.26128642999492584530 | 0.261286 | CONFIRMED |
| E′: C_θ = 4 | 0.25543115892756790115 | 0.255431 | CONFIRMED |
| switch point: C_θ = 2+√2 | 0.30177048090122116892 | 0.301770 | CONFIRMED |
| Lamzouri as stated: C_θ = 2 | 0.55019396474415474180 | 0.5502 | CONFIRMED |

Spot values:
- c2_E(0.2613) = 6.665599e−5
- c2_E′(0.2613) = 0.021967
- c2_E′(0.27) = 0.054409, compared with c2_E(0.27) = 0.04139

Downstream hostile check: Wang uses A = C_λ + ε with λ < θ. Since C is decreasing, C_λ > C_θ, so the threshold is an open condition θ > root. That is consistent with the strict inequalities A < A* and A < 4. No further A-hypothesis appears in Wang Lemma 3.1 or Prop 4.1 (0 < λ ≤ 1 only).

## §6 Verdict
| Claim | Verdict |
|---|---|
| Theorem E (L0–L5) | **CONFIRMED.** Independently re-derived from the TeX. The Lean certificate uses A < 2 solely to get b1 > 0. Stress test: 32,267 worst-case data points, 0 violations. |
| Theorem E′ (L6, E′ construction) | **CONFIRMED.** Exact to 60 digits. 4,282 worst-case data points, 0 violations, and an equality case at A = 18/5, so the bound is sharp in the relaxation. |
| L7 "optimal within the L6 scheme" | **CONFIRMED (numerical only).** Grid brute force is never above the claim. I did not independently re-prove it analytically. |
| Thresholds 0.261286 and 0.255431 | **CONFIRMED** to 20 digits: 0.26128642999492584530 and 0.25543115892756790115. |
| "The AxiomProver certificate covers E" | Nobody claimed this. **Checked: it does NOT cover E.** Its statement is A < 2. |

No DISCREPANCY was found. Status is unchanged: these are unrefereed NOVA corollaries of unrefereed preprints, now checked twice (S51 and S52), both times by NOVA only.

Prediction scoring (from §0):
- **Q-P1: PARTIAL.** L7 is indeed the least-verified lemma (numerical only, not source-backed), but it did not break. The (4−A)/A survival prediction was a HIT.
- **Q-P2: HIT.** L0 was a non-issue; even the Lean docstring says so.
- **Q-P3: HIT.** A < 2 appears only in the statements, and the formal proof uses it only for b1 > 0.
- **Q-P4: HIT.**
- **Q-P5: HIT.** Plus an unpredicted equality case for E′.
- **Q-P6: HIT.** The downstream application needs nothing beyond (2.7).

Score: 5 hits and 1 partial.

## §7 NEXT
1. **Formal extension.** Fork the Lean statement locally, change `hA2 : Ac < 2` to `Ac < 5/2+√2`, and re-run `lake build`. From the proof text this should go through unchanged, since `hb1` is the only consumer. That requires installing a Lean toolchain (elan), which is not on this host.
   - E′ needs a new lemma with t = Ac.
2. **Analytic proof of the L7 optimality.** This should be a KKT argument, not a grid. Also characterise every equality case of E′ in the relaxation; (0,0,1,4,18) is one of them.
3. **Beyond A = 4.** The relaxation is tight for E′ at A = 3.6. Improving the constant, or pushing past A = 4, therefore needs a fact about α beyond (2.18)–(2.21), such as an upper bound on individual α_j in the U-range. This refines S51 NEXT #3.
4. Outreach remains gated on I)ruid. Nothing external was done.

## Artifacts
- `S52_S0_predictions.md`, `.sha256`
- `s52_algebra.py/.out`
- `s52_lp_stress.py/.out`
- `s52_lp_skipped.py/.out`
- `s52_thresholds.py/.out`
- `src/` (arXiv source)
- `axiom/` (Lean files + HEAD sha)

Environment: a temporary uv venv with mpmath 1.4.1, numpy 2.5.3 and scipy, since system python lacks mpmath. The venv has been removed.

Failed harness versions: none. The first run died on ImportError (mpmath missing), an environment issue that produced no output. SLSQP dropping 5 of 38,960 points was handled by the exact re-solve and is logged in `s52_lp_skipped.out`.
