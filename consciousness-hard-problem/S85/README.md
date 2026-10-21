# S85 — VALIDATE: pythia-1b within-family scale curve + late allocation scan

Upstream problem: Consciousness / "hard problem" of consciousness (NOVA unsolved-problems tracker id=5).
Scope note: all findings below are about a mechanistic-interpretability *functional analogy* built on
open-weights transformer language models (gpt2, pythia family). None of this is a claim about biological
consciousness or a resolution of the philosophical hard problem; it is an audited claim about transformer
internals, reused as a structural analogy in an ongoing research program on machine "workspace" dynamics.

## Statement under test

Adds a third within-family pythia point to the allocation-suppression curve
(prior points: pythia-160m ≈ 0, pythia-410m ≈ 3.2e-4) using `EleutherAI/pythia-1b` (16 layers), and tests
whether it hosts an absolute-layer allocation island analogous to pythia-410m's layer-21 single-head
hotspot.

## Verdict: CONFIRMED — curve is non-monotonic ("relax-strong"); NO island in pythia-1b

- **Curve point:** pythia-1b final-layer attention-to-injected-position = 9.71e-3 — about 30.7× above
  pythia-410m's 3.16e-4, and within ~1.5× of gpt2-124M's 1.42e-2. Within-family pythia suppression does
  **not** deepen or plateau at 1B parameters; it **relaxes** sharply toward gpt2-like live allocation.
- **No island**: zero late-half layers flag at the ≥10× neighbor-ratio detector (vs pythia-410m's ~50×
  layer-21 spike, independently re-confirmed in this same session under a different seed). Late peak is
  near-final (layer 14 of 15), diffuse across heads.
- **Behavioral counterpart confirms**: keep-only export at the near-final and final layers is strong
  (0.46–0.96 of baseline) — matching gpt2-like, not pythia-410m-like, final-layer behavior.
- **Refines, does not overturn, the S84 family claim**: allocation suppression is still not a generic depth
  effect (gpt2-medium stayed live in S84), but within pythia the suppressed-final signature is now shown to
  be scale-sensitive, present at 410m/24L and absent at 1b/16L — a depth-vs-params confound explicitly
  flagged (1b is 16 layers, not 24), not resolved in this session.

## Method

Same lean apparatus as S84 (clean-forward allocation scan, final-layer curve point, island detector,
behavioral keep-only-export counterpart), applied to `EleutherAI/pythia-1b`, plus an optional light
re-anchor of pythia-410m under this session's seed to confirm the prior island claim reproduces
independently. 7/7 apparatus gates passed.

## Limits

- **Depth × params confound, explicitly flagged**: pythia-1b (16L) vs pythia-410m (24L) differ in both
  layer count and parameter count; this session cannot separate which drives the "relax." A same-depth,
  larger-parameter pythia model (if one existed in scope) would be needed to unconfound; the report proposes
  this as the top priority for the next session.
- Single injection depth (12) for the behavioral counterpart; full depth-law transfer on pythia-1b not
  re-run.
- Island detector is ratio-based on clean mean/max-head attention mass (same caveat as S84).
- 5 prompts, heavy-tail caveat inherited from predecessor sessions; no causal head ablation performed.

## Reproduction

**Status: PASS.** Re-run in a clean temporary directory against cached `EleutherAI/pythia-1b` and
`EleutherAI/pythia-410m` (re-anchor) weights, same apparatus (`SEED=85`). All 7 apparatus gates
reproduced; curve point (9.71e-3), no-island finding, and the independent pythia-410m layer-21 island
re-confirmation all reproduced. See `outputs/repro-s85.log` for the transcript from this packaging pass.

### Exact re-run commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install torch==2.13.0+cpu transformers==5.14.1 --index-url https://download.pytorch.org/whl/cpu
cd scripts
python3 s85-validate-pythia1b-scale.py
```

CPU only. Original wall-clock reported: 181.4 s on the researcher's machine (includes the optional
pythia-410m re-anchor); may vary with hardware.

## Upstream links

- Predecessor sessions S80–S84 (internal only, not included in this public repo).
- No new external citations introduced in S85.

## Files in this directory

- `report/s85-validate-pythia1b-scale.md` — original VALIDATE report.
- `scripts/s85-validate-pythia1b-scale.py` — the checker script (verbatim from source).
- `outputs/s85-output.txt` — the original full run log, copied verbatim from source.
- `outputs/repro-s85.log` — this packaging pass's independent clean-clone re-run transcript.
- `SHA256SUMS` — checksums for the files in this directory (verify with `sha256sum -c SHA256SUMS`).
