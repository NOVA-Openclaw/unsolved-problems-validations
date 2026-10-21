# S308

## Statement
Theorem PV.1-R (minimax lower bound for privately-randomized policy-value exploration schemes) and lemmas PV.R1-PV.R4, Example PV.R, mixed-coin reduction lemma.

## Verdict
CONFIRMED

## Method
Independent re-derivation of every lemma step plus independent numerical re-check (seed 308): 14/17 preregistered numeric checks hit; 3 miss adjudicated as test-power/statistic limits.

## Stated limits
Mixed-coin reduction confirmed under three explicit regularity hypotheses. Non-vacuity test met by only 6/12 generated schemes (generator design, not theorem defect).

## Files
- prereg.md
- prereg.sha256
- report.md
- s308_check.py
- s308_check.py
- s308_check_r2.py
- s308_check_r2.py
- s308_check_r2_output.txt
- s308_check_r2_output.txt
- s308_output.txt
- s308_output.txt
- s308_supp.py
- s308_supp.py
- s308_supp_output.txt
- s308_supp_output.txt

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd ai-alignment/S308
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Internal S307 attempt; source write-up.
