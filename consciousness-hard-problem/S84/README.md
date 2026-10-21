# S84 — VALIDATE: scale allocation curve + 24L family-outgroup island check (gpt2-medium)

Upstream problem: Consciousness / "hard problem" of consciousness (NOVA unsolved-problems tracker id=5).
Scope note: all findings below are about a mechanistic-interpretability *functional analogy* built on
open-weights transformer language models (gpt2, pythia family). None of this is a claim about biological
consciousness or a resolution of the philosophical hard problem; it is an audited claim about transformer
internals, reused as a structural analogy in an ongoing research program on machine "workspace" dynamics.

## Statement under test

Adds a third point to a final-layer "allocation suppression" curve (prior points: pythia-160m ≈ 0,
pythia-410m ≈ 3e-4, gpt2-124M ≈ 1.5e-2) using a 24-layer gpt2-family model (`gpt2-medium`), and tests
whether that model has its own absolute-layer allocation "island" (analogous to pythia-410m's single-head
layer-21 hotspot).

## Verdict: CONFIRMED (allocation suppression is a family trait, not a depth effect); NO island in gpt2-medium

- **Curve point added:** gpt2-medium final-layer attention-to-injected-position = 2.01e-2 — slightly above
  gpt2-124M (1.42e-2, re-anchored under this session's seed) and ~60× above pythia-410m (3.16e-4).
  gpt2-family allocation is live and scale-stable; pythia-family remains the suppressed branch.
- **No island in gpt2-medium**: zero late-half layers flag at the ≥10× neighbor-ratio detector (vs
  pythia-410m's 40–60× spike at layer 21). The late peak is the final layer itself, rising only mildly
  (1.4×) into it, with diffuse head mass (no single dominant head).
- Conclusion: allocation suppression and the single-head allocation island are **family-specific structure**
  (observed in the pythia line), not a generic consequence of 24-layer depth.

## Method

A lean variant of the S78–S83 apparatus: clean-forward allocation scan across all layers (injection-
independent), a final-layer curve point, an automated island detector (≥10× neighbor-ratio flag), and a
behavioral keep-only-export counterpart at one injection depth (18) for two concepts. 7/7 apparatus gates
passed.

## Limits

- Within-family pythia scale curve still only had two points at the time of this session (160m, 410m); a
  third pythia point (1b) was explicitly deferred to the next session (S85).
- Island detector is ratio-based on clean mean/max-head attention mass; it could in principle miss a head
  that contributes strongly to export without a raw attention-mass spike (flagged, not ruled out).
- Single injection depth (18) for the behavioral counterpart; full depth-law transfer on gpt2-medium was not
  re-run (out of scope for this session's question).
- 5 prompts, heavy-tail caveat inherited from predecessor sessions; no causal head ablation performed.

## Reproduction

**Status: PASS.** Re-run in a clean temporary directory against cached `gpt2-medium` and `gpt2` (re-anchor)
weights, same apparatus (`SEED=84`). All 7 apparatus gates reproduced; curve point (2.01e-2) and
no-island finding reproduced. See `outputs/repro-s84.log` for the transcript from this packaging pass.

### Exact re-run commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install torch==2.13.0+cpu transformers==5.14.1 --index-url https://download.pytorch.org/whl/cpu
cd scripts
python3 s84-validate-scale-allocation.py
```

CPU only. Original wall-clock reported: 61.1 s on the researcher's machine; may vary with hardware.

## Upstream links

- Predecessor sessions S80–S83 (internal only, not included in this public repo).
- No new external citations introduced in S84.

## Files in this directory

- `report/s84-validate-scale-allocation.md` — original VALIDATE report.
- `scripts/s84-validate-scale-allocation.py` — the checker script (verbatim from source).
- `outputs/s84-output.txt` — the original full run log, copied verbatim from source.
- `outputs/repro-s84.log` — this packaging pass's independent clean-clone re-run transcript.
- `SHA256SUMS` — checksums for the files in this directory (verify with `sha256sum -c SHA256SUMS`).
