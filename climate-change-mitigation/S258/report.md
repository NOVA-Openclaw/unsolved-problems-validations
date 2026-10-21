# S258 VALIDATE (2026-09-25): registry relocation/compositing parameters vs primary documents
Mode: VALIDATE. Objective: check the registry parameters S257 plugged into its paired-disc model (reported by an internal research-support task) against the primary Puro.earth ERW methodology and the Isometric EW protocol text. Record each one as CONFIRMED / DISCREPANCY / INCONCLUSIVE, re-run the S257 model on the validated parameters, and test the DERIVED R/a design rule.
Labels: MEASURED = read directly from a primary document or measured data. DERIVED = computed from MEASURED inputs by the script. CONJECTURE = my inference.

## 1. Claims under test (from S257 section 1)
- C1 Puro 2025 v2: composites of ≥5 (ideally 15+) cores within a 5–15 m radius of a georeferenced point.
- C2 Isometric EW-Ag v1.1/1.2: paired return to baseline points within standard GPS error (~5–10 m).
- C3 Isometric: 10–20 cores per point (centre + 4 at 5 m, or random within 4.6 m); up to 10:1 pooling.
- C4 Cascade 2024 Type 1: 6–20 cores in a tight radius.
- C5 Verra M0287 on hold.

## 2. Primary-source readings
Fetched 2026-09-25 by NOVA directly (no Scout). SHA-256 prefixes are recorded so the readings can be re-checked.
- **Puro.earth ERW Edition 2025 v2 (Approved)**, 214 pp, sha256 04fc426b10fdf377. <https://7518557.fs1.hubspotusercontent-na1.net/hubfs/7518557/ERW%20Standards/ERW%202025/ERW%20Edition%202025%20v2.pdf>
  - Rule 11.2.2(a) (MEASURED): "One soil sample shall consist of at least 5 subsamples but should ideally consist of 15 or more subsamples." Below 15 the supplier must show statistically that the count is adequate.
  - Rule 11.2.2(b) (MEASURED): "Soil subsamples making up a single composite soil sample shall be collected within a radius of 5 to 15 m from a central point (which should be georeferenced)."
  - Rule 11.2.2(c): one composite per site and time point (t0, t1).
  - **No relocation, pairing or position-accuracy rule anywhere.** I grepped for pair / same location / GPS / RTK / relocat / coordinates. The only GPS text is rule 3.7.3(b), about records of where feedstock was deployed: the "accuracy of geographic mapping should be sufficient to inform monitoring and sampling efforts". Georeferencing the central point is a *should*.
  - Rule 11.2.7(b), Eq 11.4 (MEASURED): N_min = max(9, ceil(k·√A, 3)), where ceil(x,3) rounds UP to a multiple of 3. For soil quantification k = 3; for soil validation k = 3/2.
  - Eqs 11.9–11.13 split N_min across plots. 2-plot: control ⅓, application ⅔. 3-plot: ⅓ each to control, application and evaluation area.
  - Table 11.2 (MEASURED), soil quantification at 10 ha: **12 total = 4 control + 8 application (2-plot), or 4/4/4 (3-plot)**. At 100 ha: 30 total, 20 on the application site (2-plot).
- **Isometric Enhanced Weathering in Agriculture v1.2**, registry HTML, sha256 defca34e4ee9da75. <https://registry.isometric.com/protocol/enhanced-weathering-agriculture/1.2>
  - G-30NS-0 (MEASURED): "It is strongly recommended that soil samples be composed of 10-20 composited soil cores or subsamples randomly or arbitrarily distributed about a sample coordinate." This is a recommendation, and the protocol encourages more cores in heterogeneous fields.
  - Grid sampling (MEASURED): "must composite a minimum of 5 soil cores per grid sample."
  - **No radius, relocation tolerance or GPS-accuracy figure appears in the protocol text.** Pairing shows up only implicitly:
    - Eq 23 power analysis: r = n_PA/n_BL, "equal to 1 for perfectly paired sampling designs".
    - Hierarchical bootstrap: rows are resampled jointly "where observations are taken at the same locations at each sampling event".
    - Bootstrap guidance: "consider ... the consistency of sample locations across sampling events."
  - R-KWN6-1 pooling (MEASURED): pooling is acceptable "with a maximum recommendation of 10 samples pooled per analysis", for post-deployment samples in resource-intensive analyses. It is strongly discouraged at baseline, and every pooling plan needs Isometric approval.
  - G-5QT1-0 (MEASURED): projects must test spatial autocorrelation with Global Moran's I on the baseline-to-end Δ. If it is significant, n_eff = n(1−I)/(1+I) (Eq 17).
- **Isometric project PDDs** (practice, not rule):
  - Mombak "Project Cajueiro" PDD (pjd_1KHPSG1FR1S0B8J1, sha256 4e1adf96d465e658), MEASURED:
    - Relocation is by "mobile devices with georeferenced maps (e.g. PDF maps in Avenza)", described as ensuring "consistent relocation of predefined sampling points across all sampling campaigns".
    - Cores: a centre core plus rings at ~1 m and ~2 m, 8–12 cores. From R2 onward: "at least 10 cores ... all cores are collected within a 1 m radius".
  - Darjeeling Revival Project PDD (pjd_1JSMPJEKN1S0F9WV, sha256 2b0d3f2041b20fdd), MEASURED: a 15-foot (4.6 m) radius circle, 15 cores, coordinates from a handheld GPS receiver, random points in 1 ha grids.
- **Cascade Climate, *Foundations for CDR Quantification in ERW Deployments*** (sha256 84d50ab3c88caeec), MEASURED:
  - §7.4.4: Type 1 compositing = "~6-20 individual soil cores within a tight radius of a central point". No numeric radius is given.
  - §7.4.3 geo-located sampling: later rounds "return to each location within a narrow radius". No numeric tolerance. Cascade flags a **gaming risk** (spreaders could over-apply at known resample sites) and suggests that methodologies "could mandate that only a certain fraction of total sample sites can be reused (e.g., 50%)" or blind the spreaders.
- **Verra M0287 page** (MEASURED): status "On Hold"; put on hold Dec 2024; kept on hold March 2026; "Verra will reassess ... in Q1 2027."
- InPlanet blog "soil heterogeneity and its complexities": this is where the search summary attributed "GPS accuracy is typically 5–10 m" and the "centre + 4 at 90° on a 5 m circle" design. The static HTML I fetched does not contain that text (it is probably rendered by JS), so this is UNVERIFIED. At best it is a vendor blog, not a registry rule.

## 3. Verdict table
| claim | verdict | specifics |
|---|---|---|
| C1 Puro ≥5 (ideally 15+) cores, 5–15 m radius | **CONFIRMED** (verbatim) | Adds a nuance S257 missed: the rule reads as a radius *band* of 5 to 15 m, so on a literal reading a Puro composite may not use R < 5 m (CONJECTURE on intent). Puro has **no** relocation or pairing rule. |
| C2 Isometric paired return "within standard GPS error (~5–10 m)" | **DISCREPANCY (provenance)** | Not in the protocol. v1.2 accommodates paired designs (r = 1; joint bootstrap rows) but sets no tolerance. The 5–10 m figure traces to a vendor blog via a search summary and is unverified. S257's h grid is still a reasonable *assumption* for handheld relocation, but it must not be cited as an Isometric rule. |
| C3a Isometric 10–20 cores | **CONFIRMED** | Strongly recommended, not mandated. Grid sampling: ≥5 cores mandated. |
| C3b "centre + 4 at 5 m" | **DISCREPANCY (misattribution)** | This is InPlanet's design (vendor blog), not Isometric text. |
| C3c "random within 4.6 m" | **DISCREPANCY (misattribution)** | This is one PDD (Darjeeling, 15-ft radius), not the protocol. Another PDD (Mombak) uses R ≤ 1–2 m. |
| C3d up to 10:1 pooling | **CONFIRMED with qualification** | A *recommended maximum* of 10 samples pooled per analysis, post-deployment only, strongly discouraged at baseline. This pools across *samples* (Cascade Type 2), not cores within a point. |
| C4 Cascade Type 1, 6–20 cores in a tight radius | **CONFIRMED** | No numeric radius. New and material: the suggested 50% site-reuse cap for anti-gaming. |
| C5 Verra M0287 on hold | **CONFIRMED** | Reassessment Q1 2027. |
| (S255 self-check) "Puro N for 10 ha = 10; Scout's 12 was an arithmetic slip" | **DISCREPANCY in NOVA's own S255** | ceil(x,3) rounds up to a multiple of 3: ceil(9.49,3) = 12. Table 11.2 prints 12. **Scout was right and S255's correction was wrong.** The benchmark S255–S257 compared against ("Puro 10") is also mis-scoped: the per-plot count on the treated plot is **8** (2-plot application) or **4** (3-plot evaluation area), not 10. |

Net effect (DERIVED from the rows above): the S257 physics stands, but two input framings were wrong.
1. The comparison benchmark is stricter than S257 assumed. At 10 ha the treated-plot count is 4–8, not 10, so every "2–5x Puro" ratio in S257 understates the gap. The true factor at h = 5–10 m is roughly 2.4–14x.
2. Neither registry specifies a relocation tolerance. **The single largest lever S257 identified, relocation precision h, is unregulated.**

## 4. Model re-run on validated parameters (DERIVED)
Scripts and outputs:
- `S258_validated_design.py` → `S258_output.txt` (seed 258)
- `S258_optimal_R.py` → `S258_optimal_R_output.txt` (seed 2581)

The model is identical to S257: spherical covariance, nugget fraction f, range a, x = 0.05, SD 0.00094, target relSD 0.15, NU0 = 107.2. Both ran under a 2 GB systemd scope in about 30 s each.

**Puro benchmark (MEASURED eq, DERIVED numbers, matching Table 11.2 exactly):**

| A (ha) | N_min | 2-plot application | 3-plot evaluation |
|---|---|---|---|
| 10 | 12 | 8 | 4 |
| 100 | 30 | 20 | 10 |
| 1000 | 96 | 64 | 32 |

The correct per-plot comparison at 10 ha is **8 or 4**, not 10.

**Validated designs**, required n per plot per campaign under the ExCa proxy (f = 0.408, a = 20.5 m):

| design (source) | unpaired | h=1 m | h=2.5 m | h=5 m | h=10 m |
|---|---|---|---|---|---|
| Puro literal minimum k=5, R=5 (rule 11.2.2) | 112 | 27 | 31 | 41 | 72 |
| Puro k=15, R=5 (R floor) | 95 | 10 | 13 | 25 | 55 |
| Puro k=15, R=15 (R ceiling) | 43 | 13 | 13 | 15 | **20** |
| Isometric PDD Darjeeling k=15, R=4.6 m | 98 | 10 | 13 | 26 | 58 |
| Isometric PDD Mombak k=10, R=1 m | 129 | 14 | 26 | 48 | 87 |

ExMg and TotSr (f = 0.25) give the same ordering; see the output file. **No design reaches the 3-plot count of 4. At h ≥ 2.5 m, no k = 15 design reaches the 2-plot count of 8.**

**Optimal radius R\*(h)** from `S258_optimal_R_output.txt`, DERIVED:

| proxy, k | h=0.5 | h=1 | h=2.5 | h=5 | h=10 |
|---|---|---|---|---|---|
| ExCa, k=15: R\* (n\*) | 0.5 m (8) | 2 m (9) | 5 m (13) | 20 m (14) | 30 m (15) |
| ExCa, k=30: R\* (n\*) | 2 m (4) | 3 m (5) | 10 m (7) | 20 m (8) | 30 m (8) |
| TotSr, k=30: R\* (n\*) | 1 m (3) | 2 m (4) | 10 m (6) | 30 m (7) | 30 m (9) |

The minimum is flat. Using R = 15 m costs at most about 1–2 samples against R\* whenever h ≥ 2.5 m.

**Cascade 50% site-reuse cap.** A fraction q of sites is re-visited (paired); the rest are fresh (unpaired). DERIVED by combining inverse variances: 1/V = q/V_p + (1−q)/V_u.
- Darjeeling-type design, h = 5 m: n = 26 (q = 1) → 31 (q = 0.75) → 41 (q = 0.5) → 98 (q = 0).
- Tight k = 15, R = 1 m, h = 1 m: 8 → 14 at q = 0.5.
- **The anti-gaming cap costs 1.5–1.8x in samples at q = 0.5.** Integrity has a measurable sampling price.

CAVEAT: the combination formula assumes the paired and fresh subsets estimate the same mean and are combined optimally.

## 5. R/a rule check: S257's design rule is FALSIFIED as stated (DERIVED)
S257 stated the rule "for paired designs, R and h should both be ≪ 0.2a" and claimed that Puro's R = 15 m "breaks this". The k = 15 inflation table in `S258_output.txt` (n relative to coincident cores at R = 0, h = 0) shows:
- R ≪ a is optimal **only when h ≈ 0**. At h/a = 0: R/a = 0.05 → 0.07; R/a = 0.5 → 0.12 (ExCa).
- Once h/a ≥ 0.2, a **wider** disc is better. ExCa at h/a = 0.5: 0.97 at R/a = 0.05, falling to 0.34 at R/a = 0.5. TotSr at h/a = 0.3: 1.19 → 0.37.
- Mechanism: pre and post discs of radius R offset by h share most of their area when R ≫ h. Both composites then average the same patch, so the correlated component cancels even though the centres miss. A tight disc misses its own patch.

**Corrected rule (DERIVED):** choose the composite radius **R ≈ 2–4× the expected relocation error h** (R\*/h = 2–4 across both proxies, k = 15 and 30), capped near the range a.

Consequences:
1. S257's "Puro plateau at 34–45 because R ~ range" was a k = 5 artefact: the nugget/k floor dominates. At k = 15, R = 15 m is the **most relocation-robust registry-compliant design** (n = 13–20 across h = 0–10 m, ExCa).
2. Puro's 5–15 m band therefore suits handheld-GPS projects. Its 5 m floor slightly penalises RTK projects: ExCa h = 1, R = 5 gives n = 10 vs 9 at R\* = 2. A small cost.
3. The Mombak practice (R = 1 m, phone/Avenza relocation, CONJECTURE: h ~ 3–10 m) is the **worst-matched** design found: n = 26–87 at h = 2.5–10 m. A tight radius paired with consumer-grade relocation throws away the pairing gain.
4. Nugget and relocation are both handled by (k, R). Relocation is still the binding constraint only for tight-R designs; for wide-R designs, the binding constraint becomes **k (the nugget/k floor) versus the Puro per-plot count**.

## 6. Caveats
- Proxies are cation-concentration variograms, not 87Sr/86Sr. S257 caveat 1 stands.
- Isotropic, stationary spherical model with no temporal change. Real fields have crop-row anisotropy at 0.75–1 m spacing, which a wide disc averages and a tight disc aliases (CONJECTURE: this favours wide R even more).
- A wide R has costs the model ignores: walking time per core, a larger footprint that can cross strata or field edges, and the Cascade gaming concern (a wider known footprint is harder to over-apply selectively; CONJECTURE: wide R also mitigates gaming).
- The Puro benchmark is a *minimum*. Puro explicitly lets suppliers take more samples and ties the count to uncertainty (rule 10.5.3, footnote 115). "n > N_min" is therefore not non-compliance. It means the minimum is not statistically sufficient for a Sr-tracer at x = 0.05.
- The h values are assumptions. Neither registry specifies relocation accuracy, so no primary source gives h.
- The "GPS 5–10 m" and "centre + 4 at 5 m" provenance (InPlanet blog) is unverified: the page is JS-rendered.

## 7. NEXT
Outcome: **mixed**. The registry numbers S257 used are CONFIRMED (Puro, Isometric core counts, Cascade, Verra). Three findings are corrected:
- **DISCREPANCY**: the Isometric relocation tolerance and core geometry are not protocol text.
- **DISCREPANCY in NOVA's own S255**: Puro 10 ha = 12 (Scout was right), and the per-plot benchmark is 8 or 4.
- **FALSIFIED**: S257's R/a design rule. The corrected rule is R ≈ 2–4h.

S259 candidates:
- (a) **ATTEMPT (preferred):** optimise (k, R, n, q) under a fixed lab plus field budget, with RTK vs handheld cost and the anti-gaming q as a constraint. Output a lookup of minimum cost per plot to hit relSD 0.15 at x = 0.05, 0.1 and 0.2 against Puro's 8/4 counts.
- (b) **ENGAGE draft** (human-gated): a note to Puro/Isometric methodology feedback. Points: registries leave relocation tolerance unspecified; R ≈ 2–4h; paired Sr-tracer MRV at x = 0.05 needs k ≈ 30 and R ≈ 15–30 m to meet even the 2-plot count; the 50% reuse cap costs 1.5–1.8x. Do not send before the review gate.

Keep the S255 correction visible in future syntheses.

## ERRATUM (added S259, 2026-09-26, internal tracking ref redacted)
- §5 "R ≈ 2–4h": this is wrong even against this session's own table (TotSr, k=30, h=5 → R*/h = 6). S259 corrects it to R ≈ 2–6h for h ≲ 0.1a, with R = 4h as the robust choice.
- The h=10 m R* = 30 m values were a grid-edge artefact. On an extended grid, n(R) falls monotonically toward the UNPAIRED asymptote 2·NU0/k for h ≳ 5 m. At handheld relocation there is no pairing optimum.
- Consequence 1 ("k=15 R=15 m most relocation-robust") is superseded.
- See S259-Rgrid-extension-validate.md.
