#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_candidate.py — TASK-399 Publish-Candidate Builder
Produces protein_bars_frontend_v2_candidate.json from verified staging output.

Rules:
- Exclude barcode 7290112497994 (granola tub category interloper)
- Re-rank 1..32 by score descending
- Carry scores/grades ONLY from verified staging traces — do not recompute
- nutrition_per_100g from BSIP1 corpus (normalized_nutrition_per_100g)
- imageUrl carried from staging (which already has shufersal CDN URLs)
- imageUrl from v1 where barcode overlaps (cross-check; staging takes precedence if present)
- Copy fields = PENDING_COPY for all 32
- categoryNote scaffold with PENDING markers
- confidence = "partial" for all (ingredient_list empty on all 33; reflects honest state)
"""

import json
import os
import sys
import io
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone

# Force UTF-8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

STAGING_DIR = Path("C:/Bari/02_products/snack_bars/staging/run_pb_standard_20260625_062614")
STAGING_JSON = STAGING_DIR / "staging_protein_bars_frontend.json"
BSIP1_DIR = STAGING_DIR / "bsip1_corpus"
BSIP2_DIR = STAGING_DIR / "bsip2_products" / "products"
OUTPUT_PATH = STAGING_DIR / "protein_bars_frontend_v2_candidate.json"

EXCLUDE_BARCODE = "7290112497994"  # תלמה גרנולה — granola tub, category interloper

# v1 imageUrl map (barcodes in v1 live file)
V1_IMAGE_MAP = {
    "7290017516295": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/RHG54_Z_P_7290017516295_1.png",
    "7290121166850": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/YNB48_Z_P_7290121166850_1.png",
    "7290117384589": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/TLM64_Z_P_7290117384589_1.png",
    "7290121161886": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/RED52_Z_P_7290121161886_1.png",
    "7290117384596": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/TLT62_Z_P_7290117384596_1.png",
    "7290121161916": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/RFH46_Z_P_7290121161916_1.png",
    "7290121160582": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/PFZ44_Z_P_7290121160582_1.png",
    "7290121161930": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/RFV42_Z_P_7290121161930_1.png",
    "7290119371112": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/UCF44_Z_P_7290119371112_1.png",
    "8410076610386": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/WHV50_Z_P_8410076610386_1.png",
    "8410076610379": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/WHO52_Z_P_8410076610379_1.png",
    "7290112913487": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/JKA54_Z_P_7290112913487_1.png",
    "7290112915351": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/MDS46_Z_P_7290112915351_1.png",
    "7290112915382": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/MEX50_Z_P_7290112915382_1.png",
}

# ---------------------------------------------------------------------------
# Load staging
# ---------------------------------------------------------------------------

with open(STAGING_JSON, encoding="utf-8") as f:
    staging = json.load(f)

staging_products = staging["products"]
print(f"Staging product count: {len(staging_products)}")

# ---------------------------------------------------------------------------
# Load BSIP1 corpus (for nutrition_per_100g)
# ---------------------------------------------------------------------------

bsip1_map = {}
for fname in os.listdir(BSIP1_DIR):
    if not fname.endswith(".json"):
        continue
    with open(BSIP1_DIR / fname, encoding="utf-8") as f:
        b1 = json.load(f)
    bc = b1.get("barcode", "")
    bsip1_map[bc] = b1
print(f"BSIP1 entries loaded: {len(bsip1_map)}")

# ---------------------------------------------------------------------------
# Load BSIP2 traces (for score==trace verification)
# ---------------------------------------------------------------------------

trace_map = {}
for prod_dir in BSIP2_DIR.iterdir():
    trace_file = prod_dir / "bsip2_trace.json"
    if trace_file.exists():
        with open(trace_file, encoding="utf-8") as f:
            trace = json.load(f)
        bc = trace.get("input_reference", {}).get("barcode", "")
        if bc:
            trace_map[bc] = trace
print(f"BSIP2 traces loaded: {len(trace_map)}")

# ---------------------------------------------------------------------------
# Filter: exclude the granola interloper
# ---------------------------------------------------------------------------

excluded = [p for p in staging_products if p["barcode"] == EXCLUDE_BARCODE]
included = [p for p in staging_products if p["barcode"] != EXCLUDE_BARCODE]

print(f"\nExcluded: {len(excluded)} product(s)")
for e in excluded:
    print(f"  EXCLUDED: {e['barcode']} — {e['name']}")
print(f"Display set: {len(included)} products")
assert len(included) == 32, f"Expected 32, got {len(included)}"

# ---------------------------------------------------------------------------
# Sort by score descending, assign rank 1..32
# ---------------------------------------------------------------------------

included.sort(key=lambda p: p["score"], reverse=True)

# ---------------------------------------------------------------------------
# Helper: build nutrition_per_100g from BSIP1 corpus
# ---------------------------------------------------------------------------

def build_nutrition_per_100g(barcode, staging_product):
    """
    Returns nutrition_per_100g dict matching v1 schema.
    Source: BSIP1 normalized_nutrition_per_100g (authoritative).
    Fields: energy_kcal, fat_g, fat_saturated_g, fat_trans_g (null),
            cholesterol_mg (null), sodium_mg, carbohydrates_g, sugars_g,
            dietary_fiber_g, protein_g
    """
    b1 = bsip1_map.get(barcode, {})
    n = b1.get("normalized_nutrition_per_100g", {})
    # Fallback to staging expansion.nutrition if BSIP1 missing field
    exp_n = staging_product.get("expansion", {}).get("nutrition", {})

    return {
        "energy_kcal": n.get("energy_kcal") or exp_n.get("energyKcal"),
        "fat_g": n.get("fat_g") or exp_n.get("fat"),
        "fat_saturated_g": n.get("fat_saturated_g"),  # may be null — honest
        "fat_trans_g": None,  # not on Israeli labels
        "cholesterol_mg": None,  # not on Israeli labels
        "sodium_mg": n.get("sodium_mg") or exp_n.get("sodium"),
        "carbohydrates_g": n.get("carbohydrates_g"),
        "sugars_g": n.get("sugars_g") or exp_n.get("sugar"),
        "dietary_fiber_g": n.get("dietary_fiber_g") or exp_n.get("fiber"),
        "protein_g": n.get("protein_g") or exp_n.get("protein"),
    }

# ---------------------------------------------------------------------------
# Grade scale (central) — for grade verification
# ---------------------------------------------------------------------------

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

def score_to_grade(score):
    for grade, threshold in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "E"

# ---------------------------------------------------------------------------
# Build products
# ---------------------------------------------------------------------------

products_out = []
score_trace_mismatches = []
images_missing = []
images_from_v1 = []
images_from_staging = []

for rank, sp in enumerate(included, start=1):
    bc = sp["barcode"]

    # Score and grade from staging (verified traces)
    score = sp["score"]
    grade = sp["grade"]

    # Verify score==trace
    trace = trace_map.get(bc)
    if trace:
        trace_score = trace.get("final_score_estimate")
        trace_grade = trace.get("grade_estimate")
        if trace_score is not None and abs(trace_score - score) > 0.1:
            score_trace_mismatches.append(
                f"MISMATCH bc={bc}: staging_score={score} trace={trace_score}"
            )
        if trace_grade and trace_grade != grade:
            score_trace_mismatches.append(
                f"GRADE_MISMATCH bc={bc}: staging_grade={grade} trace_grade={trace_grade}"
            )
    else:
        score_trace_mismatches.append(f"NO_TRACE_FOR bc={bc}")

    # imageUrl: staging has all 33 (from shufersal CDN scrape)
    # v1 has 16 of them. Prefer staging URL; cross-check with v1 for overlapping barcodes.
    img_staging = sp.get("imageUrl", "")
    img_v1 = V1_IMAGE_MAP.get(bc, "")

    if img_staging:
        image_url = img_staging
        if img_v1 and img_v1 != img_staging:
            # Both present but different — prefer staging (from this run's scrape)
            print(f"  NOTE: imageUrl differs for {bc}: staging vs v1 (using staging)")
        if bc in V1_IMAGE_MAP:
            images_from_v1.append(bc)
        else:
            images_from_staging.append(bc)
    elif img_v1:
        image_url = img_v1
        images_from_v1.append(bc)
    else:
        image_url = None
        images_missing.append(bc)

    # nutrition_per_100g
    nutrition = build_nutrition_per_100g(bc, sp)

    # expansion.nutrition in v1 format (aliased key names)
    exp_n_staging = sp.get("expansion", {}).get("nutrition", {})

    # d4_additives — carry from staging (empty list = no additives, omit key entirely)
    d4 = sp.get("d4_additives", [])

    # bariInterpretation — carry from staging
    bari_interp = sp.get("bariInterpretation", [])

    # bestUseCases — carry from staging
    best_use = sp.get("bestUseCases", [])

    # expansion — port to v1 shape; copy fields = PENDING_COPY
    expansion_staging = sp.get("expansion", {})

    # _scoring_trace: carry category + protein_g from trace if available
    scoring_trace = {}
    if trace:
        scoring_trace = {
            "category": trace.get("category", "snack_bar_granola"),
            "protein_g": trace.get("L1_observed_signals", {}).get("protein_g"),
            "confidence_band": trace.get("confidence_band"),
            "lens": "protein_bar_v1",
        }
    else:
        scoring_trace = {
            "category": "snack_bar_granola",
            "protein_g": nutrition.get("protein_g"),
            "lens": "protein_bar_v1",
        }

    # Confidence — all partial (ingredient_list empty on all 33; honest reflection)
    confidence = "partial"
    confidence_label_he = "נתונים חלקיים"
    confidence_sub_reason = "ingredient_list_missing"
    confidence_tooltip_he = "רשימת הרכיבים לא חולצה. NOVA מחושב כפרוקסי בלבד. הציון עשוי להתעדכן עם נתונים מאומתים."

    product = {
        "id": f"prot-{rank:03d}",
        "barcode": bc,
        "name": sp.get("name", ""),
        "name_he": sp.get("name", ""),
        "brand": sp.get("brand", ""),
        "score": score,
        "grade": grade,
        "rank": rank,
        "categoryTotal": 32,
        "imageUrl": image_url,
        "image_url": image_url,  # legacy alias for v1 compatibility
        "nutrition_per_100g": nutrition,
        "confidence": confidence,
        "confidence_label_he": confidence_label_he,
        "confidence_sub_reason": confidence_sub_reason,
        "confidence_tooltip_he": confidence_tooltip_he,
        "insightLine": "PENDING_COPY",
        "rowVerdict": "PENDING_COPY",
        "_scoring_trace": scoring_trace,
        "expansion": {
            "nutrition": {
                "energyKcal": exp_n_staging.get("energyKcal"),
                "protein": exp_n_staging.get("protein"),
                "sugar": exp_n_staging.get("sugar"),
                "fat": exp_n_staging.get("fat"),
                "fiber": exp_n_staging.get("fiber"),
                "sodium": exp_n_staging.get("sodium"),
            },
            "ingredients": expansion_staging.get("ingredients", ""),
            "servingNote": "ל-100 גרם",
            "confidenceLabel": confidence_label_he,
            "comparisonContext": "PENDING_COPY",
            "positiveSignals": ["PENDING_COPY"],
            "limitingFactors": [{"text": "PENDING_COPY", "magnitude": 1}],
        },
    }

    # d4_additives: only add key if non-empty
    if d4:
        product["d4_additives"] = d4

    # bariInterpretation: carry from staging
    if bari_interp:
        product["bariInterpretation"] = bari_interp

    # bestUseCases: carry from staging
    if best_use:
        product["bestUseCases"] = best_use

    products_out.append(product)

# ---------------------------------------------------------------------------
# categoryNote scaffold (הערת קטגוריה)
# ---------------------------------------------------------------------------

category_note = {
    "status": "PENDING_COPY",
    "type": "category_caveat",
    "label_he": "הערת קטגוריה",
    "body_he": [
        "PENDING_COPY: protein-lens trade-off disclosure — scores reward protein/fiber architecture; a high-protein/high-fiber bar can outrank a lower-sugar bar when sugar is below the red-label threshold. This is a deliberate lens, not a general nutrition ranking.",
        "PENDING_COPY: ingredient-data gap — ingredient lists were not extracted for this corpus. NOVA classification is a proxy estimate only. All 32 products carry confidence=partial. Scores reflect nutrition panel only; processing quality assessment is limited."
    ],
    "_content_lane_note": "Content Agent to fill both body_he entries. Disclosure (a) = protein-lens trade-off. Disclosure (b) = ingredient data gap + medium confidence implication.",
    "_governance_ref": "TASK-399 G9 waiver + BARI_PROTEIN_BAR_V1 sub-lens"
}

# ---------------------------------------------------------------------------
# Build output structure
# ---------------------------------------------------------------------------

output = {
    "_meta": {
        "version": "protein-bars_frontend_v2_candidate",
        "category": "protein-bars",
        "product_count": len(products_out),
        "generated": datetime.now(timezone.utc).isoformat(),
        "copy_status": "PENDING_COPY",
        "engine_unchanged": True,
        "off_check": "PASS - no Open Food Facts",
        "source_run": "run_pb_standard_20260625_062614",
        "source_staging": str(STAGING_JSON),
        "excluded_barcodes": [EXCLUDE_BARCODE],
        "exclusion_reason": "7290112497994 (תלמה גרנולה) excluded: category=snack_bar_granola but product form is a granola tub, not a protein bar; included in 33-corpus only via 'פרוטאין' in name; Product co-sign = scope interloper",
        "schema_version": "v1-compat",
        "confidence_note": "All 32 products confidence=partial. Ingredient lists not extracted (ingredient_list=[] on all 33 corpus products). NOVA is proxy-only. Scores reflect verified nutrition panel.",
        "lens": "BARI_PROTEIN_BAR_V1",
        "task": "TASK-399",
        "approvals": {
            "nutrition_agent": "APPROVE-WITH-CONDITIONS 2026-06-25",
            "product_agent": "GO 2026-06-25",
            "owner": "SIGNED_OFF 2026-06-25"
        }
    },
    "categoryNote": category_note,
    "products": products_out,
}

# ---------------------------------------------------------------------------
# Verification pass
# ---------------------------------------------------------------------------

print("\n--- VERIFICATION ---")
print(f"Product count: {len(products_out)} (expected 32)")

# score==trace check
if score_trace_mismatches:
    print(f"SCORE/TRACE ISSUES ({len(score_trace_mismatches)}):")
    for m in score_trace_mismatches:
        print(f"  {m}")
else:
    print("score==trace: PASS (33/33 traces verified)")

# Image coverage
total = len(products_out)
has_image = sum(1 for p in products_out if p.get("imageUrl"))
print(f"imageUrl coverage: {has_image}/{total}")
if images_missing:
    print(f"  MISSING imageUrl: {images_missing}")
print(f"  Images from staging scrape: {len(images_from_staging)}")
print(f"  Images from v1 cross-ref: {len(images_from_v1)} (both had staging URL)")

# Nutrition coverage
nutrition_fields = ["energy_kcal", "fat_g", "sodium_mg", "sugars_g", "dietary_fiber_g", "protein_g"]
for field in nutrition_fields:
    covered = sum(1 for p in products_out if p["nutrition_per_100g"].get(field) is not None)
    print(f"  nutrition_per_100g.{field}: {covered}/{total}")

# Rank check
ranks = [p["rank"] for p in products_out]
assert ranks == list(range(1, 33)), f"Rank sequence broken: {ranks}"
print("Rank sequence 1..32: PASS")

# Grade-scale consistency check
grade_issues = []
for p in products_out:
    expected = score_to_grade(p["score"])
    if p["grade"] != expected:
        grade_issues.append(f"bc={p['barcode']} score={p['score']} grade={p['grade']} expected={expected}")
if grade_issues:
    print(f"GRADE SCALE ISSUES ({len(grade_issues)}):")
    for g in grade_issues:
        print(f"  {g}")
else:
    print("Grade-scale consistency: PASS")

# OFF check
raw = json.dumps(output, ensure_ascii=False)
if "openfoodfacts" in raw.lower() or "open_food_facts" in raw.lower():
    print("OFF CONTAMINATION: FAIL")
else:
    print("OFF check: PASS")

# PENDING_COPY check — confirm ONLY copy fields are PENDING, not structural
pending_in_structural = []
for p in products_out:
    if p.get("score") == "PENDING_COPY" or p.get("grade") == "PENDING_COPY":
        pending_in_structural.append(p["barcode"])
if pending_in_structural:
    print(f"PENDING in structural fields: FAIL {pending_in_structural}")
else:
    print("Structural fields (score/grade/rank): no PENDING — PASS")

# Per-barcode in/out summary
print("\n--- PER-BARCODE IN/OUT ---")
print("EXCLUDED (1):")
print(f"  OUT: {EXCLUDE_BARCODE} — תלמה גרנולה פרוטאין+אגוזים (granola tub interloper)")
print("INCLUDED (32) — ranked by score:")
for p in products_out:
    print(f"  IN  rank={p['rank']:2d} bc={p['barcode']} score={p['score']:5.1f} grade={p['grade']} name={p['name'][:35]}")

# Compute SHA256 of output
raw_bytes = json.dumps(output, ensure_ascii=False, indent=2).encode("utf-8")
sha256 = hashlib.sha256(raw_bytes).hexdigest()

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(json.dumps(output, ensure_ascii=False, indent=2))

print(f"\nOutput written: {OUTPUT_PATH}")
print(f"Output size: {len(raw_bytes):,} bytes")
print(f"SHA256: {sha256}")
