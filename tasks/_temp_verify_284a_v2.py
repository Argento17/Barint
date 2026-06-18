"""
TASK-284A v2 - Data verification pass.
Deliverable 1: PHVO partial-vs-generic split (unblocks EV-097)
Deliverable 2: Milk seed-oil anomaly (3 products)
Deliverable 3: Exact seed_pen 10->5 blast radius (firms EV-096)

Run: python tasks/_temp_verify_284a_v2.py 2>&1
"""

import json
import sys
import os
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("C:/Bari")
PRODUCTS_DIR = ROOT / "02_products"
FAT_QUALITY_WEIGHT = 0.08  # from score_engine.py

# Grade function (A>=80, B>=65, C>=50, D>=35, E<35)
def grade(score):
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"

# ============================================================
# Load all traces
# ============================================================
print("=== Loading traces ===")
trace_files = list(PRODUCTS_DIR.rglob("bsip2_trace.json"))
print(f"Total trace files: {len(trace_files)}")

def get_category(tf):
    parts = tf.parts
    try:
        cat_idx = parts.index("02_products") + 1
        return parts[cat_idx]
    except (ValueError, IndexError):
        return "unknown"

# ============================================================
# DELIVERABLE 1: PHVO partial-vs-generic split
# ============================================================
print("\n=== DELIVERABLE 1: PHVO partial-vs-generic split ===")

PARTIAL_TERMS = ["מוקשה חלקית", "partially hydrogenated", "partially-hydrogenated"]
# Terms that indicate generic hardened fat WITHOUT partial qualifier
GENERIC_MUKSHA_TERMS = [
    "שומן מוקשה", "שומנים מוקשים", "שומן צמחי מוקשה",
    "שמן צמחי מוקשה", "מוקשים מן הצומח", "חלקם מוקשים",
    "שומן דקלים מוקשה", "שמן קוקוס מוקשה",
]
MARGARINE_TERMS = ["מרגרינה"]

# First, collect all has_phvo products and their bsip1_source_path
phvo_prods = []
for tf in trace_files:
    with open(tf, encoding='utf-8') as f:
        data = json.load(f)
    l3 = data.get('L3_inferred_classifications', {})
    if not isinstance(l3, dict): continue
    if not l3.get('has_phvo', False): continue

    category = get_category(tf)
    barcode = ""
    product_name = ""
    bsip1_path = ""

    inp = data.get('input_reference')
    if isinstance(inp, dict):
        barcode = str(inp.get('barcode', '') or inp.get('canonical_product_id', ''))
        product_name = inp.get('product_name_he', '') or inp.get('product_name', '')
        bsip1_path = inp.get('bsip1_source_path', '')
    elif isinstance(inp, list):
        # input_reference stored as list of field names
        pass

    final_score = data.get('final_score_estimate')
    grade_est = data.get('grade_estimate', '')

    phvo_prods.append({
        "barcode": barcode,
        "category": category,
        "product_name": product_name,
        "bsip1_path": bsip1_path,
        "final_score": final_score,
        "grade": grade_est,
        "trace_path": str(tf),
    })

print(f"has_phvo=True products: {len(phvo_prods)}")

# Now recover ingredient text from BSIP1 source files and BSIP0 raw files
# Build a barcode -> ingredient text map

print("\nBuilding ingredient text index from BSIP1 files...")
barcode_to_ing = {}  # barcode -> {"ing_text": str, "source": str}

def extract_ing(obj):
    """Try to extract ingredient text from a product dict."""
    for key in ["ingredients_text", "ingredient_text", "ingredients_raw",
                "ingredients", "ingredients_he", "raw_ingredients",
                "product_text", "label_text"]:
        val = obj.get(key)
        if isinstance(val, str) and len(val) > 5:
            return val
        if isinstance(val, list) and val:
            return " ".join(str(v) for v in val)
    return ""

def get_bc(obj):
    for key in ["barcode", "canonical_product_id", "product_id", "ean", "gtin", "id", "bsip1_id"]:
        val = obj.get(key)
        if val:
            return str(val).strip()
    return ""

phvo_barcodes = {p["barcode"] for p in phvo_prods if p["barcode"]}
print(f"PHVO barcodes to match: {len(phvo_barcodes)}")

# Search BSIP1 JSON files
bsip1_json = list(ROOT.rglob("bsip1_*.json")) + list(ROOT.rglob("*_bsip1.json"))
print(f"BSIP1 JSON files to scan: {len(bsip1_json)}")

for bf in bsip1_json:
    try:
        with open(bf, encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        continue
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for k in ["products", "items", "data", "results"]:
            if isinstance(data.get(k), list):
                items = data[k]
                break
        if not items:
            items = [data]
    for obj in items:
        if not isinstance(obj, dict): continue
        bc = get_bc(obj)
        if bc and bc in phvo_barcodes and bc not in barcode_to_ing:
            ing = extract_ing(obj)
            if ing:
                barcode_to_ing[bc] = {"ing_text": ing, "source": str(bf.name)}

print(f"Barcodes found in BSIP1: {len(barcode_to_ing)}")

# Also search bsip0 raw files
print("Scanning BSIP0 raw files...")
raw_json = [f for f in PRODUCTS_DIR.rglob("*.json") if "bsip2_trace" not in f.name]
print(f"Non-trace JSON files in 02_products: {len(raw_json)}")

for rf in raw_json:
    try:
        with open(rf, encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        continue
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for k in ["products", "items", "data", "results"]:
            if isinstance(data.get(k), list):
                items = data[k]
                break
        if not items:
            items = [data]
    for obj in items:
        if not isinstance(obj, dict): continue
        bc = get_bc(obj)
        if bc and bc in phvo_barcodes and bc not in barcode_to_ing:
            ing = extract_ing(obj)
            if ing:
                barcode_to_ing[bc] = {"ing_text": ing, "source": str(rf.name)}

print(f"Total barcodes with ingredient text: {len(barcode_to_ing)}")

# Now classify
bucket_partial = []
bucket_generic = []
bucket_indeterminate = []
bucket_empty = []

per_cat = defaultdict(lambda: {"partial": [], "generic": [], "indeterminate": [], "empty": []})

for p in phvo_prods:
    bc = p["barcode"]
    cat = p["category"]

    ing_info = barcode_to_ing.get(bc)
    ing_text = ing_info["ing_text"] if ing_info else ""
    source = ing_info["source"] if ing_info else ""

    if not ing_text:
        bucket_empty.append({**p, "classified": "empty"})
        per_cat[cat]["empty"].append(bc)
        continue

    has_partial = any(term in ing_text for term in PARTIAL_TERMS)

    if has_partial:
        # Confirmed partial hydrogenation
        bucket_partial.append({
            **p,
            "classified": "partial",
            "trigger": [t for t in PARTIAL_TERMS if t in ing_text],
            "ing_snippet": ing_text[:200],
            "ing_source": source,
        })
        per_cat[cat]["partial"].append(bc)
    else:
        # Check for generic muksha terms
        generic_hits = [t for t in GENERIC_MUKSHA_TERMS if t in ing_text]
        margarine_hits = [t for t in MARGARINE_TERMS if t in ing_text]
        all_generic_hits = generic_hits + margarine_hits

        if all_generic_hits:
            bucket_generic.append({
                **p,
                "classified": "generic",
                "trigger": all_generic_hits,
                "ing_snippet": ing_text[:200],
                "ing_source": source,
            })
            per_cat[cat]["generic"].append(bc)
        else:
            # Has ingredient text but no muksha/margarine term found
            # Check for any 'מוקש' variant
            if "מוקש" in ing_text or "moqash" in ing_text.lower() or "hydrogenated" in ing_text.lower():
                bucket_partial.append({
                    **p,
                    "classified": "partial_fallback",
                    "trigger": ["hydrogenated (no Hebrew term found)"],
                    "ing_snippet": ing_text[:200],
                    "ing_source": source,
                })
                per_cat[cat]["partial"].append(bc)
            else:
                bucket_indeterminate.append({
                    **p,
                    "classified": "indeterminate",
                    "ing_snippet": ing_text[:200],
                    "ing_source": source,
                    "note": "has_phvo fired but no PHVO term found in recovered text",
                })
                per_cat[cat]["indeterminate"].append(bc)

print(f"\n--- PHVO Classification Results ---")
print(f"PARTIAL (confirmed חלקית / partially hydrogenated): {len(bucket_partial)}")
print(f"GENERIC (מוקשה without חלקית):                      {len(bucket_generic)}")
print(f"INDETERMINATE (text present, no term found):         {len(bucket_indeterminate)}")
print(f"EMPTY (no ingredient text recovered):                {len(bucket_empty)}")
print(f"TOTAL has_phvo:                                      {len(phvo_prods)}")

print("\nPer-category breakdown:")
for cat in sorted(per_cat.keys()):
    d = per_cat[cat]
    total = sum(len(v) for v in d.values())
    print(f"  {cat}: total={total} partial={len(d['partial'])} generic={len(d['generic'])} indet={len(d['indeterminate'])} empty={len(d['empty'])}")

print("\nPARTIAL barcodes (confirmed חלקית):")
for p in bucket_partial:
    print(f"  BC={p['barcode']!s:25s} cat={p['category']!s:25s} trigger={p['trigger']}")
    print(f"    snippet: {p['ing_snippet'][:120]}")

print("\nGENERIC barcodes (מוקשה without חלקית):")
for p in bucket_generic:
    print(f"  BC={p['barcode']!s:25s} cat={p['category']!s:25s} trigger={p['trigger']}")
    print(f"    snippet: {p['ing_snippet'][:120]}")

print("\nINDETERMINATE (text present, term not found):")
for p in bucket_indeterminate:
    print(f"  BC={p['barcode']!s:25s} cat={p['category']!s:25s}")
    print(f"    snippet: {p['ing_snippet'][:120]}")
    print(f"    note: {p['note']}")

print(f"\nEMPTY (no text recovered) - count by category:")
empty_by_cat = defaultdict(list)
for p in bucket_empty:
    empty_by_cat[p["category"]].append(p["barcode"])
for cat, bcs in sorted(empty_by_cat.items()):
    print(f"  {cat}: {len(bcs)} -- {bcs[:5]}")

# ============================================================
# DELIVERABLE 2: Milk seed-oil anomaly
# ============================================================
print("\n\n=== DELIVERABLE 2: Milk seed-oil anomaly ===")

SEED_OIL_MARKERS = [
    "שמן חמניות", "שמן קנולה", "שמן תירס", "שמן סויה",
    "שמן צמחי", "שמנים צמחיים",
]

# Find milk category slug
# Look at categories present
all_categories = set(get_category(tf) for tf in trace_files)
print(f"All categories: {sorted(all_categories)}")

# Find milk-like category
milk_cats = [c for c in all_categories if "milk" in c.lower() or "חלב" in c]
print(f"Milk-like categories: {milk_cats}")

milk_seed_products = []
for tf in trace_files:
    with open(tf, encoding='utf-8') as f:
        data = json.load(f)
    cat = get_category(tf)
    if cat not in milk_cats and cat != "milk_and_alternatives":
        continue

    l3 = data.get('L3_inferred_classifications', {})
    if not isinstance(l3, dict): continue
    if not l3.get('has_seed_oil', False): continue

    barcode = ""
    product_name = ""
    inp = data.get('input_reference')
    if isinstance(inp, dict):
        barcode = str(inp.get('barcode', '') or inp.get('canonical_product_id', ''))
        product_name = inp.get('product_name_he', '') or inp.get('product_name', '')

    seed_oil_matches = l3.get('seed_oil_matches', [])
    final_score = data.get('final_score_estimate')
    grade_est = data.get('grade_estimate', '')

    milk_seed_products.append({
        "barcode": barcode,
        "category": cat,
        "product_name": product_name,
        "seed_oil_matches": seed_oil_matches,
        "final_score": final_score,
        "grade": grade_est,
        "trace_path": str(tf),
    })

print(f"\nMilk products with has_seed_oil=True: {len(milk_seed_products)}")

# Now recover ingredient text for these products
milk_barcodes = {p["barcode"] for p in milk_seed_products if p["barcode"]}
print(f"Milk seed-oil barcodes to search: {milk_barcodes}")

milk_ing_texts = {}
# Search all raw files including bsip0
for rf in raw_json:
    try:
        with open(rf, encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        continue
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for k in ["products", "items", "data"]:
            if isinstance(data.get(k), list):
                items = data[k]
                break
        if not items:
            items = [data]
    for obj in items:
        if not isinstance(obj, dict): continue
        bc = get_bc(obj)
        if bc and bc in milk_barcodes:
            ing = extract_ing(obj)
            name = obj.get("name") or obj.get("product_name") or obj.get("product_name_he", "")
            if bc not in milk_ing_texts:
                milk_ing_texts[bc] = {"ing": ing, "name": name, "source": str(rf.name)}
            elif ing and not milk_ing_texts[bc]["ing"]:
                milk_ing_texts[bc] = {"ing": ing, "name": name, "source": str(rf.name)}

# Also search bsip1 for milk products
for bf in bsip1_json:
    try:
        with open(bf, encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        continue
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for k in ["products", "items", "data"]:
            if isinstance(data.get(k), list):
                items = data[k]
                break
        if not items:
            items = [data]
    for obj in items:
        if not isinstance(obj, dict): continue
        bc = get_bc(obj)
        if bc and bc in milk_barcodes:
            ing = extract_ing(obj)
            name = obj.get("name") or obj.get("product_name") or obj.get("product_name_he", "")
            if bc not in milk_ing_texts:
                milk_ing_texts[bc] = {"ing": ing, "name": name, "source": str(bf.name)}
            elif ing and not milk_ing_texts[bc]["ing"]:
                milk_ing_texts[bc] = {"ing": ing, "name": name, "source": str(bf.name)}

print(f"\nIngredient text found for {len(milk_ing_texts)} milk seed-oil products")

for p in milk_seed_products:
    bc = p["barcode"]
    ing_info = milk_ing_texts.get(bc, {})
    ing = ing_info.get("ing", "")
    src = ing_info.get("source", "")

    print(f"\n  --- Product: {p['product_name'] or bc} ---")
    print(f"  Barcode: {bc}")
    print(f"  Category: {p['category']}")
    print(f"  Score: {p['final_score']} / Grade: {p['grade']}")
    print(f"  seed_oil_matches (from trace): {p['seed_oil_matches']}")
    print(f"  Ingredient text source: {src}")
    print(f"  Ingredient text: {ing[:250] if ing else '(EMPTY)'}")

    if ing:
        fired = [m for m in SEED_OIL_MARKERS if m in ing]
        print(f"  Markers fired in ingredient text: {fired}")

    # Assess: real or artifact?
    name_lower = (p['product_name'] or "").lower()
    if "שקד" in (p['product_name'] or "") or "שיבולת" in (p['product_name'] or "") or "סויה" in (p['product_name'] or ""):
        verdict = "LIKELY REAL: plant-based or flavored product"
    elif ing and any(m in ing for m in SEED_OIL_MARKERS):
        verdict = "REAL: seed-oil marker confirmed in ingredient text"
    elif not ing:
        verdict = "UNKNOWN: no ingredient text to verify"
    else:
        verdict = "POSSIBLE ARTIFACT: seed_oil fired but not confirmed in recovered text"

    print(f"  VERDICT: {verdict}")

# ============================================================
# DELIVERABLE 3: Exact seed_pen 10->5 blast radius
# ============================================================
print("\n\n=== DELIVERABLE 3: Exact seed_pen 10->5 blast radius ===")
# seed_pen fires when:
# 1. has_seed_oil=True
# 2. The product is NOT on the neutral-50 path (sat_fat absent) or SRC-04 path
# The Nutrition Agent confirmed 719 products on the confirmed path.
# We need to find these and compute grade shifts.

# Strategy: scan traces for has_seed_oil=True, check fat_quality dimension note
# to confirm seed_pen is in the computation (note contains "-seed10" or "seed10")

DELTA = 5 * FAT_QUALITY_WEIGHT  # = +0.4 to final score

confirmed_path = []
grade_crossers = []

# Categories with published/frozen scores
FROZEN_CATS = {"milk_and_alternatives", "milk", "milks"}
PUBLISHED_CATS = {
    "milk_and_alternatives", "milk", "milks",
    "bread_light", "bread",
    "salty_snacks", "cookies_coffee", "brined_cheeses", "yogurt_system",
    "cakes_hard_cookies", "breakfast_cereals",
}

for tf in trace_files:
    with open(tf, encoding='utf-8') as f:
        data = json.load(f)

    l3 = data.get('L3_inferred_classifications', {})
    if not isinstance(l3, dict): continue
    if not l3.get('has_seed_oil', False): continue

    # Get fat_quality dimension note
    dim_notes = data.get('dimension_notes', {})
    fat_q_note = ""
    if isinstance(dim_notes, dict):
        fat_q_note = dim_notes.get('fat_quality', '')

    # Get fat_quality score
    dim_scores = data.get('dimension_scores', {})
    fat_q_score = None
    if isinstance(dim_scores, dict):
        fat_q_score = dim_scores.get('fat_quality')

    # Determine if seed_pen is on the confirmed path
    on_confirmed_path = False
    if fat_q_note:
        note_lower = fat_q_note.lower()
        # seed_pen fires on EV-012 path or fat_v1 path
        # Note format: "EV-012 fat_ratio: fat=Xg ratio=X.XXX base=XX.X-seed10-trans0=XX.X"
        # or "fat_v1(...): ... base=XX.X-seed10..."
        # Key pattern: "-seed10" or "seed10" in note
        if "-seed10" in fat_q_note or "seed10" in fat_q_note:
            on_confirmed_path = True
        elif "seed" in note_lower and "10" in fat_q_note:
            # Check it's seed_pen=10 not something else
            if "seed_pen" in note_lower or "-seed" in fat_q_note:
                on_confirmed_path = True
        # Exclude neutral paths
        if "neutral 50" in note_lower or "neutral-50" in note_lower or "src-04" in note_lower:
            on_confirmed_path = False
        if "sat_fat absent" in note_lower:
            on_confirmed_path = False

    if not on_confirmed_path:
        continue

    # Get final score
    final_score = data.get('final_score_estimate')
    grade_est = data.get('grade_estimate', '')
    category = get_category(tf)

    barcode = ""
    product_name = ""
    inp = data.get('input_reference')
    if isinstance(inp, dict):
        barcode = str(inp.get('barcode', '') or inp.get('canonical_product_id', ''))
        product_name = inp.get('product_name_he', '') or inp.get('product_name', '')

    confirmed_path.append({
        "barcode": barcode,
        "category": category,
        "product_name": product_name,
        "final_score": final_score,
        "grade": grade_est,
        "fat_q_note": fat_q_note[:120],
    })

    # Check grade boundary crossing
    if final_score is not None:
        try:
            fs = float(final_score)
            score_after = round(fs + DELTA, 2)
            g_before = grade(fs)
            g_after = grade(score_after)
            if g_before != g_after:
                is_frozen = category in FROZEN_CATS
                is_published = category in PUBLISHED_CATS
                grade_crossers.append({
                    "barcode": barcode,
                    "category": category,
                    "product_name": product_name,
                    "score_before": round(fs, 2),
                    "score_after": score_after,
                    "grade_before": g_before,
                    "grade_after": g_after,
                    "is_frozen": is_frozen,
                    "is_published": is_published,
                    "fat_q_note": fat_q_note[:80],
                })
        except (TypeError, ValueError):
            pass

print(f"Confirmed seed_pen-path products (from fat_quality notes): {len(confirmed_path)}")
print(f"Grade-boundary crossers (seed_pen 10->5, +0.4 final): {len(grade_crossers)}")

# If confirmed_path count differs from Nutrition Agent's 719, explain
diff = len(confirmed_path) - 719
print(f"Expected: 719. Delta from expected: {diff:+d}")

# Note distribution for debugging
if len(confirmed_path) == 0:
    print("\nDEBUG: Showing fat_quality note patterns from has_seed_oil=True products...")
    seed_sample = []
    for tf in trace_files:
        if len(seed_sample) >= 10: break
        with open(tf, encoding='utf-8') as f:
            data = json.load(f)
        l3 = data.get('L3_inferred_classifications', {})
        if not isinstance(l3, dict): continue
        if not l3.get('has_seed_oil', False): continue
        dim_notes = data.get('dimension_notes', {})
        fat_q_note = ""
        if isinstance(dim_notes, dict):
            fat_q_note = dim_notes.get('fat_quality', '')
        seed_sample.append(fat_q_note[:150])
    for s in seed_sample:
        print(f"  note: {s!r}")

print(f"\nGrade crosser breakdown:")
for g_change in [("D", "E"), ("C", "D"), ("B", "C"), ("A", "B"),
                  ("E", "D"), ("D", "C"), ("C", "B"), ("B", "A")]:
    crossers_of_type = [p for p in grade_crossers if p["grade_before"] == g_change[0] and p["grade_after"] == g_change[1]]
    if crossers_of_type:
        print(f"  {g_change[0]}->{g_change[1]}: {len(crossers_of_type)}")

print(f"\nFull grade crosser table:")
print(f"{'Barcode':25s} | {'score_before':12s} | {'score_after':12s} | {'grade':15s} | {'category':25s} | flags")
print("-" * 120)
frozen_count = 0
published_count = 0
for p in sorted(grade_crossers, key=lambda x: x["score_before"]):
    flags = ""
    if p["is_frozen"]: flags += "[FROZEN]"
    if p["is_published"] and not p["is_frozen"]: flags += "[PUBLISHED]"
    print(f"  {p['barcode']!s:25s} | {p['score_before']:12.2f} | {p['score_after']:12.2f} | {p['grade_before']}->{p['grade_after']:10s} | {p['category']:25s} | {flags}")
    if p["is_frozen"]: frozen_count += 1
    if p["is_published"]: published_count += 1

print(f"\nFrozen category crossers: {frozen_count}")
print(f"Published category crossers (incl. frozen): {published_count}")
print(f"Unpublished category crossers: {len(grade_crossers) - published_count}")

# ============================================================
# SUMMARY
# ============================================================
print("\n\n=== FINAL SUMMARY ===")
print(f"D1 PHVO split (total has_phvo={len(phvo_prods)}):")
print(f"  PARTIAL (confirmed חלקית/partially hydrogenated): {len(bucket_partial)}")
print(f"  GENERIC (מוקשה without חלקית):                    {len(bucket_generic)}")
print(f"  INDETERMINATE:                                     {len(bucket_indeterminate)}")
print(f"  EMPTY (no ingredient text recoverable):            {len(bucket_empty)}")
print(f"D2 Milk seed-oil: {len(milk_seed_products)} products")
print(f"D3 Confirmed seed_pen path: {len(confirmed_path)} products")
print(f"   Grade crossers on 10->5 (+0.4 delta): {len(grade_crossers)}")
print(f"   Frozen category crossers: {frozen_count}")
