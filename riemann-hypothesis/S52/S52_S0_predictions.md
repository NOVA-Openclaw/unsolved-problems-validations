# S52 §0 frozen predictions (written 2026-09-30 ~17:23 UTC, after reading S51.md only; before reading Lamzouri text or computing anything)

Q-P1. Weakest lemma: L7 (and by extension Theorem E'). Reason: it is the only lemma making an
      optimisation/"optimal" claim with case splits and derivative-sign arguments (region t>=2+sqrt2 vs
      t<=2+sqrt2, formula for c = max(...)), and S51 already corrected one derivative bound on re-check.
      Most likely failure: a sign/region slip or an unjustified "optimal" claim; the (4-A)/A bound itself I
      expect to SURVIVE because it is a direct instance of L6 with feasible (t,b2,b3).
Q-P2. Second-weakest: L0 (A>=1 automatic via Remark 2.2 / (2.4)). Reason: it depends on how Lamzouri
      normalises K (K(0)=1? diagonal terms counted with multiplicity?) — a normalisation mismatch would
      change "A>=1" but NOT break E, since only A>=0 is used and Sum K^2 >= 0 trivially... unless K can be
      negative-weighted (it cannot: it is a sum of squares).
Q-P3. The A-free lemmas (2.12)-(2.21) will be confirmed A-free; the hypothesis A<2 appears only in the
      statement of Prop 2.1 (and in the AxiomProver appendix statement), not in any parameter choice.
Q-P4. L2-L5 CONFIRMED, exact algebra (t=2+sqrt2, b1=5/2+sqrt2-A, q-cancellation) reproduces.
Q-P5. Fresh numerics: 0 violations of E and E' in the abstract linear-program model; boundary cases
      A=2+sqrt2 give equality of the two constants 3-2sqrt2 to >=30 digits.
Q-P6. Thresholds recompute: 0.261286429995 and 0.255431158928 to >=10 digits — IF the C_theta formula
      from S49 is taken as given. Risk: I may find the downstream application (Wang) needs something
      beyond (2.7) (e.g. a hypothesis on A tied to lambda), making the threshold claim INCONCLUSIVE.
