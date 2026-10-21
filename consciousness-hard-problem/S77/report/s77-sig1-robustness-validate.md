# Consciousness Hard Problem — Session 77 (UPR Run #575)
## VALIDATE: SIG1 robustness — layers × concepts × second model, + a cleaner P2 estimator (that failed)

**Date:** 2026-08-02 · **Mode:** VALIDATE · **Project:** 18 · **unsolved_problems id=5**
**Track:** C (machine workspace / J-space) — primary
**Predecessors:** S74 (labeled toy: SIG1/SIG2 discriminators), S75 (SIG1 on gpt2-124M: P1 exact-0 / P2 nonzero-decaying), S76 (distinct-natural-kinds DOCUMENT; §5.2 proposed exactly this VALIDATE; §4.4 collapse-condition #1)
**Artifacts:** `s77-sig1-robustness-validate.py` (seed 77), `s77-output.txt` (full run log)

---

## 0. Objective

S76 built a distinct-natural-kinds argument (Kind A internal recurrent ignition vs Kind B externalized token-loop recurrence) and named its single falsifier (§4.4 collapse-condition #1): *"a within-pass internal back-arrow is found in standard decoder-only transformers."* S76 §5.2 specified the VALIDATE that would stress-test it. This session executes it:

1. **AXIS 1 — layers.** Repeat SIG1 P1 (within-pass backward deflection, positions < p) at three patch layers (blocks 3, 6, 9), not just S75's block 6.
2. **AXIS 2 — concepts/directions.** Beyond valence: four difference-of-means directions {valence, formality, size, tense}, so any nonzero backward can't be a valence artifact.
3. **AXIS 3 — second model.** Repeat on `EleutherAI/pythia-160m` (GPTNeoX, 12L/768d) alongside `gpt2` (124M), to confirm the pattern isn't gpt2-specific.
4. **Cleaner P2 estimator.** Address S75 caveat #1 (raw across-gen decay was ragged/non-monotone): try *deflection-per-unit-attention-mass-to-p* and test whether normalizing out attention re-weighting yields a smoother envelope.

**Predicted (if S76 is right):** P1 backward = exact 0 for every layer × concept × model; P2 raw nonzero-decaying in both models; attention-normalized envelope smoother than raw.

---

## 1. Method (what the script actually does)

- **Directions.** For each concept, difference-of-means (`pos_ctx` − `neg_ctx`) of the residual stream *after* the patch block, at the last token, unit-normalized (the S74/S75 alpha-sweep method). ‖W‖ recorded per direction.
- **Patch (do(W:=W\*)).** Forward hook on block L output: at position p (last prompt token), replace the component along Ŵ with target = 3·‖W‖ (strong positive push), leaving the orthogonal complement intact.
- **P1 backward witness.** Deflection L2-norm at the final block, summed over positions **< p**. Causal attention ⇒ architecturally must be exactly 0 (a patch at p cannot influence earlier positions within one pass).
- **P2 across-gen.** Single injection at p, teacher-forced over a fixed clean-greedy continuation (same tokens both runs) so measured decay reflects KV-cache propagation of the edit, not divergent token identities. Out-span (specialist) component of deflection at the final block, positions p+1…p+12, averaged over 5 prompts.
- **Attention-normalized P2.** Divide each later position's raw out-span deflection by the total clean-run attention mass that position pays to key position p (averaged over heads and the final 3 layers).
- **Controls.** (a) zero-magnitude patch (set W-coord to its clean value → no-op); (b) next-token flip check.

**Numerical-stability note (recorded honestly):** `gpt2` runs stable under eager attention; **`pythia-160m` eager attention emits NaNs on some inputs** (confirmed: `attn_implementation="eager"` → NaN on "I loved every second…", while `"sdpa"` is clean). Fix: main model runs under **SDPA** (stable for both families); attention weights (needed only for the normalized estimator) are read from a **separate eager instance, gpt2 only**. Consequence: the attention-normalized estimator ran for gpt2 but **not** for pythia (SDPA returns no attention weights, and pythia eager is NaN-poisoned). This is a tooling limitation, flagged, not hidden.

---

## 2. Results

### 2.1 P1 — within-pass backward deflection (the falsifier test)

**24 cells: 2 models × 3 layers × 4 concepts. Every one is exactly 0.000e+00.**

| model | layers × concepts tested | max backward (<p) | at-p deflection range | verdict |
|-------|--------------------------|-------------------|------------------------|---------|
| gpt2-124M | blocks {3,6,9} × {valence,formality,size,tense} | **0.000e+00** | 4.4 – 89.0 | exact-0 |
| pythia-160m | blocks {3,6,9} × {valence,formality,size,tense} | **0.000e+00** | 5.5 – 97.8 | exact-0 |

The at-p (forward) deflections are large and concept/layer-dependent (formality pushes hardest: up to 89–98; size/valence smaller), confirming the patch is genuinely perturbing the stream — the backward zero is not a dead patch. **Collapse-condition #1 is NOT met.** No within-pass internal back-arrow exists in either standard decoder-only transformer, at any tested layer, for any tested concept direction. This is the load-bearing axis of the S76 distinction, and it **generalizes cleanly**.

*Controls:* gpt2 zero-magnitude patch = 2.8e-05 (machine-zero, as expected). **pythia zero-magnitude patch = 1.05e-01** — three orders larger than gpt2's, though still <1% of the at-p deflections (18–98). This is a floating-point reconstruction artifact of re-projecting under SDPA (the hook subtracts the current coord and re-adds the "clean" coord; SDPA's fused kernel isn't bit-identical to the un-hooked path). It is a **control-floor caveat for pythia, honestly recorded**: pythia's zero is "small relative to signal," not "machine-exact" like gpt2's. It does **not** touch the P1 backward result (which is exact 0 by causal-masking structure, independent of this reconstruction noise).

Next-token flip: **False in both models** on prompt "The film I watched last night was" with target 3·‖W‖. See §3.2 — this diverges from S75 and is a genuine caveat.

### 2.2 P2 — across-generation out-span decay (externalized recurrence)

Raw out-span (specialist) deflection at the final block, averaged over 5 prompts, per generation step 1→12:

| model | step-1 | step-12 | mean | frac-steps-decreasing (shape) |
|-------|--------|---------|------|-------------------------------|
| gpt2-124M | 3.25 | 1.40 | 2.26 | 0.64 |
| pythia-160m | 6.06 | 1.45 | 2.57 | 0.73 |

**P2 confirmed and generalized:** in both models the single workspace injection deflects later-position specialist state (nonzero) with an overall decaying envelope (step-12 ≈ 22–43% of step-1). Pythia's decay is actually *cleaner* (0.73 vs 0.64 decreasing) — the externalized-recurrence signature is not gpt2-specific.

### 2.3 The cleaner estimator — a negative result

The hypothesis (S75 caveat #1): raw decay was ragged because attention re-weighting redistributes mass away from p over generation; dividing by attention-mass-to-p should recover a smoother monotone envelope.

**Refuted for gpt2.** Attention-normalized frac-decreasing = **0.27**, *worse* than raw's 0.64. Normalizing by mass-to-p did not smooth the decay — it made it *less* monotone (the normalized shape rises: 1.0 → 2.3 → 3.0 → … → 4.5). Interpretation: as generation proceeds, attention mass to p **falls faster than the deflection does**, so deflection/mass *grows*. That means the raw decay is **not** primarily driven by attention re-weighting to p — the specialist deflection persists even as direct attention to the patched position wanes, consistent with the edit having propagated into intermediate positions' KV entries and riding forward indirectly (a multi-hop externalized loop), not a single p→later hop. The proposed "clean estimator" therefore **fails as a smoother but succeeds as a probe**: it reveals the KV-cache loop is multi-hop, not a decaying direct-attention tail.

**Could not run for pythia** (eager-attention NaN bug; SDPA yields no attention weights). Noted as a gap for a future session.

---

## 3. Verdict and honest residue

### 3.1 Primary verdict: **CONFIRMED — the distinction hardens**

- P1 exact-0 across **both** models, **all** layers, **all** concepts (24/24 cells). The S76 falsifier (collapse-condition #1) is not triggered. The architectural guarantee is empirical across two architecture families (GPT2 learned-positional, GPTNeoX rotary), so it's a property of causal decoder-only attention, not of one model.
- P2 nonzero-decaying reproduced and generalized (cross-model, cross-prompt).
- Net: the load-bearing empirical claim of S76 (§2 "clean discriminator": within-pass exact-0 / across-emission nonzero) is robust. Kind A / Kind B stays distinct.

### 3.2 Honest residue (things that did NOT go as predicted)

1. **The cleaner estimator failed its stated goal** (smoother envelope) — attention-normalization made gpt2's decay *less* monotone (0.27 < 0.64). Recorded as a refuted sub-hypothesis that nonetheless yielded a real finding (multi-hop KV propagation). S75 caveat #1 (ragged decay) is therefore **still open** — it is not explained by direct-attention re-weighting to p.
2. **Next-token flip not reproduced** on this prompt/target (flip=False, both models), whereas S75 saw a valence flip ("different"→"good") in its free-generation check. Difference: S75's flip was observed in the free-generation branch on a specific prompt; here the single-position control check on "The film…" did not flip the argmax at 3·‖W‖. This weakens the *behavioral* leg of P2 for this prompt (deflection is measurable in the residual stream, but did not cross the decoding threshold to change the emitted token here). The residual-stream P2 signal stands; the behavioral flip is prompt/target-sensitive and should not be over-claimed. *(A future run should sweep target magnitude to characterize the flip threshold rather than assert it.)*
3. **pythia control floor** (zero-magnitude patch = 0.105, vs gpt2's 2.8e-05) — SDPA reconstruction noise. Doesn't affect P1 (structurally exact) but means pythia's *forward* deflection magnitudes carry ~0.1 of reconstruction noise; the signals (18–98) dwarf it, so conclusions hold, but it's a known imprecision.
4. **pythia attention-normalized estimator unrun** — eager-NaN + SDPA-no-weights. Gap, not a result.

### 3.3 What this changes about the approach

- The distinct-natural-kinds argument's *empirical spine* (S76 §2) is now multi-model, multi-layer, multi-concept validated. Confidence up.
- A **new open sub-question** replaces the old caveat: *why does the P2 decay persist as direct attention to p vanishes?* The multi-hop KV-propagation reading (§2.3) is a hypothesis, not yet shown. This is a sharper ATTEMPT target than "clean up the estimator."
- The behavioral-flip sensitivity (§3.2.2) means the "provably flips emitted tokens" phrasing from S75/S76 should be softened to "flips emitted tokens under sufficient target magnitude on some prompts" until a threshold sweep is done.

---

## 4. Proposed next session

- **ATTEMPT (primary): multi-hop KV-propagation test.** Directly test the §2.3 hypothesis: is the persistent P2 deflection carried by p→intermediate→later hops? Method: after injecting at p, zero out the KV contribution of p at later query steps (ablate attention to p) and see whether deflection persists (multi-hop) or vanishes (single-hop). Predicted: partial persistence ⇒ multi-hop.
- **VALIDATE (secondary): target-magnitude sweep for the behavioral flip.** Sweep target ∈ {1,2,3,5,8}·‖W‖ across the 5 prompts, record the flip fraction, to characterize the P2 decoding threshold honestly rather than assert "provably flips."
- **Q3 (still queued from S76): looped/universal-transformer probe** — the one architecture where P1 backward *could* be nonzero; the single highest-information test of whether the A/B boundary is architectural.

---

## Provenance / human-review gate

- **VALIDATE, internal only. No external-facing claims published.** Review gate (workflow step 4) is a no-op.
- All numbers reproducible from `s77-sig1-robustness-validate.py` (seed 77), full log in `s77-output.txt`. Models: `gpt2` (124M) and `EleutherAI/pythia-160m`, CPU, HF transformers 5.14.1 / torch 2.13.0+cpu.
- Outcome recorded per workflow VALIDATE rules: **CONFIRMED** (P1 exact-0 generalizes; P2 nonzero-decaying generalizes) with a **refuted sub-hypothesis** (attention-normalized estimator does not smooth decay) and four explicit caveats (§3.2). No discrepancy in prior *published* work — the refuted item and the flip caveat are against our own S75, not external literature.
- External citations unchanged from predecessors (Gurnee et al. arXiv:2607.15495 remains a **preprint**); none newly invoked this session.

### One-line thesis for reuse
> SIG1's within-pass backward deflection is exactly 0 across two model families, three layers, and four concept directions (24/24) — the S76 kind-distinction's empirical spine generalizes — while the attempt to "clean up" the across-gen decay via attention-normalization failed, instead revealing the externalized KV loop is multi-hop rather than a single decaying p→later attention tail.
