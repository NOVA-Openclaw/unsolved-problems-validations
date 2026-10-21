#!/usr/bin/env python3
"""S308 VALIDATE of S307 (Theorem PV.1-R). Fresh code, seed 308, exact Fractions.
Does not import or reuse s307_*.py.
d = 8 cube: pairs i=0..3, elements (i,s), s in {+1,-1}; tau in {+1,-1}^4; S_tau = {(i,tau_i)}.
"""
import itertools, random, sys, math
from fractions import Fraction as Fr
import numpy as np

SEED = 308
random.seed(SEED)
NPR = np.random.default_rng(SEED)
M = 4
N = 48
TAUS = list(itertools.product((1, -1), repeat=M))
ELEMS = [(i, s) for i in range(M) for s in (1, -1)]
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}", flush=True)


def p(beta, tau, j):
    i, s = j
    return (1 + beta) / 8 if tau[i] == s else (1 - beta) / 8


def ham(t1, t2):
    return sum(a != b for a, b in zip(t1, t2))


def PS(beta, tau, tp):  # P_tau(S_tp)
    return (1 + beta) / 2 - Fr(ham(tau, tp)) * beta / M


# ---------------- exact z-law ----------------
# z_i in {(+1,strong),(+1,weak),(-1,weak),(-1,strong)}; D = k+ - k-, ties -> +; strong iff |D| >= c0
ZV = [(1, True), (1, False), (-1, False), (-1, True)]


def zi_of(kp, km, c0):
    D = kp - km
    sg = 1 if D >= 0 else -1
    return (sg, abs(D) >= c0)


def z_law(beta, tau, c0):
    """exact law of z = (z_0..z_3) under P_tau^n (multinomial over 8 elems)."""
    fact = [math.factorial(k) for k in range(N + 1)]
    # per pair: q(Ni, zi | tau_i): sum over kp of p+^kp p-^km / (kp! km!)
    pair = {}
    for ti in (1, -1):
        pp = p(beta, (ti,) * M, (0, 1))  # prob of (i,+)
        pm = p(beta, (ti,) * M, (0, -1))
        tab = {}
        for Ni in range(N + 1):
            row = {zv: Fr(0) for zv in ZV}
            for kp in range(Ni + 1):
                km = Ni - kp
                row[zi_of(kp, km, c0)] += pp ** kp * pm ** km / (fact[kp] * fact[km])
            tab[Ni] = row
        pair[ti] = tab
    # DP over pairs: state (used, z-prefix) -> weight
    dp = {(0, ()): Fr(1)}
    for i in range(M):
        nd = {}
        for (used, zp), wgt in dp.items():
            rng = range(N - used + 1) if i < M - 1 else [N - used]
            for Ni in rng:
                row = pair[tau[i]][Ni]
                for zv, q in row.items():
                    if q == 0:
                        continue
                    key = (used + Ni, zp + (zv,))
                    nd[key] = nd.get(key, Fr(0)) + wgt * q
        dp = nd
    law = {}
    for (used, zp), wgt in dp.items():
        law[zp] = law.get(zp, Fr(0)) + wgt * fact[N]
    tot = sum(law.values())
    assert tot == 1, tot
    return law


def sig(z):
    return tuple(zv[0] for zv in z)


# ---------------- outputs ----------------
# atom = (mass, ell, kind, dev) ; kind 'S' => f = 1_{S_visit} + dev ; 'Z' => f = 0
# dev = None or (j, amt) with amt = P_visit-mass of the deviation (removal if j in S_visit, addition otherwise)

def atom_vals(beta, atom, visit, tau):
    """returns (qual_test_value, target_full_on_(tau,[d]), target_on_(tau,S_tau) [only meaningful if visit==tau])"""
    mass, ell, kind, dev = atom
    a = (1 + beta) / 2
    if kind == 'Z':
        return (PS(beta, visit, visit), Fr(0), Fr(0))
    test = Fr(0)
    full = PS(beta, tau, visit)
    if dev is not None:
        j, amt = dev
        ratio = p(beta, tau, j) / p(beta, visit, j)
        test = amt
        inS = (visit[j[0]] == j[1])
        full += (-amt if inS else amt) * ratio
    return (test, full, a - test)


def make_scheme(beta, c0, rnd):
    thr = beta * (1 - beta) / 8
    w = thr * Fr(rnd.randint(32, 63), 64)
    a = (1 + beta) / 2
    lam0 = Fr(rnd.randint(0, 20), 500)
    lam1 = Fr(rnd.randint(0, 40), 500)
    nu = Fr(rnd.randint(0, 25), 500)
    eta = Fr(rnd.randint(0, 30), 500)
    nh = rnd.randint(2, 3)
    honest = []
    for _ in range(nh):
        u = Fr(rnd.randint(0, 63), 64)
        r = Fr(rnd.randint(0, 80), 64)  # up to 1.25: slightly unsound atoms
        honest.append((u, r, rnd.randrange(8)))
    table = {}  # (z, visit) -> list of atoms
    for z in itertools.product(ZV, repeat=M):
        sh = sig(z)
        weak = [i for i in range(M) if not z[i][1]]
        strong = [i for i in range(M) if z[i][1]]
        out = {tp: [] for tp in TAUS}
        # honest atoms at visit sh
        hm = (1 - nu) / nh
        for (u, r, jidx) in honest:
            amt = r * u * w
            j = ELEMS[jidx]
            out[sh].append((hm, a - u * w, 'S', (j, amt) if amt > 0 else None))
        # hedges at weak-only neighbours
        C = [t for t in TAUS if all(t[i] == sh[i] for i in strong)]
        for tp in C:
            if tp == sh:
                continue
            ell = min(PS(beta, t2, tp) for t2 in C)
            out[tp].append((eta, ell, 'S', None))
        # lies
        lam = lam0 + lam1 * len(weak) / M
        rivals = [t for t in TAUS if t != sh]
        k = rnd.randint(1, 4)
        chosen = rnd.sample(rivals, k)
        for idx, tp in enumerate(chosen):
            if idx % 2 == 0:
                out[tp].append((lam / k, a, 'S', None))  # full lie, policy test 0
            else:
                js = [e for e in ELEMS if tp[e[0]] != e[1]]
                j = rnd.choice(js)
                out[tp].append((lam / k, a - w, 'S', (j, w)))  # boundary lie, test = w exactly
        for tp in TAUS:
            used = sum(at[0] for at in out[tp])
            assert used <= 1
            if used < 1:
                out[tp].append((1 - used, Fr(0), 'Z', None))
            table[(z, tp)] = out[tp]
    return dict(beta=beta, w=w, a=a, table=table, c0=c0)


def coin_measures(S, z, tau):
    beta, w, a = S['beta'], S['w'], S['a']
    H = {}
    f = {}
    for tp in TAUS:
        h = Fr(0)
        fl = Fr(0)
        for at in S['table'][(z, tp)]:
            test, full, _ = atom_vals(beta, at, tp, tau)
            ell = at[1]
            if ell >= a - w and test <= w:
                h += at[0]
            if ell > full:
                fl += at[0]
        H[tp] = h
        f[tp] = fl
    t = Fr(0)
    f2 = Fr(0)
    for at in S['table'][(z, tau)]:
        test, full, tS = atom_vals(beta, at, tau, tau)
        if at[1] >= a - w:
            t += at[0]
        if at[2] == 'Z':
            tS = Fr(0)
        if at[1] > tS:
            f2 += at[0]
    return H, f, t, f2


def decode(H):
    mx = max(H.values())
    arg = [t for t in TAUS if H[t] == mx]
    return arg[0] if len(arg) == 1 else None


def main():
    configs = [(Fr(1, 2), 4), (Fr(1, 4), 3)]
    laws = {}
    for beta, c0 in configs:
        for tau in TAUS:
            laws[(beta, tau)] = z_law(beta, tau, c0)
    print("z-laws computed", flush=True)

    NS = 12  # schemes per beta
    n1_cells = n1_pos = n1_viol = 0
    n2_viol = 0
    n3_viol = 0
    nonvac_w = Fr(0)
    nonvac_wtot = Fr(0)
    nonvac_cnt = cells3 = 0
    n4_viol = 0
    min_bounds = []
    schemes = []
    for beta, c0 in configs:
        for sidx in range(NS):
            S = make_scheme(beta, c0, random)
            schemes.append(S)
            worst = Fr(2)
            for tau in TAUS:
                law = laws[(beta, tau)]
                Eg = EF = Et = Ef2 = succ = Fr(0)
                for z, pz in law.items():
                    H, f, t, f2 = coin_measures(S, z, tau)
                    g = H[tau]
                    F = max(f.values())
                    for tp in TAUS:
                        if tp == tau:
                            continue
                        n1_cells += 1
                        if H[tp] > 0:
                            n1_pos += 1
                        if H[tp] > f[tp]:
                            n1_viol += 1
                    if g < t - f2:
                        n2_viol += 1
                    ok = 1 if decode(H) == tau else 0
                    cells3 += 1
                    if ok < g - F:
                        n3_viol += 1
                    if g - F > 0:
                        nonvac_cnt += 1
                        nonvac_w += pz
                    nonvac_wtot += pz
                    Eg += pz * g; EF += pz * F; Et += pz * t; Ef2 += pz * f2; succ += pz * ok
                bound = 1 - (1 - Et) - Ef2 - EF
                if not (succ >= Eg - EF >= bound):
                    n4_viol += 1
                worst = min(worst, bound)
            min_bounds.append((beta, sidx, worst))
            print(f" scheme beta={beta} #{sidx} w/thr={float(S['w']/(beta*(1-beta)/8)):.3f} min_tau bound={float(worst):.4f}", flush=True)

    check("N1 H(x,tau') <= f_tau(x,tau') off-diagonal (PV.R3)", n1_viol == 0 and n1_pos >= 100000,
          f"cells={n1_cells} H>0 cells={n1_pos} violations={n1_viol}")
    check("N2 g >= t - f2 pointwise (PV.R2)", n2_viol == 0, f"cells={cells3} violations={n2_viol}")
    share_w = nonvac_w / nonvac_wtot
    check("N3a 1{unique argmax H = tau} >= g - F pointwise (PV.R4)", n3_viol == 0, f"cells={cells3} violations={n3_viol}")
    check("N3b non-vacuous share >= 50% (probability-weighted)", share_w >= Fr(1, 2),
          f"weighted={float(share_w):.4f} unweighted={nonvac_cnt}/{cells3}={nonvac_cnt/cells3:.4f}")
    check("N4a success >= Eg-EF >= 1-delta-a2-a3 every (scheme,tau)", n4_viol == 0, f"cases={len(schemes)*16} violations={n4_viol}")
    mb_half = [x[2] for x in min_bounds if x[0] == Fr(1, 2)]
    mb_q = [x[2] for x in min_bounds if x[0] == Fr(1, 4)]
    check("N4b every scheme non-vacuous (min_tau bound >= 0.3)", min(x[2] for x in min_bounds) >= Fr(3, 10),
          f"beta=1/2 min bounds in [{float(min(mb_half)):.3f},{float(max(mb_half)):.3f}]; beta=1/4 in [{float(min(mb_q)):.3f},{float(max(mb_q)):.3f}]")
    check("N4c (diagnostic) every beta=1/2 scheme non-vacuous (>=0.3)", min(mb_half) >= Fr(3, 10), "")

    # ---------------- N5: Monte Carlo Fubini / W-blind check ----------------
    print("== N5 Monte Carlo ==", flush=True)
    R = 20000
    probs_idx = ELEMS
    n5_ok = True
    law_ok = True
    for S in schemes[:3]:
        beta = S['beta']
        for tau in [TAUS[0], TAUS[5], TAUS[15]]:
            law = laws[(beta, tau)]
            pv = np.array([float(p(beta, tau, e)) for e in ELEMS])
            counts = NPR.multinomial(N, pv, size=R)
            # exact EF and sigma*
            cache = {}
            EF = Fr(0)
            for z, pz in law.items():
                H, f, t, f2 = coin_measures(S, z, tau)
                F = max(f.values())
                sstar = next(tp for tp in TAUS if f[tp] == F)
                cache[z] = (sstar,)
                EF += pz * F
            fails = 0
            zc = {}
            for row in counts:
                z = tuple(zi_of(int(row[2 * i]), int(row[2 * i + 1]), S['c0']) for i in range(M))
                zc[z] = zc.get(z, 0) + 1
                sstar = cache[z][0]
                atoms = S['table'][(z, sstar)]
                uu = NPR.random()
                acc = 0.0
                chosen = atoms[-1]
                for at in atoms:
                    acc += float(at[0])
                    if uu < acc:
                        chosen = at
                        break
                _, full, _ = atom_vals(beta, chosen, sstar, tau)
                if chosen[1] > full:
                    fails += 1
            ef = float(EF)
            sd = math.sqrt(max(ef * (1 - ef), 1e-12) / R)
            dev = abs(fails / R - ef)
            if dev > 4 * sd + 1e-9:
                n5_ok = False
            maxdev = 0.0
            for z, pz in law.items():
                pzf = float(pz)
                sdz = math.sqrt(max(pzf * (1 - pzf), 1e-12) / R)
                dz = abs(zc.get(z, 0) / R - pzf)
                maxdev = max(maxdev, dz / sdz if sdz > 0 else 0)
            # max over 256 cells: allow 4.5 sigma (Bonferroni-ish over 256 cells at ~1e-5 each)
            if maxdev > 4.5:
                law_ok = False
            print(f"   beta={beta} tau={tau}: MC fail={fails/R:.4f} exact EF={ef:.4f} ({dev/sd:.2f} sd); z-law max dev {maxdev:.2f} sd", flush=True)
    check("N5a MC failure of first-argmax W-blind explorer matches exact E F (4 sd)", n5_ok, "")
    check("N5b MC z-law matches exact law (max cell dev <= 4.5 sd)", law_ok, "")

    # ---------------- N6: threshold control ----------------
    beta = Fr(1, 2)
    a = Fr(3, 4)
    tau = (1, 1, 1, 1)
    tp = (-1, 1, 1, 1)
    w = beta * (1 - beta) / 8
    j = (0, 1)
    at = (Fr(1), a - w, 'S', (j, w))
    test, full, _ = atom_vals(beta, at, tp, tau)
    Hq = (at[1] >= a - w and test <= w)
    fail = at[1] > full
    Delta = w / p(beta, tp, j)
    check("N6a equality w=beta(1-beta)/8: fractional rec (Delta=1/2) at Ham-1 rival gives H=1, f=0",
          Hq and not fail and Delta == Fr(1, 2), f"Delta={Delta} ell={at[1]} target={full}")
    # exact LP (fractional knapsack) over continuous f in [0,1]^8 for every (tau, rival):
    # max P_tau(f) s.t. V P_rival(f triangle S_rival) <= w. Greedy: start at f = 1_{S_rival}; each unit of
    # test budget spent adding j outside S_rival gains p_tau(j)/p_rival(j); removing j in S_rival only loses.
    def lpmax(t1, t2, wv):
        best = PS(beta, t1, t2)
        outs = sorted([e for e in ELEMS if t2[e[0]] != e[1]], key=lambda e: -p(beta, t1, e) / p(beta, t2, e))
        budget = wv
        for e in outs:
            take = min(budget, p(beta, t2, e))
            best += take * p(beta, t1, e) / p(beta, t2, e)
            budget -= take
            if budget == 0:
                break
        return best
    eq_hits = 0
    below_ok = True
    for t1 in TAUS:
        for t2 in TAUS:
            if t1 == t2:
                continue
            if lpmax(t1, t2, w) >= a - w and ham(t1, t2) == 1:
                eq_hits += 1
            wv = w - Fr(1, 10**6)
            if lpmax(t1, t2, wv) >= a - wv:
                below_ok = False
    check("N6b exact LP over continuous f: some rival qualifies w/o failing at equality (all Ham-1 pairs)",
          eq_hits == 16 * 4, f"Ham-1 pairs reaching a-w at equality = {eq_hits}/64")
    check("N6c exact LP: at w = thr - 1e-6 no rival (any Ham) qualifies w/o failing", below_ok, "")

    # ---------------- N7: Example PV.R exact ----------------
    print("== N7 Example PV.R ==", flush=True)
    beta = Fr(1, 2)
    a = Fr(3, 4)
    lawEx = {tau: {} for tau in TAUS}
    for tau in TAUS:
        for z, pz in laws[(beta, tau)].items():
            s = sig(z)
            lawEx[tau][s] = lawEx[tau].get(s, Fr(0)) + pz
    eps = {tau: 1 - lawEx[tau].get(tau, Fr(0)) for tau in TAUS}
    print(f"   eps_tau in [{float(min(eps.values())):.5f},{float(max(eps.values())):.5f}]")
    # explicit worst explorer over all U (256 sets) and tau''
    supports = {tau: frozenset((i, tau[i]) for i in range(M)) for tau in TAUS}
    alpha_glob = Fr(0)
    for t2 in TAUS:
        for bits in range(256):
            U = frozenset(e for k, e in enumerate(ELEMS) if bits >> k & 1)
            feas = [k for k in TAUS if supports[k] <= U]
            tot = Fr(0)
            for s, pz in lawEx[t2].items():
                best = Fr(0)
                for k in feas:
                    if k == t2:
                        fl = Fr(0)
                    elif k == s:
                        fl = Fr(1)
                    else:
                        fl = Fr(1, 15)
                    best = max(best, fl)
                tot += pz * best
            alpha_glob = max(alpha_glob, tot)
    closed = max(eps[t] + (1 - eps[t]) / 15 for t in TAUS)
    delta = {t: Fr(14, 15) * eps[t] for t in TAUS}
    dmax = max(delta.values())
    print(f"   global alpha={float(alpha_glob):.5f} closed={float(closed):.5f} delta_max={float(dmax):.5f} eps_max={float(max(eps.values())):.5f}")
    check("N7a alpha exact = max_tau(eps+(1-eps)/15); matches S307 0.23582; 2alpha+delta<1",
          alpha_glob == closed and abs(float(alpha_glob) - 0.23582) < 5e-6 and 2 * alpha_glob + dmax < 1,
          f"2a+d={float(2*alpha_glob+dmax):.5f}")
    # delta exact by enumeration: under E_tau, ell=a iff s==tau or phi_W==tau
    dok = True
    for tau in TAUS:
        dd = Fr(0)
        for s, pz in lawEx[tau].items():
            dd += pz * (0 if s == tau else Fr(14, 15))
        dok = dok and dd == delta[tau]
    check("N7b delta_tau = (14/15) eps_tau exactly", dok, "")
    # fixed coin: alpha_u = 1 and PV.1 decoder 2 qualifiers
    fok = True
    for u in range(15):
        for t2 in TAUS:
            tot = Fr(0)
            for s, pz in lawEx[t2].items():
                rivals = [k for k in TAUS if k != s]
                phi = rivals[u]
                visit = s if s != t2 else phi
                # visiting S_visit on (t2,[d]) with ell = a: fail iff visit != t2
                tot += pz * (1 if visit != t2 else 0)
            fok = fok and tot == 1
        for s in TAUS:
            rivals = [k for k in TAUS if k != s]
            qual = {s, rivals[u]}
            fok = fok and len(qual) == 2
    check("N7c every fixed coin u: alpha_u = 1 exactly; PV.1 decoder has 2 qualifiers at every x (success 0)", fok, "")
    aok = True
    for tau in TAUS:
        succ = lawEx[tau].get(tau, Fr(0))
        # H(x, s)=1, H(x,k)=1/15 -> argmax = s
        aok = aok and succ == 1 - eps[tau] and succ >= 1 - 2 * alpha_glob - dmax
        EF = sum(pz * (Fr(1, 15) if s == tau else Fr(1)) for s, pz in lawEx[tau].items())
        aok = aok and EF == eps[tau] + (1 - eps[tau]) / 15
    check("N7d averaged decoder success = 1-eps >= 1-2alpha-delta; E F = alpha_tau (R1 tight)", aok,
          f"min succ={float(min(1-e for e in eps.values())):.5f} bound={float(1-2*alpha_glob-dmax):.5f}")

    # ---------------- N8: Fano arithmetic ----------------
    s = Fr(1, 2)
    eq64 = (s * 64 / 16 == s * 64 / 32 + 1)
    strict = all(s * d / 16 > s * d / 32 + 1 for d in range(66, 1001, 2))
    c = math.sqrt(0.5 * math.log(2) / 256) / 4
    check("N8 Fano: d=64 equality, even d>=66 strict, c/4=0.0022996", eq64 and strict and abs(c / 4 - 0.0022996) < 5e-8,
          f"c={c:.7f} c/4={c/4:.7f}")

    npass = sum(1 for _, ok in RESULTS if ok)
    print(f"TOTAL {npass} PASS / {len(RESULTS)-npass} FAIL")


if __name__ == "__main__":
    main()
