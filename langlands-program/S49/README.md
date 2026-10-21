# S49-validate-fu

## Statement
Fu et al. literature claim.

## Verdict
CONFIRMED

## Method
Primary-source comparison.

## Stated limits
Scope corrections: paper itself has no discrepancy; internal finding/summary was under-scoped.

## Files
- abs.html
- cf26-arxiv-api.xml
- report.md
- s49_lemma521_toy.out
- s49_lemma521_toy.py

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd langlands-program/S49
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
Fu et al. arXiv:2610.16445v1.
