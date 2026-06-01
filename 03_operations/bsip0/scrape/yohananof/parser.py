from pathlib import Path
import json
import re
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
RETAILER = "yohananof"
RETAILER_DIR = OUTPUT_DIR / RETAILER


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
    text = text.replace(",", ".")
    text = text.replace("L ", "")
    text = text.replace("<", "")
    text = text.replace("פחות מ", "")
    text = text.strip()

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
    rows = soup.select("div.MuiTypography-body2")
    for row in rows:
        text = clean(row.get_text(" ", strip=True))
        if text and text.startswith(label + ":"):
            return clean(text.replace(label + ":", "", 1))
    return None


def first_value_by_label(label, *soups):
    for soup in soups:
        value = find_value_by_label(soup, label)
        if value:
            return value
    return None


def extract_product_name(*soups):
    selectors = ['[class*="ccnpqe"]', "h1", "h2"]
    for soup in soups:
        for selector in selectors:
            el = soup.select_one(selector)
            if el:
                value = clean(el.get_text(" ", strip=True))
                if value:
                    return value
    return None


def extract_image_url(*soups):
    for soup in soups:
        el = soup.select_one('img[src*="729"], img[srcset*="729"]')
        if el:
            return el.get("src") or el.get("srcset")
    return None


def extract_breadcrumbs(*soups):
    for soup in soups:
        breadcrumbs = [
            clean(a.get_text(" ", strip=True))
            for a in soup.select("nav a")
            if clean(a.get_text(" ", strip=True))
        ]
        if breadcrumbs:
            return breadcrumbs
    return []


def extract_pricing(*soups):
    for soup in soups:
        all_text = soup.get_text(" ", strip=True)
        if not all_text:
            continue

        price_el = soup.select_one('[data-aria-desc="final_price"]')
        price_text = clean(price_el.get_text(" ", strip=True)) if price_el else None

        unit_price = None
        unit_match = re.search(r"‏?(\d+(?:\.\d+)?)\s*‏?₪\s*/\s*100 גרם", all_text)
        if unit_match:
            unit_price = float(unit_match.group(1))

        promo_text = None
        promo_match = re.search(r"(\d+\s*יח['׳]?\s*ב-\s*‏?\d+(?:\.\d+)?\s*₪)", all_text)
        if promo_match:
            promo_text = clean(promo_match.group(1))

        promo_expiry = None
        expiry_match = re.search(r"המבצע בתוקף עד לתאריך\s*([0-9.]+)", all_text)
        if expiry_match:
            promo_expiry = clean(expiry_match.group(1)).rstrip(".")

        return {
            "current_price_ils": parse_number(price_text),
            "current_price_text": price_text,
            "price_per_100g_ils": unit_price,
            "promotion_text": promo_text,
            "promotion_expiry": promo_expiry,
        }

    return {
        "current_price_ils": None,
        "current_price_text": None,
        "price_per_100g_ils": None,
        "promotion_text": None,
        "promotion_expiry": None,
    }


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

    if "ל-100 גרם" in text or "100 גרם" in text:
        return {
            "basis_raw": "ל-100 גרם",
            "basis_type": "per_100g"
        }

    if "ל-100 מ״ל" in text or "ל-100 מל" in text or "100 מ״ל" in text or "100 מל" in text:
        return {
            "basis_raw": "ל-100 מ״ל",
            "basis_type": "per_100ml"
        }

    if "למנה" in text or "ליחידה" in text:
        return {
            "basis_raw": "למנה/ליחידה",
            "basis_type": "per_serving_or_unit"
        }

    return {
        "basis_raw": None,
        "basis_type": "unknown"
    }


def extract_nutrition(soup):
    nutrition = {}

    label_map = [
        ("אנרגיה", "energy_kcal_100g"),
        ("חומצות שומן רוויות", "saturated_fat_g_100g"),
        ("חומצות שומן טראנס", "trans_fat_g_100g"),
        ("שומנים", "fat_g_100g"),
        ("כולסטרול", "cholesterol_mg_100g"),
        ("נתרן", "sodium_mg_100g"),
        ("סך הפחמימות", "carbohydrates_g_100g"),
        ("סוכרים מתוך פחמימות", "sugars_g_100g"),
        ("מתוכן כפיות סוכר", "sugar_teaspoons_100g"),
        ("סיבים תזונתיים", "fiber_g_100g"),
        ("חלבונים", "protein_g_100g"),
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


def parse_product_folder(product_dir):
    ingredients_html = product_dir / "ingredients.html"
    nutrition_html = product_dir / "nutrition.html"
    allergens_html = product_dir / "allergens.html"
    output_json = product_dir / "product.json"

    if not any(path.exists() for path in [ingredients_html, nutrition_html, allergens_html]):
        return None

    ingredients_soup = soup_from_file(ingredients_html)
    nutrition_soup = soup_from_file(nutrition_html)
    allergens_soup = soup_from_file(allergens_html)

    discovery = load_json_if_exists(product_dir / "discovery.json") or {}
    capture_status = load_json_if_exists(product_dir / "capture_status.json") or {}
    image_info = discovery.get("image") or {}

    ingredients_raw = extract_ingredients(ingredients_soup)
    nutrition_basis = extract_nutrition_basis(nutrition_soup)
    nutrition = extract_nutrition(nutrition_soup)
    allergens_raw = extract_allergens(allergens_soup)

    barcode = (
        first_value_by_label("ברקוד", ingredients_soup, nutrition_soup, allergens_soup)
        or discovery.get("barcode")
        or product_dir.name
    )

    name = (
        extract_product_name(ingredients_soup, nutrition_soup, allergens_soup)
        or discovery.get("name")
    )

    brand = (
        first_value_by_label("מותג/יצרן", ingredients_soup, nutrition_soup, allergens_soup)
        or discovery.get("brand")
    )

    parser_warnings = []

    if nutrition and nutrition_basis.get("basis_type") != "per_100g":
        parser_warnings.append(
            "nutrition_values_present_but_basis_not_confirmed_as_per_100g"
        )

    if not nutrition:
        parser_warnings.append("nutrition_missing_or_unparsed")

    if ingredients_raw is None:
        parser_warnings.append("ingredients_missing_or_unparsed")

    if allergens_raw is None:
        parser_warnings.append("allergens_missing_or_unparsed")

    product = {
        "schema_version": "bsip0.v1",
        "source": {
            "retailer": "Yohananof",
            "retailer_id": RETAILER,
            "source_type": "product_modal_html_tabs",
        },
        "product_identity": {
            "name": name,
            "brand": brand,
            "barcode": barcode,
            "country_of_origin": first_value_by_label("ארץ יצור", ingredients_soup, nutrition_soup, allergens_soup),
            "package_size": first_value_by_label("מידה", ingredients_soup, nutrition_soup, allergens_soup),
            "kosher": first_value_by_label("כשרות", ingredients_soup, nutrition_soup, allergens_soup),
            "image_url": image_info.get("source_image_url") or extract_image_url(ingredients_soup, nutrition_soup, allergens_soup),
            "local_image_file": image_info.get("local_image_file"),
            "category_path": extract_breadcrumbs(ingredients_soup, nutrition_soup, allergens_soup),
        },
        "pricing": extract_pricing(ingredients_soup, nutrition_soup, allergens_soup),
        "raw_observations": {
            "ingredients_raw_he": ingredients_raw,
            "allergens_raw_he": allergens_raw,
        },
        "nutrition_basis": nutrition_basis,
        "nutrition_per_100g": nutrition if nutrition_basis.get("basis_type") == "per_100g" else {},
        "nutrition_observed_values": nutrition,
        "provenance": {
            "discovery": discovery,
            "capture_status": capture_status,
            "folder": str(product_dir),
        },
        "parser_status": {
            "product_modal_parsed": True,
            "ingredients_present": ingredients_raw is not None,
            "nutrition_present": bool(nutrition),
            "nutrition_basis_confirmed_per_100g": nutrition_basis.get("basis_type") == "per_100g",
            "allergens_extracted": allergens_raw is not None,
            "image_present": image_info.get("local_image_file") is not None,
            "parsed_from_partial_capture": not all(
                path.exists() and path.stat().st_size > 0
                for path in [ingredients_html, nutrition_html, allergens_html]
            ),
            "parser_warnings": parser_warnings,
        },
    }

    output_json.write_text(json.dumps(product, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Parsed: {output_json}")
    return product


def main():
    all_products = []

    if not RETAILER_DIR.exists():
        print(f"Retailer directory not found: {RETAILER_DIR}")
        return

    for product_dir in RETAILER_DIR.iterdir():
        if not product_dir.is_dir():
            continue

        if product_dir.name.startswith("_tmp"):
            continue

        product = parse_product_folder(product_dir)
        if product:
            all_products.append(product)

    summary_path = RETAILER_DIR / "all_products.json"
    summary_path.write_text(json.dumps(all_products, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n==============================")
    print(f"Parsed products: {len(all_products)}")
    print(f"Saved summary: {summary_path}")
    print("==============================")


if __name__ == "__main__":
    main()