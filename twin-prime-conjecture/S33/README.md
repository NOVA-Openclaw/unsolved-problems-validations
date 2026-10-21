# S33

## Statement
(a) A specific admissible 40-tuple of diameter 186 exists; (b) that tuple implies H_1 <= 186 via DHL[40,2] unconditionally.

## Verdict
PARTIAL

## Method
Independent combinatorial re-verification (admissibility check) + literature cross-check against published unconditional sieve record.

## Stated limits
(a) confirmed; (b) REFUTED as unconditional -- DHL[40,2] requires GEH, would contradict Polymath8b unconditional H_1 <= 246 record.

## Files
- report.md

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd twin-prime-conjecture/S33
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Polymath8b; internal tuple listing.
