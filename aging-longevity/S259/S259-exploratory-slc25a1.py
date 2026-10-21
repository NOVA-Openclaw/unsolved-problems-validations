#!/usr/bin/env python3
"""S259 EXPLORATORY retry: SLC25A1 promoter GC-box / E-box scan.
The SLC25A1 block of S259-exploratory-promoters.py died on an Ensembl read timeout
(TimeoutError, exit 1); this re-runs ONLY that block with a longer timeout.
Post-hoc / exploratory, NOT pre-registered."""
import json, urllib.request
UA={"User-Agent":"nova-upr-s259/1.0"}
def get(u,t=90):
    r=urllib.request.Request(u,headers=UA)
    with urllib.request.urlopen(r,timeout=t) as f: return f.read().decode()
def finds(p,s):
    o=[];i=s.find(p)
    while i!=-1: o.append(i); i=s.find(p,i+1)
    return o
def scan(sym, up, dn):
    g=json.loads(get("https://rest.ensembl.org/lookup/symbol/homo_sapiens/%s?content-type=application/json;expand=1"%sym))
    tid=g["canonical_transcript"].split(".")[0]
    tr=[t for t in g.get("Transcript",[]) if t["id"]==tid][0]
    st=tr["strand"]; tss= tr["start"] if st==1 else tr["end"]
    lo,hi=(tss-up,tss+dn) if st==1 else (tss-dn,tss+up)
    seq=json.loads(get("https://rest.ensembl.org/sequence/region/human/%s:%d..%d:%d?content-type=application/json"%(g["seq_region_name"],lo,hi,st)))["seq"].upper()
    rel=lambda i:i-up
    cpg=len(finds("CG",seq)); exp=(seq.count("C")*seq.count("G"))/len(seq)
    print("%-8s %s:%d-%d strand %+d TSS=%d len=%d GC=%.1f%% CpG o/e=%.2f"%(sym,g["seq_region_name"],lo,hi,st,tss,len(seq),100*(seq.count("G")+seq.count("C"))/len(seq),cpg/exp if exp else 0))
    print("          CACGTG n=%d %s"%(len(finds("CACGTG",seq)),[rel(i) for i in finds("CACGTG",seq)]))
    print("          GGGGCGGGG n=%d %s"%(len(finds("GGGGCGGGG",seq)),[rel(i) for i in finds("GGGGCGGGG",seq)]))
    print("          GGGCGG n=%d | CCGCCC n=%d (Sp1 GC-box core, both strands)"%(len(finds("GGGCGG",seq)),len(finds("CCGCCC",seq))))
print("=== SLC25A1 -1000..+200 (exploratory) ===")
scan("SLC25A1",1000,200)
print()
print("=== EGR1 -1000..+200 (exploratory, CArG/SRE control) ===")
scan("EGR1",1000,200)
