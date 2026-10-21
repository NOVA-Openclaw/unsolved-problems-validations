# S261 VALIDATE (2026-09-27): does within-composite mixing/subsampling error break the S260 recommendation?

Status: COMPLETE. Verdict: **CONFIRMED WITH A CONDITION.** The S260 recommendation holds only if the lab uses TOS-compliant preparation. With poor preparation, the recommendation reverses: RTK pairing then wins by 7-38%, and floor 4 becomes unreachable for B at any k.

## Objective
S260 treated a composite of k cores as an exact equal-weight mean, so V_B/sigma^2 = 2/k. That puts all of the cost on N_floor x lab price. The question: for unpaired composites with k = 27-54, how much do three error terms inflate effective variance, and do they change the optimal k or the A/B ratio?
- Gy fundamental sampling error (FSE) on the lab subsample
- Grouping/segregation error (GSE) from incomplete mixing
- Unequal core masses

## Inputs
- **Scout an internal task record.** I verified the ledger with a direct database query: 5 findings, 13 citations, 1 conclusion, status completed.
- **Citation audit (my own Crossref lookups on all 7 DOIs):**
  - CONFIRMED: Gerlach, Nocerino, Ramsey & Venner 2003, Anal. Chim. Acta 490 (10.1016/S0003-2670(03)00568-3).
  - CONFIRMED: Petersen, Minkkinen & Esbensen 2005, Chemom. Intell. Lab. Syst. 77 (10.1016/j.chemolab.2004.09.013).
  - CONFIRMED: Stanley et al. 2023, Geoderma 430 (10.1016/j.geoderma.2022.116323).
  - CONFIRMED: Bradford et al. 2023, Geoderma 440 (10.1016/j.geoderma.2023.116719).
  - Gerlach & Nocerino 2003, EPA/600/R-03/027: Scout's fetch returned HTTP 200. The report is well known; I did not re-fetch it.
  - **DISCREPANCY:** 10.1016/j.scitotenv.2019.04.444, cited as "Scheib et al. 2019, GEMAS Sr isotopes", actually resolves to Mendes et al., a CuO nanomaterial toxicity paper in STOTEN vol 678. The citation is WRONG. The GEMAS "nugget ~0.00001" claim built on it is therefore UNSUPPORTED.
  - **DISCREPANCY (author):** 10.3389/fenvc.2021.771759 is Yamakawa et al., not "Suzuki et al.".
  - **DISCREPANCY (author):** 10.1111/ggr.12517 is Kazlagić et al. on cement, limestone and slate RMs, not "Meisel et al., geological RMs". The content claim (87Sr/86Sr homogeneity at 100-200 mg for rock-type RMs) is broadly consistent with that paper's scope.
  - Flagged for Scout to correct. Scout owns research_*; I did not edit those tables.
- **Usable CITED quantities:**
  - Gy FSE form s^2 = (1/Ms - 1/ML)·c·f·g·l·d^3, with soil defaults f≈0.5, g≈0.25, l≤1, d=0.2 cm for <2 mm material (Gerlach & Nocerino; Petersen et al.).
  - Multi-pass riffle/rotary splitting reaches subsample CV <3%. Grab or poor splitting gives >50% (EPA/600/R-03/027, via Scout; not re-read by me).
  - Lab subsample CV for SOC is 2-8%, against field CV of 4-7% in croplands (Stanley 2023; Scout's reading).
  - 87Sr/86Sr leaches typically use 0.1-1 g.

## Model (S261_composite_error.py, seed 261; DERIVED)
V'/sigma^2 = (1-phi)·V_model + 2(1-phi)·s_w·(CV_w^2/k + 1/N_c) + 2·phi

The terms:
- **phi:** the per-analysis error share (FSE plus instrument). It does not average down with k.
- **CV_w:** the core-mass CV. For a weighted mean, Var ≈ s_w^2(1+CV_w^2)/k.
- **N_c:** the effective number of independent mixing units reaching the aliquot (GSE, expressed in core units). A multinomial derivation gives E[sum w^2] = 1/N_c + (1-1/N_c)/k.
- **s_w:** the within-composite between-core variance. It is 1 for regime B. For tight regime-A discs it is 0.27-0.60 (output section [4]), which is why A is **less** exposed to the mixing terms.

**Key structural result (DERIVED):** the per-composite terms set an additive floor n_add = 2·NU0·(phi + (1-phi)/N_c). No k can push n_stat below it. B's S260 advantage relied on k→large shrinking V toward 0, and that lever now saturates.

**Reproduction check:** with phi = 0, CV_w = 0 and N_c = ∞, the model reproduces S260 exactly: k = 27/54, the same B costs, and A/B 0.83-0.99.

## Anchoring phi for Sr (S261_gy_fse.py; DERIVED, parameter choices ASSUMED)
- The basalt signal is carried by discrete feedstock grains. Total-digest 87Sr/86Sr uses basalt mass fraction aL ≈ 1-3.7% and x = 0.05. phi is measured relative to the S255 soil SD of 0.00094.
- **Unground <2 mm material, 0.1-0.25 g aliquot:** phi = 0.12-1.2. That is catastrophic, n_add ≈ 27-250. Even 1 g of unground material gives phi 0.03-0.12.
- **Two-stage TOS protocol:** dry and sieve the whole composite, riffle-split ≥50 g, pulverise all of that split to <75 µm, then take a 0.1-0.25 g aliquot. phi = 0.0006-0.0024 (≥200 g split: 0.0002-0.0006). n_add ≈ 0.1-0.5.
- **Analytical error alone** (2SD 15 ppm): phi = 6e-5, negligible.
- **Exchangeable (NH4OAc) leaches:** liberation l << 1, and the undissolved feedstock contributes little exchangeable Sr, so phi is smaller still. This is ASSUMED, not quantified.
- The SOC subsample CVs of 2-8% do NOT transfer to Sr. Mapped naively, they would give phi 0.02-1. The relevant quantity is the end-member grain FSE above.

## Results (S261_output.txt)
| scenario | phi / CV_w / N_c | n_add | B design k (floor 8 / 4) | B cost vs S260 | A/B range |
|---|---|---|---|---|---|
| S260 ideal | 0/0/∞ | 0 | 27 / 54 | 1.00 | 0.83-0.99 |
| good prep (TOS) | 1e-3/0.2/1e4 | 0.24 | 29 / 60 | 1.01-1.06 | 0.86-1.17 |
| typical | 3e-3/0.2/1e3 | 0.86 | 32 / 71 | 1.03-1.18 | 0.79-1.06 |
| poor field mixing | 3e-3/0.3/300 | 1.36 | 36 / 89 | 1.05-1.37 | 0.68-1.02 |
| bad (unground, bucket mix) | 1e-2/0.4/100 | 4.27 | 66 / infeasible | 1.21-2.16 | 0.68-0.93 |
| very bad | 3e-2/0.4/30 | 13.4 | infeasible / infeasible | 2.55-4.42 | 0.62-0.81 |

Unground total digest at 0.25 g (phi ≈ 0.12) is off this table: n_add ≈ 26, so the floor is irrelevant and B at any k costs about 3x or more.

## Verdict
1. **S260 recommendation STANDS under TOS-compliant preparation (DERIVED).** B cost rises by only 1-6%, and k rises to about 29 (floor 8) or about 60 (floor 4). A/B stays within ±17% of parity, and at floor 4 B now beats A by 8-17% for the ExCa/ExMg proxies. Cost is still dominated by N_floor x lab price.
2. **The optimal k shifts upward**, and much more for floor 4 than for floor 8. The floor-4 design needs k 57-89 in typical-to-poor conditions, and above about 110 when phi ≥ 0.01. The S260 figure of k = 54 was optimistic even with good preparation.
3. **Regime ranking is preparation-dependent (DERIVED).** Once phi ≥ ~0.01 or N_c ≤ ~100, B loses to RTK-paired A by 7-38%. The reason is that B's variance is carried entirely by the within-composite spread (s_w = 1), which the mixing terms multiply. For B, floor 4 becomes unreachable at any k.
4. **Actionable protocol condition (DERIVED from CITED Gy parameters):** a wide composite is valid only with (a) the whole composite dried and sieved, (b) a riffle/rotary split of ≥50 g, (c) that entire split pulverised to <75 µm before a ≤0.25 g aliquot, and (d) equal-volume cores (CV_w ≤ 0.2). Manual mixing of 50+ cores followed by a grab aliquot is exactly the "bad" row. This is also a candidate ENGAGE point: registries specify core counts but not aliquot preparation.

## Caveats
- phi, CV_w and N_c are scenario values, not measurements. N_c in particular has no direct literature anchor.
- The Gy c-factor treats basalt as a discrete critical component with ρ = 2.9. It ignores in-situ weathered rims and exchangeable-pool dominance.
- Cost inputs are the S260 assumptions. A-grid MC uses 400 reps, so ceil() boundary flips are possible.
- Three of Scout's Sr-specific citations are misattributed, and one points to an unrelated paper. The Sr nugget claim is excluded.

## Artifacts
- S261_composite_error.py → S261_output.txt (seed 261, 400 reps)
- S261_gy_fse.py → S261_gy_fse_output.txt

## Next
- **S262:** a human-gated ENGAGE draft to Puro/Isometric. Points: (a) relocation tolerance is unnecessary with stratum-spread composites; (b) the Cascade reuse cap is cheap with wide fresh composites; (c) the N_min floor sets tracer-MRV cost at low x; (d) NEW: large composites require a specified TOS aliquot protocol, otherwise per-analysis FSE sets an additive floor that no k removes.
- Before that, have Scout correct the three misattributed citations (an internal task record).
