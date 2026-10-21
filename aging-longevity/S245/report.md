# S245 VALIDATE -- rentosertib proteomic-clock claim

Claim under test: Zhavoronkov et al., Nature Biotechnology, Sept 2026: rentosertib reverses
proteomic age by 3-4y across 6 "independent" clocks.

Cross-reference check: DOI 10.1038/s41587-026-03286-y = "Integration of proteomic aging clocks in
a phase 2a clinical trial supports simultaneous geroprotective assessment", Nature Biotechnology,
Zhavoronkov...Gladyshev, online 2026-09-07. CONFIRMED.

## Verdicts
1. Paper exists: CONFIRMED.
2. Signal: REAL but EXPLORATORY. GENESIS-IPF NCT05938920, nested substudy n=42 (placebo 11, 30QD 11,
   30BID 11, 60QD 9), 12 wk, Olink 3072. 21/54 clock x timepoint x arm contrasts vs placebo
   significant at BH Q<0.10. Signal clusters at week 4.
3. "3-4y across 6 independent clocks": DISCREPANCY (overstated). The magnitude is peak- and
   contrast-specific, not uniform. Mortality-trained clocks (PAC, OrganAge_mortality) moved less.
   The clocks are NOT independent: shared UK Biobank training, shared Olink inputs, inter-clock r
   0.78-0.89. The cohort is IPF, so disease-activity reduction is confounded with any aging effect.

Open inconsistency found in this session: the peak arm was reported as 30mg BID in one internal
note and as 60mg QD (-2.71 to -3.46y at wk4) in another; per-arm numbers had not yet been pulled
from the primary figures. This was resolved in a follow-up session (S246, see adjacent report).

Implication: this does not work as "clinical proof of age reversal." It is proof of concept that a
clock endpoint can be run inside a trial and pick up signal. Clocks are useful as responsive
secondary endpoints, not as evidence of rejuvenation.

## Verdict
CONFIRMED (paper exists, real but exploratory signal) with DISCREPANCY (magnitude overstated;
clocks not independent; peak-arm attribution ambiguous pending S246).
