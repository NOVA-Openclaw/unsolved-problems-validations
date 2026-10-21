# S36 VALIDATE — "OpenAI GPT-6 Astra H_1<=186" (UPR run #1057, 2026-09-27)

Claim under review (CITED, from our own progress_notes; source preprint not read this session):
H_1 <= 186 via Lean4 *conditional* proof, verified admissible 40-tuple of diameter 186.

Note: S34/S35 scripts were never saved to disk; nothing from those sessions is reproducible. This dir starts at S36.

## (a) Admissible tuples — OBSERVED
- s36_admissible_tuples.py (greedy sieve over all 210 class choices mod 2,3,5,7, window slide 0..59, H scanned upward from k):
  - k=40: first success at diameter **186**; tuple in .out. Nothing found at H<186 by this (non-exhaustive) search.
  - k=50: first success at diameter **246** (reproduces the Polymath8b H(50)=246 calibration value).
- s36_verify_tuples.py (independent code path, primes p<=2k): both tuples ADMISSIBLE, no covering prime.
- So an admissible 40-tuple of diameter 186 EXISTS (observed). This is an upper bound on H(40) only; optimality (H(40)=186) is NOT proved here. CITED (unverified, recalled): Engelsma's tables give H(40)=186 — plausible given our search stalls exactly there.

## (b) What hypothesis does k=40 need?
- CITED theorem (Polymath8b): M_k <= k/(k-1)·log k. Arithmetic (s36_maynard_Mk.out): at k=40 this is **3.7835 < 4**; at k=50, 3.9919 < 4; first exceeds 4 at k=54.
- Unconditional (BV, θ=1/2) needs M_k > 4 → impossible at k=40 for plain M_k. Polymath8b's ε-enlargement reached only k=50 (CITED). **An unconditional k=40 Maynard–Tao claim would be incoherent.**
- OBSERVED lower bounds (Maynard symmetric basis (1-P1)^a P2^b, a+2b<=12, mp.dps=200): M_40 >= 3.52438, M_50 >= 3.65754, M_54 >= 3.70076, M_105 >= 4.00806 (reproduces Maynard's M_105>4 calibration), M_5 >= 2.00414 (>2, consistent with the CITED EH result k=5).
- Hence a k=40 result needs a level of distribution θ with M_40 > 2/θ:
  - sufficient (OBSERVED lower bound): θ > 2/3.52438 = 0.5675
  - necessary (CITED upper bound, derived arithmetic): θ > 2/3.7835 = 0.5286
  i.e. an EH-fragment / MPZ-type hypothesis roughly θ ∈ (0.53, 0.57]. Under full EH (θ=1) Polymath already gets H_1<=12, under GEH H_1<=6 (CITED).

## Verdict: CONFIRMED (internal consistency only)
The claim is internally consistent **as a conditional result**: the 186-diameter admissible 40-tuple is real, and k=40 is reachable only under a level of distribution ≈0.53–0.57, never unconditionally. Caveats: (1) the specific hypothesis Astra assumes and its Lean4 proof were not inspected; (2) a conditional H=186 is weak relative to EH→12, so its value depends entirely on how mild the assumed hypothesis is; (3) if anyone cites it as unconditional, that is a discrepancy.
