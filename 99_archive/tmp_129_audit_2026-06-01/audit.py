# -*- coding: utf-8 -*-
import json, os, glob, io, statistics as st

BASE = r"C:\Bari\02_products"
OUT = r"C:\Bari\tmp_audit_129a"

# (category_label, run_dir_with_products, kind)
RUNS = {
    "hummus":   os.path.join(BASE, "hummus", "intelligence_bsip2", "run_hummus_002", "products"),
    "maadanim": os.path.join(BASE, "maadanim", "bsip2_outputs", "run_maadanim_001", "products"),
    "snacks":   os.path.join(BASE, "snack_bars", "bsip2_outputs", "run_snack_bars_synthesis_001", "products"),
    "yogurts":  os.path.join(BASE, "yogurt_system", "bsip2_outputs", "run_yogurt_001", "products"),
    "bread":    os.path.join(BASE, "bread_light", "bsip2_outputs", "run_synthesis_calibration_001", "products"),
    "milk":     os.path.join(BASE, "milk_and_alternatives", "intelligence_bsip2", "run_004_recalibrated", "products"),
}

def load_traces(pdir):
    rows = []
    for tp in glob.glob(os.path.join(pdir, "*", "bsip2_trace.json")):
        try:
            with io.open(tp, encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            rows.append({"_load_error": str(e), "_path": tp})
            continue
        ir = d.get("input_reference", {}) or {}
        l1 = d.get("L1_observed_signals", {}) or {}
        sc = d.get("structural_class", {}) or {}
        ing = l1.get("ingredient_list") or []
        # heuristic: ingredient list looks like marketing prose, not a real ingredient list
        joined = " ".join(ing) if isinstance(ing, list) else str(ing)
        marketing = any(tok in joined for tok in ["מסייע", "חשוב בתזונה", "טרי", "מיחזור", "האריזה", "עשיר בחלבון", "מומלץ", "ניתנת"]) or (len(joined) > 220 and len(ing) <= 5)
        rows.append({
            "id": ir.get("canonical_product_id"),
            "name": ir.get("product_name_he"),
            "category": d.get("category"),
            "cat_conf": d.get("category_confidence"),
            "cat_band": d.get("category_confidence_band"),
            "cat_instab": d.get("category_instability_flag"),
            "sec_cat": d.get("secondary_category"),
            "sec_conf": d.get("secondary_confidence"),
            "nova": d.get("nova_proxy"),
            "nova_conf": d.get("nova_confidence"),
            "nova_band": d.get("nova_confidence_band"),
            "conf": d.get("confidence_score"),
            "conf_band": d.get("confidence_band"),
            "conf_red": d.get("confidence_reductions") or [],
            "eval_status": d.get("evaluation_status"),
            "data_suff": d.get("data_sufficiency"),
            "score": d.get("final_score_estimate"),
            "grade": d.get("grade_estimate"),
            "wds": d.get("weighted_dimension_score"),
            "binding_cap": d.get("binding_cap"),
            "drivers": d.get("explanation_drivers") or [],
            "unresolved": d.get("unresolved_flags") or [],
            "ing_count": l1.get("ingredient_count"),
            "ing_qual": l1.get("ingredient_text_quality"),
            "missing_nutr": l1.get("missing_nutrition_fields") or [],
            "trust": l1.get("bsip1_trust_level"),
            "trust_score": l1.get("bsip1_trust_score"),
            "sc_primary": sc.get("primary"),
            "sc_primary_conf": sc.get("primary_confidence"),
            "sc_between": sc.get("is_between_worlds"),
            "marketing_ingredients": marketing,
            "load_errors": ir.get("load_errors") or [],
            "_path": tp,
        })
    return rows

def num(x):
    return x if isinstance(x, (int, float)) else None

report = {}
allrows = {}
for cat, pdir in RUNS.items():
    if not os.path.isdir(pdir):
        report[cat] = {"error": "missing dir " + pdir}
        continue
    rows = load_traces(pdir)
    allrows[cat] = rows
    scored = [r for r in rows if num(r.get("score")) is not None]
    confs = [num(r.get("conf")) for r in rows if num(r.get("conf")) is not None]
    catconfs = [num(r.get("cat_conf")) for r in rows if num(r.get("cat_conf")) is not None]
    novaconfs = [num(r.get("nova_conf")) for r in rows if num(r.get("nova_conf")) is not None]
    # bands
    band_counts = {}
    for r in rows:
        b = r.get("conf_band")
        band_counts[b] = band_counts.get(b, 0) + 1
    grade_counts = {}
    for r in rows:
        g = r.get("grade")
        grade_counts[g] = grade_counts.get(g, 0) + 1
    # anomaly flags
    def flag(r):
        fl = []
        c = num(r.get("conf"))
        if r.get("eval_status") not in (None, "standard"):
            fl.append("eval_status=" + str(r.get("eval_status")))
        if r.get("data_suff") not in (None, "sufficient"):
            fl.append("data_suff=" + str(r.get("data_suff")))
        if r.get("marketing_ingredients"):
            fl.append("ingredient_list=marketing_prose")
        if c is not None and c >= 85 and r.get("marketing_ingredients"):
            fl.append("HIGHCONF_on_bad_ingredients")
        if num(r.get("cat_conf")) is not None and num(r.get("cat_conf")) < 0.6:
            fl.append("low_category_confidence")
        if r.get("cat_instab"):
            fl.append("category_instability")
        if num(r.get("sc_primary_conf")) is not None and num(r.get("sc_primary_conf")) < 0.35:
            fl.append("structural_class_guess<0.35")
        if (not r.get("ing_count")) or (r.get("ing_count") or 0) <= 1:
            fl.append("ingredient_count<=1")
        if len(r.get("missing_nutr") or []) >= 3:
            fl.append("missing>=3_nutr_fields")
        # weak explanation: single driver that is just a cap
        drv = r.get("drivers") or []
        if len(drv) == 1 and ("Binding cap" in drv[0] or "DOMINANT" in drv[0]):
            fl.append("single_cap_driver")
        if r.get("unresolved"):
            fl.append("unresolved_flags")
        return fl
    flagged = []
    for r in rows:
        fl = flag(r)
        if fl:
            flagged.append({"id": r["id"], "name": r["name"], "score": r["score"], "grade": r["grade"],
                            "conf": r["conf"], "conf_band": r["conf_band"], "cat": r["category"],
                            "cat_conf": r["cat_conf"], "flags": fl})
    # rankings
    sscored = sorted(scored, key=lambda r: r["score"])
    top = [(r["name"], r["score"], r["grade"], r["conf"]) for r in sscored[-6:]][::-1]
    bottom = [(r["name"], r["score"], r["grade"], r["conf"]) for r in sscored[:6]]
    report[cat] = {
        "n_traces": len(rows),
        "n_scored": len(scored),
        "conf_mean": round(st.mean(confs), 1) if confs else None,
        "conf_min": min(confs) if confs else None,
        "conf_max": max(confs) if confs else None,
        "cat_conf_mean": round(st.mean(catconfs), 3) if catconfs else None,
        "cat_conf_min": min(catconfs) if catconfs else None,
        "nova_conf_mean": round(st.mean(novaconfs), 3) if novaconfs else None,
        "score_mean": round(st.mean([r["score"] for r in scored]), 1) if scored else None,
        "score_min": min([r["score"] for r in scored]) if scored else None,
        "score_max": max([r["score"] for r in scored]) if scored else None,
        "band_counts": band_counts,
        "grade_counts": grade_counts,
        "n_flagged": len(flagged),
        "n_marketing_ing": sum(1 for r in rows if r.get("marketing_ingredients")),
        "n_low_catconf": sum(1 for r in rows if num(r.get("cat_conf")) is not None and num(r.get("cat_conf")) < 0.6),
        "n_eval_nonstd": sum(1 for r in rows if r.get("eval_status") not in (None, "standard")),
        "n_data_insuff": sum(1 for r in rows if r.get("data_suff") not in (None, "sufficient")),
        "n_scprimary_guess": sum(1 for r in rows if num(r.get("sc_primary_conf")) is not None and num(r.get("sc_primary_conf")) < 0.35),
        "n_single_cap_driver": sum(1 for r in rows if len(r.get("drivers") or [])==1 and ("Binding cap" in (r.get("drivers") or [""])[0] or "DOMINANT" in (r.get("drivers") or [""])[0])),
        "top6": top,
        "bottom6": bottom,
        "flagged": flagged,
    }

with io.open(os.path.join(OUT, "audit_summary.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# ASCII-safe console digest
print("CATEGORY | traces | scored | conf(mean/min/max) | catconf(mean/min) | score(mean/min/max) | flagged | mktIng | lowCat | evalNonStd | dataInsuff | scGuess | singleCap")
for cat, r in report.items():
    if "error" in r:
        print(cat, r["error"]); continue
    print("%-9s| %4d | %4d | %s/%s/%s | %s/%s | %s/%s/%s | %3d | %3d | %3d | %3d | %3d | %3d | %3d" % (
        cat, r["n_traces"], r["n_scored"], r["conf_mean"], r["conf_min"], r["conf_max"],
        r["cat_conf_mean"], r["cat_conf_min"], r["score_mean"], r["score_min"], r["score_max"],
        r["n_flagged"], r["n_marketing_ing"], r["n_low_catconf"], r["n_eval_nonstd"], r["n_data_insuff"],
        r["n_scprimary_guess"], r["n_single_cap_driver"]))
    print("   bands:", r["band_counts"], " grades:", r["grade_counts"])
print("\nWrote audit_summary.json")
