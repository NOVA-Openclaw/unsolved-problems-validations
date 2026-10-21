#!/usr/bin/env python3
"""UPR #1057 S36 VALIDATE (Twin Prime, id=10): admissible k-tuple search.
Upper-bound search for H(k) (minimal diameter of an admissible k-tuple).
Method: for each window [0,H], exhaustively choose the deleted residue class
mod 2,3,5,7 (210 combos) and greedily delete the least-populated class for
every remaining prime p<=k; also slide window start s in [0,S). Keep the
survivors; if >=k survivors, take the k-subset of minimal diameter and verify
admissibility independently (for every prime p<=k the tuple misses a class).
Primes p>k cannot be covered by k elements, so checking p<=k suffices.
Only an UPPER bound on H(k) is produced (no exhaustive lower-bound proof).
"""
import itertools, sys

def primes_upto(n):
    s = [True]*(n+1); s[0:2] = [False, False]
    for i in range(2, int(n**0.5)+1):
        if s[i]: s[i*i::i] = [False]*len(s[i*i::i])
    return [i for i in range(n+1) if s[i]]

def admissible(t):
    k = len(t)
    for p in primes_upto(max(k, 2)):
        if len({x % p for x in t}) == p:
            return False, p
    return True, None

def best_subset(surv, k):
    surv = sorted(surv)
    best = None
    for i in range(len(surv)-k+1):
        d = surv[i+k-1]-surv[i]
        if best is None or d < best[0]:
            best = (d, surv[i:i+k])
    return best

def search(k, Hmax, starts=range(0, 60)):
    P = primes_upto(k)
    small = [p for p in P if p <= 7]
    rest = [p for p in P if p > 7]
    for H in range(k, Hmax+1, 2):
        for s in starts:
            base = list(range(s, s+H+1))
            for combo in itertools.product(*[range(p) for p in small]):
                surv = [x for x in base if all(x % p != r for p, r in zip(small, combo))]
                if len(surv) < k: continue
                for p in rest:
                    cnt = [0]*p
                    for x in surv: cnt[x % p] += 1
                    r = min(range(p), key=lambda j: cnt[j])
                    surv = [x for x in surv if x % p != r]
                    if len(surv) < k: break
                if len(surv) >= k:
                    d, t = best_subset(surv, k)
                    t0 = [x - t[0] for x in t]
                    ok, bad = admissible(t0)
                    assert ok, (t0, bad)
                    return d, t0
    return None

if __name__ == "__main__":
    for k in [int(a) for a in sys.argv[1:]] or [40, 50]:
        res = search(k, 400)
        d, t = res
        ok, _ = admissible(t)
        print(f"k={k} found admissible tuple diameter={d} admissible_check={ok} len={len(t)}")
        print("tuple:", t)
        sys.stdout.flush()
