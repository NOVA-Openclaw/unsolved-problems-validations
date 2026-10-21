#!/usr/bin/env python3
"""S253 VALIDATE: derived arithmetic on EPI-321 WMS 2026 slide values (Roxburgh, slides 13-15).
Means are OBSERVED (printed on slides). SEMs are DERIVED by reading error-bar endpoints off a
90-dpi render (slide-13.png / slide-14.png, 1200 px wide); treat them as approximate (+/-0.2 units)."""
import math
from scipy import stats

n = 6
# (label, epi_mean, epi_sem_approx, comp_mean, comp_sem_approx, comp_n, comp_name)
rows = [
 ("LMV total %",      1.3, 1.93, -2.7, 0.21,  6, "digital twin (model prediction)"),
 ("LMV upper %",      3.0, 2.40, -3.5, 0.50,  6, "digital twin (model prediction)"),
 ("LMV lower %",      0.3, 1.86, -2.5, 0.23,  6, "digital twin (model prediction)"),
 ("QMT total PPN",    3.3, 3.59, -0.8, 0.21, 39, "ReSolve ECA"),
 ("QMT upper PPN",    4.1, 3.78, -0.3, 0.30, 39, "ReSolve ECA"),
 ("QMT lower PPN",    0.8, 2.03, -1.3, 0.51, 39, "ReSolve ECA"),
]
tcrit = stats.t.ppf(0.975, n-1)
print(f"t_crit(0.975, df={n-1}) = {tcrit:.3f}")
print("label | EPI mean | ~SEM | ~SD | one-sample t vs 0 | 95% CI (EPI alone) | comparator | net delta | naive Welch t vs comparator | approx p")
for lab, m, se, cm, cse, cn, cname in rows:
    sd = se*math.sqrt(n)
    t0 = m/se
    lo, hi = m - tcrit*se, m + tcrit*se
    d = m - cm
    sed = math.sqrt(se**2 + cse**2)
    tw = d/sed
    # Welch-Satterthwaite df
    df = (se**2 + cse**2)**2 / (se**4/(n-1) + cse**4/(cn-1))
    p = 2*stats.t.sf(abs(tw), df)
    print(f"{lab} | {m:+.1f} | {se:.2f} | {sd:.2f} | {t0:.2f} | [{lo:+.1f}, {hi:+.1f}] | {cname} {cm:+.1f} | {d:+.1f} | {tw:.2f} (df~{df:.1f}) | {p:.3f}")

print()
print("Slide 15 muscle-level table (OBSERVED values), net deltas (DERIVED):")
tab = [("Shoulder Abduction",4.0,-3.2,1.0,2.2),("Shoulder External Rotation",1.9,-1.9,2.2,-1.6),
       ("Elbow Extension",3.2,-9.0,8.1,-1.1),("Elbow Flexion",1.7,-9.3,0.7,-0.2),("Total Upper Body",2.8,-4.0,3.0,-0.2)]
for name,l,dt,q,rs in tab:
    print(f"{name}: LMV net {l-dt:+.1f} pts vs DT; QMT net {q-rs:+.1f} PPN vs ReSolve" + ("  <-- comparator > EPI-321" if q-rs<0 else ""))
print()
print("Caveat: naive Welch treats the digital-twin SEM as sampling error of an independent arm. It is a model")
print("prediction for the SAME 6 patients, so the correct test is paired (obs - predicted) with model RMSE;")
print("neither the paired SD nor the 6-month prediction error is disclosed. These p-values are NOT evidence of")
print("significance; they only show that the per-arm EPI-321 95% CIs all include 0 at n=6.")
