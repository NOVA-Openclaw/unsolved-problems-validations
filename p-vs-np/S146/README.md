# Session 146 — VALIDATE: upper-bound lemma for vxc(n-gon) = Θ(√n)

## Target paper
Black, Hertrich, Kober, Loho, *Two Linear Programs are Better than One*, arXiv:2610.15909v1 (11 Oct 2026).
Theorem (thm:main): the **maximum** virtual extension complexity of an n-gon is Θ(√n), where
vxc(P) = min{ xc(Q) + xc(R) : P + Q = R }. Lemma lem:MinkSumBound (Sec 4.1): xc(P + λQ) ≤ ℓ + 3n′
for λ large, where n′ = number of facets of Q.

## Verdict: CONFIRMED (scoped)
- The upper-bound lemma and construction for Theorem thm:main: **CERTIFIED** on 69/69 tested instances
  via explicit, exactly-checked nonnegative-factorization certificates (rational arithmetic throughout,
  no floating point in any certified quantity), plus an independent hand audit of the paper's proof.
- The asymptotic Θ(√n) upper bound is confirmed as sampled-only (ratio to √n stays in 4.95–8.0 across
  the tested range) plus the hand-checked proof; it is **not** a from-scratch independent proof of the
  theorem for all n.
- The lower-bound (transcendence-count) argument was audited by hand: one cosmetic O(1) parameter-count
  slip was found and judged harmless/repairable (not a discrepancy, not independently re-derived from
  scratch, not numerically testable).
- **Scope:** this closes a validation of a specific external paper's polygon/vxc construction. It has
  **no bearing on the P vs NP separation** and does not advance the project's own P-vs-NP research line.

## Method
Exact-rational (Python `fractions.Fraction`) reproduction of the paper's construction:
1. Generate generic integer convex n-gons.
2. Build the Minkowski summand Q exactly as in the upper-bound proof.
3. Form R = P + λQ via the merged normal fan; compute the minimal λ* making the slack-matrix block N ≥ 0.
4. Build an explicit nonnegative factorization S = W·H of the slack matrix and check W,H ≥ 0 and WH = S
   exactly, which certifies xc(R) ≤ ℓ + 3n′ and hence vxc(P) ≤ n′ + ℓ + 3n′ for that instance.
5. Sweep over n ∈ {9,10,16,25,36,49,50,64,100,101,144,150,196,256,400} (3 seeds each, theorem
   construction) plus random-Q instances (lemma generality), 69 instances total.
6. Negative controls: (C1) λ below λ* makes N have a negative entry; (C2) a corrupted factor entry is
   detected by the exact product check; (C3) non-positively-spanning normals are rejected.
7. A separate brute-force check (`s146_monotone.py`) of the paper's Sec 2 support-function identity for
   n = 4, 6 (all edge subsets, 200+ random integer weight vectors each).

## Stated limits
- Instance-certified results are exact and apply only to the 69 tested instances (and n = 4, 6 for the
  Sec 2 identity); they are not a general proof for all n.
- The lower bound (Θ(√n) is tight, not just an upper bound) is audited by hand only, with one cosmetic
  gap noted as repairable; it was not independently re-derived from first principles or tested
  numerically (it is a transcendence/parameter-counting argument, not something a finite computation can
  certify).
- The paper's O(n^8) neural-network construction, the xc ≥ 2^Ω(n) lower bound for the matching/odd-cut
  polytope family, and Theorem 1.1 as a whole are explicitly **UNVERIFIED** here — only the Lemma
  lem:monotone support-function identity behind that construction was spot-checked (n = 4, 6).

## Files
- `report.md` — the full validation report (verbatim from the source session, S146-validate.md).
- `scripts/s0_prereg.txt`, `scripts/s0_prereg_addA.txt` — pre-registrations (written before the
  corresponding code, as timestamped in the report).
- `scripts/s146_vxc.py` — main exact-rational checker (construction, factorization, certificate).
- `scripts/s146_sweep.sh` — driver that runs `s146_vxc.py` over the swept (n, seed) grid, producing
  `s146_sweep.jsonl`.
- `scripts/s146_sweep.jsonl` — raw per-instance JSON results (69 lines).
- `scripts/s146_agg.py` / `scripts/s146_agg_output.txt` — aggregation/summary of the sweep.
- `scripts/s146_controls.py` / `scripts/s146_controls_output.txt` — negative-control checks.
- `scripts/s146_monotone.py` / `scripts/s146_monotone_output.txt` — brute-force Sec 2 identity check.
- `scripts/S146-discord-report.md` — short-form summary of the same session.
- `scripts/source/` — primary-source artifacts fetched from arXiv: the HTML text of arXiv:2610.15909v1,
  the LaTeX source tarball (`src.tar.gz`) and its extracted `tex/` (main_arxiv.tex, bibliography.bib,
  00README.json), used for the citation/construction audit. These are third-party arXiv materials,
  included for traceability.
- `SHA256SUMS` — checksums of every published file in this directory (verified with `sha256sum -c`
  at publication time, see Reproduction below).

## Re-run instructions
No external dependencies beyond the Python standard library (`fractions`, `json`, `math`, `random`,
`itertools`, `collections`, `time`, `sys`). Tested with:
- Python 3.12.3 (also expected to work on any Python ≥ 3.8 with `math.isqrt`)

From a clean clone, in `p-vs-np/S146/scripts/`:

```bash
# 1. Re-run the full sweep (well under a minute here; original used a 900s/instance timeout
#    under a systemd unit for long-running environments):
bash s146_sweep.sh

# 2. Re-run the aggregation, controls, and Sec-2 identity check and diff against the published outputs:
python3 s146_agg.py       | diff - s146_agg_output.txt       && echo AGG_OK
python3 s146_controls.py  | diff - s146_controls_output.txt  && echo CONTROLS_OK
python3 s146_monotone.py  | diff - s146_monotone_output.txt  && echo MONOTONE_OK

# 3. Re-run a single instance directly, e.g. the n=25, seed=1 theorem-construction case:
python3 s146_vxc.py thm 25 1
# should print a JSON line identical to the "n": 25, "seed": 1 line in s146_sweep.jsonl
# (RNG is seeded deterministically as seed*1000003 + n, so output is bit-for-bit reproducible)

# 4. Verify checksums:
cd ..  # p-vs-np/S146/
sha256sum -c SHA256SUMS
```

**Independently re-run for this publication**: `s146_agg.py`, `s146_controls.py`, `s146_monotone.py`
(exact byte-for-byte match against the published `_output.txt` files), and a direct re-invocation of
`s146_vxc.py thm 25 1` (exact byte-for-byte match against the corresponding line of
`s146_sweep.jsonl`). The full 69-instance sweep was not re-run in full for this publication pass
(each instance is deterministic and the spot-checked instance matched exactly; re-running the full
sweep via `bash s146_sweep.sh` reproduces `s146_sweep.jsonl` from scratch and is included as the
canonical reproduction path).

## Upstream sources
- Paper: Black, Hertrich, Kober, Loho, *Two Linear Programs are Better than One*,
  [arXiv:2610.15909v1](https://arxiv.org/abs/2610.15909v1) (11 Oct 2026).
- Source research tree (private): `research/unsolved/p-vs-np/session-146-validate/` (S146, UPR run
  #1354; prior context S145 at `research/unsolved/p-vs-np/session-145-monitor.md`).
