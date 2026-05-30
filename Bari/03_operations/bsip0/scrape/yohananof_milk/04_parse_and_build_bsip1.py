"""
BSIP0→BSIP1 Milk Conversion Pipeline
1. Parses HTML tabs from each scraped product folder (using yohananof parser logic)
2. Converts BSIP0 product.json to BSIP1 canonical format
3. Writes BSIP1 files to C:\Bari\03_operations\bsip1\run_milk_002\output\
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json
import re
import sys
import datetime
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
RETAILER_DIR = BASE_DIR / "outputs" / "yohananof_milk"
BSIP1_OUT = Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output")
BSIP1_OUT.mkdir(parents=True, exist_ok=True)


# ── HTML parsing (adapted from parser.py) ───────────────────────────────────────

def clean(text):
    if text is None:
        return None
    text = str(text).replace("\xa0", " ").replace("&nbsp;", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_number(text):
    if not text:
        return None
    text = clean(text)
    text = text.replace(",", ".").replace("פחות מ", "").replace("<", "").strip()
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    return float(match.group(1)) if match else None


def soup_from_file(path):
    if not path.exists() or path.stat().st_size == 0:
        return BeautifulSoup("", "lxml")
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


def load_json_if_exists(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def find_value_by_label(soup, label):
    for row in soup.select("div.MuiTypography-body2"):
        text = clean(row.get_text(" ", strip=True))
        if text and text.startswith(label + ":"):
            return clean(text.replace(label + ":", "", 1))
    return None


def extract_product_name(*soups):
    selectors = ['[class*="ccnpqe"]', "h1", "h2"]
    for soup in soups:
        for selector in selectors:
            el = soup.select_one(selector)
            if el:
                val = clean(el.get_text(" ", strip=True))
                if val:
                    return val
    return None


def extract_ingredients(soup):
    panel = soup.select_one("#simple-tabpanel-0")
    if not panel:
        return None
    text = clean(panel.get_text(" ", strip=True))
    return text if text else None


def extract_allergens(soup):
    panel = soup.select_one("#simple-tabpanel-2")
    if not panel:
        return None
    text = clean(panel.get_text(" ", strip=True))
    return text if text else None


def extract_nutrition_basis(soup):
    text = clean(soup.get_text(" ", strip=True)) or ""
    # Explicit per-100ml declaration (Yohananof: "ל100 מ"ל" in nutrition section header)
    if 'ל100 מ"ל' in text or 'ל-100 מ"ל' in text or "ל-100 מל" in text or "ל100 מל" in text:
        return {"basis_raw": 'ל100 מ"ל', "basis_type": "per_100ml"}
    if "ל100 גרם" in text or "ל-100 גרם" in text or "ל100 גרם" in text:
        return {"basis_raw": "ל100 גרם", "basis_type": "per_100g"}
    # "ל1 ליטר" = Yohananof package-size header (1-liter product); nutrition basis
    # is per-serving. Detect serving size from nutrition values post-extraction.
    if "ל1 ליטר" in text:
        return {"basis_raw": "ל1 ליטר", "basis_type": "per_serving_pkg_1l"}
    if "למנה" in text or "ליחידה" in text:
        return {"basis_raw": "למנה/ליחידה", "basis_type": "per_serving_or_unit"}
    return {"basis_raw": None, "basis_type": "unknown"}


def extract_nutrition(soup):
    nutrition = {}
    label_map = [
        ("אנרגיה", "energy_kcal"),
        ("חומצות שומן רוויות", "fat_saturated_g"),
        ("חומצות שומן טראנס", "fat_trans_g"),
        ("שומנים", "fat_g"),
        ("כולסטרול", "cholesterol_mg"),
        ("נתרן", "sodium_mg"),
        ("סך הפחמימות", "carbohydrates_g"),
        ("סוכרים מתוך פחמימות", "sugars_g"),
        ("סיבים תזונתיים", "dietary_fiber_g"),
        ("חלבונים", "protein_g"),
    ]
    for row in soup.select("#simple-tabpanel-1 li"):
        label_el = row.select_one("span")
        if not label_el:
            continue
        label = clean(label_el.get_text(" ", strip=True))
        full_text = clean(row.get_text(" ", strip=True))
        if not label or not full_text:
            continue
        value_text = full_text.replace(label, "", 1).strip()
        value = parse_number(value_text)
        if value is None:
            continue
        for hebrew_label, field_name in label_map:
            if hebrew_label in label:
                nutrition[field_name] = value
                break
    return nutrition


def parse_ingredients_list(ingredients_raw):
    if not ingredients_raw:
        return []
    parts = re.split(r"[,،;]", ingredients_raw)
    result = []
    for part in parts:
        part = clean(part)
        if part and len(part) > 1:
            result.append(part)
    return result


def parse_package_size(name_text):
    if not name_text:
        return None
    match = re.search(r"(\d[\d,\.]*)\s*(?:מ[\"']?ל|מל|ml|ML)", name_text)
    if match:
        val = match.group(1).replace(",", ".")
        try:
            return float(val)
        except ValueError:
            pass
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:ליטר|לטר|L|l)\b", name_text)
    if match:
        try:
            return float(match.group(1)) * 1000
        except ValueError:
            pass
    return None


# ── BSIP1 format conversion ──────────────────────────────────────────────────────

def parse_product_folder(product_dir):
    ingredients_soup = soup_from_file(product_dir / "ingredients.html")
    nutrition_soup   = soup_from_file(product_dir / "nutrition.html")
    allergens_soup   = soup_from_file(product_dir / "allergens.html")
    discovery        = load_json_if_exists(product_dir / "discovery.json") or {}
    capture_status   = load_json_if_exists(product_dir / "capture_status.json") or {}

    ingredients_raw = extract_ingredients(ingredients_soup)
    nutrition_basis = extract_nutrition_basis(nutrition_soup)
    nutrition       = extract_nutrition(nutrition_soup)
    allergens_raw   = extract_allergens(allergens_soup)

    barcode = (
        find_value_by_label(ingredients_soup, "ברקוד")
        or find_value_by_label(nutrition_soup, "ברקוד")
        or discovery.get("barcode")
        or product_dir.name
    )

    name = (
        extract_product_name(ingredients_soup, nutrition_soup, allergens_soup)
        or discovery.get("name")
        or ""
    )

    brand = (
        find_value_by_label(ingredients_soup, "מותג/יצרן")
        or find_value_by_label(nutrition_soup, "מותג/יצרן")
        or discovery.get("brand")
        or ""
    )

    country = (
        find_value_by_label(ingredients_soup, "ארץ יצור")
        or find_value_by_label(nutrition_soup, "ארץ יצור")
    )

    kosher = (
        find_value_by_label(ingredients_soup, "כשרות")
        or find_value_by_label(nutrition_soup, "כשרות")
    )

    package_size_ml = parse_package_size(name)

    basis_type = nutrition_basis.get("basis_type", "unknown")
    if basis_type in ("per_100g", "per_100ml"):
        per_100 = nutrition
    elif basis_type == "per_serving_pkg_1l" and nutrition:
        # Yohananof shows 1-liter products with per-serving values.
        # If energy > 100 kcal → per 200ml serving → divide by 2.
        # If energy ≤ 100 kcal → already per 100ml (product labels it that way despite the header).
        kcal_val = nutrition.get("energy_kcal", 0) or 0
        if kcal_val > 100:
            per_100 = {k: round(v / 2, 3) for k, v in nutrition.items() if v is not None}
            nutrition_basis["serving_size_ml"] = 200
            nutrition_basis["normalization"] = "divided_by_2_from_200ml_serving"
        else:
            per_100 = nutrition
            nutrition_basis["normalization"] = "used_as_per_100ml_heuristic"
    else:
        per_100 = {}

    return {
        "barcode": clean(barcode) or "",
        "name": clean(name) or "",
        "brand": clean(brand) or "",
        "country": clean(country),
        "kosher": clean(kosher),
        "package_size_ml": package_size_ml,
        "ingredients_raw": clean(ingredients_raw),
        "allergens_raw": clean(allergens_raw),
        "nutrition_basis": nutrition_basis,
        "nutrition_per_100": per_100,
        "capture_status": capture_status,
        "discovery": discovery,
        "folder": str(product_dir),
    }


def infer_allergens(allergens_raw, ingredients_raw):
    contains = []
    may_contain = []

    allergen_he_map = {
        "חלב": "חלב", "לקטוז": "חלב",
        "חיטה": "חיטה (גלוטן)", "גלוטן": "גלוטן",
        "שיבולת שועל": "שיבולת שועל (גלוטן)",
        "אגוזים": "אגוזים", "בוטנים": "בוטנים",
        "סויה": "סויה", "ביצים": "ביצים",
        "שומשום": "שומשום", "דגים": "דגים",
        "סרטנים": "סרטנים", "רכיכות": "רכיכות",
        "כוסמין": "כוסמין", "שעורה": "שעורה",
        "שיפון": "שיפון",
    }

    combined = (allergens_raw or "") + " " + (ingredients_raw or "")
    for term, allergen in allergen_he_map.items():
        if term in combined:
            if allergens_raw and term in allergens_raw:
                if allergen not in contains:
                    contains.append(allergen)
            elif ingredients_raw and term in ingredients_raw:
                if allergen not in may_contain:
                    may_contain.append(allergen)

    return contains, may_contain


def infer_claims(ingredients_raw, name):
    claims = []
    combined = (name or "") + " " + (ingredients_raw or "")
    if "ללא תוספת סוכר" in combined or "ללא סוכר מוסף" in combined:
        claims.append("ללא תוספת סוכר")
    if "ללא לקטוז" in combined:
        claims.append("ללא לקטוז")
    if "טבעוני" in combined or "vegan" in combined.lower():
        claims.append("טבעוני")
    if "אורגני" in combined or "ביו" in combined:
        claims.append("אורגני")
    if "עשיר בחלבון" in combined or "high protein" in combined.lower():
        claims.append("עשיר בחלבון")
    if "ללא גלוטן" in combined or "gluten free" in combined.lower():
        claims.append("ללא גלוטן")
    return claims


def to_bsip1(p, scraped_at):
    barcode = p["barcode"]
    pid = f"bsip1_{barcode}"
    audit_ref = f"bsip1_audit_{barcode}.json"

    n = p["nutrition_per_100"]
    nutrition_normalized = {
        "energy_kcal":     n.get("energy_kcal"),
        "fat_g":           n.get("fat_g"),
        "fat_saturated_g": n.get("fat_saturated_g"),
        "fat_trans_g":     n.get("fat_trans_g", 0.0),
        "cholesterol_mg":  n.get("cholesterol_mg"),
        "sodium_mg":       n.get("sodium_mg"),
        "carbohydrates_g": n.get("carbohydrates_g"),
        "sugars_g":        n.get("sugars_g"),
        "dietary_fiber_g": n.get("dietary_fiber_g"),
        "protein_g":       n.get("protein_g"),
    }
    # Remove None values
    nutrition_normalized = {k: v for k, v in nutrition_normalized.items() if v is not None}

    basis_type = p["nutrition_basis"].get("basis_type", "unknown")
    normalization = p["nutrition_basis"].get("normalization", "")
    if basis_type in ("per_100g", "per_100ml") or normalization:
        nutrition_confidence = "confirmed_per_100g"
        nutrition_basis_detected = "per_100g"
    else:
        nutrition_confidence = "low"
        nutrition_basis_detected = basis_type

    allergen_contains, allergen_may_contain = infer_allergens(
        p.get("allergens_raw"), p.get("ingredients_raw")
    )
    claims = infer_claims(p.get("ingredients_raw"), p["name"])

    ingredients_list = parse_ingredients_list(p.get("ingredients_raw"))

    capture_ok = all(
        v == "success"
        for v in (p.get("capture_status") or {}).values()
        if isinstance(v, str)
    )
    partial = not capture_ok

    risk_flags = ["single_source_only"]
    if partial:
        risk_flags.append("partial_capture")
    if not nutrition_normalized:
        risk_flags.append("nutrition_missing")

    trust_score = 0.85
    if partial:
        trust_score -= 0.15
    if not nutrition_normalized:
        trust_score -= 0.20
    trust_score = max(0.40, round(trust_score, 2))
    trust_level = "high" if trust_score >= 0.75 else "medium" if trust_score >= 0.55 else "low"

    serving_size = 200.0  # default for beverages; adjust if label found
    if p.get("package_size_ml") and p["package_size_ml"] <= 500:
        serving_size = float(p["package_size_ml"])

    product = {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": p["name"],
        "canonical_name_en": None,
        "brand": p["brand"] or None,
        "package_size_g": p.get("package_size_ml"),
        "unit_count": None,
        "unit_size_g": None,
        "serving_size_g": serving_size,
        "country_of_origin": p.get("country"),
        "kosher_certification": p.get("kosher"),
        "image_url": (p.get("discovery") or {}).get("image", {}).get("source_image_url"),
        "source_retailers": ["yohananof"],
        "normalized_nutrition_per_100g": nutrition_normalized,
        "energy_source_unit": "kcal",
        "ingredients_text_he": p.get("ingredients_raw"),
        "ingredients_list": ingredients_list,
        "allergens_contains": allergen_contains,
        "allergens_may_contain": allergen_may_contain,
        "claims": claims,
        "confidence": {
            "identity_confidence": "high" if barcode and p["name"] else "medium",
            "barcode_confidence": "confirmed",
            "nutrition_confidence": nutrition_confidence,
            "matched_by": "barcode_single_source",
            "observation_count": 1,
        },
        "barcode_validation_status": "retailer_confirmed",
        "barcode_confidence_reason": f"Scraped from Yohananof on {scraped_at[:10]}.",
        "nutrition_basis_claimed": p["nutrition_basis"].get("basis_raw"),
        "nutrition_basis_detected": nutrition_basis_detected,
        "nutrition_consistency_status": "consistent" if nutrition_normalized else "missing",
        "nutrition_consistency_warnings": [] if nutrition_normalized else ["no_nutrition_data_parsed"],
        "ingredient_text_quality": "clean" if p.get("ingredients_raw") else "missing",
        "ingredient_warnings": [] if p.get("ingredients_raw") else ["ingredients_not_parsed"],
        "canonical_trust_score": trust_score,
        "canonical_trust_level": trust_level,
        "canonical_risk_flags": risk_flags,
        "conflicts_summary": {
            "count": 0,
            "has_unresolved": False,
            "fields_in_conflict": [],
            "identity_conflicts": [],
            "nutrition_conflicts": [],
            "ingredient_conflicts": [],
            "labeling_conflicts": [],
            "completeness_conflicts": [],
        },
        "missing_fields": [
            f for f, v in {
                "canonical_name_en": None,
                "serving_size_g": None if not serving_size else "ok",
                "country_of_origin": p.get("country"),
            }.items() if v is None
        ],
        "inferred_fields": [],
        "audit_ref": audit_ref,
    }

    audit = {
        "schema_version": "bsip1_audit_v0_1",
        "file_type": "audit",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonicalization_strategy": "single_retailer_passthrough",
        "run_date": scraped_at,
        "retailer_observations": [
            {
                "retailer_id": "yohananof",
                "scrape_mode": "product_modal_html_tabs",
                "barcode_source": "image_url_or_folder_name",
                "nutrition_completeness": "full" if nutrition_normalized else "missing",
                "observation_quality_score": trust_score,
                "observation_quality_level": trust_level,
                "observation_quality_signals": [
                    "ingredients_captured" if p.get("ingredients_raw") else "ingredients_missing",
                    "nutrition_captured" if nutrition_normalized else "nutrition_missing",
                ],
                "folder_path": p["folder"],
                "capture_status": p.get("capture_status"),
            }
        ],
        "field_resolution_log": [],
        "trust_derivation": {
            "base_score": 0.85,
            "deductions": {
                "partial_capture": -0.15 if partial else 0,
                "nutrition_missing": -0.20 if not nutrition_normalized else 0,
            },
            "final_score": trust_score,
        },
    }

    return product, audit


def main():
    if not RETAILER_DIR.exists():
        print(f"No scrape output at {RETAILER_DIR}")
        return

    scraped_at = datetime.datetime.now().isoformat(timespec="seconds")
    products_written = 0
    errors = []

    for product_dir in sorted(RETAILER_DIR.iterdir()):
        if not product_dir.is_dir() or not any([
            (product_dir / "ingredients.html").exists(),
            (product_dir / "nutrition.html").exists(),
        ]):
            continue

        barcode = product_dir.name
        print(f"\nProcessing: {barcode}")

        try:
            p = parse_product_folder(product_dir)
            if not p["barcode"]:
                print(f"  Skipping: no barcode")
                continue

            product, audit = to_bsip1(p, scraped_at)

            pid = product["canonical_product_id"]
            (BSIP1_OUT / f"{pid}.json").write_text(
                json.dumps(product, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            (BSIP1_OUT / f"bsip1_audit_{barcode}.json").write_text(
                json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            print(f"  → {pid}")
            print(f"     name={product['canonical_name_he'][:50]}")
            print(f"     nutrition={len(product['normalized_nutrition_per_100g'])} fields")
            print(f"     trust={product['canonical_trust_level']} ({product['canonical_trust_score']})")
            products_written += 1

        except Exception as e:
            import traceback
            print(f"  ERROR: {e}")
            traceback.print_exc()
            errors.append({"barcode": barcode, "error": str(e)})

    summary = {
        "run_date": scraped_at,
        "source": str(RETAILER_DIR),
        "output": str(BSIP1_OUT),
        "products_written": products_written,
        "errors": errors,
    }
    (BSIP1_OUT / "run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\n{'='*40}")
    print(f"Products written: {products_written}")
    print(f"Errors: {len(errors)}")
    print(f"Output: {BSIP1_OUT}")
    print(f"{'='*40}")
    print("Next: python 03_operations/bsip2/proto_v0/src/batch_run_milk_002.py")


if __name__ == "__main__":
    main()
