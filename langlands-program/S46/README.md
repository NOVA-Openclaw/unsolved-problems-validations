# S46-validate-peng — Langlands Program

**Problem:** Langlands Program (NOVA unsolved-problems tracking, mathematics category).
**Mode:** VALIDATE of a literature-summary claim against its primary source.
**Verdict:** CONFIRMED overall, with one substantive discrepancy (over-generalization) and several
scope omissions.

## Statement under test

An internal research-tracking note had summarized Hao Peng's preprint arXiv:2503.04623
("Fargues-Scholze correspondence and endoscopic classification for special orthogonal and unitary
groups", v4) as establishing: (1) that the Fargues-Scholze local Langlands correspondence matches
the semisimplification of the classical local Langlands correspondence for odd primes and
unramified extensions, for special orthogonal and unitary groups; (2) Fargues' eigensheaf
conjecture; (3) the strong Kottwitz conjecture; (4) torsion vanishing for the associated Shimura
varieties.

## Method

Primary-source comparison, claim-by-claim, against all four versions (v1-v4) of the arXiv
preprint (fetched directly: abstract-page metadata plus `pdftotext -layout` extracts of each PDF).
A small toy-model numerical recomputation was also run to spot-check one combinatorial claim in
§8.1 of v4 (generic ⇒ regular for Cases U/O1 but not O2, and the Std-generic fix for O2).

## Verdicts (summary)

| # | Claim | Verdict |
|---|---|---|
| 1 | v4 metadata (title, dates, versions) | confirmed |
| 2 | FS = classical LLC semisimplification (Thm A) | confirmed (the internal note omits the `O(2n,C)`-conjugation caveat for even SO) |
| 3 | Fargues' eigensheaf conjecture | confirmed, scoped to supercuspidal φ |
| 4 | strong Kottwitz conjecture | **discrepancy**: conditional on an extra hypothesis (4.5.8) except for SO over the base field itself; unconditional only up to a reparametrization. The over-generalization traces back to the preprint's own abstract, not to this project's summary alone. |
| 5 | torsion vanishing | confirmed, under-qualified (requires properness, extra field conditions, genericity, and an extra "Std-regularity" condition in one case) |
| V-1 | v2 dropped the non-compact case rather than fixing it | confirmed |
| V-2 | v4's regularity-hypothesis swap (§8.1) | confirmed; toy recomputation, 0 mismatches across 25 parameter cases |
| V-3 | errata | none posted; paper appears to be under peer review as of the check |

Full claim-by-claim reasoning, version-history diffs, and a noted label typo in the source (Def.
8.1.4 vs. a reference to "Std-regular") are in `report.md`.

## Toy-model numerical checks

Two scripts spot-check the §8.1 combinatorial claim ("genericity is sufficient for regularity in
Cases U and O1, but not O2") in an unramified split toy model (mod-ℓ toral parameters for
`SO(2n+1)`, `SO(2n)`, and `GL_n` as a proxy for Case U):

- `scripts/s46_generic_vs_regular.py`: 18 parameter cases, **0 mismatches** against the predicted
  pattern (always 0 generic-but-not-regular for O1/GL, always >0 for O2).
- `scripts/s46_stdgeneric_o2.py`: adds the paper's "Std-generic" condition (Lemma 8.1.5) for the O2
  case; **0 mismatches**, and the extra condition is confirmed non-vacuous and strictly stronger than
  plain genericity in the tested cases.

Scope: this checks only the combinatorial content of one lemma/remark in an idealized unramified
toy; it says nothing about the paper's deep geometric theorems (Fargues-Scholze matching,
eigensheaf conjecture, torsion vanishing), which were checked by primary-source reading, not
recomputation.

## Limits

- This is a literature/proof-audit of a third-party preprint, not an original contribution to the
  Langlands program by this project.
- The toy-model scripts model only a simplified unramified combinatorial sub-claim; they do not
  independently verify the paper's main geometric results.
- The preprint itself appears not yet to have a journal reference as of the check date (2026-09-30);
  its "errata" status is therefore inconclusive, not confirmed-clean.

## Upstream source

- Hao Peng, "Fargues-Scholze correspondence and endoscopic classification for special orthogonal
  and unitary groups", [arXiv:2503.04623](https://arxiv.org/abs/2503.04623) (versions v1-v4;
  current as of this check: v4, 2026-07-09).

## Re-running this check

```sh
cd scripts
python3 s46_generic_vs_regular.py   # exit 0 on success
python3 s46_stdgeneric_o2.py        # exit 0 on success
```

No external data, network access, credentials, or fixtures are required; both scripts are pure
finite-field combinatorics. Expected output matches `outputs/s46_generic_vs_regular.out` and
`outputs/s46_stdgeneric_o2.out` exactly. The PDF/text primary-source fetches described in
`report.md` are not re-run by these scripts (re-fetch https://arxiv.org/abs/2503.04623 directly to
reproduce the primary-source comparison).

## Reproduction status

**PASS.** Both scripts re-run cleanly with system `python3` (no extra dependencies, `s46_stdgeneric_o2.py`
imports `s46_generic_vs_regular.py` from the same directory); output is byte-for-byte identical to
the recorded `.out` files, and both exit 0.
