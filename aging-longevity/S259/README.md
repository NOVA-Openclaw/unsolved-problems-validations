# S259

## Statement
Transcription-factor motif consensus follow-up and promoter exploration.

## Verdict
PARTIAL

## Method
Motif verification and promoter exploration scripts.

## Stated limits
Internal pre-registration coherence discrepancy (~+0.034 prior-drift bias) separate from motif verdicts.

## Files
- S259-exploratory-egr1.out.txt
- S259-exploratory-egr1.py
- S259-exploratory-promoters.out.txt
- S259-exploratory-promoters.py
- S259-exploratory-slc25a1.out.txt
- S259-exploratory-slc25a1.py
- S259-hocomoco-nampt.out.txt
- S259-hocomoco-nampt.py
- exploratory_egr1.err.txt
- exploratory_egr1.out.txt
- exploratory_egr1.py
- exploratory_promoters.err.txt
- exploratory_promoters.out.txt
- exploratory_promoters.py
- exploratory_slc25a1.err.txt
- exploratory_slc25a1.out.txt
- exploratory_slc25a1.py
- hocomoco_nampt.err.txt
- hocomoco_nampt.out.txt
- hocomoco_nampt.py
- report.md

## Re-run instructions
See the scripts in this folder. Most checkers are plain Python 3 (>=3.8). Run:

```bash
cd aging-longevity/S259
# For Python scripts:
python3 <script.py>
# Verify checksums:
sha256sum -c SHA256SUMS
```

Some scripts depend on external data or model downloads; the per-script header notes those cases.

## Upstream sources
HOCOMOCO/JASPAR; NAMPT/EGR1/SLC25A1 promoters.
