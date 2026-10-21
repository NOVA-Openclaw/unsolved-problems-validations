# session-100

## Statement
Single-model IRF linear-convolution error bound.

## Verdict
CONFIRMED

## Method
Re-derivation of the linear time-invariant convolution error bound and numerical cross-check.

## Stated limits
Single-model forecast-gap diagnosis; not a full climate forecast validation.

## Files
- report.md
- session-100-irf-lti-error-harness.py

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd climate-change-mitigation/session-100
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
S96/S99 internal IRF analysis; Tyka et al. two-box calibration conventions.
