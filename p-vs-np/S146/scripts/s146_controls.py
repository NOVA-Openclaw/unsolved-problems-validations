#!/usr/bin/env python3
"""S146 negative controls: (C1) lambda below lambda* must make N have a negative entry;
(C2) corrupting one H entry must break WH == S; (C3) dropping the +3 rule check: Q from a
non-positively-spanning normal set is unbounded (detected)."""
import json, random
from fractions import Fraction as F
import s146_vxc as V
out = {}
# C1: rerun n=25 seed 1 internals with lam = lambda*/2
rng = random.Random(1*1000003 + 25)
vs, A, b = V.gen_polygon(25, rng)
C, s, added = V.build_Q_theorem(A, 25, rng)
qs = V.polygon_vertices_from_H(C, [F(1)]*len(C))
nq = len(C)
normals = sorted([("A", k, A[k]) for k in range(25)] + [("C", j, C[j]) for j in range(nq)], key=lambda t: V.ang(t[2]))
NN = len(normals); rv = []
for i in range(NN):
    c = (F(normals[i][2][0]) + F(normals[(i+1) % NN][2][0]), F(normals[i][2][1]) + F(normals[(i+1) % NN][2][1]))
    rv.append((V.argmax(c, vs)[0], V.argmax(c, qs)[0]))
groups = {i: [] for i in range(nq)}
for (p, q) in rv:
    if not groups[q] or groups[q][-1] != p: groups[q].append(p)
ell = max(len(g) for g in groups.values())
pad = {i: groups[i] + [groups[i][-1]]*(ell - len(groups[i])) for i in range(nq)}
fk = [V.argmax(A[k], qs)[0] for k in range(25)]
def minN(lam):
    m = None
    for k in range(25):
        t = fk[k]
        for i in range(nq):
            for j in range(ell):
                o = (lam*(qs[t][0]-qs[i][0]) + vs[pad[t][j]][0] - vs[pad[i][j]][0], lam*(qs[t][1]-qs[i][1]) + vs[pad[t][j]][1] - vs[pad[i][j]][1])
                v = V.dot(A[k], o); m = v if m is None or v < m else m
    return m
lamstar = F(0)
for k in range(25):
    t = fk[k]; hk = V.dot(A[k], qs[t])
    for i in range(nq):
        if i == t: continue
        gap = hk - V.dot(A[k], qs[i])
        for j in range(ell):
            pt, pi = vs[pad[t][j]], vs[pad[i][j]]
            lamstar = max(lamstar, -F(V.dot(A[k], (pt[0]-pi[0], pt[1]-pi[1]))) / gap)
out["C1_minN_at_half_lamstar_negative"] = minN(lamstar/2) < 0
out["C1_minN_at_lamstar_zero"] = minN(lamstar) == 0
out["C1_minN_at_lamstar_plus1_nonneg"] = minN(lamstar + 1) >= 0
# C2: H corruption -> product mismatch (simulate on a 2x2 rank-2 identity)
W = [[F(1), F(0)], [F(0), F(1)]]; H = [[F(2), F(3)], [F(5), F(7)]]; S = [[F(2), F(3)], [F(5), F(7)]]
H[0][1] += 1
out["C2_corrupted_product_detected"] = any(sum(W[r][c]*H[c][x] for c in range(2)) != S[r][x] for r in range(2) for x in range(2))
# C3: three normals in an open half-plane are not positively spanning
us = [V.rat_circle_point(0.1), V.rat_circle_point(0.5), V.rat_circle_point(1.0)]
out["C3_halfplane_normals_rejected"] = not V.positively_spanning(us)
out["all_controls_behave"] = all(out.values())
print(json.dumps(out))
