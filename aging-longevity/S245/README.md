# S245 -- VALIDATE: rentosertib proteomic-clock claim, plus pre-readout registry monitor

Statement under test: rentosertib reverses proteomic age by "3-4 years" across "6 independent
clocks" (Zhavoronkov et al., Nature Biotechnology, Sept 2026, DOI 10.1038/s41587-026-03286-y;
GENESIS-IPF trial NCT05938920).

Verdict: CONFIRMED that the paper exists and the trial produced a real exploratory signal, with
DISCREPANCY on the headline "3-4 years across 6 independent clocks" framing (overstated magnitude;
clocks are correlated, not independent).

Method: Independent re-check against the publisher DOI record; recomputation of the
significant-contrast fraction (21/54 clock x timepoint x arm contrasts significant at BH Q<0.10);
cross-check of inter-clock correlation structure (shared Olink panel, shared UK Biobank training,
r 0.78-0.89).

Companion file: monitor.md is a separate, lighter-weight registry-monitoring pass run in the
same work session, re-checking public ClinicalTrials.gov status for several related trials ahead of
a conference data readout, and correcting one over-claim about the Phase 3 trial endpoints.

Limits: Literature/registry audit only; no new patient-level data were analyzed. The
peak-dose-arm attribution for the "3-4 years" figure was still ambiguous at the end of this session
and was resolved in the follow-up validation (session S246, included separately in this repository).

Re-run: Document review -- retrieve the paper at the DOI below and the trial registries via the
ClinicalTrials.gov API, and compare reported statistics/timing against any summary claim being
checked.

Upstream links:
- Paper: https://doi.org/10.1038/s41587-026-03286-y
- GENESIS-IPF trial: https://clinicaltrials.gov/study/NCT05938920
- GENESIS-IPF-3 (Phase 3): https://clinicaltrials.gov/study/NCT07687459
- ClinicalTrials.gov API v2: https://clinicaltrials.gov/data-api/api

Files: report.md (clock-claim validation), monitor.md (registry monitor), SHA256SUMS.
