#!/usr/bin/env python3
"""S259 EXPLORATORY retry 2: EGR1 promoter CArG/SRE scan only.
Previous block died on an Ensembl read timeout. Post-hoc, NOT pre-registered."""
import json, urllib.request, re
UA={"User-Agent":"nova-upr-s259/1.0"}
def get(u,t=120):
    r=urllib.request.Request(u,headers=UA)
    with urllib.request.urlopen(r,timeout=t) as f: return f.read().decode()
def finds(p,s):
    o=[];i=s.find(p)
    while i!=-1: o.append(i); i=s.find(p,i+1)
    return o
g=json.loads(get("https://rest.ensembl.org/lookup/symbol/homo_sapiens/EGR1?content-type=application/json;expand=1"))
tid=g["canonical_transcript"].split(".")[0]
tr=[t for t in g.get("Transcript",[]) if t["id"]==tid][0]
st=tr["strand"]; tss= tr["start"] if st==1 else tr["end"]
lo,hi=(tss-1000,tss+200) if st==1 else (tss-200,tss+1000)
seq=json.loads(get("https://rest.ensembl.org/sequence/region/human/%s:%d..%d:%d?content-type=application/json"%(g["seq_region_name"],lo,hi,st)))["seq"].upper()
rel=lambda i:i-1000
cpg=len(finds("CG",seq)); exp=(seq.count("C")*seq.count("G"))/len(seq)
print("EGR1 %s:%d-%d strand %+d TSS=%d len=%d GC=%.1f%% CpG o/e=%.2f"%(g["seq_region_name"],lo,hi,st,tss,len(seq),100*(seq.count("G")+seq.count("C"))/len(seq),cpg/exp))
carg=[m.start()-1000 for m in re.finditer(r'(?=CC[ATWSKMRY]{6}GG)', seq)]
cargW=[m.start()-1000 for m in re.finditer(r'(?=CC[AT]{6}GG)', seq)]
print("CArG CC(A/T)6GG n=%d positions(rel TSS)=%s"%(len(cargW),cargW))
print("CArG-like CCn6GG n=%d"%len(carg))
# CpG inside each CArG box
for p in cargW:
    box=seq[p+1000:p+1010]
    print("   box at %+d: %s  contains CG: %s"%(p,box,"CG" in box))
print("ELK1 core GGAA/TTCC n=%d/%d"%(len(finds("GGAA",seq)),len(finds("TTCC",seq))))
print("CCGGAAGT (ELK1 ETS with CpG) n=%d | CCGGAA n=%d"%(len(finds("CCGGAAGT",seq)),len(finds("CCGGAA",seq))))
