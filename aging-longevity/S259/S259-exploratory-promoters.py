#!/usr/bin/env python3
"""S259 EXPLORATORY (post-hoc, NOT pre-registered, does not alter the H5 call):
widen the NAMPT E-box scan and sanity-check the TSS/window machinery on a positive control."""
import json, urllib.request
UA={"User-Agent":"nova-upr-s259/1.0"}
def get(u,t=30):
    import urllib.request
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
    if st==1: lo,hi=tss-up,tss+dn
    else: lo,hi=tss-dn,tss+up
    seq=json.loads(get("https://rest.ensembl.org/sequence/region/human/%s:%d..%d:%d?content-type=application/json"%(g["seq_region_name"],lo,hi,st)))["seq"].upper()
    rel=lambda i:i-up
    can=[rel(i) for i in finds("CACGTG",seq)]
    v1=[rel(i) for i in finds("CATGTG",seq)]
    v2=[rel(i) for i in finds("CACATG",seq)]
    cpg=len(finds("CG",seq))
    exp=(seq.count("C")*seq.count("G"))/len(seq)
    print("%-8s %s:%d-%d strand %+d TSS=%d len=%d GC=%.1f%% CpG o/e=%.2f" % (sym,g["seq_region_name"],lo,hi,st,tss,len(seq),100*(seq.count("G")+seq.count("C"))/len(seq), cpg/exp if exp else 0))
    print("          CACGTG n=%d %s" % (len(can),can))
    print("          CATGTG n=%d %s" % (len(v1),v1))
    print("          CACATG n=%d %s" % (len(v2),v2))
    print("          GGGGCGGGG (Sp1 GC-box) n=%d | GGGCGG n=%d | CCGCCC n=%d" % (len(finds("GGGGCGGGG",seq)),len(finds("GGGCGG",seq)),len(finds("CCGCCC",seq))))
    return can,v1,v2

print("=== pre-registered window, restated ===")
scan("NAMPT",1000,200)
print()
print("=== EXPLORATORY wider windows (post-hoc, labelled) ===")
for up,dn in ((2000,500),(5000,1000)):
    print("-- NAMPT -%d..+%d --"%(up,dn)); scan("NAMPT",up,dn); print()
print("=== positive control: PER1 (canonical CLOCK:BMAL1 E-box gene) -1000..+200 ===")
scan("PER1",1000,200)
print()
print("=== SLC25A1 promoter, Sp1 GC-box presence check (exploratory) -1000..+200 ===")
scan("SLC25A1",1000,200)
