# S37

## Statement
Theorem 4.1 of Williams preprint (structural 'crown' result tied to residues mod 5).

## Verdict
CONFIRMED

## Method
Independent proof re-derivation + exhaustive computational certification for every cell of every target row k <= 4002 plus blind prime-free test k <= 302.

## Stated limits
Confirms an external preprint's specific theorem; not a resolution of the Collatz conjecture.

## Files
- report.md
- verify_output.txt
- verify_williams_crown.py

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd collatz-conjecture/S37
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Williams, arXiv:2607.01718v1.
