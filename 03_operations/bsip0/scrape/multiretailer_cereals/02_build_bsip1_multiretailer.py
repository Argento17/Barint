"""
BSIP1 builder for the multi-retailer cereals acquisition (TASK-184).

REUSES the Shufersal builder's curation + governance-construct code UNCHANGED — in
particular `_curate()` which carries the EV-045/045b corpus-purity ruling under test
(ptitim/pasta/flour/bread/chocolate/drink exclusions + 150 kcal energy floor + the
Hebrew word-boundary yeast trap שמרים != משמרים). We import those functions rather than
copy them, so this run validates the *exact* live ruling, not a fork of it.

Per retailer it writes BSIP1 product files to run_cereals_<retailer>_001/output and a
curation_report.json with the per-reason exclusion tally (the contaminant tally the task
asks for). Engine/curation byte-identical to the Shufersal path.
"""
from __future__ import annotations

import json
import sys
import pathlib
from datetime import datetime, timezone

SHUF_BUILDER = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\shufersal_cereals")
sys.path.insert(0, str(SHUF_BUILDER))
sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip1\core")))

# Import the live curation + construct code UNCHANGED (the ruling under test).
import importlib.util
spec = importlib.util.spec_from_file_location(
    "shuf_cereals_builder", SHUF_BUILDER / "02_build_bsip1_cereals.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

RAW_DIR = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs\multiretailer")


def build_retailer(retailer: str):
    raws_files = sorted(RAW_DIR.glob(f"{retailer}_bsip0_raw_*.json"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
    if not raws_files:
        print(f"[{retailer}] no raw file — skipping")
        return None
    raws = json.loads(raws_files[0].read_text(encoding="utf-8"))
    run_id = f"run_cereals_{retailer}_001"
    out_dir = pathlib.Path(rf"C:\Bari\03_operations\bsip1\{run_id}\output")
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob("bsip1_*.json"):
        f.unlink()

    from ingredient_enricher import enrich as enrich_product

    included, excluded = [], []
    seen = set()
    for raw in raws:
        name = (raw.get("name_he") or "").strip()
        barcode = str(raw.get("barcode", "")).strip()
        if barcode in seen:
            excluded.append({"barcode": barcode, "name": name, "reason": "duplicate_barcode"})
            continue
        reason = B._curate(raw)                      # <-- EV-045/045b ruling, UNCHANGED
        if reason:
            excluded.append({"barcode": barcode, "name": name, "reason": reason})
            continue
        seen.add(barcode)

        nn = B._parse_nutrition(raw.get("nutrition", {}))
        ingr_text = (raw.get("ingredients_raw") or "").strip()
        ingr_list = B._parse_ingredients(ingr_text)
        claims = ""  # OFF path carries no claims_raw
        serving_g = raw.get("serving_size_g_hint")
        conf = B._confidence(nn, ingr_list)
        subtype = B._classify_subtype(name, ingr_text)
        pid = f"bsip1_cereal_{barcode}"

        record = {
            "schema_version": "bsip1_v0_1", "file_type": "product",
            "canonical_product_id": pid, "barcode": barcode,
            "canonical_name_he": name, "canonical_name_en": None,
            "brand": raw.get("brand", ""), "package_size_g": raw.get("weight_g"),
            "unit_count": None, "unit_size_g": None, "serving_size_g": serving_g,
            "country_of_origin": "ישראל", "kosher_certification": None,
            "image_url": (raw.get("image_urls") or [None])[0],
            "image_urls": raw.get("image_urls", []),
            "source_retailers": [retailer], "source_url": raw.get("source_url", ""),
            "normalized_nutrition_per_100g": nn, "energy_source_unit": "kcal",
            "ingredients_text_he": ingr_text, "ingredients_list": ingr_list,
            "ingredients_raw": ingr_text,
            "ingredients_raw_provenance": {
                "source": "open_food_facts", "bsip0_status": "off_candidate",
                "populated_at": f"bsip1_build_{run_id}", "missing": not bool(ingr_text),
                "note": "il_prices identity + OFF candidate panel (EDPG candidate, not promoted)",
            },
            "allergens_contains": [], "allergens_may_contain": [],
            "claims_raw": claims, "claims": [],
            "confidence": conf["confidence"],
            "barcode_validation_status": "retailer_confirmed",
            "barcode_confidence_reason": "il_prices transparency feed barcode (law-mandated catalog).",
            "nutrition_basis_claimed": "ל-100 גרם", "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf["nutrition_consistency_status"],
            "data_sufficiency": conf["data_sufficiency"],
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
            "inferred_fields": ["bsip_cereal_subtype"], "audit_ref": None,
            "bsip_cereal_subtype": subtype,
            "price": raw.get("price", ""), "price_per_100g": raw.get("price_per_100g"),
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

        ingredient_order = record.get("ingredient_order", [])
        wg = B._whole_grain_construct(name, claims, ingr_text, ingredient_order)
        gr = B._granola_construct(name, ingr_text, subtype, nn)
        ch = B._childrens_construct(name, ingr_text, serving_g)
        fortified = B._fortification_flag(ingr_text, ingr_text)
        record["cereals_governance"] = {
            "construct_1_granola_subpool": gr,
            "construct_2_childrens": ch,
            "construct_3_whole_grain": wg,
            "construct_4_fortification_flag": {"fortified": fortified,
                "evidence_ref": "cereals_gap_resolution_v1 Sec 6.4 (Resolution 2, DISTORTION-004)"},
        }
        # EV-045c — Nestlé Fitness savory-cracker guard (flag-not-drop, curation only) — UNCHANGED ruling
        ev045c = B.fitness_noncereal_flag(name, ingr_text, nn)
        if ev045c:
            record["cereals_governance"]["ev_045c_fitness_noncereal_flag"] = ev045c
            record.setdefault("canonical_risk_flags", []).append("fitness_savory_cracker_suspect")
        (out_dir / f"bsip1_{barcode}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        included.append({"barcode": barcode, "name": name, "subtype": subtype,
            "has_ingredients": bool(ingr_text),
            "nutrition_fields": sum(1 for v in nn.values() if v is not None),
            "data_sufficiency": conf["data_sufficiency"], "subpool": gr["subpool"],
            "ev_045c_flag": bool(ev045c),
            "ev_045c_triggers": (ev045c or {}).get("triggers")})

    tally = {}
    for e in excluded:
        tally[e["reason"]] = tally.get(e["reason"], 0) + 1
    ev045c_flagged = [i for i in included if i.get("ev_045c_flag")]
    report = {"run_id": run_id, "retailer": retailer,
              "generated": datetime.now(timezone.utc).isoformat(),
              "source_file": str(raws_files[0]), "raw_count": len(raws),
              "included_count": len(included), "excluded_count": len(excluded),
              "exclusion_tally": tally,
              "ev_045c_fitness_flag_count": len(ev045c_flagged),
              "ev_045c_flagged": [{"barcode": i["barcode"], "name": i["name"],
                                   "triggers": i.get("ev_045c_triggers")} for i in ev045c_flagged],
              "included": included, "excluded": excluded}
    (out_dir.parent / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{retailer}] raw={len(raws)} included={len(included)} excluded={len(excluded)}")
    for r, c in sorted(tally.items(), key=lambda x: -x[1]):
        print(f"    excluded[{r}] = {c}")
    return report


if __name__ == "__main__":
    for r in ("carrefour", "yohananof"):
        build_retailer(r)
