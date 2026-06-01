"""
TASK-034 — Convert hummus BSIP0 observations to BSIP1 format.

Reads:   C:\Bari\02_products\hummus\observations_bsip0\shufersal\P_*.json
Writes:  C:\Bari\03_operations\bsip1\run_hummus_001\output\bsip1_{barcode}.json
"""
from __future__ import annotations
import json
import re
import sys
import datetime
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OBS_DIR = pathlib.Path(r"C:\Bari\02_products\hummus\observations_bsip0\shufersal")
OUT_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_hummus_001\output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

_NUM_RE = re.compile(r"(\d+(?:[.,]\d+)?)")
_WEIGHT_PATS = [
    re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.IGNORECASE),  # ק"ג / קג
    re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.IGNORECASE),  # גרם / גר'
    re.compile(r"(\d[\d,.]*)\s*g\b", re.IGNORECASE),
    re.compile(r"(\d[\d,.]*)\s*מ[\"']?ל", re.IGNORECASE),  # מ"ל / מל
]

JUNK_MARKERS = [
    "ערכים תזונתיים",  # ערכים תזונתיים
    "מאפיינים נוספים",  # מאפיינים נוספים
    "ttrn",
    "הנתונים המדויקים",  # הנתונים המדויקים
]

CATEGORY_MAP = {
    "A162406_hummus_tahini": "hummus_spread",
    "A162403_eggplant":      "eggplant_spread",
    "A162408_schug_matbucha": "matbucha_pepper_spread",
    "A162405_chilled":       "chilled_spread",
    "search":                "hummus_and_savory_dips",
}


def parse_num(s: str) -> float | None:
    if not s:
        return None
    m = _NUM_RE.search(str(s).replace(",", "."))
    return float(m.group(1)) if m else None


def extract_weight_g(name: str) -> float | None:
    for pat in _WEIGHT_PATS:
        m = pat.search(name or "")
        if m:
            try:
                v = float(m.group(1).replace(",", "."))
                # ק = kilogram prefix
                if "ק" in m.group(0):
                    v *= 1000
                if 5 < v < 5000:
                    return v
            except ValueError:
                pass
    return None


def clean_ingredients(raw: str) -> str:
    if not raw:
        return ""
    s = raw.strip()
    for marker in JUNK_MARKERS:
        idx = s.find(marker)
        if idx > 20:
            s = s[:idx].strip()
    return s.rstrip(".,; ")


def make_ingredients_list(text: str) -> list[str]:
    if not text:
        return []
    items: list[str] = []
    cur = ""
    depth = 0
    for c in text:
        if c == "(":
            depth += 1
            cur += c
        elif c == ")":
            depth -= 1
            cur += c
        elif c == "," and depth == 0:
            stripped = cur.strip()
            if stripped:
                items.append(stripped)
            cur = ""
        else:
            cur += c
    if cur.strip():
        items.append(cur.strip())
    return items


def convert_one(src: pathlib.Path) -> dict:
    p = json.loads(src.read_text(encoding="utf-8"))

    barcode = (p.get("barcode") or "").strip() or src.stem.replace("P_", "")
    n = p.get("nutrition", {})
    ingr_raw = clean_ingredients(p.get("ingredients_raw", "") or "")
    ingr_list = make_ingredients_list(ingr_raw)
    weight_g = p.get("weight_g") or extract_weight_g(p.get("name_he", ""))
    image_url = (p.get("image_urls") or [None])[0]

    energy  = parse_num(n.get("energy_kcal_raw"))
    protein = parse_num(n.get("protein_raw"))
    carbs   = parse_num(n.get("carbs_raw"))
    fat     = parse_num(n.get("fat_raw"))
    fiber   = parse_num(n.get("fiber_raw"))
    sodium  = parse_num(n.get("sodium_raw"))
    sugar   = parse_num(n.get("sugar_raw"))

    nutr: dict = {}
    if energy  is not None: nutr["energy_kcal"]     = energy
    if fat     is not None: nutr["fat_g"]            = fat
    if carbs   is not None: nutr["carbohydrates_g"]  = carbs
    if sugar   is not None: nutr["sugars_g"]         = sugar
    if fiber   is not None: nutr["dietary_fiber_g"]  = fiber
    if protein is not None: nutr["protein_g"]        = protein
    if sodium  is not None: nutr["sodium_mg"]        = sodium

    has_nutr = bool(energy and protein and carbs and fat)
    has_ingr = bool(ingr_raw)

    return {
        "schema_version":       "bsip1_v0_1",
        "file_type":            "product",
        "canonical_product_id": f"bsip1_{barcode}",
        "barcode":              barcode,
        "canonical_name_he":    p.get("name_he", ""),
        "canonical_name_en":    None,
        "brand":                p.get("brand") or None,
        "package_size_g":       weight_g,
        "unit_count":           None,
        "unit_size_g":          None,
        "serving_size_g":       None,
        "country_of_origin":    "ישראל",  # ישראל
        "kosher_certification": None,
        "image_url":            image_url,
        "source_retailers":     ["shufersal"],
        "normalized_nutrition_per_100g": nutr,
        "energy_source_unit":   "kcal",
        "ingredients_text_he":  ingr_raw or None,
        "ingredients_list":     ingr_list,
        "allergens_contains":   [],
        "allergens_may_contain": [],
        "claims":               [],
        "confidence": {
            "identity_confidence":   "high" if (has_nutr and has_ingr) else "medium",
            "barcode_confidence":    "confirmed" if len(barcode) == 13 else "inferred",
            "nutrition_confidence":  "confirmed_per_100g" if has_nutr else "partial",
            "matched_by":            "shufersal_bsip0_html_scrape",
            "observation_count":     1,
        },
        "barcode_validation_status": "shufersal_scraped",
        "barcode_confidence_reason":
            "Scraped from Shufersal product page; barcode from LD+JSON gtin13 field.",
        "nutrition_basis_claimed":   "ל-100 גרם",  # ל-100 גרם
        "nutrition_basis_detected":  "per_100g",
        "nutrition_consistency_status":
            "consistent" if has_nutr else "incomplete",
        "nutrition_consistency_warnings":
            [] if has_nutr else ["partial_nutrition_only"],
        "ingredient_text_quality":
            "scraped_html" if has_ingr else "missing",
        "ingredient_warnings":
            [] if has_ingr else ["ingredients_raw_missing"],
        "canonical_trust_score":
            0.82 if (has_nutr and has_ingr) else 0.55,
        "canonical_trust_level":
            "high" if (has_nutr and has_ingr) else "low",
        "canonical_risk_flags": ["single_source_only"],
        "bsip0_source": {
            "retailer":               "shufersal",
            "source_url":             p.get("source_url", ""),
            "scraped_at":             p.get("scraped_at", ""),
            "source_category":        p.get("source_category", ""),
            "product_category":       CATEGORY_MAP.get(
                p.get("source_category", ""), "hummus_and_savory_dips"
            ),
            "extraction_method":      p.get("extraction_method", "html_parse"),
            "extraction_confidence":  p.get("extraction_confidence", ""),
            "price_ils":              p.get("price") or None,
            "price_per_100g":         p.get("price_per_100g") or None,
        },
        "bsip1_converted_at":       datetime.datetime.now().isoformat(timespec="seconds"),
        "bsip1_conversion_source":  "TASK-034",
    }


def main() -> None:
    sources = sorted(OBS_DIR.glob("P_*.json"))
    print(f"Converting {len(sources)} BSIP0 files to BSIP1 ...")
    converted = 0
    errors = 0
    for src in sources:
        try:
            record = convert_one(src)
            barcode = record["barcode"]
            out_path = OUT_DIR / f"bsip1_{barcode}.json"
            out_path.write_text(
                json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            converted += 1
        except Exception as e:
            print(f"  ERROR {src.name}: {e}")
            errors += 1

    print(f"  Converted : {converted}")
    print(f"  Errors    : {errors}")
    print(f"  Output    : {OUT_DIR}")


if __name__ == "__main__":
    main()
