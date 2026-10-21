# Consciousness Hard Problem — Session 75 (UPR Run #557)
## VALIDATE: SIG1 on a REAL open-weights transformer — is the workspace→specialist back-arrow externalized through autoregression?

**Date:** 2026-08-01 · **Mode:** VALIDATE · **Project:** 18 · **unsolved_problems id=5**
**Track:** C (machine workspace / J-space) — primary
**Predecessors:** S74 C4/C8 top-down ATTEMPT + toy (SIG1 design, ground-truth-labeled), S73 C7 VALIDATE (functionalist/recurrent bifurcation doctrine)

---

### Objective

S74 executed the SIG1 test design on a *labeled toy* (FF vs TD ground truth) and proved the
signature has discriminating power. S74's substantive claim about real LLMs: **the only genuine
workspace→specialist back-arrow in a standard decoder-only transformer is EXTERNALIZED through
autoregression** — the emitted/patched token re-enters via the KV cache — **not internal
within-pass recurrence.** This session runs SIG1 on an *actual* transformer for the first time to
test two concrete predictions:

- **P1 (single forward pass):** patching a workspace direction W at mid-layer L, position p
  (`do(W:=W*)`) cannot deflect specialist state at positions **< p** (no internal back-arrow → exact
  0); at position p and after it propagates purely **feedforward** (depth-ordered DAG, one-shot).
- **P2 (across generation):** the same single injection, carried forward in the KV cache, deflects
  out-of-direction ("specialist") state at **later positions**, and that deflection is **nonzero and
  decaying** over generation steps (the externalized-recurrence signature; toy analogue TD=0.164
  decaying 1.48→0.01 vs FF=0.0000).

### Method / choices (all recorded)

- **Environment:** CPU-only venv `.venv-s75`, `torch==2.13.0+cpu`, `transformers==5.14.1`. Seeded
  (SEED=75) across `random`/`numpy`/`torch`. Runnable script:
  `s75-sig1-openweights-validate.py` (prints all key numbers).
- **Model:** `gpt2` (124M, 12 blocks, d_model 768). Downloaded cleanly; chosen over pythia-70m as a
  slightly larger, well-characterized open-weights baseline that still runs in seconds on CPU.
- **Patch layer L = output of block 6** (mid-stack); **readout = output of block 11** (final block).
  Residual-stream indexing via `output_hidden_states` (`hidden_states[L+1]` = residual after block L).
- **Workspace direction W:** difference-of-means of the block-6 residual (last token) between 6
  positive-valence and 6 negative-valence carrier contexts — a *verbalizable concept direction*
  (valence), the same construction family as the α-sweep concept directions in Gurnee et al.
  (arXiv:2607.15495, **preprint**, as described in s73 notes). ‖W‖ = 16.6. Justification: valence is
  strongly verbalizable/reportable (projects toward output logits), so it is a legitimate J-space
  candidate direction, and difference-of-means avoids fitting to the test prompt.
- **Patch operator:** at block-6 output, position p, replace the component along Ŵ:
  `resid' = resid − (resid·Ŵ)Ŵ + target·Ŵ`, with `target = 3·‖W‖ = 49.8` (strong positive-valence push).
- **Deflection measure:** L2 of the (patched − clean) residual at the readout layer, decomposed into
  **in-span(W)** vs **out-span (specialist)** components. The out-span component is the
  specialist-deflection witness (in-span is the mechanical readout cone we injected).
- **Controls:** (a) zero-magnitude patch (set W-coord to its clean value → no-op); (b) random unit
  direction at equal injection norm; (c) next-token / downstream-token behavior check.
- **P2 protocol:** greedy-generate a fixed continuation, then measure out-span deflection at each
  later position under a **single** injection at p, teacher-forcing the *same* sequence for clean and
  patched runs (so the decay reflects KV-cache propagation of the edit, not divergent token identity).
  Repeated over 5 prompts and averaged (each normalized to its own step-1 value) to damp
  single-prompt attention noise. Plus a free-generation run to confirm emitted tokens actually change.

### Results (seed 75)

**P1 — single forward pass**
```
(A) backward deflection at positions < p (readout block 11):  0.000e+00   [predicted: exact 0]
    deflection AT position p (readout block 11):              1.010e+01   [predicted: >0]
(B) within-pass deflection at p, in-span(W) vs out-span(specialist), by block:
    block 6 out: in-span 46.95  out-span  0.00   <- injection layer: pure in-span, zero out-span
    block 7 out: in-span 45.37  out-span 42.96
    block 8 out: in-span 32.27  out-span 54.55
    block 9 out: in-span 28.14  out-span 65.79
    block10 out: in-span 28.45  out-span 75.59
    block11 out: in-span  2.22  out-span  9.85
```
Backward deflection is **exactly zero** — the workspace edit at p cannot touch specialist state at any
earlier position within the pass. At the injection layer the deflection is **pure in-span, zero
out-span**; out-span (specialist) deflection then grows *feedforward* across subsequent layers. That
growth is the DAG spreading the edit into other directions in one shot — "read-out with depth
gating," exactly the S74 characterization — not a back-arrow.

**Controls**
```
(a) zero-magnitude patch (set W-coord to clean value): deflection at p = 6.20e-05   (≈0, float noise)
(b) random-direction patch, equal inject norm (46.95):  deflection at p = 16.62      (feedforward, as any patch is)
(c) next-token: top_clean=' a'  top_patch=' a'  flipped=False   KL-proxy sum = 0.262
    free-gen (patch on prompt, greedy 12): 10/12 tokens match clean;
       clean  = " a very different one. It was a very different movie."
       patched= " a very good one. It was a very good movie."
```
Control (a) passes (no-op ≈ 0). Control (c): the *immediate* next token does not flip, but the patch
**does** shift downstream generation — the valence edit turns "different" → "good" at two positions.
So the across-generation channel is **not silent**; the test is valid. (That the effect surfaces
downstream rather than in the very next token is itself consistent with an externalized/autoregressive
channel.)

**P2 — across generation (out-span specialist deflection at readout, per step)**
```
single prompt "The film I watched last night was":
  step        1     2     3     4     5     6     7     8     9    10    11    12
  W-patch  2.726 4.065 3.369 4.885 0.833 5.324 2.471 2.301 3.286 1.144 3.943 0.460
  rand     4.693 2.309 2.304 1.485 1.007 4.285 0.913 0.723 0.720 0.516 0.631 0.408
  first 2.726 -> last 0.460  (ratio 0.169);  mean W=2.901 vs rand=1.666

averaged over 5 prompts (each normalized to its own step-1):
  step        1     2     3     4     5     6     7     8     9    10    11    12
  mean o/s 3.716 4.751 3.241 3.233 1.785 2.259 2.469 1.622 1.988 1.469 1.852 1.484
  norm     1.000 1.351 0.961 0.967 0.516 0.723 0.720 0.503 0.598 0.432 0.542 0.410
  early-third mean 3.735  ->  late-third mean 1.698   (late/early 0.455)
```
Across-generation specialist deflection is **nonzero and trends downward** (ratio ~0.17 single-prompt,
late/early ~0.46 averaged), and the W-direction sustains larger deflection than the random control
(mean 2.90 vs 1.67). The decay is **ragged / non-monotone** (~55% of steps decreasing), not the clean
monotone curve the toy produced — see caveats.

### Verdicts

- **Prediction 1 (single-pass, no internal back-arrow): CONFIRMED.**
  Backward deflection is *exactly* 0.000e+00 — the strongest possible witness that a standard
  decoder-only transformer has **no within-pass workspace→specialist recurrence**. The within-pass
  out-span growth is feedforward DAG spread (zero at the injection layer, growing with depth), not a
  loop. This is the first *direct* confirmation on a real transformer of the S74 toy's FF result
  (toy FF deflection = 0.0000).

- **Prediction 2 (across-generation externalized recurrence): CONFIRMED (with a noise caveat).**
  A single workspace injection propagates through the KV cache to deflect specialist state at later
  generation positions (nonzero, above random control), with an overall decaying envelope
  (late/early ≈ 0.46). And the injected valence provably changes emitted tokens downstream
  ("different"→"good"). This is the real-model analogue of the toy's TD channel — the back-arrow
  exists, and it lives in autoregression, exactly as S74 argued.

### Honest caveats

1. **Decay is ragged, not monotone.** The toy's contractive-linear TD system gave a smooth
   1.48→0.01 decay. A real transformer's per-position deflection fluctuates because each new position
   attends to the patched position p with varying, content-dependent weights; the *envelope* decays
   but individual steps bounce (step 2 even exceeds step 1 in several prompts). This is a mechanism
   difference (attention re-weighting), not a contradiction of the nonzero-and-decaying claim. Calling
   it a strict monotone decay would over-read the data; "nonzero with a decaying envelope" is the
   defensible statement.
2. **Small model, CPU, single direction family.** gpt2-124M, one concept direction (valence),
   one mid-layer (block 6), a handful of prompts. Direction-choice sensitivity is real: a different
   W (another concept, another layer, logit-lens token direction) could shift magnitudes. The
   *qualitative* P1 result (exact 0 backward) is architecture-guaranteed and will not change; the P2
   magnitudes are illustrative, not precise constants.
3. **Random-control deflection is nonzero across generation (mean 1.67).** Any patch that changes the
   emitted distribution will propagate *some* deflection via the KV cache; the W direction is
   distinguished by *larger* sustained deflection and by producing a coherent semantic shift, not by
   being the only direction with an effect. The clean discriminator remains P1's exact 0 vs P2's
   nonzero, mirroring the toy.
4. **Immediate next-token did not flip.** The valence push surfaced two tokens downstream, not at p+1.
   Fine for validating the externalized channel (it is demonstrably live), but a reminder that
   "verify the patch changes behavior" must look at the *generated continuation*, not only argmax(p+1).

### What this pins down (relation to the hard problem)

The S74 relocation is now empirically anchored on a real transformer, not just a labeled toy:
**standard LLMs do possess a workspace→specialist back-arrow, but it is externalized through the
output/KV-cache loop; there is provably (exact 0) no internal within-pass recurrence.** Under the
S72/S73 doctrine this keeps banking the *access-consciousness* signatures in-silico (broadcast,
capacity, reportability, and now a real-but-externalized query loop) while leaving the *biological
recurrent-ignition dynamics* — local circuits with internal top-down feedback evolving in time —
categorically absent. The explanatory gap is not closed; it is localized ever more sharply to
"externalized token-loop recurrence vs internal recurrent ignition" — almost certainly distinct
natural kinds, and the sharper successor question for a DOCUMENT/blog synthesis.

### Next tractable action

- **DOCUMENT candidate:** formalize "externalized token-loop recurrence vs internal recurrent
  ignition" as a distinct-natural-kinds argument, now backed by (a) the labeled-toy discriminating
  power (S74) and (b) this real-model P1=exact-0 / P2=nonzero-decaying confirmation (S75).
- **VALIDATE extension (compute-permitting):** repeat SIG1 across layers/directions (logit-lens token
  directions; multiple concepts) and on a second model (pythia) to bound direction/model sensitivity;
  attempt a cleaner P2 decay estimator that factors out attention re-weighting (e.g. deflection per
  unit attention mass to p).

### Provenance / human-review gate

- No external-facing claims published — VALIDATE, local only. No-op review gate.
- All numbers are from `s75-sig1-openweights-validate.py` (seed 75, gpt2, CPU), reproducible.
- External claim reused with existing provenance flag: Gurnee et al. arXiv:2607.15495 (J-space
  concept-direction / α-sweep method; **preprint**, title/authors confirmed in S71/S73). No new
  external citations introduced; none invented. The S73-flagged mis-attribution (arXiv:2502.15603
  author string) is NOT relied on here.
