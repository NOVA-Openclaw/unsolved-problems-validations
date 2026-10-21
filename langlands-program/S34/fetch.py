import sys, time, urllib.request, xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
ids=["2608.20225","2608.20125","2608.19570","2608.19129","2608.13869","2606.10149"]
for i in ids:
    url=f"https://export.arxiv.org/api/query?id_list={i}&max_results=1"
    raw=urllib.request.urlopen(url, timeout=60).read()
    open(f"raw-{i}.xml","wb").write(raw)
    r=ET.fromstring(raw)
    e=r.find('a:entry',ns)
    print("="*70)
    print("QUERIED:",i)
    if e is None:
        print("  *** NO ENTRY RETURNED ***"); time.sleep(3); continue
    print("  id       :",e.findtext('a:id',default='',namespaces=ns))
    print("  title    :"," ".join(e.findtext('a:title',default='',namespaces=ns).split()))
    print("  authors  :",", ".join(a.findtext('a:name',default='',namespaces=ns) for a in e.findall('a:author',ns)))
    print("  published:",e.findtext('a:published',default='',namespaces=ns))
    print("  updated  :",e.findtext('a:updated',default='',namespaces=ns))
    print("  abstract :"," ".join(e.findtext('a:summary',default='',namespaces=ns).split()))
    time.sleep(3)
