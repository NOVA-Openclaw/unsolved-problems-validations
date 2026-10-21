#!/usr/bin/env python3
"""S49 VALIDATE claim 1: minimizer of C(f)=int f^2 + iint |u-v| f(u)f(v) on J=[-lam/2,lam/2], int f=1.
Discretize (midpoint rule, n cells), solve KKT (quadratic form + linear constraint) exactly,
compare min value to C_lam = lam/2 + cot(lam/sqrt2)/sqrt2 and argmin to f_lam."""
import numpy as np

def C_formula(lam):
    return lam/2 + (1/np.sqrt(2))/np.tan(lam/np.sqrt(2))

def f_formula(u, lam):
    return np.cos(np.sqrt(2)*u)/(np.sqrt(2)*np.sin(lam/np.sqrt(2)))

def discrete_min(lam, n):
    a = lam/2; h = lam/n
    u = -a + h*(np.arange(n)+0.5)
    # exact cell-averaged |u-v| kernel: off-diagonal |ui-uj| (exact for piecewise-const cell pair avg),
    # diagonal cell self-average of |u-v| over a cell = h/3
    D = np.abs(u[:, None]-u[None, :]); np.fill_diagonal(D, h/3)
    M = h*np.eye(n) + h*h*D          # C(f) = f^T M f for piecewise-constant f
    w = h*np.ones(n)                 # int f = w^T f
    x = np.linalg.solve(M, w); f = x/(w@x)
    return u, f, f@M@f

def value_of(fvals, lam, n):
    a = lam/2; h = lam/n
    u = -a + h*(np.arange(n)+0.5)
    D = np.abs(u[:, None]-u[None, :]); np.fill_diagonal(D, h/3)
    return h*fvals@fvals + h*h*fvals@D@fvals

print(f"{'lam':>5} {'n':>5} {'C_discrete':>14} {'C_formula':>14} {'rel.diff':>10} {'max|f-f_lam|/max f_lam':>24} {'C(f_lam) disc':>14} {'G spread':>10}")
for lam in [0.2, 0.2613, 0.3, 0.5, 0.5502, 0.8, 1.0, 1.5]:
    for n in [400, 1600]:
        u, f, Cd = discrete_min(lam, n)
        fl = f_formula(u, lam)
        Cf = C_formula(lam)
        # Euler-Lagrange: G(u)=f(u)+int|u-v|f(v)dv should be constant = C_lam
        h = lam/n
        D = np.abs(u[:, None]-u[None, :]); np.fill_diagonal(D, h/3)
        G = fl + h*D@fl
        print(f"{lam:5.4g} {n:5d} {Cd:14.10f} {Cf:14.10f} {abs(Cd-Cf)/Cf:10.2e} {np.max(np.abs(f-fl))/np.max(fl):24.3e} {value_of(fl,lam,n):14.10f} {G.max()-G.min():10.2e}")
    # also check int f_lam = 1
    uu = np.linspace(-lam/2, lam/2, 200001)
    print(f"      int f_lam = {np.trapezoid(f_formula(uu,lam),uu):.12f};  f_lam>0 on J: {bool(np.all(f_formula(uu,lam)>0))}")

# random perturbation test: C(f_lam + eps*h) - C_lam >= 0 for mean-zero h
rng = np.random.default_rng(49)
print("\nperturbation test (mean-zero random h, 2000 trials per lam): min of C(f)-C_lam")
for lam in [0.3, 0.5, 1.0]:
    n = 800; h = lam/n; u = -lam/2 + h*(np.arange(n)+0.5)
    fl = f_formula(u, lam); base = value_of(fl, lam, n); worst = np.inf
    for _ in range(2000):
        pert = rng.standard_normal(n).cumsum(); pert -= pert.mean()
        pert *= 0.1*np.max(fl)/np.max(np.abs(pert))
        worst = min(worst, value_of(fl+pert, lam, n)-base)
    print(f"  lam={lam}: min delta = {worst:.3e} (should be >0)")
