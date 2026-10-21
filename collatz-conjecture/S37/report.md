# Collatz S37 — VALIDATE: Williams "crown-triangle" L1 no-primes claim (arXiv:2607.01718)

Run #1048 (workflow 32), 2026-09-27. Mode: VALIDATE.

## 0. Objective
Validate claim: in principal skeleton L1, rows with k=a+b ≡ 2 (mod 4), k>=6, contain no primes (div-by-5 + difference-of-squares obstruction).

## 0.1 Noted gaps
- progress_notes cite a session-31-validate path that does not exist on disk (only session-37-validate exists under research/unsolved/collatz/). Not reconstructed.

## 1. Source retrieval (GUARD)
OBSERVED: abs page https://arxiv.org/abs/2607.01718 fetched 2026-09-27T04:21Z — "A Coordinate System for Collatz Dynamics", Jennifer Williams (Univ. Southampton), v1 2 Jul 2026, math.NT, "21 pages, 5 figures, under peer review".
OBSERVED: PDF https://arxiv.org/pdf/2607.01718v1 downloaded to williams-2607.01718v1.pdf, sha256 6bd835b71fea1ca70f56b1f05f880f97bfbeb843801ea96207349245a7ea5996; text extracted with pdftotext to williams.txt. Read Sections 1–4 in full (definitions, Thm 4.1 proof, Thm 4.2, Remarks 4.5–4.7).
Scout NOT dispatched: primary source retrieved directly; no new external data needed (step 2 optional in VALIDATE).

## 2. Verbatim definitions (quoted from williams.txt, pdftotext; superscripts flattened by extraction, restored in brackets)

**Map (Sec. 1):** "The Collatz function C(n) = n/2 if n ≡ 0 (mod 2), 3n + 1 if n ≡ 1 (mod 2) … We write C for this full map throughout. … Our results concern C."

**Coordinates (Sec. 1):** "every odd positive integer n can be written uniquely as n = λ · 2^a · 3^b − 1 where gcd(λ, 6) = 1, a ≥ 1, and b ≥ 0, which follows from writing n + 1 = 2^a · 3^b · λ … The parameter λ indexes which odd skeleton a nonnegative integer belongs to. The pair (a, b) gives coordinates within the odd skeleton triangle, and the sum k = a + b gives the row."

**Definition 3.1 (Odd skeleton).** "The odd skeleton Lλ consists of the odd elements of Tc where λ = (c + 2)/2. We index these elements by coordinates (a, b) where a is the exponent of 2 and b is the exponent of 3 in the factorization n + 1 = λ · 2^a · 3^b."

**Proposition 3.3 (Skeleton structure).** "The odd skeleton Lλ consists of exactly the integers Lλ = {λ · 2^a · 3^b − 1 : a ≥ 1, b ≥ 0}. The element at position (a, b) lies in row k = a + b of Tc."

**Example 3.4:** "The principal skeleton L1 consists of nonnegative integers 2^a · 3^b − 1" (table rows k=1..5: 1 | 3,5 | 7,11,17 | 15,23,35,53 | 31,47,71,107,161).

**Theorem 4.1 (Zero-Prime Rows).** "For k ≡ 2 (mod 4) with k ≥ 6, row k of the skeleton L1 contains no primes." Proof opens: "The elements of row k in L1 are {2^a · 3^b − 1 : a + b = k, a ≥ 1}."

### 2.1 Resolved interpretation (no invention needed)
- Cell value at (a,b) in L1: N(a,b) = 2^a·3^b − 1 (the integer itself; not a chain length or index).
- Row k of L1: {N(a,b) : a+b=k, a≥1, b≥0} — exactly k cells (b = 0..k−1).
- Quantifier scope: universal — for EVERY k ≡ 2 (mod 4) with k ≥ 6 and EVERY cell of row k, N(a,b) is not prime.
- Edge cases flagged by the paper itself: k=2 row {3,5} both prime (Remark 4.5), hence k ≥ 6. Note a=0 is excluded (a ≥ 1 because n odd); b=k would give 3^k − 1, even, not in L1.
- The definition is UNAMBIGUOUS for λ=1 (λ=1 coprime to 6, so n+1 = 2^a 3^b exactly, a ≥ 1). GUARD satisfied.

## 3. Independent re-derivation (DERIVED — by me, not copied from the paper's route)

Let k ≡ 2 (mod 4), k ≥ 6, a + b = k, a ≥ 1, b ≥ 0, N = 2^a 3^b − 1.

**L0 (parity split).** a + b even ⇒ a ≡ b (mod 2). So every cell is even-even or odd-odd. (b=0 ⇒ a=k even: even-even case.)

**L1 (even-even ⇒ composite).** a=2m, b=2n with m ≥ 1 (a ≥ 1 and even ⇒ a ≥ 2), m+n = k/2 ≥ 3. N = x² − 1 = (x−1)(x+1), x = 2^m 3^n ≥ 2^3 = 8 (minimum at n=0 since 3>2). So x−1 ≥ 7 > 1 and x+1 < N: proper factorization. ∎
  - Edge: at k=2, cell (2,0) gives x=2, x−1=1 → N=3 prime. So the bound matters.
  - **Minor erratum in the paper's proof text (DERIVED):** Case 1 says "For k ≥ 2, we have m + n = k/2 ≥ 1, so 2^m·3^n ≥ 2. Both factors exceed 1" — false at k=2 (x=2 ⇒ x−1=1), as the paper's own Remark 4.5 concedes ("4 − 1 = 1 × 3"). For k ≥ 6 the argument is correct since x ≥ 8. Cosmetic; does not affect Theorem 4.1.

**L2 (odd-odd ⇒ 5 | N).** Different route from the paper's case table: since 6 ≡ 1 (mod 5),
  2^a 3^b = 6^b · 2^(a−b) ≡ 2^(a−b) (mod 5) (for a ≥ b; for a < b use 2^a3^b = 6^a·3^(b−a) ≡ 3^(b−a) ≡ 2^(a−b) since 3 ≡ 2^{-1} mod 5).
  So 5 | N ⟺ 2^(a−b) ≡ 1 (mod 5) ⟺ 4 | (a − b) (ord_5(2)=4). This is an iff — sharper than the paper's one-directional table.
  With a,b odd and a+b ≡ 2 (mod 4): a − b = k − 2b ≡ 2 − 2b ≡ 2 − 2 = 0 (mod 4) since b odd ⇒ 2b ≡ 2 (mod 4). Hence 5 | N. ∎
**L3 (N > 5).** Odd-odd with k ≥ 6: N ≥ min over a+b=k, a,b≥1 of 2^a3^b − 1 ≥ 2^(k−1)·3 − 1 ≥ 95 > 5. So 5 is a proper factor. ∎
**Conclusion (DERIVED):** Theorem 4.1 holds for all k ≡ 2 (mod 4), k ≥ 6. The obstruction is correct.

**L4 (scope of 'uniqueness', Cor. 4.3 — DERIVED).** By L2's iff, for k ≡ 0 (mod 4) odd-odd cells have a−b ≡ 2 (mod 4) ⇒ 2^a3^b ≡ 4 (mod 5) ⇒ N ≡ 3 (mod 5), never divisible by 5; for k odd, cells are mixed parity. So within the paper's two obstructions the claim is right. NOTE: "unique class admitting complete algebraic obstruction" is only proved relative to {DoS, 5}; it is not a theorem that no other covering system (other moduli / Aurifeuillean-type factorizations) could kill rows in another class. Empirical check in §4 (primes exist in other classes' rows) supports it at the tested range but is not proof.

## 4. Computational verification (OBSERVED — I ran it)

Script: verify_williams_crown.py (sha256 d795bf16d5b654d9b4ec2db7d471b7aee851a3fc46733baefb5c708e19612fa8)
Run: `.venv/bin/python verify_williams_crown.py 4002 302 80` → verify_output.txt (sha256 897fd517f0cb368da51b9d2d90646780605b4e06fbdc4c5ff11b98390404fef0), 25.3 s, rc=0. sympy 1.14.0 isprime (BPSW).

- **[A] Certificate, exhaustive:** all 1000 target rows k = 6, 10, …, 4002; 2,004,000 cells. Every cell carried an explicit verified divisor 1<d<N: 1,002,000 via DoS (d = 2^(a/2)3^(b/2) − 1), 1,002,000 via 5. Uncovered cells: 0. No mixed-parity cells in target rows.
- **[B] Blind primality (obstruction not used):** all 75 target rows k=6..302, 11,550 cells (numbers up to ~480 bits): 0 primes.
- **[C] Liveness control:** L1 non-target rows k ≤ 80 with ≥1 prime: 59/60 — the only prime-free one is k=1 (row {1}; 1 is not prime). So the primality test is not vacuous. k=2 row = [3,5], both prime (matches Remark 4.5). In k≡0 (mod 4) rows, zero primes ever landed on DoS (even-even) cells — consistent with Thm 4.2(c).
- **[D] Figure 3 (right panel) reproduced exactly:** prime counts for 11 λ × rows k=2,6,…,38 — 0/11 λ rows mismatch (110/110 cells equal).
- **[E] Remark 4.7 spot-checks:** λ=49 (square, ≡4 mod 5): rows k≡0 (mod 4), k=4..80: all 0 primes ✔. λ=121 (square, ≡1 mod 5): rows k≡2 (mod 4), k=2..78: all 0 primes ✔ (k=2 included: 483 = 3·7·23 (DoS, 11·2−1=21 | 483), 725 = 5²·29). Control λ=49 rows k≡2 (mod 4): primes present (e.g. k=22: 5) ✔.
- **[F] Converse (my L2 iff):** 45,150 odd-odd cells k ≤ 600: 5 | N ⟺ a ≡ b (mod 4), 0 violations.

Earlier smoke run (k≤202/70/40) gave identical conclusions (not saved separately).

## 5. Outcome: **CONFIRMED** (with one cosmetic erratum)

- Theorem 4.1 (Williams, arXiv:2607.01718v1): **CONFIRMED** — proof independently re-derived (DERIVED, §3, via the 6≡1 (mod 5) reduction giving an iff), exhaustively certified for every cell of every target row k ≤ 4002 and blind-tested prime-free for k ≤ 302 (OBSERVED, §4).
- Theorem 4.2 / Cor 4.3: correct *relative to the two stated obstructions*; "unique class admitting complete algebraic obstruction" is not a claim about arbitrary covering systems (DERIVED caveat, §3 L4).
- Remark 4.7 generalization: spot-checks consistent (λ=49, λ=121).
- Figure 3 data: reproduced exactly.
- **Erratum (cosmetic, DERIVED):** Thm 4.1 Case 1 text "For k ≥ 2 … 2^m·3^n ≥ 2. Both factors exceed 1" is false at k=2 (x−1 = 1). Harmless under the stated k ≥ 6 hypothesis (then x ≥ 8); the paper's Remark 4.5 already acknowledges the k=2 behaviour. Not a discrepancy in the theorem.
- Context: this result is elementary number theory on {2^a3^b − 1} (Pierpont 2nd-kind family) and is independent of the Collatz conjecture — the paper says so itself. It gives no leverage on Collatz convergence. Low value as an ENGAGE target (erratum is too minor to warrant contacting the author beyond, at most, a one-line note).

## 6. Artifacts
- S37-validate-williams-crown.md (this file)
- williams-2607.01718v1.pdf (sha256 6bd835b71fea1ca70f56b1f05f880f97bfbeb843801ea96207349245a7ea5996), williams.txt (sha256 c25d84109613bcf8e7312c5ab81bf671bf063e1aad00127821be86db71757d67)
- verify_williams_crown.py, verify_output.txt (hashes in §4)
