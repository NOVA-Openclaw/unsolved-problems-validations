#!/usr/bin/env python3
"""S49 VALIDATE claims 2-4: algebra + roots + monotonicity/boundedness."""
import numpy as np
from scipy.optimize import brentq
r2 = np.sqrt(2)
cot = lambda x: 1/np.tan(x)
C = lambda t: t/2 + cot(t/r2)/r2                               # Wang Prop 4.1 C_lambda
c_wang = lambda t: 2 - C(t)                                    # Wang (1.7) simple&critical
d_avg = lambda t: (3 - C(t))/2                                 # Lamzouri (2.6) -> (Ns+N0)/(2N)
c2_from_27 = lambda t: (5 + 2*r2 - 2*C(t))/(3 + 2*r2)          # Lamzouri (2.7) with A=C(t)
c2_S47 = lambda t: (5 + 2*r2 - t - r2*cot(t/r2))/(3 + 2*r2)    # S47 formula as written
d_S47 = lambda t: 1.5 - t/4 - cot(t/r2)/(2*r2)                 # S47 d(theta) as written

ts = np.linspace(0.05, 0.999, 20000)
print("max |c2_S47 - c2_from_(2.7)| :", np.max(np.abs(c2_S47(ts)-c2_from_27(ts))))
print("max |d_S47 - (3-C)/2|        :", np.max(np.abs(d_S47(ts)-d_avg(ts))))

roots = {
 "c2(theta)=0  [S47 claims 0.261286]": brentq(c2_S47, 0.1, 0.9, xtol=1e-15),
 "d(theta)=0   [S47 claims 0.346658; Wang 0.346658926139761]": brentq(d_S47, 0.1, 0.9, xtol=1e-15),
 "c(theta)=0 Wang simple&crit [0.550193964744154]": brentq(c_wang, 0.1, 0.9, xtol=1e-15),
 "C(theta)=2  (Lamzouri (2.7) stated hypothesis A<2 boundary)": brentq(lambda t: C(t)-2, 0.1, 0.9, xtol=1e-15),
 "C(theta)=5/2+sqrt2 (b1>0 boundary actually used in proof)": brentq(lambda t: C(t)-(2.5+r2), 0.05, 0.9, xtol=1e-15),
}
for k, v in roots.items():
    print(f"{k}: {v:.12f}")

print("\nvalues at theta=1 (global):")
C0 = 1.5 - cot(1/r2)/r2
print(f"  C_MT=C(1)={C(1):.13f}  C0=2-C(1)={c_wang(1):.13f}  (Lamzouri C0=0.6725007)")
print(f"  c2(1)={c2_S47(1):.13f}  Lamzouri C2=(1+2r2+2C0)/(3+2r2)={(1+2*r2+2*C0)/(3+2*r2):.13f}  (paper: 0.88762)")
print(f"  d(1)={d_S47(1):.13f}  Lamzouri C1=(C0+1)/2={(C0+1)/2:.13f}  (paper: 0.83625)")
print(f"  BGST/Soundararajan conditional (2+C0)/3={(2+C0)/3:.5f} (c2 should be below this)")

# monotonicity: c2'(t) = cot^2(t/r2)/(3+2r2) > 0  (analytic); check numerically
tt = np.linspace(roots['c2(theta)=0  [S47 claims 0.261286]'], 1.0, 200001)
v = c2_S47(tt); dv = np.diff(v)
print(f"\non [theta_c2, 1]: c2 min={v.min():.3e} max={v.max():.10f} strictly increasing={bool(np.all(dv>0))} <=1: {bool(np.all(v<=1))}")
num_der = np.gradient(v, tt); ana = cot(tt/r2)**2/(3+2*r2)
print(f"  max |numeric c2' - cot^2/(3+2r2)| = {np.max(np.abs(num_der-ana)[1:-1]):.2e}")
print("\ntable:")
for t in [0.2613, 0.3, 0.3293, 0.35, 0.4, 0.5, 0.5502, 0.6, 0.75, 0.9, 1.0]:
    print(f"  theta={t:<7} C={C(t):8.5f}  c_wang={c_wang(t):+.5f}  d={d_S47(t):+.5f}  c2={c2_S47(t):+.5f}  (A<2? {C(t)<2})")
