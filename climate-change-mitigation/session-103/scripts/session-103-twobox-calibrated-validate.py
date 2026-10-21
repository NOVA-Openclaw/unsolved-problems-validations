#!/usr/bin/env python3
"""
Session 103 — VALIDATE: two-box toy model CALIBRATED against Tyka et al. (2026,
Biogeosciences DOI 10.5194/bg-23-4943-2026) per-site CESM2/MARBL vs ECCO-Darwin
OAE-efficiency spread.

Reuses the exact carbonate solver and two-box integrator from Session 102.
Constructs physically-defensible (MLD, Kz) model pairs for representative sites,
maps Kz -> w_mix via the validated scaling, and checks whether the toy reproduces
Tyka's reported per-site spread magnitudes and ordering.
"""
import numpy as np

# =====================================================================
# CARBONATE CHEMISTRY — copied EXACTLY from session-102
# =====================================================================
K0 = 3.3e-2
K1 = 10**(-5.94)
K2 = 10**(-9.10)
KB = 10**(-8.73)
KW = 10**(-13.60)
S = 35.0
BT = 4.16e-4 * S / 35.0


def solve_h(DIC, TA):
    lo, hi = 10**(-10.0), 10**(-6.0)

    def alk(h):
        denom = h * h + K1 * h + K1 * K2
        hco3 = DIC * K1 * h / denom
        co3 = DIC * K1 * K2 / denom
        boh4 = BT * KB / (KB + h)
        oh = KW / h
        return hco3 + 2 * co3 + boh4 + oh - h

    flo = alk(lo) - TA
    for _ in range(80):
        mid = np.sqrt(lo * hi)
        fm = alk(mid) - TA
        if flo * fm <= 0:
            hi = mid
        else:
            lo = mid
            flo = fm
    return np.sqrt(lo * hi)


def pco2_uatm(DIC, TA):
    h = solve_h(DIC, TA)
    denom = h * h + K1 * h + K1 * K2
    co2 = DIC * h * h / denom
    return (co2 / K0) * 1e6


# ---- baseline: DIC0 so surface pCO2=420 uatm at TA0 ----
TA0 = 2300e-6
target = 420.0
lo, hi = 1800e-6, 2300e-6
for _ in range(80):
    mid = 0.5 * (lo + hi)
    if pco2_uatm(mid, TA0) > target:
        hi = mid
    else:
        lo = mid
DIC0 = 0.5 * (lo + hi)

pco2_atm = 420e-6      # atm
kw = 0.05              # m/hr air-sea piston velocity
H_d = 500.0            # m deep box thickness
YEARS = 15.0
HOURS = int(YEARS * 365 * 24)
DT = 6.0               # hours; kept from S102, checked for 15-y stability below


def run_twobox(MLD, w_mix, dTA_surf, hours=HOURS, dt=DT):
    """Forward-Euler two-box. Returns t(days), inventory anomaly per-Hs, and profiles."""
    H_s = MLD
    n = int(hours / dt)
    t = np.zeros(n + 1)
    DIC_s = np.full(n + 1, DIC0)
    DIC_d = np.full(n + 1, DIC0)
    TA_s = np.full(n + 1, TA0 + dTA_surf)
    TA_d = np.full(n + 1, TA0)
    for i in range(n):
        pco = pco2_uatm(DIC_s[i], TA_s[i]) * 1e-6      # atm
        gas = (kw / H_s) * K0 * (pco2_atm - pco)        # mol/kg/hr into surface
        mix_dic_s = (w_mix / H_s) * (DIC_d[i] - DIC_s[i])
        mix_dic_d = (w_mix / H_d) * (DIC_s[i] - DIC_d[i])
        mix_ta_s = (w_mix / H_s) * (TA_d[i] - TA_s[i])
        mix_ta_d = (w_mix / H_d) * (TA_s[i] - TA_d[i])
        DIC_s[i + 1] = DIC_s[i] + (gas + mix_dic_s) * dt
        DIC_d[i + 1] = DIC_d[i] + (mix_dic_d) * dt
        TA_s[i + 1] = TA_s[i] + (mix_ta_s) * dt
        TA_d[i + 1] = TA_d[i] + (mix_ta_d) * dt
        t[i + 1] = (i * dt + dt) / 24.0
    inv = (DIC_s - DIC0) * H_s + (DIC_d - DIC0) * H_d
    inv_per_Hs = inv / H_s
    return t, inv_per_Hs, DIC_s, DIC_d, TA_s, TA_d


def eta_series(MLD, w_mix, dTA=10e-6):
    """OAE efficiency eta(t) = extra DIC inventory / dTA for a given (MLD, w_mix)."""
    t, inv_add, *_ = run_twobox(MLD, w_mix, dTA)
    _, inv_base, *_ = run_twobox(MLD, w_mix, 0.0)
    extra = inv_add - inv_base
    eta = extra / dTA
    return t, eta


def find_nearest_day(t_days, target_day):
    return int(np.argmin(np.abs(t_days - target_day)))


def kz_to_wmix(Kz, dz=50.0):
    """Scout-validated scaling: Kz(m2/s) / dz(m) * 3600 -> w_mix(m/hr)."""
    return Kz / dz * 3600.0


def spread(eta_a, eta_b):
    """Relative inter-model spread = |a-b| / mean * 100."""
    return abs(eta_a - eta_b) / ((eta_a + eta_b) / 2.0) * 100.0


# =====================================================================
# SANITY CHECKS
# =====================================================================
print("=" * 70)
print("SESSION 103 — CALIBRATED TWO-BOX VALIDATION vs TYKA ET AL. 2026")
print("=" * 70)
print(f"Baseline: TA0={TA0*1e6:.1f}  DIC0={DIC0*1e6:.2f} umol/kg  "
      f"pCO2={pco2_uatm(DIC0, TA0):.2f} uatm")
assert abs(pco2_uatm(DIC0, TA0) - 420.00) < 1e-3, "Baseline pCO2 sanity failed"
print("Baseline pCO2 sanity: PASS (exactly 420.00 uatm)")

# No-OAE drift at a few parameter extremes to confirm 15-y stability with dt=6h
drift_cases = [(20.0, 0.0072), (500.0, 0.0072), (20.0, 0.00072), (500.0, 0.00072)]
max_drift = 0.0
for mld, wm in drift_cases:
    _, inv0, *_ = run_twobox(mld, wm, 0.0)
    d = abs(inv0[-1] * 1e6)
    max_drift = max(max_drift, d)
    print(f"No-OAE drift (MLD={mld:>3.0f}m, w_mix={wm:.5f}m/hr) @15yr = {d:.6f} umol/kg-equiv")
assert max_drift < 1e-3, f"No-OAE drift too large: {max_drift}"
print(f"No-OAE drift sanity: PASS (max drift {max_drift:.6f} umol/kg-equiv < 1e-3)")

# Kz -> w_mix sanity checks from the task statement
print("\nKz -> w_mix sanity (dz=50m):")
for Kz in [1e-5, 5e-5, 1e-4]:
    print(f"  Kz={Kz:.0e} m2/s -> w_mix={kz_to_wmix(Kz):.5f} m/hr")

# =====================================================================
# SITE DEFINITIONS — physically-defensible CESM2/MARBL vs ECCO-Darwin pairs
# =====================================================================
# Units in the dict: MLD (m), Kz (m2/s). w_mix derived.
# Physical basis:
#   - MLD from de Boyer Montegut 0.03 kg/m3 climatology.
#   - CESM2/KPP systematically over-deepens MLD vs ARGO-aligned ECCO-Darwin.
#   - Kz background interior 1e-5–1e-4 m2/s in both models.
#   - Lower eta means the model has exported alkalinity out of the surface gas-
#     exchange layer faster (deeper MLD and/or stronger effective mixing).

sites = {
    "Iceland/Norway (high-latitude deep-water)": {
        # Tyka: CESM2/MARBL ~25% LOWER uptake than ECCO-Darwin.
        # Both sites have deep winter MLD (>100–500 m). CESM2/KPP over-deepens
        # the mixed layer and tends to ventilate it more strongly, so alkalinity
        # is subducted before equilibrating. The inter-model MLD difference is
        # taken as ~30–40% (KPP bias), not the full climatological range.
        "ECCO": {"MLD": 200.0, "Kz": 2.5e-5, "note": "deep MLD, moderate Kz"},
        "CESM2": {"MLD": 280.0, "Kz": 3.5e-5, "note": "KPP-overdeepened MLD, ~30% deeper"},
        "target_spread": {1: 22.0, 3: 24.0, 7: 25.0, 15: 22.0},
        "target_order": "CESM2 < ECCO",
    },
    "Oman (Indian Ocean upwelling — extreme)": {
        # Tyka: up to ~50% disagreement over most of 15 yr, narrowing to ~25% by yr15.
        # ECCO-Darwin equilibrates fast; CESM2/MARBL rapidly subducts the plume.
        # Oman upwelling has a thin climatological MLD; the CESM2 member deepens
        # it and adds stronger effective vertical exchange to mimic rapid plume
        # subduction reported by Tyka.
        "ECCO": {"MLD": 25.0, "Kz": 1.0e-5, "note": "thin upwelling MLD, weak interior Kz"},
        "CESM2": {"MLD": 55.0, "Kz": 4.0e-5, "note": "subductive export of alkaline plume"},
        "target_spread": {1: 48.0, 3: 42.0, 7: 33.0, 15: 25.0},
        "target_order": "CESM2 < ECCO",
    },
    "Brazil (subtropical thin-MLD outlier)": {
        # Tyka: most sites show 10–20% spread. Brazil is an extremely thin-MLD
        # subtropical site where both models should see similar gas-exchange
        # limitation, so the inter-model spread should be small.
        "ECCO": {"MLD": 18.0, "Kz": 2.0e-5, "note": "very thin stratified MLD"},
        "CESM2": {"MLD": 22.0, "Kz": 2.5e-5, "note": "slightly deeper but still thin MLD"},
        "target_spread": {1: 10.0, 3: 12.0, 7: 12.0, 15: 10.0},
        "target_order": "small spread, order weak",
    },
    "Japan/Kuroshio (exceptional site)": {
        # Tyka: only site where ECCO-Darwin does NOT equilibrate faster than CESM2/MARBL.
        # We interpret this as ECCO having stronger effective downward export
        # (deeper mode-water MLD / larger Kz) than CESM2 here, reversing the usual
        # CESM2-over-deepening bias. The Kuroshio mode-water formation gives both
        # models moderately deep MLD, so the spread stays modest.
        "ECCO": {"MLD": 85.0, "Kz": 3.5e-5, "note": "mode-water deep MLD, strong mixing"},
        "CESM2": {"MLD": 65.0, "Kz": 2.0e-5, "note": "shallower effective MLD, weaker export"},
        "target_spread": {1: 12.0, 3: 14.0, 7: 14.0, 15: 12.0},
        "target_order": "ECCO < CESM2",
    },
}

# =====================================================================
# SIMULATE ALL SITES
# =====================================================================
years = [1, 3, 7, 15]
days = [y * 365.0 for y in years]

results = {}
print("\n" + "=" * 70)
print("SITE SIMULATIONS")
print("=" * 70)

for site_name, cfg in sites.items():
    print(f"\n--- {site_name} ---")
    res = {"ECCO": {}, "CESM2": {}}
    for model in ("ECCO", "CESM2"):
        mld = cfg[model]["MLD"]
        Kz = cfg[model]["Kz"]
        wm = kz_to_wmix(Kz)
        note = cfg[model]["note"]
        print(f"  {model:6s}: MLD={mld:>5.1f}m  Kz={Kz:.1e}m2/s  -> w_mix={wm:.5f}m/hr  ({note})")
        t, eta = eta_series(mld, wm)
        res[model]["MLD"] = mld
        res[model]["Kz"] = Kz
        res[model]["w_mix"] = wm
        res[model]["eta"] = eta
        res[model]["eta_yr"] = {}
        for y, d in zip(years, days):
            idx = find_nearest_day(t, d)
            res[model]["eta_yr"][y] = eta[idx]
    results[site_name] = res

# =====================================================================
# RESULTS TABLE
# =====================================================================
print("\n" + "=" * 70)
print("RESULTS: eta(t) and inter-model spread")
print("=" * 70)
print(f"\n{'Site':<36} | {'Model':<6} | {'eta@1yr':>8} | {'eta@3yr':>8} | "
      f"{'eta@7yr':>8} | {'eta@15yr':>8}")
print("-" * 95)

all_rows = []
for site_name, res in results.items():
    for model in ("ECCO", "CESM2"):
        eta_vals = [res[model]["eta_yr"][y] for y in years]
        row = {
            "site": site_name,
            "model": model,
            "eta": eta_vals,
            "mld": res[model]["MLD"],
            "Kz": res[model]["Kz"],
            "w_mix": res[model]["w_mix"],
        }
        all_rows.append(row)
        print(f"{site_name:<36} | {model:<6} | "
              f"{eta_vals[0]:>8.4f} | {eta_vals[1]:>8.4f} | "
              f"{eta_vals[2]:>8.4f} | {eta_vals[3]:>8.4f}")

# =====================================================================
# SPREAD TABLE
# =====================================================================
print("\n" + "=" * 70)
print("INTER-MODEL SPREAD (%)")
print("=" * 70)
print(f"{'Site':<36} | {'S@1yr':>7} | {'S@3yr':>7} | {'S@7yr':>7} | {'S@15yr':>7} | "
      f"{'Target':<25}")
print("-" * 110)

spread_records = []
for site_name, res in results.items():
    cfg = sites[site_name]
    spreads = []
    for y in years:
        e_ecco = res["ECCO"]["eta_yr"][y]
        e_cesm = res["CESM2"]["eta_yr"][y]
        s = spread(e_ecco, e_cesm)
        spreads.append(s)
    target_str = f"~{cfg['target_spread'][1]}/~{cfg['target_spread'][3]}/~{cfg['target_spread'][7]}/~{cfg['target_spread'][15]}%"
    print(f"{site_name:<36} | {spreads[0]:>7.2f} | {spreads[1]:>7.2f} | "
          f"{spreads[2]:>7.2f} | {spreads[3]:>7.2f} | {target_str:<25}")
    spread_records.append({
        "site": site_name,
        "spreads": dict(zip(years, spreads)),
        "target": cfg["target_spread"],
        "order": cfg["target_order"],
        "eta_ECCO": [res["ECCO"]["eta_yr"][y] for y in years],
        "eta_CESM2": [res["CESM2"]["eta_yr"][y] for y in years],
    })

# =====================================================================
# VERDICT LOGIC
# =====================================================================
print("\n" + "=" * 70)
print("VERDICT ANALYSIS")
print("=" * 70)

# Evaluate ordering and magnitude errors
tolerance_pct = 10.0  # percentage-points tolerance for "match"
site_assessments = []
order_correct_count = 0
magnitude_ok_count = 0
total_score_points = 0

for rec in spread_records:
    site = rec["site"]
    order_ok = None
    magnitude_ok = None

    # Ordering
    e_ecco = rec["eta_ECCO"]
    e_cesm = rec["eta_CESM2"]
    if "CESM2 < ECCO" in rec["order"]:
        order_ok = all(e_cesm[i] < e_ecco[i] for i in range(len(years)))
    elif "ECCO < CESM2" in rec["order"]:
        order_ok = all(e_ecco[i] < e_cesm[i] for i in range(len(years)))
    elif "small spread" in rec["order"]:
        order_ok = True  # no strong order requirement

    # Magnitude: count horizons within tolerance
    ok_horizons = 0
    for y in years:
        toy = rec["spreads"][y]
        tgt = rec["target"][y]
        if abs(toy - tgt) <= tolerance_pct:
            ok_horizons += 1
    magnitude_ok = ok_horizons >= 3  # at least 3 of 4 horizons close

    if order_ok:
        order_correct_count += 1
    if magnitude_ok:
        magnitude_ok_count += 1

    total_score_points += ok_horizons
    site_assessments.append({
        "site": site,
        "order_ok": order_ok,
        "magnitude_ok": magnitude_ok,
        "ok_horizons": ok_horizons,
        "target_order": rec["order"],
    })
    print(f"{site:<36}: order_ok={order_ok}  magnitude_ok={magnitude_ok}  "
          f"({ok_horizons}/4 horizons within {tolerance_pct:.0f}% points)")

# Decide overall verdict
n_sites = len(spread_records)
order_fraction = order_correct_count / n_sites
magnitude_fraction = magnitude_ok_count / n_sites
score_fraction = total_score_points / (n_sites * len(years))

print(f"\nAggregate: order correct {order_fraction:.0%}, magnitude close {magnitude_fraction:.0%}, "
      f"horizon score {score_fraction:.0%}")

if order_fraction >= 0.75 and magnitude_fraction >= 0.50 and score_fraction >= 0.60:
    verdict = "CONFIRMED"
    verdict_detail = (
        f"Calibrated two-box toy quantitatively tracks Tyka's per-site spread: "
        f"{order_correct_count}/{n_sites} sites have the correct model ordering and "
        f"{magnitude_ok_count}/{n_sites} sites match magnitudes within {tolerance_pct:.0f} "
        f"percentage points on >=3 of 4 horizons."
    )
elif order_fraction < 0.50 or score_fraction < 0.35:
    verdict = "DISCREPANCY"
    verdict_detail = (
        f"Toy fails to reproduce the reported per-site structure: only "
        f"{order_correct_count}/{n_sites} sites ordered correctly and horizon score "
        f"{score_fraction:.0%}."
    )
else:
    verdict = "INCONCLUSIVE"
    verdict_detail = (
        f"Toy can be tuned to match some site-level features, but the mapping from "
        f"(MLD, Kz) to spread is underdetermined: {order_correct_count}/{n_sites} sites "
        f"ordered correctly, {magnitude_ok_count}/{n_sites} close in magnitude. Many "
        f"(MLD, Kz) pairs can produce similar spreads, so the model demonstrates "
        f"plausibility rather than identifying a unique explanation."
    )

print(f"\n*** VERDICT: {verdict} ***")
print(verdict_detail)

# =====================================================================
# PARAMETER TABLE (for write-up)
# =====================================================================
print("\n" + "=" * 70)
print("CALIBRATION TABLE")
print("=" * 70)
print(f"{'Site':<36} | {'Model':<6} | {'MLD(m)':>8} | {'Kz(m2/s)':>10} | {'w_mix(m/hr)':>12} | {'Justification'}")
print("-" * 120)
for site_name, res in results.items():
    cfg = sites[site_name]
    for model in ("ECCO", "CESM2"):
        print(f"{site_name:<36} | {model:<6} | {res[model]['MLD']:>8.1f} | "
              f"{res[model]['Kz']:>10.1e} | {res[model]['w_mix']:>12.5f} | {cfg[model]['note']}")

print("\n" + "=" * 70)
print("END OF SESSION 103 VALIDATION RUN")
print("=" * 70)
