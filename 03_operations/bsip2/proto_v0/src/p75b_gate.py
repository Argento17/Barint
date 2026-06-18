"""P75b EV-058 bleed sim + migration gate."""
import json, os, pathlib, sys
ROOT = pathlib.Path(r"C:/Bari")
SRC = ROOT / "03_operations/bsip2/proto_v0/src"
OUT = ROOT / "02_products/cookies_coffee/bsip2_outputs"
sys.path.insert(0, str(SRC))
for k,v in {
    "BARI_RECAL_P0":"off","BARI_GRAD_SODIUM_V1":"off","BARI_SODIUM_SHELF_RELATIVE_V1":"off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off","BARI_REDLABEL_V1":"off","BARI_SODIUM_CEREAL":"off",
    "BARI_GLASSBOX_W4":"on",
}.items(): os.environ[k]=v
from router_v2 import _check_anchors, classify_category
from signal_extractor import extract_signals
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product

def load_trace(run_dir, barcode):
    for p in (run_dir/"products").rglob("bsip2_trace.json"):
        t = json.loads(p.read_text(encoding="utf-8"))
        bc = str(t.get("barcode") or (t.get("input_reference") or {}).get("barcode") or "")
        if bc == str(barcode):
            return t
    return None

def score_bsip1(doc):
    signals = extract_signals(doc)
    cat_result = classify_category(doc)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(doc, l3)
    eval_result = assign_evaluation_scope(doc, cat_result["category"])
    score_result = score_product(doc, signals, cat_result, nova_result, eval_result)
    return {"category": cat_result["category"], "score": score_result.get("final_score_estimate"), "grade": score_result.get("grade_estimate")}

LIVE = {
    "milk": ROOT/"02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products",
    "cereals": ROOT/"03_operations/bsip1/run_cereals_008/output",
    "yogurt": ROOT/"03_operations/bsip1/run_yogurt_006/output",
    "bread": ROOT/"02_products/bread_retail_001/bsip1",
    "granola_snackbars": ROOT/"02_products/snack_bars/canonical_bsip1/run_001",
    "snack_bars": ROOT/"02_products/snack_bars/canonical_bsip1/run_001",
    "cheese_spreads": ROOT/"03_operations/bsip1/run_cheese_003/output",
    "hard_cheeses": ROOT/"03_operations/bsip1/run_hard_cheeses_001/output",
    "brined": ROOT/"03_operations/bsip1/run_brined_cheeses_002/output",
    "hummus": ROOT/"03_operations/bsip1/run_hummus_001/output",
    "salty_snacks": ROOT/"02_products/salty_snacks/bsip1_outputs",
    "juices": ROOT/"03_operations/bsip1/run_juices_001/output",
}
bleed_hits, corpus_counts, seen = [], {}, set()
for cat, d in LIVE.items():
    key = str(d)
    if key in seen: continue
    seen.add(key)
    files = [p for p in d.glob("*.json") if "audit" not in p.name and "bsip2" not in p.name]
    corpus_counts[cat] = len(files)
    for fp in files:
        doc = json.loads(fp.read_text(encoding="utf-8"))
        name = doc.get("canonical_name_he") or doc.get("product_name_he") or ""
        if not name: continue
        anc = _check_anchors(name)
        if anc and anc[0] == "biscuit":
            bleed_hits.append({"corpus":cat,"barcode":str(doc.get("barcode","")),"name":name,"term":anc[3]})

maadanim_hits = []
for fp in (ROOT/"03_operations/bsip1/run_maadanim_001/output").glob("bsip1_*.json"):
    doc = json.loads(fp.read_text(encoding="utf-8"))
    name = doc.get("canonical_name_he") or ""
    anc = _check_anchors(name)
    if anc and anc[0] == "biscuit":
        maadanim_hits.append({"barcode":str(doc.get("barcode")), "name":name, "term":anc[3]})

live_diffs = []
for cat, trace_dir, bsip1_dir in [
    ("milk", ROOT/"02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products", ROOT/"02_products/milk_and_alternatives/intelligence_bsip2/run_milk_005_recal_p0/products_recal_on"),
    ("cereals", ROOT/"02_products/breakfast_cereals/bsip2_outputs/run_cereals_008_reconstruction/products", ROOT/"03_operations/bsip1/run_cereals_008/output"),
]:
    traces = list(trace_dir.rglob("bsip2_trace.json"))
    if not traces: continue
    t0 = json.loads(traces[0].read_text(encoding="utf-8"))
    bc = str(t0.get("barcode") or (t0.get("input_reference") or {}).get("barcode"))
    bsip1_path = bsip1_dir / f"bsip1_{bc}.json"
    if bsip1_path.exists():
        doc = json.loads(bsip1_path.read_text(encoding="utf-8"))
        new = score_bsip1(doc)
        old = {"category": t0.get("category"), "score": t0.get("final_score_estimate"), "grade": t0.get("grade_estimate")}
        if new != old:
            live_diffs.append({"corpus":cat,"barcode":bc,"old":old,"new":new})

run001 = ROOT/"02_products/cookies_coffee/bsip2_outputs/run_cookies_001"
run003 = ROOT/"02_products/cookies_coffee/bsip2_outputs/run_cookies_003"
movers, grade_mig = [], {}
before_routing, after_routing, before_grades, after_grades = {}, {}, {}, {}
for p in (run001/"products").rglob("bsip2_trace.json"):
    t1 = json.loads(p.read_text(encoding="utf-8"))
    bc = str(t1.get("barcode") or (t1.get("input_reference") or {}).get("barcode"))
    t3 = load_trace(run003, bc)
    if not t3: continue
    c1, c3 = t1.get("category"), t3.get("category")
    s1, s3 = t1.get("final_score_estimate"), t3.get("final_score_estimate")
    g1, g3 = t1.get("grade_estimate"), t3.get("grade_estimate")
    before_routing[c1] = before_routing.get(c1,0)+1
    after_routing[c3] = after_routing.get(c3,0)+1
    before_grades[g1] = before_grades.get(g1,0)+1
    after_grades[g3] = after_grades.get(g3,0)+1
    if c1 != c3 or s1 != s3 or g1 != g3:
        name = (t1.get("input_reference") or {}).get("product_name_he") or t1.get("canonical_name_he")
        movers.append([bc,c1,c3,s1,s3,g1,g3,name])
        if g1 != g3:
            grade_mig[f"{g1}->{g3}"] = grade_mig.get(f"{g1}->{g3}",0)+1

redlabel_ed = []
for p in (run003/"products").rglob("bsip2_trace.json"):
    t = json.loads(p.read_text(encoding="utf-8"))
    caps = t.get("caps_applied") or []
    red = sum(1 for c in caps if "RED_LABEL" in (c.get("rule") or ""))
    g = t.get("grade_estimate")
    if red >= 2 and g in ("E","D"):
        redlabel_ed.append({"barcode": str(t.get("barcode") or ""), "grade": g, "score": t.get("final_score_estimate"), "name": (t.get("input_reference") or {}).get("product_name_he")})

report = {
    "bleed_sim": {"hits": bleed_hits, "hit_count": len(bleed_hits), "corpus_counts": corpus_counts, "verdict": "PASS" if len(bleed_hits)==0 else "FAIL"},
    "maadanim_cookie_pollution": {"hit_count": len(maadanim_hits), "hits": maadanim_hits},
    "live_rescore_diff_sample": live_diffs,
    "migration_001_to_003": {"before_routing": before_routing, "after_routing": after_routing, "before_grades": before_grades, "after_grades": after_grades, "movers_count": len(movers), "grade_migrations": grade_mig, "movers": movers},
    "redlabel_2plus_ed_cohort": redlabel_ed,
}
OUT.joinpath("p75b_bleed_sim_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
OUT.joinpath("run_cookies_003/p75b_migration_report.json").write_text(json.dumps(report["migration_001_to_003"], ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"bleed_hits": len(bleed_hits), "live_diffs": len(live_diffs), "movers": len(movers), "grade_migrations": grade_mig, "after_routing": after_routing, "after_grades": after_grades, "redlabel_ed_count": len(redlabel_ed)}, ensure_ascii=False))
