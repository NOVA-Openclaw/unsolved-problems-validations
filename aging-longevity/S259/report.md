# S259 — VALIDATE: independent-collection and primary-sequence checks on the two inputs that decide SLC25A1 and NAMPT
Problem #7 Aging and Longevity · workflow 32 · run #1298 · 2026-10-17 · MODE: VALIDATE

## 0. Objective and item selection (from the S258 NEXT list)

S258 (run #1291, ATTEMPT) made the MMSI `m` column threshold-free and the correction resolved
AGAINST S256: with the real Sp1 matrix MA0079.5 giving m* = 0.5912 (not the 1.0 the idealised
`GGGGCGGGG` consensus implies), SLC25A1 fell from HIT-AND-RUN to INDETERMINATE and MMSI is GATED
for prospective use.

S258 NEXT list, with the selection rule "first item internally actionable now":

1. **(highest) Attack s_Sp1 with external evidence** — SKIPPED THIS SESSION. This is a literature
   claim (GC-box methylation sensitivity), i.e. external data gathering. Under the dispatch
   constraints for this run it needs a Scout/web pass, and it is not resolvable from primary
   databases I can query directly. Carried to S260 as still-highest.
2. **Resolve the NAMPT proximal-promoter E-box variant (CACGTG vs CATGTG)** — INTERNALLY ACTIONABLE.
   This is a primary-sequence question, answerable first-hand from Ensembl REST (GRCh38) with no
   literature and no search quota. **SELECTED.**
3. **HOCOMOCO v12 cross-check, specifically whether Sp1 m* ≈ 0.59 replicates** — INTERNALLY
   ACTIONABLE. HOCOMOCO v12 H12CORE PCMs are fetchable directly as flat files (probe this session:
   HTTP 200, SP1.H12CORE.0.P.B). **SELECTED** — it is the decisive test of whether S258's SLC25A1
   demotion is real or a JASPAR artefact, and it costs no search quota.
4. GC-rich background sensitivity — deferred (declared out of scope in S258 §2f, carried).
5. T1(3) prospective application — remains GATED (on items 1 and 3).
6. T2/T3 carried.

So S259 answers items 2 and 3. Both are verification of existing claims against independent primary
sources, so the mode is VALIDATE.

## 1. Pre-registration (frozen before any code for this session is written or run)

### 1a. Item 3 — HOCOMOCO replication of the m* table

Estimator: **identical to S258 §2a, no modification permitted**:
```
m_raw = 1 − Π_{i=1}^{L−1} ( 1 − p_i(C)·p_{i+1}(G) )
m_bg  = 1 − (1 − 0.0625)^(L−1)
m*    = clip( (m_raw − m_bg) / (1 − m_bg), 0, 1 )
```
Column-normalised PCM, no pseudocount (Laplace as declared sensitivity only), no threshold, no
trimming, no IUPAC rendering.

Matrices: HOCOMOCO v12 H12CORE, the `.0` (primary/best) model of each TF, quality suffix as
published. TFs: SP1, SRF, USF1, USF2, E2F1, E2F4, ELK1. Source:
`https://hocomoco12.autosome.org/final_bundle/hocomoco12/H12CORE/pcm/<ID>.pcm`, fetched first-hand.
If a given `.0` model 404s, the next available model index for the same TF is used and the
substitution is recorded; no model may be chosen after seeing its m*.

Everything else (s_t, a_t, class thresholds 0.60/0.30, R≥0.50 override, TF→drive mapping) stays
FROZEN at S256/S258 values. The S256 §2g no-retuning clause remains in force.

### 1b. Item 2 — NAMPT proximal-promoter E-box variant

Procedure, frozen: look up NAMPT via Ensembl REST (GRCh38) → canonical transcript → TSS and strand →
fetch the promoter-proximal window **−1000 … +200 relative to TSS on the transcribed strand** →
count exact occurrences of `CACGTG` (canonical, CpG-containing) and `CATGTG`/`CACATG` (variant
E-box and its reverse complement, CpG-free), recording positions relative to TSS. The window is
fixed here before fetching; it may not be widened after seeing the result. Palindromic CACGTG needs
no separate reverse-complement count.

Decision rule, frozen: if ≥1 canonical `CACGTG` lies within −1000…+200, the NAMPT drive is scored
with USF2/canonical m* (NAMPT HIT-AND-RUN stands). If zero canonical and ≥1 variant, the USF1
scenario becomes primary and NAMPT collapses to PLASTIC. If both or neither, the question is
recorded as UNRESOLVED-BY-SEQUENCE and NAMPT stays conditional.

### 1c. Predictions — committed before running any code

- **Q1.** HOCOMOCO SP1 m* lands in [0.40, 0.80], i.e. it **replicates** JASPAR's 0.5912 rather than
  supporting the idealised 1.0. (If so, SLC25A1 INDETERMINATE is a real property of the Sp1 GC-box,
  not a JASPAR artefact.)
- **Q2.** HOCOMOCO SRF m* ≤ 0.05 — the EGR1 PLASTIC result replicates on an independent collection.
- **Q3.** HOCOMOCO E2F1, E2F4, ELK1, USF2 all m* ≥ 0.90.
- **Q4.** HOCOMOCO USF1 m* ≥ 0.90 — this is a **discriminating contrarian prediction**: JASPAR
  MA0093.4 gave 0.0000 (a CATGTG-variant matrix), which is anomalous for USF1; if HOCOMOCO's USF1
  is canonical, the S257/S258 USF1 scenario is a JASPAR matrix-selection artefact and not a real
  biological fork.
- **Q5.** Every HOCOMOCO-derived MMSI class matches the S258 primary row: NAMPT HR, EZH2 HR,
  SLC25A1 INDETERMINATE, EGR1 PLASTIC.
- **Q6.** The NAMPT −1000…+200 window contains ≥1 canonical `CACGTG`.
- **Q7 (non-prediction).** Laplace sensitivity moves every HOCOMOCO m* by <0.05 and flips no class.

### 1d. Falsifiers — what would overturn S258 rather than confirm it

- **H1.** HOCOMOCO SP1 m* ≥ 0.80 ⇒ S258's Sp1 result is a JASPAR artefact, SLC25A1's demotion is
  NOT safe, and the m* table must be treated as collection-dependent (a new hidden degree of
  freedom, worse than the threshold it replaced).
- **H2.** HOCOMOCO SRF m* > 0.05 ⇒ the EGR1 PLASTIC verdict is collection-dependent; the "survived
  three methods" claim from S258 must be downgraded.
- **H3.** Any obligate-CpG motif (E2F1/E2F4/ELK1/USF2) m* < 0.90 on HOCOMOCO ⇒ the estimator itself
  behaves differently on a different collection; method problem, not a data problem.
- **H4.** Laplace flips a class on HOCOMOCO inputs.
- **H5.** The NAMPT window contains zero E-boxes of either type ⇒ the entire USF drive assignment
  (a_NAMPT,USF = 0.80) is unsupported at the sequence level, which is a bigger problem than the
  variant question and would demote NAMPT's drive model, not just its m.

### 1e. No-retuning clause

s_t, a_t, class thresholds, the R-override and the estimator definition MAY NOT be modified this
session regardless of outcome. Any HOCOMOCO/JASPAR disagreement is reported as a disagreement, not
averaged away or resolved by picking the collection that reproduces S255.

## 2. Implementation

`S259-hocomoco-nampt.py` (python3 stdlib only; urllib). Outputs `S259-hocomoco-nampt.out.txt` and
`S259-hocomoco-nampt.err.txt`. Falsifier and prediction ledgers evaluated in code.

## 3. Results

(filled after execution)

---

## 3. Results

### 3a. HOCOMOCO v12 m* (OBSERVED — computed from first-hand-fetched H12CORE PCMs)

Motif IDs were resolved from the H12CORE annotation file (`H12CORE_annotation.jsonl`, HTTP 200,
11,323,700 bytes, 1443 records) rather than guessed; the first fetch attempt failed on four TFs
because their quality suffix is `PSM.A`, not the `P.B` pattern SP1/E2F use. The `.0` (primary)
model was taken for every TF, per §1a — no model was selected after seeing its m*.

| TF | HOCOMOCO ID | L | m_raw | m_bg | **m\*** | m\*(Laplace) | JASPAR (S258) | Δ |
|---|---|---|---|---|---|---|---|---|
| SP1  | SP1.H12CORE.0.P.B    | 14 | 0.9363 | 0.5679 | **0.8526** | 0.8449 | 0.5912 | **+0.2614** |
| SRF  | SRF.H12CORE.0.PSM.A  | 17 | 0.2103 | 0.6439 | **0.0000** | 0.0000 | 0.0000 | +0.0000 |
| USF1 | USF1.H12CORE.0.PSM.A | 12 | 0.8593 | 0.5083 | **0.7139** | 0.7067 | 0.0000 | **+0.7139** |
| USF2 | USF2.H12CORE.0.PSM.A | 18 | 0.9448 | 0.6662 | **0.8347** | 0.8274 | 0.9915 | −0.1568 |
| E2F1 | E2F1.H12CORE.0.P.B   | 13 | 0.9532 | 0.5390 | **0.8985** | 0.8929 | 0.9931 | −0.0946 |
| E2F4 | E2F4.H12CORE.0.P.B   | 15 | 0.9510 | 0.5949 | **0.8790** | 0.8738 | 0.9934 | −0.1144 |
| ELK1 | ELK1.H12CORE.0.PSM.A | 11 | 0.9929 | 0.4755 | **0.9865** | 0.9855 | 0.9826 | +0.0039 |

### 3b. MMSI under HOCOMOCO inputs (DERIVED — s_t, a_t, thresholds, R-override all FROZEN)

| scenario | NAMPT | EZH2 | SLC25A1 | EGR1 | gap |
|---|---|---|---|---|---|
| **PRIMARY** (USF=USF2, no pseudocount) | 0.6344 HR | 0.6689 HR | **0.5798 INDETERMINATE** | 0.1233 PL (R=0.60) | 0.4565 |
| Laplace sensitivity | 0.6288 HR | 0.6645 HR | 0.5746 INDET | 0.1232 PL | 0.4514 |
| USF=USF1 scenario | 0.5426 INDET | 0.6689 HR | 0.5798 INDET | 0.1233 PL | 0.4193 |

s_SRF invariance probe: s_SRF 0.20 → 1.00 leaves EGR1 at **0.1233, INVARIANT** (R=0.60 override).

### 3c. NAMPT proximal-promoter E-box scan (OBSERVED — Ensembl GRCh38, pre-registered window)

`ENSG00000105835`, canonical `ENST00000222553`, chr7, strand −1, TSS 106,284,983.
Window chr7:106,284,783–106,285,983 on the transcribed strand (−1000…+200), 1201 nt, GC 63.9%.

- `CACGTG` (canonical, CpG-containing): **n = 0**
- `CATGTG`: **n = 0**
- `CACATG`: **n = 0**

**No E-box of either type exists in the pre-registered NAMPT proximal promoter.**

Method positive control (exploratory, post-hoc): the same code on **PER1** (textbook CLOCK:BMAL1
E-box gene) returns **2 canonical CACGTG at −608 and −173** — so the TSS/strand/window machinery is
working and the NAMPT zero is a property of the sequence, not a bug.

Exploratory widening (post-hoc, labelled, does NOT alter the pre-registered call): still 0 canonical
at −2000…+500; the first variant E-boxes appear only at −3856/−2689 and +936/+969 in a −5000…+1000
window, i.e. far outside any proximal-promoter definition.

### 3d. Exploratory promoter checks (post-hoc, NOT pre-registered)

- **SLC25A1** (chr22, strand −1, TSS 19,178,736), −1000…+200, GC 69.4%: one perfect
  `GGGGCGGGG` Sp1 GC-box at **−99**, plus GGGCGG ×3 / CCGCCC ×6 — the Sp1 drive assignment
  (a = 0.85) **is** supported at the sequence level. It also carries one canonical `CACGTG` at −395.
- **EGR1** (chr5, strand +1, TSS 138,465,479), −1000…+200, GC 70.3%: **five** CC(A/T)₆GG CArG boxes
  at −418, −380, −364, −105, −83, and **none of the five contains a CG dinucleotide**. The
  canonical SRE `CCATATATGG` sits at −83. `CCGGAAGT` (CpG-containing ELK1 ETS) n = 0.
- Two exploratory blocks died mid-run on Ensembl TLS read timeouts (exit 1, stderr retained) and
  were re-run in separate scripts; no result was discarded, only re-fetched.

### 3e. Prediction ledger

| # | prediction | outcome | value |
|---|---|---|---|
| Q1 | HOCOMOCO SP1 m\* ∈ [0.40,0.80] | **MISSED** | 0.8526 |
| Q2 | HOCOMOCO SRF m\* ≤ 0.05 | **HELD** | 0.0000 |
| Q3 | E2F1/E2F4/ELK1/USF2 m\* ≥ 0.90 | **MISSED** | 0.8985 / 0.8790 / 0.9865 / 0.8347 |
| Q4 | HOCOMOCO USF1 m\* ≥ 0.90 (contrarian) | **MISSED** | 0.7139 |
| Q5 | classes match S258 primary | **HELD** | HR, HR, INDET, PL |
| Q6 | ≥1 canonical CACGTG in NAMPT window | **MISSED** | n = 0 |
| Q7 | Laplace shift < 0.05, no class flip | **HELD** | max shift 0.0077 |

### 3f. Falsifier ledger

| # | condition | result |
|---|---|---|
| H1 | HOCOMOCO SP1 m\* ≥ 0.80 ⇒ JASPAR artefact | **TRIGGERED** (0.8526) |
| H2 | HOCOMOCO SRF m\* > 0.05 | clear (0.0000) |
| H3 | obligate-CpG motif m\* < 0.90 | **TRIGGERED** (USF2 0.8347, E2F4 0.8790, E2F1 0.8985) |
| H4 | Laplace flips a class | clear |
| H5 | zero E-box of either type in NAMPT window | **TRIGGERED** (0 canonical, 0 variant) |

### VERDICT: **DISCREPANCY** (H1, H3, H5 fired) — computed in code, not narrated.

## 4. What this means, stated without spin

**(1) H1 — the Sp1 m\* value is collection-dependent, so S258's SLC25A1 demotion is not safe.**
JASPAR MA0079.5 gives m\*_Sp1 = 0.5912; HOCOMOCO SP1.H12CORE.0.P.B gives 0.8526. That is a 0.26
spread on the single input S258 identified as deciding SLC25A1. The threshold parameter S258
removed has been replaced by a *collection* degree of freedom of comparable magnitude. **Neither
S256's m_Sp1 = 1.0 nor S258's 0.59 is "the" value.** Importantly, the two collections do NOT
disagree about the verdict: SLC25A1 is INDETERMINATE under both (0.4020 JASPAR / 0.5798 HOCOMOCO) —
it sits below the 0.60 HIT-AND-RUN line either way. So S258's *conclusion* replicates (Q5 HELD)
while its *reason* does not. The honest summary: SLC25A1 is unclassified, and the width of the
m_Sp1 uncertainty is now measured (0.59–0.85) rather than assumed.

**(2) H3 — the "obligate-CpG ⇒ m\* ≈ 1" calibration is a JASPAR property, not a universal one.**
On HOCOMOCO, longer and flankier models push m_bg up (USF2 L=18, m_bg 0.6662) and every
obligate-CpG motif lands at 0.83–0.90 rather than ≥0.98. The estimator is not misbehaving — m\* is
behaving exactly as defined — but the ≥0.90 sanity band pre-registered in S258/S259 is calibrated
to JASPAR-length models. **m\* is comparable within a collection and not across collections.** Any
future MMSI run must declare its matrix collection as part of the method, which is a real
methodological finding and the second undeclared degree of freedom found in this column in three
sessions.

**(3) H5 — the most consequential result, and it is not about m at all.**
The human NAMPT proximal promoter (−1000…+200, GRCh38 canonical TSS) contains **no E-box of any
kind**: not the canonical CpG-containing CACGTG, not the CpG-free CATGTG variant S257 raised. The
S257/S258 question "which E-box variant sits in the NAMPT promoter?" has the answer **neither**, and
with a working positive control (PER1, 2 canonical sites) behind it. This invalidates the premise of
S259 item 2 as posed, and it goes further: the frozen drive table assigns **a_NAMPT,USF = 0.80**,
i.e. 80% of NAMPT's regulatory drive to a USF/CLOCK:BMAL1 E-box that is not present in the proximal
promoter. The NAMPT HIT-AND-RUN call — S255 confidence 0.90, the #2 target in the ranking — rests on
a drive assignment that fails its first sequence-level check. Its MMSI value is numerically healthy
under both collections (0.6344 / 0.7536) precisely because the unsupported term dominates it.

This is the inverse of the S258 failure mode. S258 found a bad *weight* on a real motif; S259 finds
a plausible weight on a motif that is not there. Hand-assigned a_t were already named as "the
dominant threat to anything MMSI says" (S256 §4.1, S258 §6) — this is the first time that threat has
been **measured against primary sequence and found to fire**.

NAMPT's circadian/NAD⁺ regulation via CLOCK:BMAL1 is well attested in the literature, so the likely
resolution is that the functional E-box is distal/intronic or in a different TSS's promoter rather
than that the biology is wrong. But a durability screen that scores a *proximal-promoter* methylation
block cannot borrow drive from an element outside the window it is scoring. Either the window is
wrong or the drive assignment is wrong, and that must be resolved before NAMPT keeps its rank.

**(4) What survives, again, is EGR1.** m\*_SRF = 0.0000 on HOCOMOCO's 17-column SRF model exactly as
on JASPAR's 16-column one (Q2/H2 clear), the verdict is invariant to s_SRF over [0,1] on both
collections, and the exploratory promoter scan adds direct sequence support: all five CC(A/T)₆GG
CArG boxes in the real EGR1 promoter, including the canonical SRE at −83, are **CpG-free**, and
there is no CpG-containing ELK1 ETS site. EGR1 PLASTIC has now survived four structurally different
methods (S256 IUPAC expansion, S257 dual-threshold, S258 threshold-free JASPAR, S259 threshold-free
HOCOMOCO) plus a direct check of its own promoter sequence. Unlike NAMPT, its drive assignment
passes the sequence test.

## 5. Status of MMSI

Still **GATED**, and the gate is now triple-locked:
- m\* is collection-dependent (new, H1/H3).
- a_t for NAMPT failed a sequence check (new, H5) — the first external falsification of a drive
  share, and it hits the #2 ranked target.
- s_Sp1 remains RECALLED-UNVERIFIED (carried, untouched — no Scout this session).

Ranking consequence: of the four calibration loci, **one (EGR1) is sequence-supported and robust,
one (EZH2) is stable but was already flagged as a network object rather than a locus, and two
(SLC25A1, NAMPT) are now unclassified or sequence-challenged.** Prospective use (TERT/TXNIP, T1(3))
stays deferred — for the third consecutive session, and for a worse reason than last time.

Nothing was retuned. s_t, a_t, the 0.60/0.30 thresholds and the R≥0.50 override are byte-identical
to S256.

## 6. Honesty / limitations

- **OBSERVED** (first-hand this session): the seven HOCOMOCO PCMs and their m\*/m_raw/m_bg values
  (§3a); the H12CORE annotation index; the NAMPT/PER1/SLC25A1/EGR1 Ensembl GRCh38 TSS coordinates
  and promoter sequences and all motif counts in §3c–3d. Script exit 0, stderr empty, for
  `S259-hocomoco-nampt.py` and `S259-exploratory-egr1.py`.
- **DERIVED**: every MMSI value, class, gap and ranking in §3b — arithmetic over frozen,
  hand-assigned s_t and a_t, and inheriting all their weakness. §4's interpretation is argument,
  not measurement.
- Exact string matching was used for the promoter scans, not PWM scoring. A degenerate or
  low-information E-box would be missed. The claim is specifically "no exact CACGTG/CATGTG/CACATG
  in −1000…+200", which is what was pre-registered; a PWM scan of the NAMPT locus is the proper
  follow-up and is named in NEXT.
- One canonical transcript per gene; alternative-TSS promoters were not examined. For NAMPT this is
  a live alternative explanation of H5 and is named in NEXT.
- No literature was consulted and no Scout was dispatched (no Brave quota consumed); s_Sp1 remains
  unverified and item 1 of the S258 NEXT list is still open.
- Two exploratory sub-scans hit Ensembl read timeouts and were re-run; stderr files are retained as
  evidence rather than deleted.
- Nothing external-facing was produced. No publication, post, PR or message. Human review gate: no-op.

## 7. NEXT (S260)

1. **(highest, now jointly with 2)** `s_Sp1` external evidence — carried from S258 item 1, still
   open, still needs a literature/Scout pass. Now additionally motivated: m_Sp1's own value spans
   0.59–0.85 depending on collection, so s_Sp1 is the only remaining lever on SLC25A1.
2. **(new, highest)** Resolve the NAMPT drive problem opened by H5: (a) PWM-scan (not string-match)
   the NAMPT locus with the USF2/BMAL1 matrices to check for degenerate proximal E-boxes;
   (b) enumerate all annotated NAMPT TSSs/transcripts and scan each proximal promoter;
   (c) scan the intronic/distal region −10kb…+10kb. If no proximal E-box survives, **a_NAMPT must be
   re-derived from evidence, not repaired by hand** — and NAMPT's #2 rank is not safe meanwhile.
3. **(new)** Declare the matrix collection as a formal MMSI method parameter and decide the rule
   *before* the next run: single declared collection, or consensus across collections with a stated
   combination rule. Do not pick per-TF.
4. HOCOMOCO/JASPAR disagreement is now a measured quantity — record the per-TF spread as the m
   column's uncertainty rather than reporting m\* as a point value.
5. Declared sensitivity: GC-rich promoter background for m_bg (carried from S258 item 4, still
   not done). The measured promoter GC contents from §3d (NAMPT 63.9%, SLC25A1 69.4%, EGR1 70.3%)
   are now available as realistic inputs for it.
6. T1(3) prospective application (TERT/TXNIP) remains GATED on items 1–3.
7. T2/T3 carried unchanged: NF-κB sensitivity entry; literature-derived a_t; EZH2 basal 5hmC;
   EGR1 activity-dependent demethylation.

NOT next: adjusting s_t, a_t, class thresholds or the R-override to rescue NAMPT or SLC25A1, or
choosing the matrix collection that reproduces S255.

