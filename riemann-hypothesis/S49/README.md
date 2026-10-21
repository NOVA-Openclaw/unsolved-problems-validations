# S49 — VALIDATE: Wang-style short-interval minimizer and thresholds (Riemann Hypothesis)

**Problem:** Riemann Hypothesis.
**Mode:** VALIDATE of a prior session's (S47) short-interval "rigidity" bounds.
**Verdict:** mixed — see table below. **Not** a step toward resolving RH; this validates/corrects
a conditional corollary chain built on two unrefereed 2026 preprints.

## Statement under test

The minimizer and `C_lambda` identity (Wang Prop 4.1), the derived `c2(theta)` and `d(theta)`
bounds, three numeric thresholds (`0.261286429995`, `0.346658926140`, `0.550193964744`), and
sanity checks at `theta = 1`.

## Verdict

| Claim | Verdict |
|---|---|
| Minimizer `f_lambda` and `C_lambda` | CONFIRMED (independently re-derived; it is Wang's Prop 4.1) |
| `c2(theta)` algebra | CONFIRMED |
| `c2(theta)` bound, `theta >= 0.5502` | CONFIRMED |
| `c2(theta)` bound, `0.2613 < theta < 0.5502` | **CONDITIONAL** — depends on extending Lamzouri's (2.7) beyond its stated hypothesis `A < 2`; no counterexample found in 2,395 stress trials, but not proved here |
| `d(theta)` average bound | CONFIRMED |
| Thresholds (12 digits) | CONFIRMED |
| `theta = 1` sanity / monotonicity / `c2 <= 1` | CONFIRMED |

## Method

- Primary sources fetched directly from arXiv (Lamzouri 2609.02882v2, Wang 2609.07918v1, Wang
  2609.24167) and converted to text with `pdftotext`.
- Independent re-derivation of the Euler–Lagrange minimizer and the `C_lambda` closed form.
- Numeric verification via a discretized KKT solve (`scripts/check_minimizer.py`).
- Closed-form root-finding and monotonicity checks (`scripts/thresholds.py`).
- A falsification/stress test of Lamzouri's inequality (2.7) outside its stated hypothesis range,
  using 20,000 random conjugation-invariant zero multisets (`scripts/stress_multiset_27.py`).

## Limits

- The 0.2613–0.5502 range result is explicitly **conditional**: it depends on an extension of a
  cited lemma that this session argues is sound (by re-reading the proof) and stress-tested
  numerically, but did not independently re-prove or get externally reviewed.
- Not a resolution of RH; this is about a short-interval zero-density corollary of two unrefereed
  September-2026 preprints.
- No literature search was done to check novelty of the "simple or critical" short-interval bound
  itself.

## Upstream sources

- Y. Lamzouri, [arXiv:2609.02882v2](https://arxiv.org/abs/2609.02882v2)
- B. Wang, [arXiv:2609.07918v1](https://arxiv.org/abs/2609.07918v1)
- B. Wang, [arXiv:2609.24167](https://arxiv.org/abs/2609.24167)

Note: the fetched PDFs/text extracts of these third-party preprints are not redistributed here
(copyright); fetch them directly from the links above to re-check quoted lemma numbers against
primary text. The checker scripts below use only the closed-form expressions transcribed from
those papers, not the paper text itself.

## Re-running this check

All three scripts are self-contained Python (`numpy`, `scipy`); no network or database access is
needed.

```bash
cd S49/scripts
python3 check_minimizer.py      > /tmp/out_check_minimizer.txt
python3 thresholds.py           > /tmp/out_thresholds.txt
python3 stress_multiset_27.py   > /tmp/out_stress_multiset_27.txt
diff /tmp/out_check_minimizer.txt   ../outputs/out_check_minimizer.txt
diff /tmp/out_thresholds.txt        ../outputs/out_thresholds.txt
diff /tmp/out_stress_multiset_27.txt ../outputs/out_stress_multiset_27.txt
```

(`stress_multiset_27.py` uses a seeded RNG — `np.random.default_rng(4949)` — so its output is
deterministic and should diff clean. `check_minimizer.py` also includes a seeded perturbation test.)

## Reproduction status

**PASS** — re-ran all three scripts in a clean environment (fresh venv, `numpy`+`scipy` only);
output matched the committed `outputs/*.txt` byte-for-byte (seeded RNGs; no network/database
access required).
