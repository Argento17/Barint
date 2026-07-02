#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, io, sys, hashlib
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CANDIDATE = "C:/Bari/02_products/snack_bars/staging/run_pb_standard_20260625_062614/protein_bars_frontend_v2_candidate.json"

with open(CANDIDATE, encoding="utf-8") as f:
    cand = json.load(f)

prods = cand["products"]
print("=== CANDIDATE FINAL VERIFICATION ===")
print("Product count:", len(prods))
print("categoryNote present:", "categoryNote" in cand)
print("_meta.lens:", cand["_meta"].get("lens"))
print("_meta.excluded_barcodes:", cand["_meta"].get("excluded_barcodes"))
print()

# Field coverage vs v1 schema
v1_fields = [
    "id", "barcode", "name", "name_he", "brand", "score", "grade",
    "rank", "categoryTotal", "imageUrl", "image_url", "nutrition_per_100g",
    "confidence", "confidence_label_he", "confidence_sub_reason",
    "confidence_tooltip_he", "insightLine", "rowVerdict",
    "_scoring_trace", "expansion"
]
print("=== V1 SCHEMA FIELD COVERAGE ===")
for field in v1_fields:
    present = sum(1 for p in prods if field in p and p[field] is not None)
    note = ""
    if present < 32:
        note = " <-- PARTIAL"
    print("  {}: {}/32{}".format(field, present, note))

# Expansion sub-fields
exp_fields = ["nutrition", "ingredients", "servingNote", "confidenceLabel",
              "comparisonContext", "positiveSignals", "limitingFactors"]
print()
print("=== EXPANSION FIELD COVERAGE ===")
for field in exp_fields:
    present = sum(1 for p in prods if field in p.get("expansion", {}))
    print("  expansion.{}: {}/32".format(field, present))

# nutrition_per_100g sub-fields
nut_fields = ["energy_kcal", "fat_g", "fat_saturated_g", "fat_trans_g",
              "cholesterol_mg", "sodium_mg", "carbohydrates_g", "sugars_g",
              "dietary_fiber_g", "protein_g"]
print()
print("=== NUTRITION_PER_100G FIELD COVERAGE ===")
for field in nut_fields:
    n = cand["products"]
    present = sum(1 for p in prods if p.get("nutrition_per_100g", {}).get(field) is not None)
    print("  {}: {}/32".format(field, present))

# Grade distribution
grade_dist = Counter(p["grade"] for p in prods)
print()
print("=== GRADE DISTRIBUTION ===")
for g in sorted(grade_dist.keys()):
    print("  {}: {}".format(g, grade_dist[g]))

# Score range
scores = [p["score"] for p in prods]
print()
print("=== SCORE RANGE ===")
print("  min: {}, max: {}".format(min(scores), max(scores)))
print("  rank1: bc={} score={} grade={}".format(prods[0]["barcode"], prods[0]["score"], prods[0]["grade"]))
print("  rank32: bc={} score={} grade={}".format(prods[31]["barcode"], prods[31]["score"], prods[31]["grade"]))

# Rank sequence
ranks = [p["rank"] for p in prods]
assert ranks == list(range(1, 33)), "RANK SEQUENCE BROKEN"
print()
print("Rank sequence 1..32: PASS")

# Confidence distribution
conf_dist = Counter(p["confidence"] for p in prods)
print()
print("=== CONFIDENCE ===")
for c in sorted(conf_dist.keys()):
    print("  {}: {}".format(c, conf_dist[c]))

# categoryTotal == 32 on all
ct_ok = all(p["categoryTotal"] == 32 for p in prods)
print()
print("categoryTotal==32 on all 32:", ct_ok)

# PENDING_COPY in structural fields check
structural_fields = ["score", "grade", "rank", "barcode", "name", "brand"]
struct_issues = []
for p in prods:
    for f in structural_fields:
        if p.get(f) == "PENDING_COPY":
            struct_issues.append("bc={} field={}".format(p["barcode"], f))
print("PENDING_COPY in structural fields:", "PASS" if not struct_issues else "FAIL: " + str(struct_issues))

# OFF check
raw_text = json.dumps(cand, ensure_ascii=False)
if "openfoodfacts" in raw_text.lower() or "open_food_facts" in raw_text.lower():
    print("OFF contamination: FAIL")
else:
    print("OFF contamination check: PASS")

# SHA256
with open(CANDIDATE, "rb") as f:
    raw_bytes = f.read()
sha256 = hashlib.sha256(raw_bytes).hexdigest()
print()
print("File size: {:,} bytes".format(len(raw_bytes)))
print("SHA256: {}".format(sha256))
print()
print("=== FIELDS NOT POPULATED vs V1 (schema gap analysis) ===")
# d4_additives is conditional (absent if empty — correct per spec)
# Fields in v1 not in candidate: check
v1_optional_absent_ok = ["d4_additives"]  # absent when no additives — correct
print("d4_additives: conditional (absent when no additives) — OK by spec")
print("nutrition_per_100g.fat_trans_g: null (not on Israeli labels) — OK by spec")
print("nutrition_per_100g.cholesterol_mg: null (not on Israeli labels) — OK by spec")
null_fiber = [p["barcode"] for p in prods if p.get("nutrition_per_100g", {}).get("dietary_fiber_g") is None]
if null_fiber:
    print("nutrition_per_100g.dietary_fiber_g NULL for:", null_fiber, "(absent in BSIP1 source — honest)")
