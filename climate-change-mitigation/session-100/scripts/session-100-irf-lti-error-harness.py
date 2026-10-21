#!/usr/bin/env python3
"""
Session 100 — VALIDATE harness for the Yankovsky (2025) IRF surrogate.

Question: quantify the error introduced by the IRF surrogate's core assumption —
that OAE uptake efficiency is a Linear, Time-Invariant (LTI) system, so cumulative
CO2 uptake can be reconstructed by linear convolution of an alkalinity-addition
time series with ONE pre-characterized efficiency kernel.

Seawater carbonate chemistry is intrinsically nonlinear (Revelle/buffer factor),
so the LTI assumption must break for large / concentrated additions. We measure
where and by how much.

Single well-mixed surface box, T=15C, S=35, MLD=50 m. Standard total-scale
carbonate equilibrium; air-sea gas exchange to a fixed atmosphere.
"""
import numpy as np

# ---- Equilibrium constants (total scale, mol/kg), approx T=15C S=35 ----
K0 = 3.3e-2            # CO2 solubility, mol/kg/atm (Weiss 1974 approx at 15C)
K1 = 10**(-5.94)       # pK1 (Lueker 2000 approx @15C S35)
K2 = 10**(-9.10)       # pK2
KB = 10**(-8.73)       # boric acid
KW = 10**(-13.60)      # water
S  = 35.0
BT = 4.16e-4 * S/35.0  # total borate, mol/kg

def solve_h(DIC, TA):
    """Solve [H+] from DIC and TA by bisection over pH 6..10."""
    lo, hi = 10**(-10.0), 10**(-6.0)  # h bounds (pH 10 .. pH 6)
    def alk(h):
        denom = h*h + K1*h + K1*K2
        hco3 = DIC * K1*h / denom
        co3  = DIC * K1*K2 / denom
        boh4 = BT * KB/(KB+h)
        oh   = KW/h
        return hco3 + 2*co3 + boh4 + oh - h
    # alk is monotonically DECREASING in h; bracket so alk(lo)>TA>alk(hi)? check signs
    flo = alk(lo) - TA
    fhi = alk(hi) - TA
    # ensure bracketing
    for _ in range(80):
        mid = np.sqrt(lo*hi)  # geometric midpoint (pH-linear)
        fm = alk(mid) - TA
        if flo*fm <= 0:
            hi = mid; fhi = fm
        else:
            lo = mid; flo = fm
    return np.sqrt(lo*hi)

def pco2_uatm(DIC, TA):
    h = solve_h(DIC, TA)
    denom = h*h + K1*h + K1*K2
    co2 = DIC * h*h/denom      # [CO2*] mol/kg
    return (co2/K0)*1e6         # uatm

# ---- Baseline: find DIC0 so pCO2 = 420 uatm at TA0 ----
TA0 = 2300e-6
target = 420.0
lo, hi = 1800e-6, 2300e-6
for _ in range(80):
    mid = 0.5*(lo+hi)
    if pco2_uatm(mid, TA0) > target:
        hi = mid
    else:
        lo = mid
DIC0 = 0.5*(lo+hi)
print(f"Baseline: TA0={TA0*1e6:.1f} umol/kg  DIC0={DIC0*1e6:.2f} umol/kg  pCO2={pco2_uatm(DIC0,TA0):.2f} uatm")

# ---- Box model integration ----
MLD = 50.0            # m
kw  = 0.05            # m/hr piston velocity (~1.2 m/day)
pco2_atm = 420e-6     # atm
def run_box(TA_series_add, DIC_init, hours, dt=6.0):
    """
    Integrate box. TA_series_add: function(t_hours)->cumulative extra TA added (mol/kg)
    applied instantaneously as a step; we track DIC only (TA is baseline+added).
    Returns arrays t(days), DIC.
    """
    n = int(hours/dt)
    t = np.zeros(n+1); DIC = np.zeros(n+1)
    DIC[0] = DIC_init
    for i in range(n):
        th = i*dt
        TA = TA0 + TA_series_add(th)
        pco = pco2_uatm(DIC[i], TA)*1e-6   # atm
        # dDIC/dt = (kw/MLD)*K0*(pco2_atm - pco2_ocean)   [mol/kg/hr]
        dDIC = (kw/MLD)*K0*(pco2_atm - pco)
        DIC[i+1] = DIC[i] + dDIC*dt
        t[i+1] = (th+dt)/24.0
    return t, DIC

YEARS = 3.0
HOURS = YEARS*365*24
DT = 6.0

# Baseline run (no addition) — should stay ~constant (already at equilibrium)
t, DIC_base = run_box(lambda th: 0.0, DIC0, HOURS, DT)
print(f"Baseline drift over {YEARS}y: dDIC={ (DIC_base[-1]-DIC0)*1e6:.4f} umol/kg (should be ~0)")

# ---- EXPERIMENT 1: reference kernel eta(t) with tiny pulse ----
dTA_ref = 1e-6  # 1 umol/kg
t, DIC_ref = run_box(lambda th: dTA_ref, DIC0, HOURS, DT)
uptake_ref = DIC_ref - DIC_base          # extra DIC taken up
eta_ref = uptake_ref/dTA_ref             # efficiency step response (dimensionless)

def eta_at(days):
    idx = np.argmin(np.abs(t-days))
    return eta_ref[idx]
print("\n=== EXPERIMENT 1: reference efficiency kernel eta(t) (dTA=1 umol/kg) ===")
for d in [30, 90, 365, 730, YEARS*365-1]:
    print(f"  eta(t={d:6.0f} d) = {eta_at(d):.4f}")
print(f"  asymptotic eta(end) = {eta_ref[-1]:.4f}")

# ---- EXPERIMENT 2: LTI superposition vs nonlinear truth vs magnitude ----
mags = [1, 10, 50, 100, 200, 400]  # umol/kg total, single pulse
print("\n=== EXPERIMENT 2: single-pulse LTI-scaling error vs magnitude ===")
print(f"{'dTA(umol/kg)':>12} | {'eta_truth@1yr':>13} | {'err@1yr(%)':>11} | {'eta_truth@end':>13} | {'err@end(%)':>11}")
idx_1yr = np.argmin(np.abs(t-365))
exp2_rows = []
for m in mags:
    dTA = m*1e-6
    t2, DIC_m = run_box(lambda th: dTA, DIC0, HOURS, DT)
    uptake_truth = DIC_m - DIC_base
    uptake_pred  = eta_ref * dTA           # linear scaling of reference kernel
    # efficiencies (per umol added)
    eta_truth_1yr = uptake_truth[idx_1yr]/dTA
    eta_truth_end = uptake_truth[-1]/dTA
    err_1yr = (uptake_pred[idx_1yr]-uptake_truth[idx_1yr])/uptake_truth[idx_1yr]*100
    err_end = (uptake_pred[-1]-uptake_truth[-1])/uptake_truth[-1]*100
    exp2_rows.append((m, eta_truth_1yr, err_1yr, eta_truth_end, err_end))
    print(f"{m:>12} | {eta_truth_1yr:>13.4f} | {err_1yr:>+11.3f} | {eta_truth_end:>13.4f} | {err_end:>+11.3f}")

# ---- EXPERIMENT 3: single vs staggered delivery of same total ----
print("\n=== EXPERIMENT 3: single 100 vs 10x10 umol/kg monthly (LTI convolution) ===")
total = 100e-6
# (i) single pulse
t3, DIC_single = run_box(lambda th: total, DIC0, HOURS, DT)
uptake_single = DIC_single - DIC_base
# (ii) 10 monthly pulses of 10 umol/kg
pulses = [(i*30*24, 10e-6) for i in range(10)]  # (t_hours, dTA)
def staggered_add(th):
    s = 0.0
    for (tp, dp) in pulses:
        if th >= tp:
            s += dp
    return s
t3b, DIC_stag = run_box(staggered_add, DIC0, HOURS, DT)
uptake_stag = DIC_stag - DIC_base

# IRF convolution prediction for both schedules using reference impulse response
# impulse response = derivative of eta step response
h_imp = np.zeros_like(eta_ref)
h_imp[1:] = np.diff(eta_ref)             # per-step increments (per umol/kg)
def conv_predict(schedule_func):
    n = len(t)
    add_rate = np.zeros(n)                # umol/kg added at each step (as delta)
    prev = 0.0
    for i in range(n):
        cur = schedule_func(t[i]*24.0)
        add_rate[i] = (cur - prev)        # mol/kg added this step
        prev = cur
    # convolve additions with impulse response (in units of dTA_ref)
    pred = np.zeros(n)
    for i in range(n):
        if add_rate[i] != 0:
            scale = add_rate[i]/dTA_ref
            L = n-i
            pred[i:] += scale * eta_ref[:L] * dTA_ref
    return pred
pred_single = conv_predict(lambda th: total)
pred_stag   = conv_predict(staggered_add)

err_single_end = (pred_single[-1]-uptake_single[-1])/uptake_single[-1]*100
err_stag_end   = (pred_stag[-1]-uptake_stag[-1])/uptake_stag[-1]*100
err_single_1yr = (pred_single[idx_1yr]-uptake_single[idx_1yr])/uptake_single[idx_1yr]*100
err_stag_1yr   = (pred_stag[idx_1yr]-uptake_stag[idx_1yr])/uptake_stag[idx_1yr]*100
print(f"  SINGLE 100 umol/kg:   truth uptake@end={uptake_single[-1]*1e6:.3f}  IRF err@1yr={err_single_1yr:+.3f}%  err@end={err_single_end:+.3f}%")
print(f"  STAGGERED 10x10:      truth uptake@end={uptake_stag[-1]*1e6:.3f}  IRF err@1yr={err_stag_1yr:+.3f}%  err@end={err_stag_end:+.3f}%")
print(f"  -> staggering reduces peak instantaneous concentration; |err| ratio single/stag @end = {abs(err_single_end)/max(abs(err_stag_end),1e-9):.2f}x")

print("\n=== SUMMARY ===")
print(f"Single-model IRF linearization (LTI) error stays < ~{max(abs(r[4]) for r in exp2_rows if r[0]<=10):.2f}% for dilute additions (<=10 umol/kg),")
print(f"and grows to {exp2_rows[-1][4]:+.2f}% at {mags[-1]} umol/kg single pulse (Revelle nonlinearity).")
print("Compare to Tyka 2026 inter-model STRUCTURAL transport spread ~50% @7y.")
