#!/usr/bin/env python3
"""S258 follow-up: optimal composite radius R*(h) for paired disc composites (k=15 and k=30),
same model as S258_validated_design.py. Tests whether S257's 'R << 0.2a' rule survives when h>0."""
import math, numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("m", "S258_validated_design.py")
# re-implement minimal pieces to avoid re-running the main script body
rng = np.random.default_rng(2581)
NU0 = (1-0.05)**2*0.00094**2/((0.7150-0.7035)**2*0.05**2*0.15**2)
def c_rel(d, f, a):
    r = np.minimum(d/a, 1.0); return np.where(d == 0, 1.0, (1-f)*(1-(1.5*r-0.5*r**3)))
def disc(k, R, c):
    rr = R*np.sqrt(rng.uniform(size=k)); th = rng.uniform(0, 2*np.pi, k)
    return np.c_[rr*np.cos(th), rr*np.sin(th)] + c
def cbar(P, Q, f, a, same):
    d = np.sqrt(((P[:, None]-Q[None])**2).sum(-1)); c = c_rel(d, f, a)
    if not same: c = np.where(d == 0, 1-f, c)
    return c.mean()
def vrel(k, R, h, f, a, reps=1000):
    acc = 0.0
    for _ in range(reps):
        P = disc(k, R, np.zeros(2)); th = rng.uniform(0, 2*np.pi)
        Q = disc(k, R, h*np.array([np.cos(th), np.sin(th)]))
        acc += 0.5*(cbar(P, P, f, a, True)+cbar(Q, Q, f, a, True)) - cbar(P, Q, f, a, False)
    return 2*acc/reps
Rs = [0.5, 1, 2, 3, 5, 7.5, 10, 15, 20, 30]
for pn, f, a in [('ExCa', 0.408, 20.5), ('TotSr f=.25', 0.25, 30.0)]:
    for k in [15, 30]:
        print(f"-- {pn} (f={f}, a={a} m), k={k}: n(R) per h; R* = argmin")
        print(f"{'h':>5s} " + " ".join(f"R={R:>4}" for R in Rs) + "   R*   n*  R*/h")
        for h in [0.5, 1.0, 2.5, 5.0, 10.0]:
            ns = [math.ceil(NU0*vrel(k, R, h, f, a)) for R in Rs]
            i = int(np.argmin(ns))
            print(f"{h:5.1f} " + " ".join(f"{n:6d}" for n in ns) + f"  {Rs[i]:5} {ns[i]:4d}  {Rs[i]/h:4.1f}")
