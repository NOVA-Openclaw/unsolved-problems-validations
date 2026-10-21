#!/usr/bin/env python3
"""S261 (UPR run #1042): Gy fundamental sampling error (FSE) anchor for phi.

Gy FSE:  s_FSE^2 (relative) = (1/Ms - 1/ML) * c * f * g * l * d^3      [Ms, ML in g; d in cm; densities g/cm3]
  c = ((1-aL)/aL) * ((1-aL)*rho_c + aL*rho_g)   mineralogical factor for critical-component mass fraction aL
  f = 0.5 shape, g = 0.25 granulometric (unsieved/broad), l = liberation (1 = discrete grains)
Standard textbook defaults (Gy 1979/1998; Pitard 1993; Gerlach & Nocerino EPA/600/R-03/027 2003) - CITED
in the artifact; parameter choices for this ERW case are ASSUMED.

Case: post-application soil where the basalt signal is carried partly by discrete feedstock grains
(total-digest 87Sr/86Sr). x = 0.05 basalt Sr fraction; aL ~ basalt mass fraction.
Converts relative FSE on aL (-> on x) into phi = sigma_S,eq^2 / sigma_S^2 with
sigma_S,eq = r_F * x * (S-B)/(1-x) and sigma_S = 0.00094 (S255).
Exchangeable-Sr leaches (NH4OAc) carry no particulate basalt term: l << 1, phi much smaller.
"""
import math
B, S, SIG, X = 0.7035, 0.7150, 0.00094, 0.05
f, g, l = 0.5, 0.25, 1.0
rho_c, rho_g = 2.9, 2.65

def c_min(aL):
    return ((1 - aL) / aL) * ((1 - aL) * rho_c + aL * rho_g)

def rF(aL, d_cm, Ms, ML=1e12):
    return math.sqrt((1 / Ms - 1 / ML) * c_min(aL) * f * g * l * d_cm**3)

def phi_from_r(r):
    return (r * X * (S - B) / (1 - X) / SIG) ** 2

print("Relative FSE r_F on basalt mass fraction, and phi (fraction of sigma_S^2), x=0.05")
for aL in (0.037, 0.01):
    print(f"\n aL = {aL} (c = {c_min(aL):.1f} g/cm3)")
    print(f"   {'d (um)':>7s} {'Ms (g)':>7s} {'r_F':>7s} {'phi':>8s}")
    for d_um in (2000, 1000, 500, 250, 75):
        for Ms in (0.1, 0.25, 1.0, 10.0, 50.0):
            r = rF(aL, d_um * 1e-4, Ms)
            print(f"   {d_um:7d} {Ms:7.2f} {r:7.3f} {phi_from_r(r):8.5f}")

print("\nTwo-stage protocol (TOS-compliant): composite ML=5 kg sieved <2 mm -> riffle split Ms1 at d=2 mm,")
print("pulverise all of Ms1 to <75 um, analytical aliquot Ms2. Stage variances add.")
for aL in (0.037, 0.01):
    for Ms1 in (20.0, 50.0, 200.0):
        for Ms2 in (0.1, 0.25):
            s1 = (1 / Ms1 - 1 / 5000.0) * c_min(aL) * f * g * l * 0.2**3
            s2 = (1 / Ms2 - 1 / Ms1) * c_min(aL) * f * g * l * 0.0075**3
            r = math.sqrt(s1 + s2)
            print(f"  aL={aL} Ms1={Ms1:5.0f} g Ms2={Ms2:.2f} g: r_F={r:.3f} phi={phi_from_r(r):.5f}")
print("\nAnalytical-only phi (2SD 15 ppm on 0.71, i.e. 1SD ~7.5e-6 abs):", f"{(7.5e-6/SIG)**2:.2e}")
