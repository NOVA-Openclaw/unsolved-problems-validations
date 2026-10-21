#!/usr/bin/env python3
# s82-validate-depth-law-pythia410m.py
# VALIDATE (UPR Session 82, Consciousness Hard Problem, Track C).
#
# TARGET: S80/S81 queued VALIDATE — do the 12-layer findings transfer to 24 layers?
# On {gpt2-124M, pythia-160m} (12 layers) S80 established:
#   (1) RELATIVE-DEPTH PATH LAW: export of the injected edit peaks at L_inj+1 and decays
#       with distance from the injection; far-position readout of the relay is available
#       at ANY layer >= L_inj+2 and exactly 0 below that hop-timing floor.
#   (2) L_inj+2 FLOOR: blocking FAR's post-p readout at L_inj+2..nL-1 kills the relay
#       EXACTLY (structural hop-timing arithmetic).
# S81 added: (3) pythia-160m's FINAL-LAYER ALLOCATION ZERO — a_{FAR,p} = 0.000000 at L11
#       (vs gpt2 0.0147) while the edit sits healthy in p's value stream (|dv_p| ~ 12-14);
#       the direct late readout is allocation-limited, the 2-hop carrier relay is
#       family-universal in absolute deflection.
#
# THIS SESSION: EleutherAI/pythia-410m (24 layers, hidden 1024, 16 heads), same family
# as pythia-160m, double the depth. Injection depths chosen to PRESERVE RELATIVE DEPTH:
#   L_inj = 12  (12/24 = 0.50 — analogue of S79's inj6 in 12 layers)
#   L_inj = 18  (18/24 = 0.75 — analogue of S80's inj9 in 12 layers)
# Bands scaled by thirds: early 0-7, mid 8-15, late 16-23 (12-layer thirds 0-3/4-7/8-11).
#
# HYPOTHESES UNDER TEST (each gets a verdict):
#   H1 (export offset absolute-in-layers): keep-only export peak at L_inj+1 — the +1 is
#       a hop count, NOT a fraction of depth. Fractional-scaling alternative at 24 layers
#       predicts peak at L_inj+2..+4.
#   H2 (readout floor L_inj+2, structural): s3-block-postinj2 (L_inj+2..23) EXACT 0 at
#       both depths; NEW tightness probe s3-block-postinj3 (L_inj+3..23) > 0 iff readout
#       AT exactly L_inj+2 is usable (12-layer inj9 late-band result implies it is).
#   H3 (readout not pinned late): at inj12, blocking late16-23 leaves the relay alive
#       (readout at 14-15 exists). Absolute-late law predicts exact 0. (At inj18 the late
#       band covers the whole >= L_inj+2 range, so block-late16-23 must be EXACT 0
#       structurally — that is a control, not a discriminator.)
#   H4 (final-layer allocation zero, family property): a_{FAR,p} ~ 0 at the LAST layer
#       (23) with |dv_p| healthy; second-to-last (22) tiny but nonzero; behavioral
#       counterpart: keep-only-L23 ~ 0 while keep-only at earlier layers works.
#
# STRUCTURAL EXACT-0 PREDICTIONS (law-independent): ctl-k0-all, s1-keep-L{L_inj},
# s1-band-postinj, s3-block-all, s3-block-postinj2, (inj18 only) s3-block-late16-23.
# ctl-noop == 1.0. Gates: 6-decimal zeros per cell; <1e-4 relative in global gates.
#
# Apparatus: S78-S81 verbatim — NaN-safe layer-aware SDPA additive-mask ablation with
# the S81 in-mask recorder (here at layers 22/23, noablate baseline pair only);
# ablation-matched referencing D(c) = mean_FAR outspan(h_patch - h_clean) at hs[24];
# do(W := 3||W||) at p (last prompt token) via forward hook on block L_inj output;
# same prompts/concepts as S77-S81; HA=12; FAR_W=3; SEED=82; CPU; float32 FORCED
# (pythia-410m checkpoint ships fp16 — dtype override documented deviation, matches
# the fp32 arithmetic of all prior sessions).
# Efficiency deviations (pure caching, no protocol change): clean greedy continuations
# computed once per prompt and reused across cells (patch/ablation off -> identical by
# construction); concept-direction hidden states computed once per direction and sliced
# per injection layer.
#
# Run: .venv-s75/bin/python s82-validate-depth-law-pythia410m.py
import math, time, random
from collections import defaultdict
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

SEED = 82
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
torch.set_grad_enabled(False)
T0 = time.time()

MODEL_NAME = "EleutherAI/pythia-410m"
FAMILY = "pythia"
INJECT_BLOCKS = [12, 18]
ALLOC_LAYERS = (22, 23)

CONCEPTS = {
    "valence": (
        ["This movie was absolutely wonderful and", "I loved every second, it felt great and",
         "What a fantastic, delightful experience that was and", "The food was delicious and",
         "She smiled, overjoyed and thrilled, and", "It was a beautiful, happy, perfect day and"],
        ["This movie was absolutely terrible and", "I hated every second, it felt awful and",
         "What a dreadful, miserable experience that was and", "The food was disgusting and",
         "He frowned, depressed and furious, and", "It was an ugly, sad, ruined day and"],
    ),
    "size": (
        ["The enormous, gigantic, colossal tower and", "A vast and immense expanse stretched and",
         "The huge, massive whale surfaced and", "An overwhelming, towering mountain and",
         "The sprawling, giant metropolis and", "A monstrous, titanic wave rose and"],
        ["The tiny, minuscule, microscopic speck and", "A small and diminutive dot appeared and",
         "The little, petite mouse scurried and", "A negligible, minute fleck and",
         "The compact, miniature cottage and", "A tiny, wee crumb fell and"],
    ),
}

AVG_PROMPTS = [
    "The film I watched last night was",
    "My review of the restaurant is that it was",
    "Honestly, the whole trip turned out to be",
    "When she opened the letter, her reaction was",
    "Looking back on the concert, I thought it was",
]

HA = 12
FAR_W = 3

# ------------- layer-aware SDPA ablation monkeypatch (S78-S81) + in-mask recorder -------------
_real_sdpa = torch.nn.functional.scaled_dot_product_attention
ABLATE = {"on": False, "specs": []}
RECORD = {"on": False, "layers": set(ALLOC_LAYERS), "data": {}, "maxerr": 0.0}
LAYER = {"i": 0}

def patched_sdpa(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False,
                 scale=None, **kw):
    if not (ABLATE["on"] or RECORD["on"]):
        return _real_sdpa(query, key, value, attn_mask=attn_mask, dropout_p=dropout_p,
                          is_causal=is_causal, scale=scale, **kw)
    L = LAYER["i"]; LAYER["i"] += 1
    q_len = query.shape[-2]; k_len = key.shape[-2]; dev = query.device
    i = torch.arange(q_len, device=dev)[:, None]
    j = torch.arange(k_len, device=dev)[None, :]
    causal = j <= i
    mask = torch.zeros(q_len, k_len, dtype=query.dtype, device=dev)
    mask = mask.masked_fill(~causal, float("-inf"))
    specs = ABLATE["specs"] if ABLATE["on"] else []
    for spec in specs:
        if spec["layers"] is not None and L not in spec["layers"]:
            continue
        rb = torch.zeros(q_len, dtype=torch.bool, device=dev); rb[spec["rows"]] = True
        cb = torch.zeros(k_len, dtype=torch.bool, device=dev); cb[spec["cols"]] = True
        block = rb[:, None] & cb[None, :]
        if spec.get("keep_diag", True):
            block &= ~(i == j)
        mask = mask.masked_fill(block, float("-inf"))
    ret = _real_sdpa(query, key, value, attn_mask=mask.view(1, 1, q_len, k_len),
                     dropout_p=dropout_p, is_causal=False, scale=scale, **kw)
    if RECORD["on"] and L in RECORD["layers"]:
        dh = query.shape[-1]
        sc = scale if scale is not None else 1.0 / math.sqrt(dh)
        q = query[0].float(); k = key[0].float(); v = value[0].float()
        logits = q @ k.transpose(-1, -2) * sc + mask.float()
        probs = torch.softmax(logits, dim=-1)
        recon = probs @ v
        err = (recon - ret[0].float()).abs().max().item()
        RECORD["maxerr"] = max(RECORD["maxerr"], err)
        RECORD["data"][L] = {"probs": probs.clone(), "value": v.clone()}
    return ret

torch.nn.functional.scaled_dot_product_attention = patched_sdpa

# ---------------- model helpers (S77-S81) ----------------
def load(model_name):
    tok = AutoTokenizer.from_pretrained(model_name)
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name, attn_implementation="sdpa", dtype=torch.float32)
    except TypeError:
        model = AutoModelForCausalLM.from_pretrained(
            model_name, attn_implementation="sdpa", torch_dtype=torch.float32)
    model.eval()
    assert next(model.parameters()).dtype == torch.float32, "float32 load failed"
    return tok, model

# concept-direction hidden-state cache: text -> tuple of hidden states (one forward,
# all layers) so both injection depths slice the same forwards
_HS_CACHE = {}
def all_resids(model, tok, text):
    if text not in _HS_CACHE:
        ids = tok(text, return_tensors="pt").input_ids
        hs = model(ids, output_hidden_states=True).hidden_states
        _HS_CACHE[text] = [h[0, -1].numpy().copy() for h in hs]
    return _HS_CACHE[text]

def concept_dir(model, tok, name, L):
    pos, neg = CONCEPTS[name]
    mp = np.mean([all_resids(model, tok, t)[L + 1] for t in pos], axis=0)
    mn = np.mean([all_resids(model, tok, t)[L + 1] for t in neg], axis=0)
    v = mp - mn; n = np.linalg.norm(v)
    return v / n, n

class Patch:
    def __init__(self): self.dir=None; self.target=0.0; self.positions=None; self.on=False
patch = Patch()

def make_hook():
    def hook(module, inp, out):
        if not patch.on: return out
        h = out[0] if isinstance(out, tuple) else out
        dhat = patch.dir.to(h.dtype)
        pos = patch.positions if patch.positions is not None else range(h.shape[1])
        for p in pos:
            cur = torch.dot(h[0, p], dhat)
            h[0, p] = h[0, p] - cur*dhat + patch.target*dhat
        if isinstance(out, tuple): return (h,)+tuple(out[1:])
        return h
    return hook

def decomp(dv_np, what):
    inspan = np.dot(dv_np, what)
    outspan_vec = dv_np - inspan*what
    return abs(float(inspan)), float(np.linalg.norm(outspan_vec))

def fwd_hs(model, seq):
    LAYER["i"] = 0
    hs = model(seq, output_hidden_states=True).hidden_states
    assert not torch.isnan(hs[-1]).any(), "NaN in hidden states (ablation mask bug?)"
    return hs

# ---------------- config builder (S80 compact core, 24-layer bands, + postinj3 probe) ----------------
def build_configs(p, S, nL, Linj):
    rows_all = list(range(p+1, S))
    far = list(range(S-FAR_W, S))
    def sever_p(rows, layers):
        return {"rows": rows, "cols": [p], "layers": layers, "keep_diag": True}
    third = nL // 3
    bands = {f"early0-{third-1}": set(range(0, third)),
             f"mid{third}-{2*third-1}": set(range(third, 2*third)),
             f"late{2*third}-{nL-1}": set(range(2*third, nL)),
             f"postinj{Linj+1}-{nL-1}": set(range(Linj+1, nL))}
    cfgs = []
    for L in range(Linj, nL):
        cfgs.append((f"s1-keep-L{L:02d}", [sever_p(rows_all, set(range(nL)) - {L})]))
    for bn, bs in bands.items():
        cfgs.append((f"s1-band-{bn}", [sever_p(rows_all, bs)]))
    cfgs.append(("ctl-k0-all", [sever_p(rows_all, None)]))
    cfgs.append(("ctl-noop", []))
    # sweep 3: relay-readout depth (S78 k=8 regime)
    spec1 = sever_p(list(range(p+9, S)), None)
    cfgs.append(("s3-relay-ref-k8", [spec1]))
    relay_cols = list(range(p+1, S))
    ro_bands = {f"early0-{third-1}": set(range(0, third)),
                f"mid{third}-{2*third-1}": set(range(third, 2*third)),
                f"late{2*third}-{nL-1}": set(range(2*third, nL)),
                f"postinj2-{Linj+2}-{nL-1}": set(range(Linj+2, nL)),
                f"postinj3-{Linj+3}-{nL-1}": set(range(Linj+3, nL))}
    for bn, bs in ro_bands.items():
        cfgs.append((f"s3-block-{bn}",
                     [spec1, {"rows": far, "cols": relay_cols, "layers": bs, "keep_diag": True}]))
    cfgs.append(("s3-block-all",
                 [spec1, {"rows": far, "cols": relay_cols, "layers": None, "keep_diag": True}]))
    return cfgs, bands

# clean greedy continuation cache (patch/ablation off -> deterministic per prompt)
_GREEDY_CACHE = {}
def greedy_seq(model, tok, pr):
    if pr not in _GREEDY_CACHE:
        ids = tok(pr, return_tensors="pt").input_ids
        ABLATE["on"] = False; patch.on = False
        cur = ids.clone()
        for _ in range(HA):
            nxt = model(cur).logits[0, -1].argmax().view(1, 1)
            cur = torch.cat([cur, nxt], 1)
        _GREEDY_CACHE[pr] = (cur, ids.shape[1] - 1)
    return _GREEDY_CACHE[pr]

# ---------------- main experiment ----------------
def run_cell(model, tok, direction, Linj, blocks, nL):
    print("\n" + "#"*78)
    print(f"# S82 DEPTH-LAW @24 LAYERS — MODEL: {MODEL_NAME} direction={direction} "
          f"INJECT-BLOCK={Linj} (rel depth {Linj/nL:.2f})")
    print("#"*78)
    READOUT = nL - 1; ro = READOUT + 1
    third = nL // 3
    handle = blocks[Linj].register_forward_hook(make_hook())
    print(f"[setup] nL={nL} inject-block={Linj} readout-block={READOUT} HA={HA} FAR_W={FAR_W}")

    ABLATE["on"] = False; patch.on = False
    what, wn = concept_dir(model, tok, direction, Linj)
    what_t = torch.tensor(what, dtype=torch.float32)
    print(f"[setup] ||W|| = {wn:.2f} target = 3||W||")

    D = {}
    base_all = []
    alloc = defaultdict(list)
    band_names = None
    for pr in AVG_PROMPTS:
        seq, p = greedy_seq(model, tok, pr)
        S = seq.shape[1]
        far_idx = list(range(S - FAR_W, S))
        cfgs, bands = build_configs(p, S, nL, Linj)
        band_names = list(bands.keys())
        assert p + 9 <= far_idx[0], "FAR not severed in k=8 regime"

        patch.dir = what_t; patch.target = 3.0*wn; patch.positions = [p]

        # baseline pair with allocation recording at layers 22/23
        ABLATE["on"] = False; patch.on = False
        RECORD["data"] = {}; RECORD["on"] = True
        hc = fwd_hs(model, seq); rec_c = dict(RECORD["data"])
        RECORD["data"] = {}
        patch.on = True
        hp = fwd_hs(model, seq); rec_p = dict(RECORD["data"])
        patch.on = False; RECORD["on"] = False
        base_all.append(np.mean([decomp((hp[ro][0,pos]-hc[ro][0,pos]).numpy(), what)[1]
                                 for pos in far_idx]))
        for L in ALLOC_LAYERS:
            pc, vc = rec_c[L]["probs"], rec_c[L]["value"]
            pp_, vp_ = rec_p[L]["probs"], rec_p[L]["value"]
            alloc[(L, "a_p_clean")].append(float(np.mean([pc[:, i, p].mean().item() for i in far_idx])))
            alloc[(L, "a_p_patch")].append(float(np.mean([pp_[:, i, p].mean().item() for i in far_idx])))
            alloc[(L, "a_p_maxh")].append(float(np.mean([pc[:, i, p].max().item() for i in far_idx])))
            alloc[(L, "dv_p")].append(float((vp_[:, p] - vc[:, p]).reshape(-1).norm().item()))
            amass = {"sink0": [0], "pre": list(range(1, p)), "p": [p],
                     "car": list(range(p+1, p+9)), "post": list(range(p+9, S))}
            for g, js in amass.items():
                alloc[(L, "amass", g)].append(float(np.mean(
                    [pc[:, i, js].sum(dim=-1).mean().item() for i in far_idx])))

        for name, specs in cfgs:
            ABLATE.update(on=True, specs=specs); patch.on = False
            hck = fwd_hs(model, seq)
            patch.on = True
            hk = fwd_hs(model, seq)
            patch.on = False; ABLATE["on"] = False; ABLATE["specs"] = []
            d = np.mean([decomp((hk[ro][0,pos]-hck[ro][0,pos]).numpy(), what)[1]
                         for pos in far_idx])
            D.setdefault(name, []).append(d)
    handle.remove()

    B = float(np.mean(base_all))
    Dm = {n: float(np.mean(v)) for n, v in D.items()}
    R = Dm["s3-relay-ref-k8"]
    A = {k: float(np.mean(v)) for k, v in alloc.items()}
    print(f"\n[baseline] B (no ablation, FAR out-span deflection) = {B:.4f}")

    def row(n, denom=B, extra=""):
        r = Dm[n]/denom if denom > 1e-9 else float('nan')
        print(f"  {n:>28} {Dm[n]:10.6f} {r:9.3f}  {extra}")

    print(f"\n--- SWEEP 1: keep-only export profile (attn-to-p at ONE layer; ratio = D/B) ---")
    print(f"  {'config':>28} {'D_far':>10} {'ratio':>9}")
    for L in range(Linj, nL):
        note = "(control: expect EXACT 0)" if L == Linj else f"(offset +{L-Linj})"
        row(f"s1-keep-L{L:02d}", extra=note)
    for bn in band_names:
        note = "(expect EXACT 0)" if bn.startswith("postinj") else ""
        row(f"s1-band-{bn}", extra=note)
    row("ctl-k0-all", extra="(expect EXACT 0)")
    row("ctl-noop", extra="(mask-apparatus check: expect 1.000)")

    print(f"\n--- SWEEP 3: relay-readout depth (k=8 regime + FAR blocked from post-p cols at band) ---")
    print(f"  {'config':>28} {'D_far':>10} {'D/R':>9}   (R = relay reference)")
    rb = R/B if B > 1e-9 else float('nan')
    row("s3-relay-ref-k8", denom=B, extra=f"(R/B = {rb:.3f})")
    for bn in [f"early0-{third-1}", f"mid{third}-{2*third-1}", f"late{2*third}-{nL-1}",
               f"postinj2-{Linj+2}-{nL-1}", f"postinj3-{Linj+3}-{nL-1}"]:
        if bn.startswith("postinj2"):
            note = "(expect EXACT 0: hop-timing floor)"
        elif bn.startswith("postinj3"):
            note = "(floor tightness: >0 iff readout AT L_inj+2 usable)"
        elif bn.startswith("late") and Linj + 2 >= 2*third:
            note = "(expect EXACT 0: late band covers all >= L_inj+2)"
        else:
            note = ""
        row(f"s3-block-{bn}", denom=R, extra=note)
    row("s3-block-all", denom=R, extra="(expect EXACT 0)")

    print(f"\n--- ALLOCATION TABLE at last two layers (noablate baseline pair; mean FAR rows) ---")
    print(f"  {'L':>3} {'a_p clean':>11} {'a_p patch':>11} {'a_p maxh':>10} {'|dv_p|':>8} "
          f"{'sink(j=0)':>10} {'pre':>8} {'j=p':>10} {'carriers':>9} {'post':>8}")
    for L in ALLOC_LAYERS:
        print(f"  {L:>3} {A[(L,'a_p_clean')]:11.6f} {A[(L,'a_p_patch')]:11.6f} "
              f"{A[(L,'a_p_maxh')]:10.6f} {A[(L,'dv_p')]:8.3f} "
              f"{A[(L,'amass','sink0')]:10.4f} {A[(L,'amass','pre')]:8.4f} "
              f"{A[(L,'amass','p')]:10.6f} {A[(L,'amass','car')]:9.4f} {A[(L,'amass','post')]:8.4f}")

    return dict(direction=direction, Linj=Linj, B=B, D=Dm, R=R, nL=nL, A=A, wn=wn,
                third=third)

# ======================= RUN =======================
tok, model = load(MODEL_NAME)
nL = model.config.num_hidden_layers
blocks = model.gpt_neox.layers
assert nL == 24, f"expected 24 layers, got {nL}"
print(f"[model] {MODEL_NAME} nL={nL} hidden={model.config.hidden_size} "
      f"heads={model.config.num_attention_heads} dtype={next(model.parameters()).dtype}")

results = []
for Linj in INJECT_BLOCKS:
    for dr in ["valence", "size"]:
        results.append(run_cell(model, tok, dr, Linj, blocks, nL))

print("\n" + "="*78)
print("SUMMARY — DEPTH-LAW TRANSFER TO 24 LAYERS (pythia-410m)")
print("="*78)
for r in results:
    B, Dm, R, Linj, third = r["B"], r["D"], r["R"], r["Linj"], r["third"]
    keeps = {L: Dm[f"s1-keep-L{L:02d}"]/B for L in range(Linj, nL)}
    best_keep = max(keeps, key=keeps.get)
    late_bn = f"late{2*third}-{nL-1}"
    print(f"\n  [{r['direction']}] inj={Linj} (rel {Linj/nL:.2f})  B={B:.3f}  R/B={R/B:.3f}")
    print(f"    controls: k0={Dm['ctl-k0-all']/B:.6f} noop={Dm['ctl-noop']/B:.6f} "
          f"keepL{Linj:02d}={Dm[f's1-keep-L{Linj:02d}']/B:.6f} "
          f"postinj-band={Dm[f's1-band-postinj{Linj+1}-{nL-1}']/B:.6f} "
          f"s3-all={Dm['s3-block-all']/R if R>1e-9 else float('nan'):.6f} "
          f"s3-postinj2={Dm[f's3-block-postinj2-{Linj+2}-{nL-1}']/R if R>1e-9 else float('nan'):.6f}")
    print(f"    keep-only by offset: " +
          " ".join(f"+{L-Linj}:{keeps[L]:.2f}" for L in sorted(keeps) if L > Linj))
    print(f"    strongest sole exporter = L{best_keep} (offset +{best_keep-Linj}); "
          f"H1 predicts +1")
    print(f"    readout blocks D/R: early={Dm[f's3-block-early0-{third-1}']/R:.2f} "
          f"mid={Dm[f's3-block-mid{third}-{2*third-1}']/R:.2f} "
          f"late={Dm[f's3-block-{late_bn}']/R:.2f} "
          f"postinj3={Dm[f's3-block-postinj3-{Linj+3}-{nL-1}']/R:.2f}")
    A = r["A"]
    print(f"    allocation: a_p L22={A[(22,'a_p_clean')]:.6f} (maxh {A[(22,'a_p_maxh')]:.6f}) "
          f"L23={A[(23,'a_p_clean')]:.6f} (maxh {A[(23,'a_p_maxh')]:.6f}) "
          f"|dv_p| L23={A[(23,'dv_p')]:.2f}  keepL22={keeps.get(22,float('nan')):.3f} "
          f"keepL23={keeps.get(23,float('nan')):.3f}")

# global exactness gates (S78-S80 convention: <1e-4 relative)
def g(cond, label):
    print(f"[GLOBAL] {label:<57} {cond}")
    return cond

print()
ok = []
ok.append(g(all(abs(r["D"]["ctl-k0-all"]/r["B"]) < 1e-4 for r in results),
            "k=0 exact-0 in all cells:"))
ok.append(g(all(abs(r["D"][f"s1-keep-L{r['Linj']:02d}"]/r["B"]) < 1e-4 for r in results),
            "keep-only-Linj exact-0 (injection-locus control):"))
ok.append(g(all(abs(r["D"][f"s1-band-postinj{r['Linj']+1}-{nL-1}"]/r["B"]) < 1e-4 for r in results),
            "postinj-band exact-0 (all edit edges severed):"))
ok.append(g(all(abs(r["D"]["ctl-noop"]/r["B"] - 1.0) < 1e-3 for r in results),
            "noop == baseline (mask apparatus):"))
ok.append(g(all(abs(r["D"]["s3-block-all"]/r["R"]) < 1e-4 for r in results if r["R"] > 1e-9),
            "s3-block-all exact-0:"))
ok.append(g(all(abs(r["D"][f"s3-block-postinj2-{r['Linj']+2}-{nL-1}"]/r["R"]) < 1e-4
                for r in results if r["R"] > 1e-9),
            "s3-block-postinj2 exact-0 (hop-timing floor):"))
ok.append(g(all(abs(r["D"][f"s3-block-late{2*r['third']}-{nL-1}"]/r["R"]) < 1e-4
                for r in results if r["Linj"] + 2 >= 2*r["third"] and r["R"] > 1e-9),
            "inj18 block-late exact-0 (late covers >= L_inj+2):"))
print(f"[GLOBAL] sdpa recorder max recon err: {RECORD['maxerr']:.2e}")

print("\n" + "="*78)
print("VERDICT SYNTHESIS (automatic; verify against tables above)")
print("="*78)
for r in results:
    B, Dm, R, Linj, third = r["B"], r["D"], r["R"], r["Linj"], r["third"]
    keeps = {L: Dm[f"s1-keep-L{L:02d}"]/B for L in range(Linj, nL)}
    best = max(keeps, key=keeps.get)
    h1 = "PEAK AT +1 (absolute-offset)" if best == Linj+1 else \
         f"PEAK AT +{best-Linj} (NOT +1 — check fractional scaling)"
    pi3 = Dm[f"s3-block-postinj3-{Linj+3}-{nL-1}"]/R if R > 1e-9 else float('nan')
    h2 = f"floor exact-0; tightness postinj3 D/R={pi3:.3f} " + \
         ("(readout AT L_inj+2 usable)" if pi3 > 0.05 else "(readout at L_inj+2 NOT usable alone)")
    if Linj + 2 < 2*third:
        late = Dm[f"s3-block-late{2*third}-{nL-1}"]/R if R > 1e-9 else float('nan')
        h3 = f"block-late D/R={late:.3f} => " + \
             ("readout NOT pinned late (RELATIVE transfers)" if late > 0.05 else
              "readout pinned late (ABSOLUTE at 24L!)")
    else:
        h3 = "late band structural control (see gates)"
    a23 = r["A"][(23, "a_p_clean")]
    h4 = f"a_p(L23)={a23:.6f}, keepL23={keeps.get(23,float('nan')):.3f} => " + \
         ("ALLOCATION ZERO REPLICATES" if a23 < 1e-3 else "allocation NOT zero at L23")
    print(f"\n  [{r['direction']}] inj={Linj}:")
    print(f"    H1 export offset: {h1}")
    print(f"    H2 floor: {h2}")
    print(f"    H3 late-pinning: {h3}")
    print(f"    H4 final-layer allocation: {h4}")

print(f"\n[wall-clock] {time.time()-T0:.1f} s")
