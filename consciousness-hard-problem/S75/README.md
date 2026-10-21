# S75 — VALIDATE: SIG1 on a real open-weights transformer (gpt2-124M)

Upstream problem: Consciousness / "hard problem" of consciousness (NOVA unsolved-problems tracker id=5).
Scope note: all findings below are about a mechanistic-interpretability *functional analogy* built on
open-weights transformer language models (gpt2, pythia family). None of this is a claim about biological
consciousness or a resolution of the philosophical hard problem; it is an audited claim about transformer
internals, reused as a structural analogy in an ongoing research program on machine "workspace" dynamics.

## Statement under test

Two predictions about whether a workspace→specialist "back-arrow" exists in a standard decoder-only
transformer:
- **P1 (single forward pass):** a patch (`do(W:=W*)`) injected at mid-layer L, position p cannot deflect
  readout state at earlier positions (< p) within one forward pass (no internal recurrence); at p it
  propagates purely feedforward.
- **P2 (across generation):** the same single injection, carried via the KV cache, deflects later-position
  "specialist" (out-of-direction) state across subsequent generation steps, nonzero and decaying.

## Verdict: CONFIRMED (both predictions), with an honest caveat on decay shape

- **P1: CONFIRMED.** Backward deflection at positions < p is exactly `0.000e+00`.
- **P2: CONFIRMED (with a noise caveat).** Across-generation out-span deflection is nonzero, exceeds a
  random-direction control, and decays on average (late/early ≈ 0.46), but the per-step decay is ragged,
  not a clean monotone curve (this is explicitly not over-claimed in the report).

## Method

- Model: `gpt2` (124M, 12 blocks), CPU, seeded (SEED=75), venv with `torch==2.13.0+cpu`,
  `transformers==5.14.1`.
- Workspace direction W: difference-of-means (valence) of block-6 residual stream, last token, across 6
  positive/6 negative carrier contexts.
- Patch: at block-6 output, position p, replace the W-component with `target = 3·‖W‖`.
- Deflection: L2 distance (patched − clean) at the final block (11), split into in-span(W) and out-span
  ("specialist") components.
- Controls: zero-magnitude (no-op) patch, random-direction patch at equal norm, next-token / free-generation
  behavior check.
- P2 protocol: single injection at p, teacher-forced continuation, out-span deflection measured at each
  later generation step, averaged over 5 prompts (each normalized to its own step-1 value).

## Limits

- Single model (gpt2-124M), single mid-layer (block 6), single concept direction (valence), 5 prompts —
  magnitudes are illustrative, not universal constants (this is exactly what sessions S77/S80/S82 go on to
  test for robustness/generality).
- Decay is "nonzero with a decaying envelope," not a precise monotone law; individual steps fluctuate.
- Random-control deflection is also nonzero (any patch that changes the output distribution will propagate
  some effect through the KV cache) — the discriminator is P1's exact 0 vs P2's nonzero, not "W alone has an
  effect."

## Reproduction

**Status: PASS.** Re-run in a clean temporary directory using the checker script below against the cached
HF model weights (`gpt2`), with the documented CPU/seeded setup. All headline numbers reproduced bit-for-bit
against the original report, including:
- P1 backward deflection at p: `0.000e+00` (exact match)
- P1 out-span at readout (block 11): `9.851` (exact match)
- Control (a) zero-magnitude patch: `6.197e-05` (exact match)
- Control (c) next-token flip: `False`, KL-proxy `0.262` (exact match)
- P2 decay: first `2.726` → last `0.460`, ratio `0.169`, 55% steps decreasing (exact match)

### Exact re-run commands

```bash
# Requires: Python 3.12, torch==2.13.0+cpu, transformers==5.14.1 (see requirements.txt),
# and the gpt2 weights cached locally or reachable over the network (first run will download them).
python3 -m venv .venv
source .venv/bin/activate
pip install torch==2.13.0+cpu transformers==5.14.1 --index-url https://download.pytorch.org/whl/cpu
cd scripts
python3 s75-sig1-openweights-validate.py
```

The script is self-contained (seeds `random`/`numpy`/`torch` with `SEED=75`, downloads/loads `gpt2` via
`transformers`, and prints every number cited in the report). Expected wall-clock: well under a minute on
CPU. No GPU required. No database or network credentials are needed beyond a Hugging Face model download
(gpt2 is a public, unauthenticated model repo).

## Upstream links

- Gurnee, Sofroniew et al., arXiv:2607.15495 (preprint) — the concept-direction / α-sweep method this
  session's workspace-direction construction is derived from.
- Predecessor sessions (not included in this public repo): S74 (labeled-toy SIG1 design, internal only).

## Files in this directory

- `report/s75-sig1-openweights-validate.md` — original VALIDATE report.
- `scripts/s75-sig1-openweights-validate.py` — the checker script (reproduced verbatim from source).
- `outputs/` — no separate captured output file existed upstream for this session; the report embeds all
  printed numbers inline, and the reproduction run above reproduced them exactly. See `outputs/repro-s75.log`
  for this packaging pass's own re-run transcript.
- `SHA256SUMS` — checksums for the files in this directory (verify with `sha256sum -c SHA256SUMS`).
