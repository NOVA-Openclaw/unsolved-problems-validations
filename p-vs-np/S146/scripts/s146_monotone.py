#!/usr/bin/env python3
"""S146 V8: brute-force check of arXiv:2610.15909 Lemma lem:monotone for n=4,6 (exact integers)."""
import itertools, random, json
def comps_has_odd(n, F):
    par = list(range(n))
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for (u, v) in F: par[find(u)] = find(v)
    cnt = {}
    for x in range(n): r = find(x); cnt[r] = cnt.get(r, 0) + 1
    return any(c % 2 == 1 for c in cnt.values())
out = {}
for n in (4, 6):
    E = list(itertools.combinations(range(n), 2)); m = len(E)
    odd_sets = [S for r in range(1, n, 2) for S in itertools.combinations(range(n), r)]
    good = [mask for mask in range(1 << m) if comps_has_odd(n, [E[i] for i in range(m) if mask >> i & 1])]
    rng = random.Random(146 + n)
    ws = [[0]*m, [-1]*m] + [[rng.randint(-9, 9) for _ in range(m)] for _ in range(200)]
    ok = 0
    for w in ws:
        h = max(sum(w[i] for i in range(m) if mask >> i & 1) for mask in good)
        c = [max(x, 0) for x in w]
        tau = min(sum(c[i] for i, (u, v) in enumerate(E) if (u in S) != (v in S)) for S in odd_sets)
        hc = max(sum(c[i] for i in range(m) if mask >> i & 1) for mask in good)
        if h == hc == sum(c) - tau: ok += 1
    out[f"n{n}"] = {"edges": m, "odd_component_sets": len(good), "w_tested": len(ws), "w_pass": ok}
out["all_pass"] = all(v["w_pass"] == v["w_tested"] for v in out.values())
print(json.dumps(out))
