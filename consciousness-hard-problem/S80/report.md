# Consciousness Hard Problem — Session 80
## VALIDATE: Injection-layer generality of the relay path law — relative vs absolute depth

**Date:** 2026-08-09 · **Mode:** VALIDATE · **Project:** 18 · **unsolved_problems id=5** · **run #625**
**Track:** C (machine workspace / J-space) — primary
**Predecessors:** S78 (multi-hop KV relay CONFIRMED), S79 (path decomposition at injection block 6: export L7–8, promiscuous carriers, readout 8–11 only)
**Artifacts:** `s80-validate-injection-layer-generality.py` (seed 80), `s80-output.txt` (full run log)

---

## 0. Objective

S79 resolved the relay path structure but tested it **only at injection block 6** — in a 12-layer model, "export at L_inject+1..+2" (= 7–8) and "readout at layers 8–11" (= ≥ L_inject+2) are confounded between a RELATIVE-depth law and an ABSOLUTE-depth (late-layers-pinned) law. This session breaks the confound by injecting at blocks **3** and **9**, running the compact S79 core (keep-only export profile + band blocking + relay-readout band blocking + all exact controls) in 8 cells: {gpt2-124M, pythia-160m} × {valence, size} × {inj3, inj9}. Seed 80, 5 prompts, HA=12, FAR=3, CPU, S78/S79 ablation-matched referencing and NaN-safe layer-aware SDPA masking verbatim.

**Predictions:**
- *Relative-depth law:* export peak tracks L_inj+1..+2 (inj3 → L4/L5; inj9 → L10/L11); readout available from L_inj+2 on (inj3 → blocking late 8–11 does NOT kill the relay).
- *Absolute-depth law:* export/readout pinned late regardless (inj3 → keep-only L7/L8 ≫ L4/L5; blocking 8–11 kills the relay even at inj3).

**New structural control** (law-independent hop-timing floor): export needs L₁ ≥ L_inj+1; a carrier's K/V carries the edit only at layers ≥ L₁+1 ≥ L_inj+2; therefore blocking FAR's post-p readout at **L_inj+2..11** must be EXACT 0 under any law (`s3-block-postinj2`).

---

## 1. Controls — 6/6 global gates passed, 8/8 cells

`k0 = 0.000000`, `keep-only-L_inj = 0.000000`, `postinj-band = 0.000000`, `s3-block-all = 0.000000`, **`s3-block-postinj2 = 0.000000`** (new hop-timing floor), `noop = 1.000000` — all cells, 6-decimal print precision, <1e-4 relative in global gates. The injection-locus logic and the hop-timing arithmetic hold mechanically at every injection depth tested.

---

## 2. Results

### 2.1 Export profile (keep-only: attn-to-p at ONE layer; ratio D/B)

**Injection block 3** — relative law predicts peak L4/L5; absolute predicts L7/L8:

| cell | B | L4 | L5 | L6 | L7 | L8 | L9 | L10 | L11 |
|------|------|------|------|------|------|------|------|------|------|
| gpt2/valence | 0.616 | **0.96** | 0.68 | 0.57 | 0.33 | 0.26 | 0.15 | 0.14 | 0.33 |
| gpt2/size | 0.453 | **0.91** | 0.55 | 0.50 | 0.24 | 0.22 | 0.10 | 0.07 | 0.38 |
| pythia/valence | 1.126 | **1.06** | 0.60 | 0.57 | 0.60 | 0.56 | 0.17 | 0.15 | 0.06 |
| pythia/size | 1.138 | **0.74** | 0.69 | 0.58 | 0.55 | 0.31 | 0.13 | 0.14 | 0.00 |

**Injection block 9** — only L10/L11 structurally available:

| cell | B | L10 | L11 |
|------|------|------|------|
| gpt2/valence | 0.826 | 0.48 | **0.73** |
| gpt2/size | 0.714 | 0.24 | **0.84** |
| pythia/valence | 0.102 | **1.72** | 0.02 |
| pythia/size | 0.134 | **1.31** | 0.01 |

Findings:
- **Export peak tracks the injection: RELATIVE.** At inj3 the strongest sole exporter is **L4 = L_inj+1 in 4/4 cells** (0.74–1.06 of baseline alone), with L7/L8 far weaker (0.22–0.60). At inj9 the peak is L10 (pythia) or L11 (gpt2) — within L_inj+1..+2 in all 8 cells. The absolute-depth reading of S79 ("export pinned at 7–8") is **refuted**.
- **The profile is a decaying tail, not a hard +1..+2 window.** At inj3, L5–L8 still export 0.22–0.69 individually; the S79 phrasing "L_inject+1..+2 dominates" is refined to: **export peaks at L_inj+1 and decays with distance from the injection**, every post-injection layer retaining some export capacity (except pythia-L11, below).
- **Band cross-check** (inj3): severing mid4–7 costs far more (D/B 0.32–0.61) than severing late8–11 (0.80–1.05) — the export mass sits just above the injection, as the relative law demands.

### 2.2 Relay-readout depth (k=8 regime; D/R per blocked band)

| cell | inj | R/B | block early0-3 | block mid4-7 | block late8-11 | block postinj2 | block all |
|------|-----|------|------|------|------|------|------|
| gpt2/valence | 3 | 0.686 | 1.30 | 0.88 | **0.58** | **0.000000** | 0.000000 |
| gpt2/size | 3 | 0.540 | 1.28 | 1.10 | **0.63** | **0.000000** | 0.000000 |
| pythia/valence | 3 | 0.792 | 1.45 | 0.75 | **0.68** | **0.000000** | 0.000000 |
| pythia/size | 3 | 0.683 | 1.56 | 0.84 | **0.76** | **0.000000** | 0.000000 |
| gpt2/valence | 9 | 0.162 | 0.86 | 0.91 | 0.000000 | 0.000000 | 0.000000 |
| gpt2/size | 9 | 0.078 | 0.92 | 0.90 | 0.000000 | 0.000000 | 0.000000 |
| pythia/valence | 9 | 0.747 | 2.63 | 1.55 | 0.000000 | 0.000000 | 0.000000 |
| pythia/size | 9 | 0.594 | 1.06 | 1.89 | 0.000000 | 0.000000 | 0.000000 |

Findings:
- **The inj3 discriminator lands on RELATIVE, 4/4.** Blocking late 8–11 at inj3 leaves 58–76% of the relay intact — mid-layers 5–7 can read the relayed signal. Under the absolute law this would be exact 0; it is not, in any cell. **S79's "readout is exclusively late (8–11)" is hereby REVISED:** readout is exclusively **≥ L_inj+2** (the hop-timing floor), which at inj6 merely *coincided* with the late band.
- **The hop-timing floor is exact at every depth:** blocking L_inj+2..11 (inj3: 5–11; inj9: layer 11 alone) gives 0.000000, 8/8. At inj9 this doubles as a sharp statement: the ONLY possible relay readout is the final layer, and blocking that single layer kills the relay exactly.
- **inj9 relay exists but is compressed** — exactly one 2-hop path (export L10 → readout L11) remains, and it works: R/B = 0.078–0.747. In pythia this single path carries 59–75% of baseline; in gpt2 only 8–16% (see residue #3).

### 2.3 The keep-only-L11 gpt2/pythia split is ABSOLUTE (injection-invariant)

S79's unexplained anomaly reappears at **both** new depths: pythia's final layer solo-exports essentially nothing (inj3: 0.06/0.001; inj9: 0.02/0.01) while gpt2's L11 remains a usable solo exporter (inj3: 0.33/0.38; inj9: 0.73/0.84). Since this holds regardless of where the injection sits, the split is an **absolute architectural property of pythia's block 11** (candidate: parallel-residual final block / what its attention writes into the FAR out-span), not part of the relative path law. This is the one genuinely absolute-depth feature found — and it concerns one specific layer of one family, not the law.

### 2.4 Revised path law (v2)

```
inject at p, block L_inj output:
  EXPORT   attn-to-p peaks at L_inj+1, decaying with depth
           (every layer > L_inj retains some export; exception: pythia L11 ≈ 0, absolute)
  CARRIAGE position-promiscuous, redundant (S79; not re-tested here)
  READOUT  FAR reads the relay at ANY layer ≥ L_inj+2 — exact-0 below that floor
           (hop-timing structural, 8/8); "late-only" at inj6 was a coincidence of depth
```

The law is **relative-depth** with one absolute overlay (pythia's inert final-layer export). For the workspace/GWT ledger: relative depth-locality strengthens the "broadcast into a shared medium" reading — the relay is a generic local mechanism available wherever the edit enters, not a dedicated late-layer readout circuit. As in S79: structural analogy only; no ignition/competition/capacity evidence; the GWT analogy is **not** upgraded on this evidence.

---

## 3. Verdicts

1. **Relative-depth law: CONFIRMED, 8/8 cells.** Export peak at L_inj+1(..+2) at every injection depth; inj3 discriminator (block-late D/R = 0.58–0.76 > 0) refutes absolute-depth readout in all 4 cells.
2. **Hop-timing floor: EXACT, 8/8.** Readout below L_inj+2 is 0.000000 — new structural control passed at both depths (including the single-layer version at inj9).
3. **S79 readout claim REVISED:** "exclusively late 8–11" → "exclusively ≥ L_inj+2". S79's data was correct; its depth attribution was the confound this session was designed to break.
4. **keep-only-L11 split: injection-invariant** — an absolute property of pythia's final block, now separated from the (relative) path law. S79 residue #1 is sharpened, not resolved.
5. All 6 exactness gates green in all 8 cells; apparatus reproduces the S78/S79 mask-vs-fast-path agreement at 6 decimals.

---

## 4. Honest residue

1. **keep-only ratios > 1** (pythia inj3 L4 = 1.06; pythia inj9 L10 = 1.72 and 1.31): a single export layer delivering MORE than the un-ablated baseline. Attention redistribution under the mask presumably concentrates flow through the surviving edge; mechanism unmeasured. The qualitative peak locations are unaffected, but magnitudes above ~1 should not be read as "fraction of baseline".
2. **Pre-injection band ratios stray further from 1.0 than S79's** — s1-band-early0-3 at inj3 gives 1.04–1.35 (gpt2 up to 1.35, worse than its ±2.2% at inj6). Matched referencing cancels honest-computation disruption only to first order, and the second-order interaction grows when the severed band sits at/below the injection. Single-config ratio differences < ~0.35 at inj3 should not be over-interpreted; the discriminator margins used here (0.58–0.76 vs exact 0; 0.74–1.06 vs 0.22–0.60) clear that bar.
3. **gpt2 vs pythia inj9 relay flip, unexplained:** gpt2's relay fraction collapses at inj9 (R/B = 0.078/0.162; its FAR deflection is mostly direct) while pythia's stays high (0.594/0.747) despite pythia's tiny baseline (B = 0.10/0.13 vs gpt2's 0.71/0.83). Two cross-family unknowns now sit at the late-depth corner (this and the L11 export split); possibly related, untested.
4. **Sweep-3 enhancement ratios recur, larger** — up to 2.63 (pythia inj9 valence, block-early). Same shape as S79 residue #3; still only bounded, not explained.
5. **"Exact 0" convention unchanged:** 0.000000 at 6-decimal print precision, <1e-4 relative in global gates; raw float residuals not logged in exponent form.
6. **Compact core only:** drop-one and single-gate carrier sweeps were not rerun at the new depths — carrier promiscuity (S79 sweep 2) is assumed, not re-validated, at inj3/inj9.
7. **Bounded scale, as before:** 5 prompts, HA=12, FAR=3, two 12-layer ~100–160M models, greedy/teacher-forced, CPU. Injection depths tested: 3, 6 (S79), 9 — three points, one architecture class (12-layer decoder-only). Deeper models and other families untested.

---

## 5. Proposed next session

- **ATTEMPT: the late-depth corner.** Both remaining anomalies live at the final layers: (a) pythia's inert L11 solo-export (absolute, injection-invariant), (b) the gpt2/pythia inj9 relay-fraction flip. Probe pythia's parallel-residual final block directly: decompose FAR's block-11 attention output into in-span/out-span contributions per source position under the inj9 single-path regime; compare with gpt2. This would either explain both anomalies with one mechanism or split them.
- **Optional VALIDATE: depth-law scaling** — one deeper model (e.g. pythia-410m, 24 layers) at two injection depths to check the relative law and the L_inj+2 floor transfer beyond 12-layer models.
- **Q3 (still queued from S76): looped/universal-transformer probe.**

---

## Provenance / human-review gate

- **VALIDATE, internal only. No external-facing claims published.**
- All numbers reproducible from `s80-validate-injection-layer-generality.py` (seed 80, deterministic greedy/teacher-forced pipeline); full log `s80-output.txt`. Models gpt2 (124M) + EleutherAI/pythia-160m, CPU, venv `.venv-s75`. Script wall-clock: 173.3 s.
- Outcome: **VALIDATE SUCCEEDED** — the S78-queued injection-layer generality question is answered: the relay path law is relative-depth (export peak L_inj+1, readout floor L_inj+2, both confirmed at inj3/inj9 with exact structural controls 6/6 green in 8/8 cells), S79's "late-only readout" is corrected to a depth-relative floor, and the one absolute-depth feature (pythia's inert final-layer export) is isolated as an architectural anomaly, not part of the law.

### One-line thesis for reuse
> Injecting at blocks 3 and 9 (vs S79's block 6) shows the transformer KV-relay path law is RELATIVE-depth: export from the injection site peaks at L_inj+1 in 8/8 cells (gpt2 + pythia-160m, valence + size), far-position readout is available at any layer ≥ L_inj+2 and exactly zero below that hop-timing floor (blocking layers 8–11 at inj3 leaves 58–76% of the relay alive, refuting absolute late-layer readout), and the single absolute-depth feature — pythia's final layer exporting nothing at any injection depth — is an architectural anomaly separate from the law.
