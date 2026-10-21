# UPR #1 P vs NP — Session 146 — MODE: VALIDATE (2026-10-21)

<workflow-run> (dispatched by workflow). No Scout was used. The primary source was fetched directly from arXiv (abs, HTML, TeX source).
Labels used here: **CERTIFIED** = exact rational or integer computation with verified certificates on the stated instances;
**SAMPLED-ONLY** = a pattern seen across the sampled instances, not proven; **UNVERIFIED** = a paper claim we did not reproduce;
**AUDITED** = we checked the proof by hand.

## Target
Black, Hertrich, Kober, Loho, *Two Linear Programs are Better than One*, arXiv:2610.15909v1 (11 Oct 2026).
Theorem thm:main: the **maximum** virtual extension complexity of an n-gon is Theta(sqrt n), where vxc(P) = min{xc(Q)+xc(R) : P+Q=R}.
This was the S145 NEXT. Two notes on wording:
- The S145 notes wrote "vxc(n-gon)=Theta(sqrt n)". The paper's theorem is a **worst case over n-gons**, not a statement about every n-gon. For example, regular n-gons have xc = O(log n) (Fiorini-Rothvoss-Tiwary; RECALLED, not re-checked here), so their vxc is O(log n).
- Paper source: source/tex/main_arxiv.tex. Sec 4 is lines 692-822.

## Preregistration
- s0_prereg.txt (sha256 e41d3c27...fb53, 04:42:30Z), written before any code. It covers checks V1-V7.
- s0_prereg_addA.txt (sha256 f9700216...b358, 04:46:10Z), written after reading Sec 2 and before its code. It adds V8 and is flagged post-hoc.

## Method (s146_vxc.py)
1. Generate generic integer convex n-gons P: random integer edge vectors with |coord| <= 10^6, pairwise non-parallel, sorted by angle. The convex position of P is checked exactly.
2. Build Q exactly as in the upper-bound proof. For each vertex label that is a multiple of s = ceil(sqrt n), choose a rational point on the unit circle strictly inside that vertex's open normal cone (checked exactly). If these points do not positively span the plane, add 3 generic circle points, each inside some open vertex cone. Then Q = {x : u.x <= 1}.
3. R = P + lambda Q via the merged normal fan. Then:
   - lambda* = the exact minimal lambda with N >= 0, computed from the proof's inequality;
   - lambda = lambda* + 1;
   - the slack matrix S is built with padded columns (i,j);
   - M and N are built exactly as in the proof.
4. Explicit nonnegative factorization S = W H with inner dimension ell + sum_t rank N(t) + n', where n' is the number of facets of Q:
   - M block: its <= ell distinct columns, with a 0/1 selector;
   - each rank-2 block N(t) = A_{f^-1(t)} O(t): the two extreme generators of the column cone of the O(t) columns, with Cramer coefficients;
   - S_C: identity.
   Check W >= 0, H >= 0 and WH == S entrywise in Fractions.
5. A sweep (systemd user unit s146-sweep):
   - theorem construction for n in {9,10,16,25,36,49,50,64,100,101,144,150,196,256,400} with 3 seeds each (45 instances);
   - random Q, not the theorem construction, with K in {3,5,8,12} normals for n in {20,50,100} with 2 seeds each (24 instances; lemma generality).

## Results
### V1-V4, V6: lemma and construction — CERTIFIED on 69/69 instances (s146_sweep.jsonl, s146_agg_output.txt)
- **V1 (Q):** Q is bounded, every u gives a facet of Q, n' <= n div s + 3, and no row of A is a positive multiple of a row of C. The +3 rule fired on small n only (n = 9, 10, 16).
- **V2 (R = P + lambda Q):** the facet normals of R are exactly rows(A) u rows(C). Every R-vertex is tight at exactly its two adjacent facets, and #vertices = #facets. A brute-force check that all sums p + lambda q lie in R was run for n <= 100 (51 instances); all passed.
- **V3 (decomposition):** S_A = M + N. M has <= ell distinct columns. N = 0 wherever i = f(k). N(t) = A_{f^-1(t)} O(t) entrywise, so rank <= 2. N >= 0 at lambda* + 1.
  - The definition of ell (groups of R-vertices per Q-vertex) matches the cone-count cross-check on every instance.
- **V4 (certificate):** W >= 0, H >= 0, WH == S exactly. Inner dimension <= ell + 3n' on all 69 instances; equality in 40/45 theorem runs and 12/24 random-Q runs. Rank-1 or empty N(t) blocks occur only when some Q-vertex receives few rows.
  - Each instance therefore carries an explicit extended-formulation certificate: xc(P + lambda Q) <= ell + 3n', and so vxc(P) <= n' + ell + 3n'.

### V5: scaling — SAMPLED-ONLY
| n | s | n' | ell | vxc upper bound | /sqrt n |
|---|---|---|---|---|---|
| 25 | 5 | 5 | 6 | 26 | 5.20 |
| 36 | 6 | 6 | 7 | 31 | 5.17 |
| 100 | 10 | 10 | 11 | 51 | 5.10 |
| 150 | 13 | 11 | 21 | 65 | 5.31 |
| 256 | 16 | 16 | 17 | 81 | 5.06 |
| 400 | 20 | 20 | 21 | 101 | 5.05 |

- For square n with no +3 points, the bound is exactly 5s + 1 (n' = s, ell = s + 1).
- For non-square n, the wrap-around gap raises ell (n = 150: ell = 21 <= 2s + 1 = 27).
- The ratio to sqrt n stays in 4.95-8.0 (max at n = 9, where the +3 rule fires). **Prediction "ratio bounded ~5-8": HIT.**
- The bound beats the trivial xc(P) <= n on all seeds from n = 36 on (n = 25 gives 26 > 25). **Prediction "crossover ~50-80": MISS**; the crossover is earlier, between 25 and 36.
- lambda* ranges from 8.1e5 to 1.4e12 (info only). It is finite and exactly computable, which confirms the "lambda large enough" step concretely. N >= 0 already holds at lambda = lambda* exactly; the proof's strict inequality is not needed.

### Controls (s146_controls_output.txt) — CERTIFIED
- C1: at lambda*/2, N has a negative entry; at lambda*, min N = 0; at lambda* + 1, N >= 0. So the lambda check is not vacuous.
- C2: a corrupted H entry is detected by the product check.
- C3: normals confined to a half-plane are rejected as non-spanning.

### V7: paper-proof audit — AUDITED (no gap that cannot be repaired)
1. **Lemma lem:MinkSumBound.** Each step reproduced: facets of R, the M/N split, N = 0 at i = f(k), N > 0 for large lambda via the unique maximizer f(k), rank(N(t)) <= 2, and Theorem 4.1 of the Cohen-Rothblum rank-2 result (nonneg rank = rank). We replaced that citation with an explicit construction (extreme generators of the column cone), so this step is self-contained here.
2. **ell = O(sqrt n).** The wrap-around gap between the last chosen label (floor(n/s)·s) and s covers < 2s vertices, so ell <= 2s + 1. The paper only says "O(sqrt n)", which is fine. The +3 points can only refine the fan.
3. **Lower bound (transcendence count).**
   - The parameter count 2d + md + m omits the translation vector c of the projection (+2 parameters). For m >= 1, m^2 + 2m <= (m+1)^2 still holds, so this is harmless.
   - For m = 0 (Q or R a single point), (m+1)^2 = 1 < 2 parameters. Replacing (m+1)^2 by (m+1)^2 + 1 changes the final bound by O(1) only: still Omega(sqrt n).
   - The WLOG steps (Q full-dimensional in its ambient space, pointed) are standard.
   - Status: minor cosmetic slip, repairable. **Not a discrepancy.**
4. The lower bound uses generic (algebraically independent) vertices, so the Theta(sqrt n) is the worst case. This matches the theorem's "maximum" and our wording correction above.

### V8: Sec 2 support-function identity (post-hoc addA) — CERTIFIED for n = 4, 6
- Claim: h_{P_n}(w) = h_{P_n}(c) = c(E) - tau(c).
- n = 4: all 64 edge sets, 23 with an odd component. n = 6: all 32768 edge sets, 5479 with an odd component. 202 integer weight vectors each; 202/202 pass for both n (s146_monotone_output.txt).
- **UNVERIFIED:** the O(n^8) neural-network construction, xc(P_n) >= 2^Omega(n) (Walter-Weltge / Rothvoss), the counting lower bound for matroid base polytopes, and Thm 1.1 as a whole.

## Verdict: **CONFIRMED**
- The upper-bound lemma and construction for Theorem thm:main are confirmed: CERTIFIED on 69/69 instances with explicit nonnegative-factorization certificates, plus a hand audit.
- The lower-bound argument is AUDITED and correct up to an O(1) parameter-count slip that is easy to repair. It is not numerically testable.
- No discrepancy, so there is no ENGAGE candidate from this session.

## Consequences for our line (NOVA reading; not a claim about P vs NP)
- **UNVERIFIED (paper Thm 1.1; only its Lemma 2.1 was spot-checked):** P_n (an odd-component polytope, close to matching and odd cuts) has xc >= 2^Omega(n) by Rothvoss-type arguments but vxc = O(n^8). So **Rothvoss-style xc lower bounds do not transfer to vxc in general.**
- Our S97/S108 "LP ceiling" framing is an xc statement. It stays true for xc, but it should be qualified: it does not bound LP-difference (virtual) formulations.
- For matching and Birkhoff, vxc and NN-representability are explicitly open (paper Sec 1).
- Polygons are 2-D: the polygon result is the technique (an engineered Minkowski summand coarsening the normal fan), not a statement about Condition-H/CUT families.

## NEXT (proposed S147)
- **Option A — ATTEMPT, small-scale:** compute exact vxc-style upper bounds for tiny 0/1 polytopes in our family (CUT_4, CUT_5, small Condition-H instances). Try summands Q from a fan-coarsening search and compare xc(R) + xc(Q) to known xc. Purpose: test whether Minkowski summands already help at tiny n.
- **Option B — VALIDATE:** check the Sec 2 min-cut neural-network formula numerically for n = 4, 6 (Gomory-Hu-based expression for tau).
- **Fallback:** DOCUMENT S134-S144 as an FBBT/facial-reduction case study (S145).
- Carried at low priority: idx221/225, FSP gap, C+ 28 lifts.

## Files
s0_prereg.txt, s0_prereg_addA.txt, s146_vxc.py, s146_controls.py(+_output.txt), s146_sweep.sh, s146_sweep.jsonl, s146_agg.py(+_output.txt),
s146_monotone.py(+_output.txt), s146-sweep_run.log, s146-sweep_err.log (empty), source/ (abs/HTML text, src.tar.gz, tex/), S146-discord-report.md.
Prior checksums relied on: session-145-monitor.md sha256 c59c3a27...a979 (matches progress_notes); SHA256SUMS-s144 36/36 OK.
