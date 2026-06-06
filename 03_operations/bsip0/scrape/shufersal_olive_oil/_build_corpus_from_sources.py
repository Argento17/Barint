"""
Build olive oil corpus from available sources (gov + OFF).
Run as: python _build_corpus_from_sources.py
TASK-197 Phase 2 — fallback when Shufersal storefront is blocked.
"""
import sys
import json
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari")

from integrations.clients.il_gov_data import query
from integrations.clients.open_food_facts import get_product

ts = datetime.utcnow().isoformat()

DILUTION_SIGNALS = [
    "שמן חמניות", "sunflower", "שמן קנולה", "canola", "rapeseed",
    "שמן סויה", "soybean", "שמן תירס", "corn oil",
    "שמן דקלים", "palm oil", "שמן דקל", "palm kernel",
    "שמן כותנה", "cottonseed", "שמן בוטנים", "groundnut", "peanut oil",
]


def detect_grade(name_he: str, name_en: str) -> str:
    combined = (name_he + " " + name_en).lower()
    if "כתית מעולה" in combined or "extra virgin" in combined:
        return "extra_virgin"
    elif "מעורב" in combined or "blend" in combined or "מזוכך" in combined or "refined" in combined:
        return "refined_blend"
    elif "כתית" in combined or "virgin" in combined:
        return "virgin"
    return "unknown"


def main():
    corpus = []

    # ── Source 1: il_gov_data imported foods ─────────────────────────────────
    print("Pulling il_gov_data imported foods...")
    gov_results = query("imported_foods", "שמן זית", limit=300)
    gov_records = gov_results.records
    print(f"  Gov records: {len(gov_records)}")

    for r in gov_records:
        name_he = r.get("name4", "")
        name_en = r.get("name5", "")
        country = r.get("name2", "")
        combined_name = (name_he + " " + name_en).lower()

        # Contamination detection
        is_contamination = False
        contamination_reason = ""
        if "שמן" not in combined_name and "oil" not in combined_name:
            is_contamination = True
            contamination_reason = "no oil term in name"
        elif any(excl in combined_name for excl in [
            "חרדל", "חומץ", "מיונז", "פסולת זיתים", "pomace",
            "טחינה", "ממרח", "ריבה",
        ]):
            is_contamination = True
            contamination_reason = "excluded category (non-olive)"

        dilution_flags_name = [s for s in DILUTION_SIGNALS if s.lower() in combined_name]
        grade = detect_grade(name_he, name_en)

        corpus.append({
            "source": "il_gov_data:imported_foods",
            "scraped_at": ts,
            "gov_record_id": r.get("_id"),
            "name_he": name_he,
            "name_en": name_en,
            "brand": "",
            "importer": r.get("name1", ""),
            "manufacturer": r.get("name6", ""),
            "cert_id": r.get("name7", ""),
            "cert_expiry": r.get("name8", ""),
            "import_date": r.get("name9", ""),
            "kashrut_type": r.get("name10", ""),
            "kashrut_body": r.get("name3", ""),
            "provenance": {
                "source": "il_gov_data:imported_foods",
                "source_id": str(r.get("_id")),
                "source_url": "https://data.gov.il/dataset/mazon",
                "fetched_at": ts,
                "client_version": "1.0",
                "verification_status": "candidate",
            },
            # Nutrition: NOT in gov data — enrichment required (OFF/USDA FDC)
            "nutrition": {
                "energy_kcal_raw": None,
                "fat_raw": None,
                "saturated_fat_raw": None,
                "protein_raw": None,
                "carbs_raw": None,
                "sodium_raw": None,
            },
            "nutrition_source": "none",
            "olive_signals": {
                "grade_claim_raw": grade,
                "origin_country_primary": country,
                "origin_countries_all": [country] if country else [],
                "origin_multi_country": False,
                "harvest_date_raw": "",
                "pdo_pgi_claim_raw": "",
                "acidity_claim_raw": "",
                "certification_raw": ["kosher"] if r.get("name10") else [],
                "dilution_flags": dilution_flags_name,
            },
            "corpus_flags": {
                "is_contamination": is_contamination,
                "contamination_reason": contamination_reason,
                "nutrition_complete": False,
                "ingredients_available": False,
            },
        })

    # ── Source 2: Open Food Facts — Israeli olive oil barcodes ───────────────
    print("Pulling OFF products (known Israeli barcodes)...")
    off_barcodes = [
        "7290003427154",  # זיתא EVOO
        "7290014692749",  # וילי פוד
        "7296073223009",  # שופרסל
        "7290002407812",  # ג'השאן
        "7290112195500",  # generic
        "7290012313011",  # קבוצת יבנה
        "7290112198044",  # רמי לוי
    ]
    for bc in off_barcodes:
        p = get_product(bc)
        if not (p and p.found):
            print(f"  {bc}: NOT FOUND in OFF")
            continue
        n = p.nutriments
        is_complete = bool(n.get("fat_100g") and n.get("energy-kcal_100g"))
        name_he = p.name or ""
        print(f"  {bc}: {name_he[:50]} | fat={n.get('fat_100g')} kcal={n.get('energy-kcal_100g')}")
        corpus.append({
            "source": "open_food_facts",
            "scraped_at": ts,
            "gov_record_id": None,
            "barcode": bc,
            "name_he": name_he,
            "name_en": "",
            "brand": p.brand or "",
            "importer": "",
            "manufacturer": "",
            "cert_id": "",
            "cert_expiry": "",
            "import_date": "",
            "kashrut_type": "",
            "kashrut_body": "",
            "provenance": {
                "source": "open_food_facts",
                "source_id": bc,
                "source_url": f"https://world.openfoodfacts.org/product/{bc}",
                "fetched_at": ts,
                "client_version": "1.0",
                "verification_status": "candidate",
            },
            "nutrition": {
                "energy_kcal_raw": str(n.get("energy-kcal_100g", "") or ""),
                "fat_raw": str(n.get("fat_100g", "") or ""),
                "saturated_fat_raw": str(n.get("saturated-fat_100g", "") or ""),
                "protein_raw": str(n.get("proteins_100g", "") or ""),
                "carbs_raw": str(n.get("carbohydrates_100g", "") or ""),
                "sodium_raw": str(n.get("sodium_100g", "") or ""),
            },
            "nutrition_source": "open_food_facts",
            "olive_signals": {
                "grade_claim_raw": "extra_virgin" if "כתית מעולה" in name_he else "unknown",
                "origin_country_primary": "",
                "origin_countries_all": [],
                "origin_multi_country": False,
                "harvest_date_raw": "",
                "pdo_pgi_claim_raw": "",
                "acidity_claim_raw": "",
                "certification_raw": ["kosher"] if any("kosher" in (l or "") for l in (p.labels or [])) else [],
                "dilution_flags": [],
            },
            "corpus_flags": {
                "is_contamination": False,
                "contamination_reason": "",
                "nutrition_complete": is_complete,
                "ingredients_available": bool(p.ingredients_text),
            },
        })

    # ── Save ──────────────────────────────────────────────────────────────────
    out_path = r"C:\Bari\02_products\olive_oil\bsip0_raw\olive_oil_bsip0_raw_20260606T000000.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    # Stats
    gov_count = sum(1 for r in corpus if r["source"] == "il_gov_data:imported_foods")
    off_count = sum(1 for r in corpus if r["source"] == "open_food_facts")
    contam = sum(1 for r in corpus if r["corpus_flags"]["is_contamination"])
    clean = sum(1 for r in corpus if not r["corpus_flags"]["is_contamination"])
    nutrition_ok = sum(1 for r in corpus if r["corpus_flags"]["nutrition_complete"])
    dilution = sum(1 for r in corpus if r["olive_signals"]["dilution_flags"])
    extra_virgin = sum(1 for r in corpus if r["olive_signals"]["grade_claim_raw"] == "extra_virgin")
    refined = sum(1 for r in corpus if r["olive_signals"]["grade_claim_raw"] == "refined_blend")

    print(f"\n=== CORPUS COMPLETE ===")
    print(f"Total records: {len(corpus)}")
    print(f"  Gov (imported_foods): {gov_count}")
    print(f"  OFF (barcode lookup): {off_count}")
    print(f"Contamination: {contam} / {len(corpus)} ({100*contam//max(len(corpus),1)}%)")
    print(f"Clean records: {clean}")
    print(f"Nutrition panels complete: {nutrition_ok} / {len(corpus)}")
    print(f"Dilution flags (from name): {dilution}")
    print(f"Grade: extra_virgin={extra_virgin}, refined_blend={refined}")
    print(f"\nOutput: {out_path}")
    return corpus


if __name__ == "__main__":
    main()
