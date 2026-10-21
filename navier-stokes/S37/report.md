# S37 — VALIDATE — arXiv 2511.09556 (Cheskidov, Dai, Palasek)
**Problem #13, Navier–Stokes Existence & Smoothness · <workflow-run> · 2026-09-28**

Source read directly: abs page + PDF v2 (12 Jan 2026, 52 pp) → `paper.pdf`, `paper.txt`.
Title: *Instantaneous Type I blow-up and non-uniqueness of smooth solutions of the Navier–Stokes equations.*

## 1. What the paper claims (testimony, from the paper)

- **Unforced.** Eq. (1.1) has zero right-hand side. The paper says explicitly (p.14) that there is "no injection of the energy by any external force or boundary." The "forced NS system with small forcing" in §5 is an internal step: an approximate solution plus an error term that the corrector (§6, fixed point) then removes.
- **Setting:** Tᵈ (periodic), every d ≥ 2, with any smooth divergence-free data u₀. Theorem 1.7 constructs the family on ℝᵈ (quasi-periodic, periodicity breaks spontaneously).
- **"Instantaneous Type I blow-up" (Thm 1.1):** u agrees with the classical solution on [0,T\*]. It is classical again on (T\*,T], and u(T\*) is C^∞. The divergence is from the right: ‖u(t)‖∞ ~ (t−T\*)^{-1/2}, bounded above by C/√(t−T\*) and matched from below along a sequence tₙ → T\*⁺. ∇u behaves the same way at rate (t−T\*)^{-1}. The solution is a weak solution, weak-* continuous in BMO⁻¹. It lies in the Koch–Tataru path space, in L^∞_t Ẇ^{-1,∞} (d≥3), and in L²_t L^p for all p<∞. It satisfies log-log-weakened LPS and BKM integrals (1.4)/(1.5).
- **Consequence:** non-uniqueness of the Cauchy problem among spatially smooth weak solutions (Thm 1.7), realised as a continuum family u^(σ) bifurcating from U at T\*.
- **Unconditional.** It is a construction; no hypotheses beyond smooth data.
- **Scope limits the paper states itself:** Remark 1.4 and Thm 2.4 say the energy must blow up, ‖u(t)‖_{L²} → ∞ as t → T\*⁺. So the new branch is **not Leray–Hopf** and not in L^∞_t L²_x. §2.1 says instantaneous blow-up can occur in the Leray–Hopf class *only after* a finite-time blow-up. The mechanism is an inverse cascade: energy moves from infinite wavenumber down to low modes, with frequencies N_k = ⌈m\* A^{b^k}⌉ (double-exponential).

## 2. What I checked (my verification)

The load-bearing step I chose is the leading-order scaling and bookkeeping of the ansatz in §2.6/§4.1: v ≈ Σ_k N_k e^{−N_k² t}·(O(1) profile on Ω_k), with |Ω_k| ≤ 2^{−k}. The question is whether this ansatz is *dimensionally capable* of every property Thm 1.1 claims. If it is, the claimed exponents are at least self-consistent. This is **not** a check of the error estimates in §5–6, which run to about 20 pages of technical bounds.

Script: `scaling_check.py` (sympy + mpmath, run via `uv run --with sympy --with mpmath`). Output: `scaling_check.out`.

| # | Check | Result |
|---|---|---|
| 1 | Eq. (2.5), ∫₀^∞ N N′ e^{−(N²+N′²)s} ds | Closed form NN′/(N²+N′²): equals ½ for j=j′ and ≈ N′/N for N′≪N. **Matches** the paper's "~1 / N_{j,k}^{-1}N_{j′,k} ≪ 1". |
| 2 | Duhamel impulse: mode N_k driven by N_{k+1}² e^{−2N_{k+1}² s} | Exact solution → (F/2) e^{−N_k² t} with relative error N_k²/(2N_{k+1}²), numerically 3.2e-2, 2.0e-3, 7.6e-6 for successive dyadic pairs. So the injection from shell k+1 to shell k is effectively a delta in time. The output amplitude is O(1) with **no N-dependence**, so the amplitude recursion a_{k+1}² → a_k closes only at Type I scaling. **Consistent** with §2.6. |
| 3 | Type I two-sided bound | Numerically sup_t √t ‖v(t)‖∞ = 0.616 (finite) on the N_k = 2^{2^k} model, and √t_k ‖v(t_k)‖∞ ≥ e^{−1} at t_k = N_k^{−2}. **Consistent** with Properties 2 and 4 and with (2.2). |
| 4 | L²_t L^∞_x | Each scale contributes exactly ½ and the cross terms sum to a finite 0.63, so the integral diverges linearly in the number of scales. **Consistent**, and in fact required: Thm 2.1 (L²L^∞ weak–strong uniqueness) would otherwise force u ≡ U. |
| 5 | Orlicz-weakened LPS (1.4), weight 1/(1+(log log‖u‖)^c) | With double-exponential N_k, log log N_k ~ k·log b, so the sum behaves like Σ k^{−c}. It diverges for c ≤ 1 (partial sums 1191 at c=0.5 and 9.7 at c=1, still growing) and converges for c > 1. **Consistent** with "for some c>0". This sharpens the statement: with this N_k growth the exponent must be c > 1. That is not a discrepancy. |
| 6 | L²_t L^p, p<∞ (1.6) | Scale k contributes ~ ½·2^{−2k/p}, a geometric series that is finite for every p<∞ and degenerates only as p→∞. **Consistent.** The volume-shrinking cutoffs Ω_k (Lemma 4.1) are what make this work. |
| 7 | Energy near T\* | Energy at t_k ~ N_k² 2^{−k} gives log₁₀ ≈ 0.03, 0.9, 3.0, 7.6, 16.9, 35.9, 74.1, so it diverges. **Consistent** with Thm 2.4 and Remark 1.4: the branch is not finite-energy. |

I also read Thm 2.4's short proof. Bounded energy gives ∫‖∇u‖² < ∞ through energy equality on [t₀,T]. Together with the Type I bound, u then falls in class 2 of Thm 2.3, hence is Leray–Hopf, and weak–strong uniqueness gives a contradiction. The logic is sound as written. It relies on [CL20] Thm 1.1, which is stated for d=3 and which the paper asserts is dimension-independent; I did not check that claim.

## 3. Outcome

**CONFIRMED at the level checked (leading-order scaling, internal consistency). INCONCLUSIVE on the full proof.**

- There is no discrepancy between the stated theorem and the ansatz's scaling. Every claimed exponent (Type I rate, borderline L²L^∞ failure, Orlicz/LPS, L²L^p, energy blow-up) is what the double-exponential inverse cascade produces at leading order.
- Not verified: the §5 error bounds (Prop 5.1 and after), the corrector fixed point (§6), and the geometric cylinder construction. The d≥3 disjoint-support claim and Lemma 4.1's improved-Hölder induction were read but not re-derived. The v2 comment "minor corrections" does not flag any substantive error.
- One small sharpening: (1.4) requires c > 1 under the chosen N_k. The paper states the existential "some c>0", which is correct.

## 4. Effect on S36 posture

**No change: STAY-MONITOR.** The reasons:
1. The result is unforced, but the non-unique branch has **infinite energy immediately after T\***. It is neither Leray–Hopf nor a finite-energy smooth solution. The Clay problem (Statements A/B) asks for smooth, finite-energy global solutions from smooth data, and this paper does not touch that.
2. By its own §2.1, an instantaneous blow-up inside the Leray–Hopf class requires a prior finite-time blow-up. The mechanism therefore presupposes the thing the Millennium problem asks about; it does not produce it.
3. The paper matters as a new non-uniqueness mechanism: smooth at every time, borderline L²L^∞, and inside the Koch–Tataru space. That confirms S36's reading of the 2609.26790 shell paper. The shell paper's DNO *forward* cascade (unforced, finite-time, barely Type II) is the direction that would matter for #13, and it remains model-level only.

Watch item carried forward: any PDE lift of the forward DNO cascade to NS, or any variant of 2511.09556 with finite energy. By Thm 2.4 the latter is impossible for instantaneous Type I blow-up, so a finite-energy variant would have to be Type II.

## Artifacts
- `paper.pdf`, `paper.txt` (arXiv 2511.09556v2)
- `scaling_check.py`, `scaling_check.out`
- this file
