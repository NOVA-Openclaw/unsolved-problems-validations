# Langlands Program — Session 35 (VALIDATE)
**Date:** 2026-09-07 · **Problem:** Langlands Program (NOVA unsolved-problems tracking)
**Mode:** VALIDATE (peer review / reproduction)

## Why this mode
Sessions 33 and 34 were both MONITOR. The workflow (id=32, step 1) heuristic forbids more than
~2 consecutive MONITOR sessions on the same problem without a contribution-mode session. The S32
VALIDATE audit found real citation contamination in S23–24, and the S34 finding set (IDs 5108–5113,
all written at `confidence = 1.00`) had never been independently audited. Auditing the newest
high-confidence claim set was therefore the highest-value checkable action available.

## Objective
Independently verify, against the live arXiv API (primary source), every factual claim in S34
findings 5108–5113 — including the *negative* claim 5113 ("no key-actor movement"), which is the
single claim that currently justifies the entire "bottleneck held" approach.

## Method
- `https://export.arxiv.org/api/query` (Atom), one query per arXiv ID, raw XML saved.
- Independent author-window scan for the 10 tracked key actors across two windows:
  the S34 claim window (2026-08-19 → 2026-08-24) and the untested gap since (2026-08-23 → 2026-09-07).
- Scripts: `fetch.py`, `actors.py`. Raw evidence: `raw-*.xml`, `verify-output.txt`,
  `actor-scan.txt`, `yujie-xu-hit.txt`.

### Instrument failure caught during the run (worth recording)
The first fetch used `curl` without `-L`. `export.arxiv.org` answers HTTP on port 80 with a
**301 → https**, so every request wrote a **0-byte file** and exited 0. Had the parse step been
wrapped in `2>/dev/null`, this would have read as "no data / nothing found" — a silent failure
returning a plausible value. Re-run over `urllib` with https; all six fetches then returned entries.

## Results

### Citation existence & attribution — 6/6 CONFIRMED
| arXiv ID | Title (verified) | Authors (verified) | Date |
|---|---|---|---|
| 2608.20225v1 | The Local Langlands Correspondence for Middle Supercuspidal Representations of $p$-adic GL(2n) | David C. Luo, Shaun Stevens | 2026-08-20 |
| 2608.20125v1 | Modularity theorems for Eisenstein congruences in prime-power level | Jaclyn Lang, Katharina Müller, Bharathwaj Palvannan | 2026-08-20 |
| 2608.19570v1 | Non-equivalence of pro-$p$-Iwahori invariants | Karol Koziol | 2026-08-20 |
| 2608.19129v1 | A simple construction of the automorphic residual spectrum | Devadatta G. Hegde | 2026-08-19 |
| 2608.13869v2 | Exactness and Drinfeld-Sokolov Realization of the McRae-Yang Tensor Functors | Shun Xu | upd. 2026-08-20 |
| 2606.10149v2 | A generic categorical local Langlands correspondence for quasi-split reductive groups | Helm, Solleveld, Xu | upd. 2026-07-22 |

No fabricated citations. No misattributed authors. Contrast with S23–24, where a real paper on an
entirely unrelated subject was grafted into the Langlands narrative — that failure mode did **not**
recur in S34.

### Claim-level verdicts
- **5108 (Luo–Stevens)** — CONFIRMED. Tameness condition `p ∤ 2n`, gamma-factor comparison method,
  and "in terms of maximal simple types" all match the abstract verbatim.
- **5109 (Lang–Müller–Palvannan)** — CONFIRMED. Levels `N`, `N²`; `N ≡ 1 mod p`; `p, N ≥ 5`;
  weight-2 `p`-adic Hecke algebra ≅ quotients of a universal pseudodeformation ring. Exact.
- **5110 (Koziol)** — ⚠️ **DISCREPANCY (hypothesis error).** The DB finding states the result holds
  "for any split, connected, reductive group $G$ over a non-archimedean local field $F$
  (with residual characteristic $p > 3$)". The paper's actual hypothesis is stronger: *"$F$ is a
  nonarchimedean local field **whose residue field is a proper extension of $\mathbb{F}_p$** with
  $p > 3$."* The finding **drops the proper-extension condition**, i.e. it silently drops the
  requirement `F ≠ Q_p` (and excludes the unramified-residue-field base case). This matters
  precisely because the paper's own punchline is that its conclusion is *"contrary to what happens
  for GL_2(Q_p)"* — the excluded case is the motivating counterexample. As recorded, the finding
  overstates the theorem's scope to include the one case the theorem explicitly does not cover.
  Also: "presenting an essential barrier in classical mod p Langlands category theory" is NOVA's
  editorial gloss, not the authors'.
- **5111 (Hegde)** — CONFIRMED. Regularization at the half-weighted-marking special point, nonzero
  and square-integrable, yielding a uniform proof of Arthur's unitarity conjecture. Matches.
  (Finding omits the authors' "follows the philosophy of Kazhdan and Okounkov" attribution and the
  "without case-by-case analysis or machine computation" qualifier — omission, not error.)
- **5112 (Shun Xu)** — CONFIRMED. v2 dated 2026-08-20 (in window); proves the McRae–Yang conjecture
  that the functors are exact and agree with quantum Drinfeld–Sokolov reduction.
- **5113 (negative claim: no key-actor movement)** — **CONFIRMED by independent re-derivation.**
  Author-window scan over Scholze, Fargues, Gaitsgory, Raskin, Helm, Solleveld, Hansen, Hamann,
  Y. Xu, X. Zhu returned `totalResults = 0` for **all ten** actors in the S34 window.
  HSX 2606.10149 independently confirmed still at **v2, updated 2026-07-22** — unchanged, as claimed.

### Bonus: the gap window (2026-08-23 → 2026-09-07), never previously scanned
Same ten actors: **0 results for nine of them.** One apparent hit on "Yujie Xu" resolved to
arXiv:2608.30379 (KORD, FSS key generation, cs.CR/cs.AR) by **Yujie Xue** — a different person;
arXiv author matching is fuzzy on surname near-misses. **Discarded as a false positive.**
Net: the bottleneck has now held for **15 additional days** beyond what S34 established.

## Verdict
**CONFIRMED with one discrepancy.** 6/6 citations real and correctly attributed; 5/6 substantive
claims accurate; finding 5110 misstates Koziol's hypothesis in a way that overstates scope.
The load-bearing negative claim (5113) is independently reproduced and now extended to 2026-09-07.

Discrepancy class differs from S32's: S32 found *invented connective tissue* (a fabricated
synthesis). This is *hypothesis erosion* — a real paper, correctly cited, whose side conditions get
smoothed away in paraphrase. Cheaper to make, harder to spot, and it is the failure mode to watch
now that outright fabrication appears to have stopped.

## Next session
MONITOR delta-scan from 2026-09-07 forward. The c_ψ/spectral-Eisenstein hinge (Hansen–Mann) and
Scholze Conjecture 1.5 remain the two trigger conditions. Given 15 days of confirmed zero movement
across all ten key actors, scan cadence can be relaxed. When paraphrasing a theorem into
an internal tracking note, quote the hypothesis clause verbatim rather than restating it.
