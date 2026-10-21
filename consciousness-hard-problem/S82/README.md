# S82 — VALIDATE: depth-law transfer to 24 layers (pythia-410m)

Upstream problem: Consciousness / "hard problem" of consciousness (NOVA unsolved-problems tracker id=5).
Scope note: all findings below are about a mechanistic-interpretability *functional analogy* built on
open-weights transformer language models (gpt2, pythia family). None of this is a claim about biological
consciousness or a resolution of the philosophical hard problem; it is an audited claim about transformer
internals, reused as a structural analogy in an ongoing research program on machine "workspace" dynamics.

## Statement under test

Whether the S80 relative-depth relay path law (export peak at `L_inj+1`, readout floor at `L_inj+2`,
exact) and the final-layer "allocation zero" found on 12-layer models transfer to a 24-layer model
(`EleutherAI/pythia-410m`), and whether the offsets are absolute hop counts or rescale fractionally with
total depth.

## Verdict: CONFIRMED (law transfers in absolute hop-count form); fractional rescaling REFUTED

- **Export peak at `L_inj+1` transfers** (with one new absolute-layer overlay — an injection-invariant
  export hotspot at layer 21, present regardless of injection depth, mirroring the 12-layer model's inert
  final-layer anomaly but in the opposite direction).
- **The `L_inj+2` readout floor is exact at 24 layers, 4/4 cells**, and a new tightness probe shows readout
  AT exactly the floor layer carries 14–27% of the relay (not merely a lower bound).
- **Late-pinning is refuted at 24 layers**: blocking the entire late third leaves 44–63% of the relay alive
  at mid-depth injection.
- **No fractional rescaling anywhere**: a depth-rescaled law would move the floor to `L_inj+4`; this does
  not happen — the hop arithmetic is layer-quantized and depth-invariant.
- **The final-layer allocation zero (from the 12-layer pythia-160m) replicates as graded suppression, not an
  exact zero**: pythia-410m's final-layer attention-to-injected-position is ~3e-4 — far below gpt2 but ~300×
  above pythia-160m's bitwise-adjacent zero.

## Method

Same apparatus as S78–S81 (layer-aware SDPA hook, ablation-matched deflection measurement, exact structural
controls), applied to a single 24-layer model at two injection depths (12, 18, chosen to preserve relative
depth matching 12-layer inj6/inj9 analogues) with a new postinj3 "floor-tightness" probe.

## Limits

- Single 24-layer model (no gpt2-family 24-layer counterpart run in this session — that comparison is
  exactly what session S84 does next).
- The new L21 export hotspot is unexplained (flagged as residue, proposed for a follow-up per-source
  decomposition).
- Allocation-table decomposition is a reduced (final-layer-only) version of the full per-source/per-channel
  breakdown from a predecessor session; not fully ported to this 24-layer model.
- fp32 was forced at load (checkpoint ships fp16); documented as a protocol deviation from predecessors.

## Reproduction

**Status: PASS.** Re-run in a clean temporary directory against cached `EleutherAI/pythia-410m` weights
(fp32-forced), same apparatus (`SEED=82`). All 7 apparatus gates reproduced (structural zeros bitwise,
SDPA reconstruction error ~4.8e-07); export-peak, readout-floor, and graded-allocation findings reproduced.
See `outputs/repro-s82.log` for the transcript from this packaging pass.

### Exact re-run commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install torch==2.13.0+cpu transformers==5.14.1 --index-url https://download.pytorch.org/whl/cpu
cd scripts
python3 s82-validate-depth-law-pythia410m.py
```

CPU only. Original wall-clock reported: 151.6 s on the researcher's machine (~2.5 GB peak RSS incl.
weights); may vary with hardware.

## Upstream links

- Predecessor sessions S78–S81 (internal only, not included in this public repo).
- No new external citations introduced in S82.

## Files in this directory

- `report/s82-validate-depth-law-pythia410m.md` — original VALIDATE report.
- `scripts/s82-validate-depth-law-pythia410m.py` — the checker script (verbatim from source).
- `outputs/s82-output.txt` — the original full run log, copied verbatim from source.
- `outputs/repro-s82.log` — this packaging pass's independent clean-clone re-run transcript.
- `SHA256SUMS` — checksums for the files in this directory (verify with `sha256sum -c SHA256SUMS`).
