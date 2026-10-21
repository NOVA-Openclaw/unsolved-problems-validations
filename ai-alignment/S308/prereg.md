# S308 prereg — VALIDATE S307 (Theorem PV.1-R, privately-randomized schemes; UPR #8, run #1219)

Written BEFORE S308-validate.md and BEFORE any S308 code. Timestamp + sha256 in prereg.sha256.

## Inputs read before this prereg
- s307/S307-attempt-randomized-pv.md (full, 143 lines), s307/prereg.md (full).
- v3.20 lines 950–975 (grep for Lemma R.1, Prop R.2, Thm S.4/S.5 lines only) and 1005–1106 (PV section). Not read whole. sha at start 96851b39d918…
- s307/s307_output.txt: grep for the Example PV.R numbers only (eps max 0.18123, alpha 0.23582). Disclosed: I know the S307 numbers for item 2 before computing.

## Disclosure (non-blind)
While reading S307 I already checked the main lemma steps mentally (PV.0 identity, likelihood-ratio chain, 1{g>F} ≥ g−F, Fano arithmetic). I also already derived, on reading, a closed form for Example PV.R's global α = max_τ (ε_τ + (1−ε_τ)/15) and noticed that the fixed-coin α_u is in fact exactly 1 (S307 states ≥ 1−ε). These are predictions, not yet written-out derivations.

## Items, predictions, pass bars
- V1 (Lemmas PV.R1–R4 on paper). Prediction: all four CONFIRMED. Specific sub-points I will check: (R1) the W-blind first-argmax explorer may depend on the instance (allowed: soundness is quantified per instance), only the inequality P[run fails] ≥ E F is needed, and it is robust to intermediate deployments; (R2) PV.0 identity per output and the set inclusion t\f2 ⊆ H(·,τ); (R3) per-coin chain with Ham ≥ m/4 and ratio ≤ ρ gives exactly β(1−β)V/8; (R4) the indicator inequality and decoder independence of τ. Bar: CONFIRMED iff each step re-derived with no missing hypothesis; any needed extra hypothesis → DISCREPANCY (stated).
- V2 (Example PV.R on paper). Prediction: CONFIRMED, with two sharpenings (not discrepancies): global α = max_τ(ε_τ + (1−ε_τ)/15) exactly (worst explorer, U=[d]); fixed-coin α_u = 1 exactly; exact δ_τ = (14/15)ε_τ ≤ ε_τ.
- V3 (mixed-coin reduction W = φ(X,W′)). Prediction: CONFIRMED as DERIVED→PROVED under the hypotheses (a) coin conditional law given the data does not depend on the instance (κ(x,·) instance-free), (b) coin space standard Borel (or finite/countable). Expect to state that (a) is necessary (an instance-dependent kernel is not a scheme) — a scope clarification, not a discrepancy.
- V4 (fresh numerics s308_check.py, seed 308, exact integer arithmetic, d = 8 cube, β ∈ {1/2, 1/4}, n = 48, near-sound coin schemes built from honest majority-decode + small lie mass + fractional boundary outputs + x-dependent coin kernels).
  - N1 H(x,τ′) ≤ f_τ(x,τ′) off-diagonal below threshold: 0 violations, ≥ 100,000 cells with H > 0.
  - N2 g ≥ t − f2 pointwise: 0 violations.
  - N3 1{unique argmax H = τ} ≥ g − F pointwise: 0 violations AND ≥ 50% of (scheme,τ,x) cells non-vacuous (g − F > 0) — the S307 P3 power failure must not recur.
  - N4 end-to-end success_τ ≥ E g − E F ≥ 1 − δ − α2 − α3 for every τ: 0 violations AND every scheme non-vacuous (min_τ bound ≥ 0.3).
  - N5 Fubini/W-blind MC check: Monte Carlo of the first-argmax explorer on raw multinomial tapes and sampled coins matches exact E F within 4σ (all tested schemes); MC stat-law matches exact law (max abs dev within 4σ).
  - N6 threshold control: at w = β(1−β)/8 exactly a fractional recommendation (k = 1/2 at a Ham-1 rival) gives H = 1, f_τ = 0; one grid step below, no 1/64-grid fractional f achieves H > f.
  - N7 Example PV.R exact: global α matches closed form and S307's 0.23582; 2α+δ < 1; α_u = 1 for every u; PV.1 decoder success 0; averaged decoder success = 1 − ε_τ ≥ 1 − 2α − δ.
  - N8 Fano arithmetic: d = 64 equality, even d ≥ 66 strict at s = 1/2; c/4 = 0.0022996 (anchor, not blind).
Scoring HIT / PARTIAL / MISS. A MISS is reported, not re-run away. Overall item verdicts CONFIRMED / DISCREPANCY / INCONCLUSIVE.
