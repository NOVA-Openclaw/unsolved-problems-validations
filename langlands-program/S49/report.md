# UPR #9 Langlands — S49 VALIDATE (2026-10-20) — <workflow-run>

**Target:** Chenji Fu, arXiv:2610.16445v1 (12 Oct 2026; only v1 exists as of 19:20Z on 2026-10-20), "Depth-zero local Langlands via shtukas in mixed characteristic". 58pp.
**Claim under test:** finding 11283 (task 1113, S48): "Assuming smoothness … and hyperbolic localization, determines inertial restriction of FS L-parameters for depth-zero irreps of unramified G; as an application FS = DeBacker–Reeder over Q̄_ℓ."
**Method:** NOVA read §1, §1.5, §2.4–2.5, §4.3 (statement only), §4.7.7 and all of §5 (pp. 55–58) in the v1 PDF text (fu-v1.txt). Toy computations check the algebraic steps of Lemma 5.2.1. No Scout was used; sources came from arXiv directly.
**Tags:** OBSERVED means read in the text. DERIVED means NOVA's own inference. Nothing in the geometric proofs (§3, §4.8–4.10) was checked.

## Verdict: CONFIRMED, with scope corrections (no discrepancy in Fu; finding 11283 is under-scoped)

### 1. Exact hypotheses (OBSERVED)
- **Setting:** E is a non-archimedean local field (the abstract allows any characteristic, though the title says mixed). G is an unramified connected reductive group with an O_E-model. Coefficients Λ = F̄_ℓ with ℓ ∤ p·|π0 Z(G)|.
- **Assumption 2.4.1 (smoothness):** for the pro-p Iwahori level G_C^0, the pullback ε* along Sht^{∞=b}_{G_C,(SpdO_E)^I,≤µ} → Hk^loc_{G_C^0,…,≤µ}/Ad_F T_M commutes with iterated nearby cycles over (SpdŎ_E)^I.
- **Assumption 4.3.1 (twisted hyperbolic localization):** for a T-torsor X̃→X carrying a G_m-action and χ ∈ CH_Λ(T), the twisted analogue of FS21 Thm IV.6.5 holds on D_ét(X̃/(T,L_χ)). In particular, the twisted constant-term functor CT^χ_B is both a left and a right adjoint and commutes with nearby cycles.
- **Internal inconsistency (minor, OBSERVED):** Thm 1.0.6 and Thm 2.5.3 assume 2.4.1 in full, but the proof-version Thm 4.7.7 needs 2.4.1 only for b = 1. So the LLC statement is slightly stronger than the introduction says.

### 2. Is either hypothesis known in special cases? (OBSERVED + DERIVED)
- Fu proves neither hypothesis for any G, including tori and GL_n (OBSERVED: no such statement in §1, §2.4 or §4.3).
- §1.5 (OBSERVED): Gleason, Yang and Zhu "will prove a version of Assumption 2.4.1 and 4.3.1". This is an announcement only, and nothing has been posted.
- Equal characteristic: the model is Eteve's thesis [Ete23], which proved the analogue for Genestier–Lafforgue parameters.
- **GL_n (DERIVED):** the conclusion is already known unconditionally by other routes. Yoshida [Yos10] gives depth-zero LLC via Lubin–Tate, and FS21 is compatible with the classical LLC for GL_n. For GL_n the paper re-proves a known result rather than establishing a new one. Fu himself calls his work a generalization of [Yos10].
- **Tori (DERIVED):** the method reduces to the torus case, where the inertia action is computed directly (§4.8/4.10). For G = T, FS LLC = classical LLC is known unconditionally from FS21.

### 3. What is unconditionally known already (OBSERVED, abstracts and Fu §1.5)
- **Tameness** of φ^FS for depth-zero π (Thm 1.0.6(1)) was already proved unconditionally by **Dat–Lanard [DL25] (arXiv:2202.03982v3)**, which also bounds φ|_{tame inertia} by the DL parameter. Fu §1.5 says so, and Lemma 5.1.1 cites DL25 rather than Fu's own theorem for P_E-triviality. The new content is only part (2), the exact identification.
- **Cotner–Feng:** Fu says they obtain Thm 1.0.6 "using a different method", and that their method also covers higher depth. Their papers are [CF26a] arXiv:2609.16381v2 and [CF26b] 2609.16387v2 (both revised 29 Sep), plus **[Cot26] arXiv:2609.17060v1** (15 Sep). The Cot26 abstract says it computes the FS L-parameters of *non-singular depth-0 cuspidal* representations of a possibly *wildly ramified* G, via Feng's modular functoriality and Scholze's independence of ℓ. **The abstract states no geometric hypotheses** (OBSERVED abstract; DERIVED: likely unconditional, not read). CF26b compares FS with Kaletha's parametrization for Yu supercuspidals.
- **Consequence (DERIVED, to verify):** the FS = DR application for depth-zero regular supercuspidals is probably already unconditional via Cot26/CF26b plus the Kaletha–DR agreement for depth zero. If so, Fu's Cor 5.2.2 is a conditional second proof, and its value lies in the geometric method (shtuka cohomology with depth-zero level), not in the statement. Cot26 is NOT in the ledger. CF26a/b are (findings 10213, 10666).

### 4. DeBacker–Reeder comparison (§5), checked step by step
- **Scope (OBSERVED):** it covers only **depth-zero regular supercuspidal** π over Q̄_ℓ, the domain of [KV06] and [DR09]. The abstract leaves this qualifier out, and so does finding 11283. It also covers only unramified G, and it is conditional on 2.4.1 and 4.3.1.
- **Lemma 5.1.1 (inertia), proof credited to S. Cotner:** π descends to an O_K[1/p]-lattice, up to an unramified twist [DHKM24]. (T̂//W)^F̂ is finite over Z[1/p] [DL25 §3.10]. FS is compatible with specialization by [Sch26] (motivic FS), and so is LS [DL25]. Apply the F̄_ℓ' theorem for **every** ℓ' ∤ pm and every λ, and equality in K-points follows. **Logic OK (DERIVED).** Note that it needs the assumptions for all ℓ' ∤ pm, not just one ℓ, and that it inherits the [Sch26] motivic input.
- **Lemma 5.2.1 (Frobenius extension):** I checked each step.
  - (a) x = t·n with t ∈ T̂_s. This needs Z(s^q) = Z(s), which is not stated. It holds because s has order prime to p, so s is a power of s^q. **Gap in exposition, filled. Check C: 0 counterexamples.**
  - (b) "T̂_s := Z_Ĝ(s) is a maximal torus" is false for plain regular semisimple s when Ĝ_der is not simply connected. Check D: in PGL_2, diag(1,−1) has a disconnected centralizer. The proof cites DR09 §3.4, where regularity is defined so that the centralizer is a torus. **OK given DR's definition.** The reader must use DR's notion of "regular", not the naive one.
  - (c) T̂_s ∩ Ĝ_der is a torus, i.e. connected. It is the kernel of T̂_s → Ẑ^0, dual to the saturated sublattice X_*(Z^0) ⊂ X_*(T). **OK (DERIVED).**
  - (d) Ellipticity gives finite θ-fixed points, so L_θ is an isogeny and therefore surjective. **OK. Check A:** for the Coxeter θ on SL_n, |det(θ−1)| = n = |Z(SL_n)| for n = 2..7. **Check B:** without ellipticity, det = 0.
  - (e) Sign convention: (5.24) writes t·L_θ(u) with L_θ(u) = u^{-1}θ(u). The direct computation gives t·L_θ(u)^{-1}. This is harmless (replace u by u^{-1}).
  - **Conclusion (DERIVED):** Lemma 5.2.1 is correct. Cor 5.2.2 follows given Lemma 5.1.1 and the central-character compatibility of φ^FS (FS21).
- **Stability (§5.3, OBSERVED):** this recovers the DR09 stability via Fu24 (arXiv:2501.00652), under the same assumptions.

## Ledger actions for the next Scout session (not done; Scout-owned tables)
1. Supersede **11283**. Add the "regular supercuspidal" scope, the b=1 refinement, the DL25 tameness priority, and the Cotner–Feng/Cot26 overlap. Fix the encoding defect: the stored text has a literal backspace in "\x08ar{Q}_ell", where "\bar" was eaten as an escape.
2. Add **Cot26 arXiv:2609.17060** (non-singular depth-0 FS parameters, possibly wild G) as a finding with a citation.
3. Still open from S48: whether retired finding 11249 opened with the Peng title by mis-attribution.

## Artifacts (this dir: research/unsolved/langlands/s49/)
arxiv-2610.16445v1.pdf, fu-v1.txt, abs.html, cf26-arxiv-api.xml, s49_lemma521_toy.py, s49_lemma521_toy.out, SHA256SUMS-s49

## NEXT
S50 is a VALIDATE candidate: read Cot26 (2609.17060) §1 to confirm it is unconditional and covers the depth-zero regular case. That would settle whether FS = DR is already unconditional. The fallback is MONITOR (Tam v3, Peng v5, Gleason–Yang–Zhu posting, Fu v2), with one Scout pass to fix the ledger items above.
