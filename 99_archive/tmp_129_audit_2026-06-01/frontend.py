# -*- coding: utf-8 -*-
import json, io, os
FE = r"C:\Users\HP\bari\src\data\comparisons"
OUT = r"C:\Bari\tmp_audit_129a"
files = {
 "hummus":"hummus_frontend_v3.json","maadanim":"maadanim_frontend_v2.json",
 "snacks":"snacks_frontend_v2.json","yogurts":"yogurts_frontend_v1.json",
 "bread":"bread_frontend_v2.json",
}
buf=[]
def w(s=""): buf.append(s)
for cat,fn in files.items():
    d=json.load(io.open(os.path.join(FE,fn),encoding="utf-8"))
    meta=d.get("_meta",{})
    prods=d.get("products",[])
    w("## %s  (%s)" % (cat, fn))
    w("meta: "+json.dumps(meta,ensure_ascii=False)[:600])
    w("n_displayed=%d" % len(prods))
    if prods:
        w("product[0] keys: "+str(list(prods[0].keys())))
        # try to find score & name & id & confidence fields
        p=prods[0]
        w("product[0] sample: "+json.dumps(p,ensure_ascii=False)[:800])
    # list names+score+confidence if available
    def g(p,*ks):
        for k in ks:
            if k in p: return p[k]
        return None
    w("displayed rows (name | score | grade | confidence):")
    for p in prods:
        nm=g(p,"name","name_he","productName","title")
        sc=g(p,"score","bsipScore","finalScore","overallScore")
        gr=g(p,"grade","gradeLetter")
        cf=g(p,"confidence","confidenceBand","confidence_band")
        w("  - %s | %s | %s | %s" % (nm,sc,gr,cf))
    w("\n"+"="*80+"\n")
io.open(os.path.join(OUT,"frontend_dump.md"),"w",encoding="utf-8").write("\n".join(buf))
print("wrote frontend_dump.md")
