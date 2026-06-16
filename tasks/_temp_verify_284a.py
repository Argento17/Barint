"""
TASK-284A verification pass.
Deliverable 1: PHVO partial-vs-generic split
Deliverable 2: Milk seed-oil anomaly
Deliverable 3: Exact seed_pen 10->5 blast radius

Run from: C:\Bari
Command: python tasks/_temp_verify_284a.py
"""

import json
import os
import re
import glob
import hashlib
from pathlib import Path
from collections import defaultdict

ROOT = Path("C:/Bari")
PRODUCTS_DIR = ROOT / "02_products"

# Grade boundaries
def grade(score):
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"

# ============================================================
# STEP 1: Collect all bsip2_trace.json files
# ============================================================
print("=== Collecting bsip2_trace.json files ===")
trace_files = list(PRODUCTS_DIR.rglob("bsip2_trace.json"))
print(f"Total trace files found: {len(trace_files)}")

# ============================================================
# STEP 2: PHVO partial-vs-generic split
# Collect all has_phvo=True products, note ingredient text
# ============================================================
print("\n=== DELIVERABLE 1: PHVO partial-vs-generic split ===")

PARTIAL_MARKERS = ["מוקשה חלקית", "partially hydrogenated", "חלקית"]
# Generic markers (without חלקית qualifier)
GENERIC_MARKERS = [
    "שומן מוקשה", "שומנים מוקשים", "שומן צמחי מוקשה",
    "שמן צמחי מוקשה", "מרגרינה", "מוקשים"
]

phvo_products = []  # list of dicts

for tf in trace_files:
    try:
        with open(tf, encoding="utf-8") as f:
            trace = json.load(f)
    except Exception:
        continue

    # Category from path
    parts = tf.parts
    # Path: .../02_products/{category}/bsip2_outputs/run_xxx/products/{pid}/bsip2_trace.json
    try:
        cat_idx = parts.index("02_products") + 1
        category = parts[cat_idx]
    except (ValueError, IndexError):
        category = "unknown"

    l3 = trace.get("l3_signals", {})
    has_phvo = l3.get("has_phvo", False)
    if not has_phvo:
        continue

    barcode = trace.get("barcode") or trace.get("product_id", "")
    # Try multiple fields for ingredient text
    ing_text = (
        l3.get("ingredients_text") or
        l3.get("ingredient_text") or
        trace.get("ingredients_text") or
        trace.get("ingredient_text") or
        trace.get("l1_raw", {}).get("ingredients_text") or
        trace.get("l1_raw", {}).get("ingredient_text") or
        trace.get("l0_raw", {}).get("ingredients_text") or
        ""
    )
    # Also check product_text
    product_text = (
        trace.get("product_text") or
        trace.get("l0_raw", {}).get("product_text") or
        ""
    )

    phvo_products.append({
        "barcode": barcode,
        "category": category,
        "trace_path": str(tf),
        "ing_text": ing_text,
        "product_text": product_text,
        "has_phvo": True,
    })

print(f"has_phvo=True products: {len(phvo_products)}")

# Show the keys available in the first 3 traces to understand structure
print("\nKeys available in first phvo trace:")
for tf in trace_files[:20]:
    try:
        with open(tf, encoding="utf-8") as f:
            trace = json.load(f)
        l3 = trace.get("l3_signals", {})
        if l3.get("has_phvo", False):
            print(f"  Top-level keys: {list(trace.keys())}")
            print(f"  l3 keys (sample): {list(l3.keys())[:30]}")
            # Print any text fields
            for k, v in trace.items():
                if isinstance(v, str) and len(v) > 20:
                    print(f"  trace[{k!r}] = {v[:80]!r}")
            for k, v in l3.items():
                if isinstance(v, str) and len(v) > 10:
                    print(f"  l3[{k!r}] = {v[:80]!r}")
            break
    except Exception:
        continue

# ============================================================
# STEP 3: Find BSIP1 source data to recover ingredient text
# ============================================================
print("\n=== Looking for BSIP1 source files ===")
# Find bsip1 output files
bsip1_dirs = list(ROOT.rglob("*bsip1*"))
print(f"BSIP1 dirs/files found: {len(bsip1_dirs)}")
for p in bsip1_dirs[:10]:
    print(f"  {p}")

# Look for BSIP0 raw files
bsip0_files = list(PRODUCTS_DIR.rglob("*.json"))
print(f"\nTotal JSON files in 02_products: {len(bsip0_files)}")

# Get the barcodes of has_phvo products
phvo_barcodes = set(p["barcode"] for p in phvo_products if p["barcode"])
print(f"PHVO barcodes to search: {len(phvo_barcodes)}")
print(f"Sample barcodes: {list(phvo_barcodes)[:10]}")

# ============================================================
# STEP 4: Search BSIP0 raw files for phvo barcodes
# ============================================================
print("\n=== Searching BSIP0 raw files for PHVO product ingredient text ===")

# Find raw data files (not trace files)
raw_json_files = [f for f in bsip0_files if "bsip2_trace" not in f.name]
print(f"Non-trace JSON files: {len(raw_json_files)}")

# Build a barcode -> ingredient text map from raw files
barcode_to_ing = {}

def extract_from_product_obj(obj):
    """Try to extract ingredients text from a product object."""
    candidates = []
    for key in ["ingredients_text", "ingredient_text", "ingredients", "raw_ingredients",
                "ingredients_he", "מרכיבים", "תרכיבים", "product_text"]:
        val = obj.get(key)
        if isinstance(val, str) and len(val) > 5:
            candidates.append(val)
        elif isinstance(val, list):
            joined = " ".join(str(v) for v in val if v)
            if len(joined) > 5:
                candidates.append(joined)
    return " | ".join(candidates) if candidates else ""

def get_barcode_from_obj(obj):
    for key in ["barcode", "product_id", "ean", "gtin", "id", "itemCode"]:
        val = obj.get(key)
        if val:
            return str(val).strip()
    return ""

for rf in raw_json_files:
    if "bsip2_trace" in str(rf):
        continue
    try:
        with open(rf, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        continue

    # Could be a list of products or a single product or a dict with products key
    products_to_check = []
    if isinstance(data, list):
        products_to_check = data
    elif isinstance(data, dict):
        # Check if it has a products sub-key
        for key in ["products", "items", "data", "results"]:
            if isinstance(data.get(key), list):
                products_to_check = data[key]
                break
        if not products_to_check:
            products_to_check = [data]

    for obj in products_to_check:
        if not isinstance(obj, dict):
            continue
        bc = get_barcode_from_obj(obj)
        if bc and bc in phvo_barcodes:
            ing = extract_from_product_obj(obj)
            if ing and bc not in barcode_to_ing:
                barcode_to_ing[bc] = ing

print(f"Barcodes matched from raw files: {len(barcode_to_ing)}")

# ============================================================
# STEP 5: Also look in BSIP1 enrichment files
# ============================================================
print("\n=== Searching BSIP1 enrichment files ===")
bsip1_json_files = list(ROOT.rglob("bsip1_*.json"))
print(f"BSIP1 JSON files found: {len(bsip1_json_files)}")

for bf in bsip1_json_files:
    try:
        with open(bf, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        continue

    products_to_check = []
    if isinstance(data, list):
        products_to_check = data
    elif isinstance(data, dict):
        for key in ["products", "items", "data"]:
            if isinstance(data.get(key), list):
                products_to_check = data[key]
                break
        if not products_to_check:
            products_to_check = [data]

    for obj in products_to_check:
        if not isinstance(obj, dict):
            continue
        bc = get_barcode_from_obj(obj)
        if bc and bc in phvo_barcodes and bc not in barcode_to_ing:
            ing = extract_from_product_obj(obj)
            if ing:
                barcode_to_ing[bc] = ing

print(f"Barcodes matched after BSIP1 search: {len(barcode_to_ing)}")

# ============================================================
# STEP 6: Classify PHVO products
# ============================================================
print("\n=== PHVO Partial vs Generic Classification ===")

PARTIAL_TERMS = ["מוקשה חלקית", "partially hydrogenated", "partially-hydrogenated"]
# Generic = muksha WITHOUT partial qualifier
GENERIC_TERMS = [
    "שומן מוקשה", "שומנים מוקשים", "שומן צמחי מוקשה",
    "שמן צמחי מוקשה", "מוקשה", "מרגרינה", "מוקשים"
]

bucket_partial = []
bucket_generic = []
bucket_indeterminate = []
bucket_empty_text = []

per_category_partial = defaultdict(list)
per_category_generic = defaultdict(list)
per_category_indet = defaultdict(list)
per_category_empty = defaultdict(list)

for prod in phvo_products:
    bc = prod["barcode"]
    category = prod["category"]

    # Combine: trace text + recovered text
    combined_text = (prod["ing_text"] + " " + prod["product_text"]).strip()
    if bc in barcode_to_ing:
        combined_text = (combined_text + " " + barcode_to_ing[bc]).strip()

    if not combined_text:
        bucket_empty_text.append(bc)
        per_category_empty[category].append(bc)
        continue

    combined_lower = combined_text.lower()
    has_partial = any(term in combined_text for term in PARTIAL_TERMS)
    has_generic_muksha = any(term in combined_text for term in GENERIC_TERMS)

    if has_partial:
        bucket_partial.append({"barcode": bc, "category": category, "text_snippet": combined_text[:200]})
        per_category_partial[category].append(bc)
    elif has_generic_muksha:
        # Check if it has 'מוקשה' without חלקית
        if "חלקית" not in combined_text:
            bucket_generic.append({"barcode": bc, "category": category, "text_snippet": combined_text[:200]})
            per_category_generic[category].append(bc)
        else:
            bucket_partial.append({"barcode": bc, "category": category, "text_snippet": combined_text[:200]})
            per_category_partial[category].append(bc)
    else:
        bucket_indeterminate.append({"barcode": bc, "category": category, "text_snippet": combined_text[:200]})
        per_category_indet[category].append(bc)

print(f"PARTIAL (has_phvo_partial): {len(bucket_partial)}")
print(f"GENERIC (has_phvo_generic): {len(bucket_generic)}")
print(f"INDETERMINATE (has text, no marker): {len(bucket_indeterminate)}")
print(f"EMPTY TEXT (no ingredient text found): {len(bucket_empty_text)}")
print(f"TOTAL: {len(phvo_products)}")

print("\nPER-CATEGORY breakdown:")
all_cats = set(list(per_category_partial.keys()) + list(per_category_generic.keys()) +
               list(per_category_indet.keys()) + list(per_category_empty.keys()))
for cat in sorted(all_cats):
    print(f"  {cat}: partial={len(per_category_partial[cat])} generic={len(per_category_generic[cat])} indet={len(per_category_indet[cat])} empty={len(per_category_empty[cat])}")

print("\nPARTIAL barcodes:")
for p in bucket_partial:
    print(f"  {p['barcode']} ({p['category']}): {p['text_snippet'][:100]}")

print("\nGENERIC barcodes:")
for p in bucket_generic:
    print(f"  {p['barcode']} ({p['category']}): {p['text_snippet'][:100]}")

print("\nINDETERMINATE (text present but no PHVO term found):")
for p in bucket_indeterminate:
    print(f"  {p['barcode']} ({p['category']}): {p['text_snippet'][:100]}")

# ============================================================
# STEP 7: Milk seed-oil anomaly
# ============================================================
print("\n\n=== DELIVERABLE 2: Milk seed-oil anomaly ===")

SEED_OIL_MARKERS = [
    "שמן חמניות", "שמן קנולה", "שמן תירס", "שמן סויה",
    "שמן צמחי", "שמנים צמחיים",
]

milk_seed_oil_products = []

for tf in trace_files:
    try:
        with open(tf, encoding="utf-8") as f:
            trace = json.load(f)
    except Exception:
        continue

    parts = tf.parts
    try:
        cat_idx = parts.index("02_products") + 1
        category = parts[cat_idx]
    except (ValueError, IndexError):
        category = "unknown"

    if category not in ("milk_and_alternatives", "milk", "milks", "milk_alternatives"):
        continue

    l3 = trace.get("l3_signals", {})
    has_seed_oil = l3.get("has_seed_oil", False)
    if not has_seed_oil:
        continue

    barcode = trace.get("barcode") or trace.get("product_id", "")
    product_name = trace.get("product_name") or trace.get("name", "")
    seed_oil_matches = l3.get("seed_oil_matches", [])

    # Get ingredient text
    ing_text = (
        l3.get("ingredients_text") or
        l3.get("ingredient_text") or
        trace.get("ingredients_text") or
        trace.get("ingredient_text") or
        ""
    )

    # Also check raw data
    raw_ing = barcode_to_ing.get(str(barcode), "")

    final_score = trace.get("final_score") or trace.get("score")
    grade_val = trace.get("grade")

    milk_seed_oil_products.append({
        "barcode": barcode,
        "category": category,
        "product_name": product_name,
        "has_seed_oil": True,
        "seed_oil_matches": seed_oil_matches,
        "ing_text_trace": ing_text[:300],
        "ing_text_raw": raw_ing[:300],
        "final_score": final_score,
        "grade": grade_val,
        "trace_path": str(tf),
    })

print(f"Milk products with has_seed_oil=True: {len(milk_seed_oil_products)}")
for p in milk_seed_oil_products:
    print(f"\n  Barcode: {p['barcode']}")
    print(f"  Name: {p['product_name']}")
    print(f"  Category: {p['category']}")
    print(f"  Score: {p['final_score']} Grade: {p['grade']}")
    print(f"  seed_oil_matches: {p['seed_oil_matches']}")
    print(f"  ing_text (trace): {p['ing_text_trace'][:150]}")
    print(f"  ing_text (raw): {p['ing_text_raw'][:150]}")

# Try to get ingredient text from raw files for these milk products
milk_barcodes = set(str(p["barcode"]) for p in milk_seed_oil_products)
print(f"\nSearching raw files for milk seed-oil barcodes: {milk_barcodes}")

# Search raw files specifically for milk products
for rf in raw_json_files:
    try:
        with open(rf, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        continue

    products_to_check = []
    if isinstance(data, list):
        products_to_check = data
    elif isinstance(data, dict):
        for key in ["products", "items", "data"]:
            if isinstance(data.get(key), list):
                products_to_check = data[key]
                break
        if not products_to_check:
            products_to_check = [data]

    for obj in products_to_check:
        if not isinstance(obj, dict):
            continue
        bc = get_barcode_from_obj(obj)
        if bc and bc in milk_barcodes:
            ing = extract_from_product_obj(obj)
            name = obj.get("name") or obj.get("product_name") or ""
            print(f"\n  Found in raw file {rf.name}:")
            print(f"    Barcode: {bc}, Name: {name}")
            print(f"    Ingredients: {ing[:200]}")
            # Look for what fired the seed oil marker
            if ing:
                for marker in SEED_OIL_MARKERS:
                    if marker in ing:
                        print(f"    >> Fired marker: '{marker}'")

# ============================================================
# STEP 8: Exact seed_pen 10->5 blast radius
# ============================================================
print("\n\n=== DELIVERABLE 3: Exact seed_pen 10->5 blast radius ===")

# We need to find all products where seed_pen actually fires in the final score
# i.e. where the fat_quality note contains "seed" or "seed_pen" and seed_pen > 0
# AND it's the sprint1 path (EV-012 or fat_v1 note)

GRADE_BOUNDARIES = [80.0, 65.0, 50.0, 35.0]

def would_cross_boundary(score_before, delta):
    """Returns True if adding delta to score_before crosses a grade boundary."""
    score_after = score_before + delta
    grade_before = grade(score_before)
    grade_after = grade(score_after)
    return grade_before != grade_after

# fat_quality weight
FAT_QUALITY_WEIGHT = 0.08
DELTA_FINAL = 5 * FAT_QUALITY_WEIGHT  # = 0.4 (reducing seed_pen by 5 adds +0.4 to final score)

confirmed_path_products = []  # products where seed_pen fires
grade_crossers = []

# We need to find the confirmed 719 products where seed_pen reaches final score
# The Nutrition Agent found: seed_pen confirmed in fat_note (EV-012 or fat_v1 path): 719
# For this we look for fat_note containing "seed" or check fat_quality note

for tf in trace_files:
    try:
        with open(tf, encoding="utf-8") as f:
            trace = json.load(f)
    except Exception:
        continue

    parts = tf.parts
    try:
        cat_idx = parts.index("02_products") + 1
        category = parts[cat_idx]
    except (ValueError, IndexError):
        category = "unknown"

    l3 = trace.get("l3_signals", {})
    has_seed_oil = l3.get("has_seed_oil", False)
    if not has_seed_oil:
        continue

    # Check if seed_pen fires on the score path
    # Look in the score trace / dimensions
    dims = trace.get("dimensions") or trace.get("score_dimensions") or {}
    fat_qual_dim = dims.get("fat_quality") or {}
    fat_note = fat_qual_dim.get("note") or fat_qual_dim.get("rationale") or ""

    # Also check scoring_trace
    scoring_trace = trace.get("scoring_trace") or {}
    fat_quality_trace = scoring_trace.get("fat_quality") or {}
    fat_q_note = fat_quality_trace.get("note") or ""

    # Try all note fields
    all_notes = " ".join([fat_note, fat_q_note])

    # Check if seed_pen appears in notes (indicates it fired on this path)
    seed_pen_in_note = "seed" in all_notes.lower() and ("seed10" in all_notes or "seed_pen" in all_notes.lower()
                        or "-seed" in all_notes or "seed0" in all_notes)

    # Also try: look for fat_quality dimension value and check if seed_pen=10 is subtracted
    # The note format is like: "EV-012 fat_ratio: fat=Xg ratio=X.XXX base=XX.X-seed10-trans0=XX.X"
    fat_quality_score = fat_qual_dim.get("score") or fat_qual_dim.get("value")
    if fat_quality_score is None:
        fat_quality_score = fat_quality_trace.get("score") or fat_quality_trace.get("value")

    final_score = trace.get("final_score") or trace.get("score")
    barcode = trace.get("barcode") or trace.get("product_id", "")
    grade_val = trace.get("grade")

    # Determine if seed_pen is ON the confirmed path
    # The Nutrition Agent's method: check if "seed10" or "-seed10" or "seed_pen=10" in fat note
    # or if has_seed_oil AND NOT on neutral-50 or SRC-04 path
    on_confirmed_path = False
    if has_seed_oil:
        if fat_note or fat_q_note:
            combined_note = (fat_note + " " + fat_q_note).lower()
            # Confirmed path: EV-012 or fat_v1 notes contain "-seed10" or "seed10"
            if "-seed10" in combined_note or "seed10" in combined_note or "seed_pen" in combined_note:
                on_confirmed_path = True
            # Also check seed=10 format variations
            elif "seed" in combined_note and "10" in combined_note:
                on_confirmed_path = True
            # Exclude neutral-50 path
            elif "neutral 50" in combined_note or "neutral-50" in combined_note or "src-04" in combined_note.lower():
                on_confirmed_path = False
            else:
                # If has_seed_oil and note doesn't say neutral, mark as confirmed
                # unless structurally empty
                if not ("structurally empty" in combined_note or "sat_fat absent" in combined_note):
                    on_confirmed_path = True
        elif has_seed_oil:
            # No note available — count conservatively: not confirmed
            pass

    if on_confirmed_path:
        confirmed_path_products.append({
            "barcode": barcode,
            "category": category,
            "final_score": final_score,
            "grade": grade_val,
            "fat_quality_score": fat_quality_score,
            "fat_note": all_notes[:150],
        })

        # Check grade boundary crossing
        if final_score is not None:
            try:
                fs = float(final_score)
                if would_cross_boundary(fs, DELTA_FINAL):
                    grade_crossers.append({
                        "barcode": barcode,
                        "category": category,
                        "score_before": round(fs, 2),
                        "score_after": round(fs + DELTA_FINAL, 2),
                        "grade_before": grade(fs),
                        "grade_after": grade(fs + DELTA_FINAL),
                        "fat_note": all_notes[:100],
                    })
            except (TypeError, ValueError):
                pass

print(f"Confirmed seed_pen-path products (from trace notes): {len(confirmed_path_products)}")
print(f"Grade-boundary crossers (seed_pen 10->5, delta=+0.4): {len(grade_crossers)}")

# Check how many are in published/frozen categories
FROZEN_CATEGORIES = {"milk_and_alternatives", "milk", "milks", "bread_light", "bread"}
PUBLISHED_CATEGORIES = {
    "milk_and_alternatives", "milk", "bread_light", "salty_snacks",
    "cookies_coffee", "brined_cheeses", "yogurt_system",
}

print("\nGrade crossers (barcode | score_before | score_after | grade_before->grade_after | category):")
frozen_crossers = []
published_crossers = []
for p in sorted(grade_crossers, key=lambda x: x["score_before"]):
    is_frozen = p["category"] in FROZEN_CATEGORIES
    is_published = p["category"] in PUBLISHED_CATEGORIES
    flag = "[FROZEN]" if is_frozen else ("[PUBLISHED]" if is_published else "")
    print(f"  {p['barcode']!s:20s} | {p['score_before']:6.2f} | {p['score_after']:6.2f} | {p['grade_before']}->{p['grade_after']} | {p['category']} {flag}")
    if is_frozen:
        frozen_crossers.append(p)
    if is_published:
        published_crossers.append(p)

print(f"\nFrozen category crossers: {len(frozen_crossers)}")
print(f"Published category crossers: {len(published_crossers)}")

# ============================================================
# STEP 9: Try alternate method - look at score dimensions more carefully
# ============================================================
print("\n=== Alternate method: scan full trace structure for fat_quality ===")
# Print structure of first few traces to understand where score data lives
shown = 0
for tf in trace_files:
    if shown >= 3:
        break
    try:
        with open(tf, encoding="utf-8") as f:
            trace = json.load(f)
    except Exception:
        continue
    l3 = trace.get("l3_signals", {})
    if not l3.get("has_seed_oil", False):
        continue
    print(f"\nTrace keys: {list(trace.keys())}")
    # Print all nested keys
    for k, v in trace.items():
        if isinstance(v, dict):
            print(f"  {k}: {list(v.keys())[:20]}")
        elif isinstance(v, (int, float, str)):
            print(f"  {k}: {v!r}")
    shown += 1

print("\n=== SUMMARY ===")
print(f"D1 PHVO: {len(phvo_products)} has_phvo products")
print(f"  PARTIAL (חלקית confirmed): {len(bucket_partial)}")
print(f"  GENERIC (מוקשה no חלקית):  {len(bucket_generic)}")
print(f"  INDETERMINATE:              {len(bucket_indeterminate)}")
print(f"  EMPTY TEXT:                 {len(bucket_empty_text)}")
print(f"D2 Milk seed-oil: {len(milk_seed_oil_products)} products")
print(f"D3 Blast radius confirmed-path: {len(confirmed_path_products)}")
print(f"   Grade crossers (10->5): {len(grade_crossers)}")
