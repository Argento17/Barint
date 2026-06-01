# -*- coding: utf-8 -*-
import json, io, glob, os
D = r"C:\Bari\02_products\bread_retail_003\bsip2"
FE = r"C:\Users\HP\bari\src\data\comparisons\bread_frontend_v2.json"
rows=[]
for f in glob.glob(os.path.join(D,"bsip2_shufersal_*.json")):
    d=json.load(io.open(f,encoding="utf-8"))
    rows.append(d)
# displayed ids
fe=json.load(io.open(FE,encoding="utf-8"))
disp_ids=set(p["id"] for p in fe["products"])
disp_names={p["id"]:p["name"] for p in fe["products"]}

def pid(d):
    return "shufersal_"+str(d.get("barcode") or d.get("product_id"))

conf_counts={}; grade_counts={}; deg_counts={}; noing=0
disp_rows=[]
for d in rows:
    cl=d.get("confidence_label_he"); conf_counts[cl]=conf_counts.get(cl,0)+1
    g=d.get("final_grade"); grade_counts[g]=grade_counts.get(g,0)+1
    dl=d.get("degradation_level"); deg_counts[dl]=deg_counts.get(dl,0)+1
    if not d.get("has_ingredients"): noing+=1
    rid=pid(d)
    if rid in disp_ids:
        disp_rows.append(d)

buf=[]
def w(s=""): buf.append(s)
w("BREAD retail_003 corpus: %d files" % len(rows))
w("confidence_label_he counts: "+json.dumps(conf_counts,ensure_ascii=False))
w("final_grade counts: "+json.dumps(grade_counts,ensure_ascii=False))
w("degradation_level counts: "+json.dumps(deg_counts,ensure_ascii=False))
w("has_ingredients == False: %d / %d" % (noing,len(rows)))
w("\nDISPLAYED matched %d of %d frontend ids" % (len(disp_rows),len(disp_ids)))
w("\nDISPLAYED bread (name | final_score | grade | conf_label | has_ingredients | degradation):")
for d in sorted(disp_rows,key=lambda x:-(x.get('final_score') or 0)):
    w("  %s | %s | %s | %s | ing=%s | %s" % (
        d.get("name_he"), d.get("final_score"), d.get("final_grade"),
        d.get("confidence_label_he"), d.get("has_ingredients"), d.get("degradation_level")))
# displayed ids not matched
matched=set(pid(d) for d in disp_rows)
miss=[disp_names[i] for i in disp_ids if i not in matched]
w("\nFrontend ids NOT found in retail_003 corpus (%d): %s" % (len(miss), " | ".join(miss)))
io.open(os.path.join(r"C:\Bari\tmp_audit_129a","bread_audit.md"),"w",encoding="utf-8").write("\n".join(buf))
print("done; displayed matched",len(disp_rows),"noing",noing,"conf",conf_counts)
