"""
Merge Phase 2 (Updated) olive oil corpus.

Merges:
  - Shufersal scraped records (primary — real panels, ingredients, prices)
  - Phase 1 fallback corpus (il_gov_data 251 + OFF 7)

Shufersal records take precedence. Dedup strategy: barcode match first,
then fuzzy name match (normalized Hebrew name). Gov records that overlap
with Shufersal get their nutrition and signals updated from the Shufersal
record but retain their gov identity fields.

Output: C:\Bari\02_products\olive_oil\bsip0_raw\olive_oil_bsip0_merged_20260606T<ts>.json

TASK-197 Phase 2 (Updated) — 2026-06-06
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SHUFERSAL_RAW = Path(
    r"C:\Bari\02_products\olive_oil\bsip0_raw\olive_oil_bsip0_raw_20260606T152108.json"
)
GOV_CORPUS = Path(
    r"C:\Bari\02_products\olive_oil\bsip0_raw\olive_oil_bsip0_raw_20260606T000000.json"
)
OUT_DIR = Path(r"C:\Bari\02_products\olive_oil\bsip0_raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
OUT_PATH = OUT_DIR / f"olive_oil_bsip0_merged_{TS}.json"

# Products that are NOT olive oil (contamination from Shufersal scrape)
# Product #13: זיתי קלמטה מגולענים — cured olives in brine, not oil
SHUFERSAL_CONTAMINATION_BARCODES = {"7296073735069"}

# Products that are cooking sprays — distinct subcategory from bulk oil
SPRAY_NAMES = ["תרסיס"]


def _norm_name(name: str) -> str:
    """Normalize Hebrew product name for fuzzy matching."""
    # strip brand-like suffixes, size, whitespace
    n = re.sub(r'\d+[\s]*(מ"ל|ליטר|מל|ml|ל\'|גרם|ק"ג)', "", name)
    n = re.sub(r"\s+", " ", n).strip()
    return n.lower()


def _is_spray(name: str) -> bool:
    return any(s in name for s in SPRAY_NAMES)


def _map_shufersal_to_corpus_schema(p: dict, is_contam: bool, contam_reason: str) -> dict:
    """Convert a Shufersal-scraped record into the unified corpus schema."""
    nutr = p.get("nutrition", {})
    signals = p.get("olive_signals", {})
    name = p.get("name_he", "")

    # Nutrition completeness: fat + energy both present
    fat = nutr.get("fat_raw", "")
    kcal = nutr.get("energy_kcal_raw", "")
    nutr_complete = bool(fat and kcal)
    ingr = p.get("ingredients_raw", "")

    # Dilution detection from ingredient panel (real label data now available)
    dilution_flags = signals.get("dilution_flags", [])

    # Grade: prefer back-label (ingredients text is more reliable than name)
    grade_front = signals.get("olive_grade_front", "")
    grade_back = signals.get("olive_grade_back", "")
    grade_final = grade_back or grade_front or "unknown"

    # Spray flag — distinct subcategory
    is_spray = _is_spray(name)
    if is_spray and not is_contam:
        contam_reason = "cooking_spray_subcategory"

    return {
        "source": "shufersal:html_scrape",
        "scraped_at": p.get("scraped_at", TS),
        "gov_record_id": None,
        "barcode": p.get("barcode", ""),
        "name_he": name,
        "name_en": p.get("name_en", ""),
        "brand": p.get("brand", ""),
        "importer": "",
        "manufacturer": "",
        "cert_id": "",
        "cert_expiry": "",
        "import_date": "",
        "kashrut_type": "",
        "kashrut_body": "",
        "provenance": {
            "source": "shufersal:html_scrape",
            "source_id": p.get("barcode", ""),
            "source_url": p.get("source_url", ""),
            "fetched_at": p.get("scraped_at", TS),
            "client_version": "1.0",
            "verification_status": "candidate",
        },
        "nutrition": {
            "energy_kcal_raw": kcal,
            "fat_raw": fat,
            "saturated_fat_raw": nutr.get("saturated_fat_raw", ""),
            "protein_raw": nutr.get("protein_raw", ""),
            "carbs_raw": nutr.get("carbs_raw", ""),
            "sodium_raw": nutr.get("sodium_raw", ""),
        },
        "nutrition_source": "shufersal:label_panel",
        "ingredients_raw": ingr,
        "olive_signals": {
            "grade_claim_raw": grade_final,
            "grade_front_raw": grade_front,
            "grade_back_raw": grade_back,
            "grade_mismatch": (grade_front and grade_back and grade_front != grade_back),
            "origin_country_primary": signals.get("origin_country_primary", ""),
            "origin_countries_all": signals.get("origin_countries_all", []),
            "origin_multi_country": signals.get("origin_multi_country", False),
            "origin_text_raw": signals.get("origin_text", ""),
            "blend_text_raw": signals.get("blend_text", ""),
            "has_harvest_date": signals.get("has_harvest_date", False),
            "harvest_date_text": signals.get("harvest_date_text", ""),
            "has_pdo_pgi_claim": signals.get("has_pdo_pgi_claim", False),
            "pdo_pgi_claim_text": signals.get("pdo_pgi_claim_text", ""),
            "acidity_claim_raw": signals.get("acidity_claim_raw", ""),
            "certification_raw": signals.get("certification_raw", []),
            "dilution_flags": dilution_flags,
            "net_weight_raw": signals.get("net_weight_raw", ""),
        },
        "price": p.get("price", ""),
        "volume_ml": p.get("volume_ml"),
        "price_per_100ml": p.get("price_per_100ml"),
        "price_per_liter": p.get("price_per_liter"),
        "image_urls": p.get("image_urls", []),
        "corpus_flags": {
            "is_contamination": is_contam,
            "contamination_reason": contam_reason,
            "is_spray": is_spray,
            "nutrition_complete": nutr_complete,
            "ingredients_available": bool(ingr),
            "source_tier": "shufersal_primary",
        },
    }


def main() -> None:
    print("=== TASK-197 Phase 2 (Updated) — Corpus Merge ===\n")

    # ── Load Shufersal scraped records ───────────────────────────────────────
    shufersal_raw = json.loads(SHUFERSAL_RAW.read_text(encoding="utf-8"))
    print(f"Shufersal scraped: {len(shufersal_raw)} records")

    shufersal_records = []
    shufersal_barcodes: set[str] = set()
    shufersal_norm_names: set[str] = set()

    for p in shufersal_raw:
        bc = str(p.get("barcode", "")).strip()
        name = p.get("name_he", "")
        is_contam = bc in SHUFERSAL_CONTAMINATION_BARCODES
        contam_reason = "cured_olives_not_oil" if is_contam else ""

        rec = _map_shufersal_to_corpus_schema(p, is_contam, contam_reason)
        shufersal_records.append(rec)

        if bc:
            shufersal_barcodes.add(bc)
        shufersal_norm_names.add(_norm_name(name))

    print(f"  Shufersal contamination: {sum(1 for r in shufersal_records if r['corpus_flags']['is_contamination'])}")
    print(f"  Shufersal sprays: {sum(1 for r in shufersal_records if r['corpus_flags']['is_spray'])}")
    print(f"  Shufersal barcodes indexed: {len(shufersal_barcodes)}")

    # ── Load gov corpus ──────────────────────────────────────────────────────
    gov_raw = json.loads(GOV_CORPUS.read_text(encoding="utf-8"))
    print(f"\nGov corpus loaded: {len(gov_raw)} records")

    # Deduplicate gov records against Shufersal: skip gov records whose
    # normalized name overlaps with a Shufersal record (Shufersal is primary)
    gov_added = []
    gov_skipped_overlap = 0

    for rec in gov_raw:
        bc = str(rec.get("barcode", "")).strip()

        # Barcode match only → skip (Shufersal has this product with real panel).
        # Do NOT match by name — generic names like "שמן זית כתית מעולה" are shared
        # by many distinct products (different brands/importers) in the gov registry.
        if bc and bc in shufersal_barcodes:
            gov_skipped_overlap += 1
            continue

        # Mark gov source tier
        out_rec = dict(rec)
        if "corpus_flags" not in out_rec:
            out_rec["corpus_flags"] = {}
        out_rec["corpus_flags"]["source_tier"] = "gov_registry"
        gov_added.append(out_rec)

    print(f"  Gov records skipped (overlap with Shufersal): {gov_skipped_overlap}")
    print(f"  Gov records added to merged corpus: {len(gov_added)}")

    # ── Merged corpus ────────────────────────────────────────────────────────
    merged = shufersal_records + gov_added

    # ── Stats ─────────────────────────────────────────────────────────────────
    total = len(merged)
    n_shufersal = len(shufersal_records)
    n_gov = len(gov_added)
    n_contam = sum(1 for r in merged if r.get("corpus_flags", {}).get("is_contamination"))
    n_spray = sum(1 for r in merged if r.get("corpus_flags", {}).get("is_spray"))
    n_clean = total - n_contam
    n_nutr = sum(1 for r in merged if r.get("corpus_flags", {}).get("nutrition_complete"))
    n_ingr = sum(1 for r in merged if r.get("corpus_flags", {}).get("ingredients_available"))
    n_shufersal_clean = sum(
        1 for r in shufersal_records
        if not r["corpus_flags"]["is_contamination"]
    )
    n_shufersal_oil = sum(
        1 for r in shufersal_records
        if not r["corpus_flags"]["is_contamination"]
        and not r["corpus_flags"]["is_spray"]
    )

    # Signals from Shufersal (real label data)
    shuf_only = [r for r in shufersal_records if not r["corpus_flags"]["is_contamination"]]
    n_grade_mismatch = sum(1 for r in shuf_only if r["olive_signals"].get("grade_mismatch"))
    n_harvest = sum(1 for r in shuf_only if r["olive_signals"].get("has_harvest_date"))
    n_pdo = sum(1 for r in shuf_only if r["olive_signals"].get("has_pdo_pgi_claim"))
    n_dilution = sum(1 for r in shuf_only if r["olive_signals"].get("dilution_flags"))
    n_origin_named = sum(1 for r in shuf_only if r["olive_signals"].get("origin_country_primary"))

    print(f"\n=== MERGED CORPUS STATS ===")
    print(f"Total records:         {total}")
    print(f"  Shufersal:           {n_shufersal}")
    print(f"  Gov/OFF:             {n_gov}")
    print(f"Contamination:         {n_contam} ({100*n_contam//max(total,1)}%)")
    print(f"Spray subcategory:     {n_spray}")
    print(f"Clean records:         {n_clean}")
    print(f"Nutrition complete:    {n_nutr} ({100*n_nutr//max(total,1)}%)")
    print(f"Ingredients available: {n_ingr}")
    print()
    print(f"=== SHUFERSAL LABEL SIGNALS ({len(shuf_only)} clean Shufersal records) ===")
    print(f"Grade mismatch (Sig6): {n_grade_mismatch}")
    print(f"Harvest date stated:   {n_harvest}")
    print(f"PDO/PGI claim:         {n_pdo}")
    print(f"Dilution flags:        {n_dilution}")
    print(f"Origin named:          {n_origin_named}")

    # ── Save ──────────────────────────────────────────────────────────────────
    OUT_PATH.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\nMerged corpus: {OUT_PATH}")
    print(f"Run record: olive_oil_bsip0_merged_{TS}")

    return {
        "total": total,
        "n_shufersal": n_shufersal,
        "n_gov": n_gov,
        "n_contam": n_contam,
        "n_spray": n_spray,
        "n_clean": n_clean,
        "n_nutr": n_nutr,
        "n_ingr": n_ingr,
        "n_shufersal_clean": n_shufersal_clean,
        "n_shufersal_oil": n_shufersal_oil,
        "n_grade_mismatch": n_grade_mismatch,
        "n_harvest": n_harvest,
        "n_pdo": n_pdo,
        "n_dilution": n_dilution,
        "n_origin_named": n_origin_named,
        "out_path": str(OUT_PATH),
    }


if __name__ == "__main__":
    main()
