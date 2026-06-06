"""
BSIP1 Builder — מעדנים (dairy desserts) from Shufersal BSIP0 raw.

Reads:  maadanim_bsip0_raw_*.json  (latest by mtime)
Writes: C:\Bari\03_operations\bsip1\run_maadanim_001\output\bsip1_*.json

Schema: bsip1_v0_1 — mirrors real snack bar / bread retail BSIP1 files.
Enrichment: uses core ingredient_enricher.py directly.

Pipeline responsibilities:
  1. Deduplicate raw products (barcode > name)
  2. Parse nutrition values from raw Hebrew strings
  3. Parse ingredient text → ordered list
  4. Run BSIP1 enrichment (additives / sweeteners / protein markers / etc.)
  5. Classify maadanim subtype
  6. Write one BSIP1 JSON per product + run summary
"""
from __future__ import annotations

import json
import re
import sys
import pathlib
import logging
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent.parent /
                       "bsip1" / "core"))

from ingredient_enricher import enrich as enrich_product

# Canonical BSIP0 numeric extraction (TASK-192 / EV-046) — single shared path so the
# "פחות מ N" handling + total_fat >= saturated_fat invariant never drift per-category.
sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")))
from bsip0_nutrition import (  # noqa: E402
    parse_num as _shared_parse_num,
    parse_sodium_mg as _shared_parse_sodium,
    parse_nutrition_numeric as _shared_parse_nutrition,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

RAW_DIR   = pathlib.Path(r"C:\Bari\02_products\maadanim")
OUT_DIR   = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_maadanim_001\output")
RUN_ID    = "run_maadanim_001"
SOURCE    = "shufersal"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# ── Nutrition parsing ─────────────────────────────────────────────────────────

# TASK-192 / EV-046: delegate to the canonical shared path. maadanim BSIP0 records
# carry alternate field names (energy/fat/sodium without the _raw suffix), so we first
# resolve those fallbacks into the canonical *_raw keys, then call the one shared
# extractor — preserving the historical fallback behaviour byte-for-byte while gaining
# the "פחות מ N" bound flag + total_fat >= saturated_fat invariant.
def _parse_num(raw):
    return _shared_parse_num(raw)


def _parse_sodium(raw):
    return _shared_parse_sodium(raw)


def _parse_nutrition(n: dict) -> dict:
    normalized = {
        "energy_kcal_raw":   n.get("energy_kcal_raw") or n.get("energy"),
        "fat_raw":           n.get("fat_raw") or n.get("fat"),
        "saturated_fat_raw": n.get("saturated_fat_raw"),
        "sodium_raw":        n.get("sodium_raw") or n.get("sodium") or "",
        "carbs_raw":         n.get("carbs_raw") or n.get("carbs"),
        "sugar_raw":         n.get("sugar_raw") or n.get("sugar"),
        "fiber_raw":         n.get("fiber_raw") or n.get("fiber"),
        "protein_raw":       n.get("protein_raw") or n.get("protein"),
    }
    return _shared_parse_nutrition(normalized)


# ── Ingredient parsing ─────────────────────────────────────────────────────────

_SPLIT_RE = re.compile(r"[,;،]\s*")

def _parse_ingredients(raw: str) -> list[str]:
    if not raw:
        return []
    raw = re.sub(r"\s+", " ", raw).strip()
    parts = _SPLIT_RE.split(raw)
    cleaned = []
    for p in parts:
        p = p.strip().strip(".")
        if p and len(p) > 1:
            cleaned.append(p)
    return cleaned


def _ingredient_order(ingredients_list: list[str]) -> list[dict]:
    result = []
    for i, text in enumerate(ingredients_list, 1):
        pct = None
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*%", text)
        if m:
            try:
                pct = float(m.group(1).replace(",", "."))
            except ValueError:
                pass
        has_sub = bool(re.search(r"\(", text))
        result.append({
            "position": i,
            "text": text,
            "percentage_declared": pct,
            "has_subgroup": has_sub,
        })
    return result


# ── Maadanim subtype classifier ───────────────────────────────────────────────

def _classify_subtype(name: str, claims: str = "") -> str:
    name_lower = name.lower()
    combined = name_lower + " " + claims.lower()

    if any(k in name_lower for k in ["חלבון", "פרוטאין", "protein", "high protein"]):
        return "protein_dessert"
    if any(k in name_lower for k in ["ילדים", "ילד", "kids", "קידס"]):
        return "kids_dessert"
    if any(k in name_lower for k in ["ללא סוכר", "דל סוכר", "zero sugar", "light"]):
        return "reduced_sugar_dessert"
    if any(k in name_lower for k in ["פרוביו", "probiotic", "פרוביוטי"]):
        return "probiotic_dessert"
    if any(k in name_lower for k in ["מוס"]):
        return "mousse_dessert"
    if any(k in name_lower for k in ["פודינג", "pudding"]):
        return "pudding_dessert"
    if any(k in name_lower for k in ["מילקי"]):
        return "milky_style"
    if any(k in name_lower for k in ["עדנה"]):
        return "adina_style"
    if any(k in name_lower for k in ["יופלה"]):
        return "flavored_yogurt_dessert"
    if any(k in name_lower for k in ["קרם", "cream"]):
        return "cream_dessert"
    if any(k in name_lower for k in ["פנה קוטה", "קרם ברולה", "panna"]):
        return "patisserie_dessert"
    return "dairy_dessert_generic"


# ── Confidence ────────────────────────────────────────────────────────────────

def _compute_confidence(p: dict, nn: dict, ingr_list: list[str]) -> dict:
    nutr_fields = ["energy_kcal", "protein_g", "sugars_g", "fat_g", "carbohydrates_g"]
    n_present = sum(1 for f in nutr_fields if nn.get(f) is not None)
    nutr_ok = n_present >= 3

    ingr_ok = len(ingr_list) >= 2

    if nutr_ok and ingr_ok:
        nutr_conf = "confirmed_per_100g"
        id_conf   = "high"
        trust     = 0.80
        trust_lvl = "high"
    elif nutr_ok:
        nutr_conf = "confirmed_per_100g"
        id_conf   = "medium"
        trust     = 0.65
        trust_lvl = "medium"
    else:
        nutr_conf = "partial"
        id_conf   = "low"
        trust     = 0.45
        trust_lvl = "low"

    missing = []
    if not nutr_ok:
        missing.extend(f for f in nutr_fields if nn.get(f) is None)
    if not ingr_ok:
        missing.append("ingredients_list")

    return {
        "confidence": {
            "identity_confidence": id_conf,
            "barcode_confidence": "inferred",
            "nutrition_confidence": nutr_conf,
            "matched_by": "barcode_single_source",
            "observation_count": 1,
        },
        "canonical_trust_score": trust,
        "canonical_trust_level": trust_lvl,
        "missing_fields": missing,
        "nutrition_consistency_status": "consistent" if nutr_ok else "partial",
    }


# ── Main builder ──────────────────────────────────────────────────────────────

def _find_latest_raw() -> pathlib.Path | None:
    candidates = sorted(RAW_DIR.glob("maadanim_bsip0_raw_*.json"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def build_bsip1(raw_products: list[dict]) -> tuple[int, int, int]:
    """Build BSIP1 files. Returns (written, skipped, errors)."""
    seen_barcodes: set[str] = set()
    written = skipped = errors = 0

    for raw in raw_products:
        name = raw.get("name_he", "").strip()
        if not name:
            skipped += 1
            continue

        # Deduplicate
        barcode_raw = str(raw.get("barcode", "")).strip() or re.sub(r"[^a-zA-Z0-9]", "", name)[:20]
        barcode = re.sub(r"[^a-zA-Z0-9_\-]", "_", barcode_raw)
        if not barcode:
            skipped += 1
            continue

        dedup_key = barcode
        if dedup_key in seen_barcodes:
            skipped += 1
            continue
        seen_barcodes.add(dedup_key)

        pid = f"bsip1_maadanim_{barcode}"

        # Nutrition
        nn = _parse_nutrition(raw.get("nutrition", {}))

        # Ingredients
        ingr_text = raw.get("ingredients_raw", "").strip()
        ingr_list = _parse_ingredients(ingr_text)

        # Confidence
        conf_block = _compute_confidence(raw, nn, ingr_list)

        # Subtype
        subtype = _classify_subtype(name, raw.get("claims_raw", ""))

        # Build base record
        record: dict = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": pid,
            "barcode": barcode_raw,
            "canonical_name_he": name,
            "canonical_name_en": None,
            "brand": raw.get("brand", ""),
            "package_size_g": raw.get("weight_g"),
            "unit_count": None,
            "unit_size_g": None,
            "serving_size_g": None,
            "country_of_origin": "ישראל",
            "kosher_certification": None,
            "image_url": (raw.get("image_urls") or [None])[0],
            "image_urls": raw.get("image_urls", []),
            "source_retailers": [SOURCE],
            "source_url": raw.get("source_url", ""),
            "normalized_nutrition_per_100g": nn,
            "energy_source_unit": "kcal",
            "ingredients_text_he": ingr_text,
            "ingredients_list": ingr_list,
            "ingredients_raw": ingr_text,
            "ingredients_raw_provenance": {
                "source": "bsip0_scrape",
                "bsip0_status": "bsip0_scrape",
                "populated_at": "bsip1_build_maadanim_001",
                "missing": not bool(ingr_text),
                "note": "Scraped from Shufersal product page",
            },
            "ingredient_order": _ingredient_order(ingr_list),
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims_raw": raw.get("claims_raw", ""),
            "claims": [],
            "confidence": conf_block["confidence"],
            "barcode_validation_status": "retailer_internal_id",
            "barcode_confidence_reason": "Shufersal product code used as barcode proxy.",
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf_block["nutrition_consistency_status"],
            "nutrition_consistency_warnings": [],
            "ingredient_text_quality": "clean" if ingr_text else "missing",
            "ingredient_warnings": [],
            "canonical_trust_score": conf_block["canonical_trust_score"],
            "canonical_trust_level": conf_block["canonical_trust_level"],
            "canonical_risk_flags": ["single_source_only", "retailer_internal_id_barcode"],
            "conflicts_summary": {
                "count": 0, "has_unresolved": False,
                "fields_in_conflict": [], "identity_conflicts": [],
                "nutrition_conflicts": [], "ingredient_conflicts": [],
                "labeling_conflicts": [], "completeness_conflicts": [],
            },
            "missing_fields": conf_block["missing_fields"],
            "inferred_fields": [],
            "audit_ref": f"bsip1_audit_{barcode}.json",
            "bsip_maadanim_subtype": subtype,
            "price": raw.get("price", ""),
            "price_per_100g": raw.get("price_per_100g"),
            "acquisition_query": raw.get("acquisition_query", ""),
        }

        # Run enrichment
        try:
            record = enrich_product(record)
        except Exception as e:
            log.warning("Enrichment error for %s: %s", pid, e)
            # Add stub enrichment fields so BSIP2 doesn't crash
            for field in ["extracted_additives", "extracted_flavors", "extracted_sweeteners",
                          "extracted_protein_markers", "extracted_matrix_markers",
                          "extracted_fermentation_markers", "extracted_roasting_markers"]:
                if field not in record:
                    record[field] = []
            if "enrichment_summary" not in record:
                record["enrichment_summary"] = {
                    "ingredient_count_parsed": len(ingr_list),
                    "additive_count": 0, "flavor_marker_count": 0,
                    "sweetener_count": 0, "protein_marker_count": 0,
                    "matrix_marker_count": 0, "fermentation_marker_count": 0,
                    "has_live_cultures": False, "has_flavor_descriptor": False,
                    "has_prebiotic_fiber": False, "has_protein_isolate_or_concentrate": False,
                }
            record["enrichment_version"] = "bsip1_enrichment_v1"
            record["enrichment_warnings"] = [f"enrichment_error: {e}"]

        out_path = OUT_DIR / f"bsip1_{barcode}.json"
        try:
            out_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
            written += 1
        except Exception as e:
            log.error("Write error for %s: %s", pid, e)
            errors += 1

    return written, skipped, errors


def write_run_summary(raw_products: list[dict], written: int, skipped: int, errors: int) -> None:
    n_nutr = sum(1 for p in raw_products if p.get("nutrition", {}).get("energy_kcal_raw"))
    n_ingr = sum(1 for p in raw_products if p.get("ingredients_raw"))
    n_img  = sum(1 for p in raw_products if p.get("image_urls"))
    bsip1_files = list(OUT_DIR.glob("bsip1_*.json"))

    lines = [
        f"# BSIP1 Maadanim Run Summary — {RUN_ID}",
        f"\n**Built:** {datetime.now().isoformat()}",
        f"**Source:** Shufersal BSIP0 raw scrape",
        f"**Raw products:** {len(raw_products)}",
        f"**BSIP1 files written:** {written}",
        f"**Skipped (duplicate/empty):** {skipped}",
        f"**Errors:** {errors}",
        f"**BSIP1 files in output dir:** {len(bsip1_files)}",
        "",
        "## Coverage",
        "",
        f"| Field | Count | % |",
        f"|-------|-------|---|",
        f"| Nutrition (energy_kcal) | {n_nutr} | {100*n_nutr//max(len(raw_products),1)}% |",
        f"| Ingredients raw | {n_ingr} | {100*n_ingr//max(len(raw_products),1)}% |",
        f"| Images | {n_img} | {100*n_img//max(len(raw_products),1)}% |",
        "",
        "## Gate Assessment",
        "",
    ]

    ingr_pct = 100 * n_ingr // max(len(raw_products), 1)
    nutr_pct = 100 * n_nutr // max(len(raw_products), 1)

    if ingr_pct >= 40 and nutr_pct >= 60 and written >= 30:
        lines += [
            "**GATE: PASS** — sufficient coverage for BSIP2.",
            "",
            "- ingredients_raw coverage ≥40% ✓",
            "- nutrition coverage ≥60% ✓",
            "- product count ≥30 ✓",
        ]
    else:
        failures = []
        if ingr_pct < 40:
            failures.append(f"ingredients_raw coverage {ingr_pct}% < 40% required")
        if nutr_pct < 60:
            failures.append(f"nutrition coverage {nutr_pct}% < 60% required")
        if written < 30:
            failures.append(f"product count {written} < 30 required")
        lines += [f"**GATE: FAIL** — do NOT proceed to BSIP2 until resolved."]
        for f in failures:
            lines += [f"- FAIL: {f}"]

    report_path = OUT_DIR.parent / "run_maadanim_001_bsip1_summary.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", report_path)


def main():
    raw_path = _find_latest_raw()
    if not raw_path:
        log.error("No maadanim_bsip0_raw_*.json found in %s", RAW_DIR)
        return

    log.info("Loading raw products from %s", raw_path)
    raw_products = json.loads(raw_path.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products", len(raw_products))

    written, skipped, errors = build_bsip1(raw_products)
    log.info("Written: %d, Skipped: %d, Errors: %d", written, skipped, errors)
    write_run_summary(raw_products, written, skipped, errors)
    log.info("BSIP1 files in: %s", OUT_DIR)


if __name__ == "__main__":
    main()
