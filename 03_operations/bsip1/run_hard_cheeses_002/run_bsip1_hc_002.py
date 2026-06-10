# -*- coding: utf-8 -*-
"""
BSIP1 Enrichment — Hard & Yellow Cheeses (run_hard_cheeses_yohananof_001)
TASK-215 re-run from REAL Yohananof storefront BSIP0 data.

Input:  bsip0_yohananof_hard_cheeses_storefront_20260607_151235.json
Output: 02_products/hard_cheeses/bsip1_outputs/  — one bsip1_hardcheese_{barcode}.json per product
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
BSIP0_FILE = ROOT / "02_products" / "hard_cheeses" / "bsip0_outputs" / \
             "bsip0_yohananof_hard_cheeses_storefront_20260607_151235.json"
OUTPUT_DIR = ROOT / "02_products" / "hard_cheeses" / "bsip1_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RUN_ID = "run_hard_cheeses_yohananof_001"

# ── NOVA assignment patterns ──────────────────────────────────────────────────
# Phosphates → NOVA 4 processed cheese
NOVA4_PAT = re.compile(r"(E339|E340|E341|E-339|E-340|E-341|פוספט|שמן דקלים)", re.UNICODE)
# Stabilizers / modified starch → NOVA 3
NOVA3_PAT = re.compile(
    r"(עמילן מתוקן|E\d{3,4}|חומר (מייצב|ייצוב)|קרגינן|חומצה ציטרית שלא|חומר (מונע|עיכוב))",
    re.UNICODE
)
# Generic E-number counter
E_PAT = re.compile(r"E[-\s]?\d{3,4}[a-z]?", re.IGNORECASE)


def extract_ingredients(raw_he: str) -> str:
    """Extract clean ingredient text from raw storefront dump.

    Algorithm:
      1. Find LAST occurrence of 'מידע אלרגני' — take everything after it.
      2. Cut at 'הנתונים המדויקים' or 'יתכנו טעויות' (whichever first).
      3. Strip whitespace. If result < 10 chars use full raw_he.
    """
    if not raw_he:
        return ""
    marker = "מידע אלרגני"
    idx = raw_he.rfind(marker)
    if idx == -1:
        text = raw_he
    else:
        text = raw_he[idx + len(marker):]

    for cutoff in ["הנתונים המדויקים", "יתכנו טעויות"]:
        ci = text.find(cutoff)
        if ci != -1:
            text = text[:ci]

    text = text.strip()
    if len(text) < 10:
        text = raw_he.strip()
    return text


def parse_ingredients_list(ing_text: str) -> list:
    """Split ingredient text on commas, semi-colons; strip empties."""
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


def assign_nova(ing_text: str, additives: list) -> dict:
    """Assign NOVA proxy for hard cheese products."""
    if not ing_text:
        return {
            "nova_proxy": 2,
            "nova_confidence": 0.3,
            "nova_confidence_band": "low",
            "nova_notes": ["no_ingredient_text: defaulting to NOVA 2 proxy"],
        }

    has_nova4 = bool(NOVA4_PAT.search(ing_text))
    has_nova3 = bool(NOVA3_PAT.search(ing_text)) or (len(additives) >= 2)

    if has_nova4:
        return {
            "nova_proxy": 4,
            "nova_confidence": 0.90,
            "nova_confidence_band": "high",
            "nova_notes": ["phosphates/vegetable_oil_detected: NOVA 4 processed cheese"],
        }
    if has_nova3:
        return {
            "nova_proxy": 3,
            "nova_confidence": 0.80,
            "nova_confidence_band": "high",
            "nova_notes": ["stabilizers_or_additives_detected: NOVA 3"],
        }
    # Minimal: milk, salt, rennet, cultures only
    e_count = len(E_PAT.findall(ing_text))
    if e_count == 0:
        return {
            "nova_proxy": 1,
            "nova_confidence": 0.90,
            "nova_confidence_band": "high",
            "nova_notes": ["minimal_ingredients_milk_salt_rennet_cultures: NOVA 1"],
        }
    return {
        "nova_proxy": 2,
        "nova_confidence": 0.70,
        "nova_confidence_band": "medium",
        "nova_notes": ["minor_additive_detected: NOVA 2"],
    }


def classify_subpool(name: str, fat_g: float, ing_text: str, additives: list) -> str:
    """Classify hard cheese sub-pool.

    Rules (applied in order):
      processed  — ingredients contain E339 / E340 / E341 phosphates
      hard_grating — name contains פרמזן or מגורר or מגורד
      bulgarian  — name contains בולגרית
      tzfatit    — name contains צפתית
      yellow_light — yellow-type AND ('מופחת שומן' in name OR fat_g <= 16)
      yellow     — name contains גאודה/גבינה צהובה/עמק/אמנטל/קשקבל/מונסטר/קולבי/גרויר/yellow
      yellow     — default fallback for cheese products
    """
    name_lower = name.lower() if name else ""
    ing_lower  = ing_text.lower() if ing_text else ""

    # Processed: phosphate emulsifiers
    if any(p in ing_text for p in ("E339", "E340", "E341", "E-339", "E-340", "E-341", "פוספט")):
        if "E339" in ing_text or "E340" in ing_text or "E341" in ing_text or "פוספט" in ing_text:
            return "processed"

    # Hard grating
    if any(k in name for k in ("פרמזן", "מגורדת", "מגורד", "מגורר")):
        return "hard_grating"

    # Bulgarian
    if "בולגרית" in name:
        return "bulgarian"

    # Tzfatit
    if "צפתית" in name:
        return "tzfatit"

    # Yellow-type keywords
    YELLOW_KEYWORDS = ("גאודה", "גבינה צהובה", "עמק", "אמנטל", "קשקבל", "מונסטר", "קולבי", "גרויר", "yellow", "נעם", "גוש חלב")
    is_yellow_type = any(k in name for k in YELLOW_KEYWORDS) or "גבינה" in name

    # Light variant
    fat = fat_g if fat_g is not None else 99.0
    if is_yellow_type and ("מופחת שומן" in name or fat <= 16):
        return "yellow_light"

    if is_yellow_type:
        return "yellow"

    # Default: yellow (catch-all for hard cheeses)
    return "yellow"


def consistency_checks(nn: dict) -> dict:
    sugar   = nn.get("sugars_g")
    carbs   = nn.get("carbohydrates_g")
    sat_fat = nn.get("fat_saturated_g")
    fat     = nn.get("fat_g")
    kcal    = nn.get("energy_kcal")

    sugar_le_carbs  = True if (sugar is None or carbs is None) else (sugar <= carbs + 0.1)
    satfat_le_fat   = True if (sat_fat is None or fat is None) else (sat_fat <= fat + 0.1)
    kcal_plausible  = True
    if kcal is not None:
        # Hard cheese: 100–500 kcal/100g is plausible
        kcal_plausible = 50 <= kcal <= 700
    macros_plausible = True
    prot = nn.get("protein_g")
    if prot is not None and prot > 100:
        macros_plausible = False

    return {
        "sugar_le_carbs": sugar_le_carbs,
        "satfat_le_fat": satfat_le_fat,
        "kcal_plausible": kcal_plausible,
        "macros_plausible": macros_plausible,
    }


def compute_trust(checks: dict, ing_text: str, additives: list) -> tuple:
    """Return (trust_level, trust_score, risk_flags)."""
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
    barcode     = product["barcode"]
    name        = product.get("product_name_he", "")
    nutrition   = product.get("nutrition") or {}
    raw_he      = product.get("ingredients_raw_he") or ""
    provenance  = product.get("provenance") or {}

    # Normalise nutrition
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
        "dietary_fiber_g":  None,
        "protein_g":        _f("protein_g"),
    }

    # Ingredient extraction
    ing_text    = extract_ingredients(raw_he)
    ing_list    = parse_ingredients_list(ing_text)
    additives   = detect_additives(ing_text)
    nova_result = assign_nova(ing_text, additives)
    subpool     = classify_subpool(name, nn.get("fat_g"), ing_text, additives)
    checks      = consistency_checks(nn)
    trust_lvl, trust_score, risk_flags = compute_trust(checks, ing_text, additives)

    missing = [k for k, v in nn.items() if v is None and k in ("energy_kcal", "fat_g", "protein_g", "sodium_mg")]

    # Allergens
    allergens = ["milk"] if ("חלב" in ing_text or "חלב" in name) else []

    doc = {
        "schema_version":           "bsip1_v0_1",
        "file_type":                "product",
        "canonical_product_id":     f"bsip1_hardcheese_{barcode}",
        "barcode":                  barcode,
        "canonical_name_he":        name,
        "brand":                    None,
        "weight_g":                 None,
        "category":                 "hard_cheeses",
        "bsip_cheese_subpool":      subpool,
        "source_retailers":         ["yohananof"],
        "retailer_prices":          {"yohananof": None},
        "image_url":                product.get("image_url"),
        "fat_per_100g_scored":      nn.get("fat_g"),
        "fat_in_dry_matter_pct":    None,
        "both_fat_values_on_label": False,
        "fat_label_documentation":  None,
        "normalized_nutrition_per_100g": nn,
        "energy_kcal":              nn.get("energy_kcal"),
        "fat_g":                    nn.get("fat_g"),
        "fat_saturated_g":          nn.get("fat_saturated_g"),
        "fat_trans_g":              None,
        "protein_g":                nn.get("protein_g"),
        "carbohydrates_g":          nn.get("carbohydrates_g"),
        "sugars_g":                 nn.get("sugars_g"),
        "sodium_mg":                nn.get("sodium_mg"),
        "dietary_fiber_g":          None,
        "calcium_mg":               None,
        "ingredients_text_he":      ing_text if ing_text else None,
        "ingredients_list":         ing_list,
        "ingredient_count":         len(ing_list),
        "ingredient_text_quality":  "good" if len(ing_list) >= 2 else ("present" if ing_text else "absent"),
        "allergens_contains":       allergens,
        "allergens_may_contain":    [],
        "confidence":               trust_score,
        "canonical_trust_level":    trust_lvl,
        "canonical_trust_score":    trust_score,
        "conflicts_summary":        [],
        "missing_fields":           missing,
        "inferred_fields":          [],
        "audit_ref":                None,
        "nova_proxy":               nova_result["nova_proxy"],
        "nova_confidence":          nova_result["nova_confidence"],
        "nova_confidence_band":     nova_result["nova_confidence_band"],
        "nova_notes":               nova_result["nova_notes"],
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

    enriched   = []
    skipped    = []
    subpool_dist = {}
    nova_dist    = {}

    for p in products:
        if p.get("data_sufficiency") != "sufficient":
            skipped.append({
                "barcode": p.get("barcode"),
                "name":    p.get("product_name_he"),
                "reason":  "data_sufficiency != sufficient",
            })
            continue

        # Additional check: must have energy_kcal > 0
        nutrition = p.get("nutrition") or {}
        kcal = nutrition.get("energy_kcal")
        fat  = nutrition.get("fat_g")
        prot = nutrition.get("protein_g")
        if kcal is None or kcal == 0.0 or fat is None or prot is None:
            skipped.append({
                "barcode": p.get("barcode"),
                "name":    p.get("product_name_he"),
                "reason":  f"missing core nutrition: energy_kcal={kcal} fat_g={fat} protein_g={prot}",
            })
            continue

        doc = build_bsip1(p, ts)
        out_path = OUTPUT_DIR / f"bsip1_hardcheese_{doc['barcode']}.json"
        out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        enriched.append(doc)
        print(f"  ENRICHED: {doc['barcode']} — {doc['canonical_name_he']} [{doc['bsip_cheese_subpool']}] NOVA {doc['nova_proxy']}")

        sp = doc["bsip_cheese_subpool"]
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
