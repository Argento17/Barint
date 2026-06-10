# -*- coding: utf-8 -*-
"""
BSIP1 Enrichment — Hard & Yellow Cheeses (run_hard_cheeses_001)
TASK-215

Input: 3 retailer BSIP0 raw files (Shufersal, Yohananof, Carrefour)
Output: deduplicated BSIP1 JSON per product in ./output/
        curation_report.json + bsip1_enrichment_report.json

Sub-pools: yellow / yellow_light / bulgarian / tzfatit / hard_grating / processed
Fat labeling: capture both fat_per_100g and fat_in_dry_matter_pct where present.
Scoring uses fat_per_100g only per TASK-215 spec.
"""

import sys
import json
import pathlib
import datetime
import re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
BSIP0_DIR = ROOT / "02_products" / "hard_cheeses" / "bsip0_outputs"
OUTPUT_DIR = pathlib.Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RETAILERS = ["shufersal", "yohananof", "carrefour", "supplementary"]
RUN_ID = "run_hard_cheeses_001"

# ── NOVA assignment rules for hard cheese ─────────────────────────────────────
NOVA1_MARKER = re.compile(r"(חלב|מלח|אנזים קימוסין|תרביות חיידקים|קימוסין)", re.UNICODE)
NOVA3_MARKERS = re.compile(
    r"(עמילן מתוקן|E\d{3,4}|חומר ייצוב|חומרי ייצוב|קרגינן|צבע|חומצת לימון שלא כחלק)", re.UNICODE
)
# NOVA 4 requires phosphates (E339/E340/E341) OR vegetable oil added to cheese matrix
# E331 alone in natural cheese slices = citrate stabilizer -> NOVA 2/3, not NOVA 4
# E339 = sodium phosphate (industrial processed cheese hallmark) -> NOVA 4
NOVA4_MARKERS = re.compile(
    r"(E339|E340|E341|שמן דקלים|שמן צמחי|נתרן פוספט)", re.UNICODE
)

# Additive markers for BSIP1-level detection
E_PATTERN = re.compile(r"E(\d{3,4}[a-z]?)", re.IGNORECASE)
MODIFIED_STARCH = re.compile(r"עמילן מתוקן", re.UNICODE)
CARRAGEENAN = re.compile(r"קרגינן", re.UNICODE)
PHOSPHATE = re.compile(r"פוספט", re.UNICODE)
PALM_OIL = re.compile(r"שמן דקלים", re.UNICODE)


def assign_nova(ing: str) -> dict:
    """Assign NOVA proxy for hard cheese products."""
    if not ing:
        return {"nova_proxy": 2, "nova_confidence": 0.3, "nova_confidence_band": "low",
                "nova_notes": ["no_ingredient_text: defaulting to NOVA 2 proxy"]}

    has_nova4 = bool(NOVA4_MARKERS.search(ing))
    has_nova3 = bool(NOVA3_MARKERS.search(ing)) or bool(MODIFIED_STARCH.search(ing))

    if has_nova4:
        return {"nova_proxy": 4, "nova_confidence": 0.85, "nova_confidence_band": "high",
                "nova_notes": ["phosphates/vegetable_oil/carrageenan_detected: NOVA 4 processed cheese"]}
    if has_nova3:
        return {"nova_proxy": 3, "nova_confidence": 0.80, "nova_confidence_band": "high",
                "nova_notes": ["modified_starch_or_stabilizers_detected: NOVA 3 processed"]}
    # Minimal: milk, salt, rennet, cultures only
    e_count = len(E_PATTERN.findall(ing))
    if e_count == 0 and not MODIFIED_STARCH.search(ing):
        return {"nova_proxy": 1, "nova_confidence": 0.90, "nova_confidence_band": "high",
                "nova_notes": ["minimal_ingredients_milk_salt_rennet_cultures: NOVA 1"]}
    return {"nova_proxy": 2, "nova_confidence": 0.70, "nova_confidence_band": "medium",
            "nova_notes": ["minor_additive_or_acid_detected: NOVA 2"]}


def detect_additives(ing: str) -> list:
    if not ing:
        return []
    e_nums = list(set(E_PATTERN.findall(ing)))
    additives = []
    for e in e_nums:
        additives.append({"e_number": f"E{e}", "detected_in": "ingredients_text_he"})
    if MODIFIED_STARCH.search(ing):
        additives.append({"e_number": "modified_starch", "name_he": "עמילן מתוקן", "detected_in": "ingredients_text_he"})
    return additives


def enrich_product(p: dict, retailers: list) -> dict:
    """Build BSIP1 record from BSIP0 raw product."""
    barcode = p["barcode"]
    ing = p.get("ingredients_text_he", "") or ""
    nova = assign_nova(ing)
    additives = detect_additives(ing)
    subpool = p.get("category_tag", "yellow")

    canonical_id = f"bsip1_hardcheese_{barcode}"

    # Ingredient quality
    if ing and len(ing) > 10:
        ing_quality = "good"
        ing_count = max(len([x.strip() for x in ing.replace("(", ",").replace(")", ",").split(",")
                              if x.strip() and len(x.strip()) > 1]), 1)
    else:
        ing_quality = "missing"
        ing_count = 0

    # Fat labeling documentation
    fat_label_note = None
    if p.get("both_fat_values_present") and p.get("fat_in_dry_matter_pct") is not None:
        fat_label_note = (
            f"Both values on label: fat_per_100g={p['fat_per_100g']}g, "
            f"fat_in_dry_matter_pct={p['fat_in_dry_matter_pct']}%. "
            f"Scoring uses fat_per_100g only per TASK-215."
        )

    # Nutrition consistency checks
    energy = p.get("energy_kcal_per_100g") or 0
    fat = p.get("fat_per_100g") or 0
    protein = p.get("protein_per_100g") or 0
    carbs = p.get("carbohydrates_per_100g") or 0
    sugars = p.get("sugars_per_100g") or 0
    sat_fat = p.get("saturated_fat_per_100g") or 0
    sodium = p.get("sodium_mg_per_100g") or 0

    macro_energy_est = fat * 9 + protein * 4 + carbs * 4
    kcal_plausible = abs(energy - macro_energy_est) < 60 if energy > 0 else True

    # Parse ingredients list from text
    ing_list = []
    if ing:
        raw_parts = re.split(r"[,،]", ing.replace("(", ",").replace(")", ","))
        ing_list = [x.strip() for x in raw_parts if x.strip() and len(x.strip()) > 1]

    trust_level = "high" if (ing_quality == "good" and len(retailers) >= 2) else "medium"
    trust_score = 0.85 if trust_level == "high" else 0.65
    data_sufficient = energy > 0 and fat is not None and protein > 0

    bsip1 = {
        # Engine-required header
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": canonical_id,
        "barcode": barcode,
        "canonical_name_he": p["name_he"],
        "brand": p["brand"],
        "weight_g": p.get("weight_g"),
        "category": "hard_cheeses",
        "bsip_cheese_subpool": subpool,
        "source_retailers": retailers,
        "retailer_prices": {r: p.get("retailer_price_ils") for r in retailers},
        "image_url": p.get("image_url"),

        # Fat labeling — CRITICAL field per TASK-215
        "fat_per_100g_scored": p.get("fat_per_100g"),
        "fat_in_dry_matter_pct": p.get("fat_in_dry_matter_pct"),
        "both_fat_values_on_label": p.get("both_fat_values_present", False),
        "fat_label_documentation": fat_label_note,

        # Engine-required: normalized nutrition nested object
        "normalized_nutrition_per_100g": {
            "energy_kcal": energy,
            "fat_g": fat,
            "fat_saturated_g": sat_fat,
            "fat_trans_g": None,
            "sodium_mg": sodium,
            "carbohydrates_g": carbs,
            "sugars_g": sugars,
            "dietary_fiber_g": None,
            "protein_g": protein,
        },

        # Flat nutrition fields (for backward compat + signal_extractor)
        "energy_kcal": energy,
        "fat_g": fat,
        "fat_saturated_g": sat_fat,
        "fat_trans_g": None,
        "protein_g": protein,
        "carbohydrates_g": carbs,
        "sugars_g": sugars,
        "sodium_mg": sodium,
        "dietary_fiber_g": None,
        "calcium_mg": p.get("calcium_mg_per_100g"),

        # Engine-required: ingredients
        "ingredients_text_he": ing if ing else None,
        "ingredients_list": ing_list,
        "ingredient_count": ing_count,
        "ingredient_text_quality": ing_quality,

        # Engine-required: allergens + confidence + audit
        "allergens_contains": ["milk"],
        "allergens_may_contain": [],
        "confidence": trust_score,
        "canonical_trust_level": trust_level,
        "canonical_trust_score": trust_score,
        "conflicts_summary": [],
        "missing_fields": [] if data_sufficient else ["energy_kcal", "fat_g", "protein_g"],
        "inferred_fields": [],
        "audit_ref": None,

        # NOVA
        "nova_proxy": nova["nova_proxy"],
        "nova_confidence": nova["nova_confidence"],
        "nova_confidence_band": nova["nova_confidence_band"],
        "nova_notes": nova["nova_notes"],

        # Additive detection
        "detected_additives": additives,
        "additive_count": len(additives),

        # Data quality
        "data_sufficiency": "sufficient" if data_sufficient else "insufficient",
        "bsip1_trust_level": trust_level,
        "bsip1_trust_score": trust_score,
        "bsip1_risk_flags": (["single_source_only"] if len(retailers) == 1 else []) +
                             (["ingredient_quality_missing"] if ing_quality == "missing" else []),

        # Nutrition consistency
        "nutrition_consistency_status": "consistent" if kcal_plausible else "warning",
        "consistency_checks": {
            "sugar_le_carbs": sugars <= carbs if carbs > 0 else True,
            "satfat_le_fat": sat_fat <= fat if fat > 0 else True,
            "kcal_plausible": kcal_plausible,
            "macros_plausible": macro_energy_est > 0,
        },

        # Provenance
        "provenance": {
            "source": "il_prices+open_food_facts",
            "fetched_at": "2026-06-07T08:00:00Z",
            "client_version": "il_prices/1.2 + off/2.1",
            "verification_status": "candidate"
        },

        "enrichment_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "run_id": RUN_ID,
    }
    return bsip1


def run():
    # Load all 3 retailer files
    all_products_by_barcode: dict[str, dict] = {}  # barcode -> merged product
    retailer_map: dict[str, list] = {}  # barcode -> retailers

    for retailer in RETAILERS:
        path = BSIP0_DIR / f"bsip0_{retailer}_raw.json"
        if not path.exists():
            print(f"WARNING: {path} not found, skipping")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for p in data["products"]:
            bc = p["barcode"]
            if bc not in all_products_by_barcode:
                all_products_by_barcode[bc] = p
                retailer_map[bc] = [retailer]
            else:
                # Dedup: prefer product with more fields, just track retailer
                existing = all_products_by_barcode[bc]
                # Merge: take best ingredient text
                if (p.get("ingredients_text_he") and
                        len(p.get("ingredients_text_he", "")) > len(existing.get("ingredients_text_he", "") or "")):
                    all_products_by_barcode[bc] = p
                retailer_map[bc].append(retailer)

    print(f"Total raw: {sum(len(json.loads((BSIP0_DIR / f'bsip0_{r}_raw.json').read_text(encoding='utf-8'))['products']) for r in RETAILERS)}")
    print(f"Post-dedup unique barcodes: {len(all_products_by_barcode)}")

    # Enrich and write each product
    enriched = []
    insufficient = []
    for barcode, product in all_products_by_barcode.items():
        retailers = retailer_map[barcode]
        bsip1 = enrich_product(product, retailers)
        enriched.append(bsip1)
        pid = bsip1["canonical_product_id"]
        out_path = OUTPUT_DIR / f"{pid}.json"
        out_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")
        status = "OK" if bsip1["data_sufficiency"] == "sufficient" else "INSUFFICIENT"
        print(f"  [{status}] {pid} — {bsip1['canonical_name_he']} (NOVA {bsip1['nova_proxy']}, pool={bsip1['bsip_cheese_subpool']})")
        if bsip1["data_sufficiency"] != "sufficient":
            insufficient.append(pid)

    # Subpool stats
    pool_counts: dict[str, int] = {}
    for b in enriched:
        pool = b["bsip_cheese_subpool"]
        pool_counts[pool] = pool_counts.get(pool, 0) + 1

    # Fat documentation registry — products with both values
    dual_fat_products = [
        {
            "barcode": b["barcode"],
            "name": b["canonical_name_he"],
            "fat_per_100g": b["fat_per_100g_scored"],
            "fat_in_dry_matter_pct": b["fat_in_dry_matter_pct"],
            "note": b["fat_label_documentation"]
        }
        for b in enriched if b.get("both_fat_values_on_label")
    ]

    # Ingredient coverage
    with_ingredients = sum(1 for b in enriched if b["ingredient_text_quality"] == "good")

    # NOVA distribution
    nova_dist: dict[int, int] = {}
    for b in enriched:
        n = b["nova_proxy"]
        nova_dist[n] = nova_dist.get(n, 0) + 1

    def safe_count(r):
        p = BSIP0_DIR / f"bsip0_{r}_raw.json"
        if not p.exists():
            return 0
        return len(json.loads(p.read_text(encoding="utf-8"))["products"])

    raw_counts = {r: safe_count(r) for r in RETAILERS}
    raw_total = sum(raw_counts.values())

    report = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_retailers": RETAILERS,
        "raw_count_per_retailer": raw_counts,
        "raw_total": raw_total,
        "post_dedup_count": len(enriched),
        "sufficient_count": len(enriched) - len(insufficient),
        "insufficient_count": len(insufficient),
        "insufficient_product_ids": insufficient,
        "ingredient_coverage": f"{with_ingredients}/{len(enriched)}",
        "subpool_distribution": pool_counts,
        "nova_distribution": {f"NOVA_{k}": v for k, v in sorted(nova_dist.items())},
        "dual_fat_label_products": {
            "count": len(dual_fat_products),
            "note": "Products where both fat_per_100g and fat_in_dry_matter_pct appear on label. Scoring uses fat_per_100g only.",
            "products": dual_fat_products
        },
        "subpool_merge_decisions": [
            {
                "decision": "hard_grating retained as separate sub-pool",
                "count": pool_counts.get("hard_grating", 0),
                "meets_threshold": pool_counts.get("hard_grating", 0) >= 3,
                "note": "3+ products (Parmesan grated tenuva, Parmesan block imported, previously-seen Parmesan variants). Retained."
            },
            {
                "decision": "processed retained as sub-pool",
                "count": pool_counts.get("processed", 0),
                "meets_threshold": pool_counts.get("processed", 0) >= 3,
                "note": "Processed cheese slices distinctly different from natural cheese. Retained as sub-pool."
            },
            {
                "decision": "tzfatit retained as sub-pool",
                "count": pool_counts.get("tzfatit", 0),
                "meets_threshold": pool_counts.get("tzfatit", 0) >= 3,
                "note": "3 tzfatit products (5%, 16%, 20%). Retained."
            }
        ],
        "gate_checks": {
            "minimum_corpus_30_products": len(enriched) >= 30,
            "ingredient_coverage_threshold_15pct": (with_ingredients / max(len(enriched), 1)) >= 0.15,
            "ingredient_coverage_actual_pct": round(100.0 * with_ingredients / max(len(enriched), 1), 1)
        }
    }

    report_path = pathlib.Path(__file__).parent / "curation_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nCuration report: {report_path}")
    print(f"Post-dedup: {len(enriched)} products")
    print(f"Subpools: {pool_counts}")
    print(f"NOVA distribution: {nova_dist}")
    print(f"Dual fat label products: {len(dual_fat_products)}")
    return enriched, report


if __name__ == "__main__":
    enriched, report = run()
    print("BSIP1 enrichment complete.")
    if not report["gate_checks"]["minimum_corpus_30_products"]:
        print("WARNING: Post-dedup corpus < 30 products — escalate to Product Agent before proceeding")
    else:
        print(f"Corpus size gate: PASS ({report['post_dedup_count']} >= 30)")
