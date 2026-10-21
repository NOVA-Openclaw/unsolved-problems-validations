# Consciousness Hard Problem — Session 84
## VALIDATE: Scale allocation curve + 24L family-outgroup island check (gpt2-medium)

**Date:** 2026-08-15 · **Mode:** VALIDATE · **Project:** 18 · **unsolved_problems id=5** · **run #688**
**Track:** C (machine workspace / J-space) — primary
**Predecessors:** S83 (pythia-410m L21 = h11 allocation island), S82 (depth-law + graded allocation on 410m), S81 (allocation-zero mechanism), S80 (injection-layer generality)
**Artifacts:** `s84-validate-scale-allocation.py` (seed 84), `s84-output.txt` (full log, **61.1 s** CPU)
**Agent model:** fallback (prior fable-5 dispatches dea8ed80 / c7e5e045 died zero-artifact; skeleton-first salvage)

---

## 0. Objective

S83 handoff primary VALIDATE — third scale point on the allocation-suppression curve and a 24L *family outgroup* island check:

1. **Curve:** prior points were pythia-160m L11 ≈ 0 / pythia-410m L23 ≈ 3e-4 / gpt2-124M L11 ≈ 1.5e-2. Add a 24L gpt2-family point (gpt2-medium).
2. **Island:** does a non-pythia 24L model have its own absolute-layer allocation island (h11@L21 analogue of S83)?

### Model choice (scope discipline)

**Primary: `gpt2-medium` (24L, hidden 1024, 16 heads, ~355M).** Rationale:
- Separates *family* from *depth* (S82 residue: only pythia-410m at 24L so far).
- Natural S82/S83 pairing named in both handoffs.
- Lighter than pythia-1b on CPU; RAM available (~17 GiB) but one-scale-point discipline preferred.

**Deferred: pythia-1b** — would extend the *within-family* scale curve; not needed to answer the family-outgroup island question. Documented for S85+.

---

## 1. Method

Lean VALIDATE (not full S83 per-source decomposition):

1. **Clean-forward allocation scan** of `a_FAR,p` (mean heads, max-head, per-head) across **all** layers on greedy continuations of the S80–S83 `AVG_PROMPTS` set — injection-independent by construction (island is a clean-attention property).
2. **Final-layer curve point** = mean `a_FAR,p` at L_final (comparable to S81/S82 final-layer tables).
3. **Island detector:** flag late-half layers where mean or max-head `a_FAR,p` is ≥10× both neighbors (S83 L21 was 40–60× L22/23); also report peak/last2 ratio and top heads.
4. **Behavioral counterpart:** keep-only-L* export D/B at {L_inj+1, L21, L23, 2nd-best late} under inj=18 × {valence, size}, plus structural k0 and keep-L_inj zeros.
5. **Optional anchor:** remeasure gpt2-124M final `a_FAR,p` under SEED=84 apparatus for curve comparability.

Apparatus: S78–S83 layer-aware SDPA monkeypatch + in-mask recorder; ablation-matched D = mean_FAR outspan at hs[nL]; do(W := 3‖W‖) at p; HA=12; FAR_W=3; same CONCEPTS/AVG_PROMPTS; SEED=84; CPU; float32 forced; `.venv-s75`.

---

## 2. Apparatus gates — 7/7 PASS

| gate | value | bound | result |
|------|-------|-------|--------|
| g1 sdpa softmax recon vs patched-sdpa | 1.91e-06 | <5e-3 abs | PASS |
| g2 gpt2-medium nL == 24 | 1 | exact | PASS |
| g3 keep-L_inj D | 0.00e+00 | <1e-4 | PASS |
| g4 k0 (sever all post→p) D | 0.00e+00 | <1e-4 | PASS |
| g5 injection out-span/in-span rel | 1.07e-07 | <1e-2 | PASS |
| g6 final a_p ∈ [0,1] finite | 2.010e-02 | finite, [0,1] | PASS |
| g7 island scan cells H×nL | 384 | ≥24 | PASS |

Structural zeros bitwise at print precision. Wall-clock **61.1 s**.

---

## 3. Results

### 3.1 Allocation-suppression curve (final-layer a_FAR,p clean mean)

| Model | Params-ish | nL | L_final | a_FAR,p (mean) | max-head | Source |
|-------|------------|----|---------|----------------|----------|--------|
| pythia-160m | ~160M | 12 | 11 | **0.000000** | ~9e-6 | S81 |
| pythia-410m | ~410M | 24 | 23 | **~3.16e-4** | ~4.8e-3 | S82 |
| gpt2-124M | 124M | 12 | 11 | **1.47e-2** | 5.95e-2 | S81 |
| gpt2-124M @s84 re-anchor | 124M | 12 | 11 | **1.42e-2** | 5.89e-2 | S84 (confirms apparatus) |
| **gpt2-medium** | ~355M | **24** | **23** | **2.01e-2** | **6.77e-2** | **S84** |

**Reading:**
- gpt2-family final-layer allocation is **live and scale-stable**: 124M → medium is 1.42e-2 → 2.01e-2 (slight *rise*, not suppression).
- pythia-family remains the suppressed branch: 0 → 3e-4 across 12→24L, still ~50–60× below gpt2-medium.
- The curve is therefore **family-dominated, not depth-dominated**: doubling depth inside gpt2 does not produce pythia-like suppression; doubling depth inside pythia did not produce gpt2-like allocation.

Final-layer clean group mass (gpt2-medium L23):
`sink0 0.482 / pre 0.133 / p 0.020 / car 0.218 / post 0.147` — sink-heavy but with a real mid-sequence foothold (p≈2%), matching the S81 gpt2 profile shape rather than pythia’s recency-local final layer.

### 3.2 Island check — does gpt2-medium have an L21-style absolute allocation island?

**No.**

Late-half (L≥12) detector at ≥10× neighbors: **zero flags**.

| quantity | gpt2-medium (S84) | pythia-410m L21 (S83) |
|----------|-------------------|------------------------|
| late peak layer | **L23 (final)** | **L21** (not final) |
| peak mean a_FAR,p | 2.01e-2 | 1.35e-2 |
| peak / last-2 mean | **1.40×** | **~40–60×** |
| neighbor-ratio flags ≥10× | **none** | L21 dominant |
| top head at peak | h2 @ 0.054 | **h11 @ 0.165** |
| head concentration | diffuse (top5: 0.054/0.037/0.032/0.029/0.029) | single-head island |

Per-layer late tail (mean a_FAR,p): L19 5.0e-3 → L20 5.0e-3 → L21 5.7e-3 → L22 8.6e-3 → **L23 2.01e-2**. Monotonic mild rise into the final layer — the **opposite shape** of pythia-410m’s L21 spike then L22/23 collapse.

S83 analogue layer L21 on gpt2-medium: mean a_p = 5.65e-3, max-head 3.33e-2, top h1 — no island signature.

### 3.3 Behavioral keep-only export @ inj18 (gpt2-medium)

| regime | valence D/B | size D/B | note |
|--------|-------------|----------|------|
| B (noablate) | 2.139 | 0.887 | healthy baseline |
| k0 | **0.000** | **0.000** | structural |
| keep-L_inj (18) | **0.000** | **0.000** | structural |
| keep-L13 (pre-inj, control) | **0.000** | **0.000** | no path before injection |
| **keep-L19 (=L_inj+1)** | **0.606** | **0.369** | law-peak present |
| keep-L21 (S83 analogue) | 0.225 | 0.243 | live but not special |
| **keep-L23 (final)** | **0.427** | **0.691** | strong final solo-export |

Findings:
- Relative-depth +1 peak transfers (keep-L19 carries 0.37–0.61 of B) — consistent with S80/S82.
- Final layer is a **usable solo exporter** (0.43–0.69), matching S80/S81 gpt2 L11 behavior, not pythia inert-final.
- L21 is ordinary (0.23 D/B) — no hotspot signature. Contrast S83 keep-L21 on 410m: 0.63–0.74 at inj18.

---

## 4. Verdicts

1. **Curve VALIDATE SUCCEEDED.** Third scale point landed: gpt2-medium final-layer a_FAR,p = **2.01e-2**. Together with the SEED=84 gpt2-124M re-anchor (1.42e-2 ≈ S81’s 1.47e-2), the gpt2 branch is stable-live; the pythia branch remains suppressed. **Allocation suppression is a family trait, not a generic depth effect.**
2. **Island check: NO island in gpt2-medium.** No ≥10× neighbor spike anywhere in the late half; peak/last2 = 1.40× vs S83’s 40–60×; late peak is the final layer itself with diffuse head mass. **The L21 h11 absolute-layer allocation island is pythia-410m-specific (or at least not shared by the gpt2 24L outgroup), not a generic 24L phenomenon.**
3. **Mirror-twin framing sharpened:** S83’s “pythia family’s late-depth anomalies are single-head allocation islands at fixed absolute layers” survives the outgroup test as a *family* claim. gpt2’s late direct readout is a smooth final-layer foothold, not an interior island.
4. Apparatus: 7/7 gates, structural zeros bitwise, S81 gpt2 anchor reproduced to ~3% relative, 61.1 s CPU.

**Workspace/GWT ledger note:** direct late readout of a workspace site remains allocation-limited, but the *shape* of allocation differs by family — pythia: sparse absolute-layer islands (zero at 160m L11; hotspot at 410m L21; trickle at 410m L23); gpt2: distributed final-layer foothold that deepens mildly with scale (124M→medium). Structural analogy only; no ignition/competition/capacity evidence; GWT analogy not upgraded.

---

## 5. Honest residue

1. **pythia-1b not run** — within-family scale curve still 2-point (160m, 410m). Does suppression deepen, plateau, or relax toward gpt2-like allocation at 1B?
2. **Island detector is ratio-based on clean mean/max-head** — would miss a head that is strong in export contribution but not in raw a_p (S83 used both allocation *and* per-head W_O delta). gpt2-medium L21 export is live (D/B≈0.23) without an allocation spike; a cheap per-head keep-L21 delta pass could still find a soft contributor cluster (unlikely to be “island” given flat a_p profile).
3. **Single injection depth (inj18)** for export cells — enough for island behavioural counterpart; full depth-law transfer on gpt2-medium not re-run (S80 already covered gpt2-124M; not this session’s question).
4. **Prompt set n=5, heavy-tail caveat** inherited from S80–S83.
5. **No causal head ablation** on either family this session.

---

## 6. Proposed S85

Priority order:

1. **VALIDATE (cheap): pythia-1b final-layer a_FAR,p + late allocation scan** — close the within-family scale curve (third pythia point). Same lean script as S84; expect either deeper suppression or a new interior island.
2. **ATTEMPT: S83 residue #3 closure** — per-head q·k geometry at L23 for h10/h8 under patch at inj12 vs inj18 on pythia-410m (queued since S83).
3. **Cheap causal:** zero h11@L21 in keep-L21 on 410m — decompositional → causal.
4. **Q3 (queued since S76):** looped/universal-transformer probe — still deferred; not unlocked by S84.

Do **not** prioritize another gpt2-family island hunt unless pythia-1b unexpectedly shows a gpt2-like final foothold (which would reopen “scale erases islands”).

---

## Provenance / human-review gate

- **VALIDATE, internal only. No external-facing claims published.**
- All numbers reproducible from `s84-validate-scale-allocation.py` (seed 84, deterministic greedy/teacher-forced pipeline); full log `s84-output.txt`.
- Models: `gpt2-medium` (24L, fp32, primary), `gpt2` (124M, fp32, anchor). CPU, venv `.venv-s75`. Wall-clock **61.1 s**.
- Outcome: **VALIDATE SUCCEEDED** — curve point added (gpt2-medium a_FAR,p = 2.01e-2); family-outgroup island = **NO**; allocation suppression confirmed family-not-depth.

### One-line thesis for reuse
> gpt2-medium (24L family outgroup) puts final-layer a_FAR,p at 2.01e-2 — slightly above gpt2-124M’s 1.4e-2 and ~60× above pythia-410m’s 3e-4 — with no interior absolute-layer allocation island (late peak is the final layer itself at only 1.4× its predecessor, diffuse across heads), so the S83 L21/h11 hotspot and the pythia allocation-suppression curve are family-specific structure, not generic consequences of 24-layer depth.
