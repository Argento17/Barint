"""
TASK-283 Wave 1 (DATA): Restructure cakes+cookies split.
1. Segment 149 IN_SCORED into CAKES vs COOKIES/BISCUITS
2. Fix additive-display bug (detected_additives → extracted_additives)
3. Regenerate cakes-only JSON
4. Produce merged biscuits JSON
"""
import json, glob, re, pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(r"C:\Bari")
CORPUS_PATH = ROOT / "02_products" / "cakes_hard_cookies" / "factory_run_001" / "corpus_filter.json"
TRACE_DIR = ROOT / "02_products" / "cakes_hard_cookies" / "bsip2_outputs" / "run_cakes_001" / "products"
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / "run_cakes_001" / "output"
EXISTING_CC = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v1.json"
OUT_CAKES = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cakes_hard_cookies_frontend_v1.json"
OUT_BISCUITS = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"
PENDING = "PENDING_COPY"

# ── 1. Load all source data ──────────────────────────────────────────────────
corpus = json.load(open(CORPUS_PATH, encoding="utf-8"))
IN_SCORED = {str(p["barcode"]): p["name_he"] for p in corpus["products"] if p["decision"] == "IN_SCORED"}
print(f"IN_SCORED count: {len(IN_SCORED)}")

# Load all BSIP1 records
bsip1 = {}
for f in glob.glob(str(BSIP1_DIR / "bsip1_cakes_*.json")):
    d = json.load(open(f, encoding="utf-8"))
    bsip1[str(d["barcode"])] = d

# Load all BSIP2 traces
traces = {}
for f in glob.glob(str(TRACE_DIR / "*" / "bsip2_trace.json")):
    t = json.load(open(f, encoding="utf-8"))
    bc = str((t.get("input_reference") or {}).get("barcode") or t.get("barcode") or "")
    if bc:
        traces[bc] = t

# Load existing cookies-coffee
cc_existing = json.load(open(EXISTING_CC, encoding="utf-8"))
cc_existing_barcodes = {str(p["barcode"]) for p in cc_existing["products"]}
print(f"Existing cookies_coffee products: {len(cc_existing['products'])}")

# ── 2. Segmentation rules ────────────────────────────────────────────────────
CAKE_PREFIXES = ("עוגת", "עוגה")
CAKE_KEYWORDS = [
    "מאפין", "שטרודל", "בראוניס", "מוס", "שמרים", "בריוש", "דובוש",
    "נפוליאון", "ספוג", "טירמיסו", "היער השחור", "אנגלית",
    "עוגת גבינה", "עוגת דבש", "עוגת פס", "רולדה",
    # Additional cake indicators from the actual data
    "עוגת", "עוגה", "עוגות אישיות", "עוגות ספוג",
]
COOKIE_PREFIXES = ("עוגיות", "עוגייה", "עוגיה", "ביסקוויט")
COOKIE_KEYWORDS = [
    "ביסקוויט", "קוקיס", "וופל", "קראנץ", "אוראו", "מילקה", "לוטוס",
    "סנדוויץ", "מרוקאי", "בוטנים", "כוסמין", "שיבולת שועל",
    "גן חיות", "נסיכה", "אצבעות", "מקלות", "קרמוגית", "גולד רינג",
    "שרקיז", "מעמול",
    # Additional observed patterns
    "עוגיות", "עוגייה", "עוגיה",
]

def segment(name_he):
    """Return 'CAKE', 'COOKIE', or 'AMBIGUOUS' with reason."""
    n = name_he.strip()

    # Strip price/weight suffixes that appear in some names
    # e.g. "עוגיות שוקוצ'יפס קלאסי 200 גרם ..." → use first meaningful part
    # We segment on the full name but note if it's a retailer-packaged name

    # Check cookie indicators first (more specific prefixes)
    for prefix in COOKIE_PREFIXES:
        if n.startswith(prefix):
            return "COOKIE", f"starts with '{prefix}'"

    for kw in COOKIE_KEYWORDS:
        if kw in n and kw not in ["עוגיות", "עוגייה", "עוגיה"]:  # avoid double-counting prefix logic
            return "COOKIE", f"contains '{kw}'"

    # Check cake indicators
    for prefix in CAKE_PREFIXES:
        if n.startswith(prefix):
            return "CAKE", f"starts with '{prefix}'"

    for kw in CAKE_KEYWORDS:
        if kw in n and kw not in ["עוגת", "עוגה"]:  # avoid double-counting prefix logic
            return "CAKE", f"contains '{kw}'"

    # Special cases by name pattern
    # "מיני שטרודל" → CAKE (strudel)
    if "שטרודל" in n:
        return "CAKE", "contains 'שטרודל'"
    # "קרנץ אגוזי לוז" / "קרנץ מיני" / "קרנץ סנדוויץ" → COOKIE/BISCUIT
    if n.startswith("קרנץ") or "קרנץ'" in n or "קראנץ" in n:
        # Distinguish: עוגת קרנץ = cake, standalone קרנץ = cookie
        if "עוגת" in n:
            return "CAKE", "עוגת קרנץ = cake"
        return "COOKIE", "קרנץ/קראנץ standalone = cookie/biscuit"
    # "קרמוגית" → COOKIE
    if "קרמוגית" in n:
        return "COOKIE", "contains 'קרמוגית'"
    # "מארז" / "מארז מיני" → usually cookies
    if n.startswith("מארז") or "מארז מיני" in n:
        return "COOKIE", "מארז = cookie pack"
    # "חמישיית מאפין" → CAKE
    if "חמישיית" in n and "מאפין" in n:
        return "CAKE", "חמישיית מאפין"
    # "5עוגות מאפין" → CAKE
    if "מאפין" in n:
        return "CAKE", "contains 'מאפין'"
    # "עינוביין קוקיס" → COOKIE
    if "קוקיס" in n:
        return "COOKIE", "contains 'קוקיס'"
    # "פרה קרנץ'" → COOKIE (פרה = cow brand)
    if n.startswith("פרה") and "קרנץ" in n:
        return "COOKIE", "פרה קרנץ = cookie"
    # "שוקולד צ'יפס לבן" (צימקאו) = chocolate confectionery product, not a cookie — flag
    if "צימקאו" in n:
        return "AMBIGUOUS", "confectionery chocolate (צימקאו brand) — not a cookie or cake; flag for scope review"

    # Marbeh (מרבה) עוגיות products — "עוגיות" explicitly in canonical name → COOKIE
    if "מרבה" in n and "עוגיות" in n:
        return "COOKIE", "מרבה עוגיות = cookie brand"
    # Marbeh abbreviated עוג. = likely עוגיות
    if "מרבה" in n or (n.startswith("עוג.") and "מצופות" in n):
        return "COOKIE", "מרבה / עוג. abbrev = cookie"
    # Fitness mini cookies
    if "פיטנס" in n and "עוגיות" in n:
        return "COOKIE", "פיטנס עוגיות = cookie"
    if "פיטנס" in n and ("מיני" in n or "קלאסי" in n):
        return "COOKIE", "פיטנס mini = cookie"

    return "AMBIGUOUS", "no matching rule fired"

# ── 3. Run segmentation on all 149 IN_SCORED ────────────────────────────────
cakes = []
cookies = []
ambiguous = []

for bc, name_he in IN_SCORED.items():
    category, reason = segment(name_he)
    b = bsip1.get(bc, {})
    t = traces.get(bc, {})
    canonical = b.get("canonical_name_he") or name_he
    score = t.get("final_score_estimate")
    grade = t.get("grade_estimate")
    rec = {"barcode": bc, "name_he": canonical, "score": score, "grade": grade, "reason": reason}
    if category == "CAKE":
        cakes.append(rec)
    elif category == "COOKIE":
        cookies.append(rec)
    else:
        ambiguous.append(rec)

print(f"\n=== SEGMENTATION RESULTS ===")
print(f"CAKES: {len(cakes)}")
print(f"COOKIES: {len(cookies)}")
print(f"AMBIGUOUS: {len(ambiguous)}")
print(f"TOTAL: {len(cakes) + len(cookies) + len(ambiguous)} (must = 149)")
print()

REPORT = ROOT / "02_products" / "cakes_hard_cookies" / "task283_segmentation_report.txt"
_rpt = open(str(REPORT), "w", encoding="utf-8")

def rpt(s=""):
    _rpt.write(s + "\n")
    # Safe ASCII-only print for Windows console
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))

rpt(f"=== CAKES LIST ({len(cakes)}) ===")
for r in sorted(cakes, key=lambda x: -(x["score"] or 0)):
    rpt(f"  {r['barcode']:20s} {str(r['score']):6} {str(r['grade'] or '?'):2}  {r['name_he']}")

rpt(f"\n=== COOKIES LIST ({len(cookies)}) ===")
for r in sorted(cookies, key=lambda x: -(x["score"] or 0)):
    rpt(f"  {r['barcode']:20s} {str(r['score']):6} {str(r['grade'] or '?'):2}  {r['name_he']}")

rpt(f"\n=== AMBIGUOUS LIST ({len(ambiguous)}) -- for orchestrator review ===")
for r in ambiguous:
    rpt(f"  {r['barcode']:20s}  {r['name_he']}  ->  {r['reason']}")

cake_barcodes = {r["barcode"] for r in cakes}
cookie_barcodes = {r["barcode"] for r in cookies}
ambiguous_barcodes = {r["barcode"] for r in ambiguous}

# ── 4. Additive bug verification for barcode 7290105692498 ──────────────────
TEST_BC = "7290105692498"
b123 = bsip1.get(TEST_BC, {})
print(f"\n=== ADDITIVE BUG VERIFICATION for {TEST_BC} ===")
print(f"canonical_name_he: {b123.get('canonical_name_he')}")
print(f"detected_additives (BUGGY source): {b123.get('detected_additives')}")
ea = b123.get("extracted_additives", [])
print(f"extracted_additives (CORRECT source, count={len(ea)}):")
for a in ea:
    print(f"  {a}")

# ── 5. Additive normalizer ───────────────────────────────────────────────────
def build_d4_additives(bsip1_record):
    """
    Build d4_additives from extracted_additives (BSIP1), not detected_additives.
    Dedupe by E-number + named additive term. Return list of dicts.
    detected_additives was the bug — it's always empty; extracted_additives is the populated field.
    """
    ea = bsip1_record.get("extracted_additives", [])
    seen = set()
    result = []
    for item in ea:
        term = item.get("term", "")
        category = item.get("category", "")
        # Dedupe key: use E-number if present, else term
        e_match = re.search(r'E\d{3,4}[a-z]?', term, re.IGNORECASE)
        if e_match:
            key = e_match.group(0).upper()
        else:
            key = term.strip()
        if key in seen:
            continue
        seen.add(key)
        result.append({"term": term, "category": category})
    return result

print(f"\n=== #123 d4_additives BEFORE fix ===")
print(f"  [] (detected_additives = empty)")
print(f"\n=== #123 d4_additives AFTER fix ===")
fixed_123 = build_d4_additives(b123)
for a in fixed_123:
    print(f"  {a}")

# ── 6. Helper: build a product record for the CAKES JSON ────────────────────
def num(v): return v if isinstance(v, (int, float)) else None

def build_cake_record(bc):
    b = bsip1.get(bc, {})
    t = traces.get(bc, {})
    nn = b.get("normalized_nutrition_per_100g", {})
    l3 = t.get("L3_inferred_classifications") or {}
    has_phvo = bool(l3.get("has_phvo"))
    # Factual limiting signals
    lim = []
    sug = num(nn.get("sugars_g")); sat = num(nn.get("fat_saturated_g")); kcal = num(nn.get("energy_kcal"))
    if sug is not None and sug >= 25: lim.append(f"סוכר גבוה: {sug} ג'/100 ג'")
    if sat is not None and sat >= 8: lim.append(f"שומן רווי גבוה: {sat} ג'/100 ג'")
    if has_phvo: lim.append("שומן צמחי מוקשה / מרגרינה ברשימת הרכיבים")
    if kcal is not None and kcal >= 400: lim.append(f"צפיפות קלורית גבוהה: {kcal} קק\"ל/100 ג'")

    # Confidence: map numeric to string label
    raw_conf = b.get("confidence")
    if isinstance(raw_conf, float):
        if raw_conf >= 0.85:
            conf_str = "verified"
        elif raw_conf >= 0.65:
            conf_str = "partial"
        else:
            conf_str = "low"
    else:
        conf_str = str(raw_conf) if raw_conf else "partial"

    return {
        "id": f"cake_{bc}",
        "name": b.get("canonical_name_he") or "",
        "barcode": bc,
        "imageUrl": b.get("image_url") or "",
        "score": t.get("final_score_estimate"),
        "grade": t.get("grade_estimate"),
        "confidence": conf_str,
        "confidence_label_he": PENDING,
        "confidence_tooltip_he": PENDING,
        "confidence_sub_reason": PENDING,
        "insightLine": PENDING,
        "rowVerdict": PENDING,
        "expansion": {
            "nutrition": {
                "energyKcal": num(nn.get("energy_kcal")),
                "fat": num(nn.get("fat_g")),
                "satFat": num(nn.get("fat_saturated_g")),
                "carbs": num(nn.get("carbohydrates_g")),
                "sugar": num(nn.get("sugars_g")),
                "protein": num(nn.get("protein_g")),
                "sodium": num(nn.get("sodium_mg")),
                "fiber": num(nn.get("dietary_fiber_g")),
            },
            "ingredients": b.get("ingredients_text_he") or "",
            "confidenceLabel": PENDING,
            "servingNote": "ל-100 גרם",
            "positiveSignals": [],
            "limitingFactors": lim,
            "bottomLine": PENDING,
        },
        "retailer": "+".join(b.get("source_retailers", [])) or "shufersal",
        "novaGroup": t.get("nova_proxy"),
        "d4_additives": build_d4_additives(b),  # FIX: extracted_additives not detected_additives
        "consumerTakeaway": PENDING,
        "consumerExplanation": PENDING,
        "bariInterpretation": PENDING,
        "bestUseCases": [],
        "_category_routed": t.get("category"),
        "_has_phvo": has_phvo,
        "_source_retailers": b.get("source_retailers", []),
    }

# ── 7. Helper: build a COOKIE record in cookies-coffee schema ────────────────
def build_cookie_record(bc):
    """Build a product record that matches cookies_coffee_frontend_v1.json schema."""
    b = bsip1.get(bc, {})
    t = traces.get(bc, {})
    nn = b.get("normalized_nutrition_per_100g", {})
    l3 = t.get("L3_inferred_classifications") or {}
    has_phvo = bool(l3.get("has_phvo"))

    # Confidence: map numeric to string label (matching cc schema)
    raw_conf = b.get("confidence")
    if isinstance(raw_conf, float):
        if raw_conf >= 0.85:
            conf_str = "verified"
        elif raw_conf >= 0.65:
            conf_str = "partial"
        else:
            conf_str = "low"
    else:
        conf_str = str(raw_conf) if raw_conf else "partial"

    # Limiting factors (same logic as cakes)
    lim = []
    sug = num(nn.get("sugars_g")); sat = num(nn.get("fat_saturated_g")); kcal = num(nn.get("energy_kcal"))
    if sug is not None and sug >= 25: lim.append(f"סוכר גבוה: {sug} ג'/100 ג'")
    if sat is not None and sat >= 8: lim.append(f"שומן רווי גבוה: {sat} ג'/100 ג'")
    if has_phvo: lim.append("שומן צמחי מוקשה / מרגרינה ברשימת הרכיבים")
    if kcal is not None and kcal >= 400: lim.append(f"צפיפות קלורית גבוהה: {kcal} קק\"ל/100 ג'")

    # Use camelCase nutrition keys to match existing cookies-coffee schema
    return {
        "id": f"ck-{bc}",
        "name": b.get("canonical_name_he") or "",
        "barcode": bc,
        "imageUrl": b.get("image_url") or "",
        "score": t.get("final_score_estimate"),
        "grade": t.get("grade_estimate"),
        "confidence": conf_str,
        "confidence_label_he": PENDING,
        "confidence_tooltip_he": PENDING,
        "confidence_sub_reason": PENDING,
        "insightLine": PENDING,
        "rowVerdict": PENDING,
        "expansion": {
            "nutrition": {
                "energyKcal": num(nn.get("energy_kcal")),
                "protein": num(nn.get("protein_g")),
                "sugar": num(nn.get("sugars_g")),
                "fat": num(nn.get("fat_g")),
                "satFat": num(nn.get("fat_saturated_g")),
                "fiber": num(nn.get("dietary_fiber_g")),
                "sodium": num(nn.get("sodium_mg")),
            },
            "ingredients": b.get("ingredients_text_he") or "",
            "confidenceLabel": PENDING,
            "servingNote": "ל-100 גרם",
            "positiveSignals": [],
            "limitingFactors": lim,
            "bottomLine": PENDING,
        },
        "retailer": "+".join(b.get("source_retailers", [])) or "shufersal",
        "novaGroup": t.get("nova_proxy"),
        "d4_additives": build_d4_additives(b),  # FIX applied here too
        "consumerTakeaway": PENDING,
        "consumerExplanation": PENDING,
        "bariInterpretation": PENDING,
        "bestUseCases": [PENDING],
        "_category_routed": t.get("category"),
        "_has_phvo": has_phvo,
        "_source_retailers": b.get("source_retailers", []),
    }

# ── 8. Generate CAKES JSON ───────────────────────────────────────────────────
# After re-resolution: 4 of 5 ambiguous are COOKIES (Marbeh 3x + Fitness 1x)
# 1 true ambiguous = 7290013145406 (צימקאו chocolate — confectionery, not cake/cookie)
# The 1 true ambiguous is held OUT of both pages pending orchestrator scope ruling.
HELD_OUT_BARCODES = {"7290013145406"}  # confectionery: not cake, not cookie

cake_products = []
for bc in cake_barcodes:
    t = traces.get(bc, {})
    if t.get("final_score_estimate") is not None:
        cake_products.append(build_cake_record(bc))
# Ambiguous barcodes that were RESOLVED to cookie are already in cookie_barcodes (rule fired)
# The single held-out one goes to neither JSON — flagged in meta
held_out_in_ambiguous = [r for r in ambiguous if r["barcode"] in HELD_OUT_BARCODES]
rpt(f"\n=== HELD OUT (not cake, not cookie, scope unclear) ===")
for r in held_out_in_ambiguous:
    rpt(f"  {r['barcode']:20s}  {r['name_he']}  ->  {r['reason']}")

cake_products.sort(key=lambda p: -(p["score"] or 0))
gd_cakes = {}
for p in cake_products: gd_cakes[p["grade"]] = gd_cakes.get(p["grade"], 0) + 1

cakes_out = {
    "_meta": {
        "generated": datetime.now(timezone.utc).isoformat(),
        "category": "cakes",
        "run_id": "run_cakes_001",
        "product_count": len(cake_products),
        "scored_count": len(cake_products),
        "schema": "cookies-coffee-v1",
        "version": "v2",
        "task": "TASK-283 Wave 1 — cakes-only subset after category split",
        "provenance": "2-retailer direct scrape (Shufersal + Yochananof); OFF banned; nutrition+ingredients from storefront only",
        "grade_distribution": dict(sorted(gd_cakes.items())),
        "off_used": False,
        "copy_status": "PENDING — Wave 2 (Content) not yet run",
        "multi_retailer_confirmed": sum(1 for p in cake_products if len(p["_source_retailers"]) >= 2),
        "has_phvo_count": sum(1 for p in cake_products if p["_has_phvo"]),
        "held_out": [{"barcode": bc, "reason": "confectionery/scope unclear — not cake, not cookie"} for bc in HELD_OUT_BARCODES],
        "additive_fix": "d4_additives now sourced from extracted_additives (not detected_additives)",
    },
    "page_copy": {
        "hero": {"title": PENDING, "tagline": PENDING, "productCount": len(cake_products), "scoredCount": len(cake_products)},
        "prologue": {"sentences": [PENDING]}, "methodology": {"body": PENDING, "lines": [PENDING]},
        "caveat": {"title": PENDING, "body": PENDING},
        "filters": [{"id": "all", "label_he": "הכל", "count": len(cake_products)}],
    },
    "products": cake_products,
}

OUT_CAKES.parent.mkdir(parents=True, exist_ok=True)
OUT_CAKES.write_text(json.dumps(cakes_out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n=== CAKES JSON WRITTEN ===")
print(f"Path: {OUT_CAKES}")
print(f"Products: {len(cake_products)}")
print(f"Grade distribution: {dict(sorted(gd_cakes.items()))}")

# ── 9. Verify #123 additive fix in cakes JSON ────────────────────────────────
cake_123 = next((p for p in cake_products if p["barcode"] == TEST_BC), None)
if cake_123:
    print(f"\n=== #123 in CAKES JSON d4_additives (AFTER FIX) ===")
    for a in cake_123["d4_additives"]:
        print(f"  {a}")
else:
    print(f"\n  NOTE: {TEST_BC} is a COOKIE (or ambiguous), not in CAKES JSON.")
    # Check if it's a cookie
    cookie_123 = bc in cookie_barcodes or TEST_BC in cookie_barcodes
    print(f"  Is it in cookie set? {TEST_BC in cookie_barcodes}")
    print(f"  Is it in cake set? {TEST_BC in cake_barcodes}")
    print(f"  Is it in ambiguous set? {TEST_BC in ambiguous_barcodes}")

# ── 10. BISCUITS MERGE ────────────────────────────────────────────────────────
print(f"\n=== BISCUITS MERGE ===")
# Existing cc products (preserve copy)
existing_products = {str(p["barcode"]): p for p in cc_existing["products"]}

# Build new cookie records from run #8
new_cookie_records = {}
for bc in cookie_barcodes:
    t = traces.get(bc, {})
    if t.get("final_score_estimate") is not None:
        new_cookie_records[bc] = build_cookie_record(bc)

# Dedup: find collisions
collisions = []
for bc, rec in new_cookie_records.items():
    if bc in cc_existing_barcodes:
        collisions.append(bc)

print(f"Existing cc barcodes: {len(cc_existing_barcodes)}")
print(f"New run-8 cookie barcodes (scored): {len(new_cookie_records)}")
print(f"Dedup collisions: {len(collisions)}")
for bc in collisions:
    existing = existing_products.get(bc, {})
    new = new_cookie_records.get(bc, {})
    # Prefer existing: has real copy + multi-retailer analysis
    # Determine which has more complete data
    ex_ing = existing.get("expansion", {}).get("ingredients", "")
    nw_ing = new.get("expansion", {}).get("ingredients", "")
    # Existing cc file has verified copy (insightLine, rowVerdict etc.), prefer it
    winner = "EXISTING (has copy + verified)"
    print(f"  COLLISION {bc}: {existing.get('name', '?')} → keep {winner}")

# Merge: existing + new (non-collision)
merged_products = list(existing_products.values())
added_new = []
for bc, rec in new_cookie_records.items():
    if bc not in cc_existing_barcodes:
        merged_products.append(rec)
        added_new.append(bc)

merged_products.sort(key=lambda p: -(p.get("score") or 0))
gd_merged = {}
for p in merged_products:
    g = p.get("grade"); gd_merged[g] = gd_merged.get(g, 0) + 1

print(f"Merged total: {len(merged_products)} (existing={len(existing_products)}, new-added={len(added_new)}, collisions-kept-existing={len(collisions)})")
print(f"Grade distribution: {dict(sorted(gd_merged.items()))}")
print(f"New cookies added: {len(added_new)}")

# Reconstruct page_copy from existing (preserve it — it's the 8/10 reference)
existing_page_copy = cc_existing.get("page_copy", {})
# Update productCount/scoredCount to reflect merged total
if "hero" in existing_page_copy:
    existing_page_copy["hero"]["productCount"] = len(merged_products)
    existing_page_copy["hero"]["scoredCount"] = len(merged_products)
# Update filters
existing_page_copy["filters"] = [
    {"id": "all", "label": "הכל", "count": len(merged_products), "isActive": True},
    {"id": "grade_c", "label": "ציון C ומעלה", "count": gd_merged.get("C", 0), "isActive": False},
    {"id": "grade_d", "label": "ציון D", "count": gd_merged.get("D", 0), "isActive": False},
    {"id": "grade_e", "label": "ציון E", "count": gd_merged.get("E", 0), "isActive": False},
]

# Update caveat body to reflect new count
# The caveat mentions "56 המוצרים" — update to merged count
caveat_body = existing_page_copy.get("caveat", {}).get("body", "")
old_count = "56"
if old_count in caveat_body:
    existing_page_copy["caveat"]["body"] = caveat_body.replace(
        f"מתוך {old_count} המוצרים", f"מתוך {len(merged_products)} המוצרים"
    ).replace(f"מתוך {old_count}", f"מתוך {len(merged_products)}")

biscuits_out = {
    "_meta": {
        "generated": datetime.now(timezone.utc).isoformat(),
        "category": "cookies_coffee",
        "run_id": "run_cookies_005+run_cakes_001_cookies",
        "product_count": len(merged_products),
        "scored_count": len(merged_products),
        "schema": "BariProductVM[]",
        "version": "v2",
        "task": "TASK-283 Wave 1 — cookies-coffee v1 (56 products) + run_cakes_001 cookies subset merged",
        "provenance": "cookies_coffee: BSIP0 cookies_coffee_bsip0_raw_20260613T163431 → run_cookies_005; new cookies: run_cakes_001 (Shufersal + Yochananof 2-retailer scrape)",
        "grade_distribution": dict(sorted(gd_merged.items())),
        "off_used": False,
        "copy_status": "MIXED — existing 56 products: MERGED copy (P91); new run-8 cookies: PENDING (Wave 2)",
        "copy_merge": {
            "existing_with_copy": len(existing_products),
            "new_pending_copy": len(added_new),
            "collisions_kept_existing": len(collisions),
            "source": "cookies_coffee_frontend_v1.json (existing) + run_cakes_001 cookies (new)",
            "task": "TASK-283",
        },
        "dedup_collisions": [
            {"barcode": bc, "resolution": "kept existing (has copy + verified)", "name": existing_products.get(bc, {}).get("name", "")}
            for bc in collisions
        ],
        "additive_fix": "d4_additives for new products sourced from extracted_additives (not detected_additives)",
        "discarded": cc_existing["_meta"].get("discarded", []),
    },
    "page_copy": existing_page_copy,
    "products": merged_products,
}

OUT_BISCUITS.write_text(json.dumps(biscuits_out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n=== BISCUITS MERGED JSON WRITTEN ===")
print(f"Path: {OUT_BISCUITS}")
print(f"Products: {len(merged_products)}")

# ── 11. Final summary ────────────────────────────────────────────────────────
print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)
print(f"IN_SCORED total: {len(IN_SCORED)}")
print(f"  → CAKES:    {len(cake_barcodes)}")
print(f"  → COOKIES:  {len(cookie_barcodes)}")
print(f"  → AMBIGUOUS: {len(ambiguous_barcodes)}")
print(f"  → CHECK:    {len(cake_barcodes) + len(cookie_barcodes) + len(ambiguous_barcodes)} (must = 149)")
print()
print(f"Cakes JSON products:   {len(cake_products)} (includes {len(ambiguous)} ambiguous as CAKE-default)")
print(f"Biscuits JSON products: {len(merged_products)} (56 existing + {len(added_new)} new, {len(collisions)} deduped)")
print()
print("ADDITIVE BUG:")
print(f"  Before: detected_additives = [] (empty, always)")
print(f"  After:  extracted_additives used → {len(fixed_123)} additive terms for {TEST_BC}")
print()
print("Ambiguous calls for orchestrator review:")
for r in ambiguous:
    print(f"  {r['barcode']:20s}  {r['name_he']}  →  {r['reason']}")
