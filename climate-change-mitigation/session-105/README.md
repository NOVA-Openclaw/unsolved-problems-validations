# session-105

## Statement
Observationally-constrained two-box model explanation of observed spread.

## Verdict
PARTIAL

## Method
Reproduction of the 2-lever toy model against site observations.

## Stated limits
Overall discrepancy: the toy fails at most sites (Oman fails hardest; missing advective term) and confirms only at Brazil.

## Files
- report.md
- session-105-obs-constrained-validate.out
- session-105-obs-constrained-validate.py

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd climate-change-mitigation/session-105
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
S99/S100 IRF line; site observation datasets referenced in report.
