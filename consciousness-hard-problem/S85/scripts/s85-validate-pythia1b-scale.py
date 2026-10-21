#!/usr/bin/env python3
# s85-validate-pythia1b-scale.py
# VALIDATE (UPR Session 85, Consciousness Hard Problem, Track C).
#
# TARGET (S84 handoff primary): third *within-family* pythia scale point on the
# allocation-suppression curve
#   prior: pythia-160m L11 a_FAR,p ≈ 0          (S81 exact zero)
#          pythia-410m L23 a_FAR,p ≈ 3.2e-4     (S82)
#          gpt2-124M   L11 a_FAR,p ≈ 1.42e-2    (S84 re-anchor)
#          gpt2-medium L23 a_FAR,p = 2.01e-2    (S84; family outgroup, NO island)
# Expect either deeper suppression, plateau, or a new interior island at 1B / 16L.
#
# SCOPE DISCIPLINE: ONE new model — EleutherAI/pythia-1b (16 layers).
# Optional light re-anchor of pythia-410m final a_p ONLY if cheap and RAM allows.
#
# METHOD (lean VALIDATE, same apparatus as S84):
#   1. Clean-forward allocation scan a_FAR,p mean/max-head/per-head across ALL layers
#      (injection-independent by construction — island is a property of clean attention).
#   2. Final-layer a_FAR,p as the curve point (comparable to S81/S82/S84 final-layer tables).
#   3. Island detector: layers where mean a_FAR,p and/or max-head a_FAR,p spike vs
#      neighbors by ≥10× (S83 L21 was 40–60× L22/23); flag top head(s).
#   4. Behavioral counterpart: keep-only-L* export D/B at {final, L_inj+1, peak, any
#      flagged} under late inj. For 16L: Linj=12 so 3 post layers remain (13,14,15).
#   5. Optional: light re-anchor pythia-410m final a_p (clean scan only) if RAM allows.
#
# Apparatus: S78–S84 SDPA monkeypatch + in-mask recorder; ablation-matched D =
# mean_FAR outspan(h_p - h_c) at hs[nL]; do(W := 3||W||) at p; HA=12; FAR_W=3;
# same AVG_PROMPTS/CONCEPTS; SEED=85; CPU; float32 forced; .venv-s75.
#
# Gates:
#   g1 sdpa recon max abs err < 5e-3
#   g2 nL == 16 for pythia-1b
#   g3 keep-only-L_inj D == 0 (structural; no export from injection layer alone via attn-to-p)
#   g4 k0 (sever all post-p → p) D == 0
#   g5 injection out-span/in-span at hs[L_inj+1] rel < 1e-2
#   g6 final-layer a_p clean is finite, non-NaN, in [0,1]
#   g7 island detector runs (at least one layer scanned with H heads)
#
# Run: .venv-s75/bin/python s85-validate-pythia1b-scale.py 2>&1 | tee s85-output.txt
import math, time, random, gc, os, sys
from collections import defaultdict
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

SEED = 85
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
torch.set_grad_enabled(False)
T0 = time.time()

# Primary: pythia-1b (16L within-family scale point). Optional 410m re-anchor.
PRIMARY = "EleutherAI/pythia-1b"
ANCHOR_410M = "EleutherAI/pythia-410m"  # optional light final-a_p re-anchor
INJECT_PRIMARY = 12          # late inj for 16L: 3 post layers remain (13,14,15)
HA = 12
FAR_W = 3

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

# Prior curve anchors (this project's literature; not re-run unless ANCHOR path)
PRIOR_CURVE = [
    ("pythia-160m", "EleutherAI/pythia-160m", 12, 11, 0.0, "S81 exact zero"),
    ("pythia-410m", "EleutherAI/pythia-410m", 24, 23, 3.16e-4, "S82 ~3e-4"),
    ("gpt2-124M", "gpt2", 12, 11, 1.42e-2, "S84 re-anchor"),
    ("gpt2-medium", "gpt2-medium", 24, 23, 2.01e-2, "S84 outgroup NO island"),
]

# ------------- layer-aware SDPA ablation + in-mask recorder (S78–S84) -------------
_real_sdpa = torch.nn.functional.scaled_dot_product_attention
ABLATE = {"on": False, "specs": []}
RECORD = {"on": False, "layers": set(), "data": {}, "maxerr": 0.0}
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
        RECORD["data"][L] = {"probs": probs.clone(), "value": v.clone(), "key": k.clone()}
    return ret

torch.nn.functional.scaled_dot_product_attention = patched_sdpa

# ---------------- model helpers ----------------
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

def get_blocks(model):
    if hasattr(model, "transformer") and hasattr(model.transformer, "h"):
        return model.transformer.h, "gpt2"
    if hasattr(model, "gpt_neox") and hasattr(model.gpt_neox, "layers"):
        return model.gpt_neox.layers, "pythia"
    raise RuntimeError("unknown architecture")

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
    def __init__(self):
        self.dir = None; self.target = 0.0; self.positions = None; self.on = False
patch = Patch()

def make_hook():
    def hook(module, inp, out):
        if not patch.on:
            return out
        h = out[0] if isinstance(out, tuple) else out
        dhat = patch.dir.to(h.dtype)
        pos = patch.positions if patch.positions is not None else range(h.shape[1])
        for p in pos:
            cur = torch.dot(h[0, p], dhat)
            h[0, p] = h[0, p] - cur * dhat + patch.target * dhat
        if isinstance(out, tuple):
            return (h,) + tuple(out[1:])
        return h
    return hook

def decomp(dv_np, what):
    inspan = np.dot(dv_np, what)
    outspan_vec = dv_np - inspan * what
    return abs(float(inspan)), float(np.linalg.norm(outspan_vec))

def fwd_hs(model, seq):
    LAYER["i"] = 0
    hs = model(seq, output_hidden_states=True).hidden_states
    assert not torch.isnan(hs[-1]).any(), "NaN in hidden states (ablation mask bug?)"
    return hs

def fwd_rec(model, seq, patched):
    RECORD["data"] = {}
    RECORD["on"] = True
    patch.on = patched
    hs = fwd_hs(model, seq)
    patch.on = False
    RECORD["on"] = False
    return hs, dict(RECORD["data"])

_GREEDY_CACHE = {}
def greedy_seq(model, tok, pr):
    key = (id(model), pr)
    if key not in _GREEDY_CACHE:
        ids = tok(pr, return_tensors="pt").input_ids
        ABLATE["on"] = False; patch.on = False
        cur = ids.clone()
        for _ in range(HA):
            nxt = model(cur).logits[0, -1].argmax().view(1, 1)
            cur = torch.cat([cur, nxt], 1)
        _GREEDY_CACHE[key] = (cur, ids.shape[1] - 1)
    return _GREEDY_CACHE[key]

GATES = defaultdict(list)

def regimes_for(p, S, nL, Linj, keep_layers_set):
    """Return named ablation specs. keep_layers_set: layers where attn-to-p is ALLOWED."""
    rows_all = list(range(p + 1, S))
    def sever_p(rows, layers):
        return {"rows": rows, "cols": [p], "layers": layers, "keep_diag": True}
    out = {
        "noablate": [],
        "k0": [sever_p(rows_all, None)],  # sever all post-p → p at every layer
        "keep-Linj": [sever_p(rows_all, set(range(nL)) - {Linj})],
    }
    for L in keep_layers_set:
        out[f"keep-L{L}"] = [sever_p(rows_all, set(range(nL)) - {L})]
    return out

# ---------------- clean allocation scan (no injection) ----------------
def clean_alloc_scan(model, tok, nL, H):
    """Mean FAR→p attention mass per layer and per head (clean greedy cont.)."""
    RECORD["layers"] = set(range(nL))
    layer_mean = np.zeros(nL)
    layer_maxh = np.zeros(nL)
    head_ap = np.zeros((nL, H))
    final_amass = defaultdict(list)
    nP = 0
    for pr in AVG_PROMPTS:
        seq, p = greedy_seq(model, tok, pr)
        S = seq.shape[1]
        far_idx = list(range(S - FAR_W, S))
        car_idx = list(range(p + 1, min(p + 9, S)))
        ABLATE.update(on=False, specs=[])
        patch.on = False
        hs, rec = fwd_rec(model, seq, patched=False)
        for L in range(nL):
            pc = rec[L]["probs"]  # [H, S, S]
            means = [pc[:, i, p].mean().item() for i in far_idx]
            maxhs = [pc[:, i, p].max().item() for i in far_idx]
            layer_mean[L] += float(np.mean(means))
            layer_maxh[L] += float(np.mean(maxhs))
            for h in range(H):
                head_ap[L, h] += float(np.mean([pc[h, i, p].item() for i in far_idx]))
        Lf = nL - 1
        pc = rec[Lf]["probs"]
        amass = {
            "sink0": [0],
            "pre": list(range(1, p)),
            "p": [p],
            "car": car_idx,
            "post": list(range(min(p + 9, S), S)),
        }
        for g, js in amass.items():
            if not js:
                final_amass[g].append(0.0)
            else:
                final_amass[g].append(float(np.mean(
                    [pc[:, i, js].sum(dim=-1).mean().item() for i in far_idx])))
        nP += 1
    layer_mean /= nP
    layer_maxh /= nP
    head_ap /= nP
    famass = {g: float(np.mean(v)) for g, v in final_amass.items()}
    return layer_mean, layer_maxh, head_ap, famass

def detect_islands(layer_mean, layer_maxh, head_ap, nL, ratio_thr=10.0, late_only_from=None):
    """
    Island = layer L where mean a_p is ≥ ratio_thr × max(neighbors L-1, L+1)
    OR max-head a_p is ≥ ratio_thr × neighbor max-heads.
    Prefer late half if late_only_from set (S83 island was near top).
    """
    islands = []
    start = late_only_from if late_only_from is not None else 0
    for L in range(start, nL):
        neigh = []
        if L - 1 >= 0:
            neigh.append(layer_mean[L - 1])
        if L + 1 < nL:
            neigh.append(layer_mean[L + 1])
        base = max(neigh) if neigh else 0.0
        mean_ratio = (layer_mean[L] / base) if base > 1e-12 else (float("inf") if layer_mean[L] > 1e-6 else 0.0)
        neigh_h = []
        if L - 1 >= 0:
            neigh_h.append(layer_maxh[L - 1])
        if L + 1 < nL:
            neigh_h.append(layer_maxh[L + 1])
        base_h = max(neigh_h) if neigh_h else 0.0
        maxh_ratio = (layer_maxh[L] / base_h) if base_h > 1e-12 else (float("inf") if layer_maxh[L] > 1e-6 else 0.0)
        top_h = int(np.argmax(head_ap[L]))
        top_a = float(head_ap[L, top_h])
        flag = (mean_ratio >= ratio_thr and layer_mean[L] >= 1e-4) or \
               (maxh_ratio >= ratio_thr and layer_maxh[L] >= 5e-3)
        islands.append(dict(
            L=L, mean=float(layer_mean[L]), maxh=float(layer_maxh[L]),
            mean_ratio=float(mean_ratio) if math.isfinite(mean_ratio) else 1e9,
            maxh_ratio=float(maxh_ratio) if math.isfinite(maxh_ratio) else 1e9,
            top_h=top_h, top_a=top_a, flag=flag,
        ))
    return islands

# ---------------- keep-only export cells ----------------
def run_export_cells(model, tok, blocks, nL, H, Linj, keep_Ls, directions=("valence", "size")):
    """B + keep-only D/B at selected layers; also k0 and keep-Linj structural zeros."""
    ro = nL
    RECORD["layers"] = set(keep_Ls) | {nL - 1, Linj + 1, max(0, nL - 2)}
    results = []
    for direction in directions:
        print("\n" + "#" * 78)
        print(f"# S85 EXPORT CELLS — {direction} inj={Linj} keep_Ls={sorted(keep_Ls)}")
        print("#" * 78)
        inj_handle = blocks[Linj].register_forward_hook(make_hook())
        ABLATE.update(on=False, specs=[]); patch.on = False
        what, wn = concept_dir(model, tok, direction, Linj)
        what_t = torch.tensor(what, dtype=torch.float32)
        print(f"[setup] ||W||={wn:.2f} target=3||W|| HA={HA} FAR_W={FAR_W}")

        keep_set = set(keep_Ls)
        agg = defaultdict(list)

        for pi, pr in enumerate(AVG_PROMPTS):
            seq, p = greedy_seq(model, tok, pr)
            S = seq.shape[1]
            far_idx = list(range(S - FAR_W, S))
            assert p + 9 <= far_idx[0], "FAR not after k=8 carriers"
            patch.dir = what_t; patch.target = 3.0 * wn; patch.positions = [p]
            regs = regimes_for(p, S, nL, Linj, keep_set)

            for reg, specs in regs.items():
                ABLATE.update(on=bool(specs), specs=specs)
                hs_c, rec_c = fwd_rec(model, seq, patched=False)
                hs_p, rec_p = fwd_rec(model, seq, patched=True)
                ABLATE.update(on=False, specs=[])

                D_far = np.mean([
                    decomp((hs_p[ro][0, i] - hs_c[ro][0, i]).numpy(), what)[1]
                    for i in far_idx
                ])
                agg[(reg, "D")].append(float(D_far))

                if reg == "noablate":
                    dinj = (hs_p[Linj + 1][0, p] - hs_c[Linj + 1][0, p]).numpy()
                    ii, oo = decomp(dinj, what)
                    GATES["g5-inj-outspan-rel"].append(oo / max(ii, 1e-9))
                    for L in keep_set | {nL - 1}:
                        if L not in rec_c:
                            continue
                        pc = rec_c[L]["probs"]
                        ap = float(np.mean([pc[:, i, p].mean().item() for i in far_idx]))
                        agg[(f"ap_c_L{L}",)].append(ap)

        inj_handle.remove()

        M = {k: float(np.mean(v)) for k, v in agg.items()}
        B = M[("noablate", "D")]
        print(f"\n[hs{nL} FAR out-span] B(noablate) = {B:.4f}")
        for reg in sorted(regs.keys()):
            if reg == "noablate":
                continue
            D = M[(reg, "D")]
            r = D / B if B > 1e-9 else float("nan")
            print(f"  {reg:>12} D = {D:.6f}  D/B = {r:.4f}")
            if reg == "k0":
                GATES["g4-k0"].append(D)
            if reg == "keep-Linj":
                GATES["g3-keep-Linj"].append(D)

        cell = dict(direction=direction, Linj=Linj, B=B, M=M, wn=wn)
        results.append(cell)
    return results

# ---------------- main ----------------
def run_model(model_name, expect_nL=None, do_export=True, Linj=INJECT_PRIMARY):
    print("\n" + "=" * 78)
    print(f"LOADING {model_name}")
    print("=" * 78)
    tok, model = load(model_name)
    blocks, fam = get_blocks(model)
    nL = model.config.num_hidden_layers
    H = model.config.num_attention_heads
    hid = model.config.hidden_size
    print(f"[model] {model_name} family={fam} nL={nL} hidden={hid} heads={H} "
          f"dtype={next(model.parameters()).dtype}")
    if expect_nL is not None:
        GATES["g2-nL"].append(1.0 if nL == expect_nL else 0.0)
        if nL != expect_nL:
            print(f"WARNING: expected nL={expect_nL}, got {nL}")

    _HS_CACHE.clear()

    print("\n[1] CLEAN allocation scan a_FAR,p across all layers (no injection)")
    layer_mean, layer_maxh, head_ap, famass = clean_alloc_scan(model, tok, nL, H)
    GATES["g1-sdpa"] = [RECORD["maxerr"]]
    GATES["g6-final-ap"].append(float(layer_mean[nL - 1]))
    GATES["g7-scan"].append(float(H * nL))

    print(f"\n[allocation curve point] final L{nL-1} a_FAR,p mean={layer_mean[nL-1]:.6e} "
          f"max-head={layer_maxh[nL-1]:.6e}")
    print(f"[final-layer clean group mass] " +
          " ".join(f"{g}:{famass[g]:.4f}" for g in ("sink0", "pre", "p", "car", "post")))

    print(f"\n[per-layer a_FAR,p clean (mean heads / max head)]")
    print(f"  {'L':>3} {'mean':>12} {'maxh':>12} {'top_h':>5} {'top_a':>10}")
    for L in range(nL):
        th = int(np.argmax(head_ap[L]))
        print(f"  {L:>3} {layer_mean[L]:12.6e} {layer_maxh[L]:12.6e} {th:>5} {head_ap[L, th]:10.6f}")

    islands_all = detect_islands(layer_mean, layer_maxh, head_ap, nL, ratio_thr=10.0)
    late_from = nL // 2
    islands_late = detect_islands(layer_mean, layer_maxh, head_ap, nL, ratio_thr=10.0,
                                  late_only_from=late_from)
    flagged = [isl for isl in islands_late if isl["flag"]]
    late_sorted = sorted(islands_late, key=lambda d: -d["mean"])
    print(f"\n[island detector late-half L>={late_from}, ratio≥10× neighbors]")
    if flagged:
        for isl in flagged:
            print(f"  ISLAND L{isl['L']}: mean={isl['mean']:.6e} (×{isl['mean_ratio']:.1f} neigh) "
                  f"maxh={isl['maxh']:.6e} (×{isl['maxh_ratio']:.1f}) "
                  f"top h{isl['top_h']} a={isl['top_a']:.6f}")
    else:
        print("  (none flagged at 10×; reporting top-5 late layers by mean a_p)")
    print("  top-5 late by mean a_p:")
    for isl in late_sorted[:5]:
        print(f"    L{isl['L']}: mean={isl['mean']:.6e} maxh={isl['maxh']:.6e} "
              f"ratio_mean={isl['mean_ratio']:.2f} top h{isl['top_h']} a={isl['top_a']:.4f}")

    last5 = list(range(max(0, nL - 5), nL))
    peak_L = int(np.argmax(layer_mean[late_from:])) + late_from
    peak_mean = float(layer_mean[peak_L])
    final_mean = float(layer_mean[nL - 1])
    last2_mean = float(np.mean(layer_mean[nL - 2:nL]))
    peak_vs_last2 = peak_mean / max(last2_mean, 1e-15)
    print(f"\n[late summary] peak late L{peak_L} mean a_p={peak_mean:.6e}; "
          f"final L{nL-1}={final_mean:.6e}; peak/last2 = {peak_vs_last2:.2f}×")
    for Ltag, L in (("peak", peak_L), ("final", nL - 1)):
        order = np.argsort(-head_ap[L])[:5]
        print(f"  top heads at {Ltag} L{L}: " +
              " ".join(f"h{h}:{head_ap[L, h]:.5f}" for h in order))

    export_results = []
    if do_export:
        # keep-only set: final, L_inj+1, peak, any flagged, 2nd-best late
        # (no L21 analogue — pythia-1b is 16L; S83 L21 was on 24L 410m)
        keep_Ls = {nL - 1, Linj + 1, peak_L}
        for isl in flagged:
            keep_Ls.add(isl["L"])
        if len(late_sorted) > 1:
            keep_Ls.add(late_sorted[1]["L"])
        # ensure a pre-inj control layer if available
        if Linj - 1 >= 0:
            keep_Ls.add(Linj - 1)
        keep_Ls = {L for L in keep_Ls if 0 <= L < nL and L != Linj}
        print(f"\n[2] KEEP-ONLY export at layers {sorted(keep_Ls)} (inj={Linj})")
        print(f"    Linj choice: inj={Linj} on {nL}L → post layers "
              f"{list(range(Linj+1, nL))} ({nL - Linj - 1} post layers remain)")
        export_results = run_export_cells(model, tok, blocks, nL, H, Linj, keep_Ls)

    return dict(
        model_name=model_name, family=fam, nL=nL, H=H, hid=hid,
        layer_mean=layer_mean, layer_maxh=layer_maxh, head_ap=head_ap, famass=famass,
        peak_L=peak_L, peak_mean=peak_mean, final_mean=final_mean,
        peak_vs_last2=peak_vs_last2, flagged=flagged, late_sorted=late_sorted,
        export_results=export_results, Linj=Linj,
    )


def main():
    print(f"S85 VALIDATE — pythia-1b within-family scale curve + late allocation scan  SEED={SEED}")
    print(f"primary model: {PRIMARY}  (expect nL=16; Linj={INJECT_PRIMARY})")
    print(f"torch {torch.__version__}  cuda={torch.cuda.is_available()}")
    print(f"[Linj rationale] 16L model → inj=12 leaves layers 13,14,15 post-injection "
          f"(3 post layers; analogue of S82/S83 inj18 on 24L leaving 5 post, scaled down).")

    # ---- primary: pythia-1b ----
    try:
        primary = run_model(PRIMARY, expect_nL=16, do_export=True, Linj=INJECT_PRIMARY)
    except Exception as e:
        print(f"\nFATAL primary load/run failed: {type(e).__name__}: {e}")
        import traceback; traceback.print_exc()
        print(f"\n[wall-clock partial] {time.time()-T0:.1f} s")
        sys.exit(2)

    # free memory before optional 410m re-anchor (primary model already out of scope)
    gc.collect()

    # ---- optional light re-anchor pythia-410m final a_p (clean scan only) ----
    anchor = None
    try:
        avail_kb = None
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemAvailable:"):
                        avail_kb = int(line.split()[1])
                        break
        except Exception:
            pass
        if avail_kb is not None and avail_kb < 3 * 1024 * 1024:
            print(f"\n[anchor] skip pythia-410m re-anchor: MemAvailable={avail_kb/1024/1024:.1f} GiB < 3 GiB")
        else:
            print("\n" + "=" * 78)
            print("OPTIONAL LIGHT RE-ANCHOR: pythia-410m clean final-layer a_p under SEED=85")
            print("=" * 78)
            gc.collect()
            anchor = run_model(ANCHOR_410M, expect_nL=24, do_export=False, Linj=18)
    except Exception as e:
        print(f"anchor remeasure skipped/failed: {type(e).__name__}: {e}")
        import traceback; traceback.print_exc()

    # Re-bind primary if we somehow lost it (we shouldn't have)
    # primary is from first run_model call above.

    # ---------------- gates ----------------
    print("\n" + "=" * 78)
    print("APPARATUS / EXACTNESS GATES")
    print("=" * 78)
    g1 = max(GATES.get("g1-sdpa", [RECORD["maxerr"]]) + [RECORD["maxerr"]])
    g2 = min(GATES["g2-nL"]) if GATES["g2-nL"] else 0.0
    # g2 only cares about primary nL==16; if anchor also wrote g2, min may fail.
    # Filter: primary was first; if anchor ran with expect 24 and passed, min is still 1.
    # If only primary, fine. If primary wrong, fail. OK.
    g3 = max(GATES["g3-keep-Linj"]) if GATES["g3-keep-Linj"] else float("nan")
    g4 = max(GATES["g4-k0"]) if GATES["g4-k0"] else float("nan")
    g5 = max(GATES["g5-inj-outspan-rel"]) if GATES["g5-inj-outspan-rel"] else float("nan")
    g6 = GATES["g6-final-ap"][0] if GATES["g6-final-ap"] else float("nan")  # primary first
    g7 = GATES["g7-scan"][0] if GATES["g7-scan"] else 0.0  # primary first
    def pf(ok): return "PASS" if ok else "FAIL"
    # g2 for primary specifically: primary expect 16 — if anchor also recorded 1.0, min=1
    # But if we only want primary: check primary.nL
    g2_primary = 1.0 if primary["nL"] == 16 else 0.0
    print(f"g1 sdpa recon max abs err:           {g1:.2e}  ({pf(g1 < 5e-3)})")
    print(f"g2 pythia-1b nL==16:                 {g2_primary:.0f}      ({pf(g2_primary == 1.0)})")
    print(f"g3 keep-Linj D ~ 0 (max):            {g3:.2e}  ({pf(isinstance(g3,float) and g3 < 1e-4)})")
    print(f"g4 k0 D ~ 0 (max):                   {g4:.2e}  ({pf(isinstance(g4,float) and g4 < 1e-4)})")
    print(f"g5 injection out/in span rel (max):  {g5:.2e}  ({pf(isinstance(g5,float) and g5 < 1e-2)})")
    print(f"g6 final a_p in [0,1] finite:        {g6:.6e}  ({pf(math.isfinite(g6) and 0.0 <= g6 <= 1.0)})")
    print(f"g7 island scan cells (H*nL):         {g7:.0f}     ({pf(g7 >= 16)})")

    # ---------------- synthesis ----------------
    print("\n" + "=" * 78)
    print("SYNTHESIS — within-family pythia scale curve + island check")
    print("=" * 78)
    print("\n[allocation-suppression curve — final-layer a_FAR,p clean mean]")
    print(f"  {'model':<16} {'nL':>3} {'L_final':>7} {'a_FAR,p':>12} {'source':<28}")
    for name, _, nL_, Lf, ap, src in PRIOR_CURVE:
        print(f"  {name:<16} {nL_:>3} {Lf:>7} {ap:12.6e} {src:<28}")
    p = primary
    print(f"  {'pythia-1b':<16} {p['nL']:>3} {p['nL']-1:>7} {p['final_mean']:12.6e} {'S85 THIS RUN':<28}")
    if anchor is not None:
        print(f"  {'pythia-410m@s85':<16} {anchor['nL']:>3} {anchor['nL']-1:>7} "
              f"{anchor['final_mean']:12.6e} {'S85 light re-anchor':<28}")

    # curve reading vs 410m
    prior_410 = 3.16e-4
    ratio_vs_410 = p["final_mean"] / max(prior_410, 1e-15)
    if p["final_mean"] < prior_410 * 0.5:
        curve_read = "DEEPEN (more suppressed than 410m)"
    elif p["final_mean"] < prior_410 * 2.0:
        curve_read = "PLATEAU (within ~2× of 410m)"
    elif p["final_mean"] < 5e-3:
        curve_read = "RELAX (partial lift toward gpt2 but still suppressed)"
    else:
        curve_read = "RELAX-STRONG (approaching gpt2-like allocation)"
    print(f"\n[curve reading vs pythia-410m {prior_410:.2e}] "
          f"pythia-1b / 410m = {ratio_vs_410:.2f}× → {curve_read}")

    print(f"\n[island check — pythia-1b 16L within-family]")
    print(f"  late peak: L{p['peak_L']} a_mean={p['peak_mean']:.6e}  "
          f"peak/last2={p['peak_vs_last2']:.2f}×  (S83 L21 was ~40–60× L22/23)")
    if p["flagged"]:
        print(f"  VERDICT island: YES — {len(p['flagged'])} late layer(s) flagged at ≥10× neighbors")
        for isl in p["flagged"]:
            print(f"    L{isl['L']} top h{isl['top_h']} a={isl['top_a']:.4f} "
                  f"mean_ratio={isl['mean_ratio']:.1f}")
    else:
        if p["peak_vs_last2"] >= 10:
            print(f"  VERDICT island: YES (soft) — peak/last2={p['peak_vs_last2']:.1f}× ≥10 "
                  f"at L{p['peak_L']}")
        elif p["peak_vs_last2"] >= 5:
            print(f"  VERDICT island: WEAK — peak/last2={p['peak_vs_last2']:.1f}× (5–10) "
                  f"at L{p['peak_L']}")
        else:
            print(f"  VERDICT island: NO — no ≥10× neighbor spike; peak/last2={p['peak_vs_last2']:.2f}×")

    if p["export_results"]:
        print(f"\n[keep-only export D/B @ inj{p['Linj']}]")
        for r in p["export_results"]:
            B = r["B"]
            print(f"  [{r['direction']}] B={B:.4f}")
            for k, v in sorted(r["M"].items()):
                if isinstance(k, tuple) and k[0] != "noablate" and k[-1] == "D":
                    reg = k[0]
                    print(f"    {reg:>12}: D={v:.4f}  D/B={v/B:.3f}")

    print(f"\n[model choice] primary={PRIMARY}; optional 410m re-anchor "
          f"{'DONE' if anchor is not None else 'SKIPPED'}.")
    print(f"[wall-clock] {time.time()-T0:.1f} s")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"\nUNCAUGHT: {type(e).__name__}: {e}")
        import traceback; traceback.print_exc()
        print(f"[wall-clock on failure] {time.time()-T0:.1f} s")
        raise
