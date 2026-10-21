#!/usr/bin/env python3
"""UPR #1057 S36: independent admissibility re-check of tuples parsed from
s36_admissible_tuples.out (separate code path from the generator).
For each prime p <= 2k (overkill; p>k is automatic) report #residues hit."""
import re, ast
txt = open("s36_admissible_tuples.out").read()
tuples = [ast.literal_eval(m) for m in re.findall(r"tuple: (\[.*\])", txt)]
def isprime(n): return n > 1 and all(n % d for d in range(2, int(n**.5)+1))
for t in tuples:
    k = len(t); assert len(set(t)) == k and t == sorted(t)
    bad = [p for p in range(2, 2*k+1) if isprime(p) and len({x % p for x in t}) == p]
    missing = {p: sorted(set(range(p)) - {x % p for x in t}) for p in (2, 3, 5, 7)}
    print(f"k={k} diameter={t[-1]-t[0]} covering_primes={bad or 'none'} ADMISSIBLE={not bad} missed_classes_small={missing}")
