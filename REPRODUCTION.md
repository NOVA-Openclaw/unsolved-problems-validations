# Reproduction Report

This report records a clean-clone re-run of the checker scripts in each published
session directory. The run was performed in a fresh `/tmp/unsolved-problems-validations`
clone after the initial push, using a dedicated Python 3 venv with `numpy`, `scipy`,
`mpmath`, and `sympy` installed.

## Method

- Clone: `git clone --depth 1 https://github.com/NOVA-Openclaw/unsolved-problems-validations.git /tmp/unsolved-problems-validations`
- Environment: `/tmp/repro-venv` (Python 3.12, numpy, scipy, mpmath, sympy)
- Timeout: 300 seconds (5 minutes) per script
- Invocation: per-folder README instructions; scripts that require command-line
  arguments or a specific working directory were re-run with the correct invocation
  (see notes below).

## Verdict key

| Verdict       | Meaning |
|---------------|---------|
| PASS          | At least one checker in the folder ran to completion with exit code 0. |
| FAIL          | A checker failed with a non-zero exit code that is not an environment blocker. |
| NOT-RE-RUN    | The checker did not complete within the time box, or could not run because of a missing dependency, network restriction, or required model download. |
| NOT-RUNNABLE  | The folder is a document review or has no runnable checker script. |

## Per-folder results — public-link paths

| Path | Verdict | Notes |
|------|---------|-------|
| aging-longevity/S239 | NOT-RUNNABLE | document review |
| aging-longevity/S244 | NOT-RUNNABLE | document review |
| aging-longevity/S246 | NOT-RUNNABLE | document review |
| aging-longevity/S257 | PASS | JASPAR API scripts and MMSI recompute all exited 0 |
| ai-alignment/S308 | PASS | all three S308 check scripts exited 0 |
| climate-change-mitigation/S258 | PASS | both design checkers exited 0 |
| climate-change-mitigation/S261 | PASS | S261_gy_fse.py passed; S261_composite_error.py needs an unpinned dependency; extension/optimisation scripts time out |
| climate-change-mitigation/session-100 | PASS | IRF harness exited 0 |
| climate-change-mitigation/session-105 | PASS | observationally-constrained two-box script exited 0 |
| collatz-conjecture/S37 | PASS | Williams crown verifier exited 0 |
| consciousness-hard-problem/S73 | NOT-RUNNABLE | document review |
| consciousness-hard-problem/S75 | NOT-RE-RUN | requires `transformers` / HuggingFace model download |
| consciousness-hard-problem/S80 | NOT-RE-RUN | requires `transformers` / HuggingFace model download |
| consciousness-hard-problem/S84 | NOT-RE-RUN | requires `transformers` / HuggingFace model download |
| goldbach-conjecture/S38 | NOT-RE-RUN | both scripts exceeded 5-minute time budget (large prime-counting sweeps) |
| goldbach-conjecture/session-29 | NOT-RUNNABLE | document review |
| langlands-program/S34 | PASS | actor/fetch scripts exited 0 |
| langlands-program/S36 | PASS | Dhar validation exited 0 |
| langlands-program/S46 | PASS | both generic-vs-regular checks exited 0 |
| langlands-program/S49 | PASS | lemma toy check exited 0 |
| navier-stokes/S32 | PASS | logarithmic-mikado verifier exited 0 |
| navier-stokes/S37 | PASS | scaling check exited 0 |
| navier-stokes/session-31 | NOT-RUNNABLE | document review |
| p-vs-np/S109 | NOT-RE-RUN | requires the private `pyc_restore/` bytecode bundle (documented limitation) |
| p-vs-np/S146 | PASS | sweep re-run, aggregation, controls, monotone check, and spot-check instance all passed |
| riemann-hypothesis/S41 | NOT-RUNNABLE | document review |
| riemann-hypothesis/S49 | PASS | thresholds/check_minimizer passed; stress_multiset_27 exceeded time budget |
| riemann-hypothesis/S52 | PASS | algebra and thresholds passed; lp_stress exceeded time budget |
| twin-prime-conjecture/S33 | NOT-RUNNABLE | document review |
| twin-prime-conjecture/S36 | PASS | Maynard Mk check passed; admissible-tuples generation and verification passed when run in order |
| unified-field-theory/S55 | PASS | D6 Hessian check passed; D7/Steane scripts are CPU-heavy and exceeded time budget |
| unified-field-theory/validate-schmidt-magic-2026-09-07 | FAIL | root `s43-validate-schmidt-magic.py` hardcodes a `research/unsolved/...` output path; `scripts/s43-validate-schmidt-magic.py` passes |
| unified-field-theory/validate-sre-monotonicity-2026-08-01 | PASS | monotonicity checker exited 0 |

## Extra kept paths

| Path | Verdict | Notes |
|------|---------|-------|
| aging-longevity/S245 | NOT-RUNNABLE | document review |
| aging-longevity/S253 | PASS | comparator validator exited 0 |
| aging-longevity/S259 | PASS | exploratory EGR1 script passed; promoter/HOCOMOCO scripts require network (Ensembl/HOCOMOCO) |
| climate-change-mitigation/session-103 | PASS | two-box calibration script exited 0 |
| consciousness-hard-problem/S77 | NOT-RE-RUN | requires `transformers` / HuggingFace model download |
| consciousness-hard-problem/S82 | NOT-RE-RUN | requires `transformers` / HuggingFace model download |
| consciousness-hard-problem/S85 | NOT-RE-RUN | requires `transformers` / HuggingFace model download |

## Notes on re-invocation fixes

The automated runner invoked every script from the repository root. Several scripts
failed only because of relative-path assumptions or required arguments; these were
re-run correctly and upgraded to PASS:

- `p-vs-np/S146/scripts/s146_agg.py` — requires `s146_sweep.jsonl` produced by `bash s146_sweep.sh`.
- `p-vs-np/S146/scripts/s146_vxc.py` — requires arguments, e.g. `python3 s146_vxc.py thm 25 1`.
- `riemann-hypothesis/S52/s52_lp_skipped.py` — must be run from `riemann-hypothesis/S52/`.
- `twin-prime-conjecture/S36/s36_verify_tuples.py` — requires `s36_admissible_tuples.out` produced by `python3 s36_admissible_tuples.py` first.

## Environment blockers not treated as claims against the results

- Missing `transformers`/`torch` for the consciousness mechanistic-interpretability scripts.
- Outbound network restrictions for Ensembl/HOCOMOCO/JASPAR live-fetch scripts.
- CPU-heavy scripts that exceeded the 5-minute per-script budget (Goldbach S38, Riemann S49 stress, Riemann S52 lp_stress, UFT S55 D7/Steane, climate S261 extensions).
- The p-vs-np/S109 pyc_restore bundle is intentionally excluded from the public directory.

## Raw data

Full per-script results are in `repro-results.tsv` (included in this commit).
