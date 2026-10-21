#!/usr/bin/env python3
"""S259 VALIDATE: HOCOMOCO v12 replication of the S258 m* table + NAMPT promoter E-box variant.
Estimator frozen per S258 2a / S259 prereg 1a. stdlib only."""
import json, re, urllib.request, sys

UA = {"User-Agent": "nova-upr-s259/1.0"}

def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode()

# ---------- estimator (frozen, identical to S258) ----------
def mstar(counts, laplace=False):
    L = len(counts)
    probs = []
    for col in counts:
        c = [x + (1.0 if laplace else 0.0) for x in col]
        s = sum(c)
        probs.append([x / s for x in c])
    prod = 1.0
    for i in range(L - 1):
        prod *= (1.0 - probs[i][1] * probs[i + 1][2])   # order A,C,G,T
    m_raw = 1.0 - prod
    m_bg = 1.0 - (1.0 - 0.0625) ** (L - 1)
    m = (m_raw - m_bg) / (1.0 - m_bg)
    return max(0.0, min(1.0, m)), m_raw, m_bg, L

# ---------- HOCOMOCO fetch ----------
BASE = "https://hocomoco12.autosome.org/final_bundle/hocomoco12/H12CORE/pcm/"
TFS = ["SP1", "SRF", "USF1", "USF2", "E2F1", "E2F4", "ELK1"]
SRC = ["P", "S", "M", "H"]
QUAL = ["A", "B", "C", "D"]

ANNO = "https://hocomoco12.autosome.org/final_bundle/hocomoco12/H12CORE/H12CORE_annotation.jsonl"
_anno_cache = {}
def load_anno():
    if _anno_cache: return _anno_cache
    txt = get(ANNO, timeout=120)
    for name in re.findall(r'"name":"([A-Z0-9]+\.H12CORE\.[0-9]+\.[A-Z]+\.[A-Z])"', txt):
        tf = name.split(".")[0]
        _anno_cache.setdefault(tf, [])
        if name not in _anno_cache[tf]:
            _anno_cache[tf].append(name)
    return _anno_cache

def fetch_pcm(tf):
    anno = load_anno()
    cands = sorted(anno.get(tf, []), key=lambda n: int(n.split(".")[2]))
    for mid in cands:
        try:
            txt = get(BASE + mid + ".pcm", timeout=30)
        except Exception as e:
            print("  (fetch fail %s: %s)" % (mid, e)); continue
        rows = []
        for line in txt.strip().splitlines():
            if line.startswith(">"): continue
            parts = line.split()
            if len(parts) == 4:
                rows.append([float(x) for x in parts])
        if rows:
            return mid, rows
    return None, None

print("=== S259 HOCOMOCO v12 H12CORE m* (estimator frozen from S258) ===")
mh = {}
mh_l = {}
ids = {}
for tf in TFS:
    mid, rows = fetch_pcm(tf)
    if rows is None:
        print("%-6s FETCH FAILED" % tf); continue
    m, mraw, mbg, L = mstar(rows)
    ml, _, _, _ = mstar(rows, laplace=True)
    mh[tf] = m; mh_l[tf] = ml; ids[tf] = mid
    print("%-6s %-24s L=%2d m_raw=%.4f m_bg=%.4f m*=%.4f  m*(Laplace)=%.4f" % (tf, mid, L, mraw, mbg, m, ml))

JASPAR = {"SP1":0.5912,"SRF":0.0000,"USF1":0.0000,"USF2":0.9915,"E2F1":0.9931,"E2F4":0.9934,"ELK1":0.9826}
print()
print("=== JASPAR (S258) vs HOCOMOCO (S259) ===")
for tf in TFS:
    if tf in mh:
        print("%-6s JASPAR %.4f  HOCOMOCO %.4f  delta %+.4f" % (tf, JASPAR[tf], mh[tf], mh[tf]-JASPAR[tf]))

# ---------- MMSI with frozen s_t, a_t ----------
S = {"Sp1":0.80, "USF":0.95, "E2F":0.85, "SRF":0.20, "ELK1":0.50, "UNREACHABLE":0.00}
A = {
 "SLC25A1": {"Sp1":0.85, "UNREACHABLE":0.15},
 "NAMPT":   {"USF":0.80, "UNREACHABLE":0.20},
 "EZH2":    {"E2F":0.75, "Sp1":0.15, "UNREACHABLE":0.10},
 "EGR1":    {"SRF":0.60, "ELK1":0.25, "UNREACHABLE":0.15},
}
def classify(mmsi, R):
    if R >= 0.50: return "PLASTIC"
    if mmsi >= 0.60: return "HIT-AND-RUN"
    if mmsi <= 0.30: return "PLASTIC"
    return "INDETERMINATE"

def run_mmsi(mmap, label):
    out = {}
    print()
    print("=== MMSI (%s) — s_t, a_t, thresholds FROZEN ===" % label)
    for locus, drives in A.items():
        mmsi = 0.0; R = 0.0
        for d, a in drives.items():
            m = mmap.get(d, 0.0)
            b = S[d] * m
            mmsi += a * b
            R = max(R, a * (1.0 - b))
        cls = classify(mmsi, R)
        out[locus] = (mmsi, R, cls)
        print("%-8s MMSI=%.4f R=%.4f -> %s" % (locus, mmsi, R, cls))
    pos = [v[0] for k, v in out.items() if k != "EGR1"]
    gap = min(pos) - out["EGR1"][0]
    print("gap(min positive - EGR1) = %.4f" % gap)
    return out, gap

def drivemap(mh, usf_tf, lap=False):
    src = mh_l if lap else mh
    return {"Sp1": src["SP1"], "USF": src[usf_tf], "E2F": (src["E2F1"]+src["E2F4"])/2.0,
            "SRF": src["SRF"], "ELK1": src["ELK1"], "UNREACHABLE": 0.0}

primary, gap_p = run_mmsi(drivemap(mh, "USF2"), "HOCOMOCO, USF=USF2, no pseudocount")
lapres, gap_l  = run_mmsi(drivemap(mh, "USF2", lap=True), "HOCOMOCO, USF=USF2, Laplace sensitivity")
usf1res, gap_u = run_mmsi(drivemap(mh, "USF1"), "HOCOMOCO, USF=USF1 scenario")

# s_SRF invariance probe for EGR1
print()
print("=== EGR1 s_SRF invariance probe (HOCOMOCO) ===")
for s_srf in (0.20, 0.50, 0.80, 1.00):
    S2 = dict(S); S2["SRF"] = s_srf
    dm = drivemap(mh, "USF2")
    mmsi = sum(a * S2[d] * dm[d] for d, a in A["EGR1"].items())
    R = max(a * (1.0 - S2[d]*dm[d]) for d, a in A["EGR1"].items())
    print("s_SRF=%.2f -> EGR1 MMSI=%.4f R=%.4f %s" % (s_srf, mmsi, R, classify(mmsi, R)))

# ---------- NAMPT promoter E-box ----------
print()
print("=== NAMPT proximal promoter E-box scan (Ensembl GRCh38, window -1000..+200 vs TSS) ===")
g = json.loads(get("https://rest.ensembl.org/lookup/symbol/homo_sapiens/NAMPT?content-type=application/json;expand=1"))
tid = g["canonical_transcript"].split(".")[0]
tr = [t for t in g.get("Transcript", []) if t["id"] == tid]
tr = tr[0] if tr else None
chrom = g["seq_region_name"]; strand = g["strand"]
if tr:
    tss = tr["start"] if tr["strand"] == 1 else tr["end"]
    strand = tr["strand"]
else:
    tss = g["start"] if strand == 1 else g["end"]
print("gene=%s chrom=%s strand=%d canonical=%s TSS=%d" % (g["id"], chrom, strand, tid, tss))
if strand == 1:
    lo, hi = tss - 1000, tss + 200
else:
    lo, hi = tss - 200, tss + 1000
url = "https://rest.ensembl.org/sequence/region/human/%s:%d..%d:%d?content-type=application/json" % (chrom, lo, hi, strand)
seq = json.loads(get(url))["seq"].upper()
print("window %s:%d-%d strand %d  len=%d" % (chrom, lo, hi, strand, len(seq)))
print("GC%% = %.1f" % (100.0*(seq.count("G")+seq.count("C"))/len(seq)))

def finds(pat, s):
    out = []; i = s.find(pat)
    while i != -1:
        out.append(i); i = s.find(pat, i+1)
    return out

# position relative to TSS: index 0 of seq corresponds to TSS-1000 on transcribed strand
def rel(i): return i - 1000
can = finds("CACGTG", seq)
var1 = finds("CATGTG", seq)
var2 = finds("CACATG", seq)
print("canonical CACGTG : n=%d positions(rel TSS)=%s" % (len(can), [rel(i) for i in can]))
print("variant  CATGTG  : n=%d positions(rel TSS)=%s" % (len(var1), [rel(i) for i in var1]))
print("variant  CACATG  : n=%d positions(rel TSS)=%s" % (len(var2), [rel(i) for i in var2]))
nearest_can = min([abs(rel(i)) for i in can]) if can else None
print("nearest canonical |dist to TSS| = %s" % nearest_can)
if can:
    nampt_call = "CANONICAL-PRESENT -> USF2/canonical m* applies; NAMPT HIT-AND-RUN stands"
elif var1 or var2:
    nampt_call = "VARIANT-ONLY -> USF1 scenario becomes primary; NAMPT collapses"
else:
    nampt_call = "NO E-BOX IN WINDOW -> H5 FIRES: USF drive assignment unsupported at sequence level"
print("NAMPT CALL: " + nampt_call)

# ---------- ledgers ----------
print()
print("=== PREDICTION LEDGER ===")
preds = [
 ("Q1 HOCOMOCO SP1 m* in [0.40,0.80]", 0.40 <= mh["SP1"] <= 0.80, "%.4f" % mh["SP1"]),
 ("Q2 HOCOMOCO SRF m* <= 0.05", mh["SRF"] <= 0.05, "%.4f" % mh["SRF"]),
 ("Q3 E2F1/E2F4/ELK1/USF2 m* >= 0.90", all(mh[t] >= 0.90 for t in ("E2F1","E2F4","ELK1","USF2")),
    ",".join("%s=%.4f" % (t, mh[t]) for t in ("E2F1","E2F4","ELK1","USF2"))),
 ("Q4 HOCOMOCO USF1 m* >= 0.90 (contrarian)", mh["USF1"] >= 0.90, "%.4f" % mh["USF1"]),
 ("Q5 classes match S258 primary", [primary[k][2] for k in ("NAMPT","EZH2","SLC25A1","EGR1")] ==
    ["HIT-AND-RUN","HIT-AND-RUN","INDETERMINATE","PLASTIC"],
    str([primary[k][2] for k in ("NAMPT","EZH2","SLC25A1","EGR1")])),
 ("Q6 >=1 canonical CACGTG in window", len(can) >= 1, "n=%d" % len(can)),
 ("Q7 Laplace shift < 0.05, no class flip",
    max(abs(mh_l[t]-mh[t]) for t in mh) < 0.05 and
    all(lapres[k][2] == primary[k][2] for k in primary),
    "maxshift=%.4f" % max(abs(mh_l[t]-mh[t]) for t in mh)),
]
for name, ok, detail in preds:
    print("%-45s %s  (%s)" % (name, "HELD" if ok else "MISSED", detail))

print()
print("=== FALSIFIER LEDGER ===")
fals = [
 ("H1 HOCOMOCO SP1 m* >= 0.80 (JASPAR artefact)", mh["SP1"] >= 0.80, "%.4f" % mh["SP1"]),
 ("H2 HOCOMOCO SRF m* > 0.05", mh["SRF"] > 0.05, "%.4f" % mh["SRF"]),
 ("H3 obligate-CpG motif m* < 0.90", any(mh[t] < 0.90 for t in ("E2F1","E2F4","ELK1","USF2")),
    ",".join("%s=%.4f" % (t, mh[t]) for t in ("E2F1","E2F4","ELK1","USF2"))),
 ("H4 Laplace flips a class", any(lapres[k][2] != primary[k][2] for k in primary), ""),
 ("H5 zero E-box of either type in window", not (can or var1 or var2), "can=%d var=%d" % (len(can), len(var1)+len(var2))),
]
fired = []
for name, ok, detail in fals:
    print("%-48s %s  (%s)" % (name, "TRIGGERED" if ok else "clear", detail))
    if ok: fired.append(name.split()[0])
print()
print("FIRED FALSIFIERS: %s" % (", ".join(fired) if fired else "none"))
print("COMPUTED VERDICT: %s" % ("REPLICATED / S258 CONFIRMED" if not fired else "DISCREPANCY (" + ",".join(fired) + ")"))
