# S38-validate-comet

## Statement
S36/S37 numeric predictions (coefficient-of-variation study).

## Verdict
PARTIAL

## Method
Independent recomputation with same/corrected code + hand verification of arithmetic identities.

## Stated limits
Numeric reproductions confirmed exactly; interpretation discrepancies: 'normalized variance' misnomer, CoV floor does not exist, q=7 'Poisson peak' entirely an off-by-one bug artifact (REFUTED).

## Files
- report.md
- s38_comet.out
- s38_comet.py
- s38_scaling_and_cheb.out
- s38_scaling_and_cheb.py

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd goldbach-conjecture/S38
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Internal S35-S37 numeric scripts.
