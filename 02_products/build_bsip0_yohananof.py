"""
Compile BSIP0 records from Yohananof storefront scrapes for juices and hard cheeses.
Parses nutrition.html from yohananof_scrape/, cross-refs il_prices identity,
runs OFF fallback for products with no storefront panel.

Run:
    python 02_products/build_bsip0_yohananof.py
"""
import json
import sys
import pathlib
import re
import datetime

ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(ROOT / "integrations"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from clients.open_food_facts import get_product as off_get

LI_PAT = re.compile(r"<span[^>]*>([^<]+)</span></div>([^<]*)</li>")

HEBREW_NUTRIENT_MAP = {
    "אנרגיה (קלוריות)": "energy_kcal",
    "שומנים (גרם)": "fat_g",
    "שומן רווי (גרם)": "fat_saturated_g",
    "שומן טרנס (גרם)": "fat_trans_g",
    "נתרן (מג)": "sodium_mg",
    "סך הפחמימות (גרם)": "carbohydrates_g",
    "סוכרים מתוך פחמימות (גרם)": "sugars_g",
    "סיבים תזונתיים (גרם)": "dietary_fiber_g",
    "חלבונים (גרם)": "protein_g",
}
SODIUM_G_LABELS = ["נתרן (גרם)"]


def parse_nutrition_html(html_path):
    if not html_path.exists():
        return {}
    content = html_path.read_text(encoding="utf-8", errors="replace")
    if len(content.strip()) < 50:
        return {}
    matches = LI_PAT.findall(content)
    raw = {}
    for lab, val in matches:
        lab = re.sub(r"\s+", " ", lab).strip()
        val_s = val.strip().replace(",", ".")
        if not val_s:
            continue
        try:
            num = float(val_s)
        except ValueError:
            continue
        raw[lab] = num

    nut = {}
    for heb_label, field in HEBREW_NUTRIENT_MAP.items():
        if heb_label in raw:
            nut[field] = raw[heb_label]
    for lab in SODIUM_G_LABELS:
        if lab in raw and "sodium_mg" not in nut:
            nut["sodium_mg"] = raw[lab] * 1000

    return nut


def extract_ingredients_text(html_path):
    if not html_path.exists():
        return None
    raw_html = html_path.read_text(encoding="utf-8", errors="replace")
    text_only = re.sub(r"<[^>]+>", " ", raw_html)
    text_only = re.sub(r"\s+", " ", text_only).strip()
    # Remove boilerplate UI text
    for boilerplate in [
        "הוסף", "לרשימה", "מבצע", "מחיר", "שמירה",
        "ביטול", "אישור",
    ]:
        text_only = text_only.replace(boilerplate, "")
    text_only = re.sub(r"\s+", " ", text_only).strip()
    return text_only[:600] if text_only else None


def _read_discovery_image_url(product_dir):
    dj = product_dir / "discovery.json"
    if not dj.exists():
        return None
    try:
        d = json.loads(dj.read_text(encoding="utf-8"))
        return (d.get("image") or {}).get("source_image_url") or None
    except Exception:
        return None


def build_bsip0_record(barcode, name, scrape_dir, il_prices_barcodes, category, run_id):
    product_dir = scrape_dir / barcode
    nut = parse_nutrition_html(product_dir / "nutrition.html")
    has_panel = bool(nut and any(v is not None for v in nut.values()))

    if il_prices_barcodes and barcode in il_prices_barcodes:
        identity_source = "il_prices:yohananof:7290455000004"
    else:
        identity_source = "storefront:yohananof"

    ingredients_raw = extract_ingredients_text(product_dir / "ingredients.html")

    rec = {
        "schema_version": "bsip0_v1",
        "barcode": barcode,
        "product_name_he": name,
        "brand": None,
        "retailer": "yohananof",
        "price": None,
        "category_tag": category,
        "image_url": _read_discovery_image_url(product_dir),
        "nutrition": nut if has_panel else {},
        "ingredients_raw_he": ingredients_raw,
        "data_sufficiency": "sufficient" if has_panel else "insufficient",
        "provenance": {
            "identity_source": identity_source,
            "panel_source": "yohananof_storefront",
            "panel_found": has_panel,
            "verification_status": "candidate",
            "fetched_at": datetime.datetime.now().isoformat(),
        },
    }
    return rec


def run_category(category, scrape_dir, run_report_path, il_prices_identity_path, output_dir, run_id):
    report = json.loads(run_report_path.read_text(encoding="utf-8"))

    il_prices_barcodes = set()
    if il_prices_identity_path.exists():
        identity = json.loads(il_prices_identity_path.read_text(encoding="utf-8"))
        il_prices_barcodes = set(identity.keys())

    products = []
    off_fallback_attempts = 0
    off_fallback_hits = 0
    source_errors = {}

    for entry in report:
        barcode = entry.get("barcode", "")
        name = entry.get("name", "")
        if not barcode:
            continue

        rec = build_bsip0_record(barcode, name, scrape_dir, il_prices_barcodes, category, run_id)

        if rec["data_sufficiency"] == "insufficient":
            off_fallback_attempts += 1
            try:
                off_data = off_get(barcode, timeout=15)
                if off_data and off_data.found and off_data.has_panel:
                    n = off_data.nutriments
                    rec["nutrition"] = {
                        "energy_kcal": n.get("energy-kcal_100g"),
                        "fat_g": n.get("fat_100g"),
                        "fat_saturated_g": n.get("saturated-fat_100g"),
                        "sodium_mg": (
                            n.get("sodium_100g", 0) * 1000
                            if n.get("sodium_100g") else None
                        ),
                        "carbohydrates_g": n.get("carbohydrates_100g"),
                        "sugars_g": n.get("sugars_100g"),
                        "dietary_fiber_g": n.get("fiber_100g"),
                        "protein_g": n.get("proteins_100g"),
                    }
                    rec["data_sufficiency"] = "sufficient"
                    rec["provenance"]["panel_source"] = "open_food_facts_fallback"
                    rec["provenance"]["panel_found"] = True
                    off_fallback_hits += 1
                    print(f"  OFF fallback HIT: {barcode} | {name}")
                else:
                    print(f"  OFF fallback MISS: {barcode} | {name}")
            except Exception as e:
                source_errors[barcode] = str(e)[:150]
                print(f"  OFF lookup error {barcode}: {e}")

        products.append(rec)

    sufficient = sum(1 for r in products if r["data_sufficiency"] == "sufficient")

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "schema_version": "bsip0_v1",
        "retailer": "yohananof",
        "category": category,
        "run_id": run_id,
        "scraped_at": datetime.datetime.now().isoformat(),
        "product_count": len(products),
        "sufficient_count": sufficient,
        "products": products,
        "source_error": source_errors if source_errors else {},
        "off_fallback": {
            "attempted": off_fallback_attempts,
            "hits": off_fallback_hits,
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"bsip0_yohananof_{category}_storefront_{ts}.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(products)} records -> {out_path}")
    print(f"  Sufficient: {sufficient}/{len(products)} | OFF fallback: {off_fallback_hits}/{off_fallback_attempts}")
    return output, str(out_path)


def main():
    print("=== BUILDING JUICES BSIP0 ===")
    juice_output, juice_path = run_category(
        category="juices",
        scrape_dir=ROOT / "02_products" / "juices" / "yohananof_scrape",
        run_report_path=ROOT / "02_products" / "juices" / "yohananof_scrape" / "run_report.json",
        il_prices_identity_path=ROOT / "02_products" / "juices" / "yohananof_scrape" / "il_prices_identity.json",
        output_dir=ROOT / "02_products" / "juices" / "bsip0_outputs",
        run_id="run_juices_yohananof_001",
    )

    print()
    print("=== BUILDING HARD CHEESES BSIP0 ===")
    cheese_output, cheese_path = run_category(
        category="hard_cheeses",
        scrape_dir=ROOT / "02_products" / "hard_cheeses" / "yohananof_scrape",
        run_report_path=ROOT / "02_products" / "hard_cheeses" / "yohananof_scrape" / "run_report.json",
        il_prices_identity_path=ROOT / "02_products" / "hard_cheeses" / "yohananof_scrape" / "il_prices_identity.json",
        output_dir=ROOT / "02_products" / "hard_cheeses" / "bsip0_outputs",
        run_id="run_cheeses_yohananof_001",
    )

    # Print summary sample
    print()
    print("=== JUICE SAMPLES ===")
    for p in juice_output["products"][:5]:
        suf = p["data_sufficiency"]
        nut_keys = list(p["nutrition"].keys()) if p["nutrition"] else []
        print(f"  {p['barcode']} | {p['product_name_he'][:40]} | {suf} | {nut_keys}")

    print()
    print("=== CHEESE SAMPLES ===")
    for p in cheese_output["products"][:5]:
        suf = p["data_sufficiency"]
        nut_keys = list(p["nutrition"].keys()) if p["nutrition"] else []
        print(f"  {p['barcode']} | {p['product_name_he'][:40]} | {suf} | {nut_keys}")

    print()
    print(f"Juice BSIP0 output: {juice_path}")
    print(f"Cheese BSIP0 output: {cheese_path}")


if __name__ == "__main__":
    main()
