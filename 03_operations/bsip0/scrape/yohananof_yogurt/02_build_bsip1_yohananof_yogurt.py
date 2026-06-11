"""
BSIP1 Builder — Yohananof Yogurt (TASK-210 Phase B).

Source: yohananof_yogurt_bsip0_raw_*.json (il_prices + OFF panels, candidate status).
Curation reuses the SAME _curate() logic as run_yogurt_004 (byte-identical).
BSIP0 filters (F1-F4, F6) from _shared/bsip0_nutrition.py applied first.

Output: C:\Bari\03_operations\bsip1\run_yogurt_yohananof_001\output\bsip1_*.json
"""
from __future__ import annotations
import importlib.util
import json
import pathlib
import sys
from datetime import datetime, timezone

# TASK-238: Open Food Facts is BANNED. This builder consumes OFF-candidate yogurt panels
# (from the now-disabled 01_acquire_yohananof_yogurt.py) and stamps `source: open_food_facts`.
raise RuntimeError(
    "OFF is banned (TASK-238): 02_build_bsip1_yohananof_yogurt.py builds BSIP1 from Open "
    "Food Facts yogurt panels and is disabled. Re-acquire nutrition from a direct scrape; never OFF."
)

sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip1\core")))
sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")))

from bsip0_nutrition import apply_bsip0_filters, dedup_by_barcode
from ingredient_enricher import enrich as enrich_product

# Import the live curation + parse code from run_yogurt_004 builder (UNCHANGED)
SHUF_BUILDER = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\shufersal_yogurt")
spec = importlib.util.spec_from_file_location(
    "yogurt_builder_004", SHUF_BUILDER / "02_build_bsip1_yogurt_004.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

RAW_DIR = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip0_outputs")
OUT_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_yohananof_001\output")
RUN_ID = "run_yogurt_yohananof_001"
RETAILER = "yohananof"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # Find latest Yohananof raw file
    raws_files = sorted(RAW_DIR.glob("yohananof_yogurt_bsip0_raw_*.json"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
    if not raws_files:
        print(f"ERROR: No yohananof_yogurt_bsip0_raw_*.json found in {RAW_DIR}")
        return None
    raws = json.loads(raws_files[0].read_text(encoding="utf-8"))
    print(f"[{RETAILER}] Loaded {len(raws)} raw records from {raws_files[0].name}")

    # F1-F4, F6: apply BSIP0 corpus filters
    bsip0_filtered = []
    bsip0_filter_tally: dict[str, int] = {}
    for p in raws:
        fired, reasons = apply_bsip0_filters(p)
        if fired:
            for r in reasons:
                key = r.split(":")[0]
                bsip0_filter_tally[key] = bsip0_filter_tally.get(key, 0) + 1
        else:
            bsip0_filtered.append(p)
    print(f"[{RETAILER}] After BSIP0 filters: {len(bsip0_filtered)} (filtered {len(raws)-len(bsip0_filtered)})")
    print(f"  BSIP0 filter tally: {bsip0_filter_tally}")

    # F4: dedup by barcode
    dedup_result = dedup_by_barcode(bsip0_filtered)
    deduped = dedup_result["survivors"]
    dup_dropped = dedup_result["dropped"]
    print(f"[{RETAILER}] After dedup: {len(deduped)} (dropped {len(dup_dropped)} dupes)")

    # Clear stale output
    for f in OUT_DIR.glob("bsip1_*.json"):
        f.unlink()

    included, excluded = [], []
    seen = set()
    for raw in deduped:
        name = (raw.get("name_he") or "").strip()
        barcode = str(raw.get("barcode", "")).strip()
        if barcode in seen:
            excluded.append({"barcode": barcode, "name": name, "reason": "duplicate_barcode"})
            continue

        # Reuse live yogurt curation ruling (byte-identical to run_yogurt_004)
        reason = B._curate(raw)
        if reason:
            excluded.append({"barcode": barcode, "name": name, "reason": reason})
            continue
        seen.add(barcode)

        nn = B._parse_nutrition(raw.get("nutrition", {}))
        ingr_text = (raw.get("ingredients_raw") or "").strip()
        ingr_list = B._parse_ingredients(ingr_text)
        conf = B._confidence(nn, ingr_list)
        subtype = B._classify_subtype(name)
        pid = f"bsip1_yogurt_{barcode}"

        record = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": pid,
            "barcode": barcode,
            "canonical_name_he": name,
            "canonical_name_en": None,
            "brand": raw.get("brand", ""),
            "package_size_g": raw.get("weight_g"),
            "unit_count": None, "unit_size_g": None, "serving_size_g": None,
            "country_of_origin": "ישראל",
            "kosher_certification": None,
            "image_url": (raw.get("image_urls") or [None])[0],
            "image_urls": raw.get("image_urls", []),
            "source_retailers": [RETAILER],
            "source_url": raw.get("source_url", ""),
            "normalized_nutrition_per_100g": nn,
            "energy_source_unit": "kcal",
            "ingredients_text_he": ingr_text,
            "ingredients_list": ingr_list,
            "ingredients_raw": ingr_text,
            "ingredients_raw_provenance": {
                "source": "open_food_facts",
                "bsip0_status": "off_candidate",
                "populated_at": f"bsip1_build_{RUN_ID}",
                "missing": not bool(ingr_text),
                "note": "il_prices identity + OFF candidate panel (EDPG candidate, not promoted)",
            },
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims_raw": raw.get("claims_raw", ""),
            "claims": [],
            "confidence": conf["confidence"],
            "barcode_validation_status": "retailer_confirmed",
            "barcode_confidence_reason": "il_prices transparency feed barcode (law-mandated catalog).",
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf["nutrition_consistency_status"],
            "nutrition_consistency_warnings": [],
            "ingredient_text_quality": "clean" if ingr_text else "missing",
            "ingredient_warnings": [] if ingr_text else ["no_ingredient_list_in_source"],
            "canonical_trust_score": conf["canonical_trust_score"],
            "canonical_trust_level": conf["canonical_trust_level"],
            "canonical_risk_flags": ["single_source_only", "off_candidate_panel"],
            "conflicts_summary": {"count": 0, "has_unresolved": False,
                                  "fields_in_conflict": [], "identity_conflicts": [],
                                  "nutrition_conflicts": [], "ingredient_conflicts": [],
                                  "labeling_conflicts": [], "completeness_conflicts": []},
            "missing_fields": conf["missing_fields"],
            "inferred_fields": ["bsip_yogurt_subtype"],
            "audit_ref": None,
            "bsip_yogurt_subtype": subtype,
            "price": raw.get("price", ""),
            "price_per_100g": raw.get("price_per_100g"),
            "acquisition_query": raw.get("acquisition_query", ""),
            "provenance": raw.get("provenance"),
        }

        try:
            record = enrich_product(record)
        except Exception as e:
            for fld in ["extracted_additives", "extracted_flavors", "extracted_sweeteners",
                        "extracted_protein_markers", "extracted_matrix_markers",
                        "extracted_fermentation_markers", "extracted_roasting_markers"]:
                record.setdefault(fld, [])
            record.setdefault("enrichment_summary", {})
            record["enrichment_version"] = "bsip1_enrichment_v1"
            record["enrichment_warnings"] = [f"enrichment_error: {e}"]

        (OUT_DIR / f"bsip1_{barcode}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        included.append({
            "barcode": barcode, "name": name, "subtype": subtype,
            "has_ingredients": bool(ingr_text),
            "nutrition_fields": sum(1 for v in nn.values() if v is not None),
        })

    tally: dict[str, int] = {}
    for e in excluded:
        tally[e["reason"]] = tally.get(e["reason"], 0) + 1

    n_ingr = sum(1 for i in included if i["has_ingredients"])
    report = {
        "run_id": RUN_ID,
        "retailer": RETAILER,
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_file": str(raws_files[0]),
        "raw_count": len(raws),
        "bsip0_filter_count": len(raws) - len(bsip0_filtered),
        "bsip0_filter_tally": bsip0_filter_tally,
        "dedup_dropped": len(dup_dropped),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "exclusion_tally": tally,
        "ingredient_coverage": f"{n_ingr}/{len(included)}",
        "included": included,
        "excluded": excluded,
    }
    (OUT_DIR.parent / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{RETAILER}] Included {len(included)}  Excluded {len(excluded)}")
    print(f"  Exclusion tally: {tally}")
    print(f"  Ingredient coverage: {n_ingr}/{len(included)}")
    return report


if __name__ == "__main__":
    main()
