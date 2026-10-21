#!/usr/bin/env python3
"""S146 VALIDATE: exact-rational reproduction of arXiv:2610.15909 Lemma (lem:MinkSumBound) and
the Theorem thm:main upper-bound construction (vxc of an n-gon = O(sqrt n)).
All certified quantities use fractions.Fraction; floats are used only to PROPOSE rational
directions, and every proposal is then checked exactly. Usage: s146_vxc.py <mode> <n> <seed> [K]
mode = thm (theorem construction of Q) | rnd (random Q with K normals, lemma generality)."""
import sys, json, math, random, time
from fractions import Fraction as F
from math import isqrt

def cross(a, b): return a[0]*b[1] - a[1]*b[0]
def dot(a, b): return a[0]*b[0] + a[1]*b[1]

def gen_polygon(n, rng, B=10**6):
    """Generic integer convex n-gon: n integer edge vectors, pairwise non-parallel, sorted by angle, closing."""
    while True:
        es = [(rng.randint(-B, B), rng.randint(-B, B)) for _ in range(n-1)]
        sx = sum(e[0] for e in es); sy = sum(e[1] for e in es)
        es.append((-sx, -sy))
        if any(e == (0, 0) for e in es): continue
        es.sort(key=lambda e: math.atan2(e[1], e[0]))
        ok = True
        for i in range(n):
            for j in range(i+1, n):
                if cross(es[i], es[j]) == 0 and dot(es[i], es[j]) > 0: ok = False; break
            if not ok: break
        if not ok: continue
        if any(cross(es[i], es[(i+1) % n]) <= 0 for i in range(n)): continue
        vs = [(0, 0)]
        for e in es[:-1]: vs.append((vs[-1][0]+e[0], vs[-1][1]+e[1]))
        A = [(e[1], -e[0]) for e in es]          # outer normal of edge k; vertex k = start of edge k
        b = [dot(A[k], vs[k]) for k in range(n)]
        for k, v in enumerate(vs):               # exact convex-position check
            tight = [i for i in range(n) if dot(A[i], v) == b[i]]
            if any(dot(A[i], v) > b[i] for i in range(n)) or sorted(tight) != sorted({k, (k-1) % n}):
                ok = False; break
        if ok: return vs, A, b

def in_open_cone(a, b, u): return cross(a, u) > 0 and cross(u, b) > 0

def rat_circle_point(theta, a=None, b=None):
    for D in [10, 100, 10**3, 10**4, 10**6, 10**9, 10**12]:
        th = math.atan2(math.sin(theta), math.cos(theta))
        if abs(abs(th) - math.pi) < 1e-9: th = th - 1e-6
        t = F(math.tan(th/2)).limit_denominator(D)
        u = ((1 - t*t)/(1 + t*t), 2*t/(1 + t*t))
        assert u[0]*u[0] + u[1]*u[1] == 1
        if a is None or in_open_cone(a, b, u): return u
    raise RuntimeError("no rational point in cone")

def ang(v): return math.atan2(float(v[1]), float(v[0]))

def bisector_angle(a, b):
    na = math.hypot(*map(float, a)); nb = math.hypot(*map(float, b))
    return math.atan2(float(a[1])/na + float(b[1])/nb, float(a[0])/na + float(b[0])/nb)

def sort_ccw(us): return sorted(us, key=ang)

def positively_spanning(us):
    us = sort_ccw(us); K = len(us)
    return K >= 3 and all(cross(us[i], us[(i+1) % K]) > 0 for i in range(K))

def vertex_cone_containing(A, u):
    n = len(A)
    for k in range(n):
        if in_open_cone(A[(k-1) % n], A[k], u): return k
    return None

def build_Q_theorem(A, n, rng):
    s = isqrt(n - 1) + 1                    # ceil(sqrt n)
    assert (s-1)*(s-1) < n <= s*s
    us = []
    for lab in range(s, n+1, s):           # labels 1..n, multiples of s
        k = lab - 1
        us.append(rat_circle_point(bisector_angle(A[(k-1) % n], A[k]), A[(k-1) % n], A[k]))
    added = 0
    if not positively_spanning(us):
        for attempt in range(1000):
            th0 = rng.uniform(0, 2*math.pi); extra = []
            for dd in range(3):
                u = rat_circle_point(th0 + dd*2*math.pi/3)
                if vertex_cone_containing(A, u) is None: break
                extra.append(u)
            if len(extra) == 3 and positively_spanning(us + extra) and len(set(us + extra)) == len(us) + 3:
                us = us + extra; added = 3; break
        else:
            raise RuntimeError("could not add 3 points")
    return sort_ccw(us), s, added

def build_Q_random(A, K, rng):
    while True:
        us = []
        for _ in range(K):
            u = rat_circle_point(rng.uniform(0, 2*math.pi))
            if any(cross(u, a) == 0 and dot(u, a) > 0 for a in A): continue
            us.append(u)
        us = list(set(us))
        if positively_spanning(us): return sort_ccw(us)

def polygon_vertices_from_H(C, d):
    K = len(C); qs = []
    for i in range(K):
        a, b = C[i], C[(i+1) % K]
        det = cross(a, b)
        x = (d[i]*b[1] - a[1]*d[(i+1) % K]) / det
        y = (a[0]*d[(i+1) % K] - d[i]*b[0]) / det
        qs.append((x, y))   # vertex i lies between normals i and i+1
    return qs

def argmax(c, pts):
    vals = [dot(c, p) for p in pts]; m = max(vals)
    return [i for i, v in enumerate(vals) if v == m]

def run(mode, n, seed, K=None, brute=False):
    t0 = time.time(); rng = random.Random(seed*1000003 + n)
    vs, A, b = gen_polygon(n, rng)
    res = {"mode": mode, "n": n, "seed": seed}
    if mode == "thm":
        C, s, added = build_Q_theorem(A, n, rng); res.update(s=s, added3=added)
    else:
        C = build_Q_random(A, K, rng); res.update(K_req=K)
    nq = len(C); d = [F(1)]*nq
    qs = polygon_vertices_from_H(C, d)
    v1 = {}
    v1["Q_bounded_pos_span"] = positively_spanning(C)
    v1["Q_all_facets_irredundant"] = all(
        all(dot(C[i], qs[j]) <= d[i] for i in range(nq)) and
        sorted(i for i in range(nq) if dot(C[i], qs[j]) == d[i]) == sorted({j, (j+1) % nq})
        for j in range(nq))
    v1["no_parallel_rows"] = all(not (cross(a, c) == 0 and dot(a, c) > 0) for a in A for c in C)
    if mode == "thm":
        v1["nq_le_n_over_s_plus_3"] = nq <= n // s + 3
        v1["nq_le_sqrtn_plus_3"] = nq <= 3 or (nq - 3)**2 <= n
    res["nq"] = nq; res["V1"] = v1
    normals = [("A", k, A[k]) for k in range(n)] + [("C", j, C[j]) for j in range(nq)]
    normals.sort(key=lambda t: ang(t[2]))
    NN = len(normals)
    assert all(cross(normals[i][2], normals[(i+1) % NN][2]) > 0 for i in range(NN)), "merged fan not strictly ccw"
    rv = []
    for i in range(NN):
        c = (F(normals[i][2][0]) + F(normals[(i+1) % NN][2][0]), F(normals[i][2][1]) + F(normals[(i+1) % NN][2][1]))
        ip = argmax(c, vs); iq = argmax(c, qs)
        assert len(ip) == 1 and len(iq) == 1
        rv.append((ip[0], iq[0]))
    groups = {i: [] for i in range(nq)}
    for (p, q) in rv:
        if not groups[q] or groups[q][-1] != p: groups[q].append(p)
    ell = max(len(g) for g in groups.values())
    res["ell"] = ell; res["R_vertices"] = len(rv); res["R_facets"] = NN
    ell2 = 0
    for i in range(nq):
        a, bb = C[i], C[(i+1) % nq]
        cnt = sum(1 for k in range(n) if (cross(a, A[k]) > 0 and cross(A[k], bb) > 0)) + 1
        ell2 = max(ell2, cnt)
    res["ell_crosscheck"] = ell2
    if mode == "thm": res["ell_le_2s_plus_1"] = ell <= 2*s + 1
    fk = []
    for k in range(n):
        ix = argmax(A[k], qs); assert len(ix) == 1; fk.append(ix[0])
    pad = {i: groups[i] + [groups[i][-1]]*(ell - len(groups[i])) for i in range(nq)}
    lamstar = F(0)
    for k in range(n):
        t = fk[k]; hk = dot(A[k], qs[t])
        for i in range(nq):
            if i == t: continue
            gap = hk - dot(A[k], qs[i]); assert gap > 0
            for j in range(ell):
                pt, pi = vs[pad[t][j]], vs[pad[i][j]]
                need = -F(dot(A[k], (pt[0]-pi[0], pt[1]-pi[1]))) / gap
                if need > lamstar: lamstar = need
    res["lambda_star_float"] = float(lamstar)
    lam = lamstar + 1 if lamstar > 0 else F(1)
    res["lambda_used_float"] = float(lam)
    rhs = [max(dot(c, v) for v in vs) + lam*max(dot(c, q) for q in qs) for (_, _, c) in normals]
    Rverts = [(vs[p][0] + lam*qs[q][0], vs[p][1] + lam*qs[q][1]) for (p, q) in rv]
    v2 = {}
    v2["facets_eq_union"] = NN == n + nq
    ok = True
    for i, r in enumerate(Rverts):
        tight = sorted(x for x in range(NN) if dot(normals[x][2], r) == rhs[x])
        if any(dot(normals[x][2], r) > rhs[x] for x in range(NN)) or tight != sorted({i, (i+1) % NN}): ok = False; break
    v2["R_vertices_tight_exactly_two"] = ok
    v2["nvert_eq_nfacet"] = len(set(Rverts)) == NN
    if brute:
        allok = True
        for p in vs:
            for q in qs:
                x = (p[0] + lam*q[0], p[1] + lam*q[1])
                if any(dot(normals[z][2], x) > rhs[z] for z in range(NN)): allok = False; break
            if not allok: break
        v2["brute_all_sums_in_R"] = allok
    res["V2"] = v2
    cols = [(i, j) for i in range(nq) for j in range(ell)]
    rpt = {(i, j): (vs[pad[i][j]][0] + lam*qs[i][0], vs[pad[i][j]][1] + lam*qs[i][1]) for (i, j) in cols}
    Aidx = {t[1]: x for x, t in enumerate(normals) if t[0] == "A"}
    Cidx = {t[1]: x for x, t in enumerate(normals) if t[0] == "C"}
    SA = [[rhs[Aidx[k]] - dot(A[k], rpt[c]) for c in cols] for k in range(n)]
    SC = [[rhs[Cidx[jj]] - dot(C[jj], rpt[c]) for c in cols] for jj in range(nq)]
    v3 = {}
    v3["slack_nonneg"] = all(x >= 0 for row in SA + SC for x in row)
    colpos = {c: x for x, c in enumerate(cols)}
    M = [[SA[k][colpos[(fk[k], j)]] for (i, j) in cols] for k in range(n)]
    N = [[SA[k][x] - M[k][x] for x in range(len(cols))] for k in range(n)]
    v3["M_distinct_cols_le_ell"] = len({tuple(M[k][x] for k in range(n)) for x in range(len(cols))}) <= ell
    v3["N_nonneg"] = all(x >= 0 for row in N for x in row)
    v3["N_zero_on_i_eq_fk"] = all(N[k][colpos[(fk[k], j)]] == 0 for k in range(n) for j in range(ell))
    def ovec(t, i, j):
        return (lam*(qs[t][0]-qs[i][0]) + vs[pad[t][j]][0] - vs[pad[i][j]][0],
                lam*(qs[t][1]-qs[i][1]) + vs[pad[t][j]][1] - vs[pad[i][j]][1])
    v3["N_t_equals_Asub_O_t"] = all(dot(A[k], ovec(fk[k], i, j)) == N[k][x] for k in range(n) for x, (i, j) in enumerate(cols))
    res["V3"] = v3
    # V4: explicit nonnegative factorization S = W H
    H_rows = []
    for j in range(ell):
        H_rows.append([F(1) if cj == j else F(0) for (ci, cj) in cols])
    Wfull = [dict() for _ in range(n + nq)]
    for k in range(n):
        for j in range(ell):
            v = SA[k][colpos[(fk[k], j)]]
            if v != 0: Wfull[k][j] = v
    inner = ell; ranks = []
    for t in range(nq):
        rows = [k for k in range(n) if fk[k] == t]
        if not rows: ranks.append(0); continue
        os_ = [ovec(t, i, j) for (i, j) in cols]
        nzmask = [any(dot(A[k], o) != 0 for k in rows) for o in os_]
        nz = [o for o, m_ in zip(os_, nzmask) if m_]
        if not nz: ranks.append(0); continue
        if len(rows) == 1:
            Wfull[rows[0]][inner] = F(1)
            H_rows.append([dot(A[rows[0]], o) for o in os_]); inner += 1; ranks.append(1); continue
        omin = nz[0]; omax = nz[0]
        for o in nz:
            if cross(o, omin) > 0: omin = o
            if cross(omax, o) > 0: omax = o
        assert all(cross(omin, o) >= 0 and cross(o, omax) >= 0 for o in nz), "column cone not pointed"
        det = cross(omin, omax)
        if det == 0:
            for k in rows:
                val = dot(A[k], omin)
                if val != 0: Wfull[k][inner] = val
            hr = []
            for o, m_ in zip(os_, nzmask):
                hr.append(((o[0]/omin[0]) if omin[0] != 0 else (o[1]/omin[1])) if m_ else F(0))
            H_rows.append(hr); inner += 1; ranks.append(1); continue
        for k in rows:
            a1, a2 = dot(A[k], omin), dot(A[k], omax)
            if a1 != 0: Wfull[k][inner] = a1
            if a2 != 0: Wfull[k][inner+1] = a2
        h1, h2 = [], []
        for o, m_ in zip(os_, nzmask):
            if not m_: h1.append(F(0)); h2.append(F(0)); continue
            h1.append(F(cross(o, omax)) / det); h2.append(F(cross(omin, o)) / det)
        H_rows.append(h1); H_rows.append(h2); inner += 2; ranks.append(2)
    for jj in range(nq):
        Wfull[n + jj][inner + jj] = F(1)
        H_rows.append(SC[jj])
    inner += nq
    S = SA + SC
    v4 = {}
    v4["W_nonneg"] = all(v >= 0 for row in Wfull for v in row.values())
    v4["H_nonneg"] = all(x >= 0 for row in H_rows for x in row)
    prod_ok = True
    for r_ in range(n + nq):
        for x in range(len(cols)):
            sacc = F(0)
            for col_, w in Wfull[r_].items(): sacc += w * H_rows[col_][x]
            if sacc != S[r_][x]: prod_ok = False; break
        if not prod_ok: break
    v4["WH_eq_S_exact"] = prod_ok
    v4["inner_le_ell_plus_3nq"] = inner <= ell + 3*nq
    res["V4"] = v4
    res["inner_dim"] = inner; res["lemma_bound"] = ell + 3*nq
    res["vxc_upper"] = nq + inner
    res["trivial_xc_R"] = n + nq; res["trivial_xc_P"] = n
    res["ratio_vxc_upper_sqrtn"] = round((nq + inner) / math.sqrt(n), 4)
    res["ranks"] = {"2": ranks.count(2), "1": ranks.count(1), "0": ranks.count(0)}
    res["all_pass"] = all(all(v for v in blk.values() if isinstance(v, bool)) for blk in (v1, v2, v3, v4)) and ell == ell2
    res["secs"] = round(time.time() - t0, 2)
    return res

if __name__ == "__main__":
    mode, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    K = int(sys.argv[4]) if len(sys.argv) > 4 else None
    print(json.dumps(run(mode, n, seed, K, brute=(n <= 100))), flush=True)
