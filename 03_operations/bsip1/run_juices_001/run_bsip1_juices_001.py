# -*- coding: utf-8 -*-
"""
BSIP1 Enrichment — Juices & Fruit Drinks (run_juices_yohananof_001)
TASK-214 re-run from REAL Yohananof storefront BSIP0 data.

Input:  bsip0_yohananof_juices_storefront_20260607_151232.json
Output: 02_products/juices/bsip1_outputs/  — one bsip1_juice_{barcode}.json per product
        bsip1_run_report.json  — subpool/NOVA distribution summary
        skipped.json           — products with data_sufficiency != sufficient
"""

import sys
import json
import pathlib
import datetime
import re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT       = pathlib.Path(r"C:\Bari")
BSIP0_FILE = ROOT / "02_products" / "juices" / "bsip0_outputs" / \
             "bsip0_yohananof_juices_storefront_20260607_151232.json"
OUTPUT_DIR = ROOT / "02_products" / "juices" / "bsip1_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RUN_ID = "run_juices_yohananof_001"

# ── E-number pattern ──────────────────────────────────────────────────────────
E_PAT = re.compile(r"E[-\s]?\d{3,4}[a-z]?", re.IGNORECASE)


def extract_ingredients(raw_he: str) -> str:
    """Extract clean ingredient text from raw storefront dump.

    Algorithm:
      1. Find LAST occurrence of 'מידע אלרגני' — take everything after it.
      2. Cut at 'הנתונים המדויקים' or 'יתכנו טעויות' (whichever first).
      3. Strip whitespace. If result < 10 chars, use full raw_he.

    For juices, ingredients often appear without 'מידע אלרגני' marker —
    also try extracting from 'רכיבים:' or 'רכיבים' marker.
    """
    if not raw_he:
        return ""

    # Primary: after last 'מידע אלרגני'
    marker = "מידע אלרגני"
    idx = raw_he.rfind(marker)
    if idx != -1:
        text = raw_he[idx + len(marker):]
        for cutoff in ["הנתונים המדויקים", "יתכנו טעויות"]:
            ci = text.find(cutoff)
            if ci != -1:
                text = text[:ci]
        text = text.strip()
        if len(text) >= 10:
            return text

    # Secondary: look for 'רכיבים:' marker (common in juice labels)
    for marker2 in ("רכיבים:", "רכיבים "):
        idx2 = raw_he.rfind(marker2)
        if idx2 != -1:
            text2 = raw_he[idx2 + len(marker2):]
            for cutoff in ["הנתונים המדויקים", "יתכנו טעויות"]:
                ci = text2.find(cutoff)
                if ci != -1:
                    text2 = text2[:ci]
            text2 = text2.strip()
            if len(text2) >= 5:
                return text2

    # Fall back: return raw stripped
    return raw_he.strip()


def parse_ingredients_list(ing_text: str) -> list:
    """Split ingredient text on commas/semi-colons; strip empties."""
    if not ing_text:
        return []
    parts = re.split(r"[,;]", ing_text)
    result = []
    for p in parts:
        p = p.strip().strip(".")
        if p and len(p) > 1:
            result.append(p)
    return result


def detect_additives(ing_text: str) -> list:
    """Return list of detected E-number additive strings."""
    if not ing_text:
        return []
    found = list(set(re.findall(r"E[-\s]?\d{3,4}[a-z]?", ing_text, re.IGNORECASE)))
    return sorted(found)


def classify_subpool(name: str, ing_text: str) -> str:
    """Classify juice sub-pool.

    Rules (applied in order):
      smoothie      — name contains שייק or smoothie
      juice_100     — name contains 100% AND no added-sugar signal
      nectar        — name contains נקטר
      juice_100     — single-ingredient pure fruit (e.g. "מיץ תפוזים", "מיץ רימונים")
      juice_100     — name has 'סחוט' or 'טרי' + single-ingredient or pure fruit label
      fruit_drink   — default: added sugar present or low fruit content
    """
    name_norm = name.lower() if name else ""
    ing_lower  = (ing_text or "").lower()

    # Smoothie
    if "שייק" in name or "smoothie" in name_norm:
        return "smoothie"

    # Known fruit_drink brands (check early — before 100% logic)
    FRUIT_DRINK_BRANDS = ("ספרינג", "קריסטל", "ג'אמפ", "תפוזינה")
    if any(b in name for b in FRUIT_DRINK_BRANDS):
        # Even if they say "נקטר" → nectar sub-pool
        if "נקטר" in name:
            return "nectar"
        return "fruit_drink"

    # Added sugar signals in ingredients
    has_added_sugar = bool(re.search(r"סוכר לבן|,\s*סוכר|^סוכר", ing_text or ""))

    # 100% declared in name AND no added sugar
    if "100%" in name and not has_added_sugar:
        return "juice_100"

    # Nectar — explicit נקטר in name
    if "נקטר" in name:
        return "nectar"

    # If name says 100% (even with some additives like preservative) → juice_100
    if "100%" in name:
        return "juice_100"

    # Single-ingredient pure fruit: ingredients text is just the fruit juice
    # E.g. "מיץ תפוזים", "מיץ ענבים", "מיץ קלמנטינות", "מיץ רימונים", "מיץ לימון"
    if ing_text:
        stripped = ing_text.strip().rstrip(".")
        # Short ingredient text = mostly single fruit
        if len(stripped) < 40 and re.match(r"^מיץ [א-ת ]+$", stripped):
            return "juice_100"
        # Ingredient starts with "מיץ [fruit]" and nothing else suspicious
        if re.match(r"^מיץ [א-ת ]+$", stripped):
            return "juice_100"

    # 'סחוט' or 'טרי' in name = fresh-squeezed → juice_100 unless added sugar
    if ("סחוט" in name or "טרי" in name) and not has_added_sugar:
        # Limenade "סחוט לימונענע" has added sugar — let that fall to fruit_drink below
        if "לימונענע" not in name:
            return "juice_100"

    # Added sugar as first ingredient → fruit_drink
    if ing_text and ing_text.lstrip().startswith(("מים", "סוכר")):
        return "fruit_drink"

    # מים + סוכר in early text → fruit_drink
    if "מים" in ing_lower[:40] and "סוכר" in ing_lower:
        return "fruit_drink"

    # Cranberry drink with added sugar → fruit_drink
    if "חמוציות" in name and "סוכר" in ing_lower:
        return "fruit_drink"

    # Lemon juice
    if "לימון" in name and not has_added_sugar:
        return "juice_100"

    # Default: fruit_drink for ambiguous products
    return "fruit_drink"


def assign_nova_juice(name: str, ing_text: str, additives: list, subpool: str) -> dict:
    """NOVA proxy for juices.

    NOVA 1: fresh-squeezed / cold-pressed 100% fruit with no additives
    NOVA 3: reconstituted / pasteurized 100% juice (מרכז), or <100% fruit, or citric acid
    NOVA 4: added white sugar as primary ingredient + artificial flavours/colours + <25% fruit
    """
    if not ing_text:
        return {
            "nova_proxy": 3,
            "nova_confidence": 0.4,
            "nova_confidence_band": "low",
            "nova_notes": ["no_ingredient_text: defaulting to NOVA 3"],
        }

    e_count = len(additives)
    has_added_sugar = bool(re.search(r"סוכר לבן|סוכר\s", ing_text))
    has_concentrate = bool(re.search(r"מרכז|רכז|משוחזר|משוחרג", ing_text))
    has_citric = bool(re.search(r"חומצה ציטרית|חומצת לימון", ing_text))
    has_artificial = bool(re.search(r"צבע מאכל|חומרי טעם וריח|ממתיק|סוכרלוז|אצסולאם", ing_text))
    has_preservative = bool(re.search(r"חומר משמר|סולפיט|E202|E223|E224", ing_text))
    single_fruit = bool(re.match(r"^\s*מיץ \w+[\s.]*$", ing_text.strip()))

    # NOVA 4: added sugar (not from fruit) + additives + low-fruit indicators
    if subpool == "fruit_drink" and has_added_sugar and (has_artificial or e_count >= 3):
        return {
            "nova_proxy": 4,
            "nova_confidence": 0.85,
            "nova_confidence_band": "high",
            "nova_notes": ["added_sugar+artificial_additives: NOVA 4 fruit drink"],
        }

    # NOVA 1: single ingredient, fresh, no additives
    if single_fruit and not has_concentrate and e_count == 0 and not has_citric:
        return {
            "nova_proxy": 1,
            "nova_confidence": 0.85,
            "nova_confidence_band": "high",
            "nova_notes": ["single_ingredient_fresh_squeezed: NOVA 1"],
        }

    # NOVA 1 edge: "סחוט" in name + single fruit ingredient
    if ("סחוט" in name or "טרי" in name) and single_fruit and e_count == 0:
        return {
            "nova_proxy": 1,
            "nova_confidence": 0.80,
            "nova_confidence_band": "high",
            "nova_notes": ["fresh_squeezed_label+minimal_ingredients: NOVA 1"],
        }

    # NOVA 3: everything else (reconstituted, pasteurised, with citric acid/preservatives)
    notes = []
    if has_concentrate:
        notes.append("reconstituted_from_concentrate")
    if has_citric or has_preservative:
        notes.append("preservative_or_acidulant_present")
    if e_count > 0:
        notes.append(f"{e_count}_e_numbers_detected")
    if not notes:
        notes = ["standard_juice_processing"]

    return {
        "nova_proxy": 3,
        "nova_confidence": 0.75,
        "nova_confidence_band": "medium",
        "nova_notes": notes,
    }


def consistency_checks(nn: dict) -> dict:
    sugar   = nn.get("sugars_g")
    carbs   = nn.get("carbohydrates_g")
    sat_fat = nn.get("fat_saturated_g")
    fat     = nn.get("fat_g")
    kcal    = nn.get("energy_kcal")

    sugar_le_carbs = True if (sugar is None or carbs is None) else (sugar <= carbs + 0.1)
    satfat_le_fat  = True if (sat_fat is None or fat is None) else (sat_fat <= fat + 0.1)
    kcal_plausible = True
    if kcal is not None:
        # Juices: 0–200 kcal/100ml plausible; milk drinks slightly higher
        kcal_plausible = 0 <= kcal <= 250
    macros_plausible = True

    return {
        "sugar_le_carbs": sugar_le_carbs,
        "satfat_le_fat": satfat_le_fat,
        "kcal_plausible": kcal_plausible,
        "macros_plausible": macros_plausible,
    }


def compute_trust(checks: dict, ing_text: str) -> tuple:
    flags = ["single_source_only"]
    score = 0.75

    if not checks.get("sugar_le_carbs") or not checks.get("satfat_le_fat"):
        score -= 0.2
        flags.append("consistency_failure")
    if not checks.get("kcal_plausible"):
        score -= 0.1
        flags.append("kcal_implausible")
    if not ing_text:
        score -= 0.1
        flags.append("no_ingredient_text")

    score = round(max(0.1, min(1.0, score)), 2)
    if score >= 0.8:
        level = "high"
    elif score >= 0.5:
        level = "medium"
    else:
        level = "low"
    return level, score, flags


def build_bsip1(product: dict, timestamp: str) -> dict:
    barcode    = product["barcode"]
    name       = product.get("product_name_he", "")
    nutrition  = product.get("nutrition") or {}
    raw_he     = product.get("ingredients_raw_he") or ""
    provenance = product.get("provenance") or {}

    def _f(key):
        v = nutrition.get(key)
        return float(v) if v is not None else None

    nn = {
        "energy_kcal":      _f("energy_kcal"),
        "fat_g":            _f("fat_g"),
        "fat_saturated_g":  _f("fat_saturated_g"),
        "fat_trans_g":      None,
        "sodium_mg":        _f("sodium_mg"),
        "carbohydrates_g":  _f("carbohydrates_g"),
        "sugars_g":         _f("sugars_g"),
        "dietary_fiber_g":  _f("dietary_fiber_g"),
        "protein_g":        _f("protein_g"),
    }

    ing_text   = extract_ingredients(raw_he)
    ing_list   = parse_ingredients_list(ing_text)
    additives  = detect_additives(ing_text)
    subpool    = classify_subpool(name, ing_text)
    nova_res   = assign_nova_juice(name, ing_text, additives, subpool)
    checks     = consistency_checks(nn)
    trust_lvl, trust_score, risk_flags = compute_trust(checks, ing_text)

    missing = [k for k, v in nn.items() if v is None and k in ("energy_kcal", "carbohydrates_g")]

    doc = {
        "schema_version":           "bsip1_v0_1",
        "file_type":                "product",
        "canonical_product_id":     f"bsip1_juice_{barcode}",
        "barcode":                  barcode,
        "canonical_name_he":        name,
        "brand":                    None,
        "weight_g":                 None,
        "category":                 "juices",
        "juice_subpool":            subpool,
        "source_retailers":         ["yohananof"],
        "retailer_prices":          {"yohananof": None},
        "image_url":                product.get("image_url"),
        "normalized_nutrition_per_100g": nn,
        "energy_kcal":              nn.get("energy_kcal"),
        "fat_g":                    nn.get("fat_g"),
        "fat_saturated_g":          nn.get("fat_saturated_g"),
        "fat_trans_g":              None,
        "protein_g":                nn.get("protein_g"),
        "carbohydrates_g":          nn.get("carbohydrates_g"),
        "sugars_g":                 nn.get("sugars_g"),
        "sodium_mg":                nn.get("sodium_mg"),
        "dietary_fiber_g":          nn.get("dietary_fiber_g"),
        "calcium_mg":               None,
        "ingredients_text_he":      ing_text if ing_text else None,
        "ingredients_list":         ing_list,
        "ingredient_count":         len(ing_list),
        "ingredient_text_quality":  "good" if len(ing_list) >= 2 else ("present" if ing_text else "absent"),
        "allergens_contains":       [],
        "allergens_may_contain":    [],
        "confidence":               trust_score,
        "canonical_trust_level":    trust_lvl,
        "canonical_trust_score":    trust_score,
        "conflicts_summary":        [],
        "missing_fields":           missing,
        "inferred_fields":          [],
        "audit_ref":                None,
        "nova_proxy":               nova_res["nova_proxy"],
        "nova_confidence":          nova_res["nova_confidence"],
        "nova_confidence_band":     nova_res["nova_confidence_band"],
        "nova_notes":               nova_res["nova_notes"],
        "detected_additives":       additives,
        "additive_count":           len(additives),
        "data_sufficiency":         "sufficient",
        "bsip1_trust_level":        trust_lvl,
        "bsip1_trust_score":        trust_score,
        "bsip1_risk_flags":         risk_flags,
        "nutrition_consistency_status": "consistent" if (checks["sugar_le_carbs"] and checks["satfat_le_fat"]) else "warnings",
        "consistency_checks":       checks,
        "provenance": {
            "source":               provenance.get("panel_source", "yohananof_storefront"),
            "fetched_at":           provenance.get("fetched_at", ""),
            "panel_source":         provenance.get("panel_source", "yohananof_storefront"),
            "verification_status":  "candidate",
        },
        "enrichment_timestamp":     timestamp,
        "run_id":                   RUN_ID,
    }
    return doc


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    bsip0 = json.loads(BSIP0_FILE.read_text(encoding="utf-8"))
    products = bsip0["products"]

    enriched      = []
    skipped       = []
    subpool_dist  = {}
    nova_dist     = {}

    for p in products:
        if p.get("data_sufficiency") != "sufficient":
            skipped.append({
                "barcode": p.get("barcode"),
                "name":    p.get("product_name_he"),
                "reason":  "data_sufficiency != sufficient",
            })
            continue

        nutrition = p.get("nutrition") or {}
        kcal = nutrition.get("energy_kcal")
        carbs = nutrition.get("carbohydrates_g")
        if kcal is None or carbs is None:
            skipped.append({
                "barcode": p.get("barcode"),
                "name":    p.get("product_name_he"),
                "reason":  f"missing core nutrition: energy_kcal={kcal} carbohydrates_g={carbs}",
            })
            continue

        doc = build_bsip1(p, ts)
        out_path = OUTPUT_DIR / f"bsip1_juice_{doc['barcode']}.json"
        out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        enriched.append(doc)
        print(f"  ENRICHED: {doc['barcode']} — {doc['canonical_name_he']} [{doc['juice_subpool']}] NOVA {doc['nova_proxy']}")

        sp = doc["juice_subpool"]
        subpool_dist[sp] = subpool_dist.get(sp, 0) + 1
        nv = f"NOVA_{doc['nova_proxy']}"
        nova_dist[nv] = nova_dist.get(nv, 0) + 1

    # Write skipped log
    (OUTPUT_DIR / "skipped.json").write_text(
        json.dumps({"run_id": RUN_ID, "skipped": skipped}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Write run report
    report = {
        "run_id":       RUN_ID,
        "generated":    ts,
        "source_file":  str(BSIP0_FILE),
        "total_input":  len(products),
        "enriched":     len(enriched),
        "skipped":      len(skipped),
        "subpool_distribution": subpool_dist,
        "nova_distribution":    nova_dist,
    }
    (OUTPUT_DIR / "bsip1_run_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\nDone. Enriched={len(enriched)}, Skipped={len(skipped)}")
    print(f"Subpool: {subpool_dist}")
    print(f"NOVA:    {nova_dist}")


if __name__ == "__main__":
    main()
