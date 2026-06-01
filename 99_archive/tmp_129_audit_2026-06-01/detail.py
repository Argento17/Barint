# -*- coding: utf-8 -*-
import json, io, os
OUT = r"C:\Bari\tmp_audit_129a"
rep = json.load(io.open(os.path.join(OUT,"audit_summary.json"), encoding="utf-8"))
buf = []
def w(s=""): buf.append(s)

for cat, r in rep.items():
    if "error" in r:
        w("## %s — ERROR %s" % (cat, r["error"])); continue
    w("## " + cat.upper())
    w("traces=%d scored=%d | conf mean/min/max=%s/%s/%s | score mean/min/max=%s/%s/%s" % (
        r["n_traces"], r["n_scored"], r["conf_mean"], r["conf_min"], r["conf_max"],
        r["score_mean"], r["score_min"], r["score_max"]))
    w("bands=%s grades=%s" % (r["band_counts"], r["grade_counts"]))
    w("counts: flagged=%d mktIng=%d lowCatConf=%d evalNonStd=%d dataInsuff=%d scGuess=%d singleCap=%d" % (
        r["n_flagged"], r["n_marketing_ing"], r["n_low_catconf"], r["n_eval_nonstd"],
        r["n_data_insuff"], r["n_scprimary_guess"], r["n_single_cap_driver"]))
    w("\nTOP6 (name | score | grade | conf):")
    for t in r["top6"]:
        w("  + %s | %s | %s | %s" % (t[0], t[1], t[2], t[3]))
    w("BOTTOM6:")
    for t in r["bottom6"]:
        w("  - %s | %s | %s | %s" % (t[0], t[1], t[2], t[3]))
    # severe exceptions: insufficient data, conf<=10, highconf-on-bad, instability, very low cat conf
    sev = []
    for fr in r["flagged"]:
        fset = set(fr["flags"])
        score_sev = 0
        if "data_suff" in " ".join(fr["flags"]): score_sev += 3
        if fr.get("conf") is not None and fr["conf"] <= 10: score_sev += 3
        if "HIGHCONF_on_bad_ingredients" in fset: score_sev += 3
        if "category_instability" in fset: score_sev += 2
        if "low_category_confidence" in fset: score_sev += 1
        if "ingredient_list=marketing_prose" in fset: score_sev += 1
        if "structural_class_guess<0.35" in fset: score_sev += 1
        fr["_sev"] = score_sev
        if score_sev >= 2: sev.append(fr)
    sev.sort(key=lambda x: -x["_sev"])
    w("\nMOST SEVERE EXCEPTIONS (sev>=2), up to 18:")
    for fr in sev[:18]:
        w("  [sev %d] %s | sc=%s gr=%s conf=%s catconf=%s cat=%s | %s" % (
            fr["_sev"], fr["name"], fr["score"], fr["grade"], fr["conf"], fr["cat_conf"], fr["cat"],
            ",".join(fr["flags"])))
    w("\n" + "="*90 + "\n")

with io.open(os.path.join(OUT,"audit_detail.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(buf))
print("wrote audit_detail.md", len(buf), "lines")
