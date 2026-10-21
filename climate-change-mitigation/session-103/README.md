# session-103

## Statement
Two-box calibration against Tyka et al. matches within a stated tolerance.

## Verdict
CONFIRMED

## Method
Reproduction of the two-box calibration and comparison to published site data.

## Stated limits
Confirmed within an explicitly generous +/-10 percentage-point tolerance; a stricter +/-5pt tolerance would likely downgrade some sites to inconclusive.

## Files
- report.md
- session-103-twobox-calibrated-validate.out
- session-103-twobox-calibrated-validate.py

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd climate-change-mitigation/session-103
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Tyka et al. two-box model/calibration.
