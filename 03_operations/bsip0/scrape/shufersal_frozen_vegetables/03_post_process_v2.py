"""
Post-processing pass: re-extract nutrition panels with correct HTML structure,
clean scope, and produce enriched BSIP0 output v2.
"""
import sys, io, json, pathlib, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from bs4 import BeautifulSoup

BASE = pathlib.Path(r"C:\Bari")
SCRAPE_DIR = BASE / "03_operations" / "bsip0" / "scrape" / "shufersal_frozen_vegetables"
PRODUCT_DIR = SCRAPE_DIR / "product_pages"
INPUT_PATH = BASE / "02_products" / "frozen_vegetables" / "bsip0_outputs" / "bsip0_shufersal_frozen_vegetables_raw.json"
OUTPUT_PATH = BASE / "02_products" / "frozen_vegetables" / "bsip0_outputs" / "bsip0_shufersal_frozen_vegetables_v2.json"

d = json.loads(INPUT_PATH.read_text(encoding="utf-8"))

# ── Re-extract nutrition from raw HTML ──────────────────────────────
re_extracted = 0
re_extracted_all = 0
for p in d["products"]:
    html_path = p.get("raw_html_path")
    if not html_path:
        continue
    full_path = PRODUCT_DIR / pathlib.Path(html_path).name
    if not full_path.exists():
        continue

    html = full_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")

    nutrition = {}
    for item in soup.find_all("div", class_="nutritionItem"):
        num_el = item.find(class_="number")
        name_el = item.find(class_="name")
        text_el = item.find(class_="text")
        if num_el and text_el:
            value = num_el.get_text(strip=True)
            label_full = text_el.get_text(strip=True)
            unit = name_el.get_text(strip=True) if name_el else ""
            if value and label_full:
                if unit:
                    nutrition[label_full] = f"{value} {unit}"
                else:
                    nutrition[label_full] = value

    if nutrition:
        had_before = bool(p.get("nutrition_raw"))
        p["nutrition_raw"] = nutrition
        if not had_before:
            re_extracted += 1
        re_extracted_all += 1

print(f"Re-extracted nutrition: {re_extracted_all} products ({re_extracted} newly found)")

# ── Scope cleanup ──────────────────────────────────────────────────
NOT_FROZEN_PATTERNS = [
    "בדין",          # Badian flowers
    "זר ",           # bouquet
    "פרח",           # flower
    "גבעול",         # stem 
]

FRESH_PRODUCE_KEYWORDS = [
    "טרי", "אורגני", "חסה", "כוסברה", "בצל ירוק",
    "בצל", "בוקצ'וי", "בטטה", "תפוח אדמה", "שום",
]

SCOPE_OUT_PRODUCT_NAMES = [
    "בדין אקסטרה",
    "גמדי",  # baby vegetables
]

processed = []
scope_excluded_extra = {}

for p in d["products"]:
    name = (p.get("name_he") or "").lower()
    code = p["product_code"]
    
    excl = None
    
    # Check flowers
    for pat in NOT_FROZEN_PATTERNS:
        if pat in name:
            excl = f"not_food: {pat}"
            break
    
    # If no category membership in frozen veg categories, flag
    cat = p.get("category_raw") or ""
    in_frozen_cat = "A160501" in cat or "A1605" in cat
    has_frozen = "קפוא" in name or "מוקפא" in name or "frozen" in name
    
    # Fresh produce without frozen indicator and not in frozen category
    if not excl and not has_frozen and not in_frozen_cat:
        for kw in FRESH_PRODUCE_KEYWORDS:
            if kw in name:
                excl = f"not_frozen: fresh produce ({kw})"
                break
    
    if excl:
        scope_excluded_extra[code] = {"name": p.get("name_he"), "reason": excl}
    else:
        processed.append(p)

print(f"Final scope-IN: {len(processed)} (excluded extra: {len(scope_excluded_extra)})")

# ── Build enhanced output ──────────────────────────────────────────
bsip0 = {
    "schema_version": "bsip0_v1",
    "run_id": "shufersal_frozen_vegetables_scrape_002",
    "run_ts": d["run_ts"],
    "category": "frozen_vegetables",
    "retailer": "shufersal",
    "acquisition_method": "static_http_requests",
    "scrape_date": d["scrape_date"],
    "identity_source": "shufersal_search_html + category_html",
    "panel_source": "shufersal_product_page_html",
    "scope_notes": "Excluded: fresh flowers (Badian), fresh produce without frozen indicator and not in frozen category A160501/A1605.",
    "scrape_artifacts": {
        "search_pages": len(list(SCRAPE_DIR.glob("search_pages/*.html"))),
        "category_pages": len(list(SCRAPE_DIR.glob("category_pages/*.html"))),
        "product_pages": len(list(SCRAPE_DIR.glob("product_pages/*.html"))),
        "artifact_root": str(SCRAPE_DIR),
    },
    "product_count": len(processed),
    "scope_excluded_total": d.get("scope_excluded_count", 0) + len(scope_excluded_extra),
    "scope_excluded_initial": d.get("scope_excluded", {}),
    "scope_excluded_extra": scope_excluded_extra,
    "completeness": {
        "with_nutrition": sum(1 for p in processed if p.get("nutrition_raw")),
        "with_ingredients": sum(1 for p in processed if p.get("ingredients_raw")),
        "with_barcode_jsonld": sum(1 for p in processed if p.get("barcode_ld")),
        "with_image_url": sum(1 for p in processed if p.get("image_url") or p.get("image_url_jsonld")),
        "with_product_url": sum(1 for p in processed if p.get("product_url")),
        "with_raw_html": sum(1 for p in processed if p.get("raw_html_path")),
    },
    "provenance": d["provenance"],
    "products": processed,
}

OUTPUT_PATH.write_text(json.dumps(bsip0, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Enriched output: {OUTPUT_PATH}")
for k, v in bsip0["completeness"].items():
    print(f"  {k}: {v}/{len(processed)}")
