"""
Debug milk score delta — compare baseline trace fields with new engine output.
"""
import os, json, pathlib, sys
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_DAIRY_SAT_FAT_INFER"] = "off"
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace

ROOT = pathlib.Path(r"C:\Bari")
MILK_BASELINE_DIR = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
MILK_BSIP1_DIR    = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"

TARGET = "bsip1_5411188112709"  # One of the failing ones

baseline = json.loads((MILK_BASELINE_DIR / TARGET / "bsip2_trace.json").read_text(encoding="utf-8"))
doc = json.loads((MILK_BSIP1_DIR / f"{TARGET}.json").read_text(encoding="utf-8"))

signals = extract_signals(doc)
cat = classify_category(doc)
l3 = signals["L3_inferred_classifications"]
nova = infer_nova(doc, l3)
ev = assign_evaluation_scope(doc, cat["category"])
sr = score_product(doc, signals, cat, nova, ev)

print(f"BASELINE score={baseline.get('final_score_estimate')} grade={baseline.get('grade_estimate')}")
print(f"BASELINE nova={baseline.get('nova_proxy')}")
print(f"BASELINE dim_scores={baseline.get('dimension_scores')}")
print()
print(f"NEW score={sr.get('final_score_estimate')} grade={sr.get('grade_estimate')}")
print(f"NEW nova={nova['nova_level']}")
print(f"NEW dim_scores={sr.get('dimension_scores')}")
print(f"NEW sat_fat_inferred={l3.get('sat_fat_inferred')}")
print()

# Compare dimension by dimension
b_dims = baseline.get("dimension_scores", {})
n_dims = sr.get("dimension_scores", {})
print("=== DIMENSION DELTA ===")
all_keys = set(list(b_dims.keys()) + list(n_dims.keys()))
for k in sorted(all_keys):
    b_v = b_dims.get(k)
    n_v = n_dims.get(k)
    if b_v != n_v:
        print(f"  {k}: baseline={b_v} new={n_v}")

print()
print("NEW binding_cap:", sr.get("binding_cap"))
print("NEW caps_applied:", [c.get("rule") for c in sr.get("caps_applied", [])])
print()

# Check nn in bsip1
nn = doc.get("normalized_nutrition_per_100g", {})
print("BSIP1 nutrition:", {k: v for k, v in nn.items() if v is not None})
