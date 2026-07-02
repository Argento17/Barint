#!/usr/bin/env python3
"""
Single-product scorer called via subprocess with a clean Python process.
Args: <engine_root> <bsip1_file> <flags_json>
Prints JSON result to stdout.
"""
import json
import os
import sys
import pathlib
import io

# Force UTF-8 stdout to handle Hebrew names
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

engine_root = pathlib.Path(sys.argv[1])
bsip1_file = pathlib.Path(sys.argv[2])
flags = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
shelf_rel = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}

# Set env flags
for k, v in flags.items():
    os.environ[k] = v

# Add engine to path
src = engine_root / "03_operations" / "bsip2" / "proto_v0" / "src"
sys.path.insert(0, str(src))

from signal_extractor import extract_signals
from router_v2 import classify_category, ROUTER_VERSION
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats

# Setup shelf stats
if shelf_rel:
    api = shelf_rel.get("api")
    nutrient = shelf_rel.get("nutrient")
    median = shelf_rel.get("median")
    scale = shelf_rel.get("scale")
    scale_type = shelf_rel.get("scale_type", "iqr")
    n = shelf_rel.get("n", 30)
    if api == "sodium_ev056":
        from score_engine import set_shelf_sodium_stats
        set_shelf_sodium_stats(median, scale)
    elif nutrient and median is not None and scale is not None:
        set_shelf_stats(nutrient, median, scale, scale_type, n)

with open(bsip1_file, encoding="utf-8") as f:
    product = json.load(f)

signals = extract_signals(product)
cat_result = classify_category(product)
l3 = signals["L3_inferred_classifications"]
nova_result = infer_nova(product, l3)
eval_result = assign_evaluation_scope(product, cat_result["category"])
score_result = score_product(product, signals, cat_result, nova_result, eval_result)

# Use final_score_estimate (the actual display score from score_engine)
final_score = score_result.get("final_score_estimate")
final_grade = score_result.get("grade_estimate")

# Also collect override trace
req362 = score_result.get("req362_override_trace") or cat_result.get("req362_override_trace") or {}
cls_basis = cat_result.get("classification_basis", [])

output = {
    "barcode": str(product.get("barcode", "")),
    "name": product.get("canonical_name_he") or product.get("name_he") or "",
    "score": final_score,
    "grade": final_grade,
    "category": cat_result.get("category"),
    "category_subtype": cat_result.get("category_subtype"),
    "override_applied": req362.get("override_applied"),
    "override_reason": req362.get("reason"),
    "classification_basis": cls_basis[:5] if cls_basis else [],
    "router_version": ROUTER_VERSION,
}
print(json.dumps(output, ensure_ascii=False))
