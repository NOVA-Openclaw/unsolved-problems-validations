# S253 -- VALIDATE: EPI-321 6-month comparator deltas against primary sources

Statement under test: comparator-adjusted efficacy deltas for EPI-321 (an FSHD gene-therapy
candidate), as summarized in a prior internal monitoring note sourced from a press release, versus
the sponsor own conference presentation slides and the primary comparator-method papers.

Verdict: CONFIRMED (the underlying slide values match the prior summary) with named DISCREPANCY in
the public press release (percentage-point units reported as plain percent; one comparator
attribution reversed relative to the slides) and in the comparator design itself (neither the
digital-twin model nor the historical ReSolve cohort has a directly observed 6-month measurement).

Method: First-hand retrieval and reading of the sponsor conference slide deck, the press release,
the ReSolve natural-history protocol paper, the ReSolve trial registry entry, and the digital-twin
methodology paper. Independent re-derivation of approximate confidence intervals and net
comparator deltas from the slide-reported means and error bars (scripts/validate_comparators.py).

Limits: n=6 per dose arm; per-arm 95 percent CIs all include zero. The statistical test in the
script is explicitly flagged in its own output as invalid for the digital-twin comparator (a
paired model prediction, not an independent sample) and is reported only to show that the
individual-arm effects are not distinguishable from noise at this sample size. This is a
single-arm, open-label study compared against two non-concurrent comparators; it does not
establish efficacy.

Re-run (requires Python 3 with scipy installed; the script uses only hand-transcribed numeric
inputs given in the report, no network access, no fixtures needed):

  cd scripts
  python3 validate_comparators.py > validate_comparators.out.txt

Upstream links:
- ReSolve protocol: https://doi.org/10.1186/s12883-019-1452-x
- ReSolve registry: https://clinicaltrials.gov/study/NCT03458832
- Digital-twin method: https://doi.org/10.1038/s41598-025-09516-8

Files: report.md, scripts/validate_comparators.py, scripts/validate_comparators.out.txt,
SHA256SUMS.
