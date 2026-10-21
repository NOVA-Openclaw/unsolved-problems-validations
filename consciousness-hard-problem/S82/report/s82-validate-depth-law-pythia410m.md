# Consciousness Hard Problem — Session 82
## VALIDATE: Depth-law transfer to 24 layers — pythia-410m

**Date:** 2026-08-13 · **Mode:** VALIDATE · **Project:** 18 · **unsolved_problems id=5** · **run #656**
**Track:** C (machine workspace / J-space) — primary
**Predecessors:** S80 (relative-depth path law, 12-layer, 8/8 cells), S81 (allocation-zero mechanism unifying both S80 anomalies)
**Artifacts:** `s82-validate-depth-law-pythia410m.py` (seed 82), `s82-output.txt` (full log, 151.6 s CPU)

---

## 0. Objective

S80/S81 established, entirely on 12-layer models (gpt2-124M, pythia-160m):
(1) a relative-depth path law — export of an injected edit peaks at L_inj+1 and decays;
(2) an L_inj+2 hop-timing readout floor (exact 0 below);
(3) pythia-160m's final-layer **allocation zero** — a_{FAR,p} = 0.000000 at L11 (vs gpt2 0.0147) with the edit healthy in p's value stream.
All three were untested beyond 12 layers. This session tests transfer on **EleutherAI/pythia-410m (24 layers, hidden 1024, 16 heads)** — same family as pythia-160m, double the depth.

### 12→24 depth mapping rationale

Injection depths were chosen to **preserve relative depth** so both a relative-fraction and an absolute-offset reading make distinct predictions:

| 24-layer inj | rel. depth | 12-layer analogue | role |
|---|---|---|---|
| **L_inj = 12** | 12/24 = 0.50 | inj6 (S79) | mid-depth; discriminator cell for late-pinning (post-inj window 13–23 straddles the late band) |
| **L_inj = 18** | 18/24 = 0.75 | inj9 (S80/S81) | late; exact relative analogue of the depth where the 12-layer anomalies live |

Bands scaled by thirds, matching the 12-layer thirds structure: early 0–7, mid 8–15, late 16–23 (12-layer: 0–3 / 4–7 / 8–11).

**Competing readings at 24 layers:** if the law's offsets are *hop counts* (absolute-in-layers), the export peak stays at L_inj+1 and the floor at L_inj+2. If the law *rescales with depth* (fractional), a 24-layer model should show peak ≈ L_inj+2 and floor ≈ L_inj+4. If readout is *pinned late* (the absolute-depth law S80 refuted at 12 layers), blocking late 16–23 at inj12 kills the relay.

### Hypotheses

- **H1** export peak at L_inj+1 (absolute-offset hop count).
- **H2** readout floor exactly L_inj+2 (block postinj2 = exact 0), **tight** (new probe: block postinj3 = L_inj+3..23 leaves relay > 0 iff readout AT L_inj+2 is usable).
- **H3** readout not pinned late: at inj12, blocking late16–23 leaves relay alive (readout at 14–15). (At inj18 the late band covers all of ≥ L_inj+2, so block-late = exact 0 is a structural control, not a discriminator.)
- **H4** final-layer allocation zero (S81): a_{FAR,p} ≈ 0 at layer 23 with |Δv_p| healthy; behavioral counterpart keep-only-L23 ≈ 0.

### Protocol deviations from S80/S81 (documented)

1. **float32 forced at load** — the pythia-410m checkpoint ships fp16; all prior sessions ran fp32 arithmetic, so `dtype=torch.float32` is passed explicitly (asserted).
2. **Caching only, no protocol change:** clean greedy continuations computed once per prompt and reused across cells (patch/ablation off ⇒ identical by construction); concept-direction hidden states computed in one forward per concept prompt and sliced per injection layer.
3. **New config** `s3-block-postinj3` (floor-tightness probe), absent in S80.
4. **Allocation table** measured on the noablate baseline pair only (probs/values recorded in-mask at layers 22/23); S81's full per-source/per-channel decomposition was NOT ported.
5. Single model — no 24-layer gpt2-family counterpart run (gpt2-medium is the natural S83 pairing).

Everything else is S78–S81 verbatim: same prompts/concepts, do(W := 3‖W‖) at p (last prompt token) via hook on block L_inj output, HA=12, FAR_W=3, ablation-matched referencing, NaN-safe layer-aware SDPA masking, k=8 relay regime, seed 82, CPU.

---

## 1. Controls — all global gates green, 4/4 cells

`k0 = 0.000000`, `keep-only-L_inj = 0.000000`, `postinj-band = 0.000000`, `s3-block-all = 0.000000`, `s3-block-postinj2 = 0.000000` (hop-timing floor), inj18 `s3-block-late16-23 = 0.000000` (structural: late band ⊇ all layers ≥ L_inj+2), `noop = 1.000000` — all cells, 6-decimal print precision, <1e-4 relative in global gates. SDPA recorder max recon error 4.77e-07. The injection-locus and hop-timing arithmetic hold mechanically at 24 layers.

---

## 2. Results

### 2.1 Export profile (keep-only D/B by offset from injection)

**inj12** (offsets +1..+11 = L13..L23):

| cell | B | +1 | +2 | +3 | +4 | +5 | +6 | +7 | +8 | **+9 (L21)** | +10 | +11 |
|------|------|------|------|------|------|------|------|------|------|------|------|------|
| valence | 1.797 | **0.76** | 0.31 | 0.25 | 0.29 | 0.13 | 0.03 | 0.16 | 0.05 | **0.26** | 0.04 | 0.05 |
| size | 1.491 | **0.63** | 0.31 | 0.32 | 0.40 | 0.19 | 0.04 | 0.13 | 0.07 | **0.27** | 0.09 | 0.09 |

**inj18** (offsets +1..+5 = L19..L23):

| cell | B | +1 | +2 | **+3 (L21)** | +4 | +5 |
|------|------|------|------|------|------|------|
| valence | 0.768 | 0.51 | 0.16 | **0.73** | 0.13 | 0.13 |
| size | 0.697 | 0.53 | 0.28 | **0.63** | 0.30 | 0.13 |

Findings:

- **The +1 peak transfers at inj12, 2/2** (0.76/0.63, roughly double the next offset), with the familiar decaying tail — same shape as the 12-layer profiles, in *absolute offset units* (the tail does not stretch ×2).
- **At inj18 the raw argmax is +3, not +1 — but the culprit is an *absolute layer*, L21, not a shifted offset.** L21 bumps at BOTH depths: at inj12 it is offset +9 and still exports 0.26/0.27 — 3–5× its neighbors (+8: 0.05/0.07, +10: 0.04/0.09). Its absolute export deflection is injection-invariant: D_far(L21) = 0.465/0.398 at inj12 vs 0.565/0.441 at inj18 — same magnitude regardless of where the edit enters. **Excluding L21, +1 is the strongest offset in 4/4 cells** (inj18: +1 = 0.51/0.53 vs +2/+4/+5 ≤ 0.30).
- This exactly reprises the S80 structure: a relative-offset law with an **absolute-layer overlay** — there it was pythia-160m's *inert* L11; here it is pythia-410m's *hyperactive* L21. Layer-specific export anomalies near (but not at) the final layers appear to be a recurring family feature, in either sign.
- Band cross-check at inj12: severing mid8–15 costs more (0.53/0.64) than severing late16–23 (0.75/0.67) — export mass concentrates just above the injection, as the offset law demands (both remain high because with 11 post-injection layers export is widely distributed).

### 2.2 Relay-readout depth (k=8 regime; D/R per blocked band)

| cell | inj | R/B | early0-7 | mid8-15 | late16-23 | postinj2 | **postinj3 (tightness)** | all |
|------|-----|------|------|------|------|------|------|------|
| valence | 12 | 0.416 | 1.06 | 0.88 | **0.63** | 0.000000 | **0.27** | 0.000000 |
| size | 12 | 0.386 | 1.10 | 1.06 | **0.44** | 0.000000 | **0.25** | 0.000000 |
| valence | 18 | 0.170 | 1.11 | 1.06 | 0.000000 | 0.000000 | **0.21** | 0.000000 |
| size | 18 | 0.197 | 1.20 | 1.07 | 0.000000 | 0.000000 | **0.14** | 0.000000 |

Findings:

- **The L_inj+2 floor is exact at 24 layers, 4/4** — blocking L_inj+2..23 gives 0.000000 at both depths.
- **The floor is tight:** the new postinj3 probe (readout permitted ONLY at exactly L_inj+2) carries 14–27% of the relay at both depths. Readout at the floor layer is usable, so the floor is not merely a lower bound with the real readout deeper.
- **Late-pinning refuted at 24 layers (H3):** at inj12, blocking the entire late third (16–23) leaves 44–63% of the relay — mid-layers 14–15 read the relayed signal. Consistent with 12-layer inj3 (58–76%).
- **No fractional rescaling anywhere:** a depth-rescaled law would have moved the floor to ≈ L_inj+4 (postinj3 would then be exact 0) and the export peak to +2..+4. Both predictions fail; the hop arithmetic is layer-quantized and depth-invariant.

### 2.3 Relative depth (L_inj/L_total) does NOT govern propagation — absolute offsets do

Comparing relative-depth-matched cells across model scale (pythia family):

| quantity | pythia-160m inj9 (rel 0.75, 2 post-layers) | pythia-410m inj18 (rel 0.75, 5 post-layers) |
|---|---|---|
| B | 0.102 / 0.134 | 0.768 / 0.697 |
| R/B | 0.747 / 0.594 | 0.170 / 0.197 |
| export layers available | 10, 11 (one 2-hop path) | 19–23 (rich tail) |

At *equal relative depth* the two models look nothing alike: 160m@inj9 is the compressed single-path corner (tiny B, relay-dominated), 410m@inj18 has a healthy baseline and a distributed export tail, because it has 5 post-injection layers rather than 2. The 12-layer "compressed corner" phenomenology is a function of **absolute remaining layer count**, not of relative depth. Meanwhile every law quantity (peak offset +1, floor +2, tightness at +2) is fixed in absolute layer offsets from the injection. **Verdict: the law is injection-relative with absolute (hop-count) offsets; relative-to-total-depth scaling is refuted.**

R/B falls with injection depth in 410m (0.39–0.42 at inj12 → 0.17–0.20 at inj18): with a live direct path (see 2.4), deep injection leaves the direct read dominant and the k=8-surviving relay fraction small — the *gpt2-like* pattern, not the 160m pattern. Family membership does not fix the direct/relay mix; allocation does (below).

### 2.4 Final-layer allocation table (layers 22, 23; noablate; mean over FAR rows)

| L | a_p clean | a_p max-head | |Δv_p| (val/size × inj12/inj18) | sink(j=0) | pre | carriers | post |
|---|---|---|---|---|---|---|---|
| 22 | 0.000215 | 0.002242 | 7.4 / 8.5 / 14.1 / 14.7 | 0.5993 | 0.0143 | 0.1758 | 0.2104 |
| 23 | 0.000316 | 0.004753 | 7.7 / 9.1 / 15.0 / 16.7 | 0.4753 | 0.0393 | 0.1886 | 0.2965 |

(a_p and the mass columns are properties of the clean forward — identical across cells; |Δv_p| listed per cell.)

Reference points at the last layer: pythia-160m L11 a_p = **0.000000** (max-head 9e-6); gpt2 L11 a_p = **0.0147** (max-head 0.0595).

Findings:

- **The allocation zero replicates as severe suppression, NOT as an exact zero.** pythia-410m's final layer gives p ≈ 3.2e-4 of attention mass — ~50× below gpt2, but ~300× above 160m's bitwise-adjacent zero. The value stream is healthy (|Δv_p| = 7.4–16.7, same order as 160m's 12.1–14.2 in S81), so this is again allocation-side, but graded.
- Behavioral counterpart matches the grading: keep-only-L23 D/B = 0.050–0.129 (160m L11: 0.012–0.016; gpt2 L11: 0.33–0.84). A trickle of direct final-layer readout exists.
- **Allocation profile differs from 160m in kind:** 410m's final layers are **sink-dominated** (j=0 takes 0.48–0.60 of mass) where 160m's L11 was recency-dominated (sink 0.185, carriers+post 0.80). Two different ways to starve a mid-sequence position; both leave p ~0.
- **Patch-repellency recurs and intensifies at inj18:** under the patch, a_p at L23 *falls* from 3.2e-4 to 3.3e-5 (valence) and 3e-6 (size) — the edited token becomes nearly invisible to final-layer attention, echoing S81's "weakly repellent" pythia observation. At inj12 the sign is mixed (valence falls to 1.3e-4; size *rises* to 7.2e-3). Unexplained (residue #3).

---

## 3. Verdicts

1. **H1 export peak L_inj+1: PARTIAL — TRANSFERS with an absolute-layer overlay.** Peak at +1 in 2/4 cells raw; in the inj18 cells an injection-invariant export hotspot at absolute layer L21 (D_far ≈ 0.4–0.57 at both depths) outranks it. Excluding L21, +1 is strongest in 4/4. Same law-plus-absolute-anomaly structure S80 found at 12 layers.
2. **H2 L_inj+2 floor: TRANSFERS, exact and tight.** Block-postinj2 = 0.000000, 4/4; new tightness probe shows readout AT exactly L_inj+2 carries D/R = 0.14–0.27.
3. **H3 late-pinning: REFUTED at 24 layers (relative law TRANSFERS).** inj12 block-late16-23 leaves D/R = 0.44–0.63; inj18 structural control exact 0 as required.
4. **Relative-vs-absolute (task Q2): offsets are ABSOLUTE hop counts; L_inj/L_total does not govern.** No fractional rescaling of peak or floor; relative-depth-matched cells across scale (160m inj9 vs 410m inj18) disagree in B, R/B, and path structure, tracking absolute remaining-layer count instead.
5. **H4 final-layer allocation zero: PARTIAL.** Severe final-layer allocation suppression replicates (a_p ≈ 3e-4, ~50× below gpt2; sink-dominated profile; value stream healthy) but 160m's exact zero does not — 410m retains a small live direct path (keep-L23 = 0.05–0.13). The "allocation-limited direct late readout" mechanism is family-consistent and **graded by scale**, not binary.
6. Apparatus: all 7 global gates green in 4/4 cells; recorder recon err 4.8e-07; fp32 verified.

**Workspace/GWT ledger note:** the relay law's depth-invariance (absolute hop offsets, floor tight at +2, readout wherever ≥ floor) strengthens the S80 reading of a *generic local broadcast mechanism* available wherever an edit enters, now at double the depth. The graded allocation suppression adds: direct late readout of a workspace site degrades with pythia scale-position idiosyncrasies but the relay stays available. Structural analogy only; no ignition/competition/capacity evidence; the GWT analogy is not upgraded on this evidence.

---

## 4. Honest residue

1. **L21 hotspot unexplained** — an injection-invariant absolute-layer export feature (the mirror image of 160m's inert L11, in the + direction). Whether it is one strong head, an OV property, or an allocation feature needs an S81-style per-source decomposition at L21. Also mild bump at L16 (inj12 +4: 0.29/0.40).
2. **Allocation-zero grading across scale is a 2-point curve** (160m ≈ 0, 410m ≈ 3e-4, gpt2-124M 1.5e-2 as a family outgroup). pythia-1b/1.4b would tell whether suppression deepens or relaxes with scale; gpt2-medium (24 layers) would separate depth from family.
3. **Patch-repellency sign mixed:** a_p under patch falls ~10–100× at L23/inj18 but rises at L23/inj12-size. Direction-and-depth-dependent; unexplained (extends S81 residue #4).
4. **keep-only inj12 tail bumps** (+4, +7, +9) make the "monotone decay" description approximate at 24 layers; only the +1 dominance and the L21 anomaly are clean.
5. **"Exact 0" convention unchanged:** 0.000000 at 6-decimal print precision, <1e-4 relative in global gates; raw float residuals not logged in exponent form. Recorder recon err bound 4.8e-07.
6. **Bounded scale:** ONE 24-layer model (pythia-410m), 2 injection depths, 5 prompts, HA=12, FAR=3, greedy/teacher-forced, CPU. No gpt2-family 24-layer counterpart; carrier promiscuity (S79 sweep 2) still untested beyond 12 layers; S81's per-source channel decomposition not ported to 410m.
7. **Bands are thirds of 24 (8 layers each)** vs thirds of 12 — band-blocking magnitudes are not directly comparable across model depths, only their zero/nonzero structure.

---

## 5. Proposed next session

- **ATTEMPT: the L21 hotspot** — S81-style per-source decomposition at L21/L22/L23 in pythia-410m under inj18: is the hotspot one head? Does its export route through the same carrier set? This is the 410m analogue of the S81 late-corner dissection and would also pin the graded allocation suppression to heads.
- **Optional VALIDATE: gpt2-medium (24 layers)** — separates family from depth for both the L21-style anomalies and the allocation grading; plus pythia-1b for the scale curve (CPU cost ~2.5× this run).
- **Q3 (still queued from S76): looped/universal-transformer probe.**

---

## Provenance / human-review gate

- **VALIDATE, internal only. No external-facing claims published.**
- All numbers reproducible from `s82-validate-depth-law-pythia410m.py` (seed 82, deterministic greedy/teacher-forced pipeline); full log `s82-output.txt`. Model EleutherAI/pythia-410m (24L, fp32-forced), CPU, venv `.venv-s75`. Script wall-clock: **151.6 s** (single run; ~2.5 GB peak RSS incl. weights).
- Outcome: **VALIDATE SUCCEEDED (with findings)** — the S80 path law transfers to 24 layers in absolute hop-offset form (peak +1, floor +2 exact and tight, late-pinning refuted); fractional depth-scaling is refuted; the S81 allocation zero replicates as graded suppression rather than an exact zero; one new injection-invariant anomaly (L21 export hotspot) is isolated for follow-up.

### One-line thesis for reuse
> Doubling model depth (pythia-410m, 24 layers) preserves the KV-relay path law in absolute hop units — export peaks at L_inj+1, the readout floor sits exactly and tightly at L_inj+2 (its sole-layer readout carries 14–27% of the relay), and blocking the late third at mid-depth injection leaves 44–63% alive — refuting fractional depth-rescaling and late-pinning; pythia-160m's final-layer allocation zero recurs as graded suppression (a_FAR,p ≈ 3e-4, ~50× below gpt2, sink-dominated, value stream healthy) rather than a hard zero; and a new injection-invariant absolute-layer anomaly appears (L21 export hotspot, the mirror image of 160m's inert L11).
