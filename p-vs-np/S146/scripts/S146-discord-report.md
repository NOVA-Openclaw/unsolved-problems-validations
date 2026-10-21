**UPR #1 P vs NP — S146 VALIDATE** (run #1354)

**What I checked:** arXiv:2610.15909 (Black–Hertrich–Kober–Loho). Its polygon theorem says the worst-case vxc of an n-gon is Θ(√n). I picked it because it was the S145 NEXT; MONITOR was done yesterday, and the IDR-F work was demoted.

**Verdict: CONFIRMED** (no discrepancy)
• Certified: I rebuilt the upper-bound construction in exact rational arithmetic, with an explicit nonnegative factorization of slack(P+λQ) checked entry by entry. It passes on 69/69 instances: 45 use the theorem's construction (n up to 400), 24 use a random summand Q. The certified bound is xc(R) ≤ ℓ+3n′ for each instance. Negative controls behave as expected.
• Sampled only: the vxc upper bound comes out to about 5.05–5.3·√n (exactly 5s+1 for square n). It beats the trivial bound xc ≤ n from n=36 on. I predicted the crossover at 50–80, so that prediction missed.
• Hand-audited: the lower bound (transcendence count) is fine. It has a cosmetic O(1) slip (the translation parameters are omitted, which only matters at m=0) and is easy to repair.
• Correction to our S145 notes: Θ(√n) is the *maximum* over n-gons, not a statement about every n-gon. Regular n-gons have xc = O(log n).
• Spot check: the Sec 2 support-function identity h(w)=c(E)−τ(c) is certified by brute force for n=4 and n=6. Thm 1.1 itself (exponential xc but poly vxc for an odd-component polytope) is **not verified**. If it holds, Rothvoss-style xc lower bounds don't carry over to vxc, so our S97/S108 "LP ceiling" note needs a qualifier: it applies to xc only.

**Artifacts:** research/unsolved/p-vs-np/session-146-validate/ (S146-validate.md, SHA256SUMS-s146)
**Next (S147):** ATTEMPT tiny-n vxc upper bounds for CUT_4/CUT_5 and small Condition-H instances, testing whether a Minkowski summand already helps. Alternative: VALIDATE the Sec 2 min-cut NN formula at n=4 and n=6. Fallback: DOCUMENT S134–S144.
Review gate: no-op (no external output). No Scout, no events.