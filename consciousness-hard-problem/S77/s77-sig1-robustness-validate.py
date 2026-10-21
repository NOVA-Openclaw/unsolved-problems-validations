#!/usr/bin/env python3
# s77-sig1-robustness-validate.py
# VALIDATE extension of S75 (SIG1 on gpt2-124M). Stress-tests the S76 distinct-natural-kinds
# claim along the exact axes S76 §5.2 flagged, and directly probes collapse-condition #1
# (§4.4): "a within-pass internal back-arrow is found in standard decoder-only transformers."
#
# Three robustness axes:
#   (1) MULTIPLE LAYERS  — patch at several mid-layers, not just block 6, and measure the
#       within-pass BACKWARD deflection (positions < p) at the final block. S76 collapse-cond#1
#       predicts EXACTLY 0 at every patch layer (architecture guarantee for causal attention).
#   (2) MULTIPLE DIRECTIONS/CONCEPTS — beyond valence: {valence, formality, size, tense}
#       difference-of-means directions. P1 backward=0 must hold direction-independently;
#       P2 across-gen must stay nonzero-decaying, not a valence artifact.
#   (3) SECOND MODEL — repeat on EleutherAI/pythia-160m (GPTNeoX, 12L/768d) to confirm the
#       P1/P2 pattern is not gpt2-specific.
#
# Plus a CLEANER P2 ESTIMATOR (addresses S75 caveat #1, ragged non-monotone decay):
#   deflection-per-unit-attention-mass — divide each later position's out-span deflection by
#   the total attention mass that position (across heads, final layers) pays to the patched
#   position p. If the raggedness in S75 was attention re-weighting, the normalized envelope
#   should be smoother / more monotone than the raw one.
#
# Expected (hardens the distinction): P1 backward == 0 for ALL layers/directions/models;
#   P2 raw nonzero-decaying; P2 attention-normalized envelope smoother (higher monotone frac).
# Falsifier (breaks the distinction): any nonzero backward (<p) deflection above fp noise.
#
# Run: .venv-s75/bin/python s77-sig1-robustness-validate.py
import numpy as np, torch, random
from transformers import AutoModelForCausalLM, AutoTokenizer

SEED = 77
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
torch.set_grad_enabled(False)

# concept probe sets: difference-of-means (pos_ctx) - (neg_ctx), measured at output of patch layer.
CONCEPTS = {
    "valence": (
        ["This movie was absolutely wonderful and", "I loved every second, it felt great and",
         "What a fantastic, delightful experience that was and", "The food was delicious and",
         "She smiled, overjoyed and thrilled, and", "It was a beautiful, happy, perfect day and"],
        ["This movie was absolutely terrible and", "I hated every second, it felt awful and",
         "What a dreadful, miserable experience that was and", "The food was disgusting and",
         "He frowned, depressed and furious, and", "It was an ugly, sad, ruined day and"],
    ),
    "formality": (
        ["I am writing to formally request your consideration and", "Pursuant to our agreement, we hereby and",
         "It would be greatly appreciated if you would kindly and", "We respectfully submit the following and",
         "In accordance with the established protocol, and", "The committee wishes to convey that and"],
        ["hey so basically i wanna ask you and", "yeah nah we totally did that thing and",
         "cmon just gimme a sec and", "lol that was super weird and",
         "dude honestly whatever just and", "gonna grab some food wanna and"],
    ),
    "size": (
        ["The enormous, gigantic, colossal tower and", "A vast and immense expanse stretched and",
         "The huge, massive whale surfaced and", "An overwhelming, towering mountain and",
         "The sprawling, giant metropolis and", "A monstrous, titanic wave rose and"],
        ["The tiny, minuscule, microscopic speck and", "A small and diminutive dot appeared and",
         "The little, petite mouse scurried and", "A negligible, minute fleck and",
         "The compact, miniature cottage and", "A tiny, wee crumb fell and"],
    ),
    "tense": (
        ["Yesterday she walked to the store and", "They had already finished the meal and",
         "He was reading a long book and", "We visited the museum last week and",
         "The train departed on time and", "I cooked dinner earlier and"],
        ["Tomorrow she will walk to the store and", "They are going to finish the meal and",
         "He will be reading a long book and", "We will visit the museum next week and",
         "The train will depart on time and", "I am going to cook dinner and"],
    ),
}

AVG_PROMPTS = [
    "The film I watched last night was",
    "My review of the restaurant is that it was",
    "Honestly, the whole trip turned out to be",
    "When she opened the letter, her reaction was",
    "Looking back on the concert, I thought it was",
]

def block_list(model, family):
    return model.transformer.h if family == "gpt2" else model.gpt_neox.layers

def load(model_name, family):
    tok = AutoTokenizer.from_pretrained(model_name)
    # SDPA is numerically stable for both families. (GPTNeoX/pythia eager attention emits
    # NaNs on some inputs — a known upstream bug — so we do NOT use eager for the main model.)
    model = AutoModelForCausalLM.from_pretrained(model_name, attn_implementation="sdpa"); model.eval()
    return tok, model

def load_eager(model_name):
    """Separate eager instance ONLY for reading attention weights (gpt2 is stable in eager)."""
    return AutoModelForCausalLM.from_pretrained(model_name, attn_implementation="eager").eval()

def resid_after_block(model, tok, family, text, L):
    """residual AFTER block L at last token: hidden_states[L+1]."""
    ids = tok(text, return_tensors="pt").input_ids
    hs = model(ids, output_hidden_states=True).hidden_states
    return hs[L+1][0, -1].numpy()

def concept_dir(model, tok, family, name, L):
    pos, neg = CONCEPTS[name]
    mp = np.mean([resid_after_block(model, tok, family, t, L) for t in pos], axis=0)
    mn = np.mean([resid_after_block(model, tok, family, t, L) for t in neg], axis=0)
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

def run(model_name, family):
    print("\n" + "#"*74)
    print(f"# MODEL: {model_name}  (family={family})")
    print("#"*74)
    tok, model = load(model_name, family)
    nL = model.config.n_layer if family=="gpt2" else model.config.num_hidden_layers
    dmod = model.config.n_embd if family=="gpt2" else model.config.hidden_size
    READOUT = nL - 1
    ro = READOUT + 1
    print(f"[setup] n_layer={nL} d_model={dmod} readout=block{READOUT}")

    blocks = block_list(model, family)

    # ---------- AXIS 1+2: P1 backward across LAYERS x CONCEPTS (single forward pass) ----------
    print("\n" + "="*72)
    print("P1 — WITHIN-PASS BACKWARD DEFLECTION (positions < p) across layers x concepts")
    print("     collapse-condition #1: any value >> fp-noise breaks the kind distinction")
    print("="*72)
    PROMPT = "The film I watched last night was"
    ids = tok(PROMPT, return_tensors="pt").input_ids
    N = ids.shape[1]; p = N - 1
    patch_layers = sorted(set([max(1,nL//4), nL//2, (3*nL)//4]))
    print(f"[cfg] prompt={PROMPT!r} n_tok={N} patch_pos p={p} patch_layers(block idx)={patch_layers}")
    max_back = 0.0
    p1_rows = []
    for L in patch_layers:
        handle = blocks[L].register_forward_hook(make_hook())
        for cname in CONCEPTS:
            what, wn = concept_dir(model, tok, family, cname, L)
            what_t = torch.tensor(what, dtype=torch.float32)
            target = 3.0 * wn
            # clean
            patch.on=False
            hs_clean = model(ids, output_hidden_states=True).hidden_states
            # patched
            patch.dir=what_t; patch.target=target; patch.positions=[p]; patch.on=True
            hs_patch = model(ids, output_hidden_states=True).hidden_states
            patch.on=False
            delta_full = hs_patch[ro][0] - hs_clean[ro][0]
            back = delta_full[:p].norm().item() if p>0 else float('nan')
            at_p = delta_full[p].norm().item()
            _, outp = decomp((hs_patch[ro][0,p]-hs_clean[ro][0,p]).numpy(), what)
            max_back = max(max_back, back)
            p1_rows.append((L, cname, back, at_p, outp))
        handle.remove()
    print(f"  {'layer':>5} {'concept':>9} {'backward(<p)':>14} {'at-p':>10} {'out-span@p':>11}")
    for L,c,b,ap,op in p1_rows:
        flag = "  <-- NONZERO!" if b > 1e-6 else ""
        print(f"  {L:5d} {c:>9} {b:14.3e} {ap:10.3f} {op:11.3f}{flag}")
    print(f"[P1] max backward deflection over ALL layers x concepts = {max_back:.3e}")
    print(f"[P1] verdict: {'CONFIRMED exact-0 (distinction holds)' if max_back<=1e-6 else 'FALSIFIER — within-pass back-arrow found'}")

    # ---------- controls (valence @ mid layer) ----------
    Lmid = nL//2
    handle = blocks[Lmid].register_forward_hook(make_hook())
    what, wn = concept_dir(model, tok, family, "valence", Lmid); what_t=torch.tensor(what,dtype=torch.float32)
    target = 3.0*wn
    patch.on=False; hs_clean = model(ids, output_hidden_states=True).hidden_states
    clean_coord = float(np.dot(hs_clean[Lmid+1][0,p].numpy(), what))
    # zero-magnitude
    patch.dir=what_t; patch.target=clean_coord; patch.positions=[p]; patch.on=True
    hz = model(ids, output_hidden_states=True).hidden_states; patch.on=False
    zero_defl = (hz[ro][0,p]-hs_clean[ro][0,p]).norm().item()
    # next-token flip
    patch.on=False; lc = model(ids).logits[0,-1]
    patch.dir=what_t; patch.target=target; patch.positions=[p]; patch.on=True
    lp = model(ids).logits[0,-1]; patch.on=False
    flipped = int(lc.argmax())!=int(lp.argmax())
    print(f"[ctrl] zero-magnitude patch deflection@p={zero_defl:.3e} (expect ~0); "
          f"next-token flipped={flipped} {tok.decode(int(lc.argmax()))!r}->{tok.decode(int(lp.argmax()))!r}")
    handle.remove()

    # ---------- AXIS: P2 across-gen, RAW vs ATTENTION-NORMALIZED (valence, mid layer) ----------
    print("\n" + "="*72)
    print("P2 — ACROSS-GEN out-span decay: RAW vs ATTENTION-NORMALIZED estimator")
    print("     (cleaner estimator = deflection / attention-mass-to-p; S75 caveat #1)")
    print("="*72)
    handle = blocks[Lmid].register_forward_hook(make_hook())
    HA = 12
    do_attn_norm = (family == "gpt2")   # only gpt2 eager attention is NaN-safe here
    eager = load_eager(model_name) if do_attn_norm else None
    raw_all, norm_all = [], []
    for pr in AVG_PROMPTS:
        _ids = tok(pr, return_tensors="pt").input_ids
        _N=_ids.shape[1]; _p=_N-1
        # clean greedy continuation
        patch.on=False; cur=_ids.clone()
        for _ in range(HA):
            nxt = model(cur).logits[0,-1].argmax().view(1,1); cur=torch.cat([cur,nxt],1)
        _seq=cur
        # attention mass to _p at readout-ish layers (avg over final 3 layers, all heads), clean run
        if do_attn_norm:
            att = eager(_seq, output_attentions=True).attentions  # tuple[nL] each [1,heads,q,k]
            late = att[-3:] if len(att)>=3 else att
            mass_to_p = np.mean([a[0,:,:, _p].mean(0).numpy() for a in late], axis=0)  # [seq]
        else:
            mass_to_p = None
        # deflection profile (single injection at _p)
        patch.on=False; hc = model(_seq, output_hidden_states=True).hidden_states
        _what,_wn = concept_dir(model, tok, family, "valence", Lmid)
        patch.dir=torch.tensor(_what,dtype=torch.float32); patch.target=3.0*_wn
        patch.positions=[_p]; patch.on=True
        hp = model(_seq, output_hidden_states=True).hidden_states; patch.on=False
        raw=[]; norm=[]
        for pos in range(_p+1, _N+HA):
            dv=(hp[ro][0,pos]-hc[ro][0,pos]).numpy()
            _,outs = decomp(dv, _what)
            raw.append(outs)
            if mass_to_p is not None and pos < mass_to_p.shape[0]:
                mv = float(mass_to_p[pos])
                norm.append(outs/mv if mv > 1e-6 else np.nan)
            else:
                norm.append(np.nan)
        raw_all.append(np.array(raw)); norm_all.append(np.array(norm))
    handle.remove()
    RAW=np.array(raw_all); NORM=np.array(norm_all)
    raw_mean=RAW.mean(0)
    # normalize each prompt's raw to its step1, then average -> shape
    raw_shape=(RAW/np.clip(RAW[:, :1],1e-9,None)).mean(0)
    norm_shape_prompt=(NORM/np.clip(NORM[:, :1],1e-9,None))
    norm_shape=np.nanmean(norm_shape_prompt,0)
    def mono(p_):
        p_=p_[~np.isnan(p_)]
        return float(np.mean(np.diff(p_)<0)) if len(p_)>1 else float('nan')
    steps=list(range(1,len(raw_mean)+1))
    print(f"  step:            " + " ".join(f"{s:6d}" for s in steps))
    print(f"  raw out-span:    " + " ".join(f"{v:6.3f}" for v in raw_mean))
    print(f"  raw shape(s1=1): " + " ".join(f"{v:6.3f}" for v in raw_shape))
    print(f"  attn-norm shape: " + " ".join(f"{v:6.3f}" for v in norm_shape))
    print(f"[P2] raw: nonzero-mean={raw_mean.mean():.3f}  frac-decreasing(raw shape)={mono(raw_shape):.2f}")
    print(f"[P2] attn-normalized: frac-decreasing={mono(norm_shape):.2f}  "
          f"(smoother if > raw frac-decreasing)")
    return dict(model=model_name, max_back=max_back, zero_defl=zero_defl, flipped=flipped,
                raw_mean=float(raw_mean.mean()), raw_mono=mono(raw_shape), norm_mono=mono(norm_shape))

results = []
results.append(run("gpt2", "gpt2"))
results.append(run("EleutherAI/pythia-160m", "pythia"))

print("\n" + "="*74)
print("CROSS-MODEL SUMMARY")
print("="*74)
for r in results:
    print(f"  {r['model']:>22}: P1 max-backward={r['max_back']:.3e}  zero-ctrl={r['zero_defl']:.3e}  "
          f"flip={r['flipped']}  P2 raw-mean={r['raw_mean']:.3f}  "
          f"mono raw={r['raw_mono']:.2f}->attn-norm={r['norm_mono']:.2f}")
allzero = all(r['max_back']<=1e-6 for r in results)
print(f"\n[VERDICT] P1 exact-0 across BOTH models, ALL layers, ALL concepts: {allzero}")
print(f"[VERDICT] {'Distinction HARDENS: no within-pass back-arrow anywhere (collapse-cond#1 not met).' if allzero else 'FALSIFIER: within-pass back-arrow found — kind distinction breaks.'}")
