# S55 — VALIDATE S54 C2 (D6 + D7) + Steane C2b fold-in
UPR run #1175, Problem #6 UFT. Started 2026-10-02 01:51 UTC. Hard stop 03:00 UTC.
Labels: OBSERVED = measured by my own code this session; DERIVED = reasoned.

## Item 1 — D6 (Hessian of M2 at stabilizer states = (4/ln2)·Id ?)
**1a. Re-derivation [DERIVED, 01:55 UTC, paper].** Convention (checked in s50_choi_nonlocal_magic.M2_pure): M2(ψ) = −log2( Σ_{P∈{I,X,Y,Z}^N} ⟨P⟩⁴ / 2^N ),
sum over the 4^N unsigned Hermitian Pauli strings (so sign/phase of σ_P is irrelevant: only ⟨P⟩⁴ enters).
φ stabilizer, group S; exactly 2^N strings P satisfy ±P∈S (Pφ = σ_P φ, σ_P=±1); all other strings have ⟨P⟩_φ = 0.
Let χθ = e^{−iθK}φ, K Hermitian. Expand ⟨P⟩_θ = ⟨P⟩ + iθ⟨[K,P]⟩ − (θ²/2)⟨[K,[K,P]]⟩ + O(θ³).
 • P∉±S: ⟨P⟩_θ = O(θ) ⇒ ⟨P⟩_θ⁴ = O(θ⁴).
 • P∈±S: ⟨[K,P]⟩ = σ_P(⟨K⟩−⟨K⟩) = 0. Write Kφ = Σ_s c_s|s⟩ in the S-eigenbasis (|0⟩=φ), P|s⟩ = σ_P χ_s(P)|s⟩. Then
   ⟨[K,[K,P]]⟩ = 2σ_P⟨K²⟩ − 2⟨KPK⟩ = 2σ_P Σ_s|c_s|²(1−χ_s(P)) = 4σ_P Σ_{s:χ_s(P)=−1}|c_s|².
   So ⟨P⟩_θ = σ_P[1 − 2θ²F_P] + O(θ³), F_P := Σ_{χ_s(P)=−1}|c_s|²; ⟨P⟩_θ⁴ = 1 − 8θ²F_P + O(θ³). (Matches S54 D6 line.)
 • Σ_{P∈±S} F_P = Σ_{s≠0}|c_s|²·#{P: χ_s(P)=−1} = 2^{N−1}·V, V := Σ_{s≠0}|c_s|² = ‖(1−Π_φ)Kφ‖² = Var_φ(K) (nontrivial character ⇒ kernel index 2).
 • Σ_P⟨P⟩⁴ = 2^N(1 − 4θ²V) + O(θ³) ⇒ M2(χθ) = (4/ln2)·θ²V + O(θ³).
 Tangent identification: dχ/dθ|0 = −iKφ, horizontal part w = −i(1−Π)Kφ, ‖w‖² = V; FS distance d_FS(φ,χθ) = arccos|⟨φ|χθ⟩| = θ√V + O(θ²).
 Every w ⊥ φ (complex, so every REAL tangent direction of CP^{2^N−1}, real dim 2(2^N−1)) arises: K = i(wφ†−φw†) gives Kφ = iw. ⇒ no subspace restriction.
 φ is a minimum (M2 ≥ 0, = 0 at φ), so gradient = 0 and the second-order form is curve-independent (any C² curve with the same velocity gives same θ² coefficient).
 ⇒ M2(χ) = (4/ln2)·d_FS(φ,χ)² + O(d³), isotropic. **Convention note:** "(4/ln2)·Id" is the coefficient of the QUADRATIC FORM (M2 ≈ Q(w));
 the Hessian MATRIX in the f ≈ ½wᵀHw convention, w.r.t. the real Hilbert inner product Re⟨·,·⟩ on the tangent space, is (8/ln2)·Id. Not an error, a labelling ambiguity.
 One unproved micro-step in S54's text: "O(θ³)" for ⟨P⟩⁴ on P∈S is fine (smooth); nothing missing. Derivation: CONFIRMED on paper.
**1b. Preregistration [OBSERVED]:** s55_prereg.md written before any S55 code; sha256 58f3ed87ec947b3041347eacc34c9604f9946fcd3e53d5780a42f287f5694fe1 (s55_prereg.sha256),
timestamp line appended inside the file (`date -u` at write, ~01:53 UTC).
**1c. Numerics N0–N2 [OBSERVED, 01:56–01:57 UTC]** (new code s55_lib.py + s55_d6.py, unit upr-s55-d6, out s55_d6.{out,err,json}; no S50–S54 imports):
- Lib sanity: Clifford-circuit states give M2 ≤ 3e-15 (N=1..5); 1q T-state M2 = 0.41504 = −log2(3/4) exact; N0 FWHT-vs-explicit-Pauli-matrices M2 max err 3.8e-15;
  enumeration of distinct stabilizer rays reaches exactly 60 (N=2) and 1080 (N=3) — the known counts.
- **N1:** 192 (state, direction) pairs, N=2..5 (6 random Clifford states × 8 random complex tangent directions each), geodesic second difference + Richardson:
  max |a − 4/ln2|/(4/ln2) = **8.8e-10** (prereg < 1e-4 → PASS). Unextrapolated h=1e-2: 2.4e-4 (pure O(h²) drift).
- **N2:** full real Hessian on the whole horizontal tangent space (dim 6 for N=2, 14 for N=3; 2 states each): all eigenvalues in [11.54144, 11.54153] vs
  8/ln2 = 11.54156 (max rel dev 1.05e-5), off-diagonal max 1.1e-5 (prereg 1e-3 rel → PASS). Isotropic: no subspace restriction.
**Item 1 verdict: CONFIRMED.** Quadratic-form coefficient 4/ln2 (Hessian matrix 8/ln2·Id in the ½vᵀHv convention, real FS/Hilbert metric), all directions, all tested states.

## Item 2 — D7 (bounds, uniform constants, LC covariance)
**2a. Paper audit [DERIVED, 02:00 UTC].**
(i) ✔ Stabilizer rays finite; LU compact ⇒ Z' = LU·stab is a finite union of compact orbits, distinct orbits disjoint ⇒ δ0 = dist(ψ0, Z'∖O) > 0. M2 = 0 iff stabilizer
   (Σ⟨P⟩⁴ ≤ Σ⟨P⟩² = 2^N, equality iff |⟨P⟩|∈{0,1} ∀P) — S54 used this without stating why; it is standard and true.
(ii) Uniform constants ✔: finitely many rays, each a nondegenerate min with the SAME isotropic Hessian (D6, now OBSERVED too), M2 is C^∞ near each ray (Σ⟨P⟩⁴≈2^N>0 inside the log),
   and the rays are isolated ⇒ ∃ε, C: in the ε-ball of each ray M2 ≥ (4/ln2)d²(1−Cd), outside all balls M2 ≥ c_ε > 0 (compactness). For d < 2/(3C), f(d)=d²(1−Cd) is increasing, which
   is needed to pass from d ≥ dist(ψθ,O) to f(d) ≥ f(dist(ψθ,O)) — S54 used monotonicity silently (minor, true).
   "Other stabilizer ray" question: for fixed U, d(Uψθ) = min_σ dist(ψθ, U†σ). Every σ with U†σ ∈ O is bounded below by dist(ψθ,O) (covers ALL branches on O: LC images,
   LU-but-not-LC images, and continuous families of Z — Z is not discrete, it contains the stabilizer subgroup of ψ0 in LU); every σ with U†σ ∉ O gives ≥ δ0 − dist(ψθ,ψ0) ≥ δ0/2.
   So no minimum can hide near an unconsidered stabilizer ray: the case split is exhaustive. ✔
   dist(ψθ,O) = θ·D + O(θ²): needs O a closed embedded submanifold with T_ψ0 O = horizontal projection of {i h ψ0} (h local Hermitian, incl. R). Standard (compact group orbits are
   embedded; orbit-map differential). ASSUMED-standard, not shown; I judge it safe. The identification of D with S51's least-squares D² requires D² = min_h ‖(1−Π0)(G+h)ψ0‖² over
   REAL span — i is an isometry, so i·T vs T makes no difference. ✔ (checked numerically in N4 with my own D²).
(iii) ✔ with one point S54 skipped: Uψθ = e^{−iθh}e^{−iθG}ψ0 is not e^{−iθ(G+h)}ψ0 (BCH θ²[h,G] term). Harmless: since φ is a minimum, the θ² coefficient of M2 along any C² curve
   depends only on the first-order velocity (normalisation fixes Re⟨φ|v2⟩ = −‖v1‖²/2 and the v2-dependence of ⟨P⟩, P∈S, cancels). So M2 = (4/ln2)θ²‖(1−Π)(G+h)ψ0‖² + O(θ³). ✔
LC-branch covariance ✔: for ANY local U0 with U0ψ0 stabilizer (Clifford or not), U0 maps (1−Π0)Gψ0 ↦ (1−Π_φ)(U0GU0†)φ and T_loc(ψ0) ↦ T_loc(φ) isometrically. S54 C2a confirmed to 3e-14.
Gaps (assumed vs shown): (g1) embedded-orbit / first-order distance fact — assumed (standard); (g2) M2=0⇔stabilizer — assumed (standard, one line); (g3) monotonicity of d²(1−Cd) — silent;
   (g4) BCH/curve-independence in (iii) — silent; (g5) θ-threshold and O(θ³) constant depend on (ψ0, G, partition) via δ0, ε, C, orbit curvature — pointwise asymptotic only, as S54's
   caveat says. None is a logical hole. Paper verdict: D7 sound.
**2b. N3 (global shape of M2 vs FS distance to the stabilizer set, N=2,3; s55_d7.py N3, unit upr-s55-N3, 01:58–01:59 UTC) [OBSERVED].**
All 60 / 1080 stabilizer rays enumerated; 20000 samples per N (half Haar, half near random stabilizer rays).
- (a) mean M2/((4/ln2)d²) for d<0.02: 0.99807 (N=2), 0.99826 (N=3) → PASS (|·−1|<2e-2).
- (c) no sample with M2<1e-6 and d>0.05 → PASS.
- (b) prereg "min M2/d² > 0" **FAILED as literally evaluated**: min = −0.0 (N=2), −0.216 (N=3), both at d ≈ 2e-8 / 7e-8 — i.e. M2 ≈ −1e-15 (float roundoff) divided by an
  arccos-roundoff d². This is a defect in my preregistered criterion/implementation (arccos(|⟨s|v⟩|) has ~1e-8 floor), not in D7. Recorded as a prereg failure.
- **POST-HOC N3b (NOT preregistered; s55_d7_N3b.py, same rng stream, robust d = arcsin‖v−⟨s,v⟩s‖) [OBSERVED]:** samples reproduce N3 exactly (same min ratios 0.49531 / 0.52507 at large d).
  For d > 1e-6: min M2/d² = 2.858 (N=2, at d=0.40) and 3.030 (N=3, at d=0.75) — strictly positive, i.e. global ratio M2/((4/ln2)d²) ≥ 0.495 / 0.525 on the samples.
  mean ratio on 1e-4<d<0.02: 0.99989 / 0.99995. Points with d ≤ 1e-6 (16 / 9) have |M2| ≤ 5.6e-12 (roundoff zeros).
  Interpretation [DERIVED]: consistent with D7(ii): near rays M2 ≈ (4/ln2)d²(1−O(d)) (ratio bins decrease smoothly: 0.997→0.99→0.97→0.84 as d grows), and away from rays a
  uniform positive constant. Ratio < 1 for d>0 means the cubic correction is NEGATIVE on average (M2 ≥ (4/ln2)d²(1−Cd) with C>0 is the right form; S54 wrote it that way ✔).

**2c. N4 end-to-end, fully independent (s55_d7.py N4, unit upr-s55-N4, 01:58–02:01 UTC) [OBSERVED].** Own D² (real least squares over local Hermitian generators of R,A,B),
own LU-min (BFGS in exp-chart with chart re-centring, 10 restarts: 1 identity + 9 Haar-random local unitaries), r = LUmin/((4/ln2)D²θ²):
| case (R|A|B) | D² | r(0.08) | r(0.04) | r(0.02) | spread over 10 restarts @0.02 | prereg |
|---|---|---|---|---|---|---|
| GHZ (1|1|1) | 0.1897 | 0.98526 | 0.99283 | 0.99646 | 0.99646–0.99654 | PASS |
| |0⟩|Φ+⟩ (1|1|1) | 1.2353 | 0.97395 | 0.99570 | 1.00005 | identical | PASS |
| rnd stab N=4 #0 (1|2|1) | 1.7966 | 0.97603 | 0.99458 | 0.99893 | 0.99893–0.99903 | PASS |
| rnd stab N=4 #1 (1|2|1) | 1.5748 | 0.98222 | 0.99994 | 1.00215 | 1.00215–1.00216 | **FAIL (monotonicity)** |
- No restart (incl. 9 Haar-random starts, which land on generic LU branches) ever went below the identity-start value by more than 1.2e-7 relative (optimizer noise; all
  ≥ ident·(1−5θ)). Every restart converged to the same r → the min over the LU orbit is attained only on the identity-branch basin (up to LU symmetry). Supports D7(ii).
- rndstab4_1 failed my preregistered "|r−1| monotone decreasing" criterion: |r−1| = 0.0178, 6.1e-5, 0.00215. Exact 2-term fit through the three points [arithmetic]:
  r−1 = 0.217θ − 5.46θ² — a sign crossing of r−1 near θ≈0.04 (the O(θ) slope and the O(θ²) term have opposite signs). |0⟩|Φ+⟩ shows the same crossing (passed only by luck of
  where θ samples sit). This is a defect of the monotonicity criterion for small finite θ, not evidence against r→1. Post-hoc N4b (below) extends θ to 0.01, 0.005 to test.
**2d. POST-HOC N4b (NOT preregistered; s55_d7_N4b.py = s55_d7.py + θ∈{0.01,0.005} for rndstab4_1; same rng stream; unit upr-s55-N4b, 02:01–02:05 UTC) [OBSERVED]:**
first four cases reproduce N4 bit-for-bit. rndstab4_1 r(θ) = 0.98222, 0.99994, 1.00215, 1.00162, 1.00097 at θ=0.08…0.005; |r−1| halving ratios at small θ: 0.75, 0.60 (→0.5).
Fit through θ=0.01, 0.005 [arithmetic]: r−1 = 0.225θ − 6.3θ² (vs 0.217θ − 5.46θ² from the 3 coarse points — stable). So r → 1 linearly; the prereg failure was the sign crossing of r−1 at θ≈0.04.
At θ=0.01 one random restart beat the identity start by 2e-6 relative (BFGS stopping noise at M2~1e-4; far inside 1−5θ). **N4 item verdict after N4b: consistent with D7.**

**Item 2 verdict: CONFIRMED (with stated assumed-standard steps g1–g5; two preregistered numeric criteria failed for criterion-design reasons — N3(b) roundoff at d~1e-8,
N4 monotonicity under a sign crossing — both resolved by labelled post-hoc reruns, neither contradicts D7).**

## Item 3 — Steane 713 consistency
**3a. Independent coefficient [OBSERVED, 02:00 UTC]** (s55_steane.py, unit upr-s55-steane; S50–S53 modules used ONLY to rebuild the identical ψ0 and G via the same rng stream as
s54_c2.py mode b; D² recomputed by my own real least squares over local Hermitian generators on the permuted R|A|B tensor): D²_own vs S54 half-coset D²:
513 Δ=5.6e-17, 422 Δ=0, rnd61 Δ=3.2e-15, **713 D² = 0.166056228 (Δ=2.8e-17) → coef 0.958274** = S54's 0.9583. Also confirms the r-denominators of all four C2b runs.
**3b. Steane r(θ) analysis [OBSERVED numbers from s54_c2b713.json; fit is arithmetic]:** r−1 = 0.01193, 0.00652, 0.00340 at θ=0.08/0.04/0.02; halving ratios 0.546, 0.521 (→0.5 = linear);
exact quadratic fit r = 0.999997 + 0.1768θ − 0.346θ²; Richardson linear extrapolation from the last two points r(0) = 1.00027. r_global − r_ident = 0 exactly at all θ.
**3c. Consistency with D7 [DERIVED]:** D7 predicts r(θ) = 1 + O(θ) (remainder O(θ³)/θ²) and that no branch beats the identity-branch coefficient. Steane: intercept 1 to 3e-6, linear
approach with positive slope (+0.177, i.e. positive θ³ term for this G — sign is G-dependent, cf. S54 422/rnd61 r<1 and my N4 cases r<1), global = identity. **CONSISTENT.**
Caveat (carried from S54): r_global = r_ident exactly means the 7 random restarts never went below the identity start; which branch they converged to is not recorded,
so "other branches explored" remains unshown for the S54 runs (my N4 records per-restart values: they converge to the same value, see 2c).

## Verdicts (02:06 UTC)
| item | verdict | basis |
|---|---|---|
| 1 D6 Hessian = (4/ln2)·Id | **CONFIRMED** | DERIVED re-derivation (all real tangent directions, sign/phase irrelevant since ⟨P⟩⁴); OBSERVED N1 192 dirs N=2..5 max rel 8.8e-10; N2 full Hessian eig 8/ln2 ±1.1e-5 (N=2,3). Convention: 4/ln2 is the quadratic-form coefficient (Hessian matrix in ½vᵀHv convention = 8/ln2). |
| 2 D7 C2 bounds | **CONFIRMED (paper sound; gaps g1–g5 are standard facts/silent steps, not holes)** | DERIVED audit: case split over stabilizer rays exhaustive incl. non-LC branches and continuous Z; monotonicity and BCH steps silent but true; constants pointwise in (ψ0,G). OBSERVED N3 (60/1080 rays, global ratio ≥0.495/0.525, →1 near rays), N4 4 independent instances no lower branch over 9 Haar restarts; 2 prereg criteria failed for design reasons, fixed post-hoc (labelled). |
| 3 Steane 713 | **CONSISTENT with D7** | coef 0.958274 reproduced by independent D² (Δ=2.8e-17); r−1 halving 0.546, 0.521, intercept 1.000 (quad fit 0.999997); global = ident exactly. |
Not checked: θ³ coefficient sign/size (D7 does not predict it); N≥5 end-to-end LU-min with my own optimizer (Steane relied on S54's lu_min for r, my code only for the coefficient).
NEXT: S54 NEXT (a) θ³ coefficient — note N4 shows the linear term can have either sign with an O(θ²) term of opposite sign, so finite-θ "r≥1" claims are unsafe; (b) |Bi_P|-even conjecture;
(c) Scout read of arXiv:2603.13475; (d) optionally an explicit-constant version of D7 (orbit curvature bound).

## Artifacts (s55/)
S55-validate-c2.md; s55_prereg.md + s55_prereg.sha256; s55_lib.py; s55_d6.py + s55_d6.{out,err,json}; s55_d7.py + s55_d7_N3.{out,err,json} + s55_d7_N4.{out,err,json};
s55_d7_N3b.py + s55_d7_N3b.{out,err,json} (post-hoc); s55_d7_N4b.py + s55_d7_N4b.{out,err} + s55_d7_N4b.json (post-hoc); s55_steane.py + s55_steane.{out,err,json}; SHA256SUMS-s55.
S54 artifacts untouched (read-only). Session 01:51–~02:08 UTC.
