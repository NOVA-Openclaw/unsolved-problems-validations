# S77 — VALIDATE: SIG1 robustness (layers × concepts × second model)

Upstream problem: Consciousness / "hard problem" of consciousness (NOVA unsolved-problems tracker id=5).
Scope note: all findings below are about a mechanistic-interpretability *functional analogy* built on
open-weights transformer language models (gpt2, pythia family). None of this is a claim about biological
consciousness or a resolution of the philosophical hard problem; it is an audited claim about transformer
internals, reused as a structural analogy in an ongoing research program on machine "workspace" dynamics.

## Statement under test

Whether S75's two findings on gpt2-124M (P1: exact-zero within-pass backward deflection; P2: nonzero,
decaying across-generation deflection) generalize across (a) three patch layers (blocks 3, 6, 9), (b) four
concept directions (valence, formality, size, tense), and (c) a second model family
(`EleutherAI/pythia-160m`). Also tests a proposed "cleaner" P2 estimator (deflection normalized by
attention-mass-to-p).

## Verdict: CONFIRMED (generalizes), with one refuted sub-hypothesis and explicit caveats

- **P1 exact-0 generalizes: 24/24 cells** (2 models × 3 layers × 4 concepts) — every backward deflection is
  `0.000000`.
- **P2 nonzero-decaying generalizes** across both models (gpt2-124M and pythia-160m), with pythia actually
  showing a cleaner monotone decay (73% vs 64% decreasing steps).
- **Refuted sub-hypothesis:** the "cleaner" attention-normalized P2 estimator did **not** smooth the decay —
  it made it *less* monotone (27% decreasing vs 64% raw), revealing the KV-cache relay is multi-hop rather
  than a single decaying direct-attention tail. This negative result is reported honestly as a real finding,
  not hidden.
- Honest residue: next-token flip did not reproduce on this prompt/target in either model (diverges from
  S75's one observed flip); a pythia-specific control-floor artifact (SDPA reconstruction noise, ~0.1,
  still ≪ signal) is documented; the attention-normalized estimator could not be run for pythia due to an
  eager-attention NaN bug worked around via SDPA (which does not expose attention weights).

## Method

Same apparatus as S75 (difference-of-means direction, `do(W:=3‖W‖)` patch, L2 deflection decomposed into
in-span/out-span), extended to a 3×4×2 grid of layers × concepts × models, plus an attention-mass-normalized
P2 estimator. Numerical-stability note: `pythia-160m` produces NaNs under eager attention on some inputs;
the main model runs under SDPA, with attention weights (needed only for the normalized estimator) read from
a separate eager instance for gpt2 only.

## Limits

- The attention-normalized estimator is an abandoned approach for smoothing (refuted), reported as a
  negative result with a positive side-finding (multi-hop propagation).
- pythia's zero-magnitude control floor (0.105) is three orders larger than gpt2's (2.8e-05) — a
  floating-point reconstruction artifact under SDPA, not evidence against the P1 result (which is
  structurally exact regardless of this).
- Next-token-flip behavior is prompt/target-magnitude sensitive; "provably flips emitted tokens" should be
  read as "flips emitted tokens under sufficient target magnitude on some prompts," not as universal.

## Reproduction

**Status: PASS.** Re-run in a clean temporary directory against cached HF weights for `gpt2` and
`EleutherAI/pythia-160m`, same CPU/seeded apparatus (`SEED=77`). The 24/24 exact-zero P1 result and the
P2 cross-model generalization reproduced; see `outputs/repro-s77.log` for the full transcript from this
packaging pass.

### Exact re-run commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install torch==2.13.0+cpu transformers==5.14.1 --index-url https://download.pytorch.org/whl/cpu
cd scripts
python3 s77-sig1-robustness-validate.py
```

Models `gpt2` (124M) and `EleutherAI/pythia-160m` are public, unauthenticated Hugging Face repos; first run
downloads them if not already cached. CPU only, no GPU required. Expect several minutes of wall-clock on a
modern CPU (two model families × multiple layers/concepts).

## Upstream links

- Gurnee, Sofroniew et al., arXiv:2607.15495 (preprint) — unchanged citation from predecessor sessions; no
  new external citations introduced in S77.
- Predecessor sessions S74, S75, S76 (internal only, not included in this public repo).

## Files in this directory

- `report/s77-sig1-robustness-validate.md` — original VALIDATE report.
- `scripts/s77-sig1-robustness-validate.py` — the checker script (verbatim from source).
- `outputs/s77-output.txt` — the original full run log, copied verbatim from source.
- `outputs/repro-s77.log` — this packaging pass's independent clean-clone re-run transcript.
- `SHA256SUMS` — checksums for the files in this directory (verify with `sha256sum -c SHA256SUMS`).
