import json,urllib.request,sys
# S257 VALIDATE: verify pre-registered motif consensus strings against JASPAR CORE.
# CpG occupancy computed ANALYTICALLY from the per-position allowed-letter sets
# (exhaustive IUPAC expansion is intractable for N-containing columns: 4^16).
IDS={"SRF":"MA0083","SP1":"MA0079","USF1":"MA0093","USF2":"MA0526","E2F1":"MA0024","E2F4":"MA0470","ELK1":"MA0028"}
IUPAC={'A':'A','C':'C','G':'G','T':'T','R':'AG','Y':'CT','S':'CG','W':'AT','K':'GT','M':'AC','B':'CGT','D':'AGT','H':'ACT','V':'ACG','N':'ACGT'}
REV={frozenset(v):k for k,v in IUPAC.items()}
def get(u):
    with urllib.request.urlopen(u,timeout=30) as r: return json.load(r)
def latest(base):
    d=get("https://jaspar.elixir.no/api/v1/matrix/?search=%s&format=json"%base)
    vs=[x for x in d["results"] if x["base_id"]==base]
    vs.sort(key=lambda x:int(x["version"]))
    return vs[-1]["matrix_id"]
def colsets(pfm,thr):
    cols=list(zip(pfm["A"],pfm["C"],pfm["G"],pfm["T"]))
    out=[]
    for c in cols:
        tot=sum(c) or 1
        f=[x/tot for x in c]
        s=set(b for b,p in zip("ACGT",f) if p>=thr)
        if not s: s={"ACGT"[f.index(max(f))]}
        out.append(s)
    return out
def render(sets): return "".join(REV.get(frozenset(s),'N') for s in sets)
def core(sets,thr_ic=0.0):
    # trim flanking fully-degenerate (N) columns
    i=0; j=len(sets)
    while i<j and len(sets[i])==4: i+=1
    while j>i and len(sets[j-1])==4: j-=1
    return sets[i:j],i,j
def cpg_analytic(sets):
    oblig=0; poss=0
    for i in range(len(sets)-1):
        a,b=sets[i],sets[i+1]
        if a=={"C"} and b=={"G"}: oblig+=1
        if "C" in a and "G" in b: poss+=1
    return oblig,poss
PREREG={"SRF":"CCWWWWWWGG","SP1":"GGGGCGGGG","USF1":"CACGTG","USF2":"CACGTG","E2F1":"TTTSSCGC","E2F4":"TTTSSCGC","ELK1":"SCGGAAGY"}
res={}
for tf,base in sorted(IDS.items()):
    mid=latest(base); d=get("https://jaspar.elixir.no/api/v1/matrix/%s/?format=json"%mid)
    entry={"matrix_id":mid,"jaspar_name":d["name"],"prereg":PREREG[tf],"length":len(d["pfm"]["A"])}
    for thr,tag in ((0.25,"t25"),(0.40,"t40")):
        sets=colsets(d["pfm"],thr); c,i,j=core(sets)
        ob,po=cpg_analytic(c)
        entry[tag]={"full":render(sets),"core":render(c),"core_span":[i,j],"obligate_cpg":ob,"possible_cpg":po,
                    "m":1.0 if ob>0 else (0.5 if po>0 else 0.0)}
    res[tf]=entry
print(json.dumps(res,indent=2))
