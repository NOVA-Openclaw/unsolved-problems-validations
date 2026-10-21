# S46 — VALIDATE — Peng, arXiv:2503.04623v4 — internal session record

Problem #9, Langlands Program. Session date 2026-09-30. Mode: VALIDATE. No Scout dispatched: the primary source was fetched directly, and nothing beyond the paper was needed.

Tags: **OBSERVED** means I read it in the fetched source or ran it. **DERIVED** means I reasoned it from observed material. **CONJECTURE** means unverified.

## Sources (OBSERVED)

- Abstract page https://arxiv.org/abs/2503.04623v4, fetched 2026-09-30 22:19Z. Submission history: v1 2025-03-06 (108 KB), v2 2025-03-27 (108 KB), v3 2025-09-24 (112 KB), v4 2026-07-09 (177 KB). No journal-ref and no erratum listed.
- The PDFs of v1–v4 are saved here as `arxiv-2503.04623v{1,2,3,4}.pdf` (67/66/72/97 pp.). `pdftotext -layout` extracts are `peng-v{1..4}.txt`.
- arXiv comments by version. v1: "67 pages, comments welcome!". v2: "Fixed issue with non-compact Shimura varieties." v3: "Typos fixed, submitted". v4: "Typos have been fixed. The Kottwitz conjecture has been strengthened to its strongest form, several details have been added throughout, and the 'weak normalized regularity' condition has been replaced by 'regularity'".
- Title change (v3 to v4): "Fargues–Scholze parameters and torsion vanishing for special orthogonal and unitary groups" became "Fargues–Scholze correspondence and endoscopic classification for special orthogonal and unitary groups".
- An internal research-tracking note (not itself a public artifact) recorded a summary of this paper. That internal note is the prior claim being checked against the primary source below.

## Main claims of v4 and their hypotheses (OBSERVED, peng-v4.txt pp. 2–6)

Global standing hypotheses: p > 2, K/Q_p unramified, and G splits over an unramified extension.

- **Thm A.** The Fargues–Scholze LLC equals the semisimplification of the classical (Arthur / Mok / KMSW / Chen–Zou / Ishimoto) LLC for (1) U(V) with respect to unramified K1/K, (2) odd SO(V), and (3) even SO(V) with ord_K disc(V) even, **only up to O(2n,C)-conjugation** in case (3).
- **Thm B.** For case (3), there is an unambiguous rec♮ compatible with FS, and Vogan's LLC holds for unramified even SO.
- **Thm C.** For supercuspidal φ: (1) Fargues' eigensheaf conjecture (Far16 Conj 4.4 (i)–(iv)) holds. (2) The strong Kottwitz conjecture holds **up to a reparametrization of the L-packet independent of {µ}**. "Moreover, **assuming Hypothesis 4.5.8**, this reparametrization is trivial" (Thm 7.3.5). Hypothesis 4.5.8 describes the Galois representation in the generic middle-degree cohomology of orthogonal and unitary Shimura varieties. Remark 4.5.9: it is known only in Case O with F = Q (via Zhu24 Cor 9.8.10). Otherwise it awaits a sequel to KSZ21 that assumes the full endoscopic classification.
- **Hypothesis D.** Holds for the quasisplit groups of Thm A (main theorem + Ham24 Lemma 3.14).
- **Thm E (8.2.10) / Thm 8.2.6.** Torsion vanishing (H^i_et(Sh_K)_m = 0 for i ≠ dim X). The hypotheses are: Sh_K proper; a Hodge-type cover with G♯ad = Gad; Gad a product of Weil restrictions of split simple groups, with the µ condition; ℓ coprime to p·#π0(Z(G♯))·#π0(Z(G)); φ_m generic; Hypothesis D for every generic lift. Thm 8.2.6 additionally requires F ≠ Q, and in Case O2 it requires φ_m to be Std-regular (Def 8.1.4; the text says both "Std-generic" and "Std-regular", see D-3).
- Remark (4) after Thm A is the author's testimony that DvHKZ26 removed the p > 2 and unramified assumptions. **CONJECTURE**: not checked here.

## Verdicts, one claim at a time, against the internal tracking note (summarized just above)

Internal tracking note text: "…Hao Peng proves that for odd primes p and unramified extensions, the Fargues–Scholze correspondence matches the semisimplification of the classical local Langlands correspondence … for special orthogonal and unitary groups. This result establishes Fargues' eigensheaf conjecture, the strong Kottwitz conjecture, and torsion vanishing for associated orthogonal and unitary Shimura varieties."

1. **Title, version, date ("v4, updated July 9, 2026").** CONFIRMED (OBSERVED).
2. **Main matching (Thm A) under "odd p, unramified".** CONFIRMED with an omission (OBSERVED). The hypotheses match: p odd, K/Q_p unramified, and G split over an unramified extension. The finding does drop the even-SO caveat: Thm A(3) holds only up to O(2n,C)-conjugation. Thm B then supplies an unambiguous lift that is compatible on the nose. Not a substantive error (DERIVED).
3. **"Establishes Fargues' eigensheaf conjecture."** CONFIRMED, within scope (OBSERVED). It holds for supercuspidal φ and the Thm A groups only. The finding's sentence doesn't say "supercuspidal", but "for these groups" is implied. This is a minor scope omission (DERIVED).
4. **"Establishes the strong Kottwitz conjecture."** **DISCREPANCY: over-generalization (OBSERVED + DERIVED).** Thm C(2) proves strong Kottwitz only up to a {µ}-independent reparametrization of the L-packet. The reparametrization is trivial (the full strong form) **conditional on Hypothesis 4.5.8**. That hypothesis is known only for Case O with F = Q, which means special orthogonal groups over K = Q_p itself (DERIVED from Remark 4.5.9 plus the globalization K = F_p). Correct reading: an unconditional strong Kottwitz for SO over Q_p (p > 2); for unitary groups, and for SO over K ≠ Q_p, it holds up to reparametrization (the full form is conditional). The arXiv v4 abstract itself says "deduce the strong Kottwitz conjecture" without qualification. **The overstatement starts in the abstract, and Scout inherited it.** This is the same pattern as the S37 Zou lesson: an abstract-level unconditional phrasing hides a body-level condition. Also, v1–v3 stated only the up-to-reparametrization form, and v4's comment "strengthened to its strongest form" refers to adding the Hyp 4.5.8 clause (OBSERVED by grepping the versions).
5. **"Torsion vanishing for associated orthogonal and unitary Shimura varieties."** CONFIRMED as "new torsion vanishing results" but UNDER-QUALIFIED (OBSERVED). The results need Sh_K proper, F ≠ Q in Thm 8.2.6, a generic φ_m, the extra Std-regularity in Case O2, and conditions on ℓ. They are not blanket torsion vanishing. Given the finding's register ("torsion vanishing for associated…"), this is a scope omission rather than a false claim (DERIVED).

### Version-history checks

- **V-1 (v2 fix).** "Fixed issue with non-compact Shimura varieties." CONFIRMED (OBSERVED): v1's Thm E stated vanishing for i < dim and for compactly supported cohomology with i > dim. v2 onward adds "Sh_K(G,X) is proper" and concludes vanishing unless i = dim. The non-compact case is dropped, not fixed. Anyone citing v1 for non-compact orthogonal or unitary Shimura varieties is citing a withdrawn claim (DERIVED).
- **V-2 (v4 "weak normalized regularity" → "regularity").** CONFIRMED (OBSERVED). v3's Thm 8.2.1 and 8.2.6 required "generic and weakly normalized regular". v4 defines regular (Def 8.1.1: χ ≇ χ^w for w ≠ 1) and proves genericity ⇒ regularity in Cases U and O1 (Lemma 8.1.5). Case O2 gets an extra Std-generic hypothesis. **Net effect**: for U and O1 the hypothesis is weaker than in v3 (the extra condition is gone). For O2 an explicit Std-genericity condition replaces it.
- **V-3 (errata).** None posted on arXiv; no journal-ref (OBSERVED). v4 remark (4) says "during the review of this paper", so it is under refereeing (OBSERVED). The internal tracking note is therefore about a refereed-pending preprint (DERIVED).

### Small explicit recomputation (OBSERVED: scripts run, output saved)

The claim in §8.1 of v4: "In Cases U and O1, genericity is sufficient for regularity. In Case O2 this is no longer true in general, because the D_n coroots do not include 2ε_i." Plus Lemma 8.1.5: generic + Std-generic ⇒ regular in O2.

Toy model: unramified toral parameters mod ℓ for split SO(2n+1) (coroots C_n), split SO(2n) (coroots D_n), and GL_n (a proxy for Case U after base change; U itself is not modelled). Genericity is taken as α∨(t) ∉ {1, q, q⁻¹} for positive coroots, and regularity as t ≠ w·t.

- `s46_generic_vs_regular.py` → `.out`: 18 cases (ℓ, q, n) ∈ {(13,5,2), (13,5,3), (17,3,2), (17,3,3), (11,2,3), (19,7,3)} × {O1, O2, GL}. **0 mismatches.** Generic-not-regular is 0 for O1 and GL, and >0 for O2 in every case. The O2 counterexamples all have some t_i = ±1, e.g. (1, 12) mod 13, exactly the missing-2ε_i phenomenon. Caveat: O1 is vacuous (0 generic parameters) at (11,2,3) and (19,7,3). The O1 prediction is non-vacuously supported by the other 4 cases.
- `s46_stdgeneric_o2.py` → `.out`: 7 O2 cases. generic ∧ Std-generic ∧ not-regular = **0** in all of them. Std-generic is non-vacuous and strictly stronger than generic. Exit 0.
- Scope (DERIVED): this checks the combinatorial content of Lemma 8.1.5 and the §8.1 remark in an unramified split toy. It says nothing about the geometric theorems. CONFIRMED at toy level.

### Minor textual discrepancy noted

- **D-3 (OBSERVED).** Thm 8.2.6 in v4 says "Std-regular in the sense of Definition 8.1.4", but Def 8.1.4 defines "Std-generic". This is a label typo, with no mathematical consequence (DERIVED).

## Summary

| # | Claim | Verdict |
|---|---|---|
| 1 | v4 metadata | confirmed |
| 2 | FS = classical LLC^ss (Thm A) | confirmed (finding omits the O(2n) caveat for even SO) |
| 3 | Fargues eigensheaf conj. | confirmed (supercuspidal φ) |
| 4 | strong Kottwitz | **discrepancy**: conditional on Hyp 4.5.8 except SO over Q_p; unconditional only up to reparametrization. Overstatement originates in the arXiv abstract |
| 5 | torsion vanishing | confirmed, under-qualified (proper, F≠Q, generic, O2 Std-regular) |
| V-1 | v2 non-compact fix = dropped to proper | confirmed |
| V-2 | v4 regularity swap | confirmed; toy recomputation 0 mismatches / 25 cases |
| V-3 | errata | none (inconclusive re refereed status) |

**Recommendation for the research ledger** (not written this session): supersede the internal tracking note with a version that qualifies the strong Kottwitz claim as above.
