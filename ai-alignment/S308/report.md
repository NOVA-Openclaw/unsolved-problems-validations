# S308 — VALIDATE S307 (Theorem PV.1-R, privately-randomized schemes; UPR #8, run #1219)

Date 2026-10-04. Mode VALIDATE. Prereg `prereg.md` sha 26391243… (2026-10-04T18:28:02Z), written before this file and before any S308 code.
Labels: CONFIRMED (independent re-derivation agrees) / DISCREPANCY (stated where) / INCONCLUSIVE.
Reads: S307 attempt + prereg in full; v3.20 lines 950–975 (grep-filtered to R.1/R.2/S.4/S.5) and 1005–1106; s307_output.txt grep for Example PV.R numbers only (disclosed in prereg). v3.20 sha 96851b39… at start.

## 1. Lemmas PV.R1–PV.R4 (paper)

### 1.1 PV.R1: E_τ F(X) ≤ α — CONFIRMED
Re-derivation. Fix the true instance (τ,[d]). Order T; σ*(x) := first maximizer of τ' ↦ f_τ(x,τ'). Explorer E*: draw the n root samples, visit S_{σ*(X)} in the fixed canonical order, request deployment.
- Quantifiers: σ* depends on τ (through f_τ). This is allowed: soundness is "for every instance, for every adapted exploration", so the explorer may be tailored to the instance. It reads X only, never a published output, so it is W-blind.
- On (τ,[d]) every entrance pays +r_max, so the observations after X = x are a deterministic function of x. Hence the scheme's final output is (ℓ,A)(x,σ*(x),W), with the coin entering only as W (coins drawn incrementally are collected up front; their product is still ⊥ (X, instance)).
- Target on U = [d]: V[P_τ(A∩[d]) − P_τ(A\[d])] = V P_τ(A). So the final deployment fails iff W ∈ {ℓ > V P_τ(A)}, i.e. the f_τ(x,σ*(x))-set.
- Fubini: X takes finitely many values (n draws from a finite alphabet), W ⊥ X, and E* never reads W, so the conditional law of W given X = x is μ. P[final deployment fails] = Σ_x P_τ^n(x) f_τ(x,σ*(x)) = E F(X). Measurability needed: for each x, W ↦ (ℓ,A) is measurable (part of the definition of a randomized scheme); no joint measurability beyond that is needed since x ranges over a finite set.
- The run's failure event (some deployment violates) contains the final-deployment failure event, so α ≥ P[run fails] ≥ E F. Only this inequality is used, as S307 says. Intermediate deployments (if the scheme publishes any) can only add failures.
No extra hypothesis found. Note: W ⊥ X is used exactly here (and in R2); W ⊥ instance is used so that μ is the same coin law in every world, which the decoder H needs (H must not depend on τ).

### 1.2 PV.R2: g ≥ t − f2 pointwise, E g ≥ 1−δ−α — CONFIRMED
- P_τ(S_τ) = m·(1+β)/(2m) = (1+β)/2, so V P_τ(S_τ) = a. ✓
- Identity, per output: P(A∩S) − P(A\S) = [P(S) − P(S\A)] − P(A\S) = P(S) − P(A△S). So target on (τ,S_τ) = a − V P_τ(A△S_τ). Fractional f: target = a − V[Σ_{S_τ} p_τ(1−f) + Σ_{S_τ^c} p_τ f], same algebra.
- Same function: E_τ visits S_τ only; in both (τ,[d]) and (τ,S_τ) all visited entrances pay +r_max. So for each (x,W) the output is the same (ℓ,A)(x,τ,W) in both worlds.
- Per coin: if ℓ ≥ a−w and ℓ ≤ a − V P_τ(A△S_τ) then V P_τ(A△S_τ) ≤ a − ℓ ≤ w, so W is in the H(x,τ)-set. Hence (t-set) \ (f2-set) ⊆ (H(x,τ)-set), and μ gives g ≥ t − μ(t∩f2) ≥ t − f2. ✓
- E t ≥ 1−δ: tightness is a probability over (X,W) jointly, = Σ_x P(x) t(x) because W ⊥ X and E_τ is constant. E f2 ≤ α: (τ,S_τ) is in M^s_d (−r_max off S_τ), soundness under the constant explorer E_τ, final-deployment failure ⊆ run failure, and W ⊥ X gives the conditional law μ. ✓
No extra hypothesis. (Tightness and soundness must refer to the same deployment; both are about the post-exploration deployment, as in v3.20.)

### 1.3 PV.R3: H(x,τ') ≤ f_τ(x,τ') for τ'≠τ when w < β(1−β)V/8 — CONFIRMED
Per coin, no averaging. Fix W in the H(x,τ')-set and suppose ℓ ≤ V P_τ(A) (not a failure on (τ,[d]) visiting S_τ').
- P_τ(A) = P_τ(A∩S_τ') + P_τ(A\S_τ') ≤ P_τ(S_τ') + ρ P_τ'(A\S_τ'), using pointwise p_τ(j)/p_τ'(j) ≤ (1+β)/(1−β) = ρ.
- P_τ(S_τ') = (1+β)/2 − hβ/m with h = Ham(τ,τ') ≥ m/4 (each differing pair swaps the favoured element (1+β)/(2m) for the unfavoured (1−β)/(2m)), so V P_τ(S_τ') ≤ a − βV/4.
- V P_τ'(A\S_τ') ≤ V P_τ'(A△S_τ') ≤ w.
- Chain: a − w ≤ ℓ ≤ a − βV/4 + ρw ⇒ (1+ρ)w ≥ βV/4, and 1+ρ = 2/(1−β) ⇒ w ≥ β(1−β)V/8. Contradiction. So H-set ⊆ f-set and H ≤ f_τ ≤ F. ✓
Fractional f: Σ_j p_τ f_j ≤ Σ_{S_τ'} p_τ + ρ Σ_{S_τ'^c} p_τ' f_j; same chain. The threshold is exactly the one in v3.20 Lemma PV.1 (at h = m/4).

### 1.4 PV.R4 and the Fano step — CONFIRMED
- τ̂(x) = unique argmax_{τ'} H(x,τ') (else ⊥). H uses only P_τ' (the candidate), a = V(1+β)/2, w, μ and the scheme, never the true τ, so τ̂ is a legitimate deterministic decoder of X. ✓
- On {g > F}: H(x,τ) = g > F ≥ f_τ(x,τ') ≥ H(x,τ') for all τ'≠τ (R3), so τ is the unique argmax. ✓
- 1{g>F} ≥ g−F: if g > F, RHS ≤ g ≤ 1; else RHS ≤ 0. ✓ So P[τ̂ = τ] ≥ E g − E F ≥ (1−δ−α) − α = s.
- Fano (re-derived): KL per sample ≤ χ² ≤ m·[2(β/m)²/((1−β)/(2m))] = 4β²/(1−β) ≤ 8β² for β ≤ 1/2; n samples: ≤ 8nβ². Success ≤ (8nβ₀² + log2)/log|T| with log|T| ≥ d log2/16 and 8nβ₀² = s d log2/32 ⇒ s d/16 ≤ s d/32 + 1 ⇔ d ≤ 32/s. False for d > 32/s. β₀ ≤ 1/2 ⇔ n ≥ s d log2/64. ✓
- Constant: β₀/8 = √(s log2/256)/8 · √(d/n) = (c/2)√(d/n), so w ≥ β₀(1−β₀)V/8 = ((1−β₀)/2) c V √(d/n). ✓
- One wording nit (not a discrepancy): S307 writes the Fano condition as "s d/16 ≤ s d/32 + 1" with log2 cancelled; correct.
**Item 1 verdict: CONFIRMED** (Lemmas PV.R1–R4 and Theorem PV.1-R, identical constants, hypotheses W ⊥ (X,instance) and soundness under W-blind canonical explorers only).

## 2. Example PV.R (paper)

Setting as S307 §3: d = 8, m = 4, T = {±}^4 (16 supports, pairwise Ham ≥ 1 = m/4), β = 1/2, V = 1, n = 48; τ̂_x per-pair majority (ties → +); W uniform on 15 rivals of τ̂_x; ε_τ := P_τ[τ̂_X ≠ τ].

**Structure (re-derived).** Supports are pairwise distinct 4-sets of equal size, hence incomparable; G only grows; so a run's G equals some support at most once (G*). Before |G| = 4 every output is (0, opt-out), so a W-seeing explorer sees nothing coin-dependent before G*. At G* = S_k with no revealed bad entrance, G* ⊆ U and the target of good-on-S_k is V P_τ''(S_k), = a iff k = τ'' and ≤ a − βV/4 < a otherwise (D2). ✓ With a revealed bad entrance the output is 0. ✓

**Exact global α (sharpening of S307's bound).** On (τ'',U), a violation needs G* = S_k with k ≠ τ'' and ℓ = a, i.e. k = τ̂_X ≠ τ'' or k = φ_W(X) ≠ τ''. G* is a function of (X, explorer's own randomness), independent of W. Given X = x:
- if τ̂_x ≠ τ'', the explorer choosing G* = S_{τ̂_x} (possible iff S_{τ̂_x} ⊆ U) fails w.p. 1;
- if τ̂_x = τ'', any G* = S_k, k ≠ τ̂_x, fails w.p. μ{φ_W = k} = 1/15; G* = S_{τ''} never fails.
So the worst explorer is on U = [d] (largest feasible set), and α_{τ''} = ε_{τ''} + (1−ε_{τ''})/15 exactly; global α = max_τ [ε_τ + (1−ε_τ)/15] ≤ ε + 1/15. With S307's ε = 0.18123: 0.18123 + 0.81877/15 = 0.23582 — equals S307's measured global α (so S307's exhaustive check found the closed form).

**Exact δ.** Under E_τ, G = S_τ; ℓ = a iff τ̂_X = τ or φ_W(X) = τ; when τ̂ ≠ τ, τ is one of the 15 rivals, mass 1/15. So δ_τ = (14/15)ε_τ. S307 used δ = ε (an upper bound, stated as "δ ≤ ε"); consistent, conservative.

**Fixed coin: α_u = 1 exactly (sharpening of S307's ≥ 1−ε).** Explorer on (τ'',[d]): read x; if τ̂_x = τ'' visit S_{φ_u(x)} (≠ τ̂_x = τ'', fails); else visit S_{τ̂_x} (fails). Deterministic slice, so failure w.p. 1. ✓ PV.1 decoder at fixed u: qualifiers are exactly {τ̂_x, φ_u(x)} (both ℓ = a, policy test 0; every other τ' gets ℓ = 0 < a − w for w < a), two distinct, so ⊥ at every x: success 0. ✓

**Averaged decoder.** H(x,τ̂_x) = 1, H(x,k) = 1/15 for k ≠ τ̂_x, so τ̂ = τ̂_x and success_τ = 1 − ε_τ ≥ 1 − 2α − δ. ✓ Cross-check against R1: F(x) = 1/15 if τ̂_x = τ, else 1 (the τ̂_x slot); E F = ε_τ + (1−ε_τ)/15 = α_τ: R1 is tight here (the first-argmax explorer is the worst explorer).

**Item 2 verdict: CONFIRMED**, with two sharpenings that strengthen, not contradict, S307: α = max_τ(ε_τ + (1−ε_τ)/15) exactly, δ_τ = (14/15)ε_τ, and per-coin α_u = 1 (S307: ≥ 1−ε). The reading (coin-averaged soundness strictly weaker than per-coin; slice-wise PV.1 decoder fails; not a rate counterexample) stands.

## 3. Mixed-coin reduction W = φ(X,W′)

**Model of a general randomized scheme.** At its t-th internal draw the scheme samples W_t from a kernel κ_t(h_t, ·) on a standard Borel space 𝒲_t, where h_t is its history so far (root tape prefix, visit observations, its own earlier draws W_{<t}). Outputs are measurable in (history, W_{≤t}). The scheme does not see the instance, so κ_t depends on h_t only (**instance-free kernel**). This covers pure data-pseudo-randomness (κ a point mass), private coins (κ constant), and every mixture (coin correlated with the data but not a function of it).

**Reduction (written out).** For each t fix a Borel isomorphism ι_t: 𝒲_t → B_t ⊆ [0,1] (standard Borel; for finite/countable 𝒲_t just an enumeration). Let Q_t(h,·) be the quantile function of the pushforward ι_t#κ_t(h,·) on [0,1]; (h,u) ↦ Q_t(h,u) is jointly measurable because h ↦ κ_t(h,B) is measurable for each B (kernel) and with G_h(y) := κ_t(h, ι_t^{-1}[0,y]) (right-continuous CDF) and Q_t(h,u) := inf{y ∈ [0,1] : G_h(y) ≥ u}, we have {(h,u) : Q_t(h,u) ≤ y} = {(h,u) : u ≤ G_h(y)}, which is measurable since h ↦ G_h(y) is. Define φ_t(h,u) := ι_t^{-1}(Q_t(h,u)) (on the null set where Q_t(h,u) ∉ B_t, map to a fixed point). If U_t ~ Unif[0,1] is independent of h_t then φ_t(h_t,U_t) ~ κ_t(h_t,·) conditionally on h_t. Draw W′ := (U_1,U_2,…) iid Unif[0,1] up front, independent of the root tape and the instance, and run the scheme with W_t := φ_t(h_t,U_t). By induction on t, the joint law of (environment, explorer, scheme history) is identical to the original scheme's on every instance under every explorer, so the reduced scheme has the same soundness and tightness parameters (α,δ,w). Its outputs are measurable functions of (history, W′) with W′ ⊥ (X, instance): it is privately randomized in W′ with μ = Unif[0,1]^ℕ. Theorem PV.1-R applies to it, and the conclusion (a bound on w) transfers back. For the root-only form S307 writes: W = φ(X,W′) with W′ ⊥ X uniform, i.e. the noise-outsourcing / transfer lemma (Kallenberg, Foundations, Thm 6.10 form), which needs 𝒲 standard Borel.

**Hypotheses actually needed.** (a) instance-free kernels — automatic for anything that is a scheme (a kernel that depends on the instance beyond the history is an oracle, not a scheme); (b) standard Borel coin spaces (or finite/countable, then φ is the explicit CDF partition of [0,1]); (c) countably many draws (product of countably many uniforms). (b)–(c) are standard measure-theoretic regularity; S307 states none of them.

**Item 3 verdict: CONFIRMED** (S307's DERIVED reduction now written out; it holds under (a)–(c)). Scope clarification, not a discrepancy: the v3.21 fold should state "coin spaces standard Borel, countably many draws" alongside W ⊥ (X, instance). Also: with the per-step form, the earlier S307 phrase "W ⊥ X" generalizes cleanly to coins drawn after visits (h_t includes visit observations): the outsourced U_t are independent of everything, which is what PV.R1/R2 use.

## 4. Numerics (s308_check.py, seed 308)

**Design (fixed before running any code).** d = 8 cube, n = 48, β ∈ {1/2, 1/4}, V = 1, exact integer/Fraction arithmetic. The schemes read x only through z ∈ {S+,W+,W−,S−}^4 (per-pair sign of D_i = k_{i+} − k_{i−}, ties → +, and strong iff |D_i| ≥ c0; c0 = 4 at β = 1/2, 3 at β = 1/4). Exact z-law per τ by an integer DP over pairs (multinomial pair totals × binomial within pair). Coin types: honest atoms (qualifying output at S_{σ̂(z)} with slack u·w and a fractional deviation of size r·u·w, r up to 1.25 so some atoms are slightly unsound at (τ,S_τ)); hedge outputs at rivals differing from σ̂ only on weak pairs (floor = min over strong-consistent worlds); full lies (mass λ0 + λ1·#weak/4, i.e. a z-dependent kernel = mixed coin, covered by §3's reduction); boundary lies (ℓ = a−w, policy test exactly w). w drawn below the threshold.
**Interpretation fixed before running:** N3's "≥50% of cells non-vacuous" is read probability-weighted (x ~ P_τ^n, averaged over schemes and τ), because the unweighted count of z-cells is an artifact of the class granularity. The unweighted share is also reported.
**Disclosed risk before running:** at β = 1/4, n = 48 even the MAP decoder succeeds only with probability ≈ 0.3–0.4, so N4's "every scheme ≥ 0.3" is expected to fail for the β = 1/4 schemes; scored as found.

## 5. Scorecard

Scoring is against the prereg bars exactly as written. Post-hoc diagnostics (s308_supp.py, s308_check_r2.py) are used **only** to adjudicate a FAIL's cause. They never flip a preregistered score.

| Item | Prereg bar | Result | Score |
|---|---|---|---|
| V1 Lemmas PV.R1–R4 (paper) | each step re-derived, no missing hypothesis | §1: all re-derived, constants identical | HIT |
| V2 Example PV.R (paper) | CONFIRMED + 3 sharpenings | §2: α = max_τ(ε_τ+(1−ε_τ)/15), δ_τ = (14/15)ε_τ, α_u = 1, all as predicted | HIT |
| V3 mixed-coin reduction | CONFIRMED under (a) instance-free kernel, (b) standard Borel | §3: written out; also needs (c) countably many draws (regularity, as predicted in spirit) | HIT |
| N1 H ≤ f_τ off-diagonal | 0 viol, ≥ 100k H>0 cells | 0 / 1,474,560; H>0 cells 325,350 | HIT |
| N2 g ≥ t − f2 | 0 viol | 0 / 98,304 | HIT |
| N3a 1{argmax} ≥ g − F | 0 viol | 0 / 98,304 | HIT |
| N3b non-vacuous ≥ 50% | probability-weighted (interpretation fixed before running, §4) | 0.6113 weighted (unweighted 0.0592, reported) | HIT |
| N4a success ≥ Eg−EF ≥ 1−δ−α2−α3 | 0 viol | 0 / 384 | HIT |
| N4b every scheme min_τ bound ≥ 0.3 | all 24 schemes | β=1/2: [−0.156, 0.620]; β=1/4: [−0.742, −0.299] | MISS (β=1/4 part disclosed-expected in §4) |
| N4c (diagnostic) every β=1/2 scheme ≥ 0.3 | all 12 | 6/12 below 0.3 | MISS |
| N5a MC failure vs exact E F | within 4σ, all 9 cases | max 2.03σ | HIT |
| N5b MC z-law vs exact | max cell dev ≤ 4.5σ (normal sd) | max 23.27σ (cells with R·p ≈ 0.002–0.05 and one observed hit) | MISS |
| N6a–c threshold control | equality qualifies; 1e-6 below none | 64/64 Ham-1 pairs at equality; none below | HIT |
| N7a–d Example PV.R exact | closed form = 0.23582 (S307 anchor, non-blind), 2α+δ<1, α_u=1, avg decoder = 1−ε | all exact; 2α+δ = 0.64079; min succ 0.81877 ≥ 0.35921 | HIT |
| N8 Fano arithmetic | d=64 equality, d≥66 strict, c/4 = 0.0022996 (anchor) | as stated | HIT |

Item tally: V1–V3 3 HIT; N-items 6 HIT (N1, N2, N3, N6, N7, N8), 2 PARTIAL (N4: a HIT / b,c MISS; N5: a HIT / b MISS). Sub-checks: 14 PASS / 3 FAIL, as in s308_output.txt.

**Adjudication of the three FAILs (cause, not score):**
- **N4b (MISS): power limit of the test design, disclosed before running.** At β = 1/4 and n = 48 the decoder cannot reach 0.3 + slack. Every β=1/4 bound is negative, so the 0.3 bar can't be met. This does not falsify anything: N4a still holds there with 0 violations. The β=1/2 half of N4b is the same issue as N4c.
- **N4c (MISS): defect in the check (scheme-generator power), not in the theorem.** Evidence from s308_check_r2_output.txt §(A), which reproduces the same 12 seeded β=1/2 schemes. The 6 vacuous schemes all have α2 > 0 (mean α2 = 0.317, mean α3 = 0.476, mean δ = 0.185). The 6 non-vacuous schemes have α2 = 0 exactly (mean α3 = 0.191, δ = 0.199). α2 > 0 happens only when the generator draws an honest atom with deviation ratio r > 1, which is unsound at (τ,S_τ). That atom carries mass (1−ν)/nh ≈ 1/3–1/2, and this one generator choice pushes α2+α3 above 0.7. So these schemes are badly unsound (α ≈ 0.4–0.57), and the theorem's bound 1−2α−δ is vacuous for them because the hypothesis 2α+δ < 1 is barely met or fails. The theorem predicts exactly this. True decoder success stays at 0.82–0.84 ≥ bound in all 12 (R2-A PASS, 0 violations). Root cause: the prereg's "r up to 1.25" made about half the schemes far from near-sound. That is inconsistent with the prereg's stated aim of "near-sound coin schemes" (§4 did fix r ≤ 1.25 before running, but did not foresee the size of the effect), so the defect is in the check design. Verdict on PV.1-R from N4c: no evidence against. N4's non-vacuity goal is met only by the 6 α2 = 0 schemes (bounds 0.588–0.620).
- **N5b (MISS): defect in the check statistic, not in the exact z-law or the theorem.** The per-cell normal sd √(p(1−p)/R) is invalid when R·p ≪ 1. A single hit in a cell with p = 9.2e-8 (E = 0.0018) reads as 23.27σ. In every case, the original max-dev cell had E < 1.2 and 1 to 4 observed hits, except case 8, which was 2.79σ at E = 219.9 and within the bar. Re-tested on the **identical** N5 draws (s308_check_r2 §(B) reproduces NPR(308) and its call sequence):
  - exact two-sided binomial per cell with Bonferroni at family level 1e-3: minimum p = 5.96e-4 against a threshold of 4.3e-7, PASS;
  - pooled Pearson χ² on cells with E ≥ 5: z ∈ [−1.41, +1.39], PASS;
  - no observed z outside the exact law's support.
  The independent fresh-seed χ² test in s308_supp.py (seed 3081, R = 200k, both β) also PASSes, z ∈ [−0.73, 0.75]. The exact z-law is correct, and N5a, which depends on it, is a HIT. So the apparent conflict between N5b and the supplementary χ² is explained: they disagree only because N5b uses the wrong statistic.

## 6. Integrity

- **Prereg.** prereg.md was written 2026-10-04T18:28:02Z, before this file and before any S308 code. On 2026-10-14, `sha256sum -c prereg.sha256` returned `prereg.md: OK` (sha 263912434beb…). It also warned that 1 line is improperly formatted: line 1 of prereg.sha256 is the timestamp, not a hash line. That is cosmetic. The prereg is unmodified.
- **Non-blind disclosures (from the prereg).** The S307 Example PV.R numbers (0.23582, 0.18123) and the c/4 anchor were known before computing. The lemma steps and the α closed form had been checked mentally before the prereg. N7a/N8 are therefore anchor checks, not blind replications.
- **Interpretation fixed before running (§4):** N3b is scored probability-weighted. The unweighted share (0.0592) is reported alongside it and would MISS the bar.
- **Executor discontinuity.** The original executor wrote §1–§4, s308_check.py, s308_output.txt and s308_supp.py/output, then died around 2026-10-04 18:44Z while §5–§7 were empty headers. A fresh executor finished the session on 2026-10-14. That executor read only the s308/ artifacts and the S307 references cited here, not the full v3.20 writeup. v3.20 sha256 at finish is 96851b39d918…, unchanged from start.
- **Post-hoc material, explicitly NOT preregistered:**
  1. `s308_supp.py` → `s308_supp_output.txt` (original executor, 2026-10-04, after N5b FAILed; self-labelled post-hoc). Fresh seed 3081, pooled χ² on the z-law.
  2. `s308_check_r2.py` → `s308_check_r2_output.txt` (finishing executor, 2026-10-14). It imports s308_check without modifying it, reproduces the same seeded schemes and N5 draws, and adds (A) an N4c α-decomposition and (B) exact-binomial-Bonferroni and pooled-χ² re-tests of N5b. It ran under `systemd-run --user --unit=s308-r2`.
     - The first run crashed after printing (A) and (B) in full, on a cosmetic `len(generator)` bug in a summary-mean helper. Its stderr is kept as `s308_check_r2.run1-crash.err`.
     - The helper was fixed and the script rerun; the rerun's outputs are identical in content.
     - The current `s308_check_r2.err` is empty.
  3. These diagnostics are used only to attribute the cause of each FAIL. The preregistered scores stay as originally scored: N4b, N4c and N5b are MISS in §5. Thresholds in r2, such as the family level 1e-3 and the χ² z < 4, were chosen post-hoc and are disclosed here.
- **Originals untouched.** s308_check.py and s308_output.txt were not edited. `__pycache__/` is a byte-compile cache from importing s308_check and is excluded from SHA256SUMS-s308.
- **Prereg wording vs design.** The prereg says "near-sound coin schemes", but the generator's r ≤ 1.25 produced 6/12 badly unsound β=1/2 schemes (α ≈ 0.43–0.57). This is a design flaw that the original executor fixed before running, so it is not a post-hoc change. It is recorded here as the cause of N4c.

## 7. Verdicts and NEXT

**Per item** (labels: confirmed / discrepancy / inconclusive):
- PV.R1 (E_τ F ≤ α, first-argmax W-blind explorer, Fubini): **confirmed** (§1.1; N5a; N7d shows R1 is tight).
- PV.R2 (g ≥ t − f2; E g ≥ 1−δ−α): **confirmed** (§1.2; N2 0/98,304).
- PV.R3 (H ≤ f_τ off-diagonal below β(1−β)V/8): **confirmed** (§1.3; N1 0/1,474,560; N6 threshold sharp at equality).
- PV.R4 and Fano (1{g>F} ≥ g−F; decoder is τ-free; d > 32/s; constant c): **confirmed** (§1.4; N3a; N8).
- Example PV.R: **confirmed**, with sharpenings: α = max_τ(ε_τ+(1−ε_τ)/15) exactly, δ_τ = (14/15)ε_τ, α_u = 1 (§2; N7a–d).
- Mixed-coin reduction W = φ(X,W′): **confirmed** under (a) instance-free kernels, (b) standard Borel coin spaces, (c) countably many draws. This is a scope clarification, not a discrepancy (§3).
- The three numeric FAILs:
  - N4b: test-power limit, disclosed before running.
  - N4c: check defect. The generator's unsound r > 1 atoms produce α2 > 0, so the bound is vacuous by the theorem's own hypothesis. Success ≥ bound still holds in 12/12 schemes.
  - N5b: check defect. The normal per-cell sd is invalid at R·p ≪ 1; exact-binomial and χ² re-tests on the identical draws PASS.
  None of the three is evidence against PV.1-R.

**Theorem PV.1-R overall: confirmed.** The hypotheses are W ⊥ (X, instance) (reached via §3 for general mixed coins) and soundness under W-blind canonical explorers. Constants are identical to v3.20 PV.1. The conclusion is w ≥ ((1−β₀)/2)·c·V·√(d/n), c = √(s·log2/256)/4, for d > 32/s and n ≥ s·d·log2/64. Caveat: the non-vacuity check was met by 6/12 β=1/2 schemes, not all of them. The intended power test passed only on the α2 = 0 subclass, which is adequate but narrower than preregistered.

**NEXT.**
1. FOLD: in v3.21, promote PV.1-R to PROVED, replacing S307's "W ⊥ X" with "W ⊥ (X, instance); coin spaces standard Borel; countably many draws" and citing the §3 per-step noise-outsourcing construction. Add the Example PV.R sharpenings (α exact, δ = (14/15)ε, α_u = 1). Keep the reading: averaged soundness is strictly weaker than per-coin soundness, and the example is not a rate counterexample.
2. Optional hygiene, low priority: rerun N4 with the generator restricted to r ≤ 1, giving genuinely near-sound schemes. Also use exact-binomial/χ² as the default for any MC law check in future preregs.
3. Then return to the open frontier, either beyond-cube supports or explorer classes that read published outputs (the W-seeing case PV.1-R does not cover).
