#!/usr/bin/env python3
"""S37 VALIDATE — Williams arXiv:2607.01718 Theorem 4.1 (Zero-Prime Rows in L1).

Definition (Prop 3.3 / Ex 3.4 / Thm 4.1 proof): row k of L_lambda is
  { lambda * 2^a * 3^b - 1 : a + b = k, a >= 1, b >= 0 }   (k cells, b = 0..k-1)
Claim: for lambda = 1, every k = 2 (mod 4), k >= 6, row k has no primes.

Parts:
 A. Obstruction certificate (no primality testing): for every cell of every target row
    k <= KA, exhibit an explicit nontrivial divisor (x-1 via DoS, or 5) and check it
    divides N with 1 < d < N.  Also asserts every cell falls in one of the two cases.
 B. Blind primality (obstruction NOT used): sympy.isprime (BPSW, deterministic < 2^64,
    no known counterexample above) on every cell of target rows k <= KB.
 C. Controls: prime counts per row in L1 for all k <= KC (non-target rows must show
    primes if the test is live — guards against a vacuous 'zero primes' result);
    edge case k = 2.
 D. Reproduce paper Figure 3 right panel (prime counts, rows k = 2,6,...,38, 11 lambdas).
 E. Remark 4.7 spot-checks: lambda=49 (square, =4 mod 5) rows k=0 mod 4; lambda=121
    (square, =1 mod 5) rows k=2 mod 4.
 F. Converse of L2: for odd-odd cells, 5 | N  iff  a = b (mod 4)  (all rows k <= KA).
"""
import sys, time
from sympy import isprime

KA = int(sys.argv[1]) if len(sys.argv) > 1 else 2002
KB = int(sys.argv[2]) if len(sys.argv) > 2 else 250
KC = int(sys.argv[3]) if len(sys.argv) > 3 else 60

def row(lam, k):
    return [(k - b, b, lam * 2**(k - b) * 3**b - 1) for b in range(0, k)]

t0 = time.time()
# ---------- A ----------
target = [k for k in range(6, KA + 1) if k % 4 == 2]
cells = dos = five = 0
for k in target:
    for a, b, N in row(1, k):
        cells += 1
        if a % 2 == 0 and b % 2 == 0:
            x = 2**(a // 2) * 3**(b // 2)
            assert x * x - 1 == N
            d = x - 1
            assert 1 < d < N and N % d == 0, (k, a, b)
            dos += 1
        elif a % 2 == 1 and b % 2 == 1:
            assert (a - b) % 4 == 0, (k, a, b)
            assert N % 5 == 0 and N > 5, (k, a, b)
            five += 1
        else:
            raise AssertionError(f"mixed-parity cell in target row k={k} a={a} b={b}")
print(f"[A] target rows k=6..{KA} (k=2 mod 4): {len(target)} rows, {cells} cells; "
      f"DoS-certified {dos}, 5-certified {five}, uncovered 0. PASS")

# ---------- B ----------
tb = [k for k in range(6, KB + 1) if k % 4 == 2]
nb = 0; primes_found = []
for k in tb:
    for a, b, N in row(1, k):
        nb += 1
        if isprime(N):
            primes_found.append((k, a, b))
print(f"[B] blind isprime over {len(tb)} target rows k=6..{KB}, {nb} cells: "
      f"primes found = {len(primes_found)} {primes_found[:10]}")

# ---------- C ----------
print(f"[C] L1 prime counts per row k=1..{KC} (k : count [class]):")
line = []
nontarget_rows_with_primes = 0; nontarget_rows = 0
for k in range(1, KC + 1):
    c = sum(1 for a, b, N in row(1, k) if isprime(N))
    cls = "T" if k % 4 == 2 else ("o" if k % 2 else "0")
    line.append(f"{k}:{c}{cls}")
    if not (k % 4 == 2):
        nontarget_rows += 1
        nontarget_rows_with_primes += (c > 0)
    if k % 4 == 2 and k >= 6:
        assert c == 0
print("    " + " ".join(line))
print(f"    non-target rows with >=1 prime: {nontarget_rows_with_primes}/{nontarget_rows}")
r2 = [N for a, b, N in row(1, 2)]
print(f"    edge k=2 row = {r2}, primes = {[N for N in r2 if isprime(N)]}")
# k=0 mod 4: prime-admissible = odd-odd cells; primes should only appear there
viol = []
for k in range(4, KC + 1, 4):
    for a, b, N in row(1, k):
        if a % 2 == 0 and b % 2 == 0 and isprime(N):
            viol.append((k, a, b))
print(f"    k=0 mod 4 rows: primes at even-even (DoS) cells = {viol} (expect [])")

# ---------- D ----------
lams = [1, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31]
ks = list(range(2, 39, 4))
paper = {
 1: [2,0,0,0,0,0,0,0,0,0], 5: [2,3,3,2,5,3,4,2,5,6], 7: [1,2,4,7,3,2,6,3,1,6],
 11:[1,1,2,0,0,1,2,3,3,3], 13:[0,3,5,3,6,2,4,2,2,5], 17:[2,4,1,5,1,2,5,5,2,1],
 19:[1,1,2,1,2,1,3,2,0,3], 23:[1,5,2,7,2,5,3,3,3,3], 25:[1,3,2,2,5,2,5,4,2,3],
 29:[1,1,3,2,1,0,2,1,2,0], 31:[0,1,0,2,3,2,1,3,4,4],
}
print(f"[D] Figure 3 right-panel reproduction (rows {ks}):")
mism = 0
for lam in lams:
    ours = [sum(1 for a, b, N in row(lam, k) if isprime(N)) for k in ks]
    ok = ours == paper[lam]
    mism += (not ok)
    print(f"    lam={lam:>2} ours={ours} paper={paper[lam]} {'OK' if ok else 'MISMATCH'}")
print(f"    mismatching lambdas: {mism}/{len(lams)}")

# ---------- E ----------
for lam, cls, lab in [(49, 0, "k=0 mod 4"), (121, 2, "k=2 mod 4"), (49, 2, "k=2 mod 4 (control)")]:
    res = []
    for k in range(max(cls, 1), 81, 4) if cls else range(4, 81, 4):
        c = sum(1 for a, b, N in row(lam, k) if isprime(N))
        res.append((k, c))
    print(f"[E] lam={lam} rows {lab} k<=80 prime counts: {res}")

# ---------- F ----------
bad = 0; n = 0
for k in range(2, min(KA, 600) + 1):
    for a, b, N in row(1, k):
        if a % 2 == 1 and b % 2 == 1:
            n += 1
            if (N % 5 == 0) != ((a - b) % 4 == 0):
                bad += 1
print(f"[F] odd-odd cells k<=600: {n}; iff(5|N, a=b mod 4) violations = {bad}")
print(f"elapsed {time.time()-t0:.1f}s")
