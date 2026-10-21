#!/usr/bin/env python3
# s75-sig1-openweights-validate.py
# FIRST direct in-silico test of the S74 SIG1 prediction on a REAL open-weights
# transformer (gpt2, 124M), CPU only. Not a toy.
#
# S74 claim: in a standard LLM the ONLY genuine workspace->specialist back-arrow is
# EXTERNALIZED through autoregression (emitted/patched token re-enters via the KV cache),
# not internal within-pass recurrence.
#
# Prediction 1 (SINGLE FORWARD PASS): patch a "workspace" direction W at mid layer L,
#   position p (do(W:=W*)). Within one pass this is a depth-ordered causal DAG:
#   - it CANNOT deflect specialist state at positions < p  (expect EXACTLY 0: no back-arrow)
#   - at positions >= p it propagates purely feedforward (one shot, no temporal decay).
#
# Prediction 2 (ACROSS GENERATION): the same single patch, carried forward in the KV cache,
#   deflects out-of-direction ("specialist") state at LATER positions (p+1, p+2, ...),
#   and that deflection should be NONZERO and DECAYING over steps (externalized recurrence).
#
# Controls: (a) zero-magnitude patch -> zero deflection; (b) random unit direction, equal
#   patch norm; (c) verify the patch actually shifts next-token behavior (else the
#   across-generation channel is silent and the test is void).
#
# Run: python3 s75-sig1-openweights-validate.py
import numpy as np, torch, random
from transformers import AutoModelForCausalLM, AutoTokenizer

SEED = 75
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
torch.set_grad_enabled(False)

MODEL = "gpt2"           # 124M, 12 blocks, d_model 768
L = 6                    # mid layer: patch is applied at the OUTPUT of block L (0-indexed)
READOUT = 11             # measure specialist deflection at output of block 11 (final block)
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL); model.eval()
d_model = model.config.n_embd
print(f"[setup] model={MODEL} n_layer={model.config.n_layer} d_model={d_model} "
      f"patch_layer(block out)={L} readout_layer(block out)={READOUT} seed={SEED}")

def resid_last(text):
    """residual stream (output of block L) at the LAST token position, as np vector."""
    ids = tok(text, return_tensors="pt").input_ids
    hs = model(ids, output_hidden_states=True).hidden_states  # tuple len n_layer+1; hs[i]=input to block i, hs[n_layer]=final
    # hidden_states[k] = residual AFTER k blocks (hs[0]=embeddings). So output of block L == hs[L+1].
    return hs[L+1][0, -1].numpy()

# ---------------------------------------------------------------------------
# (1) Build W: difference-of-means concept (valence) direction at output of block L.
#     Verbalizable concept direction, per the alpha-sweep method (Gurnee et al.
#     arXiv:2607.15495, preprint, as described in s73 notes).
# ---------------------------------------------------------------------------
pos_ctx = [
    "This movie was absolutely wonderful and", "I loved every second, it felt great and",
    "What a fantastic, delightful experience that was and", "The food was delicious and the service was excellent and",
    "She smiled, overjoyed and thrilled, and", "It was a beautiful, happy, perfect day and",
]
neg_ctx = [
    "This movie was absolutely terrible and", "I hated every second, it felt awful and",
    "What a dreadful, miserable experience that was and", "The food was disgusting and the service was horrible and",
    "He frowned, depressed and furious, and", "It was an ugly, sad, ruined day and",
]
mp = np.mean([resid_last(t) for t in pos_ctx], axis=0)
mn = np.mean([resid_last(t) for t in neg_ctx], axis=0)
Wvec = mp - mn
Wn = np.linalg.norm(Wvec)
What = Wvec / Wn
What_t = torch.tensor(What, dtype=torch.float32)
print(f"[W] difference-of-means valence direction: ||W||={Wn:.3f}")

# random control direction (unit), fixed seed
g = np.random.default_rng(SEED); r = g.standard_normal(d_model); r /= np.linalg.norm(r)
Rhat_t = torch.tensor(r, dtype=torch.float32)

# ---------------------------------------------------------------------------
# Patch hook: at OUTPUT of block L, at chosen positions, do(component along dir := target).
#   resid' = resid - (resid . dhat) dhat + target * dhat
# ---------------------------------------------------------------------------
class Patch:
    def __init__(self): self.dir=None; self.target=0.0; self.positions=None; self.on=False
patch = Patch()

def hook(module, inp, out):
    if not patch.on: return out
    h = out[0] if isinstance(out, tuple) else out   # [batch, seq, d]
    dhat = patch.dir.to(h.dtype)
    pos = patch.positions if patch.positions is not None else range(h.shape[1])
    for p in pos:
        cur = torch.dot(h[0, p], dhat)
        h[0, p] = h[0, p] - cur*dhat + patch.target*dhat
    if isinstance(out, tuple): return (h,)+tuple(out[1:])
    return h

handle = model.transformer.h[L].register_forward_hook(hook)

def run_hidden(ids):
    return model(ids, output_hidden_states=True).hidden_states  # tuple

def run_logits(ids):
    return model(ids).logits

# choose target magnitude: strong push along W. Natural in-span coords are ~ +-Wn/2 around mean;
# set to +3*||W|| positive-valence to strongly drive the direction.
TARGET = 3.0 * Wn
print(f"[patch] target coordinate along dir = {TARGET:.3f} (= 3*||W||)")

# ===========================================================================
# PROMPT for the experiment
# ===========================================================================
PROMPT = "The film I watched last night was"
ids = tok(PROMPT, return_tensors="pt").input_ids
N = ids.shape[1]
patch_pos = N - 1   # patch the LAST prompt token (the "workspace" edit position p)
print(f"[prompt] {PROMPT!r}  n_tok={N}  patch_pos p={patch_pos}")

def decomp(delta_vec):
    """L2 of in-span(W) and out-span(specialist) components of a deflection vector (torch)."""
    dv = delta_vec.numpy()
    inspan = np.dot(dv, What)
    inspan_vec = inspan * What
    outspan_vec = dv - inspan_vec
    return float(np.linalg.norm(inspan_vec)), float(np.linalg.norm(outspan_vec))

# ---- clean pass ----
patch.on = False
hs_clean = run_hidden(ids)
logits_clean = run_logits(ids)[0, -1]

# ---- patched pass (do(W:=W*) at block L, position p) ----
patch.dir = What_t; patch.target = TARGET; patch.positions = [patch_pos]; patch.on = True
hs_patch = run_hidden(ids)
logits_patch = run_logits(ids)[0, -1]
patch.on = False

# =============== SIG1 / Prediction 1: SINGLE FORWARD PASS ===================
print("\n" + "="*72)
print("PREDICTION 1 — SINGLE FORWARD PASS (depth-ordered causal DAG)")
print("="*72)

# (A) backward witness: deflection at positions < p, at the readout layer -> must be EXACTLY 0
ro = READOUT + 1  # hidden_states index for output of block READOUT
delta_full = (hs_patch[ro][0] - hs_clean[ro][0])  # [seq, d]
back_defl = delta_full[:patch_pos].norm().item() if patch_pos > 0 else float('nan')
fwd_defl_atp = delta_full[patch_pos].norm().item()
print(f"(A) backward deflection at positions < p (readout layer {READOUT}): {back_defl:.3e}   [expect 0]")
print(f"    deflection AT position p (readout layer {READOUT}):            {fwd_defl_atp:.3e}   [expect >0]")

# (B) within-pass in-span vs out-span at position p across downstream layers
print(f"(B) within-pass deflection at position p, decomposed (in-span W vs out-span specialist):")
for LL in range(L+1, model.config.n_layer+1):
    dv = hs_patch[LL][0, patch_pos] - hs_clean[LL][0, patch_pos]
    ins, outs = decomp(dv)
    print(f"    block {LL-1:2d} out: in-span={ins:8.3f}  out-span(specialist)={outs:8.3f}")

# =============== Controls ===================================================
print("\n" + "="*72)
print("CONTROLS")
print("="*72)
# (a) zero-magnitude patch: set component along W to its clean value (no-op edit) -> ~0 deflection
clean_coord = float(np.dot(hs_clean[L+1][0, patch_pos].numpy(), What))
patch.dir=What_t; patch.target=clean_coord; patch.positions=[patch_pos]; patch.on=True
hs_zero = run_hidden(ids); patch.on=False
zero_defl = (hs_zero[ro][0, patch_pos] - hs_clean[ro][0, patch_pos]).norm().item()
print(f"(a) zero-magnitude patch (set W-coord to its clean value): deflection at p = {zero_defl:.3e}  [expect ~0]")

# (b) random unit direction, equal patch NORM (match the magnitude of change we injected)
inject_norm = abs(TARGET - clean_coord)   # how much we moved along the patch dir
patch.dir=Rhat_t
rand_clean_coord = float(np.dot(hs_clean[L+1][0, patch_pos].numpy(), r))
patch.target = rand_clean_coord + inject_norm
patch.positions=[patch_pos]; patch.on=True
hs_rand = run_hidden(ids); patch.on=False
rand_defl_p = (hs_rand[ro][0, patch_pos] - hs_clean[ro][0, patch_pos]).norm().item()
print(f"(b) random-direction patch (equal inject norm {inject_norm:.2f}): deflection at p = {rand_defl_p:.3e}")

# (c) verify the patch shifts next-token behavior (else across-gen channel is silent)
kl = torch.nn.functional.kl_div(torch.log_softmax(logits_patch,0), torch.softmax(logits_clean,0),
                                reduction='sum').item()
top_clean = tok.decode(int(logits_clean.argmax()))
top_patch = tok.decode(int(logits_patch.argmax()))
print(f"(c) next-token shift: KL(clean||patch)-proxy sum={kl:.3f}  top_clean={top_clean!r}  top_patch={top_patch!r}  "
      f"flipped={top_clean!=top_patch}")

# =============== SIG1 / Prediction 2: ACROSS GENERATION =====================
# Single injection at prompt pass (position p). Teacher-force the SAME clean-greedy
# continuation for both runs so the decay reflects propagation of the workspace edit
# through the KV cache (externalized recurrence), not divergent token identities.
print("\n" + "="*72)
print("PREDICTION 2 — ACROSS GENERATION (externalized recurrence via KV cache)")
print("="*72)
H = 12
# clean greedy generation to get a fixed continuation
cur = ids.clone()
for _ in range(H):
    nxt = run_logits(cur)[0, -1].argmax().view(1,1)
    cur = torch.cat([cur, nxt], dim=1)
seq = cur  # length N+H
gen_txt = tok.decode(seq[0, N:])
print(f"[gen] clean greedy continuation: {gen_txt!r}")

def decay_profile(dir_t, target_scalar):
    """Run clean & patched (single injection at p) over the SAME fixed seq; return
    out-span specialist deflection at readout layer for positions p+1..N+H-1."""
    patch.on=False
    hc = run_hidden(seq)
    patch.dir=dir_t; patch.target=target_scalar; patch.positions=[patch_pos]; patch.on=True
    hp = run_hidden(seq); patch.on=False
    ro = READOUT + 1
    prof = []
    for pos in range(patch_pos+1, N+H):
        dv = hp[ro][0, pos] - hc[ro][0, pos]
        _, outs = decomp(dv)
        prof.append(outs)
    return np.array(prof)

prof_W = decay_profile(What_t, TARGET)
# random-direction decay control (equal inject norm)
prof_R = decay_profile(Rhat_t, rand_clean_coord + inject_norm)

steps = list(range(1, len(prof_W)+1))
print(f"[decay] out-span (specialist) deflection at readout layer {READOUT}, per generation step:")
print(f"  step:      " + " ".join(f"{s:6d}" for s in steps))
print(f"  W-patch:   " + " ".join(f"{v:6.3f}" for v in prof_W))
print(f"  rand-ctrl: " + " ".join(f"{v:6.3f}" for v in prof_R))

def monotone_decay_frac(p):
    if len(p) < 2: return float('nan')
    return float(np.mean(np.diff(p) < 0))
print(f"[decay] W-patch: first={prof_W[0]:.3f} last={prof_W[-1]:.3f} "
      f"ratio(last/first)={prof_W[-1]/max(prof_W[0],1e-9):.3f} "
      f"frac-steps-decreasing={monotone_decay_frac(prof_W):.2f}")
print(f"[decay] mean out-span deflection over gen (W)={prof_W.mean():.3f}  (rand)={prof_R.mean():.3f}")

# ---- averaged decay over multiple prompts (reduce single-prompt attention noise) ----
print("\n[decay-avg] averaging across-gen out-span decay over multiple prompts:")
AVG_PROMPTS = [
    "The film I watched last night was",
    "My review of the restaurant is that it was",
    "Honestly, the whole trip turned out to be",
    "When she opened the letter, her reaction was",
    "Looking back on the concert, I thought it was",
]
HA = 12
all_prof = []
for pr in AVG_PROMPTS:
    _ids = tok(pr, return_tensors="pt").input_ids
    _N = _ids.shape[1]; _p = _N - 1
    # clean greedy continuation
    _cur = _ids.clone()
    patch.on = False
    for _ in range(HA):
        _nxt = run_logits(_cur)[0, -1].argmax().view(1,1)
        _cur = torch.cat([_cur, _nxt], dim=1)
    _seq = _cur
    # measure deflection with single injection at _p
    patch.on=False; _hc = run_hidden(_seq)
    patch.dir=What_t; patch.target=TARGET; patch.positions=[_p]; patch.on=True
    _hp = run_hidden(_seq); patch.on=False
    _ro = READOUT + 1
    prof = []
    for pos in range(_p+1, _N+HA):
        dv = _hp[_ro][0, pos] - _hc[_ro][0, pos]
        _, outs = decomp(dv); prof.append(outs)
    all_prof.append(np.array(prof))
AP = np.array(all_prof)                 # [prompts, steps]
mean_prof = AP.mean(axis=0)
# normalize each prompt to its own step-1 value, then average -> shape-of-decay
norm_prof = (AP / np.clip(AP[:, :1], 1e-9, None)).mean(axis=0)
stepsA = list(range(1, len(mean_prof)+1))
print(f"  step:        " + " ".join(f"{s:6d}" for s in stepsA))
print(f"  mean out-sp: " + " ".join(f"{v:6.3f}" for v in mean_prof))
print(f"  norm(step1): " + " ".join(f"{v:6.3f}" for v in norm_prof))
# fit exponential-ish: report early-vs-late mean and Spearman-ish monotone frac on normalized
early = mean_prof[:len(mean_prof)//3].mean(); late = mean_prof[-len(mean_prof)//3:].mean()
print(f"[decay-avg] early-third mean={early:.3f}  late-third mean={late:.3f}  "
      f"late/early={late/max(early,1e-9):.3f}  norm frac-decreasing={monotone_decay_frac(norm_prof):.2f}")

# free-generation divergence check (patch active on prompt only, then generate greedily)
def free_gen(dir_t, target_scalar):
    cur = ids.clone(); out=[]
    for k in range(H):
        # apply patch only while position p is inside current context (single injection at p)
        patch.dir=dir_t; patch.target=target_scalar; patch.positions=[patch_pos]; patch.on=True
        nxt = run_logits(cur)[0,-1].argmax().view(1,1); patch.on=False
        cur = torch.cat([cur, nxt], dim=1); out.append(int(nxt))
    return out
free_clean = [int(t) for t in seq[0, N:]]
free_W = free_gen(What_t, TARGET)
same = sum(a==b for a,b in zip(free_clean, free_W))
print(f"[free-gen] patched vs clean greedy tokens matching: {same}/{H}  "
      f"patched={tok.decode(free_W)!r}")

handle.remove()

# =============== VERDICTS ===================================================
print("\n" + "="*72)
print("SUMMARY NUMBERS (for artifact)")
print("="*72)
print(f"P1 backward deflection (<p): {back_defl:.3e}  (expect exact 0 = no within-pass back-arrow)")
print(f"P1 within-pass out-span at readout: {decomp(hs_patch[ro][0,patch_pos]-hs_clean[ro][0,patch_pos])[1]:.3f}")
print(f"CTRL zero-patch deflection: {zero_defl:.3e}")
print(f"CTRL next-token flipped: {top_clean!=top_patch}  (KL-proxy {kl:.3f})")
print(f"P2 across-gen out-span decay: first {prof_W[0]:.3f} -> last {prof_W[-1]:.3f} "
      f"(ratio {prof_W[-1]/max(prof_W[0],1e-9):.3f}, {monotone_decay_frac(prof_W)*100:.0f}% steps decreasing)")
