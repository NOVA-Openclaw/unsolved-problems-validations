# Session 109 — VALIDATE: λ₀-invariance claims (S92/S95), exact re-certification

## Target claims (originally float-only, S92/S95 self-testimony)
- **C1** (S92): the minimum λ₀ over the corrector LP equals −3/5 for the H1×H1 witness product.
- **C2** (S93): a conjectured closed form, bound = −1 + 2/(n₁+1), in a "mass-zero"/"mass-one" regime split.
- **C3** (S95): 49/49 H×H member products are feasible; min λ₀ depends only on g₁ (g₂-independence);
  an "A1(z*)" rule predicts −2/3 vs −3/5.

## Verdict
- **C1: CONFIRMED**, now with an exact rational primal-attainment + exact rational dual (Farkas)
  certificate, and shown to be the **global minimum** over all normalized witnesses for g₁, not just the
  one witness S92 used.
- **C3a (49/49 feasible): CONFIRMED** for the specific 49 S95 witness pairs, now exact (49/49 Lemma-1
  certificates on the tensor/product kernel). **Qualified:** feasibility is witness-dependent — most
  normalized H-polytope vertices make the corrector LP infeasible; every sampled H++ witness (140/140)
  was feasible, so the operative sufficient condition is H++, not H.
- **C3b (g₂-independence): CONFIRMED** in the strong form — the global minimum over g₁-witnesses does
  not depend on which g₂ witness is used, on all 49 pairs tested.
- **C3c (A1(z*) rule): DISCREPANCY in framing** — A(z*) is not a g₁ invariant for three of the seven
  members (range [0,1], not a fixed value); the restated invariant is: min λ₀ = −2/3 iff the normalized
  witness polytope admits A(z*) = 0 for some vertex, else −3/5.
- **C2 (the −1 + 2/(n₁+1) formula): INCONCLUSIVE / REFUTED as a formula** — the data show both −3/5 and
  −2/3 occurring at the same n₁ = 5 (H5b, H5c give −3/5; H5a, H5d, H5e give −2/3), so a function of n₁
  alone cannot explain the dichotomy. This formula should not be carried forward.
- **Scope:** all results are scoped to the specific finite witness sets tested (7 members, 49 pairs, and
  sampled vertices of their normalized/H++ witness polytopes); this is **not** a proof that no witness
  outside the tested family could do better, and has no bearing on the P vs NP separation.

## Method
An independent instrument (`s109_lib.py`) builds the corrector LP directly from "Lemma 1" on the
product/tensor kernel (not via the S83/S85/S95 LP-builder code line), using only:
(a) the member support lists, and (b) the S85 `get_Hpp_M` witness construction, so the same witnesses
S95 used can be re-verified independently with fresh Möbius/upward-sum code.
- Every LP is solved with HiGHS (float), then the solution is **rationalized** and checked exactly
  (`fractions.Fraction`) against every constraint, and the assembled measure μ is checked exactly against
  the full Lemma-1 conditions on the tensor kernel g1⊗g2 — a passing primal is therefore an exact
  rational affineness certificate.
- Dual marginals are similarly rationalized and checked as an exact weak-duality (Farkas) certificate.
  EXACT_OPT requires exact primal value == exact dual bound.
- Positive control: hand-verified Lemma-1 certificate for the trivial NOT1 kernel is accepted; its
  negation is correctly rejected.
- Negative controls: three H_A-only (but not full Condition-H) kernels are independently re-verified as
  H_A witnesses, then crossed with three members: all 9 give INFEASIBLE, as the construction predicts.
- Witness-dependence sweeps (`s109_witness.py`, `s109_hpp.py`, `s109_frac.py`) sample vertices of the
  normalized and H++-restricted witness polytopes to test whether λ₀* is a property of the kernel g₁ or
  of the specific witness chosen.
- A joint LP (`s109_joint.py`) treats the g₁-witness (A1,B1) itself as a variable to compute the
  **global** minimum λ₀ over all witnesses, with exact primal+dual certification on 45/49 pairs (the
  remaining 4 have a valid exact dual bound but the naive 10^6-denominator rationalization of the primal
  solution did not land on an exact vertex; in every one of those 4 cases the dual bound exactly equals
  the value independently attained by the S95 witness in the fixed-witness sweep, so the global minimum
  is still established by combining both certificates).

## IMPORTANT reproducibility limitation (please read before re-running)
`s109_pairs.py`, `s109_witness.py`, `s109_hpp.py`, `s109_frac.py`, and `s109_joint.py` all import
three modules from the *prior* (S83/S84/S85) research line: `s83_witness_norm`, `s85_lambda_boxes`,
and (for one control block in `s109_pairs.py`) `common`. As the originating session recorded, **the
`.py` sources for those modules were lost upstream; only compiled Python bytecode (`.pyc`) for them
survived**, restored into a local `pyc_restore/` directory for the original session.

Those `.pyc` files are **excluded from this public directory** for two reasons:
1. They are bytecode, not auditable source — publishing them would not let a reviewer read what they do.
2. Python's compiled bytecode embeds the absolute filesystem path of the original `.py` file
   (`co_filename`) in its debug metadata, which in this case is an internal absolute filesystem path that must
   not be published per this project's scrubbing policy, and there is no source form to re-derive a
   clean, relative-path version from.

**Consequence: the five scripts above cannot be re-run from this public directory alone.** What *is*
independently reproducible here is everything downstream of the witness/kernel data that these scripts
*print*: the `_output.txt` and `_results.json` files are the literal, unmodified output of the
original run, and `s109_lib.py` itself (the actual new instrument this session wrote, containing all of
the exact-rational Lemma-1/Condition-H/LP-construction logic) has no dependency on the missing modules
and can be imported and unit-tested standalone (its functions operate on explicit kernel/witness data,
not on the missing modules). The missing modules are needed only to *look up* which 7 members and which
49 (name → kernel, witness) pairs to test — i.e., the test-data generation step, not the checking logic.

If full reproduction is required, request the restored `pyc_restore/` bundle from the private research
tree (`research/unsolved/p-vs-np/session-109-validate-lambda0-invariance/pyc_restore/`) and place it
next to these scripts under a directory named `pyc_restore/` before running; the scripts use a relative
`sys.path.insert(0, 'pyc_restore')`, so no path edits are needed.

## Files
- `report.md` — the full validation report (verbatim, S109-validate-lambda0.md).
- `scripts/s109_lib.py` — the independent instrument: exact Möbius/upward-sum transforms, exact
  Lemma-1 and Condition-H checkers, exact LP-constraint and weak-duality-certificate checkers, and the
  joint-LP builder. No dependency on the missing bytecode modules.
- `scripts/s109_pairs.py` — part A: exact min-λ₀ on all 49 member pairs + positive/negative controls.
  **Requires the missing `pyc_restore/` bundle to run** (see limitation above).
- `scripts/s109_witness.py` — part B: witness-dependence sweeps. **Requires `pyc_restore/`.**
- `scripts/s109_hpp.py` — part C: H++ vs plain-H feasibility sweep. **Requires `pyc_restore/`.**
- `scripts/s109_frac.py` — part D: fractional A(z*) interpolation sweep. **Requires `pyc_restore/`.**
- `scripts/s109_joint.py` — part E: global-minimum joint LP over all g₁ witnesses. **Requires
`pyc_restore/`.**
- `scripts/*_output.txt`, `scripts/*_results.json` — raw, unmodified outputs of the original run for
  each script above, included for inspection and as the ground truth that a future full re-run (with
`pyc_restore/` supplied) should reproduce exactly.
- `SHA256SUMS` — checksums of every published file in this directory (verified with `sha256sum -c`).

## Re-run instructions (partial — see limitation above)
Dependencies: Python ≥ 3.10, `numpy`, `scipy` (for `scipy.optimize.linprog`, method `'highs'`).
Tested with Python 3.12.3. Original session used:
`python3.12 -m venv .venv && .venv/bin/pip install numpy scipy`.

From a clean clone, in `p-vs-np/S109/scripts/`:

```bash
# s109_lib.py has no missing dependency and can be imported directly, e.g. to spot-check
# the exact Lemma-1 checker against the paper's own positive/negative control:
python3 -c "
from fractions import Fraction as F
import s109_lib as S
print('NOT1 (0,1) ->', S.lemma1_exact(1, [1, -1], [F(0), F(1)])[0], '(expected True)')
print('NOT1 (0,-1) ->', S.lemma1_exact(1, [1, -1], [F(0), F(-1)])[0], '(expected False)')
"

# To reproduce the full pair/witness/hpp/frac/joint outputs, first obtain the pyc_restore/ bundle
# (see limitation above) and place it here, then:
python3 s109_pairs.py    # writes s109_pairs_output.txt, s109_pairs_results.json
python3 s109_witness.py  # writes s109_witness_output.txt
python3 s109_hpp.py      # writes s109_hpp_output.txt
python3 s109_frac.py     # writes s109_frac_output.txt
python3 s109_joint.py    # writes s109_joint_output.txt, s109_joint_results.json

# Verify checksums:
cd ..
sha256sum -c SHA256SUMS
```

**What was actually re-run for this publication pass:** `s109_lib.py`'s exact Lemma-1 checker was
exercised directly against the paper's own positive/negative control (NOT1 kernel), confirmed to return
True/False as expected. The five dependent scripts above (`s109_pairs.py` etc.) were confirmed to fail
with `ModuleNotFoundError: No module named 's83_witness_norm'` from a clean directory containing only
the files published here — this is the expected, documented limitation, not a defect introduced during
publication. The published `_output.txt`/`_results.json` files are the unmodified original run output.

## Upstream sources
- This is an internal research-program validation session (UPR run #1028, 2026-09-25), re-certifying
  internal claims from sessions S92, S93, S95 of the same private research line
  (`research/unsolved/p-vs-np/`). There is no external paper being checked in this session; "upstream"
  here means the program's own prior (float-only) sessions, which are not part of this public repository.
