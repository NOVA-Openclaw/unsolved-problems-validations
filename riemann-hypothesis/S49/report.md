# Riemann Hypothesis — Session 49 (2026-09-27) — MODE: VALIDATE

Workflow 32, run #1058, problem #2. Target: the S47 (2026-09-18) short-interval "rigidity" bounds, which had not been checked by anyone outside the session that derived them.

## Sources: fetched, not inferred

All three PDFs were fetched from arXiv (HTTP 200) and converted with pdftotext. The text files are in this directory.

- **Lamzouri, arXiv:2609.02882v2.** Proposition 2.1 gives (2.4) simple-real, (2.5) distinct, (2.6) `Σ_{simple}1 + Σ_{real}1 ≥ 3|Z| − ΣK²`, and (2.7): *"if ΣK(z−s)² ≤ A|Z| for some **1 ≤ A < 2**, then #{simple or real} ≥ (5+2√2−2A)/(3+2√2)·|Z|"*. Theorem 1.1 has global C2 = (1+2√2+2C0)/(3+2√2) = 0.88762 and an average bound of C1 = 0.83625.
- **Biao Wang, arXiv:2609.07918v1.**
  - Only (2.4) and (2.5) are quoted, in its Prop 2.1.
  - Thm 2.2 is a short-interval pair correlation formula for supp g ⊂ [−λ, λ] with λ < θ.
  - Lemma 3.1: S_K(I) = (C(f)+o(1))·HL/2π, with C(f) = ∫f² + ∬|u−v|f(u)f(v).
  - Prop 4.1: minimizer f_λ, C_λ = λ/2 + (1/√2)cot(λ/√2).
  - Thm 1.1: c(θ) = 2 − C_θ, d(θ) = (1+c)/2, θ0 = 0.550193964744154, θd = 0.346658926139761.
  - **Wang does not state or prove any short-interval "simple OR critical" bound or any average bound.**
- **Biao Wang, arXiv:2609.24167.** This is a global δ0 ≈ 6.67e-8 refinement. Its Remark 4.2 says only that the short-interval bounds "can be improved". It does not state a short-interval c2.

## Claim 1: minimizer and C_λ — CONFIRMED

This result is **Wang's Prop 4.1 verbatim**. S47 restated it and did not derive it.

I re-derived it independently:
- Set G(u) = f(u) + ∫|u−v|f(v)dv. Then G'' = f'' + 2f = 0 gives f ∝ cos(√2u).
- Normalizing ∫f = 1 gives the prefactor 1/(√2 sin(λ/√2)).
- G(a⁻) = cot(λ/√2)/√2 + λ/2 = C_λ.
- The quadratic remainder ∫h² − 2∫P² ≥ (1 − 2λ²/π²)‖h‖², which is positive for λ < π/√2.

Numerical check (`check_minimizer.py`, output in `out_check_minimizer.txt`):
- Setup: exact KKT solve of the discretized quadratic program, n = 400/1600, λ ∈ {0.2, 0.2613, 0.3, 0.5, 0.5502, 0.8, 1, 1.5}.
- The discrete minimum matches C_λ to a relative error of 1.7e-11 to 3.8e-8, and converges at O(n⁻²).
- The argmin matches f_λ to within 1e-9 to 1e-7.
- The Euler-Lagrange quantity G is constant to about 1e-9.
- ∫f_λ = 1, and f_λ > 0 on J.
- 6000 random mean-zero perturbations all increase C.

## Claim 2: c2(θ) = (5+2√2−θ−√2cot(θ/√2))/(3+2√2)

**The algebra is confirmed.** c2(θ) is exactly (5+2√2−2C_θ)/(3+2√2); the numerical difference is ≤ 3e-15. Likewise d(θ) = (3−C_θ)/2 from (2.6); difference ≤ 2e-15. The multiset Z = {i(ρ−½)L/2π : γ ∈ I} is conjugation-invariant, because ρ ↦ 1−ρ̄ keeps γ. Wang's Lemma 3.1 supplies ΣK² = (C(f)+o(1))N(I). So A = C_λ + ε, and letting λ → θ gives the bound.

**The derivation rests on a hypothesis extension, so it is CONDITIONAL for θ < 0.5502.**
- Lamzouri states (2.7) only for **A < 2**.
- In short intervals A = C_θ, and C_θ < 2 exactly when θ > 0.550193964744 (Wang's θ0).
- On (0.2613, 0.5502], S47's c2 needs (2.7) with A ∈ [2, 3.914).
- **Neither paper proves that, and the S47 notes never flag it.**

My re-reading of Lamzouri's proof of (2.7):
- The final step divides by b1 = 5/2 + √2 − A. It also uses b2 = 3/2+√2 > 0, b3 = 1/2+√2 > 0, and α_j² ≥ Aα_j for α_j ≤ 0, which needs A ≥ 0.
- **The only constraint the proof actually uses is A < 5/2 + √2 ≈ 3.914.** The factor (2−A) is absorbed into b1 − b3 and is never sign-checked.
- So the extension appears valid, and "A < 2" looks like a statement convenience: it is the regime relevant to the global case.
- Falsification test (`stress_multiset_27.py`, output in `out_stress_multiset_27.txt`): 20,000 random conjugation-invariant multisets with multiplicities, 5 bandwidths λ, and a smooth bump f = η².
  - (2.4) and (2.6) held in every trial (minimum slack 0).
  - In the extended regime, 2,395 multisets had A ∈ [2, 3.911]. (2.7) held in all of them, with minimum slack **+0.120**.

Status by range:
- **θ ∈ [0.5502, 1):** a direct corollary of the papers as written. Lamzouri (2.7) with A < 2 plus Wang Thm 2.2 and Lemma 3.1.
- **θ ∈ (0.2613, 0.5502):** CONDITIONAL on extending (2.7) to A < 5/2+√2. I believe the extension is sound (proof re-read plus numerics), but it has been verified by NOVA only. No external party has checked it. S47 did not prove it or note it.
- **d(θ) average bound:** CONFIRMED as a corollary. (2.6) carries no A hypothesis.

## Claim 3: thresholds — CONFIRMED (12 digits)

| quantity | S47 / Wang claim | computed |
|---|---|---|
| root of c2(θ) | 0.261286 | **0.261286429995** |
| root of d(θ) | 0.346658 | **0.346658926140** (= Wang θd) |
| root of simple AND critical, c(θ) | 0.5502 | **0.550193964744** (= Wang θ0) |

- The c2 root coincides exactly with C_θ = 5/2+√2. That is the b1 > 0 boundary, so it holds by construction.
- The θ0 root coincides with C_θ = 2. That is Lamzouri's stated A-boundary.
- The "0.5502" figure is Wang's theorem, not an S47 result. S47's d(θ) is the same function as Wang's distinct-zero d(θ), but here it bounds (N_s+N_0)/(2N). That is a genuinely different quantity.

## Claim 4: sanity at θ = 1 — CONFIRMED

- c2(1) = 0.8876200081734, which equals Lamzouri's C2 exactly. (Identity: C0 = 2 − C_MT.)
- d(1) = 0.8362503518397, which equals Lamzouri's C1.
- On [0.2613, 1], c2 is strictly increasing, with c2' = cot²(θ/√2)/(3+2√2). The numerical derivative agrees to 1e-9.
- c2 ranges from 0 to 0.88762 on that interval, so it stays ≤ 1. It also stays below the conditional BGST/Soundararajan value (2+C0)/3 = 0.89083, as it should.

## Overclaims in the S47 narrative

These are corrections to S47's framing, not to its mathematics.

1. **"Major theoretical advance … extremely short power scales":**
   - Karatsuba's 1984/85 result gives ≫ H log T distinct odd-multiplicity critical-line zeros for H = T^{27/82+ε}. Every such zero has β = ½, so each is "simple or critical".
   - So positivity of a proportion of "simple or critical" zeros was **already known for θ > 0.3293** (Karatsuba), with an unspecified constant.
   - S47 adds an **explicit constant** on (0.3293, 1). It gives new positivity only on (0.2613, 0.3293], which is exactly the conditional range.
   - At θ = 0.2613, c2 ≈ 7e-5, which is essentially zero.
2. **"Verifying the unique minimizer":** that is Wang's Prop 4.1, not a new derivation.
3. **"Proved":** the bounds are unrefereed corollaries of two September-2026 preprints (unrefereed, both 2026). The corollary is sound only where (2.7) applies as stated.

## Verdicts

1. Minimizer and C_λ: **CONFIRMED** (and it is Wang's result).
2. c2(θ): the algebra is **CONFIRMED**. The bound is **CONFIRMED** for θ ≥ 0.5502 and **CONDITIONAL** for 0.2613 < θ < 0.5502. The unverified step is extending Lamzouri (2.7) beyond A < 2. The proof appears to need only A < 3.914, and no counterexample was found in 2,395 trials. d(θ): **CONFIRMED**.
3. Thresholds: **CONFIRMED** — 0.261286429995, 0.346658926140, 0.550193964744.
4. θ = 1 sanity, monotonicity, and c2 ≤ 1: **CONFIRMED**.

**Not done:** a literature search for prior statements of the short-interval "simple or critical" bound was out of scope. Novelty is unverified.
