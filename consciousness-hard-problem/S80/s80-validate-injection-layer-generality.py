#!/usr/bin/env python3
# s80-validate-injection-layer-generality.py
# VALIDATE (UPR Session 80, Consciousness Hard Problem, Track C).
#
# TARGET: S79 residue #7 / S78 queued VALIDATE — injection-layer generality of the relay
# path law. S79 (injection at block 6 only) found:
#   EXPORT   depth-local: attn-to-p at L_inject+1..+2 dominates (keep-only-L7 recovers
#            45-99% of baseline); layers <= L_inject exactly nothing.
#   READOUT  exclusively late (8-11): blocking FAR's post-p attention at 8-11 kills the
#            relay EXACTLY (4/4 cells).
# But with L_inject=6, "L_inject+1..+2" == "layers 7-8" and "readout >= L_inject+2" ==
# "readout >= 8" — RELATIVE depth and ABSOLUTE depth are confounded. This session breaks
# the confound by injecting at blocks 3 and 9.
#
#   RELATIVE-DEPTH LAW predicts: export peak tracks L_inj+1..+2 (inj3 -> L4-L5 dominant;
#     inj9 -> L10 dominant); readout available from L_inj+2 on (inj3 -> blocking late
#     8-11 does NOT kill the relay, mid-layers 5-7 can read it).
#   ABSOLUTE-DEPTH LAW predicts: export/readout pinned late regardless (inj3 -> keep-only
#     L4-L6 weak, L7-L8 strong; blocking late 8-11 kills relay exactly even for inj3).
#
# COMPACT CORE (from S79, drop-one and single-gate sweeps omitted):
#   SWEEP 1 (keep-only export profile): attn-to-p available at ONE layer only, for
#     L = L_inj..nL-1; plus fixed bands early0-3 / mid4-7 / late8-11 / postinj(L_inj+1..11).
#   SWEEP 3 (relay-readout depth): S78 k=8 regime (reference R), FAR additionally severed
#     from ALL post-p columns at one band: early0-3 / mid4-7 / late8-11 /
#     postinj2(L_inj+2..11) / all.
#
# STRUCTURAL EXACT-0 PREDICTIONS (law-independent, from injection locus + hop timing):
#   ctl-k0-all             EXACT 0  (all rows > p severed from p at all layers)
#   s1-keep-L{L_inj}       EXACT 0  (K/V at p at layers <= L_inj computed pre-injection)
#   s1-band-postinj        EXACT 0  (every edit-carrying attention-to-p edge severed)
#   s3-block-all           EXACT 0  (FAR severed from p AND all post-p columns)
#   s3-block-postinj2      EXACT 0  (NEW: export needs L1 >= L_inj+1, carrier K/V carries
#                                    the edit only at layers >= L1+1 >= L_inj+2; blocking
#                                    FAR's post-p readout at L_inj+2..11 leaves no path)
#   ctl-noop               ratio 1.0 (explicit-mask path == SDPA fast path)
# Gates: 6-decimal zeros in per-cell prints; <1e-4 relative in global gates (S78/S79
# convention).
#
# DISCRIMINATOR CELLS:
#   inj3 keep-only peak: L4/L5 (relative) vs L7/L8 (absolute).
#   inj3 s3-block-late8-11: > 0 (relative: mid readout 5-7 exists) vs exact 0 (absolute).
#   inj9: compressed-relay corner — relative law leaves exactly one 2-hop path
#     (export L10, readout L11); check it exists and check the S79 keep-only-L11
#     gpt2/pythia split at the new depths (diagnostic for absolute-depth readout).
#
# Referencing (S78 confound fix, unchanged): for every config c,
#     D(c) = mean_FAR outspan( h_inject_c - h_clean_c ) at readout block nL-1,
#   with ablation ON in both forwards; B = D(no ablation); ratios D(c)/B (sweep 3: D/R).
# Setup otherwise identical to S79: do(W := W*) at p (last prompt token) via forward hook
# on block L_inj output, target 3*||W|| (direction computed at block L_inj), out-span-
# preserving; teacher-forced clean-greedy continuation HA=12; FAR = last 3 positions;
# gpt2 (124M) + EleutherAI/pythia-160m; valence + size; 5 prompts; SEED=80; CPU.
# NaN-safe layer-aware SDPA additive-mask ablation (S78/S79) verbatim.
#
# Run: .venv-s75/bin/python s80-validate-injection-layer-generality.py
import time, random
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

SEED = 80
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
torch.set_grad_enabled(False)
T0 = time.time()

INJECT_BLOCKS = [3, 9]

# ---- concept probe sets (identical to S77/S78/S79) ----
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

HA = 12      # teacher-forced continuation length
FAR_W = 3    # far window = last FAR_W positions

# ---------------- layer-aware SDPA ablation monkeypatch (S78/S79 verbatim) ----------------
_real_sdpa = torch.nn.functional.scaled_dot_product_attention
ABLATE = {"on": False, "specs": []}   # spec: {rows:[...], cols:[...], layers:set|None, keep_diag:bool}
LAYER = {"i": 0}

def patched_sdpa(query, key, value, attn_mask=None, dropout_p=0.0, is_causal=False,
                 scale=None, **kw):
    if not ABLATE["on"]:
        return _real_sdpa(query, key, value, attn_mask=attn_mask, dropout_p=dropout_p,
                          is_causal=is_causal, scale=scale, **kw)
    L = LAYER["i"]; LAYER["i"] += 1
    q_len = query.shape[-2]; k_len = key.shape[-2]; dev = query.device
    i = torch.arange(q_len, device=dev)[:, None]
    j = torch.arange(k_len, device=dev)[None, :]
    causal = j <= i
    mask = torch.zeros(q_len, k_len, dtype=query.dtype, device=dev)
    mask = mask.masked_fill(~causal, float("-inf"))
    for spec in ABLATE["specs"]:
        if spec["layers"] is not None and L not in spec["layers"]:
            continue
        rb = torch.zeros(q_len, dtype=torch.bool, device=dev); rb[spec["rows"]] = True
        cb = torch.zeros(k_len, dtype=torch.bool, device=dev); cb[spec["cols"]] = True
        block = rb[:, None] & cb[None, :]
        if spec.get("keep_diag", True):
            block &= ~(i == j)
        mask = mask.masked_fill(block, float("-inf"))
    mask = mask.view(1, 1, q_len, k_len)
    return _real_sdpa(query, key, value, attn_mask=mask, dropout_p=dropout_p,
                      is_causal=False, scale=scale, **kw)

torch.nn.functional.scaled_dot_product_attention = patched_sdpa

# ---------------- model helpers (S77/S78/S79) ----------------
def block_list(model, family):
    return model.transformer.h if family == "gpt2" else model.gpt_neox.layers

def load(model_name, family):
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, attn_implementation="sdpa"); model.eval()
    return tok, model

def resid_after_block(model, tok, text, L):
    ids = tok(text, return_tensors="pt").input_ids
    hs = model(ids, output_hidden_states=True).hidden_states
    return hs[L + 1][0, -1].numpy()

def concept_dir(model, tok, name, L):
    pos, neg = CONCEPTS[name]
    mp = np.mean([resid_after_block(model, tok, t, L) for t in pos], axis=0)
    mn = np.mean([resid_after_block(model, tok, t, L) for t in neg], axis=0)
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

# ---------------- config builder (compact core, parameterized by Linj) ----------------
def build_configs(p, S, nL, Linj):
    rows_all = list(range(p+1, S))
    far = list(range(S-FAR_W, S))
    def sever_p(rows, layers):
        return {"rows": rows, "cols": [p], "layers": layers, "keep_diag": True}
    bands = {"early0-3": set(range(0,4)), "mid4-7": set(range(4,8)),
             "late8-11": set(range(8,nL)),
             f"postinj{Linj+1}-{nL-1}": set(range(Linj+1, nL))}
    cfgs = []
    # sweep 1: keep-only export profile + bands
    for L in range(Linj, nL):
        cfgs.append((f"s1-keep-L{L:02d}", [sever_p(rows_all, set(range(nL)) - {L})]))
    for bn, bs in bands.items():
        cfgs.append((f"s1-band-{bn}", [sever_p(rows_all, bs)]))
    cfgs.append(("ctl-k0-all", [sever_p(rows_all, None)]))
    cfgs.append(("ctl-noop", []))
    # sweep 3: relay-readout depth (regime = S78 k=8)
    spec1 = sever_p(list(range(p+9, S)), None)
    cfgs.append(("s3-relay-ref-k8", [spec1]))
    relay_cols = list(range(p+1, S))
    ro_bands = {"early0-3": set(range(0,4)), "mid4-7": set(range(4,8)),
                "late8-11": set(range(8,nL)),
                f"postinj2-{Linj+2}-{nL-1}": set(range(Linj+2, nL))}
    for bn, bs in ro_bands.items():
        cfgs.append((f"s3-block-{bn}",
                     [spec1, {"rows": far, "cols": relay_cols, "layers": bs, "keep_diag": True}]))
    cfgs.append(("s3-block-all",
                 [spec1, {"rows": far, "cols": relay_cols, "layers": None, "keep_diag": True}]))
    return cfgs

# ---------------- main experiment ----------------
def run_cell(model_name, family, tok, model, direction, Linj):
    print("\n" + "#"*78)
    print(f"# INJECTION-LAYER GENERALITY — MODEL: {model_name} (family={family}) "
          f"direction={direction} INJECT-BLOCK={Linj}")
    print("#"*78)
    nL = model.config.n_layer if family=="gpt2" else model.config.num_hidden_layers
    READOUT = nL-1; ro = READOUT+1
    blocks = block_list(model, family)
    handle = blocks[Linj].register_forward_hook(make_hook())
    print(f"[setup] nL={nL} inject-block={Linj} readout-block={READOUT} HA={HA} FAR_W={FAR_W}")

    ABLATE["on"]=False; patch.on=False
    what, wn = concept_dir(model, tok, direction, Linj)
    what_t = torch.tensor(what, dtype=torch.float32)

    D = {}
    base_all = []
    for pr in AVG_PROMPTS:
        ids = tok(pr, return_tensors="pt").input_ids
        p = ids.shape[1]-1
        ABLATE["on"]=False; patch.on=False
        cur = ids.clone()
        for _ in range(HA):
            nxt = model(cur).logits[0,-1].argmax().view(1,1); cur = torch.cat([cur,nxt],1)
        seq = cur; S = seq.shape[1]
        far_idx = list(range(S-FAR_W, S))
        cfgs = build_configs(p, S, nL, Linj)
        assert p + 9 <= far_idx[0], "FAR not severed in k=8 regime"

        patch.dir = what_t; patch.target = 3.0*wn; patch.positions = [p]

        ABLATE["on"]=False; patch.on=False
        hc = fwd_hs(model, seq)
        patch.on=True
        hp = fwd_hs(model, seq)
        patch.on=False
        base_all.append(np.mean([decomp((hp[ro][0,pos]-hc[ro][0,pos]).numpy(), what)[1]
                                 for pos in far_idx]))

        for name, specs in cfgs:
            ABLATE.update(on=True, specs=specs); patch.on=False
            hck = fwd_hs(model, seq)
            patch.on=True
            hk = fwd_hs(model, seq)
            patch.on=False; ABLATE["on"]=False; ABLATE["specs"]=[]
            d = np.mean([decomp((hk[ro][0,pos]-hck[ro][0,pos]).numpy(), what)[1]
                         for pos in far_idx])
            D.setdefault(name, []).append(d)
    handle.remove()

    B = float(np.mean(base_all))
    Dm = {n: float(np.mean(v)) for n,v in D.items()}
    R = Dm["s3-relay-ref-k8"]
    print(f"\n[baseline] B (no ablation, FAR out-span deflection) = {B:.4f}")

    def row(n, denom=B, extra=""):
        r = Dm[n]/denom if denom > 1e-9 else float('nan')
        print(f"  {n:>26} {Dm[n]:10.6f} {r:9.3f}  {extra}")

    print(f"\n--- SWEEP 1: keep-only export profile (attn-to-p at ONE layer; ratio = D/B) ---")
    print(f"  {'config':>26} {'D_far':>10} {'ratio':>9}")
    for L in range(Linj, nL):
        note = "(control: expect EXACT 0)" if L == Linj else "(sole export layer)"
        row(f"s1-keep-L{L:02d}", extra=note)
    for bn in ["early0-3","mid4-7","late8-11",f"postinj{Linj+1}-{nL-1}"]:
        note = "(expect EXACT 0)" if bn.startswith("postinj") else ""
        row(f"s1-band-{bn}", extra=note)
    row("ctl-k0-all", extra="(expect EXACT 0)")
    row("ctl-noop", extra="(mask-apparatus check: expect 1.000)")

    print(f"\n--- SWEEP 3: relay-readout depth (k=8 regime + FAR blocked from post-p cols at band) ---")
    print(f"  {'config':>26} {'D_far':>10} {'D/R':>9}   (R = relay reference)")
    rb = R/B if B > 1e-9 else float('nan')
    row("s3-relay-ref-k8", denom=B, extra=f"(R/B = {rb:.3f})")
    for bn in ["early0-3","mid4-7","late8-11",f"postinj2-{Linj+2}-{nL-1}"]:
        note = "(expect EXACT 0: hop-timing floor)" if bn.startswith("postinj2") else ""
        row(f"s3-block-{bn}", denom=R, extra=note)
    row("s3-block-all", denom=R, extra="(expect EXACT 0)")

    return dict(model=model_name, family=family, direction=direction, Linj=Linj,
                B=B, D=Dm, R=R, nL=nL)

# ======================= RUN =======================
MODELS = [("gpt2","gpt2"), ("EleutherAI/pythia-160m","pythia")]
results = []
for mn, fam in MODELS:
    tok, model = load(mn, fam)
    for Linj in INJECT_BLOCKS:
        for dr in ["valence","size"]:
            results.append(run_cell(mn, fam, tok, model, dr, Linj))
    del model

print("\n" + "="*78)
print("CROSS-MODEL SUMMARY — INJECTION-LAYER GENERALITY (relative vs absolute depth)")
print("="*78)
for r in results:
    B, Dm, nL, Linj, R = r["B"], r["D"], r["nL"], r["Linj"], r["R"]
    keeps = {L: Dm[f"s1-keep-L{L:02d}"]/B for L in range(Linj, nL)}
    best_keep = max(keeps, key=keeps.get)
    late_ro = Dm["s3-block-late8-11"]/R if R > 1e-9 else float('nan')
    print(f"\n  {r['model']} [{r['direction']}] inj={Linj}  B={B:.3f}  R/B={R/B:.3f}")
    print(f"    controls: k0={Dm['ctl-k0-all']/B:.6f} noop={Dm['ctl-noop']/B:.6f} "
          f"keepL{Linj:02d}={Dm[f's1-keep-L{Linj:02d}']/B:.6f} "
          f"postinj-band={Dm[f's1-band-postinj{Linj+1}-{nL-1}']/B:.6f} "
          f"s3-all={Dm['s3-block-all']/R if R>1e-9 else float('nan'):.6f} "
          f"s3-postinj2={Dm[f's3-block-postinj2-{Linj+2}-{nL-1}']/R if R>1e-9 else float('nan'):.6f}")
    print(f"    keep-only: " + " ".join(f"L{L}:{keeps[L]:.2f}" for L in sorted(keeps))
          + f" | strongest-sole-exporter=L{best_keep}"
          + f" | rel-law-predicts=L{Linj+1}/L{Linj+2}")
    print(f"    readout blocks D/R: early={Dm['s3-block-early0-3']/R if R>1e-9 else float('nan'):.2f} "
          f"mid={Dm['s3-block-mid4-7']/R if R>1e-9 else float('nan'):.2f} "
          f"late={late_ro:.2f}"
          + ("  [inj3 discriminator: late>0 => RELATIVE, late==0 => ABSOLUTE]" if Linj==3 else ""))

# global exactness gates (S78/S79 convention: <1e-4 relative)
ok_k0 = all(abs(r["D"]["ctl-k0-all"]/r["B"]) < 1e-4 for r in results)
ok_keepinj = all(abs(r["D"][f"s1-keep-L{r['Linj']:02d}"]/r["B"]) < 1e-4 for r in results)
ok_postinj = all(abs(r["D"][f"s1-band-postinj{r['Linj']+1}-{r['nL']-1}"]/r["B"]) < 1e-4 for r in results)
ok_noop = all(abs(r["D"]["ctl-noop"]/r["B"] - 1.0) < 1e-3 for r in results)
ok_s3all = all(abs(r["D"]["s3-block-all"]/r["R"]) < 1e-4 for r in results if r["R"] > 1e-9)
ok_pi2 = all(abs(r["D"][f"s3-block-postinj2-{r['Linj']+2}-{r['nL']-1}"]/r["R"]) < 1e-4
             for r in results if r["R"] > 1e-9)
print(f"\n[GLOBAL] k=0 exact-0 in all cells:                         {ok_k0}")
print(f"[GLOBAL] keep-only-Linj exact-0 (injection-locus control): {ok_keepinj}")
print(f"[GLOBAL] postinj-band exact-0 (all edit edges severed):    {ok_postinj}")
print(f"[GLOBAL] noop == baseline (mask apparatus):                {ok_noop}")
print(f"[GLOBAL] s3-block-all exact-0:                             {ok_s3all}")
print(f"[GLOBAL] s3-block-postinj2 exact-0 (hop-timing floor):     {ok_pi2}")

# verdict synthesis
print("\n" + "="*78)
print("VERDICT SYNTHESIS (automatic; verify against tables above)")
print("="*78)
for r in results:
    B, Dm, nL, Linj, R = r["B"], r["D"], r["nL"], r["Linj"], r["R"]
    keeps = {L: Dm[f"s1-keep-L{L:02d}"]/B for L in range(Linj, nL)}
    rel_mass = max(keeps.get(Linj+1, 0.0), keeps.get(Linj+2, 0.0))
    abs_mass = max((keeps[L] for L in (7, 8) if L in keeps and L > Linj), default=0.0)
    if Linj == 3:
        exp_verdict = "RELATIVE" if rel_mass > abs_mass else "ABSOLUTE"
        late_ro = Dm["s3-block-late8-11"]/R if R > 1e-9 else float('nan')
        ro_verdict = "RELATIVE (mid readout survives)" if late_ro > 0.05 else \
                     "ABSOLUTE (late-only readout)"
        print(f"  {r['model']} [{r['direction']}] inj=3: export peak L{max(keeps,key=keeps.get)} "
              f"(rel-mass {rel_mass:.2f} vs L7/L8 {abs_mass:.2f}) => {exp_verdict}; "
              f"block-late D/R={late_ro:.3f} => readout {ro_verdict}")
    else:
        print(f"  {r['model']} [{r['direction']}] inj=9: R/B={R/B:.3f}; "
              f"keep-only L10:{keeps.get(10,float('nan')):.2f} L11:{keeps.get(11,float('nan')):.2f} "
              f"(rel law: L10/L11 only possible exporters); "
              f"keep-L11 split check: {keeps.get(11,float('nan')):.3f}")

print(f"\n[wall-clock] {time.time()-T0:.1f} s")
