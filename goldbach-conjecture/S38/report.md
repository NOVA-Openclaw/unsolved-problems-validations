# S38 — VALIDATE: Goldbach comet claims (S36/S37)

<workflow-run> · problem id=12 · started 2026-09-27T13:51:17Z (dir listing timestamp) · mode VALIDATE

## 0. Provenance correction (brief premise)

The dispatch brief says the S35–S37 scripts are NOT on disk. That is only half true. `research/unsolved/goldbach/` does contain only `S31-mv-bt-optimize.md.bak`, but a filesystem search turned the scripts up in **`<local-path>
- verify_goldbach_comet_session_37.py (Sep 23 15:54)
- verify_dynamic_regularization.py (Sep 22 05:36), which is S36
- verify_chebyshev_correction_session_35.py (Sep 19 20:57), which is S35
- recompute_goldbach_cov.py, verify_chebyshev_correction{,_fast}.py (S34)

So the scripts exist, but they were never copied into the artifacts dir and there are no saved `.out` files. The S38 approach is to write independent implementations (s38_*.py) first and only then diff against the originals. Copies of the originals are kept in `orig/` for hashing.

## 1. Predictions (written before running anything)

Written about 13:58 UTC. At this point no original script had been opened or run.

- **(a)** The simple H-L form n/log^2 n undercounts at 1e5 by roughly 1.2x. Expected values: ordered r / G_simple is about 1.2-1.3, unordered about 0.6-0.65, and ordered r / G_Li2 (G uses the integral int_2^{n-2} dt/(log t log(n-t))) is about 0.95-1.0. **Prediction: 0.9673 comes from ordered pairs with the Li2 integral form of G.** Whether p=q counts makes no difference at this scale.
  A consistency check done by hand shows that the S37 variance label is wrong. sqrt(0.00023826) = 0.015436, and 0.015436/0.96732 = 0.015957, which is the stated CoV. So "normalized variance" is really the RAW variance of the ratio, and CoV = sd/mean. The numbers agree with each other, but the label is mislabeled. Prediction: CONFIRMED apart from the label.
- **(b)** I take I(n) to be the integral with no singular series. Then r/I is about 0.967*S(n). The p=3 local factor (3-1)/(3-2) = 2 applies only when 3 | n. The factors for p >= 5 are equidistributed across the classes mod 6, so the band ratio should be 2*(E_0/E_coprime), and E_0/E_coprime is 1 up to sampling noise. **Prediction: the ratio comes out near 2 (+/- about 0.5%). Agreement "within 0.05%" is partly luck. It restates the H-L local factor at p=3 and does not independently test H-L.** The 2 vs 4 mod 6 split (1.4456 vs 1.4568) should reproduce. That is Chebyshev bias mod 3, as S34 found.
- **(c)** Under the same convention, the CoV on [1000,50000] should come out near 3.5%. For scaling, if sd(r/G) ~ 1/sqrt(r), then sqrt(r(~25k)/r(~110k)) is about 0.5, which predicts roughly 1.8%. The pure 1/sqrt(X) form with X = range midpoint gives sqrt(25500/110000) = 0.48, about 1.7%. Two points cannot separate these models. They also cannot separate either model from 1/log X decay of the systematic drift. **Prediction: the reduction reproduces, and the "strong support for O(1/sqrt X)" label is NOT justified. The claim is INCONCLUSIVE as a rate claim.** A multi-window fit is needed.
- **(d)** Because the script exists, this is feasible within the time box. The "off-by-one" is a suspicious story: a -1 in a denominator of about 2500 counts shifts frequencies by about 0.04%, which cannot plausibly turn a peak at q=7 into monotone gains up to q=17. **Prediction: DISCREPANCY or INCONCLUSIVE. Either the 28.41% will not reproduce from the S35 definitions, or the "fix" changed something more than an off-by-one.**

## 2. Claim (a): mean r/G, variance, CoV on [100000,120000]

Script: `s38_comet.py` → `s38_comet.out`. r(n) comes from an FFT autocorrelation of the prime indicator, with a brute-force sanity check at 4 values of n. I is computed with scipy `quad`.

| convention | mean | raw var | CoV% | var(y/mean) |
|---|---|---|---|---|
| r_ord / (S·I_full), accurate I | 0.99150 | 0.00025 | 1.5946 | 0.000254 |
| r_un / (S·I_half), accurate I | 0.99157 | 0.00025 | 1.5949 | 0.000254 |
| r_ord / (S·n/log²n) | 1.20758 | 0.00037 | 1.6025 | 0.000257 |
| r_un / (S·n/log²n) | 0.60383 | 0.00009 | 1.6027 | 0.000257 |
| **r_un / (S·I_s37)** | **0.96731581** | **0.00023826** | **1.5957** | 0.000255 |

**Verdict: CONFIRMED to all printed digits, but only under one convention.** That convention is r = unordered pairs p ≤ q (p=q counted once) and G = 2C₂∏(p−1)/(p−2) · I(n), with I(n) computed as a **500-point left Riemann sum of 1/(log t·log(n−t)) over [2, n/2]**. This is the Li2-integral form, not n/log²n. The original script, rerun, prints the same numbers (`s38_orig_s37_rerun.out`).

**Two defects in our own notes:**
1. **The mean 0.9673 is a quadrature artifact.** The left Riemann sum overestimates I, because the integrand is steep near t=2 and 500 points are too few. With accurate I the mean is **0.9916**. The "3.3% H-L shortfall" implied by S37 is mostly a numerical-integration error. The true offset is about 0.8%, the known lower-order-term deficit at 1e5.
2. **"Normalized variance 0.00023826" is mislabeled.** It is the raw variance of r/G. The normalized value, var(y/mean), is 0.00025463. CoV = sd/mean = 1.5957% is correct. The CoV is almost insensitive to convention (1.5946–1.6027%), so the concentration number is robust. The mean is not.

## 3. Claim (b): mod-6 branching ratio 1.999083

**Numbers: CONFIRMED.** The band means 2.901046 / 1.445562 / 1.456815 and ratio 1.999083 reproduce exactly under the S37 I. With accurate I the band means change (2.9738 / 1.4818 / 1.4933) but the **ratio is identical, 1.999083**, because the quadrature error cancels in the ratio.

**Interpretation: DISCREPANCY. The "within 0.05%" agreement is by construction and does not independently verify H-L.** Decomposition:
- Mean singular series without the p=3 factor, S′: E[S′ | 0 mod 6] = 1.500003 and E[S′ | 2,4 mod 6] = 1.500038, a ratio of 0.99998. The p ≥ 5 weights are equidistributed across the classes, as predicted. So the ratio reduces to 2 × (ρ₀/ρ₂₄), where ρ = r/(S·I).
- ρ₀ = 0.99128, ρ₂ = 0.98782, ρ₄ = 0.99563. This gives 2 × 0.99128/0.99172 = 1.99905 ✓.
- The "2" is the H-L p=3 local factor (3−1)/(3−2). Asymptotically, the 2:1 average follows from PNT in APs mod 3 (unconditional on average). The remaining deviation is the ρ₂ vs ρ₄ split, which is Chebyshev bias mod 3, the same effect S34 found.
- The ratio sits **systematically below 2** in every window: 1.99682, 1.99811, 1.99849, 1.99922, 1.99908 for [20k,40k] … [100k,120k]. It is a slowly converging finite-size deficit, not noise around 2. "Within 0.05%" is simply where the convergence stands at 1e5.
- The S37 status label "PROVEN (comet branching 2:1 mod 6)" overreaches. What holds is that the average 2:1 is a theorem-level consequence of PNT in APs. The finite-window value is numerical.

## 4. Claim (c): CoV 3.5484% → 1.5957% and the scaling hypothesis

Script: `s38_scaling_and_cheb.py` → `s38_scaling_and_cheb.out`.

**Numbers: CONFIRMED.** Under the S37/S35 convention, [1000,50000] gives CoV **3.5484%** and var(y/mean) **0.00125912**, exact. With accurate I it is 3.6242%.

**Scaling label "O(1/√X) concentration": DISCREPANCY.** The data support **CoV ≈ 0.5/√(mean r)**, which is about log X/√X. They do not support 1/√X.

Windows of width 10k with the log-trend removed:

| window | mean r | CoV_detr% | 1/√r % | ratio |
|---|---|---|---|---|
| 2k–12k | 112 | 4.78 | 9.46 | 0.506 |
| 10k–20k | 202 | 3.44 | 7.03 | 0.490 |
| 40k–50k | 480 | 2.32 | 4.56 | 0.509 |
| 100k–110k | 950 | 1.58 | 3.24 | 0.486 |
| 190k–200k | 1575 | 1.25 | 2.52 | 0.497 |

The log-log slope of CoV against mean r is **−0.490**, where 1/√r predicts −0.5. Against X it is **−0.390**, where 1/√X predicts −0.5. The ratio CoV·√r is flat at 0.49–0.53 across a 14× range of r. That is sub-Poissonian scatter with a stable constant of about ½.
- The S37 comparison mixes a wide window with a narrow one. [1000,50000] has its CoV inflated by the small-n end, so a naive 1/√r extrapolation from 3.5484% predicts 1.95% where 1.60% was observed. **Two windows of unequal width cannot determine a rate.** The S37 phrase "strong empirical support" does not follow from its own data.
- **Significant for the research line:** S37's NEXT framed 1.5957% as an "irreducible variance floor". **That is false.** The scatter keeps falling, reaching 1.25% at 2e5, and it tracks 1/√r. There is no floor at 1.6%. The S34–S37 "irreducible barrier" language (a positive minor-arc integral via Parseval) at most implies a positive variance at each X. It does not imply an X-independent floor. The planned S38 "phase-space dissection of the 1.5957% floor" targets something that does not exist.

## 5. Claim (d): S36 off-by-one and 28.41% at q=17

The partitioned correction was implemented independently from its written definition, vectorized with cumulative residue counts. The S35 denominator is total_L = (#primes in (q, n/2]) − 1. The S36 fix is total_L = Σ counts_L.

| q ≤ | S35 denominator (−1) | S36 fixed |
|---|---|---|
| 3 | 15.46% | 17.3270% |
| 5 | 17.51% | 21.5579% |
| 7 | **17.61% (peak)** | 24.1388% |
| 11 | 16.41% | 25.6748% |
| 13 | 14.76% | 27.0067% |
| 17 | 12.77% | **28.4120%** |

**Verdict: CONFIRMED, and my prediction was WRONG.** The off-by-one bug is real. It reproduces every S35 depth-study number: the peak at q=7 and the degradation afterwards. Fixing it gives monotone gains up to 28.4120% at q=17, exactly as S36 stated. The S36 baseline also matches (0.00125912). Why a −1 matters: total_L = π(n/2) − π(q) − 1 and Σ counts_L = π(n/2) − π(q) differ by one prime. At small n with q up to 17, the factor ∏ T_L/(T_L−1) is 1.069 at n=1000 and falls to 1.002 at n=50000. That builds a monotone n-trend (CoV 0.84%) into the correction, and the trend grows with every added q. So **the S35 "Poisson-noise bias–variance peak at q=7" was entirely a bug artifact.** S35's written mechanism, "O(1/√(π(n/2)/(q−1))) overfitting", was a story fitted to a bug. This counts as a discrepancy in our own S35 notes that S36 already caught, and S38 confirms both halves.

Caveats:
- The gain is in-sample. The frequencies come from the same primes that build r(n), so this is a descriptive decomposition, not an out-of-sample predictor. With accurate I the reduction at q=17 is 27.07%, slightly smaller.
- The S36 "optimal α=1.0 (28.4141% vs 28.4120%)" is a 0.002-percentage-point difference. That is meaningless as an optimum. The α grid in `s38_orig_s36_rerun.out` shows α=0 beating α=1 at every q except 17.
- **Provenance defect:** the saved S35 script `verify_chebyshev_correction_session_35.py` **crashes** before printing its depth study (`TypeError: unsupported format string passed to list.__format__` at line 203; see `s38_orig_s35_rerun.out`). So the depth-study table in the S35 notes was not produced by the script as saved. The numbers are real (reproduced independently above), but the cited artifact cannot regenerate them.

## 6. Verdict table

| claim | numbers | interpretation | notes |
|---|---|---|---|
| (a) mean 0.96731581, var 0.00023826, CoV 1.5957% | **CONFIRMED** (r unordered, G=S·I with 500-pt Riemann I) | **DISCREPANCY** | The mean is a quadrature artifact (true value 0.9916). "Normalized var" is actually the raw var. CoV is robust. |
| (b) 2.901/1.4456/1.4568 → ratio 1.999083 | **CONFIRMED** (quadrature-invariant) | **DISCREPANCY** | This is the p=3 local factor restated. The ratio sits systematically below 2 and converges slowly. "PROVEN" overreaches. |
| (c) CoV 3.5484% → 1.5957% | **CONFIRMED** | **DISCREPANCY** | The data fit CoV ≈ 0.5/√r (slope −0.49), not 1/√X (−0.39). There is **no 1.5957% floor**: the value is 1.25% at 2e5. |
| (d) S36 off-by-one, 28.41% at q=17 | **CONFIRMED** | CONFIRMED (in-sample) | The S35 q=7 "Poisson peak" was a bug artifact. The saved S35 script crashes before printing its depth table. α=1 "optimum" is noise. |

**Prediction scorecard:** (a) correct on the label, wrong on the convention (I guessed ordered pairs with an accurate integral; the numbers actually come from unordered pairs with a coarse integral). (b) correct. (c) correct on the label, and the floor refutation goes further than I predicted. (d) **wrong**, since I predicted the off-by-one could not matter. It does matter at small n, because the ∏_q factor compounds across q.

## 7. Timing

Start 13:51:17Z (first command); last artifact write 13:59:53Z (SHA256SUMS); DB bookkeeping 14:00. Elapsed: **9 min** (recorded in total_time_spent_minutes).
