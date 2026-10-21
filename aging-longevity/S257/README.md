# S257 -- VALIDATE: transcription-factor motif consensus verification

Statement under test: five hand-recalled IUPAC consensus strings for transcription factors (SRF,
Sp1, E2F, ELK1, USF) used as inputs to an internal methylation-durability screen ("MMSI") over four
aging-related gene promoters, and the resulting classification of those four loci.

Verdict: CONFIRMED WITH DISCREPANCY. Four of five consensus strings (SRF, Sp1, E2F, ELK1) verify
against real JASPAR CORE position-frequency matrices, with minor form corrections that do not
change the CpG-occupancy score at the strict threshold. One (USF1) is a discrepancy: the
pre-registered canonical CACGTG E-box describes USF2, not USF1, whose real matrix centroid is a
CpG-free CATGTG variant. The single most consequential result -- that the SRF/CArG motif can never
contain a CpG dinucleotide, which decides a downstream "PLASTIC" classification -- survives
verification against the real matrix.

Method: First-hand retrieval of JASPAR CORE position-frequency matrices via the public REST API;
independent re-derivation of IUPAC consensus strings at two information thresholds; analytic
(not brute-force) computation of obligate/possible CpG occupancy; re-scoring of the four-locus
classification under each resulting motif-occupancy scenario with every other model parameter held
frozen.

Key finding: the motif-occupancy score is not threshold-free. Moving the consensus-rendering
threshold from a stricter to a more permissive cutoff changes one locus classification and
collapses the separation margin between classes. This is reported as a genuine methodological gap,
not papered over, and a threshold-free fix is proposed for future validation but not applied here.

Limits: Single reference database (JASPAR CORE) in this session; a second database (HOCOMOCO) was
cross-checked in a related follow-up session. The weighting parameters for transcription-factor
methylation sensitivity and promoter-level drive shares remain hand-assigned estimates, unverified
by this session.

Re-run:
scripts/jaspar_verify.py fetches live data from the JASPAR CORE REST API
(https://jaspar.elixir.no/api/v1/) and requires outbound network access to that host; in this
archival environment that host was not reachable (network-restricted sandbox), so this script was
not re-executed here -- see reproduction notes. Its recorded output (scripts/jaspar_verify.out.txt)
is the original session artifact, unmodified.

scripts/mmsi_rerun.py is pure arithmetic over the values in jaspar_verify.out.txt (no network) and
was re-executed in this environment; it reproduced its original output byte-for-byte.

To re-run jaspar_verify.py in an environment with outbound network access:
  cd scripts
  python3 jaspar_verify.py > jaspar_verify.out.txt
  python3 mmsi_rerun.py > mmsi_rerun.out.txt

Upstream links:
- JASPAR CORE: https://jaspar.elixir.no/
- JASPAR REST API docs: https://jaspar.elixir.no/docs/web-services/

Files: report.md, scripts/jaspar_verify.py, scripts/jaspar_verify.out.txt,
scripts/mmsi_rerun.py, scripts/mmsi_rerun.out.txt, SHA256SUMS.
