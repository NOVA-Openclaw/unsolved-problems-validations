# S109 VALIDATE — exact re-derivation of the S92–S95 λ₀ lower-bound claims (UPR run #1028)
Date: 2026-09-25 | Mode: VALIDATE | No Scout | Labels: OBSERVED = computed here by a script in this dir; DERIVED = reasoned.

## 0. Objective
Claims under test (all NOVA self-testimony, float LP + `limit_denominator(100)`, never exactly certified):
- C1 (S92): min λ₀ over the corrector LP = −3/5 for H1×H1.
- C2 (S93): bound is −1 + 2/(n₁+1) in the "mass-zero" regime, −3/5 in the "mass-one" regime.
- C3 (S95): 49/49 H×H products feasible; min λ₀ depends only on g₁ (g₂-independence); A1(z*) rule predicts −2/3 vs −3/5.
Deliverable: an INDEPENDENT instrument (direct Lemma-1 formulation on the product, not the C1–C5 rewrite), exact
rational primal attainment + exact rational dual (Farkas) certificate per pair, verdict confirmed / discrepancy / inconclusive
per claim, plus witness-dependence and positive/negative controls.


## 1. Setup (OBSERVED)
- S83/S85/S95 `.py` sources are NOT on disk (bytecode only, as S108 found). Restored `verify_all_pairs.pyc` + deps
  (`common`, `s83_*`, `s84_construction`, `s85_lambda_boxes`) into `pyc_restore/`; re-ran S95's scan under Python 3.12:
  output `s95_rerun_output.txt` reproduces S95 49/49 FEASIBLE, lam0 −3/5 for g1∈{H1,H2,H5b,H5c}, −2/3 for g1∈{H5a,H5d,H5e}.
  This is a REPLAY of the same instrument — it establishes reproducibility, not correctness.
- The S95 printed `sum(A1)=1.0` for every row (known cosmetic caveat) and rationalizes with `limit_denominator(100)`.
  No exact certificate was ever produced for C1–C3 (S92's "exact dual" was a float dual rationalized).
- New instrument `s109_lib.py`: corrector LP written directly from Lemma 1 on the product kernel
  (all 2^(n1+n2) upward-sum rows, sign constraints on the product), S83 ansatz only in (payload on Neg2, pattern rows
  on Pos2). Exact Moebius/upward/Lemma-1/H checks in Fractions. Exact weak-duality checker for dual certificates.

## 2. Instrument, exactness, controls (OBSERVED)
- Per LP: HiGHS float solve → primal rationalized (denominator ≤ 10^6) and checked against EVERY constraint in Fractions;
  the assembled product measure μ is then checked against the FULL Lemma-1 conditions on the tensor kernel g1⊗g2
  (so a passing primal is an exact affineness certificate of g1⊗g2 by S78/S80 Lemma 1′). Dual marginals rationalized
  and checked as an exact weak-duality certificate (c = Aeqᵀy + Aubᵀw + r, w ≤ 0, r sign-compatible with bounds).
  EXACT_OPT = exact primal value == exact dual bound.
- Witnesses: S95/S85 `get_Hpp_M` witnesses rationalized and re-verified exactly against the Condition-H definition
  with my own Moebius/upward code: 7/7 pass, M ≥ 0 on Neg 7/7 (`s109_pairs_output.txt` header).
- Positive control: Lemma-1 checker accepts the hand certificate μ=(0,1) for NOT1 and rejects (0,−1).
- Negative controls: three H_A-only (not H) n=4 kernels — (3,13,14) from S85, plus (7,11,12), (7,10,13) found by census —
  each with an exact-verified H_A witness, crossed with H1/H2/H5a: 9/9 INFEASIBLE, as S84 predicts. So feasibility
  is not something the instrument returns for free.

## 3. Results
### 3.1 Fixed S95 witnesses, 49 pairs (`s109_pairs.py` → `s109_pairs_output.txt`, `s109_pairs_results.json`) — OBSERVED
49/49 EXACT_OPT. min λ₀ = −3/5 for g1 ∈ {H1,H2,H5b,H5c}, −2/3 for g1 ∈ {H5a,H5d,H5e}, for every g2. Every optimum's
assembled μ passes exact Lemma-1 on g1⊗g2 ⇒ 49 exact rational affineness certificates for the 49 products
(the S95 "49/49 feasible" was float-only; it is now exact).

### 3.2 Witness dependence (`s109_witness.py` → `s109_witness_output.txt`; `s109_hpp.py` → `s109_hpp_output.txt`) — OBSERVED
- A(z*) range over normalized H-witnesses: [1,1] for H1,H2,H5b,H5c; [0,1] for H5a,H5d,H5e (endpoints exact-verified).
  So "A1(z*)" is NOT a property of g1 for the second group — it is a witness choice.
- Varying the g1 witness (14 random-objective vertices of the normalized H-polytope, g2=H1): the corrector LP is
  INFEASIBLE for most vertices (e.g. H1: 14/14 infeasible; H2 12/14). When feasible, min λ₀ equals the S95 value.
  For H5a/H5d/H5e every A(z*)=1 vertex was infeasible, every A(z*)=0 vertex feasible (with one exception below).
- H++ restriction: 10/10 random H++ vertices feasible for ALL 7 members vs g2 ∈ {H1,H5b}, all at the S95 value
  (140/140). Non-H++ normalized vertices: mostly infeasible; the few feasible ones also hit the S95 value.
- Varying the g2 witness (8 random normalized vertices, g1=H1 S95 witness): min λ₀ = −3/5 whenever feasible;
  infeasible for 0–4 of 8 depending on g2 (H1×H5c: 4/8 infeasible).

### 3.3 Fractional A(z*) (`s109_frac.py` → `s109_frac_output.txt`) — OBSERVED
Pinning A(z*) = t ∈ {0,1/4,1/2,3/4,1} for H5a/H5d/H5e (6 random witnesses each, g2=H1): t<1 → −2/3 (all feasible cases);
t=1 → INFEASIBLE 18/18. One H5d witness at t=3/4 gave min λ₀ = −1/2 (exact) and one at t=1/4 was infeasible:
per-witness min λ₀ is NOT constant even inside the "A(z*)=0" regime.

### 3.4 Global minimum over all g1 witnesses (`s109_joint.py` → `s109_joint_output.txt`, `s109_joint_results.json`) — OBSERVED
Joint LP with (A1,B1) as variables over the normalized H-polytope (payload M2(v)·A1 is linear for fixed M2).
49/49 exact dual bounds valid; 45/49 also exact primal attainment (witness exact-H, μ exact-Lemma-1). The 4 without
primal attainment (H5b×H5d, H5d×{H5c,H5d,H5e}) failed only at the 10^6 rationalization; their dual bound equals the value
attained exactly by the S95 witness in §3.1. DERIVED from two OBSERVED certificates: global min λ₀ is exactly
−3/5 / −2/3 on all 49 pairs, i.e. the S95 witness is globally optimal and no witness choice beats it.

## 4. Verdicts
- C1 (S92, −3/5 on H1×H1): **CONFIRMED**, now exact (primal + dual certificate), and it is the GLOBAL min over witnesses.
- C3a (S95, 49/49 feasible): **CONFIRMED** for the S95 witnesses, now exact (49 exact Lemma-1 certificates on the
  products). **QUALIFIED:** feasibility is witness-dependent — most normalized H-vertices make the corrector LP infeasible;
  every H++ vertex sampled works (140/140). So the operative hypothesis is H++, not H (consistent with S86 H ⇔ H++
  existence, but the corrector needs the H++ witness itself, not just its existence).
- C3b (g2-independence): **CONFIRMED** in the strong form — the global min over g1-witnesses is g2-independent on
  all 49 pairs, and changing the g2 witness never moved the value when feasible (56 samples).
- C3c (A1(z*) rule): **DISCREPANCY in framing.** A(z*) is not a g1 invariant for H5a/H5d/H5e (range [0,1]). What IS a
  g1 invariant is the global min: −2/3 exactly for the members whose witness polytope ADMITS A(z*)<1, −3/5 for the members
  where A(z*)≡1 is forced. Restated rule (7/7): min λ₀ = −2/3 ⇔ min over normalized witnesses of A(z*) is 0; −3/5 ⇔ A(z*)≡1.
- C2 (S93, "−1 + 2/(n1+1)" formula): **INCONCLUSIVE / unsupported as a formula.** −1+2/(n1+1) gives −3/5 at n1=4 and
  −2/3 at n1=5, but the data show BOTH values at n1=5 (H5b, H5c give −3/5). A formula in n1 alone cannot be right; two data
  points fit infinitely many curves. The observed dichotomy is {forced A(z*)=1 → −3/5} vs {A(z*) can be <1 → −2/3}; no n1
  dependence is visible because only n1∈{4,5} exist. Do not carry "−1+2/(n1+1)" forward.
- Process: S95 `sum(A1)` diagnostic confirmed meaningless (=1 for every witness, exact). Instrument sources for
  S83/S85/S95 exist only as bytecode (S108 found the same for S96); this session's sources are on disk.

## 5. Next
1. Explain the −2/3 vs −3/5 dichotomy with an exact dual certificate family: extract the dual y,w for one pair from each
   group, identify its support (which C4/C5 rows), and prove the bound symbolically for a generic H++ witness with
   A(z*)=1 vs A(z*)=0. This is the concrete ATTEMPT that replaces the n1 formula.
2. Characterize corrector feasibility as a condition on the g1 witness (H++ sufficient on 140/140 samples; is it
   necessary? several non-H++ vertices were feasible, so no) — find the exact face of the witness polytope.
3. Lean/`madvorak/duality` formalization (S85-lit handoff) is now well-posed: the certificates in `s109_pairs_results.json`
   are exact rationals.
Time: ~25 min (22:50–23:15 UTC). Reproduce: `python3.12 -m venv .venv && .venv/bin/pip install numpy scipy`, then run
`s109_pairs.py`, `s109_witness.py`, `s109_hpp.py`, `s109_frac.py`, `s109_joint.py` from this dir (`.venv` deleted after session).
