# S36

## Statement
Internal 'astra-186' construction consistency.

## Verdict
CONFIRMED

## Method
Self-consistency verification of the construction.

## Stated limits
Internal consistency only, not an external/independent confirmation of a new prime-gap record.

## Files
- report.md
- s36_admissible_tuples.out
- s36_admissible_tuples.py
- s36_maynard_Mk.out
- s36_maynard_Mk.py
- s36_verify_tuples.out
- s36_verify_tuples.py

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd twin-prime-conjecture/S36
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Internal S36 construction; Maynard sieve code.
