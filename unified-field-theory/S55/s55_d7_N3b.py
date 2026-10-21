"""POST-HOC (not preregistered) N3b: N3 criterion (b) failed only at d~1e-8 (arccos roundoff + M2 roundoff ~1e-16).
Re-run identical sampling with robust distance d = arcsin(||v - <s,v>s||) and report min M2/d^2 for d > 1e-4 and d > 1e-6."""
import numpy as np, json, s55_lib as L
out = {}; c0 = 4 / L.LN2
for N in (2, 3):
    rng = np.random.default_rng(55707); D = 2 ** N; st = L.enumerate_stab(N, rng, 60 if N == 2 else 1080); rows = []
    if N == 3:  # replicate the N3 rng stream: N=2 consumed it first
        rng = np.random.default_rng(55707); st2 = L.enumerate_stab(2, rng, 60)
        for k in range(20000):
            if k % 2 == 0: rng.normal(size=4); rng.normal(size=4)
            else:
                rng.integers(60); rng.normal(size=4); rng.normal(size=4); rng.uniform(0, .5)
                if k % 4 == 1: rng.uniform()
        st = L.enumerate_stab(3, rng, 1080)
    for k in range(20000):
        if k % 2 == 0: v = rng.normal(size=D) + 1j * rng.normal(size=D)
        else:
            phi = st[rng.integers(len(st))]; w = rng.normal(size=D) + 1j * rng.normal(size=D); w -= np.vdot(phi, w) * phi; w /= np.linalg.norm(w)
            t = rng.uniform(0, 0.5) * (rng.uniform() ** 2 if k % 4 == 1 else 1); v = np.cos(t) * phi + np.sin(t) * w
        v /= np.linalg.norm(v); ov = st.conj() @ v; j = np.argmax(np.abs(ov)); r = v - ov[j] * st[j]
        d = float(np.arcsin(min(1, np.linalg.norm(r)))); rows.append((d, L.M2(v)))
    a = np.array(rows); d, m = a[:, 0], a[:, 1]
    res = {}
    for cut in (1e-6, 1e-4):
        s = d > cut; q = m[s] / d[s] ** 2; res[f'd>{cut}'] = dict(n=int(s.sum()), min_M2_over_d2=float(q.min()), min_ratio=float(q.min() / c0), d_at_min=float(d[s][np.argmin(q)]))
    s = (d > 1e-4) & (d < 0.02); res['mean_ratio_1e-4<d<0.02'] = float((m[s] / (c0 * d[s] ** 2)).mean())
    res['n_d_le_1e-6'] = int(np.sum(d <= 1e-6)); res['max_abs_M2_at_d_le_1e-6'] = float(np.max(np.abs(m[d <= 1e-6]))) if np.any(d <= 1e-6) else None
    out[f'N={N}'] = res; print(N, res, flush=True)
json.dump(out, open('s55_d7_N3b.json', 'w'), indent=1)
