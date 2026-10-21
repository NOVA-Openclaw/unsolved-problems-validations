#!/usr/bin/env python3
"""
Session 105 — VALIDATE: observationally constrained (MLD, Kz) vs the S104
response surface / Tyka et al. (2026) per-site efficiency spread targets.

S104 showed the two-box toy's per-site efficiency response is effectively
2-lever (MLD short-horizon, w_mix long-horizon) and that matching the Tyka
per-site CESM2-vs-ECCO spread at +-5pt requires observationally pinning the
per-site (MLD, Kz) pair (unconstrained defensible boxes give only ~17% mean
acceptance at +-5pt). Scout (task 760, findings 4875-4880) has now delivered
observational values for the 4 Tyka sites:

  Iceland  61.7N 19.3W: MLD annual mean ~110 m (summer 25-35, winter 500-600);
           Kz background 1e-5..5e-5 m^2/s (topographic 1e-4..1e-3 excluded as
           non-site-mean); upper-pycnocline ventilation tau 2-5 yr.
  Oman     24.2N 59.5E: MLD annual mean ~40-45 m (seasonal 15-80);
           Kz shear-driven 1e-6..5.4e-6, double-diffusive effective ~1e-5;
           tau 1-4 yr (ASHSW subduction).
  Brazil   1.9N 48.2W:  MLD annual mean ~20-25 m (seasonal 10-45);
           Kz 1e-5..3e-5 (topographic 1e-4..4e-4 excluded); tau 1-3 yr (max 5).
  Japan    32.3N 136.5E: MLD annual mean ~70-85 m (summer 15-25, winter
           150-250); Kz 5e-5..1e-4 (Tokara/Izu spikes excluded); STMW tau 2-5yr.

QUESTION: if BOTH model members are forced to live inside the observational
(MLD, Kz) box, can the toy still generate the Tyka inter-model spread — i.e.
does observational pinning deliver the +-5pt magnitude match, or does it
collapse the achievable spread below the Tyka envelope (=> the inter-model
spread is driven by parameter values observations exclude, and/or a 3rd
structural axis such as advective dilution)?

MAPPING DECISIONS (documented, both interpretations run where ambiguous):
  (M1) PRIMARY — Kz-based, S104 convention EXACTLY:
       w_mix(m/hr) = Kz(m^2/s) / dz(m) * 3600, dz = 50 m.
       MLD box = ANNUAL-MEAN climatology +- criterion/climatology uncertainty
       (the toy has no seasonal cycle; annual mean is the like-for-like value).
  (M2) ALT — tau-based: w_mix = H_s / tau_vent, using Scout's ventilation
       timescales. tau_vent includes isopycnal/advective ventilation the toy
       lumps into w_mix, so M2 is an UPPER bound on effective exchange. At
       Oman M1 and M2 disagree by ~1 order of magnitude (diapycnal Kz is tiny,
       ventilation is fast because it is advective) — genuinely ambiguous, so
       both are reported rather than silently picking one.
  (M3) ALT — SEASONAL-ENVELOPE MLD box (full summer-min..winter-max span) as a
       structural sensitivity. Iceland winter 500-600 m exceeds the toy's
       H_d = 500 m deep box, so its envelope is CAPPED at 300 m (S104 grid max)
       and flagged: an annual-mean toy structurally cannot represent deep
       winter convection.
  Winter-weighted effective MLD (Iceland: (3mo*30 + 3mo*550 + 6mo*110)/12
  ~ 200 m) is reported as a point diagnostic — notable because S103's
  Iceland ECCO calibration used exactly 200 m.

Carbonate chemistry + two-box physics + Newton [H+] solver reused EXACTLY from
session-104 (which is exactly S103's physics; Newton==bisection to 2.6e-12).
Base (dTA=0) run skipped by the same proof as S104 (zero drift at baseline).

Targets and conventions from S103: spread = |a-b|/mean*100 at 1/3/7/15 yr;
site match = correct ordering AND >=3/4 horizons within tolerance; tolerances
+-10pt (S103 headline) and +-5pt (the stricter gate S104 says needs obs
pinning).
"""
import numpy as np
import time

# =====================================================================
# CARBONATE CHEMISTRY — constants copied EXACTLY from session-103/104
# =====================================================================
K0 = 3.3e-2
K1 = 10**(-5.94)
K2 = 10**(-9.10)
KB = 10**(-8.73)
KW = 10**(-13.60)
S = 35.0
BT = 4.16e-4 * S / 35.0


def alk_of_h(h, DIC):
    denom = h * h + K1 * h + K1 * K2
    hco3 = DIC * K1 * h / denom
    co3 = DIC * K1 * K2 / denom
    boh4 = BT * KB / (KB + h)
    oh = KW / h
    return hco3 + 2 * co3 + boh4 + oh - h


def dalk_dh(h, DIC):
    denom = h * h + K1 * h + K1 * K2
    dden = 2 * h + K1
    dhco3 = DIC * K1 * (denom - h * dden) / denom**2
    dco3 = -DIC * K1 * K2 * dden / denom**2
    dboh4 = -BT * KB / (KB + h)**2
    doh = -KW / (h * h)
    return dhco3 + 2 * dco3 + dboh4 + doh - 1.0


def solve_h_newton(DIC, TA, h0):
    h = h0 if (1e-10 < h0 < 1e-6) else 1e-8
    lo, hi = 1e-11, 1e-5
    for _ in range(60):
        f = alk_of_h(h, DIC) - TA
        if abs(f) < 1e-14:
            break
        d = dalk_dh(h, DIC)
        step = f / d if d != 0 else 0.0
        hn = h - step
        if not (lo < hn < hi):
            if alk_of_h(lo, DIC) - TA > 0:
                lo, hi = hi, lo
            mid = np.sqrt(abs(lo * hi))
            fm = alk_of_h(mid, DIC) - TA
            if (alk_of_h(lo, DIC) - TA) * fm <= 0:
                hi = mid
            else:
                lo = mid
            hn = mid
        if abs(hn - h) < 1e-16:
            h = hn
            break
        h = hn
    return h


def solve_h_bisect(DIC, TA):
    lo, hi = 10**(-10.0), 10**(-6.0)
    flo = alk_of_h(lo, DIC) - TA
    for _ in range(80):
        mid = np.sqrt(lo * hi)
        fm = alk_of_h(mid, DIC) - TA
        if flo * fm <= 0:
            hi = mid
        else:
            lo = mid
            flo = fm
    return np.sqrt(lo * hi)


def pco2_uatm_h(DIC, h):
    denom = h * h + K1 * h + K1 * K2
    co2 = DIC * h * h / denom
    return (co2 / K0) * 1e6


TA0 = 2300e-6
lo, hi = 1800e-6, 2300e-6
for _ in range(80):
    mid = 0.5 * (lo + hi)
    hmid = solve_h_bisect(mid, TA0)
    if pco2_uatm_h(mid, hmid) > 420.0:
        hi = mid
    else:
        lo = mid
DIC0 = 0.5 * (lo + hi)
H0_BASE = solve_h_bisect(DIC0, TA0)

pco2_atm = 420e-6
kw = 0.05
H_d = 500.0
YEARS = 15.0
HOURS = int(YEARS * 365 * 24)
DT = 6.0
YEARS_LIST = [1, 3, 7, 15]
HORIZONS = [y * 365 for y in YEARS_LIST]


def run_twobox_eta(MLD, w_mix, dTA=10e-6, want_days=None):
    H_s = MLD
    n = int(HOURS / DT)
    DIC_s = DIC0
    DIC_d = DIC0
    TA_s = TA0 + dTA
    TA_d = TA0
    h_s = H0_BASE
    want = sorted(want_days) if want_days is not None else list(HORIZONS)
    out = {}
    wi = 0
    for i in range(n):
        h_s = solve_h_newton(DIC_s, TA_s, h_s)
        pco = pco2_uatm_h(DIC_s, h_s) * 1e-6
        gas = (kw / H_s) * K0 * (pco2_atm - pco)
        mix_dic_s = (w_mix / H_s) * (DIC_d - DIC_s)
        mix_dic_d = (w_mix / H_d) * (DIC_s - DIC_d)
        mix_ta_s = (w_mix / H_s) * (TA_d - TA_s)
        mix_ta_d = (w_mix / H_d) * (TA_s - TA_d)
        DIC_s += (gas + mix_dic_s) * DT
        DIC_d += (mix_dic_d) * DT
        TA_s += (mix_ta_s) * DT
        TA_d += (mix_ta_d) * DT
        day = (i * DT + DT) / 24.0
        while wi < len(want) and day >= want[wi]:
            inv = (DIC_s - DIC0) * H_s + (DIC_d - DIC0) * H_d
            out[want[wi]] = (inv / H_s) / dTA
            wi += 1
        if wi >= len(want):
            break
    inv = (DIC_s - DIC0) * H_s + (DIC_d - DIC0) * H_d
    for w in want:
        out.setdefault(w, (inv / H_s) / dTA)
    return out


def kz_to_wmix(Kz, dz=50.0):
    """S103/S104 convention EXACTLY: w_mix(m/hr) = Kz(m^2/s)/dz(m)*3600."""
    return Kz / dz * 3600.0


def tau_to_wmix(H_s, tau_yr):
    """M2 alternative: w_mix(m/hr) = H_s / tau, tau in hours."""
    return H_s / (tau_yr * 365.0 * 24.0)


def spread(a, b):
    return abs(a - b) / ((a + b) / 2.0) * 100.0


# =====================================================================
# OBSERVATIONAL SITE CONSTRAINTS  (Scout, task 760, findings 4875-4880)
# =====================================================================
# mld_annual: (min, mean, max) annual-mean climatology band (criterion/
#             climatology uncertainty around the reported mean)
# mld_seasonal: (summer-min, annual-mean, winter-max[capped]) envelope
# kz: (min, max) site-mean background band, topographic hotspots excluded
# tau_yr: (min, max) upper-pycnocline ventilation timescale
# target/order: Tyka spread targets + model ordering, from S103
SITES = {
    "Iceland/Norway": {
        "finding": 4876,
        "mld_annual": (90.0, 110.0, 130.0),
        "mld_seasonal": (30.0, 110.0, 300.0),   # winter 500-600 CAPPED at 300, flagged
        "mld_cap_note": "winter MLD 500-600 m exceeds H_d=500; capped at 300 m",
        "mld_winterweighted": 200.0,            # (3*30+3*550+6*110)/12
        "kz": (1.0e-5, 5.0e-5),
        "tau_yr": (2.0, 5.0),
        "target": {1: 22.0, 3: 24.0, 7: 25.0, 15: 22.0},
        "order": "CESM2<ECCO",
    },
    "Oman": {
        "finding": 4877,
        "mld_annual": (35.0, 42.5, 50.0),
        "mld_seasonal": (15.0, 42.5, 80.0),
        "mld_cap_note": None,
        "mld_winterweighted": None,
        "kz": (1.0e-6, 1.0e-5),                 # shear 1e-6..5.4e-6; DD effective ~1e-5
        "tau_yr": (1.0, 4.0),
        "target": {1: 48.0, 3: 42.0, 7: 33.0, 15: 25.0},
        "order": "CESM2<ECCO",
    },
    "Brazil": {
        "finding": 4878,
        "mld_annual": (18.0, 22.5, 28.0),
        "mld_seasonal": (10.0, 22.5, 45.0),
        "mld_cap_note": None,
        "mld_winterweighted": None,
        "kz": (1.0e-5, 3.0e-5),
        "tau_yr": (1.0, 3.0),
        "target": {1: 10.0, 3: 12.0, 7: 12.0, 15: 10.0},
        "order": "small",                        # S104 convention: ordering not binding
    },
    "Japan/Kuroshio": {
        "finding": 4879,
        "mld_annual": (65.0, 77.5, 90.0),
        "mld_seasonal": (20.0, 77.5, 250.0),
        "mld_cap_note": None,
        "mld_winterweighted": 93.75,             # (3*20+3*200+6*77.5)/12
        "kz": (5.0e-5, 1.0e-4),
        "tau_yr": (2.0, 5.0),
        "target": {1: 12.0, 3: 14.0, 7: 14.0, 15: 12.0},
        "order": "ECCO<CESM2",
    },
}

# S103 calibrated pairs, for containment check against observations
S103_CAL = {
    "Iceland/Norway": {"ECCO": (200.0, 2.5e-5), "CESM2": (280.0, 3.5e-5)},
    "Oman":           {"ECCO": (25.0, 1.0e-5), "CESM2": (55.0, 4.0e-5)},
    "Brazil":         {"ECCO": (18.0, 2.0e-5), "CESM2": (22.0, 2.5e-5)},
    "Japan/Kuroshio": {"ECCO": (85.0, 3.5e-5), "CESM2": (65.0, 2.0e-5)},
}

TYKA_SPREAD_RANK = ["Oman", "Iceland/Norway", "Japan/Kuroshio", "Brazil"]

# =====================================================================
# SANITY
# =====================================================================
t_start = time.time()
print("=" * 74)
print("SESSION 105 — OBS-CONSTRAINED (MLD,Kz) VALIDATE vs S104/Tyka  [VALIDATE]")
print("=" * 74)
print(f"Baseline DIC0={DIC0*1e6:.2f} umol/kg  pCO2={pco2_uatm_h(DIC0, H0_BASE):.4f} uatm")
assert abs(pco2_uatm_h(DIC0, H0_BASE) - 420.0) < 1e-3
anchor = run_twobox_eta(200.0, kz_to_wmix(2.5e-5))
print(f"S103/S104 anchor Iceland/ECCO eta@1/3/7/15 = "
      f"{anchor[365]:.4f}/{anchor[3*365]:.4f}/{anchor[7*365]:.4f}/{anchor[15*365]:.4f}"
      f"  (expected 0.1176/0.2860/0.4638/0.5848)")
assert abs(anchor[365] - 0.1176) < 5e-4 and abs(anchor[15 * 365] - 0.5848) < 5e-4
print("Anchor reproduced: PASS")

# =====================================================================
# HELPERS
# =====================================================================
def grid_etas(mld_pts, wmix_pts):
    """etas for every (MLD, w_mix) grid point -> list of dicts."""
    pts = []
    for m in mld_pts:
        for w in wmix_pts:
            e = run_twobox_eta(m, w)
            pts.append({"MLD": m, "w": w, "eta": {y: e[y * 365] for y in YEARS_LIST}})
    return pts


def max_spread_per_horizon(pts):
    out = {}
    for y in YEARS_LIST:
        vals = [p["eta"][y] for p in pts]
        out[y] = spread(min(vals), max(vals))
    return out


def acceptance(pts, cfg):
    """S104 acceptance convention over ordered pairs (a=ECCO, b=CESM2) drawn
    from the SAME observational box: ordering + >=3/4 horizons within tol."""
    total = ok10 = ok5 = order_ok_count = 0
    for a in pts:
        for b in pts:
            total += 1
            ea = a["eta"]
            eb = b["eta"]
            if cfg["order"] == "CESM2<ECCO":
                ord_ok = all(eb[y] < ea[y] for y in YEARS_LIST)
            elif cfg["order"] == "ECCO<CESM2":
                ord_ok = all(ea[y] < eb[y] for y in YEARS_LIST)
            else:
                ord_ok = True
            if ord_ok:
                order_ok_count += 1
            d10 = sum(1 for y in YEARS_LIST
                      if abs(spread(ea[y], eb[y]) - cfg["target"][y]) <= 10.0)
            d5 = sum(1 for y in YEARS_LIST
                     if abs(spread(ea[y], eb[y]) - cfg["target"][y]) <= 5.0)
            if ord_ok and d10 >= 3:
                ok10 += 1
            if ord_ok and d5 >= 3:
                ok5 += 1
    return total, order_ok_count / total, ok10 / total, ok5 / total


def horizon_match_table(maxspread, target):
    """Per-horizon: is the target reachable within tol given achievable
    spread range [0, max]? matched iff target - tol <= max."""
    rows = {}
    for y in YEARS_LIST:
        rows[y] = {
            "max": maxspread[y],
            "target": target[y],
            "m10": target[y] - 10.0 <= maxspread[y],
            "m5": target[y] - 5.0 <= maxspread[y],
        }
    return rows


def npts(lohimean, n=4):
    lo, mid, hi = lohimean
    return np.unique(np.concatenate([np.linspace(lo, hi, n), [mid]]))


def kzpts(kzrange, n=4):
    return np.geomspace(kzrange[0], kzrange[1], n)


# =====================================================================
# (1) PRIMARY M1: annual-mean MLD box x Kz box (S104 mapping)
# =====================================================================
print("\n" + "=" * 74)
print("(1) PRIMARY (M1): annual-mean MLD box x observational Kz box")
print("    mapping: w_mix = Kz/50*3600  (S103/S104 convention)")
print("=" * 74)
results_m1 = {}
for site, cfg in SITES.items():
    mlds = npts(cfg["mld_annual"])
    kzs = kzpts(cfg["kz"])
    wms = [kz_to_wmix(k) for k in kzs]
    pts = grid_etas(mlds, wms)
    ms = max_spread_per_horizon(pts)
    tot, fo, f10, f5 = acceptance(pts, cfg)
    hm = horizon_match_table(ms, cfg["target"])
    results_m1[site] = {"pts": pts, "maxspread": ms, "accept": (tot, fo, f10, f5),
                        "hmatch": hm}
    # center-point eta
    ec = run_twobox_eta(cfg["mld_annual"][1],
                        kz_to_wmix(np.sqrt(cfg["kz"][0] * cfg["kz"][1])))
    print(f"\n{site}  [finding {cfg['finding']}]")
    print(f"  MLD box {cfg['mld_annual'][0]:.0f}..{cfg['mld_annual'][2]:.0f} m "
          f"(mean {cfg['mld_annual'][1]:.0f});  Kz box "
          f"{cfg['kz'][0]:.1e}..{cfg['kz'][1]:.1e} m2/s")
    print(f"  center-point eta@1/3/7/15yr = "
          + "/".join(f"{ec[y*365]:.3f}" for y in YEARS_LIST))
    print(f"  {'horizon':<8}{'max spread':>11}{'target':>9}{'match+-10':>11}{'match+-5':>10}")
    for y in YEARS_LIST:
        r = hm[y]
        print(f"  {y:>4}yr  {r['max']:>10.1f}% {r['target']:>8.1f}%"
              f"{str(r['m10']):>11}{str(r['m5']):>10}")
    print(f"  acceptance over {tot} ordered pairs: ordering {fo:.1%}, "
          f"+-10pt {f10:.1%}, +-5pt {f5:.1%}")

# =====================================================================
# (2) ALT M2: tau-based mapping (w_mix = H_s/tau)
# =====================================================================
print("\n" + "=" * 74)
print("(2) ALT (M2): ventilation-timescale mapping w_mix = H_s/tau")
print("    (upper bound on effective exchange; includes advective ventilation)")
print("=" * 74)
results_m2 = {}
for site, cfg in SITES.items():
    mlds = npts(cfg["mld_annual"])
    taus = np.linspace(cfg["tau_yr"][0], cfg["tau_yr"][1], 4)
    pts = []
    for m in mlds:
        for t in taus:
            w = tau_to_wmix(m, t)
            e = run_twobox_eta(m, w)
            pts.append({"MLD": m, "w": w, "eta": {y: e[y * 365] for y in YEARS_LIST}})
    ms = max_spread_per_horizon(pts)
    tot, fo, f10, f5 = acceptance(pts, cfg)
    hm = horizon_match_table(ms, cfg["target"])
    results_m2[site] = {"maxspread": ms, "accept": (tot, fo, f10, f5), "hmatch": hm}
    # Kz-equivalent of the tau-derived w_mix range (at mean MLD)
    w_lo = tau_to_wmix(cfg["mld_annual"][1], cfg["tau_yr"][1])
    w_hi = tau_to_wmix(cfg["mld_annual"][1], cfg["tau_yr"][0])
    kz_lo = w_lo * 50.0 / 3600.0
    kz_hi = w_hi * 50.0 / 3600.0
    ratio_note = ""
    if kz_lo > cfg["kz"][1] or kz_hi < cfg["kz"][0]:
        ratio_note = "  << MAPPINGS DISJOINT: tau-implied Kz outside obs Kz box"
    print(f"\n{site}: tau {cfg['tau_yr'][0]:.0f}-{cfg['tau_yr'][1]:.0f} yr -> "
          f"Kz-equiv {kz_lo:.1e}..{kz_hi:.1e} m2/s "
          f"(obs Kz {cfg['kz'][0]:.1e}..{cfg['kz'][1]:.1e}){ratio_note}")
    for y in YEARS_LIST:
        r = hm[y]
        print(f"  {y:>4}yr  max {r['max']:>6.1f}%  target {r['target']:>5.1f}%"
              f"  m10={str(r['m10']):<5}  m5={str(r['m5'])}")
    print(f"  acceptance: ordering {fo:.1%}, +-10pt {f10:.1%}, +-5pt {f5:.1%}")

# =====================================================================
# (3) ALT M3: seasonal-envelope MLD box (structural sensitivity)
# =====================================================================
print("\n" + "=" * 74)
print("(3) ALT (M3): seasonal-envelope MLD box x obs Kz (structural sensitivity)")
print("=" * 74)
results_m3 = {}
for site, cfg in SITES.items():
    mlds = npts(cfg["mld_seasonal"], n=3)
    kzs = kzpts(cfg["kz"], n=3)
    wms = [kz_to_wmix(k) for k in kzs]
    pts = grid_etas(mlds, wms)
    ms = max_spread_per_horizon(pts)
    tot, fo, f10, f5 = acceptance(pts, cfg)
    hm = horizon_match_table(ms, cfg["target"])
    results_m3[site] = {"maxspread": ms, "accept": (tot, fo, f10, f5), "hmatch": hm}
    cap = f"  [{cfg['mld_cap_note']}]" if cfg["mld_cap_note"] else ""
    print(f"\n{site}: MLD envelope {cfg['mld_seasonal'][0]:.0f}.."
          f"{cfg['mld_seasonal'][2]:.0f} m{cap}")
    for y in YEARS_LIST:
        r = hm[y]
        print(f"  {y:>4}yr  max {r['max']:>6.1f}%  target {r['target']:>5.1f}%"
              f"  m10={str(r['m10']):<5}  m5={str(r['m5'])}")
    print(f"  acceptance: ordering {fo:.1%}, +-10pt {f10:.1%}, +-5pt {f5:.1%}")

# Winter-weighted Iceland diagnostic
ww = SITES["Iceland/Norway"]["mld_winterweighted"]
eww = run_twobox_eta(ww, kz_to_wmix(2.5e-5))
print(f"\nIceland winter-weighted effective MLD diagnostic: {ww:.0f} m "
      f"(S103 ECCO used 200 m) -> eta = "
      + "/".join(f"{eww[y*365]:.3f}" for y in YEARS_LIST))

# =====================================================================
# (4) S103 calibration containment vs observational boxes
# =====================================================================
print("\n" + "=" * 74)
print("(4) S103 CALIBRATED PAIRS vs OBSERVATIONAL BOXES (containment)")
print("=" * 74)
print(f"{'site':<16}{'member':<7}{'MLD':>6}{'Kz':>9}"
      f"{'in ann-mean box?':>18}{'in seasonal box?':>18}{'Kz in obs box?':>16}")
for site, mem in S103_CAL.items():
    cfg = SITES[site]
    for name, (m, k) in mem.items():
        in_ann = cfg["mld_annual"][0] <= m <= cfg["mld_annual"][2]
        in_sea = cfg["mld_seasonal"][0] <= m <= cfg["mld_seasonal"][2]
        # note: Iceland seasonal cap 300 also true for the uncapped 600 check:
        if site == "Iceland/Norway":
            in_sea = 25.0 <= m <= 600.0
        in_kz = cfg["kz"][0] <= k <= cfg["kz"][1]
        print(f"{site:<16}{name:<7}{m:>6.0f}{k:>9.1e}"
              f"{str(in_ann):>18}{str(in_sea):>18}{str(in_kz):>16}")

# =====================================================================
# (5) INTER-SITE ORDERING (by max achievable spread, M1 primary)
# =====================================================================
print("\n" + "=" * 74)
print("(5) INTER-SITE SPREAD ORDERING")
print("=" * 74)
for label, res in [("M1 annual-mean", results_m1), ("M2 tau-based", results_m2),
                   ("M3 seasonal", results_m3)]:
    mean_ms = {s: np.mean([res[s]["maxspread"][y] for y in YEARS_LIST]) for s in SITES}
    rank = sorted(SITES, key=lambda s: -mean_ms[s])
    ok = rank == TYKA_SPREAD_RANK
    print(f"{label:<16}: " + " > ".join(f"{s}({mean_ms[s]:.0f}%)" for s in rank)
          + f"   Tyka-order match: {ok}")
print(f"{'Tyka':<16}: " + " > ".join(TYKA_SPREAD_RANK))

# =====================================================================
# (6) VERDICT
# =====================================================================
print("\n" + "=" * 74)
print("SESSION 105 VERDICT INPUTS")
print("=" * 74)
print(f"{'site':<16}{'M1 +-10':>9}{'M1 +-5':>8}{'M2 +-10':>9}{'M2 +-5':>8}"
      f"{'M3 +-10':>9}{'M3 +-5':>8}")
for s in SITES:
    a1 = results_m1[s]["accept"]
    a2 = results_m2[s]["accept"]
    a3 = results_m3[s]["accept"]
    print(f"{s:<16}{a1[2]:>9.1%}{a1[3]:>8.1%}{a2[2]:>9.1%}{a2[3]:>8.1%}"
          f"{a3[2]:>9.1%}{a3[3]:>8.1%}")
mean5_m1 = np.mean([results_m1[s]["accept"][3] for s in SITES])
mean10_m1 = np.mean([results_m1[s]["accept"][2] for s in SITES])
print(f"\nM1 mean acceptance: +-10pt {mean10_m1:.1%}, +-5pt {mean5_m1:.1%}")
print(f"(S104 unconstrained-defensible-box baseline: +-10pt 47.5%, +-5pt 16.6%)")

# residuals: target minus max achievable, per site (M1), flag Oman/Iceland
print("\nResiduals (Tyka target - max achievable spread, M1, per horizon; "
      "positive = box CANNOT reach target):")
for s in SITES:
    resid = {y: SITES[s]["target"][y] - results_m1[s]["maxspread"][y]
             for y in YEARS_LIST}
    print(f"  {s:<16}: " + "  ".join(f"{y}yr:{resid[y]:+6.1f}pt" for y in YEARS_LIST))

print(f"\nTotal wall time: {time.time()-t_start:.1f}s")
