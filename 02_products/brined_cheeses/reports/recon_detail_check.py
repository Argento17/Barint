"""
Detail check for yogurt and cheese-spreads moved products under BARI_REDLABEL_V1=on.
Also confirm non-dairy cereals movement reason.
"""
import os, sys, json, pathlib, importlib

ROOT = pathlib.Path(r"C:\Bari")
SRC  = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
sys.path.insert(0, str(SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def _run_pipeline_with_flag(bsip1_doc, recal_p0, redlabel):
    os.environ["BARI_RECAL_P0"] = recal_p0
    os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "off"
    os.environ["BARI_REDLABEL_V1"] = redlabel
    os.environ["BARI_SODIUM_CEREAL"] = "off"
    os.environ["BARI_TASK144_FIXES"] = "off"
    os.environ["BARI_TASK250_CONF"] = "off"
    os.environ["BARI_GLASSBOX_D5D6"] = "off"
    os.environ["BARI_GLASSBOX_W15"] = "off"
    os.environ["BARI_GLASSBOX_W2"] = "off"
    for mod_name in ["constants", "score_engine", "signal_extractor", "router_v2",
                     "nova_proxy", "evaluation_scope", "trace_writer", "structural_classifier"]:
        if mod_name in sys.modules:
            importlib.reload(sys.modules[mod_name])
        else:
            importlib.import_module(mod_name)
    from signal_extractor  import extract_signals
    from router_v2         import classify_category
    from nova_proxy        import infer_nova
    from evaluation_scope  import assign_evaluation_scope
    from score_engine      import score_product
    from trace_writer      import assemble_trace
    from structural_classifier import classify_structural_class
    signals = extract_signals(bsip1_doc)
    cat_result = classify_category(bsip1_doc)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(bsip1_doc, l3)
    eval_result = assign_evaluation_scope(bsip1_doc, cat_result["category"])
    score_result = score_product(bsip1_doc, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(bsip1_doc, signals, cat_result, nova_result, eval_result, score_result)
    sodium = (bsip1_doc.get("normalized_nutrition_per_100g") or {}).get("sodium_mg") or 0
    return {
        "barcode": bsip1_doc.get("barcode", "?"),
        "category": trace.get("category"),
        "nova": trace.get("nova_proxy"),
        "sodium_mg": sodium,
        "score": trace.get("final_score_estimate"),
        "grade": trace.get("grade_estimate"),
        "binding_cap": trace.get("binding_cap"),
        "caps_applied": [c.get("rule") for c in (trace.get("caps_applied") or [])],
        "pens_applied": [c.get("rule") for c in (trace.get("penalties_applied") or [])],
    }

print("=== YOGURT moved products ===")
YOGURT_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_yogurt_006" / "output"
yogurt_records = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(YOGURT_BSIP1.glob("bsip1_*.json"))]
print(f"Total yogurt records: {len(yogurt_records)}")

moved_yogurt = []
identical_yogurt = 0
for doc in yogurt_records:
    r_off = _run_pipeline_with_flag(doc, "on", "off")
    r_on  = _run_pipeline_with_flag(doc, "on", "on")
    if r_off["score"] != r_on["score"] or r_off["grade"] != r_on["grade"]:
        moved_yogurt.append({
            "barcode": r_off["barcode"], "category": r_off["category"], "nova": r_off["nova"],
            "sodium_mg": r_off["sodium_mg"],
            "score_off": r_off["score"], "grade_off": r_off["grade"],
            "score_on": r_on["score"], "grade_on": r_on["grade"],
            "delta": round((r_on["score"] or 0) - (r_off["score"] or 0), 2),
            "caps_on": r_on["caps_applied"],
            "pens_on": r_on["pens_applied"],
        })
    else:
        identical_yogurt += 1

print(f"Yogurt: identical={identical_yogurt} moved={len(moved_yogurt)}")
for m in moved_yogurt:
    print(f"  bc={m['barcode']} cat={m['category']} nova={m['nova']} sodium={m['sodium_mg']} off={m['score_off']}/{m['grade_off']} on={m['score_on']}/{m['grade_on']} delta={m['delta']:+.2f} caps={m['caps_on']}")

print()
print("=== CHEESE-SPREADS moved products ===")
CHEESE_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_cheese_003" / "output"
cheese_records = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CHEESE_BSIP1.glob("bsip1_*.json"))]
print(f"Total cheese records: {len(cheese_records)}")

moved_cheese = []
identical_cheese = 0
for doc in cheese_records:
    r_off = _run_pipeline_with_flag(doc, "on", "off")
    r_on  = _run_pipeline_with_flag(doc, "on", "on")
    if r_off["score"] != r_on["score"] or r_off["grade"] != r_on["grade"]:
        moved_cheese.append({
            "barcode": r_off["barcode"], "category": r_off["category"], "nova": r_off["nova"],
            "sodium_mg": r_off["sodium_mg"],
            "score_off": r_off["score"], "grade_off": r_off["grade"],
            "score_on": r_on["score"], "grade_on": r_on["grade"],
            "delta": round((r_on["score"] or 0) - (r_off["score"] or 0), 2),
            "caps_on": r_on["caps_applied"],
        })
    else:
        identical_cheese += 1

print(f"Cheese: identical={identical_cheese} moved={len(moved_cheese)}")
for m in moved_cheese[:15]:
    print(f"  bc={m['barcode']} cat={m['category']} nova={m['nova']} sodium={m['sodium_mg']} off={m['score_off']}/{m['grade_off']} on={m['score_on']}/{m['grade_on']} delta={m['delta']:+.2f} caps={m['caps_on']}")

if len(moved_cheese) > 15:
    print(f"  ... {len(moved_cheese)-15} more")

print()
print("=== CEREALS sample (non-dairy) moved products ===")
CEREALS_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_cereals_multiretailer_001" / "output"
cereal_records = []
for p in sorted(CEREALS_BSIP1.glob("bsip1_*.json"))[:20]:
    cereal_records.append(json.loads(p.read_text(encoding="utf-8")))
print(f"Total cereal records sample: {len(cereal_records)}")

moved_cereals = []
identical_cereals = 0
for doc in cereal_records:
    r_off = _run_pipeline_with_flag(doc, "on", "off")
    r_on  = _run_pipeline_with_flag(doc, "on", "on")
    if r_off["score"] != r_on["score"] or r_off["grade"] != r_on["grade"]:
        moved_cereals.append({
            "barcode": r_off["barcode"], "category": r_off["category"], "nova": r_off["nova"],
            "sodium_mg": r_off["sodium_mg"],
            "score_off": r_off["score"], "grade_off": r_off["grade"],
            "score_on": r_on["score"], "grade_on": r_on["grade"],
            "delta": round((r_on["score"] or 0) - (r_off["score"] or 0), 2),
            "caps_on": r_on["caps_applied"],
        })
    else:
        identical_cereals += 1

print(f"Cereals: identical={identical_cereals} moved={len(moved_cereals)}")
for m in moved_cereals:
    print(f"  bc={m['barcode']} cat={m['category']} nova={m['nova']} sodium={m['sodium_mg']} off={m['score_off']}/{m['grade_off']} on={m['score_on']}/{m['grade_on']} delta={m['delta']:+.2f} caps={m['caps_on']}")

print()
print("=== BRINED pinned-at-72 analysis ===")
BRINED_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_brined_cheeses_001" / "output"
BRINED_CORPUS_FILTER = ROOT / "02_products" / "brined_cheeses" / "factory_run_001" / "corpus_filter.json"
corpus_filter = json.loads(BRINED_CORPUS_FILTER.read_text(encoding="utf-8"))
in_scored_barcodes = {str(p["barcode"]) for p in corpus_filter["products"] if p["decision"] == "IN_SCORED"}
brined_records = []
for p in sorted(BRINED_BSIP1.glob("bsip1_brinedcheese_*.json")):
    doc = json.loads(p.read_text(encoding="utf-8"))
    if str(doc.get("barcode","")) in in_scored_barcodes:
        brined_records.append(doc)
print(f"Brined records: {len(brined_records)}")

# Load run_brined_002 pinned-at-72 list
RUN002_DIR = ROOT / "02_products" / "brined_cheeses" / "bsip2_outputs" / "run_brined_002" / "products"
pinned_at_72 = set()
for tf in sorted(RUN002_DIR.glob("bsip1_brinedcheese_*/bsip2_trace.json")):
    tr = json.loads(tf.read_text(encoding="utf-8"))
    bc = str((tr.get("input_reference") or {}).get("barcode") or "")
    if tr.get("binding_cap") == 72:
        pinned_at_72.add(bc)
print(f"Pinned at 72 in run_brined_002: {len(pinned_at_72)}")

broken = []
same = []
for doc in brined_records:
    bc = str(doc.get("barcode", ""))
    if bc not in pinned_at_72:
        continue
    r_off = _run_pipeline_with_flag(doc, "on", "off")
    r_on  = _run_pipeline_with_flag(doc, "on", "on")
    entry = {
        "barcode": bc, "category": r_off["category"], "nova": r_off["nova"],
        "sodium_mg": r_off["sodium_mg"],
        "score_off": r_off["score"], "grade_off": r_off["grade"],
        "score_on": r_on["score"], "grade_on": r_on["grade"],
        "delta": round((r_on["score"] or 0) - (r_off["score"] or 0), 2),
        "caps_on": r_on["caps_applied"],
    }
    if r_off["score"] != r_on["score"]:
        broken.append(entry)
    else:
        same.append(entry)

print(f"72-pin broken: {len(broken)} / {len(broken)+len(same)}")
print(f"72-pin same:   {len(same)} / {len(broken)+len(same)}")
print()
print("BROKEN (sample 10):")
for m in sorted(broken, key=lambda x: x["barcode"])[:10]:
    print(f"  bc={m['barcode']} cat={m['category']} nova={m['nova']} sodium={m['sodium_mg']} off={m['score_off']}/{m['grade_off']} on={m['score_on']}/{m['grade_on']} delta={m['delta']:+.2f} caps={m['caps_on']}")
print()
print("SAME (not broken):")
for m in sorted(same, key=lambda x: x["barcode"])[:15]:
    print(f"  bc={m['barcode']} cat={m['category']} nova={m['nova']} sodium={m['sodium_mg']} off={m['score_off']}/{m['grade_off']}")

print()
print("=== NOVA x sodium differentiation (broken products) ===")
from collections import defaultdict
groups = defaultdict(list)
for m in broken:
    fat_val = None
    for doc in brined_records:
        if str(doc.get("barcode")) == m["barcode"]:
            fat_val = (doc.get("normalized_nutrition_per_100g") or {}).get("fat_g")
            break
    fat_t = "low<10" if (fat_val or 0) < 10 else "mid10-20" if (fat_val or 0) < 20 else "high>=20"
    groups[(m["nova"], fat_t)].append(m)

for key in sorted(groups.keys()):
    grp = groups[key]
    off_s = sorted(set(x["score_off"] for x in grp))
    on_s  = sorted(set(x["score_on"]  for x in grp))
    print(f"  NOVA={key[0]} fat={key[1]} n={len(grp)}: off={off_s} -> on={on_s}")
