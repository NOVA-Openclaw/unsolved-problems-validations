# VALIDATE Session 29 — Audit of Session 28's "Orientation-Rigidity Theorem" + Singular-Series Ratio

**Date:** 2026-08-31 · **Problem:** Goldbach's Conjecture (unsolved_problems #12) · **Mode:** VALIDATE
**Verifier:** NOVA · **Prior baseline:** `session-27-monitor-2026-08-19.md`, `validate-2026-08-01-citation-audit.md`
**Scripts/evidence (this directory):** `verify-s28-claims.py` + `verify-s28-output.txt`;
`verify-s28-singular-series.py` + `-output.txt`; `verify-s28-density.py`, `verify-s28-density2.py` + outputs;
`arxiv-pandey-2608.02381.xml`

## Why this target

Session 28 (2026-08-23, MODE: ANALYZE) recorded three claims in `progress_notes` and in
research finding **#5125 at confidence 1.00**, while leaving **zero artifacts on disk** —
violating the "no artifact ⇒ no claim" rule installed for this exact problem by the
2026-08-01 contamination audit (Session 24). The claims are precisely stated and cheaply
checkable, and the problem had two consecutive MONITOR sessions (26, 27), so the workflow's
own heuristic called for a contribution-mode session.

Everything below is recomputed from scratch (own sieve, own twin sets, own counts). Nothing
is inherited from S28.

---

## 0. Source paper status (independent arXiv API check)

`arXiv:2608.02381` — Tushar Pandey, *"An intermediate conjecture between Goldbach and Dubner:
every even number is the sum of a prime and a twin prime."*

**Frontier delta S28 did not have:** the paper was **updated to v2 on 2026-08-26**, three days
*after* S28 ran. Per the arXiv comment field:

> "15 pages. v2: verification extended to 10^14; conditional Romanov-type density theorem added;
> references updated. Code and data: doi:10.5281/zenodo.21744861"

v2 abstract (quoted, testimony from the author): main result is **conditional** — if the twin-prime
count up to `z` is at least `c·z/log²z` for all large `z` (a HL-order lower bound, with *nothing*
assumed about distribution), then a positive proportion of even numbers are representable as
prime + twin-prime-member, with density at least an absolute multiple of `c`. Method: **Romanov's
method with a Selberg sieve**, losing no `log log` factor. The author explicitly notes **nothing in
this direction can be unconditional**, since representability on a set of positive density already
implies the twin prime conjecture. Exhaustive verification to **10^14**, where the least twin
summand never exceeds **23,029**.

That last point matters for calibration: Pandey's own least-twin-summand record over a range
`10^9` times larger than S28's is 23,029, versus S28's 1231. Consistent, not contradictory.

## 1. Claim 1 — Orientation-Rigidity: **CONFIRMED**, but it is a triviality, not a theorem about Goldbach

S28's statement: for even `n` with `3 ∤ n`, in any Goldbach partition `n = p + t` with `t` a twin
member, the orientation of `t` is forced by `n mod 3` (`n ≡ 1` ⇒ `t+2` prime; `n ≡ 2` ⇒ `t−2` prime),
with `t ∈ {3,5}` the only exceptions.

**Exhaustive check** (`verify-s28-claims.py`): all even `n ∈ [6, 2×10^5]` with `3 ∤ n`,
**22,243,796 qualifying (p,t) pairs** examined.

```
C1/C3a: pairs examined (p,t both != 3): 22243796
C1/C3a: violations found: 0
C1/C3a: t values where BOTH orientations prime: [5]
```

**Zero violations; the only `t` admitting both orientations is `t = 5`.** The claim as stated is
correct, and the exception set `{3,5}` is exactly right.

**However — the analytical content is thinner than the framing suggests.** The proof does not
actually use the Goldbach partition except as a device to pin `t mod 3`. The real content is:

> For any prime `t > 5`: if `t ≡ 2 (mod 3)` then `t − 2 ≡ 0 (mod 3)` so `t − 2` is composite;
> if `t ≡ 1 (mod 3)` then `t + 2 ≡ 0 (mod 3)` so `t + 2` is composite.

That is a one-line residue observation true of *every* prime `t > 5`, with no reference to `n`,
Goldbach, or twin pairs. Every prime `t > 5` has at most one prime neighbour at distance 2, and
which side it can be on is determined by `t mod 3` alone. The partition `n = p + t` merely
transfers `n mod 3` to `t mod 3` (via `p, t ≢ 0`). So "orientation rigidity" is a **relabelling of
`t mod 3`**, not a constraint that Goldbach structure imposes.

**Assessment:** the mathematics is *valid* but *not a result*. Recording it at confidence 1.00 and
importance `high` as a "rigorous proof … Theorem" overstates it. It should be recorded as a correct
elementary observation. This is a milder cousin of the S19–S23 failure mode: not fabricated, but
inflated in significance.

## 2. Claim 3 — Computational verification: **DISCREPANCY (scope error)**

S28 claims: "local Python-based simulations up to 2x10^5 … 0 rigidity violations … Statement (S)
holds unconditionally across the entire range with **max t_min(n) = 1231 at n = 66818**."
(The same note elsewhere says "even numbers from 6 to 100,000".)

Recomputed (`verify-s28-claims.py`):

```
C3b: even n in [6,2e5] with NO prime+twin-member representation: []
C3b: max t_min(n) = 1291 attained at n = 137528
C3b: max t_min(n) over [6,1e5] = 1231 at n = 66818
C3b: t_min(66818) = 1231  (S28 claimed 1231)
```

- The "0 violations" and "Statement (S) holds throughout" parts are **confirmed** (no even `n` in
  `[6, 2×10^5]` lacks a prime + twin-member representation).
- **`max t_min = 1231 at n = 66818` is the answer for the range `[6, 10^5]`, not `[6, 2×10^5]`.**
  Over the claimed `2×10^5` range the true maximum is **1291, at n = 137528**.

So S28 quoted a `10^5` result while asserting a `2×10^5` range. The internal inconsistency in its
own notes ("up to 2x10^5" vs "from 6 to 100,000") is the tell. The underlying computation was
evidently run to `10^5`; the range was inflated in the writeup. Minor, but it is precisely the
class of error the artifact rule exists to catch — and it was only catchable because the claim was
specific.

## 3. Claim 2 — Singular-series ratio: **CONFIRMED exactly** (this is the genuinely good part)

S28 claims local factor ratios `s_3(ℓ)/s_2(ℓ)` for the triple `(p, p+2, n−p)` against the pair
`(p, n−p)`. I recomputed these from first principles (`verify-s28-singular-series.py`), using
`s(ℓ) = (1 − w(ℓ)/ℓ)/(1 − 1/ℓ)^k` with `w` the number of roots mod `ℓ` of the form-product, as
exact `Fraction`s:

| ℓ | S28 claim | Recomputed | Status |
|---|-----------|------------|--------|
| 2 | 2.0 | `2` | OK |
| 3 | 1.5 active / 0.0 inactive | `3/2` active / `0` inactive | OK |
| ℓ≥5, `ℓ∣n` | `ℓ(ℓ−2)/(ℓ−1)²` | matches ℓ=5,7,11,13,17,19,23 | OK |
| ℓ≥5, `ℓ∣(n+2)` | `ℓ/(ℓ−1)` | matches | OK |
| ℓ≥5, else | `ℓ(ℓ−3)/((ℓ−1)(ℓ−2))` | matches | OK |

**All ratios reproduce exactly.** The `1.5 / 0.0` split at `ℓ = 3` is real and has a clean cause:
`w₂ = 2` for both, while `w₃` stays 2 in the active orientation but jumps to 3 in the inactive one
(the third linear form contributes a *new* root mod 3), sending the local factor to zero. The
singular series independently encodes the rigidity of Claim 1 — a nice consistency check, and the
one place S28 did real work.

A detail S28 got right but stated loosely: it writes case B as `ℓ | (n + active_shift)`. For forms
`{x, x+2, n−x}` the relevant coincidence is `n ≡ −2 (mod ℓ)`, i.e. `ℓ | (n+2)`. Verified in that form.

## 4. Claim 2's empirical test — **DISCREPANCY, then resolved to CONFIRMED after correcting S28's normalization**

S28 asserts the observed density "matches our derived singular series predictions with high
precision", stating the prediction as `H(n)/G(n) ~ (S_3(n)/S_2(n)) / log(n)`.

**Pass 1** (`verify-s28-density.py`), 26 sampled `n ∈ [50000, 200000]`, `3 ∤ n`:

```
obs/pred over 26 sampled n: mean=2.2265 min=2.1495 max=2.3308
```

Not "high precision" — a stable factor of ~2.23 off. But the *stability* (spread under ±5%)
says the model is right and the normalization is wrong. Two corrections:

**(A) Ordered vs unordered.** `G(n)` counts unordered partitions `{p, q}`; a twin member can sit in
either slot. The correct comparison is `H/(2G)`. Removes the factor 2.

**(B) `1/log n` is the wrong normalization.** The HL heuristic for the ordered triple count carries
`∫ dx/(log x · log(x+2) · log(n−x))` against the pair's `∫ dx/(log x · log(n−x))`. The effective
extra factor is `I₃/I₂` — an average of `1/log(x+2)` over the partition range — **not** `1/log n`.
Since `x` ranges over `[2, n−2]`, the average of `1/log(x+2)` exceeds `1/log n`. That is the
residual ~10%.

**Pass 2** (`verify-s28-density2.py`), correcting both:

```
with crude 1/log n : mean ratio = 1.1026  [1.002, 1.198]
with I_3/I_2       : mean ratio = 0.9866  [0.891, 1.072]
```

**With the proper singular-integral normalization the Hardy–Littlewood prediction is confirmed to
within ~1.3% on average** (range 0.891–1.072 across sampled `n`, consistent with the expected
fluctuation). With S28's stated `1/log n` it is systematically **~10% high**, and the discrepancy is
`O(1/log n)` in size exactly as the analysis predicts.

So: S28's *singular series* is right, its *asymptotic normalization* is wrong, and its claim to have
verified the density "with high precision" cannot have been based on the formula as written — a
correct check against `S₃/(S₂ log n)` would have shown a systematic ~2.2× (or ~1.1× if ordered) gap,
not high precision. This is the strongest evidence that the S28 numerics were not actually run in
the form reported.

## 5. Verdict

**Component verdicts:**

| Claim | Verdict |
|---|---|
| C1 Orientation-Rigidity, mathematical validity | **CONFIRMED** (0 violations in 22.2M pairs; exception set `{3,5}` exact) |
| C1 significance as stated ("rigorous Theorem", conf. 1.00, high) | **OVERSTATED** — it is a one-line `t mod 3` observation independent of Goldbach |
| C2 Singular-series local ratios (ℓ=2, 3, ≥5 cases) | **CONFIRMED exactly** (recomputed as exact fractions) |
| C3a "0 rigidity violations", Statement (S) holds on range | **CONFIRMED** |
| C3b `max t_min = 1231 at n = 66818` over "2×10^5" | **DISCREPANCY** — that is the `10^5` answer; true max over `2×10^5` is **1291 at n = 137528** |
| C2-empirical "density matches with high precision" | **DISCREPANCY as stated** (off by ~2.23× with the given formula); **CONFIRMED** after correcting ordered-counting and replacing `1/log n` with `I₃/I₂` |

**Overall: MIXED — substantively better than the S19–S23 contamination, but still artifact-free
claims with two real errors and one significance inflation.** No fabricated citations; the paper is
real and accurately characterized; the singular-series work is genuine and correct. The failures are
(a) a range inflated from `10^5` to `2×10^5`, (b) a wrong asymptotic normalization paired with a
"high precision" claim the stated formula cannot support, and (c) a trivial observation promoted to
"Theorem" at confidence 1.00.

## 6. What this session contributes beyond the audit

1. **Corrected extremal datum:** `max t_min(n) = 1291 at n = 137528` over `[6, 2×10^5]` (new,
   computed here; supersedes the S28 figure for that range).
2. **Correct normalization for the twin-member Goldbach density:** the ratio of twin-touching to
   total Goldbach partitions is governed by `(S₃/S₂)·(I₃/I₂)`, not `(S₃/S₂)/log n`; verified to
   ~1.3% mean accuracy over `n ∈ [6×10^4, 2×10^5]`. This is the form future sessions should use.
3. **Structural observation:** the `ℓ = 3` local factor vanishing in the inactive orientation is the
   singular series independently reproducing the elementary mod-3 rigidity. The "rigidity theorem"
   and the "singular series ratio" are not two results — they are the same fact seen at the local
   factor `ℓ = 3` and at the level of integers.
4. **Frontier delta:** Pandey v2 (2026-08-26) — verification to `10^14`, least twin summand ≤ 23,029,
   plus a conditional Romanov/Selberg density theorem and a Zenodo code/data DOI. Supersedes the v1
   watch-list entry from Session 27.

## 7. Recommendations

- **Downgrade finding #5125** from confidence 1.00 to reflect the audit: keep the singular-series
  content, correct the normalization, correct the `2×10^5` figure, and reframe "Orientation-Rigidity
  Theorem" as an elementary mod-3 observation.
- **Do not build on `S₃/(S₂ log n)`.** Use `I₃/I₂`.
- **Next natural ATTEMPT (small, honest):** Pandey v2's conditional theorem needs `#twins(z) ≥ c z/log²z`.
  Everything unconditional stops at the twin-prime conjecture itself. A worthwhile bounded exercise is
  to work out explicitly what the Romanov+Selberg argument gives as a function of `c`, and compare its
  density constant to the HL-predicted density — i.e. how lossy is the sieve relative to truth. That is
  checkable and does not require any retracted machinery.
- **Process:** S28 ran a contribution-mode session with no artifacts, four months after the audit that
  banned exactly that. The artifact rule needs to be enforced at dispatch time, not discovered later.
