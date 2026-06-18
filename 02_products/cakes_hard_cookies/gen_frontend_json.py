"""
Generate cakes_hard_cookies_frontend_v1.json (factory run #8 / TASK-283).
Source: run_cakes_001 traces + run_cakes_001 BSIP1 + corpus_filter (2 retailers).
Copy fields = PENDING_COPY (filled in the supervised Content stage). All nutrition/
ingredient/signal values are REAL (trace + BSIP1); no fabrication, OFF banned.
Schema mirrors cookies_coffee_frontend_v1.json so the page components can consume it.
"""
import json, glob, pathlib, re
from datetime import datetime, timezone

ROOT = pathlib.Path(r"C:\Bari")
TRACE_DIR = ROOT/"02_products"/"cakes_hard_cookies"/"bsip2_outputs"/"run_cakes_001"/"products"
BSIP1_DIR = ROOT/"03_operations"/"bsip1"/"run_cakes_001"/"output"
CORPUS = ROOT/"02_products"/"cakes_hard_cookies"/"factory_run_001"/"corpus_filter.json"
OUT = ROOT/"bari-web"/"src"/"data"/"comparisons"/"cakes_hard_cookies_frontend_v1.json"
PENDING = "PENDING_COPY"

bsip1 = {}
for f in glob.glob(str(BSIP1_DIR/"bsip1_cakes_*.json")):
    d = json.load(open(f, encoding="utf-8"))
    bsip1[str(d["barcode"])] = d

# Only IN_SCORED barcodes belong on the page — ignore any stale traces (e.g. removed
# savory/out-of-scope items) that may linger in the trace dir from an earlier run.
_corpus = json.load(open(CORPUS, encoding="utf-8"))
IN_SCORED = {str(p["barcode"]) for p in _corpus["products"] if p["decision"] == "IN_SCORED"}

def num(v): return v if isinstance(v, (int, float)) else None

def _build_d4_additives(bsip1_record):
    """
    TASK-283 fix: populate d4_additives from extracted_additives, not detected_additives.
    detected_additives is always [] (empty) — a BSIP1 bug. extracted_additives is the
    populated field containing E-numbers and named additive terms parsed from ingredients.
    Dedupe by E-number (if present) or term string.
    """
    ea = bsip1_record.get("extracted_additives", [])
    seen = set()
    result = []
    for item in ea:
        term = item.get("term", "")
        e_match = re.search(r'E\d{3,4}[a-z]?', term, re.IGNORECASE)
        key = e_match.group(0).upper() if e_match else term.strip()
        if key in seen:
            continue
        seen.add(key)
        result.append({"term": term, "category": item.get("category", "")})
    return result

products = []
for f in glob.glob(str(TRACE_DIR/"*"/"bsip2_trace.json")) + glob.glob(str(TRACE_DIR/"bsip2_trace.json")):
    t = json.load(open(f, encoding="utf-8"))
    bc = str((t.get("input_reference") or {}).get("barcode") or t.get("barcode") or "")
    if bc not in IN_SCORED:
        continue
    b = bsip1.get(bc, {})
    nn = b.get("normalized_nutrition_per_100g", {})
    l3 = t.get("L3_inferred_classifications") or {}
    has_phvo = bool(l3.get("has_phvo"))
    # factual limiting signals (no interpretation — grounded in real values)
    lim = []
    sug = num(nn.get("sugars_g")); sat = num(nn.get("fat_saturated_g")); kcal = num(nn.get("energy_kcal"))
    if sug is not None and sug >= 25: lim.append(f"סוכר גבוה: {sug} ג'/100 ג'")
    if sat is not None and sat >= 8: lim.append(f"שומן רווי גבוה: {sat} ג'/100 ג'")
    if has_phvo: lim.append("שומן צמחי מוקשה / מרגרינה ברשימת הרכיבים")
    if kcal is not None and kcal >= 400: lim.append(f"צפיפות קלורית גבוהה: {kcal} קק\"ל/100 ג'")
    products.append({
        "id": f"cake_{bc}", "name": b.get("canonical_name_he") or "", "barcode": bc,
        "imageUrl": b.get("image_url") or "", "score": t.get("final_score_estimate"),
        "grade": t.get("grade_estimate"), "confidence": b.get("confidence"),
        "confidence_label_he": PENDING, "confidence_tooltip_he": PENDING, "confidence_sub_reason": PENDING,
        "insightLine": PENDING, "rowVerdict": PENDING,
        "expansion": {
            "nutrition": {k: num(nn.get(v)) for k, v in {
                "energy_kcal": "energy_kcal", "fat_g": "fat_g", "saturated_fat_g": "fat_saturated_g",
                "carbs_g": "carbohydrates_g", "sugar_g": "sugars_g", "protein_g": "protein_g",
                "sodium_mg": "sodium_mg", "fiber_g": "dietary_fiber_g"}.items()},
            "ingredients": b.get("ingredients_text_he") or "",
            "confidenceLabel": PENDING, "servingNote": PENDING,
            "positiveSignals": [], "limitingFactors": lim, "bottomLine": PENDING,
        },
        "retailer": "+".join(b.get("source_retailers", [])) or "shufersal",
        "novaGroup": t.get("nova_proxy"),
        # FIX (TASK-283): detected_additives is always empty (additive detection bug).
        # Use extracted_additives (the populated field) instead. Dedupe by E-number / term.
        "d4_additives": _build_d4_additives(b),
        "consumerTakeaway": PENDING, "consumerExplanation": PENDING,
        "bariInterpretation": PENDING, "bestUseCases": [],
        "_category_routed": t.get("category"), "_has_phvo": has_phvo,
        "_source_retailers": b.get("source_retailers", []),
    })

products = [p for p in products if p["score"] is not None]
products.sort(key=lambda p: -(p["score"] or 0))
gd = {}
for p in products: gd[p["grade"]] = gd.get(p["grade"], 0) + 1
corpus = json.load(open(CORPUS, encoding="utf-8"))

out = {
    "_meta": {
        "generated": datetime.now(timezone.utc).isoformat(), "category": "cakes-hard-cookies",
        "run_id": "run_cakes_001", "product_count": len(products), "scored_count": len(products),
        "schema": "milk-depth-v3", "version": "v1",
        "provenance": "2-retailer direct scrape (Shufersal + Yochananof); OFF banned; nutrition+ingredients from storefront only",
        "grade_distribution": dict(sorted(gd.items())), "off_used": False,
        "copy_status": "PENDING — Content stage not yet run (autonomous run #8 landed at data-complete)",
        "multi_retailer_confirmed": sum(1 for p in products if len(p["_source_retailers"]) >= 2),
        "has_phvo_count": sum(1 for p in products if p["_has_phvo"]),
        "transparency_null": corpus["counts"]["transparency_null"],
    },
    "page_copy": {
        "hero": {"title": PENDING, "tagline": PENDING, "productCount": len(products), "scoredCount": len(products)},
        "prologue": {"sentences": [PENDING]}, "methodology": {"body": PENDING},
        "caveat": {"title": PENDING, "body": PENDING},
        "filters": [{"id": "all", "label_he": "הכל", "count": len(products)}],
    },
    "products": products,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"WROTE {OUT}")
print(f"products={len(products)} grade_dist={dict(sorted(gd.items()))} "
      f"multi_retailer={out['_meta']['multi_retailer_confirmed']} has_phvo={out['_meta']['has_phvo_count']} off=False")
