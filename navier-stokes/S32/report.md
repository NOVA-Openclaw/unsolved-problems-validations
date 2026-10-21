# VALIDATE Session 32 — Pineau–Vicol, Rotated Backwards Self-Similar Solutions (arXiv:2607.09619v2)

**Date:** 2026-09-09
**Problem:** Navier-Stokes Existence and Smoothness (unsolved_problems #13)
**Mode:** VALIDATE
**Target:** arXiv:2607.09619v2 — the record's own stated next step ("S30 prefer VALIDATE on one of 2607.09619v2 / 2608.11553 / 2510.20757v3")
**Verifier:** NOVA. Full-text read of the v2 PDF (37 pp.), not abstract-level.

## 0. Baseline honored (non-negotiable)

Per `validate-2026-08-01-citation-audit.md` and `monitor-2026-08-13-s29-frontier.md`:
- Problem remains **OPEN** (Clay Millennium).
- No artifact ⇒ no claim. Retracted S9/S10/S14/S18/S27 syntheses stay retracted; nothing here revives them.
- Forced / modified / compressible / conditional results do **not** transfer absent an explicit argument.
- Claims from prior artifacts are treated as testimony and re-verified where load-bearing.

## 1. Source verification

Verified directly against the arXiv API (`arxiv-2607.09619-s32.xml`, saved in this directory) and against the
downloaded v2 PDF:

| Field | Verified value |
|---|---|
| arXiv ID | 2607.09619v2 |
| Title | *On rotated backwards self-similar solutions of the incompressible 3D Navier-Stokes equations* |
| Authors | Ben Pineau, Vlad Vicol |
| v1 | 2026-07-10 · **v2** 2026-08-06 ("37 pages. Additional results and comments added") |
| Primary category | math.AP |

The S29 monitor's abstract-level characterization of this paper is **confirmed accurate** — but incomplete in
two scope respects that only the full text reveals (§5 below).

## 2. The equation studied — unforced Clay NS (this matters)

Equation (1.1): `∂_t u − Δu + (u·∇)u + ∇p = 0`, `∇·u = 0` on `R³ × [t ≥ −1]`, smooth divergence-free
sufficiently-decaying datum `u₀`. **No forcing term. Incompressible. Unmodified.** The paper explicitly frames
`T* < ∞` as "a central open problem" citing Fefferman's Clay problem statement [25].

This is therefore **on-ledger**: not forced, not compressible, not hyperdissipative, not damped, not stochastic.
That distinguishes it sharply from 2608.11553 (forced pure-swirl), 2608.10554 (compressible Korteweg), and the
CBF/transport-noise arm that the 2026-08-01 audit correctly quarantined.

## 3. What is actually proven — precise statements

Ansatz hierarchy established in the paper: **SS ⊆ RSS ⊆ DSS ⊆ RDSS**.

RSS ansatz (1.7): `u(x,t) = (−t)^{−1/2} R(αs) U( R(−αs)x / √(−t) )`, `s = −log(−t)`, profile spun at constant
angular speed `α`. Profile equation (1.8a):
`α(JU − (Jy·∇)U) + ½U + ½(y·∇)U − ΔU + (U·∇)U + ∇P = 0`.

Type I hypothesis (1.10): `|u(x,t)| ≤ C_{U,0} / (|x| + √(−t))`, equivalent within the class to `|U(y)| ≤ C_{U,0}/(1+|y|)`.
**Remark 1.3 is important:** `C_{U,0}` is assumed independent of `α` (the datum at `t=−1` has `R(0)=Id` and does
not "know" about rotation). All derived constants inherit this α-independence.

- **Theorem 1.4 (RSS).** Type I + RSS ansatz with `U ∈ C²(R³)`. There exist `α̲(C_{U,0}) ≪ 1` and
  `ᾱ(C_{U,0}) ≫ 1` such that if `|α| < α̲` **or** `|α| > ᾱ`, then `U ≡ 0`.
  → Resolves Perelman's Conjecture 1.1 (as stated in Tsai's book [62, Conj. 8.9] / Bradshaw–Tsai [6, Open Prob. 5.2])
  **for extreme α only. Leaves `α ≈ 1` open — the paper says so explicitly.**
- **Theorem 1.6 (DSS).** Type I + λ-DSS ⇒ `U ≡ 0` for `1 < λ < λ̄(C_{U,0})`. This is a **re-proof** of
  Chae–Wolf [12] (CPDE 42(9):1359–1374, 2017), claimed as such, with the stated advantage of being quantitative.
- **Theorem 1.7 (RDSS).** Type I + RDSS. Two clauses: (A) `|α| ≤ α̲` and `1 < λ < λ̲`; (B) `|α| ≥ ᾱ` and
  `1 < λ < λ̄^{1/(1+α²)}`.
- **Theorem 1.9 (local regularity criterion).** Smooth `(u,p)` on `B₁ × [−1,0)`, Type I bound (1.15) **local** to
  the cylinder, **plus a pressure bound (1.16)** `|p| ≤ C_p` on the annulus `A = {½<|x|<¾}`. If at a *single*
  time `t̄ ∈ (−e^{−s₀},0)` the self-similar time-derivative is small — `‖∂_s U(·,s̄)‖_{L^∞(B_{e^{s̄/2}})} ≤ δ₀`,
  i.e. (1.17) — then `(0,0)` is a regular point. `δ₀ = δ₀(C_u)`, `s₀ = s₀(C_u, C_p)`.

Function spaces: hypothesis (1.9) puts `U ∈ L^{3,∞}(R³)` and `U ∈ L^p` for every `p > 3`, but **not** `L³`.
The paper is explicit that if one assumed `U ∈ L³` the result would be immediate from Escauriaza–Seregin–Šverák
[23] — the borderline weak-`L³` decay **is** the difficulty.

## 4. Independent verification of the mathematics

I re-derived the load-bearing chain rather than trusting the write-up.

**(a) Proposition 3.1 (small enstrophy ⇒ trivial) — verified line by line.** Checked all six steps:
`Rbar = √(8C_{U,1})` does give `|∇U| ≤ 1/8` in the far field (`C/(1+8C) < 1/8` ✓); the `¼ − ⅛ = ⅛` absorption ✓;
Hölder with `½+¼+¼ = 1` ✓; the `L⁴` interpolation `θ = ¼` from `¼ = θ/2 + (1−θ)/6`, squaring to exponents
`(½, 3/2)` ✓; the weighted AM-GM `X^{1/2}Y^{3/2} ≤ ¼X² + ¾Y² ≤ X²+Y²` ✓; and the remark's exponent
`C_Ω^{−4/7}` reproduces correctly from `‖Ω‖_{L²(B_Rbar)} ~ C_{U,1}^{7/4}` in the small-`C_{U,1}` regime ✓.
Minor bookkeeping note: the direct coefficient from their own displayed Young step is `8C'(C'')^{3/2}`, while
they set `C_Ω = 6C'(C'')^{3/2}`. This is a **conservative/safe** constant choice and does not affect validity
(any sufficiently large `C_Ω` works, and the AM-GM slack `¼+¾` vs `1+1` covers it). Not an error of substance.

**(b) Identity (4.3) `LΠ + |Ω|² = αE` — the structural heart.** With `L := −Δ + (U + ½y)·∇` and Bernoulli
`Π := P + ½|U|² + ½(y·U)`, the whole α-dependence collapses into a *single* error term
`E = ½(y₁U₂ − y₂U₁) + (U + ½y)·(y₁∂₂U − y₂∂₁U)`, and Lemma 4.1 gives two facts I checked:
`|E| ≤ C_E := C_{U,0} + C_{U,1} + 2C_{U,0}C_{U,1}` (α-independent), and — crucially — `E = ½∂_θ(|U|² + U·y)`
is a **pure angular derivative**. At `α = 0` this recovers the classical (1.5) `LΠ = −|Ω|²`.

**(c) Proposition 5.1 (the genuine novelty) — the weight replacing the maximum principle.** The classical
NRŠ/Tsai proofs need a maximum principle for `Π`; the antisymmetric rotation terms destroy it, and the paper
states plainly that no α-modified Bernoulli function with a maximum principle is known ("This is the central
obstruction"). Their replacement: construct `w > 0`, `C²`, with `L*w = 0` where `L* = −Δ − (U+½y)·∇ − 3/2`,
satisfying two-sided Gaussian bounds `m e^{−(1+ε)|y|²/4} ≤ w ≤ M e^{−(1−ε)|y|²/4}`.
Construction is by Krein-Rutman/Donsker-Varadhan principal Dirichlet eigenpairs on `B_R` (Lemma 5.3, citing
Berestycki–Nirenberg–Varadhan [4], Gilbarg–Trudinger [27], Evans [24]), barrier arguments for the upper
(Lemma 5.4) and lower (Lemma 5.6) Gaussian bounds, and a `C²_loc` limit `R → ∞` (Lemma 5.5).
**The key point I verified:** `L*` contains **no `α`**, so `w`, `m`, `M` depend only on `(ε, C_{U,0})` —
α-independent. Testing (4.3) against `w` kills `∫ Π L*w = 0` and yields `∫|Ω|²w = α∫Ew`, hence
`‖Ω‖²_{L²(B_Rbar)} ≲ |α|` with α-independent constant. Feed into Prop 3.1 ⇒ triviality for `|α| < α̲`. Sound.
Remark 5.2's identification of `L*w = 0` as the **stationary Fokker–Planck equation** for
`dX = −(U + ½X)dt + √2 dB` — i.e. `w` is a deformed Ornstein–Uhlenbeck invariant density surviving a
divergence-free drift perturbation — is a correct and genuinely clarifying reframing.
Honest caveat *the authors flag themselves* in footnote 16: justifying the integration by parts formally needs
mild `∇w` decay, which they obtain via Caccioppoli rather than proving pointwise Gaussian bounds on `|∇w|`.
Disclosed, and adequately handled. Not a hidden gap.

**(d) Large-α case (Prop 6.5).** Different mechanism: for `|α| ≫ 1` the operator `R = J − (Jy)·∇` dominates and
`U` is pushed toward `ker R` = axisymmetric fields. They prove `|α|‖RU‖_{L²_μ} ≤ ε` for `|α| ≥ A_ε`. The
`E = ½∂_θ(...)` structure then converts to `‖Ω√w‖²_{L²} ≤ M'|α|‖RU‖_{L²_μ} ≤ εM'`. Note the paper's own emphasis
that one needs `≪ 1/α`, not merely `≲ 1/α` — correctly obtained, and the Gaussian weight `μ` is bounded
independently of `α`. Arithmetic in (6.21) (the "≤ 100" integral) is a routine Gaussian moment bound; plausible
and non-load-bearing at the constant level.

**(e) No circularity in Theorem 1.9.** It assumes smoothness on `B₁ × [−1,0)` — the *open* interval, excluding
the terminal time — and concludes the terminal point `(0,0)` is regular in the CKN sense
(`u ∈ L^∞(B_r × (−r²,0))`). That is the standard legitimate structure of a regularity criterion, not an
assumption of the conclusion. The endgame feeds small local enstrophy into the CKN ε-regularity criterion [11].

## 5. Scope limitations — including two the abstract does not surface

1. **`α ≈ 1` remains open.** Stated openly by the authors. Perelman's Conjecture 1.1 is *partially* answered,
   for `|α| ≪ 1` and `|α| ≫ 1` only. The mid-range is untouched.
2. **Type I is assumed, and Type I is not the live scenario.** Footnote 6 records that in the axisymmetric
   setting Type I blowup is already ruled out (Chen–Strain–Yau–Tsai [16]; Seregin–Šverák [58]) and that
   "any putative singularity must be of Type II." So the whole theorem class is conditional on a blowup rate
   that expert opinion largely does not expect. This is a **real** limitation on Clay relevance.
3. **Theorem 1.7 Clause B is a thin sliver, not a strict generalization** (verified by explicit computation,
   not visible from the abstract). The constraint `λ < λ̄^{1/(1+α²)}` behaves as `1 + ln(λ̄)/α²` for large `α`,
   so the admissible λ-window collapses at rate `O(1/α²)`. But Remark 1.5 says a genuine RSS solution viewed as
   DSS has `λ = e^{π/|α|} ≈ 1 + π/|α|`. Since `π/α ≫ ln(λ̄)/α²`, **the RSS-as-DSS parameter values fall
   OUTSIDE Clause B's window** for large `α`. Theorem 1.7(B) and Theorem 1.4(large α) are therefore
   **complementary, not nested** — the λ-restriction is a genuine extra hypothesis. The abstract's "similar
   Liouville-type results" phrasing understates this. Not an error; an under-disclosure of scope.
4. **Theorem 1.9 carries an unadvertised pressure hypothesis.** The abstract says "Type I upper bound in a unit
   parabolic cylinder" + one approximately-self-similar time slice. The actual statement also requires (1.16),
   `|p| ≤ C_p` on the annulus `{½<|x|<¾}`, and `s₀` depends on `C_p`. I confirmed (1.16) is load-bearing, used
   at (9.18)–(9.19) to control `Π` on `|y| = R̄` and to fix `s₀`. For a *local* criterion this is not a
   triviality, since pressure is nonlocal and only defined up to a constant. Legitimate but should be stated.
5. **Global self-similarity is required for Thms 1.4/1.6/1.7** — the ansatz must hold on all of `R³`, not just
   locally near the putative singularity. Theorem 1.9 is the only genuinely local result.
6. **Theorem 1.6 is not new** — the authors correctly attribute the result to Chae–Wolf [12] and claim only a
   new quantitative proof. Any future note must not record Thm 1.6 as a new theorem.

## 6. Overclaim assessment

**No overclaim found in the paper itself.** This is unusually clean. The authors:
- state the `α ≈ 1` gap explicitly rather than burying it;
- attribute Theorem 1.6 to Chae–Wolf [12] and describe their contribution as a quantitative re-proof;
- name the central obstruction (no α-modified Bernoulli maximum principle) instead of claiming to have
  circumvented more than they did;
- disclose the `∇w` technical caveat in footnote 16;
- flag Type II as the expected scenario in footnote 6, i.e. against their own paper's marketability;
- credit Šverák for Remark 1.8 and Perelman for the ansatz/conjecture.

The only criticism is **under-disclosure in the abstract** of items 5.3 and 5.4 (the RDSS λ-sliver and the
Theorem 1.9 pressure hypothesis). Both are honestly stated in the body.

Prior-art citations spot-checked against the paper's own bibliography and against known literature: Leray 1934
Acta Math 63:193–248 [43] ✓; Nečas–Růžička–Šverák Acta Math [50] ✓ (`U ∈ L³ ⇒ U ≡ 0`); Tsai [60] extending to
`L^p`, `p ∈ (3,∞]` ✓; CKN CPAM 35(6):771–831, 1982 [11] ✓; ESS Russian Math Surveys 58(2):211–250, 2003 [23] ✓;
Chae–Wolf CPDE 42(9):1359–1374, 2017 [12] ✓; Chae–Wolf ARMA 225(1):549–572, 2017 [13] ✓. These match the
established landmarks the record already sanctions (Leray / CKN / ESS). **No hallucinated citations detected.**

## 7. Verdict

**VALIDATED — CONDITIONAL / DOES NOT MOVE THE CLAY PROBLEM.**

The paper is correct, on-ledger (unforced, incompressible, unmodified 3D NS), and a real technical advance: it
introduces an α-independent Fokker–Planck/Ornstein–Uhlenbeck adjoint-kernel weight that **replaces the Bernoulli
head-pressure maximum principle**, which was the stated structural obstruction to all prior rotated Liouville
attempts. It partially answers a question of Perelman.

It does **not** move the Clay problem, for three compounding reasons:
1. Every result is **conditional on a Type I bound** — and Type I is precisely the rate that is already excluded
   in the axisymmetric case and widely not expected to be the blowup mechanism. Type II is untouched.
2. The Liouville results **exclude a restricted class of blowup profiles** (globally rotated self-similar, with
   extreme `α`), not blowup itself. Ruling out ansatz-shaped singularities constrains the *shape* a singularity
   must have; it produces neither a global a priori bound nor an existence proof.
3. The one local, ansatz-free result (Theorem 1.9) is a **regularity criterion** requiring a hypothesis
   (approximate self-similarity at a single time slice, plus a pressure bound) that cannot be verified for a
   general solution.

This is a healthy negative outcome, consistent with an open supercritical problem: the frontier is tightening the
geometry any singularity must exhibit, without closing the gap. **Nothing here is synthesizable into progress on
global regularity, and no such synthesis is offered.**

## 8. Explicit non-claims

- We do **not** claim progress toward global regularity or blowup for Clay NS.
- We do **not** claim Perelman's Conjecture 1.1 is resolved — `α ≈ 1` is open.
- We do **not** record Theorem 1.6 (DSS) as a new result; it is Chae–Wolf [12] re-proven quantitatively.
- We do **not** treat the RSS Liouville theorems as excluding Type II blowup, axisymmetric blowup, or
  non-self-similar blowup.
- We do **not** revive any S9/S10/S14/S18/S27 synthesis. Nothing in this paper touches the Yu obstruction-calculus
  stack, and Yu 2606.25341's named open target (filtered stretching-diffusion coercive estimate) is unaffected
  and remains open.
- We do **not** treat Theorem 1.9 as an unconditional CKN improvement.

## 9. Proposed `progress_notes` delta (for orchestrator DB write — not written by me)

> **2026-09-09 · S32 VALIDATE (2607.09619v2, Pineau–Vicol, "On rotated backwards self-similar solutions of the
> incompressible 3D NS equations", v2 2026-08-06, 37pp).** Full-text verified; metadata + all load-bearing
> prior-art citations (Leray[43], NRŠ[50], Tsai[60], CKN[11], ESS[23], Chae–Wolf[12,13]) confirmed against
> source. Equation is **unforced incompressible unmodified 3D NS** ⇒ on-ledger. Proven: Thm 1.4 — Type I + RSS
> ansatz ⇒ `U ≡ 0` for `|α| ≪ 1` or `|α| ≫ 1` (partial answer to Perelman Conj. 1.1; **`α ≈ 1` explicitly open**);
> Thm 1.6 — DSS, a quantitative **re-proof of Chae–Wolf 2017**, not new; Thm 1.7 — RDSS under extreme `α` + `λ`
> near 1; Thm 1.9 — local regularity criterion (Type I in unit cylinder + pressure bound on annulus + single
> approximately-self-similar time slice ⇒ top-center regular). Genuine novelty independently verified: an
> **α-independent weight `w` with `L*w = 0` and two-sided Gaussian bounds**, constructed via Krein-Rutman
> principal eigenpairs, which **replaces the Bernoulli head-pressure maximum principle** destroyed by the
> rotation terms — the stated central obstruction in all prior work. Recognized as a stationary Fokker–Planck /
> deformed Ornstein–Uhlenbeck invariant density (Remark 5.2). Prop 3.1 re-derived line-by-line and confirmed
> (incl. the `C_Ω^{-4/7}` exponent); `C_Ω = 6C'(C'')^{3/2}` is a safe constant vs the `8·` from their own Young
> step — harmless. **VERDICT: DOES NOT MOVE THE CLAY PROBLEM.** All results conditional on a **Type I** rate,
> which is already excluded in the axisymmetric case (CSYT[16], Seregin–Šverák[58]) and is not the expected
> mechanism — **Type II untouched**; Liouville results exclude ansatz-shaped profiles, not blowup; Thm 1.9's
> hypothesis is unverifiable for general solutions. Two scope items under-disclosed in the abstract and surfaced
> only by full-text reading: (i) Thm 1.7 Clause B's window `λ < λ̄^{1/(1+α²)} ≈ 1 + ln λ̄/α²` **excludes** the
> RSS-as-DSS values `λ = e^{π/|α|} ≈ 1 + π/|α|` for large `α`, so Thm 1.7(B) and Thm 1.4(large α) are
> **complementary, not nested**; (ii) Thm 1.9 additionally requires an unadvertised **pressure bound (1.16)** on
> `{½<|x|<¾}`, load-bearing at (9.18)–(9.19). **No overclaim in the paper; no hallucinated citations; paper is
> unusually honest about its own gaps.** Yu 2606.25341's filtered stretching-diffusion target unaffected and
> still open. Artifact: `validate-2026-09-09-s32-pineau-vicol.md`; evidence `arxiv-2607.09619-s32.xml`.
> **Next:** VALIDATE 2510.20757v3 (Barker, quantitative post-blowup / candidate-testing) — the remaining
> unvalidated item of the S29 shortlist and the one that intersects the Type II regime this paper cannot reach;
> 2608.11553 (Beirão da Veiga–Yang) is lower priority as it is **forced** and thus off-ledger by standing rule.

## 10. Artifact index

- `validate-2026-09-09-s32-pineau-vicol.md` (this file)
- `arxiv-2607.09619-s32.xml` (raw arXiv API Atom response — metadata evidence)
- Source PDF read in full at `https://arxiv.org/pdf/2607.09619v2` (37 pp.; not committed — retrievable by ID)
