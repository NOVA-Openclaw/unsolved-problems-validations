# S261

## Statement
Composite vs paired-disc sampling recommendation.

## Verdict
PARTIAL

## Method
Analytical error model and numerical comparison of composite vs paired-disc sampling designs.

## Stated limits
Holds only if TOS-compliant sample preparation is used; with poor preparation the recommendation reverses.

## Files
- S259_Rgrid_extension.py
- S260_cost_optimisation.py
- S261_composite_error.py
- S261_composite_error.py
- S261_gy_fse.py
- S261_gy_fse.py
- S261_gy_fse_output.txt
- S261_gy_fse_output.txt
- S261_output.txt
- S261_output.txt
- report.md

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd climate-change-mitigation/S261
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Internal S260 cost optimisation and registry sampling design documents.
