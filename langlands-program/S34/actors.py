import time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
actors=["Peter Scholze","Laurent Fargues","Dennis Gaitsgory","Sam Raskin","David Helm",
        "Maarten Solleveld","David Hansen","Linus Hamann","Yujie Xu","Xinwen Zhu"]
# S34 window claim: 2026-08-19 .. 2026-08-23 ; also scan 08-23 .. 09-07 (since last session)
for lo,hi,label in [("202608190000","202608240000","S34-WINDOW"),("202608230000","202609072359","SINCE-S34")]:
    print("#"*72); print(label, lo, hi)
    for a in actors:
        q=f'au:"{a}" AND submittedDate:[{lo} TO {hi}]'
        url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode(
            {"search_query":q,"max_results":40,"sortBy":"submittedDate","sortOrder":"descending"})
        raw=urllib.request.urlopen(url,timeout=60).read()
        r=ET.fromstring(raw)
        tot=r.findtext('{http://a9.com/-/spec/opensearch/1.1/}totalResults',default='?')
        ents=r.findall('a:entry',ns)
        print(f"  {a:22s} total={tot}")
        for e in ents:
            au=[x.findtext('a:name',default='',namespaces=ns) for x in e.findall('a:author',ns)]
            if not any(a.split()[-1].lower()==n.split()[-1].lower() for n in au): continue
            print("      *",e.findtext('a:id',default='',namespaces=ns).split('/')[-1],
                  "|",e.findtext('a:published',default='',namespaces=ns)[:10],
                  "|"," ".join(e.findtext('a:title',default='',namespaces=ns).split())[:95],
                  "|",", ".join(au)[:80])
        time.sleep(3)
