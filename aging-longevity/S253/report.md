# S253 VALIDATE: EPI-321 6-month comparator deltas checked against primary sources

Mode: VALIDATE. Trigger: a prior monitoring session flagged this as the next validation step.
Locked inputs, untouched: the pre-registration and its amendments from earlier sessions in this
line of work; no amendment of the pre-registration was made in this session.
Labels: OBSERVED = read first-hand in this session (source given). DERIVED = computed from
OBSERVED values. UNVERIFIED = the source could not be reached or does not state it.

## 0. Primary sources reached (first-hand)

| # | Source | Status |
|---|---|---|
| P1 | WMS 2026 presentation slides, Roxburgh R., "Emerging Data from the First-in-Human Study of EPI-321...", 17 slides, PDF created 2026-10-05, published by Epicrispr | OBSERVED |
| P2 | Epicrispr / Business Wire press release, 2026-10-05, re the same readout | OBSERVED |
| P3 | ReSolve protocol: LoRusso et al., BMC Neurol 2019;19:224, doi 10.1186/s12883-019-1452-x | OBSERVED, full text |
| P4 | ReSolve registry, NCT03458832, via ClinicalTrials.gov API v2 | OBSERVED |
| P5 | Digital-twin method: Blemker et al., Sci Rep 15:25339 (2025), doi 10.1038/s41598-025-09516-8 | OBSERVED, full text |
| P6 | WMS 2026 abstract 20O, NMD 67 S1 107362, doi 10.1016/j.nmd.2026.107362 | UNVERIFIED / INCONCLUSIVE (access-walled); superseded in practice by P1, which uses a later cutoff |
| P7 | Secondary coverage headline re a severe liver-enzyme-elevation AE | Secondary, consistent with P1 |

Key upgrade over the prior monitoring pass: that pass worked from the press release (P2) alone. The
actual presented slides (P1) are public on the sponsor's site. They contain the full composite
tables, SEM error bars, the ReSolve comparator n and matching method, a dose-split safety table, and
a DUXz biomarker readout. Every prior-session number is traced here to P1.

## 1. Item-by-item verification of the comparator deltas

| Item | Prior value | Primary source (P1 slide) | Verdict |
|---|---|---|---|
| I1. Upper-body LMV, EPI-321 vs digital twin | +3.0% vs -3.5% | Slide 13, "Upper Composite": EPI-321-02 (N=6) +3.0 vs Digital Twin (N=6) -3.5, % change from baseline at month 6, SEM bars. The press release (P2) gives the same values | CONFIRMED (OBSERVED) |
| I2. Upper-body QMT, EPI-321 vs ReSolve | +4.1% vs -0.3% | Slide 14, "Upper Composite": +4.1 vs ReSolve ECA (N=39) -0.3. Units are "Change from Baseline, Percent Predicted Normal (PPN)", i.e. percentage points of predicted-normal strength, not a relative % change. The press release says "4.1 percent" | CONFIRMED (values); DISCREPANCY (units) in P2 |
| I3. Elbow extension, strength +8.1% and LMV +3.2% vs -1.1% / -9.0% | as stated | Slide 15 table: Elbow Extension LMV +3.2 vs Digital Twin -9.0; QMT +8.1 PPN vs ReSolve ECA -1.1. The press release (P2) attributes -1.1 to the digital twin and -9.0 to ReSolve, the reverse of the slide, and also implausible on method grounds (digital twin is an MRI/LMV model; ReSolve ECA is a QMT comparator) | CONFIRMED (values and pairing per P1); DISCREPANCY in P2 (comparator attribution reversed; QMT again in PPN, not %) |
| I4. "First six patients", dose unstated | likely all 2e13 (inference) | P1 does not state the cohort of the efficacy n=6 ("EPI-321-02 (N=6)"). Slide 7: cohorts 2e13 (n=6) and 4e13 (n=6), enrolled sequentially. Slide 10: "Pt #6 data not available" | INCONCLUSIVE. Still DERIVED (likely cohort 1), not stated |
| I5. Total and lower-body LMV (prior note: "qualitative only") | n/a | Slide 13: Total +1.3 vs -2.7; Lower +0.3 vs -2.5 (OBSERVED) | Correction to the prior caveat. The values are now known |
| I6. Total and lower-body QMT | n/a | Slide 14: Total +3.3 vs -0.8; Lower +0.8 vs -1.3 PPN (OBSERVED; checked visually on the render). A web-search summary swapped total and lower; the slide is authoritative | New OBSERVED values |
| I7. No variance / no DUX4 data | n/a | SEM error bars are on slides 13 and 14, but no numeric SEM, p-value or CI is given. DUXz (cfDNA ZBTB17 signature) box plot, baseline vs 6 months, n=5 (Pt #6 missing), shows a lower median at 6 months. No statistic is given (slide 10) | Correction to the prior caveat. Biomarker data were presented on the slides, though not in the press release |

### Internal-consistency observations
- Two different "upper body" figures: Slide 13/14 "Upper Composite" gives LMV +3.0/-3.5 and QMT
  +4.1/-0.3. Slide 15 "Total Upper Body" gives LMV +2.8/-4.0 and QMT +3.0/-0.2. The press-release
  headline uses the composite (larger) QMT figure. These are different muscle groupings, not an
  arithmetic error. Still a selective-reporting signal.
- The comparator outperformed EPI-321 on one manoeuvre: Shoulder abduction QMT: EPI-321 +1.0 vs
  ReSolve ECA +2.2 (slide 15). The press release does not mention this. Elbow flexion QMT is close
  to null (+0.7 vs -0.2).
- Size of the 6-month digital-twin declines: the twin predicts -9.0% (elbow extensors) and -9.3%
  (elbow flexors) LMV in 6 months -- roughly 18%/yr linearly. The model (P5) predicts annualized
  change and was trained on roughly 1-year follow-up; P1 does not disclose how a 6-month value was
  obtained. Plausibility of these muscle-level rates: UNVERIFIED.

## 2. Comparator comparability (populations, windows, dosing)

| Dimension | EPI-321 | Digital twin (P5) | ReSolve ECA (P3, P4) | Match? |
|---|---|---|---|---|
| Population | Adults 18-75, FSHD1, Ricci 2-4 (of 5) | Model trained on >100 adult FSHD1 patients from pooled cohorts; severity metrics were not used (not harmonised across cohorts) | Age 18-75, FSHD1 (or clinical FSHD), symptomatic limb weakness, ambulatory 30 ft; up to 9 ReSolve matches per EPI-321 patient on age, sex, repeat length, Ricci, age-adjusted CSS/QMT; N=39 | Age band and FSHD1 match; severity-score use is a mismatch for the twin |
| Comparator type | Single-arm, open-label | Model prediction for the same 6 patients (not an observed control) | Historical external control (observational, untreated) | Neither is concurrent or randomized |
| Time window | Baseline to month 6 | Predicts annualized change; the 6-month derivation is not disclosed | Assessments at baseline, 3, 12 and 18 months only -- no 6-month visit | WINDOW MISMATCH for both comparators |
| Measurement | Whole-body MRI (Springbok) LMV; QMT in PPN | Same Springbok MRI pipeline | Fixed-myometry QMT; muscle set not fully specified | MRI matches; manoeuvre-level QMT match UNVERIFIED |
| Concomitant treatment | Prophylactic immunosuppression (prednisone cohort 1; prednisone+sirolimus+rituximab cohort 2) | none | none | Mismatch; not quantified in P1 |
| Dosing | 2e13 (n=6) / 4e13 (n=6) vg/kg IV; dose of the efficacy n=6 not stated | n/a | n/a | INCONCLUSIVE (I4) |

### DERIVED statistics (see scripts/validate_comparators.py, output scripts/validate_comparators.out.txt)
SEMs were read off the slide error bars (approximately +/-0.2). With n=6 (t_crit 2.571), every
per-arm EPI-321 95% CI includes 0. Net deltas versus comparator: LMV upper +6.5, total +4.0, lower
+2.8; QMT upper +4.4, total +4.1, lower +2.1 PPN. A naive Welch test only reaches p approx 0.04 for
upper LMV versus the twin; that test is invalid because the twin is a paired model prediction with
undisclosed 6-month error, so it is not reported as significance.

## 3. Dose and safety specifics (data cutoff reported on the slides; all OBSERVED)

| | 2e13 vg/kg (n=6) | 4e13 vg/kg (n=6) |
|---|---|---|
| Any AE | 6 (100%) | 3 (50%) |
| Related AE | 6 (100%) | 3 (50%) |
| Severe (>=Grade 3 CTCAE) | 1 (16.7%) | 1 (16.7%) |
| SAE | 0 | 1 (16.7%)* |
| Related SAE | 0 | 0 |
| AE leading to death | 0 | 0 |

- One participant had 2 severe AEs related to AAV (ALT and AST elevation), cohort 1 (prednisone
  prophylaxis only); responded to high-dose IV methylprednisolone with no clinical sequelae.
- *Cohort 2 SAE: Grade 3 hypertension with headache, hospitalized, assessed as not related to
  treatment.
- Presenter conclusion: the product "appears safe and well-tolerated with a manageable safety
  profile at both dose levels." A later-phase trial is expected to open.

The related-AE rate is lower at the higher dose, and the only severe related AE occurred at the low
dose -- confounded by intensified immunosuppression in cohort 2 and probably shorter follow-up for
cohort 2 at the data cutoff. The presenters do not flag any AE pattern as affecting dose selection
or the dosing window.

## 4. Bin decision (internal tracking terminology retained for continuity)
The prior monitoring session's classification bin STANDS. No re-classification. The discrepancies
found are in the press release's presentation (units and comparator attribution) and in comparator
design (window and population), not in the underlying slide data.

## 5. Discrepancy register
- D1 (press release): the elbow-extension comparator attribution is reversed relative to the
  slides. Factual, low-stakes, correctable.
- D2 (press release): QMT changes are reported as "percent," while the slides report change in
  percent-predicted-normal points.
- D3 (methods gap): the "6-month" ECA comes from a natural-history study with no 6-month visit, and
  the 6-month twin comes from an annualized model. The derivation method is undisclosed.

## 6. Verdict
CONFIRMED (the underlying slide data) with named DISCREPANCY in the public press release (units,
comparator attribution) and in comparator design (no true 6-month measurement exists for either
comparator).
