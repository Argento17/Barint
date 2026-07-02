import sys, json, pathlib, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "on"
SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))
from signal_extractor import extract_signals
from nova_proxy import infer_nova
from router_v2 import classify_category

bc = "7290110114886"
f = pathlib.Path(r"C:\Bari\02_products\juices\bsip1_outputs") / f"bsip1_juice_{bc}.json"
doc = json.loads(f.read_text(encoding="utf-8"))
sigs = extract_signals(doc)
L1 = sigs["L1_observed_signals"]
L3 = sigs["L3_inferred_classifications"]
cat = classify_category(doc)
nova = infer_nova(doc, L3)
print("Category:", cat["category"])
print("L1 ingredient_count:", L1.get("ingredient_count"))
print("L1 ingredient_list:", L1.get("ingredient_list"))
print("nova_level:", nova.get("nova_level"), "nova_confidence:", nova.get("nova_confidence"))
print("nova_evidence_for:", nova.get("nova_evidence_for"))
print("juice_sub_pool from doc:", repr(doc.get("juice_sub_pool")))

from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats
set_shelf_stats("sugars_g", 9.5, 2.82, "iqr", n=65)
ev = assign_evaluation_scope(doc, cat["category"])
sr = score_product(doc, sigs, cat, nova, ev)
print()
print("score_product final_score:", sr.get("final_score_estimate"))

from trace_writer import assemble_trace
from structural_classifier import classify_structural_class
tr = assemble_trace(doc, sigs, cat, nova, ev, sr)
tr["structural_class"] = classify_structural_class(tr)
print("trace nova_proxy:", tr.get("nova_proxy"))
print("trace nova_confidence:", tr.get("nova_confidence"))
print("trace L1 ingredient_count:", tr.get("L1_observed_signals", {}).get("ingredient_count"))
print("trace floors_applied:", tr.get("floors_applied"))
print("trace floors_considered:", tr.get("floors_considered"))
