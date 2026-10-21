#!/usr/bin/env python3
"""S46: Peng v4 Def. 8.1.4 + Lemma 8.1.5 (Case O2): generic AND Std-generic => regular.
Toy unramified model as in s46_generic_vs_regular.py. Std-generic: Std o phi_T has eigenvalues
eta = (t_1..t_n, t_n^-1..t_1^-1); for all a != b: eta_a/eta_b not in {1, q, q^-1}.
Predictions: (i) #(generic & Std-generic & not regular) == 0; (ii) Std-generic is not vacuous in some case;
(iii) Std-generic is strictly stronger than generic in some case (so it is a real extra hypothesis)."""
import itertools, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from s46_generic_vs_regular import run  # noqa: F401 (reuse module for consistency)

def check(l, q, n):
    units = list(range(1, l)); inv = {x: pow(x, l - 2, l) for x in units}
    bad = {1, q % l, inv[q % l]}
    W = [(p, s) for p in itertools.permutations(range(n)) for s in itertools.product([1, -1], repeat=n)
         if s.count(-1) % 2 == 0 and not (p == tuple(range(n)) and all(x == 1 for x in s))]
    act = lambda t, p, s: tuple(t[p[i]] if s[i] == 1 else inv[t[p[i]]] for i in range(n))
    gen = sg = sg_notreg = 0
    for t in itertools.product(units, repeat=n):
        cv = [t[i] * inv[t[j]] % l for i in range(n) for j in range(i + 1, n)] + \
             [t[i] * t[j] % l for i in range(n) for j in range(i + 1, n)]
        if any(x in bad for x in cv):
            continue
        gen += 1
        eta = list(t) + [inv[x] for x in reversed(t)]
        if any(eta[a] * inv[eta[b]] % l in bad for a in range(2 * n) for b in range(2 * n) if a != b):
            continue
        sg += 1
        if any(act(t, p, s) == t for p, s in W):
            sg_notreg += 1
    return gen, sg, sg_notreg

if __name__ == '__main__':
    fail = 0; nonvac = stricter = False
    for l, q, n in [(13, 5, 2), (13, 5, 3), (17, 3, 2), (17, 3, 3), (11, 2, 3), (19, 7, 3), (29, 2, 3)]:
        g, s, snr = check(l, q, n)
        fail += snr != 0; nonvac |= s > 0; stricter |= s < g
        print(f"l={l:2d} q={q:2d} n={n} O2: generic={g:6d} generic&Std-generic={s:6d} of_which_not_regular={snr}")
    print(f"mismatches={fail} stdgeneric_nonvacuous={nonvac} stdgeneric_strictly_stronger={stricter}")
    sys.exit(1 if (fail or not nonvac or not stricter) else 0)
