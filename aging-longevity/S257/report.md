# S257 -- VALIDATE: motif consensus verification against JASPAR CORE

## 0. Objective
Independently verify five pre-registered motif consensus strings (for an internal "MMSI" durability
screen covering four aging-related promoter loci) against a primary motif database (JASPAR CORE
vertebrates), recompute the m_t (motif CpG occupancy) column from the verified matrices, and re-run
the screen with every other input frozen. Primary falsifier under test (PF3): if a verified CArG/SRE
consensus admits an obligate or common CpG, the SRF m=0 result dies and the EGR1 PLASTIC verdict
reverts to depending on an unverified sensitivity parameter.

Only the m column was permitted to change. The sensitivity weights, drive-share weights, the
0.60/0.30 thresholds and the R>=0.50 override are frozen exactly as pre-registered, per a strict
no-retuning clause.

## 1. Method
- Source: JASPAR CORE (jaspar.elixir.no REST API v1), latest version of each base matrix, fetched
  first-hand. Matrices used: SRF MA0083.3, SP1 MA0079.5, USF1 MA0093.4, USF2 MA0526.5, E2F1 MA0024.3,
  E2F4 MA0470.3, ELK1 MA0028.3.
- Each PFM column was converted to an allowed-letter set at two information thresholds
  (per-position frequency >= 0.25 "permissive", >= 0.40 "strict"), rendered back to an IUPAC string,
  and flanking fully-degenerate (N) columns trimmed.
- CpG occupancy computed analytically from the per-position letter sets -- obligate CpG at position
  i iff the set at i is exactly {C} and the set at i+1 is exactly {G}; possible CpG iff C is in the
  set at i and G is in the set at i+1. (Exhaustive IUPAC expansion is intractable at 16 columns with
  N; the analytic rule is exactly equivalent and reproduces all five pre-registered m values on the
  pre-registered strings.)
- m = 1.0 obligate / 0.5 possible-not-obligate / 0.0 impossible.
- Scripts: scripts/jaspar_verify.py (fetches JASPAR, computes verified consensus strings and m) and
  scripts/mmsi_rerun.py (re-scores the four loci under each m scenario, pure arithmetic, no network).

## 2. Retrieved matrices vs pre-registered strings

| TF | Pre-registered | JASPAR matrix | verified consensus (t=0.40) | verified consensus (t=0.25) |
|---|---|---|---|---|
| SRF | CCWWWWWWGG | MA0083.3 | TGACCATATATGGTCA | TGMCCATATAWGGKCA |
| Sp1 | GGGGCGGGG | MA0079.5 | GGGGCGGGG | GGGGMGGRG |
| USF (E-box) | CACGTG | MA0093.4 (USF1) | GTCATGTGAC | GTCATGTGAC |
| USF (E-box) | CACGTG | MA0526.5 (USF2) | GTCACGTGAC | RTCACGTGAY |
| E2F | TTTSSCGC | MA0024.3 / MA0470.3 | TTTGGCGCCAAA / TTTTGGCGCCATT | TTTGGCGCCAAA / WTTTGGCGCCAWW |
| ELK1 | SCGGAAGY | MA0028.3 | ACCGGAAGT | ACCGGAAGT |

### Verdicts on the five strings
1. SRF -- CONFIRMED in substance, CORRECTED in form. The pre-registered CCWWWWWWGG is the textbook
   10-mer CArG box; MA0083.3 is a 16-mer palindrome whose core is CCATATATGG -- the same
   CC-(AT-rich 6)-GG architecture. Neither rendering admits a CpG at any threshold.
2. Sp1 -- CONFIRMED at strict threshold, DEGRADED at permissive. GGGGCGGGG is reproduced exactly at
   t=0.40. At t=0.25 position 5 becomes M (A/C) and position 8 becomes R (A/G), so CpG is possible
   but not obligate -> m drops 1.0 -> 0.5.
3. E2F -- CONFIRMED and strengthened. Real matrices are the 12-mer TTTGGCGCCAAA palindrome; obligate
   CpG at both thresholds, both family members. m=1.0 holds.
4. ELK1 -- CONFIRMED. ACCGGAAGT vs pre-registered SCGGAAGY: same CGGAAG ETS core, obligate CpG.
   m=1.0 holds.
5. USF / E-box -- DISCREPANCY (the one real hit). USF2 (MA0526.5) contains the canonical CACGTG
   E-box as expected -> m=1.0. But USF1 (MA0093.4) renders as GTCATGTGAC, a CATGTG-variant E-box
   with NO CpG at all -> m=0.0. The pre-registered CACGTG is correct for the canonical site but is
   not what the USF1 PFM centroid gives.

## 3. Re-scoring re-run (verified m, everything else frozen)

| scenario | NAMPT | EZH2 | SLC25A1 | EGR1 | all 4 reproduce baseline? | gap |
|---|---|---|---|---|---|---|
| pre-registered strings (baseline) | 0.7600 HR | 0.7575 HR | 0.6800 HR | 0.1250 PL | yes | 0.5550 |
| JASPAR t=0.40 strict | 0.7600 HR | 0.7575 HR | 0.6800 HR | 0.1250 PL | yes | 0.5550 |
| JASPAR t=0.25 permissive | 0.7600 HR | 0.6975 HR | 0.3400 PL | 0.1250 PL | no (SLC25A1 flips) | 0.2150 |
| t=0.25 + USF1-only E-box | 0.0000 PL | 0.6975 HR | 0.3400 PL | 0.1250 PL | no (2 flips) | 0.1250 |

HR = HIT-AND-RUN, PL = PLASTIC (both EGR1 and the flipped loci go PLASTIC via the R>=0.50 override).

## 4. Verdict

PF3: NOT TRIGGERED -- the load-bearing result survives. The verified SRF matrix MA0083.3 admits
zero CpG, obligate or possible, at both thresholds. m_SRF = 0.0 stands against a real PFM, so the
EGR1 PLASTIC classification remains independent of the contested SRF-sensitivity parameter.

Overall outcome: CONFIRMED WITH DISCREPANCY. Four of five strings verify (SRF, Sp1, E2F, ELK1 --
with form corrections that do not change m at strict threshold). One discrepancy (USF1 E-box) and
one newly exposed methodological fragility (threshold dependence) are recorded. Under the
strict-consensus reading, all four baseline verdicts reproduce exactly, with identical values to
four decimal places.

New finding -- the m column is not as objective as claimed. m is a property of the alphabet given a
consensus string, but the consensus string is itself a thresholding choice over a PFM. Moving the
rendering threshold from 0.40 to 0.25 -- a defensible choice either way -- flips SLC25A1 from
HIT-AND-RUN to PLASTIC and destroys the gap. The claimed objectivity of m silently imports an
undeclared free parameter. This is a genuine, self-inflicted methodological gap that must be fixed
before any prospective (blind) application, otherwise the first prospective call is
threshold-shoppable after the fact.

Proposed fix (not applied this session, requires pre-registration in a follow-up): replace the
0/0.5/1 m ladder with a PFM-derived continuous quantity -- expected CpG occupancy computed directly
from the matrix's own position-wise nucleotide distribution, threshold-free, reducing to ~1 for
obligate-CpG motifs and exactly 0 for SRF.

## 5. Honesty / limitations
- Single database (JASPAR CORE) used this session. HOCOMOCO was not consulted here; that
  cross-check was performed in a later session (S259, included separately in this repository).
- The consensus-rendering procedure (threshold over column frequencies, N-trimming) is this
  session own method, not JASPAR's; JASPAR does not publish an official IUPAC consensus.
- The sensitivity-weight and drive-share values remain pre-registered estimates and UNVERIFIED by
  this session; this session does nothing to repair that.
- No prospective application of the screen was made this session. Doing so before fixing the m
  threshold ambiguity would have burned a blind test on a method with a known free parameter.
- No external publication of any kind.
