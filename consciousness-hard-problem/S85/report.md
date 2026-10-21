# Consciousness Hard Problem — Session 85
## VALIDATE: pythia-1b within-family scale curve + late allocation scan

**Date:** 2026-08-15 · **Mode:** VALIDATE · **Project:** 18 · **unsolved_problems id=5** · **run #697**
**Track:** C (machine workspace / J-space) — primary
**Predecessors:** S84 (gpt2-medium family-outgroup island = NO; curve family-not-depth), S83 (pythia-410m L21 = h11 allocation island), S82 (depth-law + graded allocation on 410m), S81 (allocation-zero mechanism)
**Artifacts:** `s85-validate-pythia1b-scale.py` (seed 85), `s85-output.txt` (full log, **181.4 s** CPU)
**Agent model:** xai/grok-4.5 (subagent VALIDATE)

---

## 0. Objective

S84 handoff primary VALIDATE — third *within-family* pythia scale point on the allocation-suppression curve:

1. **Curve:** prior pythia points were 160m L11 ≈ 0 / 410m L23 ≈ 3.2e-4. Add pythia-1b (16L) final-layer `a_FAR,p`. Expect deeper suppression, plateau, or a new interior island — or (as observed) **relax** toward gpt2-like allocation.
2. **Island:** does pythia-1b host an absolute-layer allocation island (L21/h11 analogue of S83), or a smooth late profile?

### Model choice (scope discipline)

**Primary: `EleutherAI/pythia-1b` (16L, hidden 2048, 8 heads, ~1B).** Rationale:
- Closes the within-family pythia scale curve (third point after 160m / 410m).
- Named first priority in S84 proposed next steps.
- Lean S84 apparatus reused; one new model only.

**Optional light re-anchor: `EleutherAI/pythia-410m`** — clean final `a_FAR,p` under SEED=85 apparatus (no export). Ran successfully; confirmed S82 value to high precision.

**Linj choice for 16L:** `inj=12` so post layers {13, 14, 15} remain (3 post layers). Analogue of S82/S83 inj18 on 24L (5 post layers), scaled down. Documented in script header and log.

---

## 1. Method

Lean VALIDATE (same apparatus as S84; not full S83 per-source decomposition):

1. **Clean-forward allocation scan** of `a_FAR,p` (mean heads, max-head, per-head) across **all** layers on greedy continuations of the S80–S84 `AVG_PROMPTS` set — injection-independent by construction.
2. **Final-layer curve point** = mean `a_FAR,p` at L_final (comparable to S81/S82/S84 final-layer tables).
3. **Island detector:** flag late-half layers where mean or max-head `a_FAR,p` is ≥10× both neighbors (S83 L21 was 40–60× L22/23); also report peak/last2 ratio and top heads.
4. **Behavioral counterpart:** keep-only-L* export D/B at {L_inj+1, peak late, final, 2nd-best late, pre-inj control} under inj=12 × {valence, size}, plus structural k0 and keep-L_inj zeros.
5. **Optional light re-anchor:** pythia-410m final `a_FAR,p` under SEED=85 (clean scan only).

Apparatus: S78–S84 layer-aware SDPA monkeypatch + in-mask recorder; ablation-matched D = mean_FAR outspan at hs[nL]; do(W := 3‖W‖) at p; HA=12; FAR_W=3; same CONCEPTS/AVG_PROMPTS; SEED=85; CPU; float32 forced; `.venv-s75`.

---

## 2. Apparatus gates — 7/7 PASS

| gate | value | bound | result |
|------|-------|-------|--------|
| g1 sdpa softmax recon vs patched-sdpa | 7.15e-07 | <5e-3 abs | PASS |
| g2 pythia-1b nL == 16 | 1 | exact | PASS |
| g3 keep-L_inj D | 0.00e+00 | <1e-4 | PASS |
| g4 k0 (sever all post→p) D | 0.00e+00 | <1e-4 | PASS |
| g5 injection out-span/in-span rel | 1.94e-07 | <1e-2 | PASS |
| g6 final a_p ∈ [0,1] finite | 9.713e-03 | finite, [0,1] | PASS |
| g7 island scan cells H×nL | 128 | ≥16 | PASS |

Structural zeros bitwise at print precision. Wall-clock **181.4 s** (includes optional 410m re-anchor).

---

## 3. Results

### 3.1 Allocation-suppression curve (final-layer a_FAR,p clean mean)

| Model | Params-ish | nL | L_final | a_FAR,p (mean) | max-head | Source |
|-------|------------|----|---------|----------------|----------|--------|
| pythia-160m | ~160M | 12 | 11 | **0.000000** | ~9e-6 | S81 |
| pythia-410m | ~410M | 24 | 23 | **~3.16e-4** | ~4.8e-3 | S82 |
| pythia-410m @s85 re-anchor | ~410M | 24 | 23 | **3.162e-04** | 4.75e-3 | S85 (confirms S82) |
| gpt2-124M | 124M | 12 | 11 | **1.42e-2** | 5.89e-2 | S84 re-anchor |
| gpt2-medium | ~355M | 24 | 23 | **2.01e-2** | 6.77e-2 | S84 |
| **pythia-1b** | **~1B** | **16** | **15** | **9.71e-03** | **2.46e-02** | **S85** |

**Reading — RELAX-STRONG (not deepen, not plateau):**
- pythia-1b final-layer a_FAR,p = **9.71e-3** ≈ **30.7×** pythia-410m’s 3.16e-4.
- Still below gpt2-124M (1.42e-2) by ~1.5× and gpt2-medium (2.01e-2) by ~2.1×, but **orders of magnitude above** the suppressed 410m final layer.
- Within-family pythia curve is therefore **non-monotonic in depth/params**: 160m exact zero → 410m trickle (3e-4) with interior L21 island → **1b redistributes to a live final-layer foothold** (~1e-2).
- S84’s “family-dominated, not depth-dominated” claim is **refined, not overturned**: the *suppressed-final + interior-island* signature remains pythia-410m-specific among models tested; at 1B/16L the same family **relaxes** toward a gpt2-like smooth final foothold. Family is necessary but not sufficient — **scale within pythia erases the extreme final-layer suppression**.

Final-layer clean group mass (pythia-1b L15):
`sink0 0.525 / pre 0.043 / p 0.010 / car 0.202 / post 0.220` — sink-heavy with a real mid-sequence foothold (p≈1%), closer to gpt2 profiles (S81/S84) than to pythia-410m’s near-zero final p-mass (p≈0.0003 @s85 re-anchor).

### 3.2 Island check — does pythia-1b have an L21-style absolute allocation island?

**No.**

Late-half (L≥8) detector at ≥10× neighbors: **zero flags**.

| quantity | pythia-1b (S85) | pythia-410m L21 (S83 / S85 re-anchor) |
|----------|-----------------|----------------------------------------|
| late peak layer | **L14** (near-final) | **L21** (interior) |
| peak mean a_FAR,p | 1.22e-2 | 1.35e-2 |
| final mean a_FAR,p | **9.71e-3** | **3.16e-4** |
| peak / last-2 mean | **1.11×** | **~50.7×** (S85 re-anchor) |
| neighbor-ratio flags ≥10× | **none** | **L21 YES** (mean ×11.7, maxh ×22.4; top h11 a=0.162) |
| top head at peak | h1 @ 0.026 | **h11 @ 0.162** |
| head concentration | diffuse (top5: 0.026/0.020/0.018/0.013/0.008) | single-head island |

Per-layer late tail (mean a_FAR,p): L11 6.5e-3 → L12 6.9e-3 → L13 5.8e-3 → **L14 1.22e-2** → L15 9.7e-3. Mild near-final bump, not a collapse-after-spike. peak/last2 = 1.11× — the opposite of 410m’s interior island then final collapse.

S85 light re-anchor also **reproduced S83’s L21 island** on 410m under SEED=85: L21 mean 1.35e-2 (×11.7 neigh), maxh 0.191 (×22.4), top h11 a=0.162; peak/last2 = 50.7×. Apparatus and prior island claim remain intact.

### 3.3 Behavioral keep-only export @ inj12 (pythia-1b)

| regime | valence D/B | size D/B | note |
|--------|-------------|----------|------|
| B (noablate) | 0.816 | 0.906 | healthy baseline |
| k0 | **0.000** | **0.000** | structural |
| keep-L_inj (12) | **0.000** | **0.000** | structural |
| keep-L9 / keep-L11 (pre-inj controls) | **0.000** | **0.000** | no path before injection |
| **keep-L13 (=L_inj+1)** | **0.725** | **0.963** | law-peak present / dominant |
| **keep-L14 (late peak a_p)** | **0.956** | **0.776** | strongest / strong solo-export |
| **keep-L15 (final)** | **0.510** | **0.458** | usable final solo-export |

Findings:
- Relative-depth +1 peak transfers strongly (keep-L13 carries 0.73–0.96 of B) — consistent with S80/S82 depth-law.
- Late peak L14 is a **dominant solo exporter** (0.78–0.96) — allocation bump and export align.
- Final layer is a **usable solo exporter** (0.46–0.51), matching gpt2 final behavior (S80/S81/S84), **not** pythia-410m’s inert final.
- Pre-inj controls and structural zeros clean.

---

## 4. Verdicts

1. **Curve VALIDATE SUCCEEDED — RELAX-STRONG.** Third within-family pythia point: pythia-1b final-layer a_FAR,p = **9.71e-3** (~30.7× above 410m’s 3.16e-4; ~0.7× gpt2-124M). Suppression does **not** deepen or plateau at 1B; it **relaxes** toward gpt2-like live final allocation.
2. **Island check: NO island in pythia-1b.** No ≥10× neighbor spike in the late half; peak/last2 = 1.11× vs S83/S85-410m’s ~50×; late peak is near-final (L14) with diffuse head mass. **The L21 h11 absolute-layer island remains pythia-410m-specific among models tested**, not a generic pythia-family or 16L phenomenon.
3. **S84 family claim refined:** allocation suppression is still not a generic depth effect (gpt2-medium stayed live), but within pythia the suppressed-final signature is **scale-sensitive** — present at 410m/24L, absent at 1b/16L. Caveat: 1b is 16L not 24L, so depth and params are confounded; a 24L ≥1B pythia (if available) would separate them.
4. **410m re-anchor PASS:** final a_p = 3.162e-4 (matches S82); L21 island reproduced (h11, peak/last2 50.7×). Prior curve point and island claim hold under SEED=85 apparatus.
5. Apparatus: 7/7 gates, structural zeros bitwise, 181.4 s CPU.

**Workspace/GWT ledger note:** direct late readout remains allocation-limited, but the *shape* now has a third family-internal mode: pythia-160m final-zero; pythia-410m interior single-head island + final trickle; **pythia-1b smooth near-final foothold with strong keep-only export** (gpt2-like). Structural analogy only; no ignition/competition/capacity evidence; GWT analogy not upgraded.

---

## 5. Honest residue

1. **Depth × params confound** — pythia-1b is 16L / ~1B; pythia-410m is 24L / ~410M. Relax could be “fewer layers” rather than “more params.” A 24L ≥1B pythia (or intermediate 12–24L points) would unconfound. No such open-weight twin was in scope this session.
2. **Island detector is ratio-based on clean mean/max-head** — would miss a head that is strong in export contribution but not in raw a_p (S83 used both allocation *and* per-head W_O delta). pythia-1b L14 export is live *with* a mild a_p bump; no evidence of a hidden single-head island at final, but a cheap per-head keep-L14/L15 delta pass could still characterize contributor clusters.
3. **Single injection depth (inj12)** for export cells — enough for island behavioural counterpart and depth-law +1 check; full depth-law transfer on pythia-1b not re-run.
4. **Prompt set n=5, heavy-tail caveat** inherited from S80–S84.
5. **No causal head ablation** this session.
6. **S84 “do not prioritize another gpt2 island hunt unless pythia-1b shows gpt2-like final foothold”** — **trigger fired.** pythia-1b *does* show a gpt2-like final foothold. That reopens “scale erases islands / scale erases suppression” as a within-family claim, and weakens pure family essentialism. Next work should treat this as the new lead, not ignore the S84 escape hatch.

---

## 6. Proposed S86

Priority order (updated by S85 result):

1. **VALIDATE / ATTEMPT (primary): unconfound depth vs scale** — if a 24L pythia ≥1B (or intermediate) is available cheaply, run the same lean final-a_p + late scan. Else: run pythia-1.4b (24L, if open weights match) or document absence and pivot.
2. **ATTEMPT: S83 residue #3 closure** — per-head q·k geometry at L23 for h10/h8 under patch at inj12 vs inj18 on pythia-410m (still queued).
3. **Cheap causal on 410m:** zero h11@L21 in keep-L21 — decompositional → causal (still high value; island remains the unique anomaly).
4. **Optional:** per-head keep-only delta at pythia-1b L14/L15 to characterize the diffuse exporter set (not expected to be an “island”).
5. **Q3 (queued since S76):** looped/universal-transformer probe — still deferred.

Do **not** treat “pythia = suppressed final” as settled family law anymore; the 1b point falsifies the simple monotone-suppression reading.

---

## Provenance / human-review gate

- **VALIDATE, internal only. No external-facing claims published.**
- All numbers reproducible from `s85-validate-pythia1b-scale.py` (seed 85, deterministic greedy/teacher-forced pipeline); full log `s85-output.txt`.
- Models: `EleutherAI/pythia-1b` (16L, fp32, primary), `EleutherAI/pythia-410m` (24L, fp32, light re-anchor). CPU, venv `.venv-s75`. Wall-clock **181.4 s**.
- Outcome: **VALIDATE SUCCEEDED** — curve point added (pythia-1b a_FAR,p = 9.71e-3); **RELAX-STRONG** vs 410m; island = **NO**; 410m L21 island re-confirmed under SEED=85.

### Progress block (for orchestrator / unsolved_problems id=5)

```
S85 VALIDATE (2026-08-15, run #697, Track C): pythia-1b final-layer a_FAR,p = 9.71e-3
(max-head 2.46e-2); NO late island (peak L14, peak/last2=1.11×); curve reading
RELAX-STRONG vs pythia-410m 3.16e-4 (~30.7× lift, approaching gpt2-124M 1.42e-2).
keep-only @inj12: L13 D/B 0.73–0.96, L14 0.78–0.96, L15 0.46–0.51; structural zeros.
Optional 410m re-anchor: final a_p=3.162e-4; L21 island reproduced (h11, peak/last2 50.7×).
Gates 7/7 PASS. Wall-clock 181.4s CPU. Artifacts: s85-validate-pythia1b-scale.py,
s85-output.txt, s85-validate-pythia1b-scale.md. Proposed S86: unconfound depth vs
params (24L≥1B pythia if available); else S83 residue #3 / causal h11@L21.
```

### One-line thesis for reuse
> pythia-1b (16L) puts final-layer a_FAR,p at 9.71e-3 — ~30× above pythia-410m’s 3e-4 and within ~1.5× of gpt2-124M — with no interior absolute-layer allocation island (late peak L14 at only 1.11× last-2, diffuse heads, strong keep-only export), so within-family pythia allocation suppression is scale-sensitive rather than monotone: the S83 L21/h11 hotspot and final-layer trickle remain 410m-specific structure, while 1B relaxes toward a gpt2-like live final foothold.
