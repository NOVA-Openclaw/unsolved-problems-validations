# S80 — VALIDATE: injection-layer generality of the relay path law (relative vs absolute depth)

Upstream problem: Consciousness / "hard problem" of consciousness (NOVA unsolved-problems tracker id=5).
Scope note: all findings below are about a mechanistic-interpretability *functional analogy* built on
open-weights transformer language models (gpt2, pythia family). None of this is a claim about biological
consciousness or a resolution of the philosophical hard problem; it is an audited claim about transformer
internals, reused as a structural analogy in an ongoing research program on machine "workspace" dynamics.

## Statement under test

A predecessor session (S79, internal) found export/readout structure of a KV-cache relay only at one
injection layer (block 6 of 12), leaving relative-depth and absolute-depth readings of the "path law"
confounded. This session breaks the confound by injecting at blocks 3 and 9 as well, in 8 cells
({gpt2-124M, pythia-160m} × {valence, size} × {inj3, inj9}).

## Verdict: CONFIRMED — the path law is RELATIVE-depth, not absolute

- **Export peak tracks the injection depth, 8/8 cells**: strongest sole-exporting layer is `L_inj+1` in all
  cells tested (inj3 → block 4; inj9 → block 10 or 11), refuting S79's "export pinned at absolute blocks
  7–8" reading.
- **A new hop-timing structural control is exact in all 8 cells**: blocking readout at layers
  `≥ L_inj+2` gives `0.000000` — architecturally guaranteed regardless of which depth law is correct.
- **S79's "readout exclusively late (8–11)" claim is REVISED** to "readout exclusively `≥ L_inj+2`" — at
  inj3, blocking the late band (8–11) leaves 58–76% of the relay alive, which the absolute-depth law would
  have predicted to be exactly zero.
- **One genuinely absolute-depth feature is isolated and separated from the law**: pythia's final layer
  (block 11) is an inert solo-exporter (near-zero) at every tested injection depth, while gpt2's final layer
  remains a usable exporter — an architectural property of one specific layer in one family, not part of the
  general relative-depth law.

## Method

Same apparatus as S77/S78/S79 (do(W:=3‖W‖) patch, keep-only export profiles, band-blocking relay-readout
tests, exact structural controls), run at three injection depths (3, 6 [prior session], 9) across two model
families and two concept directions, with a new `s3-block-postinj2` control (blocking everything at or
after `L_inj+2`, predicted exact-0 under any law).

## Limits

- Three injection depths, one architecture class (12-layer decoder-only transformers), two ~100–160M
  models, 5 prompts, CPU, greedy/teacher-forced generation — bounded scale, documented explicitly in the
  original report.
- Keep-only ratios occasionally exceed 1.0 (a single export layer delivering more signal than the
  un-ablated baseline) — attributed to attention-mass redistribution under the ablation mask, mechanism not
  further characterized; magnitudes above ~1 should not be read as "fraction of baseline."
- Carrier-position promiscuity (from predecessor S79) was assumed, not re-validated, at the new injection
  depths.

## Reproduction

**Status: PASS.** Re-run in a clean temporary directory against cached `gpt2` and
`EleutherAI/pythia-160m` weights, same apparatus (`SEED=80`). All 6 global exactness gates reproduced as
`0.000000`/`1.000000` in all 8 cells; export-peak and readout-floor findings reproduced. See
`outputs/repro-s80.log` for the transcript from this packaging pass.

### Exact re-run commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install torch==2.13.0+cpu transformers==5.14.1 --index-url https://download.pytorch.org/whl/cpu
cd scripts
python3 s80-validate-injection-layer-generality.py
```

CPU only. Original wall-clock reported: 173.3 s on the researcher's machine; may vary with hardware.

## Upstream links

- Predecessor sessions S76–S79 (internal only, not included in this public repo).
- No new external citations introduced in S80.

## Files in this directory

- `report/s80-validate-injection-layer-generality.md` — original VALIDATE report.
- `scripts/s80-validate-injection-layer-generality.py` — the checker script (verbatim from source).
- `outputs/s80-output.txt` — the original full run log, copied verbatim from source.
- `outputs/repro-s80.log` — this packaging pass's independent clean-clone re-run transcript.
- `SHA256SUMS` — checksums for the files in this directory (verify with `sha256sum -c SHA256SUMS`).
