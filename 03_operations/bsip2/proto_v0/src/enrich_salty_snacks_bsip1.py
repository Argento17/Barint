"""
BSIP1 enrichment for salty snacks corpus (TASK-213).
Reads the three BSIP0 retailer files, deduplicates by barcode (keep richest record),
assigns NOVA proxy, detects additives, assigns sub_pool, writes one bsip1_snack_*.json
per canonical product.
"""
import json, pathlib, datetime, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BSIP0_DIR   = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs")
OUT_DIR     = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")
DEDUP_REPORT= pathlib.Path(r"C:\Bari\02_products\salty_snacks\reports\dedup_report.json")
OUT_DIR.mkdir(parents=True, exist_ok=True)
DEDUP_REPORT.parent.mkdir(parents=True, exist_ok=True)

# ---- Sub-pool assignment (by subcategory_raw, name cues) ----
def assign_subpool(product: dict) -> str:
    sub = product.get("subcategory_raw", "").lower()
    name = product.get("name_he", "").lower()
    if sub == "popcorn" or "פופקורן" in name: return "popcorn"
    if sub == "puffed" or any(k in name for k in ["ביסלי", "במבה", "תירס", "גבינה"]): return "puffed"
    if sub == "rice_cakes" or any(k in name for k in ["אורז", "פצפוצי", "גלעינון", "שיפון"]): return "rice_cakes"
    if sub == "pretzels" or any(k in name for k in ["בייגל", "בייגלה", "פרצל"]): return "pretzels"
    if sub == "baked" or any(k in name for k in ["אפוי", "פיתות", "קרקר", "ביסקוצ'י",
                                                   "עדשים", "חומוס", "פייס", "קריספ"]): return "baked"
    if sub == "chips" or any(k in name for k in ["צ'יפס", "טייסטי", "תפוצ'יפס",
                                                   "פרינגלס", "דורטוס", "צ'יפסי",
                                                   "צ'יפסט"]): return "chips"
    return "chips"

# ---- NOVA proxy — ingredient-list based ----
# Additive E-number patterns and known UPF markers
NOVA4_ADDITIVE_PATTERNS = [
    r'\bE6\d\d\b',       # flavor enhancers (E621, E635 etc)
    r'\bE1\d\d\b',       # colorants
    r'\bE1[3-9]\d\b',    # more colorants
    r'\bE3[0-9][0-9]\b', # antioxidants/preservatives
    r'\bE4[0-9][0-9]\b', # emulsifiers
    r'\bE5[0-9][0-9]\b', # acidity regulators
    r'E150[a-d]',
    r'E160[a-z]',
    r'E172',
    r'E322',
    r'E330',
    r'E301',
    r'E300',
]
NOVA4_INGREDIENT_MARKERS = [
    "גלוקוז", "סירופ גלוקוז", "גלוקוז-פרוקטוז",
    "עמילן מטופל", "עמילן מורכב", "עמילן מכיל",
    "שומן צמחי מוקשה", "שומן הידרוגני", "הידרוגני",
    "לציטין", "תמצית", "תמצית עשן", "תמצית קרמל",
    "מחמצת", "שמרי בירה מיובשים"
]
NOVA3_MARKERS = ["מלח", "שמן", "סוכר", "שמרים"]

def infer_nova(ingredients: str, product: dict = None) -> tuple[int, float]:
    """Returns (nova_group, confidence).

    Salty snacks NOVA logic:
    - NOVA 4: any E-number additive; puffed/extruded subcategory; industrial flavor markers;
      palm oil + compound matrix (Bamba-style); caramel/glucose/hydrogenated fat.
    - NOVA 3: processed with salt/sugar/oil — baked goods with simple ingredient lists,
      plain pretzels. Wheat flour + oil + salt + yeast = NOVA 3.
    - NOVA 2: plain kettle chips (potato+oil+salt), plain popcorn (corn+oil+salt),
      plain rice cakes (rice+salt), rye crispbreads (rye flour+water+salt).
    - NOVA 1: single ingredient (rice only, corn only). Uncommon on retail shelf.
    """
    if not ingredients:
        return (4, 0.3)

    ing_lower = ingredients.lower()

    # Hard NOVA 4 signals: any E-number additive
    nova4_hits = 0
    for pat in NOVA4_ADDITIVE_PATTERNS:
        if re.search(pat, ingredients, re.IGNORECASE):
            nova4_hits += 1
    for marker in NOVA4_INGREDIENT_MARKERS:
        if marker in ing_lower:
            nova4_hits += 1

    if nova4_hits >= 2:
        return (4, 0.85)
    if nova4_hits == 1:
        return (4, 0.70)

    # Subcategory-based override: puffed/extruded products are industrial by nature
    # even with minimal additives — Bamba is NOVA 4 (extruded corn + industrial peanut butter)
    if product:
        sub = (product.get("subcategory_raw") or "").lower()
        name = (product.get("name_he") or "").lower()
        is_puffed = (sub == "puffed" or
                     any(k in name for k in ["ביסלי", "במבה", "ניבים", "גבינה"]))
        if is_puffed:
            # Even 4-ingredient extruded snacks are NOVA 4 due to industrial processing
            return (4, 0.80)

    # Palm oil is a strong NOVA 4 indicator in snack context
    if "שמן דקלים" in ing_lower:
        return (4, 0.75)

    # Count ingredients
    ing_parts = [p.strip() for p in re.split(r'[,،.]', ingredients) if p.strip()]
    ing_count = len(ing_parts)

    # Very short ingredient lists — possible NOVA 1-2
    if ing_count == 1:
        clean = ingredients.strip()
        if clean in ["אורז", "תירס", "חיטה"]:
            return (1, 0.9)

    # Simple 2-3 ingredient snacks: grain/veg + oil + salt (no palm oil, no E-numbers)
    # Plain kettle chips, plain popcorn, plain rice cakes, rye crispbread
    if ing_count <= 3 and "שמן דקלים" not in ing_lower:
        return (2, 0.75)

    # 4-6 ingredients with minimal processing: baked goods, plain pretzels
    if ing_count <= 6 and nova4_hits == 0 and "שמן דקלים" not in ing_lower:
        return (3, 0.65)

    # Default: NOVA 4 for anything else in salty snacks
    return (4, 0.7)


# ---- Additive detection ----
ADDITIVE_PATTERNS = {
    "flavor_enhancer": [r'E621', r'E635', r'E627', r'גלוטמט'],
    "colorant": [r'E1[0-9][0-9][a-z]?', r'E172', r'צבע מאכל', r'צבע\s*E'],
    "emulsifier": [r'E322', r'E471', r'לציטין'],
    "preservative": [r'E3[02][0-9]', r'E211', r'E202', r'חומר מעכב'],
    "acidity_regulator": [r'E330', r'E300', r'E301', r'חומצה ציטרית'],
}

def detect_additives(ingredients: str) -> dict:
    cats = []
    for cat, patterns in ADDITIVE_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, ingredients, re.IGNORECASE):
                cats.append(cat)
                break
    return {"additive_categories": list(set(cats)), "additive_count": len(set(cats))}


# ---- Main dedup + enrichment ----
all_records: list[dict] = []
retailer_files = list(BSIP0_DIR.glob("salty_snacks_bsip0_*.json"))
print(f"Loading BSIP0 files: {[f.name for f in retailer_files]}")

for f in retailer_files:
    records = json.loads(f.read_text("utf-8"))
    all_records.extend(records)

print(f"Total raw records: {len(all_records)}")

# Dedup by barcode — keep record with most fields populated
by_barcode: dict[str, dict] = {}
by_barcode_retailers: dict[str, list] = {}

for rec in all_records:
    bc = str(rec.get("barcode", ""))
    if not bc:
        continue
    retailer = rec.get("retailer_id", "unknown")
    by_barcode_retailers.setdefault(bc, [])
    if retailer not in by_barcode_retailers[bc]:
        by_barcode_retailers[bc].append(retailer)

    if bc not in by_barcode:
        by_barcode[bc] = rec
    else:
        existing = by_barcode[bc]
        # Prefer record with more ingredient text
        existing_ing = existing.get("ingredients_he", "") or ""
        new_ing = rec.get("ingredients_he", "") or ""
        if len(new_ing) > len(existing_ing):
            # Preserve retailers list from existing
            by_barcode[bc] = rec

dedup_count = len(by_barcode)
dup_removed = len(all_records) - dedup_count
print(f"After dedup: {dedup_count} unique products ({dup_removed} duplicates removed)")

# Write canonical BSIP1 records
written = []
for barcode, rec in by_barcode.items():
    retailers = by_barcode_retailers.get(barcode, [rec.get("retailer_id", "unknown")])
    pid = f"bsip1_snack_{barcode}"
    ingredients = rec.get("ingredients_he", "") or ""
    nova_group, nova_conf = infer_nova(ingredients, rec)
    additives = detect_additives(ingredients)
    sub_pool = assign_subpool(rec)
    nutr = rec.get("nutrition", {})

    # Ingredient count
    ing_parts = [p.strip() for p in re.split(r'[,،.]', ingredients) if p.strip() and len(p.strip()) > 1]
    ing_count = len(ing_parts)

    canonical = {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": rec.get("name_he", ""),
        "canonical_name_en": rec.get("name_en") or None,
        "brand": rec.get("brand", ""),
        "package_size_g": rec.get("weight_g"),
        "source_retailers": retailers,
        "sub_pool": sub_pool,
        "category": "salty_snack",
        "image_url": rec.get("image_url", ""),
        "image_urls": [rec["image_url"]] if rec.get("image_url") else [],
        "price_ils": rec.get("price_ils"),
        "normalized_nutrition_per_100g": {
            "energy_kcal": nutr.get("energy_kcal"),
            "fat_g": nutr.get("fat_g"),
            "fat_saturated_g": nutr.get("saturated_fat_g"),
            "fat_trans_g": None,
            "sodium_mg": nutr.get("sodium_mg"),
            "carbohydrates_g": nutr.get("carbs_g"),
            "sugars_g": nutr.get("sugar_g"),
            "dietary_fiber_g": nutr.get("fiber_g"),
            "protein_g": nutr.get("protein_g"),
        },
        "ingredients_text_he": ingredients,
        "ingredients_list": ing_parts,
        "ingredients_raw": ingredients,
        "ingredient_count": ing_count,
        "claims_raw": ", ".join(rec.get("claims", [])),
        "claims": rec.get("claims", []),
        "nova_proxy": nova_group,
        "nova_confidence": nova_conf,
        "additive_categories": additives["additive_categories"],
        "additive_count": additives["additive_count"],
        "allergens_contains": [],
        "allergens_may_contain": [],
        "data_sufficiency": "sufficient" if nutr.get("energy_kcal") and ingredients else "partial",
        "nutrition_basis_claimed": "ל-100 גרם",
        "nutrition_basis_detected": "per_100g",
        "nutrition_consistency_status": "consistent",
        "ingredient_text_quality": "clean" if ingredients else "missing",
        "canonical_trust_score": 0.8 if ingredients else 0.6,
        "canonical_trust_level": "high" if ingredients else "medium",
        "canonical_risk_flags": ["off_candidate_panel"] if not ingredients else [],
        "confidence": {
            "identity_confidence": "high",
            "barcode_confidence": "confirmed",
            "nutrition_confidence": "confirmed_per_100g",
            "matched_by": "retailer_catalog_direct",
            "observation_count": len(retailers),
        },
        "conflicts_summary": [],
        "missing_fields": [] if nutr.get("energy_kcal") and ingredients else ["ingredients_text_he"],
        "inferred_fields": ["nova_proxy"] if ingredients else ["nova_proxy", "ingredient_count"],
        "audit_ref": None,
        "enrichment_run_id": "run_salty_snacks_bsip1_001",
        "enriched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    out_path = OUT_DIR / f"bsip1_snack_{barcode}.json"
    out_path.write_text(json.dumps(canonical, ensure_ascii=False, indent=2), encoding="utf-8")
    written.append({"barcode": barcode, "pid": pid, "name": rec.get("name_he"), "sub_pool": sub_pool, "nova": nova_group})

# Dedup report
nova_dist = {}
subpool_dist = {}
for w in written:
    nova_dist[str(w["nova"])] = nova_dist.get(str(w["nova"]), 0) + 1
    subpool_dist[w["sub_pool"]] = subpool_dist.get(w["sub_pool"], 0) + 1

dedup_report = {
    "run_id": "run_salty_snacks_bsip1_001",
    "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "raw_records": len(all_records),
    "unique_products": dedup_count,
    "duplicates_removed": dup_removed,
    "nova_distribution": nova_dist,
    "subpool_distribution": subpool_dist,
    "products": written,
}
DEDUP_REPORT.write_text(json.dumps(dedup_report, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Written {len(written)} canonical BSIP1 records to {OUT_DIR}")
print(f"NOVA distribution: {nova_dist}")
print(f"Sub-pool distribution: {subpool_dist}")
print(f"Dedup report: {DEDUP_REPORT}")
