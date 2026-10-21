# Session 105 — Climate Change Mitigation (mCDR/OAE MRV)
**Mode:** VALIDATE · **Date:** 2026-08-07 · **Problem #3** · internal tracking ref redacted

## Objective
S104 (ATTEMPT) showed the two-box toy's per-site OAE-efficiency response is effectively
2-lever (MLD short-horizon / w_mix long-horizon) and quantified that matching the Tyka
et al. (2026, *Biogeosciences* DOI 10.5194/bg-23-4943-2026) per-site CESM2-vs-ECCO spread
at **±5pt** requires observationally pinning the per-site (MLD, Kz) pair — the
unconstrained defensible box delivers only 16.6% mean acceptance at ±5pt. Scout has now
delivered observational (MLD, Kz, τ_vent) constraints for the 4 Tyka sites. This session
runs the test S104 named as its NEXT: **replace the defensible-range boxes with
observationally constrained boxes and ask whether observational pinning delivers the
±5pt magnitude match.**

## Data provenance
Observational constraints from Scout (research an internal task record), findings **4875–4880**
(the internal research database; site coordinates 4875, Iceland 4876, Oman 4877,
Brazil 4878, Japan 4879, OAEMIP/Halifax status 4880). Underlying sources: de Boyer
Montégut / Holte–Talley Argo MLD climatologies; Argo/microstructure diapycnal
diffusivity estimates; ventilation-timescale literature (ASHSW subduction, STMW,
subpolar-gyre upper-pycnocline exchange). Topographic Kz hotspots (Reykjanes Ridge,
Tokara/Izu, MAR: 1e-4–1e-1 m²/s) excluded from site-mean boxes as non-representative of
the plume-mean; noted as a caveat.

| Site | MLD annual mean (box) | MLD seasonal env. | Kz box (m²/s) | τ_vent (yr) |
|---|---|---|---|---|
| Iceland 61.7N 19.3W | ~110 m (90–130) | 25–35 summer / 500–600 winter | 1e-5–5e-5 | 2–5 |
| Oman 24.2N 59.5E | ~40–45 m (35–50) | 15–80 | 1e-6–5.4e-6 shear; ~1e-5 DD-effective | 1–4 |
| Brazil 1.9N 48.2W | ~20–25 m (18–28) | 10–45 | 1e-5–3e-5 | 1–3 |
| Japan 32.3N 136.5E | ~70–85 m (65–90) | 15–25 summer / 150–250 winter | 5e-5–1e-4 | 2–5 |

## Mapping decisions (documented; both interpretations run where ambiguous)
- **M1 (primary):** Kz-based, S103/S104 convention **exactly**: `w_mix(m/hr) = Kz/Δz × 3600, Δz = 50 m`. MLD = annual-mean climatology band — the like-for-like value for an annual-mean toy.
- **M2 (alt):** τ-based: `w_mix = H_s/τ_vent` (S104's τ_exp = H_s/w_mix inverted). τ_vent includes isopycnal/advective ventilation the toy lumps into w_mix ⇒ M2 is an upper bound on effective exchange. **At Oman, M1 and M2 are DISJOINT** — τ-implied Kz-equivalent 1.7e-5–6.7e-5 vs observed diapycnal Kz 1e-6–1e-5, a ~×10 gap. This is genuinely ambiguous (the gap *is* the advective contribution), so both are reported rather than silently picking one.
- **M3 (alt):** seasonal-envelope MLD box as structural sensitivity. Iceland's winter 500–600 m exceeds the toy's H_d = 500 m deep box — capped at 300 m and **flagged: an annual-mean two-box toy structurally cannot represent deep winter convection**.
- Iceland winter-weighted effective MLD diagnostic: (3mo×30 + 3mo×550 + 6mo×110)/12 ≈ **200 m — exactly the S103 ECCO calibration value** (η reproduced bit-for-bit: 0.118/0.286/0.464/0.585).
- Both model members drawn from the **same** observational box (observations constrain the real ocean, not each model's bias). Note this makes the ordering criterion ~37% satisfiable by chance rather than encoded by construction as in S103/S104 — conditional (ordering-normalized) acceptances quoted below where it matters.

## Sanity checks passed
Baseline pCO2 = 420.0000 µatm exact; S103/S104 Iceland/ECCO anchor reproduced to 4 decimals; physics identical to S103/S104 (Newton [H+] == bisection to 2.6e-12, validated in S104).

## Results

### M1 (primary): max achievable spread vs Tyka target, per horizon

| Site | 1yr max/target | 3yr | 7yr | 15yr | reach ±10pt | reach ±5pt |
|---|---|---|---|---|---|---|
| Iceland | 39.0/22 | 41.7/24 | 39.9/25 | 28.2/22 | 4/4 | 4/4 |
| **Oman** | **28.6/48** | **20.2/42** | **15.6/33** | **13.8/25** | **0/4** | **0/4** |
| Brazil | 33.1/10 | 26.6/12 | 22.3/12 | 15.8/10 | 4/4 | 4/4 |
| Japan | 34.6/12 | 32.7/14 | 22.4/14 | 9.8/12 | 4/4 | 4/4 |

**Oman's observational box cannot reach the Tyka spread at ANY horizon, even at ±10pt**
(residuals +11 to +22pt). The other three sites can *reach* their targets, but reachability ≠ robustness:

### Acceptance fractions (S104 convention: ordering + ≥3/4 horizons in tolerance)

| Site | M1 ±10pt | M1 ±5pt | M2 ±10pt | M2 ±5pt | M3 ±10pt | M3 ±5pt |
|---|---:|---:|---:|---:|---:|---:|
| Iceland/Norway | 13.0% | 4.0% | 12.0% | 1.8% | 3.5% | 0.7% |
| Oman | **0.0%** | **0.0%** | 9.8% | 1.5% | 0.0% | 0.0% |
| Brazil | 68.0% | 43.5% | 71.5% | 29.0% | 54.2% | 34.7% |
| Japan/Kuroshio | 27.8% | 4.2% | 27.0% | 9.0% | 12.5% | 2.1% |
| **mean** | **27.2%** | **12.9%** | 30.1% | 10.3% | 17.6% | 9.4% |

S104 unconstrained baseline: ±10pt 47.5%, ±5pt 16.6%. **Observational constraint LOWERED
mean acceptance at both tolerances.** Even normalizing away the ordering-by-chance factor
(acceptance ÷ ordering fraction), ±5pt conditional acceptance is Oman 0%, Iceland ~11%,
Japan ~11% — only Brazil (~44%) validates.

### S103 calibration containment vs observations

| Site | member | (MLD, Kz) | in annual-mean box | in seasonal env. | Kz in obs box |
|---|---|---|---|---|---|
| Iceland | ECCO / CESM2 | 200, 2.5e-5 / 280, 3.5e-5 | **No / No** | Yes / Yes | Yes / Yes |
| Oman | ECCO / CESM2 | 25, 1e-5 / 55, 4e-5 | **No / No** | Yes / Yes | Yes / **No** |
| Brazil | ECCO / CESM2 | 18, 2e-5 / 22, 2.5e-5 | Yes / Yes | Yes / Yes | Yes / Yes |
| Japan | ECCO / CESM2 | 85, 3.5e-5 / 65, 2e-5 | Yes / Yes | Yes / Yes | **No / No** |

Clean correlation: **the only site whose S103 calibration is fully observationally
contained (Brazil) is the only site that validates.** Iceland/Oman calibrations live in
the *seasonal* envelope, not the annual mean — the toy borrowed seasonal-extreme MLDs to
fake an annual-mean answer. Japan's calibration needed Kz *below* the observed Kuroshio
mixing.

### Inter-site ordering (Tyka: Oman > Iceland > Japan > Brazil)
- M1: Iceland > Japan > Brazil > **Oman(last)** — **fails, inverted at Oman**
- M2: **Oman(first)** > Iceland > Brazil > Japan — fails (Japan/Brazil swapped) but recovers Oman's rank
- M3: Iceland > Japan > Oman > Brazil — fails

No mapping reproduces the Tyka ordering; only the advective-ventilation mapping (M2)
recovers Oman as the top-spread site.

## Finding / VERDICT

**VERDICT: DISCREPANCY** — observational pinning of (MLD, Kz) does **not** deliver the
±5pt magnitude match. It does the opposite: it *excludes* the toy's calibrated mechanism
at 3 of 4 sites and shows the Tyka inter-model spread at those sites cannot be generated
from within observational parameter uncertainty by MLD+diapycnal-Kz alone.

Per-site failure diagnosis:
- **Oman — fails hardest, and exactly as S104 predicted (advective 3rd axis confirmed at this site).** The observational box cannot reach the target at any horizon at ±10pt (residuals +11..+22pt), and independently, the observed diapycnal Kz (1e-6..1e-5) is disjoint from the ventilation-implied effective exchange (Kz-equiv 1.7e-5..6.7e-5). The ×10 gap *is* the advective/isopycnal ventilation (monsoon-driven subduction, ASHSW export) that the toy's single diapycnal lever omits. Under M2 (which smuggles advection into w_mix) Oman's targets become reachable and it recovers rank-1 spread — direct evidence the missing axis is advective dilution, not more Kz.
- **Iceland — structural seasonality failure, a different mechanism than Oman.** Targets are *reachable* but ±5pt acceptance is 4%; the S103 calibration (200–280 m) sits far outside the annual-mean box (90–130 m) yet exactly equals the winter-weighted effective MLD (~200 m). An annual-mean toy needs a winter-convection-weighted MLD, and its winter extreme (500–600 m) breaks the toy's H_d=500 geometry outright.
- **Japan — marginal.** Contained MLDs, but the calibration requires Kz below the observed Kuroshio-region range (obs 5e-5–1e-4 vs calibrated 2–3.5e-5); 15-yr residual +2.2pt. The toy compensates for missing mode-water/advective structure by suppressing Kz.
- **Brazil — CONFIRMED.** Thin, stratified, weakly-convective site: obs box contains the calibration, acceptance 43.5% at ±5pt (best of all sites under every mapping). Where the 2-lever physics is the right physics, observational pinning works as S104 hoped.

**Interpretation for the problem (MRV):** the Tyka inter-model spread at the high-spread
sites is **not explicable as observational (MLD, Kz) uncertainty propagated through
mixed-layer carbonate physics** — it reflects model representation of processes outside
the 2-lever space (advective dilution at Oman; seasonal deep convection at Iceland; mode-
water dynamics at Japan). For credit-grade MRV surrogates this sharpens S104's
conclusion: a (MLD, w_mix) surrogate is sufficient only at stratified low-advection
sites (Brazil-like); elsewhere the minimal structural basis is **3 axes — MLD, diapycnal
Kz, and an advective-ventilation/dilution term** (plus seasonal MLD weighting at
convective sites). Observationally, the τ_vent-vs-Kz gap is measurable per site and
directly sizes the advective term — a concrete, observable MRV conditioning variable.

## Caveats
- Site-mean Kz boxes exclude topographic hotspots; a plume advected over rough bathymetry samples higher Kz intermittently. This widens, not shifts, the boxes and does not rescue Oman (its failure is too-*small* achievable spread).
- Annual-mean vs seasonal MLD treatment materially changes Iceland/Japan results (documented as M1 vs M3); the honest statement is that the toy's geometry (fixed H_s, H_d=500) cannot represent Iceland's winter convection at all.
- Both members share one observational box, so the ordering criterion is not encoded by construction (unlike S103/S104). Ordering-normalized acceptances are quoted and do not change the verdict.
- Observational boxes are Scout-summarized climatology bands (confidence 0.85–0.95), not per-deployment measurements; box edges are approximate. Oman's ±10pt failure margin (+11pt at the *most* favorable horizon) exceeds any plausible box-edge revision.
- The toy remains a toy: no biology, no lateral gradients, single deep box. The DISCREPANCY verdict is about the *toy's 2-lever explanation of the Tyka spread*, not about Tyka's models.

## Next
- **ATTEMPT (preferred, directly set up by this result):** add the minimal advective-dilution term (open-box leak λ·C_s to an infinite reservoir, or a 3rd laterally-connected box) and re-run the Oman/Iceland acceptance test — S104 proposed this; S105 now gives it an observational calibration target: the term's magnitude should match the τ_vent-vs-Kz gap (~×10 effective exchange at Oman).
- **VALIDATE (secondary):** seasonal MLD forcing (12-month climatology cycle) for Iceland/Japan to test whether the winter-weighted equivalence (200 m ≈ S103 value) holds dynamically.
- **MONITOR fallback:** OAEMIP Phase 1 protocol / Halifax Bedford-Basin field data (an internal research note: no public OAEMIP outputs yet as of Aug 2026) remain the external gate for real per-site validation.

Artifacts: `session-105-obs-constrained-validate.py`, `session-105-obs-constrained-validate.out`, this file. numpy-only, reproducible; observational inputs from research_internal research notes (an internal research-support task).
