#!/usr/bin/env python3
"""S46 VALIDATE Peng arXiv:2503.04623v4, section 8.1 (before Definition 8.1.4):
  "In Cases U and O1, genericity is sufficient for regularity. In Case O2 this is
   no longer true in general, because the D_n coroots do not include the characters 2*eps_i."

Toy model (a proxy, not the paper's full setting):
  * split group G over K, unramified toral parameter phi_T, i.e. Frobenius -> t in T^(F_l) = (F_l^x)^n
  * G's torus is a torus, so the highest-weight tilting module of ^L T at mu is the 1-dim character mu.
    For an unramified character with Frobenius value x, RGamma(W_K, x) = 0  <=>  x != 1 and x != q (H^0 / H^2 by Tate duality).
    Imposing this on phi_T and on its Chevalley dual phi_T^vee gives: generic <=> for every positive coroot a of G,
        a(t) not in {1, q, q^-1}   (mod l).
  * regular (Def. 8.1.1): chi != chi^w for all nontrivial w in W_G; unramified => t != w(t).
Groups (coroots of G = roots of the dual group):
  O1: G = SO(2n+1), coroots type C_n: e_i +- e_j, 2e_i ; W = signed permutations
  O2: G = SO(2n) split, coroots type D_n: e_i +- e_j ; W = signed permutations with an even number of sign flips
  GL: G = GL_n (proxy for Case U after base change to the splitting field; U itself not modelled): e_i - e_j ; W = S_n
Counts: generic parameters that are NOT regular. The paper's claim predicts 0 for O1 and GL, >0 for O2.
"""
import itertools, sys

def run(l, q, n):
    units = list(range(1, l))
    inv = {x: pow(x, l - 2, l) for x in units}
    bad = {1, q % l, inv[q % l]}
    perms = list(itertools.permutations(range(n)))
    signs = list(itertools.product([1, -1], repeat=n))
    def act(t, p, s):
        return tuple(t[p[i]] if s[i] == 1 else inv[t[p[i]]] for i in range(n))
    def ws(kind):
        out = []
        for p in perms:
            for s in (signs if kind != 'GL' else [(1,) * n]):
                if kind == 'O2' and s.count(-1) % 2:
                    continue
                if p == tuple(range(n)) and all(x == 1 for x in s):
                    continue
                out.append((p, s))
        return out
    def coroot_vals(t, kind):
        v = []
        for i in range(n):
            for j in range(i + 1, n):
                v.append(t[i] * inv[t[j]] % l)
                if kind != 'GL':
                    v.append(t[i] * t[j] % l)
            if kind == 'O1':
                v.append(t[i] * t[i] % l)
        return v
    res = {}
    for kind in ('O1', 'O2', 'GL'):
        W = ws(kind)
        gen = gen_notreg = 0
        example = None
        for t in itertools.product(units, repeat=n):
            if any(x in bad for x in coroot_vals(t, kind)):
                continue
            gen += 1
            if any(act(t, p, s) == t for p, s in W):
                gen_notreg += 1
                if example is None:
                    example = t
        res[kind] = (gen, gen_notreg, example)
    return res

if __name__ == '__main__':
    cases = [(13, 5, 2), (13, 5, 3), (17, 3, 2), (17, 3, 3), (11, 2, 3), (19, 7, 3)]
    fail = 0
    for l, q in {(a, b) for a, b, _ in cases}:
        assert pow(q, 2, l) != 1, (l, q)
    for l, q, n in cases:
        r = run(l, q, n)
        for kind, (g, gnr, ex) in r.items():
            pred_zero = kind in ('O1', 'GL')
            ok = (gnr == 0) if pred_zero else (gnr > 0)
            fail += (not ok)
            print(f"l={l:2d} q={q:2d} n={n} {kind}: generic={g:6d} generic_not_regular={gnr:5d} example={ex} "
                  f"prediction={'0' if pred_zero else '>0'} {'OK' if ok else 'MISMATCH'}")
    print(f"TOTAL cases={len(cases)*3} mismatches={fail}")
    # sanity: the count is non-vacuous (some generic parameters exist in every case)
    sys.exit(1 if fail else 0)
