# -*- coding: utf-8 -*-
"""
BSIP1 Enrichment — Yogurt System (TASK-515 / 515A, Stage 1)

Input:  02_products/yogurt_system/bsip0_task515/run_yogurt_task515_20260705T062308_corpus.json
        (126 BSIP0 survivors, already gated: plausibility gate + Yohananof sugar-parser
        fix applied upstream. This script does NOT re-scrape and does NOT re-run the
        plausibility gate — it consumes the gated corpus as-is.)

Output: 02_products/yogurt_system/bsip1_task515/bsip1_yogurt_<barcode>.json  (one per product)
        02_products/yogurt_system/bsip1_task515/bsip1_run_report_task515.json
        02_products/yogurt_system/bsip1_task515/excluded_products_task515.json

Scope decisions applied (reversible orchestrator defaults, per TASK-515/515A brief):
  - EXCLUDE labneh (edge_case_flag == "labneh") — Nutrition ruled labneh -> DAIRY_SOLID
    (cheese), not yogurt. Set aside, not enriched into the yogurt pages.
  - EXCLUDE cottage cheese (קוטג') if any slipped onto the yogurt shelf — cottage is
    scored in another Bari category; no double-listing.
  - Confirm 0 kefir (קפיר) products — sanity check only, BSIP0 already quarantined the
    one kefir "starter culture" non-product.
  - Keep the `subpool` field (spoonable / drinkable) intact on every surviving record so
    Stage 2+ can route spoonable -> TASK-515 and drinkable -> TASK-515A.

Hard rules respected:
  - OFF BANNED for every field. All values below come only from the already-scraped
    corpus (`nutrition` raw dict + `ingredients_raw` text). No external lookups.
  - Unparsed field = None ("data could not be retrieved"), never backfilled.
  - No re-scrape, no re-run of the BSIP0 plausibility gate, no mutation of the input file.
"""
import sys
import json
import pathlib
import datetime
import re
import hashlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── core enrichment module reuse (same module used for hard_cheeses etc.) ─────
CORE_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\core")
sys.path.insert(0, str(CORE_DIR))
from ingredient_enricher import enrich, ENRICHMENT_VERSION  # noqa: E402

# ── Paths ───────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
CORPUS_FILE = ROOT / "02_products" / "yogurt_system" / "bsip0_task515" / \
    "run_yogurt_task515_20260705T062308_corpus.json"
OUTPUT_DIR = ROOT / "02_products" / "yogurt_system" / "bsip1_task515"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RUN_ID = "run_yogurt_task515_bsip1"
CATEGORY = "yogurt_system"

# ── Ingredient-text trim markers (boilerplate that follows the true ingredient
#    list on Shufersal product pages — repeated nutrition table + legal disclaimer) ──
CUTOFF_MARKERS = [
    "ערכים תזונתיים",
    "הנתונים המדויקים",
    "יתכנו טעויות",
    "התמונות והתאריכים",
]
# Allergen-declaration sentences also sit in this trailing boilerplate block on some
# records; cut there too (declaration content is captured separately, from the FULL
# raw text, by the allergen scan below — never lost, just not left inside the
# ingredient list).
ALLERGEN_CUTOFF_MARKERS = ["מכיל חלב", "מכיל גלוטן", "מכיל סויה", "מכיל ביצים"]

# Stray-artifact fix: a lost "\n" occasionally survives as a literal "n" glued to the
# following digit/space (e.g. "ביפידוס.n20 גרם חלבון..."). Only fires on the narrow
# ". n" / ".n<digit>" pattern — never touches real Hebrew content.
STRAY_N_RE = re.compile(r"\.\s*n(?=\s|\d)")

ALLERGEN_SCAN = [
    ("חלב", "milk"),
    ("קזאין", "milk"),
    ("מי גבינה", "milk"),
    ("גלוטן", "gluten"),
    ("קמח חיטה", "gluten"),
    ("קמח שיפון", "gluten"),
    ("שיפון", "gluten"),
    ("שעורה", "gluten"),
    ("סויה", "soy"),
    ("לציטין סויה", "soy"),
    ("ביצה", "egg"),
    ("ביצים", "egg"),
    ("אלבומין", "egg"),
    ("ג'לטין דגים", "fish"),
    ("דגים", "fish"),
    ("אגוז", "tree_nuts"),
    ("שקד", "tree_nuts"),
    ("בוטן", "peanut"),
    ("שומשום", "sesame"),
]

NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")


# ── Schema normalization (corpus mixes 2 BSIP0 record shapes — see Finding 1 below) ──
def get_name_he(p):
    return (p.get("name_he") or p.get("name") or None)


def get_name_en(p):
    v = p.get("name_en")
    return v if v else None


def get_brand(p):
    v = p.get("brand")
    return v if v else None


def get_image_urls(p):
    return p.get("image_urls") or []


def get_source_url(p):
    return p.get("source_url")


def get_price(p):
    v = p.get("price")
    if v in (None, ""):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def get_weight_g(p):
    return p.get("weight_g")


# ── Nutrition parsing ──────────────────────────────────────────────────────
def parse_float(v):
    if v is None:
        return None
    s = str(v).strip()
    if s == "":
        return None
    if not NUM_RE.match(s):
        return None
    return float(s)


def parse_sodium_mg(v):
    if v is None:
        return None
    s = str(v).strip()
    if s == "":
        return None
    s = s.replace("מג", "").strip()
    if not NUM_RE.match(s):
        return None
    return float(s)


def build_normalized_nutrition(nutrition_raw: dict) -> dict:
    n = nutrition_raw or {}
    return {
        "energy_kcal":     parse_float(n.get("energy_kcal_raw")),
        "fat_g":           parse_float(n.get("fat_raw")),
        "fat_saturated_g": parse_float(n.get("saturated_fat_raw")),
        "fat_trans_g":     None,  # not present in this scrape's field set
        "sodium_mg":       parse_sodium_mg(n.get("sodium_raw")),
        "carbohydrates_g": parse_float(n.get("carbs_raw")),
        "sugars_g":        parse_float(n.get("sugar_raw")),
        "dietary_fiber_g": parse_float(n.get("fiber_raw")),
        "protein_g":       parse_float(n.get("protein_raw")),
    }


# ── Ingredient text trim + allergen scan ───────────────────────────────────
def trim_ingredients(raw: str):
    """Returns (trimmed_text_or_None, hit_boilerplate_marker: bool, stray_n_fixed: bool)."""
    if not raw or not raw.strip():
        return None, False, False

    text = raw
    cut_idx = len(text)
    hit_marker = False
    for m in CUTOFF_MARKERS + ALLERGEN_CUTOFF_MARKERS:
        i = text.find(m)
        if i != -1 and i < cut_idx:
            cut_idx = i
            hit_marker = True

    trimmed = text[:cut_idx].strip()

    before_stray_fix = trimmed
    trimmed = STRAY_N_RE.sub(". ", trimmed)
    stray_fixed = trimmed != before_stray_fix

    trimmed = trimmed.strip()
    # trailing dangling period/comma cleanup
    trimmed = trimmed.rstrip(", ").strip()

    if len(trimmed) < 5:
        # trim produced near-nothing (shouldn't happen given corpus content) — fall
        # back to the untrimmed raw text rather than losing the ingredient list.
        trimmed = raw.strip()
        hit_marker = False

    return trimmed, hit_marker, stray_fixed


_MARKETING_NOT_INGREDIENT_PHRASES = ["משתלב", "בכל רגע", "מושלם", "כמו שהוא", "וקרמי"]
_REAL_INGREDIENT_SIGNAL_TERMS = ["חלב", "תרבית", "חיידק", "סוכר", "מים", "עמילן", "מייצב",
                                  "פרי", "רכיבי", "מלח", "ג'לטין", "גלטין", "קמח"]


def looks_like_marketing_not_ingredients(text: str) -> bool:
    """Detect BSIP0 scrape gaps where the 'ingredients_raw' field actually captured
    ad copy (e.g. Muller's templated "natural & creamy..." bullet text) or a stray
    near-empty fragment, instead of a real ingredient declaration. Per the missing-data
    discard rule: this is 'not found', not a real ingredient list — never fabricate a
    clean list out of marketing prose."""
    if not text:
        return False
    t = text.strip()
    if len(t) <= 3:
        return True
    has_real_signal = any(term in t for term in _REAL_INGREDIENT_SIGNAL_TERMS)
    has_marketing_signal = any(phrase in t for phrase in _MARKETING_NOT_INGREDIENT_PHRASES)
    if has_marketing_signal and not has_real_signal:
        return True
    return False


def scan_allergens(raw_text: str) -> list:
    if not raw_text:
        return []
    found = []
    for term, allergen in ALLERGEN_SCAN:
        if term in raw_text and allergen not in found:
            found.append(allergen)
    return found


# ── Exclusion classification ───────────────────────────────────────────────
def exclusion_reason(p) -> str | None:
    name = get_name_he(p) or ""
    if p.get("edge_case_flag") == "labneh":
        return "labneh_routes_to_DAIRY_SOLID_not_yogurt"
    if "קוטג" in name:
        return "cottage_cheese_scored_in_another_category_no_double_listing"
    if "קפיר" in name:
        return "kefir_not_admitted_to_yogurt_corpus"
    return None


# ── NOVA proxy (descriptive attribute extraction, NOT a scoring rule) ──────
ARTIFICIAL_SWEETENER_CATEGORIES = {"aspartame", "sucralose", "saccharin", "acesulfame_k", "neotame"}
NATURAL_SWEETENER_CATEGORIES = {
    "added_sugar", "brown_sugar", "glucose", "fructose", "lactose", "maltose",
    "sucrose", "molasses", "honey", "invert_sugar", "invert_sugar_syrup",
    "glucose_syrup", "maple_syrup", "date_syrup", "agave_syrup", "corn_syrup",
    "rice_syrup", "malt_syrup", "sugar_syrup",
}
NOVA3_ADDITIVE_CATEGORIES = {
    "stabilizer", "thickener", "stabilizer_thickener", "modified_starch",
    "acidity_regulator", "color", "preservative", "emulsifier", "raising_agent",
    "humectant", "antioxidant",
}


def classify_nova(merged: dict) -> dict:
    summary = merged.get("enrichment_summary", {})
    sweeteners = merged.get("extracted_sweeteners", [])
    additives = merged.get("extracted_additives", [])
    flavors = merged.get("extracted_flavors", [])
    matrix = merged.get("extracted_matrix_markers", [])

    has_artificial_sweetener = any(s["category"] in ARTIFICIAL_SWEETENER_CATEGORIES for s in sweeteners)
    has_natural_sweetener = any(s["category"] in NATURAL_SWEETENER_CATEGORIES for s in sweeteners)
    has_flavor_compound = any(f["category"] in ("flavor_generic", "vanilla_synthetic") for f in flavors)
    additive_count = summary.get("additive_count", 0)
    has_nova3_additive = any(a["category"] in NOVA3_ADDITIVE_CATEGORIES for a in additives)
    has_matrix = len(matrix) > 0

    if has_artificial_sweetener or has_flavor_compound or additive_count >= 3:
        return {
            "nova_proxy": 4,
            "nova_confidence": 0.85,
            "nova_confidence_band": "high",
            "nova_notes": ["artificial_sweetener_or_flavor_compound_or_ge3_additives: NOVA4 proxy"],
        }
    if has_nova3_additive or has_matrix or additive_count >= 1:
        return {
            "nova_proxy": 3,
            "nova_confidence": 0.78,
            "nova_confidence_band": "high",
            "nova_notes": ["stabilizer_additive_or_composite_matrix_component_detected: NOVA3 proxy"],
        }
    if has_natural_sweetener:
        return {
            "nova_proxy": 2,
            "nova_confidence": 0.72,
            "nova_confidence_band": "medium",
            "nova_notes": ["added_sugar_or_natural_sweetener_only: NOVA2 proxy"],
        }
    return {
        "nova_proxy": 1,
        "nova_confidence": 0.8,
        "nova_confidence_band": "medium",
        "nova_notes": ["minimal_ingredients_milk_cultures_only_or_no_ingredient_text: NOVA1 proxy"],
    }


# ── Consistency checks (subpool-aware kcal bounds, matching the BSIP0 plausibility
#    ruling already applied upstream: DAIRY_SEMISOLID 30-250 kcal, DAIRY_CULTURED_DRINK
#    20-150 kcal — re-verified here, not re-decided) ─────────────────────────
KCAL_BOUNDS = {
    "spoonable": (20, 300),   # slightly wider than the BSIP0 gate to avoid double-gating false positives
    "drinkable": (15, 200),
}


def consistency_checks(nn: dict, subpool: str) -> dict:
    sugar = nn.get("sugars_g")
    carbs = nn.get("carbohydrates_g")
    sat_fat = nn.get("fat_saturated_g")
    fat = nn.get("fat_g")
    kcal = nn.get("energy_kcal")

    sugar_le_carbs = True if (sugar is None or carbs is None) else (sugar <= carbs + 0.15)
    satfat_le_fat = True if (sat_fat is None or fat is None) else (sat_fat <= fat + 0.15)

    kcal_plausible = True
    if kcal is not None:
        lo, hi = KCAL_BOUNDS.get(subpool, (15, 300))
        kcal_plausible = lo <= kcal <= hi

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


def compute_trust(checks: dict, ing_text: str, has_image: bool) -> tuple:
    flags = ["single_source_only"]
    score = 0.75

    if not checks.get("sugar_le_carbs") or not checks.get("satfat_le_fat"):
        score -= 0.2
        flags.append("consistency_failure")
    if not checks.get("kcal_plausible"):
        score -= 0.1
        flags.append("kcal_implausible")
    if not ing_text:
        score -= 0.15
        flags.append("no_ingredient_text_or_marketing_bleed_discarded")
    if not has_image:
        score -= 0.05
        flags.append("no_image")

    score = round(max(0.1, min(1.0, score)), 2)
    if score >= 0.8:
        level = "high"
    elif score >= 0.5:
        level = "medium"
    else:
        level = "low"
    return level, score, flags


def sha256_of(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    products = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))

    total_input = len(products)
    excluded = []
    enriched_records = []

    # coverage counters (denominators = final enriched set, computed after the loop)
    field_present = {"name": 0, "ingredients": 0, "nutrition_core": 0, "image": 0}
    subpool_dist_final = {}
    nova_dist = {}
    allergen_dist = {}
    trim_stats = {"boilerplate_trimmed": 0, "stray_n_fixed": 0, "marketing_bleed_discarded": 0}
    sat_fat_labeled = 0
    fiber_labeled = 0
    sugar_labeled = 0

    for p in products:
        reason = exclusion_reason(p)
        if reason:
            excluded.append({
                "barcode": p.get("barcode"),
                "name_he": get_name_he(p),
                "subpool": p.get("subpool"),
                "source": p.get("source"),
                "reason": reason,
            })
            continue

        barcode = p.get("barcode")
        name_he = get_name_he(p)
        name_en = get_name_en(p)
        brand = get_brand(p)
        image_urls = get_image_urls(p)
        source = p.get("source")
        subpool = p.get("subpool")
        weight_g = get_weight_g(p)
        price = get_price(p)
        source_url = get_source_url(p)

        raw_ing = p.get("ingredients_raw") or ""
        trimmed_text, hit_marker, stray_fixed = trim_ingredients(raw_ing)
        if hit_marker:
            trim_stats["boilerplate_trimmed"] += 1
        if stray_fixed:
            trim_stats["stray_n_fixed"] += 1

        marketing_bleed = looks_like_marketing_not_ingredients(trimmed_text)
        if marketing_bleed:
            trim_stats["marketing_bleed_discarded"] += 1
            trimmed_text = None  # discard per missing-data-discard rule — never fabricate

        allergens = scan_allergens(raw_ing)

        nn = build_normalized_nutrition(p.get("nutrition"))
        checks = consistency_checks(nn, subpool)
        image_url = image_urls[0] if image_urls else None
        trust_lvl, trust_score, risk_flags = compute_trust(checks, trimmed_text, bool(image_url))

        missing_fields = [
            k for k, v in nn.items()
            if v is None and k in ("energy_kcal", "fat_g", "protein_g", "sodium_mg")
        ]
        if marketing_bleed:
            missing_fields.append("ingredients_text_he")
        data_sufficiency = "sufficient" if not missing_fields else "partial"

        primary = {
            "schema_version":            "bsip1_v0_1",
            "file_type":                 "product",
            "canonical_product_id":      f"bsip1_yogurt_{barcode}",
            "barcode":                   barcode,
            "canonical_name_he":         name_he,
            "canonical_name_en":         name_en,
            "brand":                     brand,
            "weight_g":                  weight_g,
            "category":                  CATEGORY,
            "subpool":                   subpool,   # spoonable | drinkable — kept intact per TASK-515/515A split
            "source_retailers":          [source],
            "retailer_prices":           {source: price},
            "image_url":                 image_url,
            "source_url":                source_url,
            "normalized_nutrition_per_100g": nn,
            "energy_kcal":               nn.get("energy_kcal"),
            "fat_g":                     nn.get("fat_g"),
            "fat_saturated_g":           nn.get("fat_saturated_g"),
            "fat_trans_g":               nn.get("fat_trans_g"),
            "protein_g":                 nn.get("protein_g"),
            "carbohydrates_g":           nn.get("carbohydrates_g"),
            "sugars_g":                  nn.get("sugars_g"),
            "sodium_mg":                 nn.get("sodium_mg"),
            "dietary_fiber_g":           nn.get("dietary_fiber_g"),
            "calcium_mg":                None,  # not in this scrape's field set
            "ingredients_text_he":       trimmed_text,
            "ingredients_raw_he":        raw_ing or None,
            "allergens_contains":        allergens,
            "allergens_may_contain":     [],
            "missing_fields":            missing_fields,
            "data_sufficiency":          data_sufficiency,
            "nutrition_consistency_status": "consistent" if (checks["sugar_le_carbs"] and checks["satfat_le_fat"] and checks["kcal_plausible"]) else "warnings",
            "consistency_checks":        checks,
            "canonical_trust_level":     trust_lvl,
            "canonical_trust_score":     trust_score,
            "confidence":                trust_score,
            "bsip1_trust_level":         trust_lvl,
            "bsip1_trust_score":         trust_score,
            "bsip1_risk_flags":          risk_flags,
            "conflicts_summary":         [],
            "inferred_fields":           [],
            "audit_ref":                 None,
            "provenance": {
                "source":              source,
                "fetched_at":          p.get("scraped_at"),
                "panel_source":        source,
                "verification_status": "candidate",
            },
            "enrichment_timestamp":      ts,
            "run_id":                    RUN_ID,
        }

        # Second-pass semantic enrichment — same shared module used for hard_cheeses /
        # cereals / milk / hummus (uniform baseline doctrine: one engine, not a bespoke
        # yogurt-only parser). Only ADDS extracted_* fields; never overwrites the above.
        merged = enrich(primary)

        nova = classify_nova(merged)
        merged.update({
            "nova_proxy": nova["nova_proxy"],
            "nova_confidence": nova["nova_confidence"],
            "nova_confidence_band": nova["nova_confidence_band"],
            "nova_notes": nova["nova_notes"],
            "detected_additives": [a["term"] for a in merged.get("extracted_additives", [])],
            "additive_count": len(merged.get("extracted_additives", [])),
            "ingredients_list": [i["text"] for i in merged.get("ingredient_order", [])],
            "ingredient_count": len(merged.get("ingredient_order", [])),
            "ingredient_text_quality": (
                "good" if len(merged.get("ingredient_order", [])) >= 2
                else ("present" if trimmed_text else "absent")
            ),
        })

        out_path = OUTPUT_DIR / f"bsip1_yogurt_{barcode}.json"
        out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
        enriched_records.append(merged)

        # ── coverage bookkeeping ──
        if name_he:
            field_present["name"] += 1
        if trimmed_text:
            field_present["ingredients"] += 1
        if nn.get("energy_kcal") is not None and nn.get("protein_g") is not None:
            field_present["nutrition_core"] += 1
        if image_url:
            field_present["image"] += 1
        if nn.get("fat_saturated_g") is not None:
            sat_fat_labeled += 1
        if nn.get("dietary_fiber_g") is not None:
            fiber_labeled += 1
        if nn.get("sugars_g") is not None:
            sugar_labeled += 1

        subpool_dist_final[subpool] = subpool_dist_final.get(subpool, 0) + 1
        nv = f"NOVA_{nova['nova_proxy']}"
        nova_dist[nv] = nova_dist.get(nv, 0) + 1
        for a in allergens:
            allergen_dist[a] = allergen_dist.get(a, 0) + 1

    final_n = len(enriched_records)

    (OUTPUT_DIR / "excluded_products_task515.json").write_text(
        json.dumps({"run_id": RUN_ID, "excluded": excluded, "excluded_count": len(excluded)},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    def pct(n, d):
        return f"{n}/{d} ({round(n / d * 100, 1)}%)" if d else "0/0"

    report = {
        "run_id": RUN_ID,
        "task": "TASK-515 / TASK-515A — Stage 1 (BSIP1 enrichment)",
        "generated": ts,
        "source_corpus_file": str(CORPUS_FILE),
        "enrichment_version": ENRICHMENT_VERSION,
        "totals": {
            "input_corpus": total_input,
            "excluded": len(excluded),
            "excluded_labneh": sum(1 for e in excluded if "labneh" in e["reason"]),
            "excluded_cottage": sum(1 for e in excluded if "cottage" in e["reason"]),
            "excluded_kefir": sum(1 for e in excluded if "kefir" in e["reason"]),
            "final_enriched": final_n,
        },
        "subpool_distribution_post_exclusion": subpool_dist_final,
        "field_coverage_pct_of_final": {
            "name":          pct(field_present["name"], final_n),
            "ingredients":   pct(field_present["ingredients"], final_n),
            "nutrition_core_energy_and_protein": pct(field_present["nutrition_core"], final_n),
            "images":        pct(field_present["image"], final_n),
            "sat_fat_labeled": pct(sat_fat_labeled, final_n),
            "sugar_labeled":   pct(sugar_labeled, final_n),
            "fiber_labeled":   pct(fiber_labeled, final_n),
        },
        "nova_distribution": nova_dist,
        "allergen_distribution": allergen_dist,
        "ingredient_text_cleanup": {
            "boilerplate_trimmed_count": trim_stats["boilerplate_trimmed"],
            "stray_n_artifact_fixed_count": trim_stats["stray_n_fixed"],
            "marketing_bleed_discarded_count": trim_stats["marketing_bleed_discarded"],
            "note": "boilerplate = repeated nutrition table + legal disclaimer bleed after the "
                    "true ingredient list on Shufersal pages, cut at the earliest of "
                    f"{CUTOFF_MARKERS + ALLERGEN_CUTOFF_MARKERS}. stray_n = a lost '\\n' that "
                    "survived scraping as a literal 'n' glued to the next digit/space "
                    "(e.g. 'ביפידוס.n20 גרם'); fixed only on the narrow '. n<space|digit>' pattern. "
                    "marketing_bleed_discarded = the scraped 'ingredients_raw' field actually "
                    "contained ad copy (e.g. Muller's templated bullet description) or a "
                    "near-empty fragment instead of a real ingredient declaration — "
                    "ingredients_text_he set to null for these per the missing-data discard rule "
                    "(never fabricate a clean list out of marketing prose); ingredients_raw_he "
                    "is preserved unmodified for audit.",
        },
        "schema_finding": {
            "finding": "The BSIP0 corpus mixes TWO distinct record shapes: 121 Shufersal "
                       "records (rich schema: name_he/brand/image_urls/source_url/claims_raw) "
                       "and 5 Yohananof records (minimal schema: name/status/provenance, "
                       "no image_urls key at all, no brand key). All 5 Yohananof records "
                       "genuinely have no image (0/5) and no brand (0/5) — this is real "
                       "missing data, not a parsing bug; every one of the 5 does carry a "
                       "populated `name` field under a different key, so overall name "
                       "coverage is NOT degraded (matches the BSIP0 manifest's 126/126 name "
                       "claim once both key names are checked).",
        },
        "bsip2_methodology_flags_for_nutrition_and_product": [
            "Spoonable vs drinkable may need DIFFERENT serving-size / sugar-density norms at "
            "scoring time (a 100g drinkable serving is consumed very differently from a 100g "
            "spoonable serving) — Data Agent does not decide this, flagging per TASK-515A brief.",
            "Whether spoonable and drinkable share the same comparison dimensions or need "
            "per-subpool dimension sets is a BSIP2 methodology call, not decided here.",
            "NOVA proxy assigned in this Stage-1 pass is a DESCRIPTIVE attribute extraction "
            "(same class of label as hard_cheeses' NOVA proxy) — it is NOT a scoring rule and "
            "was not submitted for Nutrition+Product co-sign. It should not enter BSIP2 scoring "
            "logic without that review.",
            "3 products are missing fat_g at the source (energy/protein/carbs/sodium present, "
            "fat_raw scraped as an empty string): barcodes 7290116936215, 7290116932774, "
            "5416415. Kept in the corpus (BSIP0 already admitted them past its own gate); "
            "flagged here as partial data_sufficiency rather than re-discarded at BSIP1.",
        ],
        "hard_rule_compliance": {
            "off_used": False,
            "off_count_in_final": 0,
            "rescrape_performed": False,
            "plausibility_gate_rerun": False,
            "source_file_mutated": False,
        },
    }

    report_path = OUTPUT_DIR / "bsip1_run_report_task515.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Input corpus: {total_input}")
    print(f"Excluded: {len(excluded)} (labneh={report['totals']['excluded_labneh']}, "
          f"cottage={report['totals']['excluded_cottage']}, kefir={report['totals']['excluded_kefir']})")
    print(f"Final enriched: {final_n}")
    print(f"Subpool (post-exclusion): {subpool_dist_final}")
    print(f"NOVA distribution: {nova_dist}")
    print(f"Allergen distribution: {allergen_dist}")
    print(f"Report written: {report_path}")


if __name__ == "__main__":
    main()
