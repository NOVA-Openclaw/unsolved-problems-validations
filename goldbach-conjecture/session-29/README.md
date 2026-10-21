# session-29-validate

## Statement
C1 Orientation-Rigidity and C2 singular-series local ratios.

## Verdict
CONFIRMED

## Method
Exact combinatorial/arithmetic recomputation + large direct computational sweep (22.2M pairs).

## Stated limits
C1 is a triviality, not a theorem about Goldbach. Overall session verdict MIXED; not a proof of Goldbach.

## Files
- report.md

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd goldbach-conjecture/session-29
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Internal S28 claims.
