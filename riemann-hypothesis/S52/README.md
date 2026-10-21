# S52

## Statement
Theorem E (lemmas L0-L5), Theorem E' (L6 construction), numeric thresholds 0.261286 and 0.255431 (20 digits), L7 optimal-within-L6-scheme claim.

## Verdict
CONFIRMED

## Method
Independent re-derivation from source TeX + Lean docstring cross-check + exact/high-precision numerics + brute-force grid search.

## Stated limits
L7 confirmed numerically only, not analytically. Conditional construction within the researchers' own program; not a resolution of RH.

## Files
- S52_S0_predictions.md
- report.md
- s52_algebra.out
- s52_algebra.py
- s52_lp_skipped.out
- s52_lp_skipped.py
- s52_lp_stress.out
- s52_lp_stress.py
- s52_thresholds.out
- s52_thresholds.py

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd riemann-hypothesis/S52
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Internal Theorem E/E' write-up; source TeX; mpmath.
