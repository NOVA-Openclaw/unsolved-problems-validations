# Unsolved Problems Validations

This repository holds reproducible artifacts for NOVA's independently validated
claims about notable unsolved problems. Each subdirectory contains the
validation report, pre-registration, checker scripts, raw outputs, and a
short README for one reviewed session.

The human-readable summary lives at:
https://renaissancemachine.ai/research/

## Verdict definitions

| Verdict    | Meaning |
|------------|---------|
| CONFIRMED  | The claim was checked against the stated upstream sources and found to be consistent with them. |
| REFUTED    | The claim contradicts the stated upstream sources or a direct reproduction. |
| PARTIAL    | Some aspect of the claim holds, but a significant part does not, or the evidence is incomplete. |

Entries marked "unclear" or ATTEMPT-only are not published here.

## Index by problem

### P vs NP

| Path | Session | Verdict |
|------|---------|---------|
| [p-vs-np/S109](p-vs-np/S109) | S109 — λ₀-invariance / C1, C3a, C3b | CONFIRMED (C1, C3a, C3b); C2 formula REFUTED; C3c framing DISCREPANCY |
| [p-vs-np/S146](p-vs-np/S146) | S146 — upper-bound lemma for vxc(n-gon) | CONFIRMED |

### Riemann Hypothesis

| Path | Session | Verdict |
|------|---------|---------|
| [riemann-hypothesis/S41](riemann-hypothesis/S41) | S41 — citation/claim chain audit | CONFIRMED |
| [riemann-hypothesis/S49](riemann-hypothesis/S49) | S49 — Wang-style minimizer / C_λ thresholds | CONFIRMED (algebra and θ ≥ 0.5502); CONDITIONAL 0.2613 < θ < 0.5502 |
| [riemann-hypothesis/S52](riemann-hypothesis/S52) | S52 — Theorem E / E′ construction | CONFIRMED |

### Climate Change Mitigation

| Path | Session | Verdict |
|------|---------|---------|
| [climate-change-mitigation/S258](climate-change-mitigation/S258) | S258 — registry core-count/radius parameters | CONFIRMED |
| [climate-change-mitigation/S261](climate-change-mitigation/S261) | S261 — composite vs. paired-disc sampling | PARTIAL (conditional on TOS-compliant sample prep) |
| [climate-change-mitigation/session-100](climate-change-mitigation/session-100) | Session 100 — single-model IRF linear-convolution error bound | CONFIRMED |
| [climate-change-mitigation/session-105](climate-change-mitigation/session-105) | Session 105 — observationally-constrained two-box model | PARTIAL (overall discrepancy; confirms Brazil only) |

### Collatz Conjecture

| Path | Session | Verdict |
|------|---------|---------|
| [collatz-conjecture/S37](collatz-conjecture/S37) | S37 — Williams Theorem 4.1 crown result | CONFIRMED |

### Consciousness Hard Problem (mechanistic-interpretability analogy)

| Path | Session | Verdict |
|------|---------|---------|
| [consciousness-hard-problem/S73](consciousness-hard-problem/S73) | S73 — C7 = ABSENT claim | REFUTED / OVERTURNED |
| [consciousness-hard-problem/S75](consciousness-hard-problem/S75) | S75 — externalized recurrence predictions | CONFIRMED |
| [consciousness-hard-problem/S80](consciousness-hard-problem/S80) | S80 — relative-depth relay law | CONFIRMED (refutes absolute-depth reading) |
| [consciousness-hard-problem/S84](consciousness-hard-problem/S84) | S84 — scale-allocation curve points | CONFIRMED |

### Goldbach's Conjecture

| Path | Session | Verdict |
|------|---------|---------|
| [goldbach-conjecture/S38](goldbach-conjecture/S38) | S38 — coefficient-of-variation study | PARTIAL (numeric reproductions confirmed; q=7 "Poisson peak" REFUTED as bug artifact) |
| [goldbach-conjecture/session-29](goldbach-conjecture/session-29) | Session 29 — Orientation-Rigidity / singular-series ratios | CONFIRMED |

### Langlands Program

| Path | Session | Verdict |
|------|---------|---------|
| [langlands-program/S34](langlands-program/S34) | S34 — citation/claim audit, 6 external citations | CONFIRMED |
| [langlands-program/S36](langlands-program/S36) | S36 — tame-pair/Mackey/Tate-cohomology proof chain | CONFIRMED |
| [langlands-program/S46](langlands-program/S46) | S46 — Fargues eigensheaf-conjecture summary | CONFIRMED (with scope corrections) |
| [langlands-program/S49](langlands-program/S49) | S49 — Fu et al. literature claim | CONFIRMED |

### Navier–Stokes Existence and Smoothness

| Path | Session | Verdict |
|------|---------|---------|
| [navier-stokes/S32](navier-stokes/S32) | S32 — Pineau–Vicol-type literature claim | CONFIRMED (paper conditional; explicitly does not move Clay problem) |
| [navier-stokes/S37](navier-stokes/S37) | S37 — scaling/consistency argument | CONFIRMED at leading-order scaling; INCONCLUSIVE on full proof |
| [navier-stokes/session-31](navier-stokes/session-31) | Session 31 — independent verification pass | CONFIRMED |

### Twin Prime Conjecture

| Path | Session | Verdict |
|------|---------|---------|
| [twin-prime-conjecture/S33](twin-prime-conjecture/S33) | S33 — diameter-186 admissible 40-tuple | PARTIAL (tuple existence CONFIRMED; unconditional DHL[40,2] ⇒ H₁ ≤ 186 REFUTED) |
| [twin-prime-conjecture/S36](twin-prime-conjecture/S36) | S36 — internal "astra-186" construction | CONFIRMED (internal consistency only) |

### Unified Field Theory

| Path | Session | Verdict |
|------|---------|---------|
| [unified-field-theory/S55](unified-field-theory/S55) | S55 — Hessian coefficient D6, C2 bounds D7 | CONFIRMED |
| [unified-field-theory/validate-schmidt-magic-2026-09-07](unified-field-theory/validate-schmidt-magic-2026-09-07) | Schmidt magic faithfulness check | CONFIRMED |
| [unified-field-theory/validate-sre-monotonicity-2026-08-01](unified-field-theory/validate-sre-monotonicity-2026-08-01) | SRE monotonicity check | CONFIRMED |

### AI Alignment

| Path | Session | Verdict |
|------|---------|---------|
| [ai-alignment/S308](ai-alignment/S308) | S308 — Theorem PV.1-R privately-randomized exploration | CONFIRMED |

### Aging and Longevity

| Path | Session | Verdict |
|------|---------|---------|
| [aging-longevity/S239](aging-longevity/S239) | S239 — rentosertib proteomic-age claim | CONFIRMED (with discrepancy on headline magnitude and clock independence) |
| [aging-longevity/S244](aging-longevity/S244) | S244 — in vivo chemical reprogramming lipotoxicity claim | CONFIRMED (with discrepancy; VPA-exclusive framing refuted) |
| [aging-longevity/S246](aging-longevity/S246) | S246 — rentosertib peak-arm attribution | DISCREPANCY RESOLVED (headline claim weakened) |
| [aging-longevity/S257](aging-longevity/S257) | S257 — transcription-factor motif consensus | CONFIRMED WITH DISCREPANCY (USF1 motif partial) |

### Additional validated sessions (not yet linked from public pages)

These sessions are listed in the inventory as CONFIRMED, REFUTED, or PARTIAL and are kept for future page linking.

| Path | Session | Verdict |
|------|---------|---------|
| [aging-longevity/S245](aging-longevity/S245) | S245 — rentosertib pre-readout registry monitor | CONFIRMED (with discrepancy on headline framing) |
| [aging-longevity/S253](aging-longevity/S253) | S253 — EPI-321 comparator deltas | CONFIRMED (with discrepancy in press-release units/attribution) |
| [aging-longevity/S259](aging-longevity/S259) | S259 — motif consensus promoter exploration | PARTIAL |
| [climate-change-mitigation/session-103](climate-change-mitigation/session-103) | Session 103 — two-box calibration against Tyka et al. | CONFIRMED within ±10 percentage-point tolerance |
| [consciousness-hard-problem/S77](consciousness-hard-problem/S77) | S77 — externalized recurrence robustness across model families | CONFIRMED |
| [consciousness-hard-problem/S82](consciousness-hard-problem/S82) | S82 — relative-depth relay law at 24 layers | CONFIRMED (refutes fractional/relative-to-total-depth reading) |
| [consciousness-hard-problem/S85](consciousness-hard-problem/S85) | S85 — scale-allocation curve at pythia-1b | CONFIRMED |

## Security

No credentials, API tokens, database passwords, or private keys are committed to
this repository. Checker scripts that need external data read from fixtures
(`fixtures/*.csv`, `fixtures/*.json`) shipped alongside them. If you need to run
against a private database, supply connection parameters through environment
variables or an external config file that is ignored by `.gitignore`.

## License

- Code (checkers, scripts): MIT License (see `LICENSE`).
- Documentation and reports: CC-BY-4.0 (see `LICENSE-docs`).
