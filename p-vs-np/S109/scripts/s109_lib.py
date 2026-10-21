"""S109 independent instrument: corrector LP built DIRECTLY from Lemma-1 on the product kernel.

Does NOT use S83/S85/S95 LP builders. Uses restored bytecode only for (a) member support lists,
(b) the S85 get_Hpp_M witness (so we test the SAME witness S95 used), and we re-verify those
witnesses exactly here with our own Moebius/upward code.

Index convention: product z = u + (v << n1), u = low n1 bits (same as common.tensor_kernel).
Lemma 1 (S78/S80) for kernel g: mu with (U mu)_0 = 1, (U mu)_T = -sign(ghat_T) on supp\\0,
|U mu| <= 1 off supp, mu(z) g(z) <= 0.  (U mu)_T = sum_{z superset T} mu(z).

Corrector ansatz (S83): mu(.,v) = M2(v) A1 for v in Neg2 (fixed payload), X_v free for v in Pos2,
with pattern (U1 X_v)_{T1} = lam_v s1(T1) on supp1\\0.  Objective: min lam_0.
"""
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog


def g_from_support(n, S):
    return [(-1 if z in set(S) else 1) for z in range(1 << n)]


def moebius(vals, n):  # exact: c_T with vals(z) = sum_{T subset z} c_T
    c = [F(x) for x in vals]
    for i in range(n):
        b = 1 << i
        for z in range(1 << n):
            if z & b:
                c[z] -= c[z ^ b]
    return c


def upward(mu, n):  # exact superset sums
    a = [F(x) for x in mu]
    for i in range(n):
        b = 1 << i
        for z in range(1 << n):
            if not z & b:
                a[z] += a[z | b]
    return a


def sgn(x):
    return (x > 0) - (x < 0)


def supp_signs(n, g):
    gh = moebius(g, n)
    return {T: (1 if T == 0 else sgn(gh[T])) for T in range(1 << n) if gh[T] != 0}


def lemma1_exact(n, g, mu):
    """Exact Lemma-1 check. Returns (ok, list_of_violations)."""
    gh = moebius(g, n)
    U = upward(mu, n)
    bad = []
    for T in range(1 << n):
        if gh[T] != 0:
            tgt = 1 if T == 0 else -sgn(gh[T])
            if U[T] != tgt:
                bad.append(('eq', T, U[T], tgt))
        elif abs(U[T]) > 1:
            bad.append(('box', T, U[T]))
    for z in range(1 << n):
        if mu[z] * g[z] > 0:
            bad.append(('sign', z, mu[z]))
    return (not bad), bad


def h_check_exact(n, g, A, B):
    """Condition H (common.condition_H docstring): A aligned, B anti-aligned,
    (U A)_T = +s(T) on supp (0 -> 1), |UA|<=1 off; (U(A+B))_0 = 1, = -s(T) on supp\\0, |.|<=1 off."""
    s = supp_signs(n, g)
    UA = upward(A, n)
    UM = upward([a + b for a, b in zip(A, B)], n)
    N = 1 << n
    ok = all(A[z] * g[z] >= 0 and B[z] * g[z] <= 0 for z in range(N))
    for T in range(N):
        if T in s:
            ok &= UA[T] == s[T]
            ok &= UM[T] == (1 if T == 0 else -s[T])
        else:
            ok &= abs(UA[T]) <= 1 and abs(UM[T]) <= 1
    return ok


def ha_check_exact(n, g, A):
    s = supp_signs(n, g)
    UA = upward(A, n)
    ok = all(A[z] * g[z] >= 0 for z in range(1 << n))
    for T in range(1 << n):
        ok &= (UA[T] == s[T]) if T in s else (abs(UA[T]) <= 1)
    return ok


def build_lp(n1, g1, A1, n2, g2, M2):
    """Returns LP data (float) + exact copies, plus index maps."""
    N1, N2 = 1 << n1, 1 << n2
    s1 = supp_signs(n1, g1)
    s2 = supp_signs(n2, g2)
    Pos = [v for v in range(N2) if g2[v] == 1]
    Neg = [v for v in range(N2) if g2[v] == -1]
    assert 0 in Pos
    a = upward(A1, n1)
    xi = {}  # (v,u) -> col
    for v in Pos:
        for u in range(N1):
            xi[(v, u)] = len(xi)
    li = {v: len(xi) + k for k, v in enumerate(Pos)}
    nv = len(xi) + len(Pos)
    Eq, beq, Ub, bub = [], [], [], []
    # pattern rows
    for v in Pos:
        for T1 in s1:
            if T1 == 0:
                continue
            r = {}
            for u in range(N1):
                if u & T1 == T1:
                    r[xi[(v, u)]] = F(1)
            r[li[v]] = F(-s1[T1])
            Eq.append(r); beq.append(F(0))
    # Lemma-1 rows on the product
    for T2 in range(N2):
        Nsum_v = [v for v in Neg if v & T2 == T2]
        Psum_v = [v for v in Pos if v & T2 == T2]
        for T1 in range(N1):
            r = {}
            for v in Psum_v:
                for u in range(N1):
                    if u & T1 == T1:
                        r[xi[(v, u)]] = r.get(xi[(v, u)], F(0)) + 1
            const = sum((F(M2[v]) for v in Nsum_v), F(0)) * a[T1]
            if T1 in s1 and T2 in s2:
                tgt = F(1) if (T1 == 0 and T2 == 0) else F(-s1[T1] * s2[T2])
                Eq.append(r); beq.append(tgt - const)
            else:
                Ub.append(dict(r)); bub.append(F(1) - const)
                Ub.append({k: -c for k, c in r.items()}); bub.append(F(1) + const)
    bounds = []
    for (v, u), j in sorted(xi.items(), key=lambda t: t[1]):
        bounds.append((None, 0) if g1[u] == 1 else (0, None))
    bounds += [(None, None)] * len(Pos)
    return dict(nv=nv, xi=xi, li=li, Pos=Pos, Neg=Neg, Eq=Eq, beq=beq, Ub=Ub, bub=bub,
                bounds=bounds, N1=N1, N2=N2)


def dense(rows, nv):
    M = np.zeros((len(rows), nv))
    for i, r in enumerate(rows):
        for j, c in r.items():
            M[i, j] = float(c)
    return M


def solve(L, obj_col, sense=1):
    nv = L['nv']
    c = np.zeros(nv); c[obj_col] = sense
    Aeq = dense(L['Eq'], nv); Aub = dense(L['Ub'], nv)
    res = linprog(c, A_ub=Aub, b_ub=[float(b) for b in L['bub']], A_eq=Aeq,
                  b_eq=[float(b) for b in L['beq']], bounds=L['bounds'], method='highs')
    return res


def rat(x, D=10**6):
    return F(float(x)).limit_denominator(D)


def exact_primal_check(L, x):
    """x: list of Fractions. Check every constraint exactly."""
    for r, b in zip(L['Eq'], L['beq']):
        if sum(c * x[j] for j, c in r.items()) != b:
            return False
    for r, b in zip(L['Ub'], L['bub']):
        if sum(c * x[j] for j, c in r.items()) > b:
            return False
    for j, (lo, hi) in enumerate(L['bounds']):
        if lo is not None and x[j] < lo: return False
        if hi is not None and x[j] > hi: return False
    return True


def exact_dual_bound(L, obj_col, y, w):
    """Weak-duality certificate for min x[obj_col]: c = Aeq^T y + Aub^T w + r, w<=0,
    r_j sign-compatible with bounds (r_j>=0 if x_j>=0 only, <=0 if x_j<=0 only, 0 if free).
    Returns exact bound b_eq.y + b_ub.w, or None if the certificate is invalid."""
    nv = L['nv']
    if any(wi > 0 for wi in w):
        return None
    r = [F(0)] * nv; r[obj_col] = F(1)
    for row, yi in zip(L['Eq'], y):
        if yi:
            for j, c in row.items(): r[j] -= c * yi
    for row, wi in zip(L['Ub'], w):
        if wi:
            for j, c in row.items(): r[j] -= c * wi
    for j, (lo, hi) in enumerate(L['bounds']):
        if lo is None and hi is None and r[j] != 0: return None
        if lo is not None and hi is None and r[j] < 0: return None   # x>=0 needs r>=0
        if hi is not None and lo is None and r[j] > 0: return None   # x<=0 needs r<=0
    return sum((b * yi for b, yi in zip(L['beq'], y)), F(0)) + sum((b * wi for b, wi in zip(L['bub'], w)), F(0))


def assemble_mu(L, n1, A1, n2, M2, x):
    N1, N2 = L['N1'], L['N2']
    mu = [F(0)] * (N1 * N2)
    for v in range(N2):
        for u in range(N1):
            z = u + (v << n1)
            mu[z] = x[L['xi'][(v, u)]] if v in L['li'] else F(M2[v]) * F(A1[u])
    return mu


def tensor(n1, g1, n2, g2):
    return [g1[z & ((1 << n1) - 1)] * g2[z >> n1] for z in range(1 << (n1 + n2))]


def h_lp(n, g, c=None, extra_ub=(), normalized=True):
    """H-witness LP in x=(A,B) (2N vars), built independently from the Condition-H definition.
    normalized: add M=A+B >= 0 on Neg (S83 H+ normalization, required by the corrector payload).
    Returns scipy result."""
    N = 1 << n
    s = supp_signs(n, g)
    Ueq, beq, Uub, bub = [], [], [], []
    def up_row(T, offA, offB):
        r = np.zeros(2 * N)
        for z in range(N):
            if z & T == T:
                if offA: r[z] = 1
                if offB: r[N + z] = 1
        return r
    for T in range(N):
        rA = up_row(T, True, False); rM = up_row(T, True, True)
        if T in s:
            Ueq.append(rA); beq.append(s[T])
            Ueq.append(rM); beq.append(1 if T == 0 else -s[T])
        else:
            for r in (rA, rM):
                Uub.append(r); bub.append(1); Uub.append(-r); bub.append(1)
    if normalized:
        for v in range(N):
            if g[v] == -1:
                r = np.zeros(2 * N); r[v] = -1; r[N + v] = -1
                Uub.append(r); bub.append(0)
    for r, b in extra_ub:
        Uub.append(np.array(r, dtype=float)); bub.append(b)
    bounds = [((0, None) if g[z] == 1 else (None, 0)) for z in range(N)] + \
             [((None, 0) if g[z] == 1 else (0, None)) for z in range(N)]
    cc = np.zeros(2 * N) if c is None else np.array(c, dtype=float)
    return linprog(cc, A_ub=np.array(Uub), b_ub=bub, A_eq=np.array(Ueq), b_eq=beq, bounds=bounds, method='highs')


def build_joint_lp(n1, g1, n2, g2, M2, hpp=False):
    """Corrector LP with the g1 witness (A1,B1) as VARIABLES (payload M2(v)A1 is linear in A1 for fixed M2).
    Witness constrained to the normalized H-polytope (M1>=0 on Neg1); optionally also H++.
    Returns an LP dict compatible with solve/exact_primal_check/exact_dual_bound."""
    base = build_lp(n1, g1, [0] * (1 << n1), n2, g2, M2)   # A1=0 -> constants carry no payload
    N1 = 1 << n1
    off = base['nv']
    nv = off + 2 * N1
    # re-add payload as linear terms: row(T2,T1) gets + (sum_{v in Neg, v>=T2} M2(v)) * (U A1)_{T1}
    Eq, beq, Ub, bub = [], [], [], []
    s1 = supp_signs(n1, g1); s2 = supp_signs(n2, g2)
    Neg = base['Neg']
    k_eq = 0; k_ub = 0
    # pattern rows come first in base['Eq'] (count them)
    npat = sum(1 for v in base['Pos'] for T1 in s1 if T1 != 0)
    for i in range(npat):
        Eq.append(dict(base['Eq'][i])); beq.append(base['beq'][i])
    ei = npat; ui = 0
    for T2 in range(1 << n2):
        Ns = sum((F(M2[v]) for v in Neg if v & T2 == T2), F(0))
        for T1 in range(N1):
            pay = {off + u: Ns for u in range(N1) if u & T1 == T1} if Ns != 0 else {}
            if T1 in s1 and T2 in s2:
                r = dict(base['Eq'][ei]); r.update({k: r.get(k, 0) + c for k, c in pay.items()})
                Eq.append(r); beq.append(base['beq'][ei]); ei += 1
            else:
                r = dict(base['Ub'][ui]); r.update({k: r.get(k, 0) + c for k, c in pay.items()})
                Ub.append(r); bub.append(base['bub'][ui])
                r2 = dict(base['Ub'][ui + 1]); r2.update({k: r2.get(k, 0) - c for k, c in pay.items()})
                Ub.append(r2); bub.append(base['bub'][ui + 1]); ui += 2
    assert ei == len(base['Eq']) and ui == len(base['Ub'])
    # H constraints on (A1,B1) at cols off..off+2N1
    for T in range(N1):
        rA = {off + z: F(1) for z in range(N1) if z & T == T}
        rM = dict(rA); rM.update({off + N1 + z: F(1) for z in range(N1) if z & T == T})
        if T in s1:
            Eq.append(rA); beq.append(F(s1[T])); Eq.append(rM); beq.append(F(1 if T == 0 else -s1[T]))
        else:
            for r in (rA, rM):
                Ub.append(dict(r)); bub.append(F(1)); Ub.append({k: -c for k, c in r.items()}); bub.append(F(1))
    for v in range(N1):
        if g1[v] == -1:
            Ub.append({off + v: F(-1), off + N1 + v: F(-1)}); bub.append(F(0))
        elif hpp and v != 0:
            Ub.append({off + v: F(1), off + N1 + v: F(1)}); bub.append(F(0))
    if hpp:
        Ub.append({off: F(1), off + N1: F(1)}); bub.append(F(2))
    bounds = base['bounds'] + [((0, None) if g1[z] == 1 else (None, 0)) for z in range(N1)] + \
             [((None, 0) if g1[z] == 1 else (0, None)) for z in range(N1)]
    L = dict(base); L.update(nv=nv, Eq=Eq, beq=beq, Ub=Ub, bub=bub, bounds=bounds, off=off)
    return L
