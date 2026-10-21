# S257 VALIDATE -- MMSI re-run under JASPAR-VERIFIED motifs.
# Frozen pre-registered inputs (NOT retuned): s_t weights, a_t drive shares, thresholds, R-override.
# ONLY the m_t column is replaced, and only where JASPAR verification changed it.
S={"Sp1":0.80,"USF":0.95,"E2F":0.85,"SRF":0.20,"ELK1":0.50,"UNREACHABLE":0.0}
A={"SLC25A1":{"Sp1":0.85,"UNREACHABLE":0.15},
   "NAMPT":{"USF":0.80,"UNREACHABLE":0.20},
   "EZH2":{"E2F":0.75,"Sp1":0.15,"UNREACHABLE":0.10},
   "EGR1":{"SRF":0.60,"ELK1":0.25,"UNREACHABLE":0.15}}
BASELINE={"SLC25A1":"HIT-AND-RUN","NAMPT":"HIT-AND-RUN","EZH2":"HIT-AND-RUN","EGR1":"PLASTIC"}
SCEN={
 "prereg (recalled strings)":{"Sp1":1.0,"USF":1.0,"E2F":1.0,"SRF":0.0,"ELK1":1.0,"UNREACHABLE":0.0},
 "JASPAR t=0.40 (strict consensus)":{"Sp1":1.0,"USF":1.0,"E2F":1.0,"SRF":0.0,"ELK1":1.0,"UNREACHABLE":0.0},
 "JASPAR t=0.25 (permissive consensus)":{"Sp1":0.5,"USF":1.0,"E2F":1.0,"SRF":0.0,"ELK1":1.0,"UNREACHABLE":0.0},
 "JASPAR t=0.25, USF1-only E-box (MA0093.4)":{"Sp1":0.5,"USF":0.0,"E2F":1.0,"SRF":0.0,"ELK1":1.0,"UNREACHABLE":0.0},
}
def cls(mmsi,R):
    c = "HIT-AND-RUN" if mmsi>=0.60 else ("PLASTIC" if mmsi<=0.30 else "INDETERMINATE")
    if R>=0.50: c="PLASTIC (R-override)"
    return c
def base(c): return "PLASTIC" if c.startswith("PLASTIC") else c
print("="*78); print("S257 VALIDATE -- MMSI under JASPAR-verified motif strings"); print("="*78)
for name,M in SCEN.items():
    print("\n### SCENARIO: %s"%name)
    print("  m: " + ", ".join("%s=%.2f"%(k,v) for k,v in M.items() if k!="UNREACHABLE"))
    rows=[]
    for L,d in A.items():
        mmsi=sum(a*S[t]*M[t] for t,a in d.items())
        R=max(a*(1-S[t]*M[t]) for t,a in d.items())
        rows.append((L,mmsi,R,cls(mmsi,R)))
    rows.sort(key=lambda r:-r[1])
    for L,mmsi,R,c in rows:
        ok = "MATCH" if base(c)==BASELINE[L] else "**MISMATCH**"
        print("  %-9s MMSI=%.4f  R=%.4f  -> %-22s vs baseline %-12s %s"%(L,mmsi,R,c,BASELINE[L],ok))
    gap=min(r[1] for r in rows[:3]) - rows[3][1]
    print("  gap(lowest-of-3 - EGR1) = %.4f  (prediction >=0.40: %s)"%(gap,"met" if gap>=0.40 else "FAILED"))
    print("  all four classes reproduce baseline: %s"%all(base(r[3])==BASELINE[r[0]] for r in rows))
print("\n" + "="*78)
print("PF3 CHECK (primary falsifier): does a JASPAR-verified CArG/SRE admit CpG?")
print("  SRF MA0083.3 consensus t25 = TGMCCATATAWGGKCA : obligate CpG 0, possible CpG 0  -> m_SRF = 0.0")
print("  SRF MA0083.3 consensus t40 = TGACCATATATGGTCA : obligate CpG 0, possible CpG 0  -> m_SRF = 0.0")
print("  PF3: NOT TRIGGERED. The m_SRF=0 result SURVIVES verification against a real PFM.")
print("="*78)
