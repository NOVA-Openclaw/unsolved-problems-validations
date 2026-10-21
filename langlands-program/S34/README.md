# validate-2026-09-07-s34-audit — Langlands Program

**Problem:** Langlands Program (NOVA unsolved-problems tracking, mathematics category).
**Mode:** VALIDATE — citation and claim audit of six internal tracking entries against the live
arXiv API (primary source), plus an independent re-derivation of one negative claim.
**Verdict:** CONFIRMED with one discrepancy. 6/6 citations real and correctly attributed; 5/6
substantive claims accurate; 1/6 (Koziol) misstates the paper's hypothesis in a way that overstates
its scope. The load-bearing negative claim ("no key-actor movement" in a tracked research area) is
independently reproduced and extended.

## Statement under test

Six prior internal tracking entries, each summarizing one arXiv preprint (listed by arXiv ID in
the table below), plus a separate negative claim that none of ten tracked researchers in this
sub-field had posted anything new during a specific date window.

## Method

- Queried `https://export.arxiv.org/api/query` (Atom feed), one request per arXiv ID, for each of
  the six cited papers; raw XML saved alongside parsed title/author/date/abstract output.
- Independently re-ran an author-name scan across the same API for ten tracked researchers, over
  two date windows (the original claim window, and a follow-on gap window never previously
  checked).
- Scripts: `scripts/fetch.py` (per-paper metadata check), `scripts/actors.py` (author-window scan).
  Raw evidence: `outputs/raw-*.xml`, `outputs/verify-output.txt`, `outputs/actor-scan.txt`,
  `outputs/yujie-xu-hit.txt`.

### Instrument failure caught during the original run (recorded for anyone re-running this)

The first attempt used a bare HTTP request to `export.arxiv.org` on port 80, which 301-redirects to
HTTPS; a tool that doesn't follow redirects (e.g. a naive `curl` without `-L`) silently writes a
0-byte response and exits 0. If that empty output were parsed without checking for emptiness, it
would read as "no results found" — a plausible-looking false negative. The fix (used here) is to
query `https://export.arxiv.org/...` directly over `urllib`, which returns real entries.

## Verdicts (summary)

| arXiv ID | Verdict |
|---|---|
| 2608.20225v1 (Luo–Stevens) | CONFIRMED — abstract matches verbatim |
| 2608.20125v1 (Lang–Müller–Palvannan) | CONFIRMED — levels, congruence conditions, and the isomorphism claim match exactly |
| 2608.19570v1 (Koziol) | **DISCREPANCY (hypothesis error).** The tracking entry drops the paper's "residue field is a proper extension of F_p" condition — i.e. it silently drops the requirement F != Q_p, which is exactly the excluded base case that motivates the paper's own counterexample framing. The finding overstates the theorem's scope to include the one case the paper explicitly does not cover. |
| 2608.19129v1 (Hegde) | CONFIRMED — matches, with two minor attribution/qualifier omissions noted |
| 2608.13869v2 (Shun Xu) | CONFIRMED — in-window version date and theorem content both match |
| 2606.10149v2 (Helm–Solleveld–Xu) | CONFIRMED — unchanged since the prior check (still v2, same update date), as claimed |
| Negative claim: no movement from 10 tracked researchers in the original window | **CONFIRMED by independent re-derivation** — total=0 for all ten in a fresh author-window scan. Extended with a bonus scan of the 15 days since the original check: also 0 for nine of ten; one apparent hit resolved to a different person with a similar surname (false positive, documented and discarded). |

Full per-claim reasoning is in `report.md`.

## Limits

- This is a citation/claim audit of third-party preprints and of this project's own internal
  tracking notes, not an original mathematical contribution.
- The author-window scan relies on arXiv's own search index and simple surname matching, which is
  known to produce false positives (documented explicitly for one case here); it is not a fully
  disambiguated author-identity match.
- Both scripts depend on live network access to `export.arxiv.org`; they cannot be re-run in a
  network-isolated environment (see "Reproduction status" below).

## Upstream sources

- David C. Luo, Shaun Stevens, [arXiv:2608.20225v1](https://arxiv.org/abs/2608.20225v1)
- Jaclyn Lang, Katharina Müller, Bharathwaj Palvannan, [arXiv:2608.20125v1](https://arxiv.org/abs/2608.20125v1)
- Karol Koziol, [arXiv:2608.19570v1](https://arxiv.org/abs/2608.19570v1)
- Devadatta G. Hegde, [arXiv:2608.19129v1](https://arxiv.org/abs/2608.19129v1)
- Shun Xu, [arXiv:2608.13869v2](https://arxiv.org/abs/2608.13869v2)
- David Helm, Maarten Solleveld, Yujie Xu, [arXiv:2606.10149v2](https://arxiv.org/abs/2606.10149v2)

## Re-running this check

```sh
cd scripts
python3 fetch.py      # re-queries the six cited papers; writes raw-*.xml + prints the same report
python3 actors.py     # re-runs the two-window author scan; prints the same actor-scan report
```

Both scripts use only Python's standard library (urllib, xml.etree.ElementTree) and require
live outbound network access to https://export.arxiv.org. No credentials, API keys, or fixtures
are needed — the arXiv API is public and unauthenticated. Expected output matches
`outputs/verify-output.txt` and `outputs/actor-scan.txt` (the historical date windows are fixed
calendar dates, so a re-run should query the same historical period and return the same results).

## Reproduction status

**NA (network-dependent, not re-run in this environment).** This validation's checker scripts query
the live arXiv API over HTTPS. The sandbox used to prepare this artifact has no outbound network
access, so the scripts could not be executed here to re-confirm the API responses byte-for-byte.
The scripts are plain, auditable standard-library Python with no external dependencies; the recorded
raw XML responses (`outputs/raw-*.xml`) are the original evidence and are included unmodified. Code
review confirms the scripts' logic matches what is described in `report.md` and would reproduce the
historical date-windowed query if network access were available.
