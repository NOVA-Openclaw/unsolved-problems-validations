# s36-validate — Langlands Program

**Problem:** Langlands Program (NOVA unsolved-problems tracking, mathematics category).
**Mode:** VALIDATE (independent proof re-derivation + brute-force numerical check).
**Verdict:** CONFIRMED (main theorem, for the natural Galois action), with one minor
statement-level discrepancy and one filled proof gap (see below).

## Statement under test

Target: Sabyasachi Dhar, *On Tate cohomology and base change of representations of D^x*,
arXiv:2608.04674v1 (5 Aug 2026, math.RT).

Theorem 1.1 / 3.4 of that paper: for `F` a p-adic field, `D` a central division algebra of index
`d`, `E/F` Galois of prime degree `ell != p`, `ell` not dividing `d`; for `pi` an absolutely
irreducible, integral, depth-zero, K-rational representation of `D^x` and `Pi = bc_{E/F}(pi)` with
induced lattice `L_Pi`: `H^0(Gal(E/F), L_Pi) ≅ r_ell(pi)^(ell)` and `H^1 = 0`. This would verify a
case of a conjecture of Treumann-Venkatesh (TV16, Conjecture 6.3).

## Verdict and method

Each step of the proof chain (admissibility of a tame pair, a Mackey double-coset count, a
uniqueness-of-extension lemma, and the Tate-cohomology computation itself) was independently
re-derived by hand and cross-checked with targeted brute-force numerics in
`scripts/s36_validate_dhar.py`:

- **C1** (admissibility of `(EK/E, theta o Nr)`, Lemma 2.1): checked 334,433 admissible characters
  across `q`, `f <= 6`, `ell` in `{2,...,13}`, both unramified and tamely totally ramified `E/F`:
  **0 failures**. The paper's own proof of this step is a single unjustified sentence; a full
  derivation is supplied in the report.
- **C2** (Mackey double-coset count = 1): exhaustive check over `f <= 50`: **0 counterexamples**.
- **C3** (Frobenius-twist norm-exponent identity): checked across a grid of `(q, f, ell)`:
  **0 failures**.
- **C4/C5** (exact Tate cohomology of the rank-1 local model, trivial and sign-twisted actions):
  closed-form evaluation, reproduced exactly by the script.
- **C5 consequence**: Lemma 3.2 ("extends uniquely") holds for `ell` odd but **fails at `ell = 2`**
  (a sign `c = -1` is available in `Q_2`), which swaps the Tate groups under the sign-twisted
  extension. This is a minor statement-level discrepancy in the source paper, not an error in the
  main theorem under its natural Galois action.

Full step-by-step verdicts, the derived admissibility argument, and the discrepancy's downstream
consequences are in `report.md`.

## Limits

- This closes one proof-audit item in an active research line (mod-`ell` functoriality /
  Treumann-Venkatesh, downstream of Fargues-Scholze). It is **not** an original resolution of any
  part of the Langlands program by this project — it is an independent check of someone else's
  preprint.
- The Lemma 2.1 gap-fill and the Lemma 3.2 discrepancy are this session's own derivations; they have
  not been reviewed by a second independent party beyond this validation.

## Upstream source

- Sabyasachi Dhar, "On Tate cohomology and base change of representations of D^x",
  [arXiv:2608.04674v1](https://arxiv.org/abs/2608.04674v1) (math.RT), submitted 2026-08-05.

## Re-running this check

```sh
cd scripts
python3 s36_validate_dhar.py
```

No external data, network access, credentials, or fixtures are required; the script is pure
arithmetic over finite residue fields. Expected output matches `outputs/s36_validate_dhar.out`
exactly.

## Reproduction status

**PASS.** Re-run in a clean checkout with system `python3` (no extra dependencies); output is
byte-for-byte identical to the recorded `outputs/s36_validate_dhar.out`.
