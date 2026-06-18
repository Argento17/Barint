"""TASK-235 Phase 2 — build the USDA generic-reference benefit lookup for 53 frozen-veg SKUs.

DATA artifact builder only. No frontend, no scoring, no consumer copy authored.
- Maps each SKU to a USDA generic food (Foundation / SR Legacy = generic, lab-measured).
- One API call per DISTINCT generic (cache on disk); throttle for DEMO_KEY rate limits.
- Blends/mixes/pasta-blends => not_characterized (no clean generic; never synthesized).
- Every pulled value is candidate-stamped, attributed to FDC id + data_type + pub date.
Outputs: frozen_vegetables_benefit_lookup_v1.json
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, r"c:\Bari")
from integrations.clients import usda_fdc  # noqa: E402
from integrations.clients.http import HttpError  # noqa: E402

HERE = Path(r"c:\Bari\02_products\frozen_vegetables")
SEED = HERE / "frozen_vegetables_v2_phase2_seed_v1.json"
CACHE = HERE / ".usda_generic_cache_v1.json"
OUT = HERE / "frozen_vegetables_benefit_lookup_v1.json"

BENEFIT_KEYS = [
    "fiber_g", "protein_g", "vitc_mg", "vita_rae_ug", "vitk_ug", "folate_ug",
    "potassium_mg", "energy_kcal",
]

# --- Generic query catalogue: query string -> preferred frozen/cooked generic phrasing.
# Chosen to land on Foundation / SR Legacy (generic, lab-measured) entries, frozen where
# a frozen entry exists in SR Legacy, otherwise the plain cooked/raw generic.
GENERIC_QUERIES = {
    "broccoli": "broccoli, frozen, cooked, boiled, drained",
    "cauliflower": "cauliflower, frozen, cooked, boiled, drained",
    "green_beans": "beans, snap, green, frozen, cooked, boiled, drained",
    "yellow_wax_beans": "beans, snap, yellow, frozen, cooked, boiled, drained",
    "sweet_corn": "corn, sweet, yellow, frozen, kernels, cooked, boiled, drained",
    "spinach": "spinach, frozen, chopped or leaf, cooked, boiled, drained",
    "okra": "okra, frozen, cooked, boiled, drained",
    "jerusalem_artichoke": "jerusalem-artichokes, raw",
    "artichoke": "artichokes globe french frozen cooked boiled drained",
    "green_peas": "peas, green, frozen, cooked, boiled, drained",
    "fava_beans": "broadbeans (fava beans), immature seeds, cooked, boiled, drained",
    "white_beans": "beans, white, mature seeds, cooked, boiled",
    "chickpeas": "chickpeas (garbanzo beans, bengal gram), mature seeds, cooked, boiled",
    "soybeans_green": "soybeans, green, cooked, boiled, drained",
    "soybeans_mature": "soybeans, mature cooked, boiled",
    "garlic": "garlic, raw",
    "parsley": "parsley, fresh",
    "ginger": "ginger root, raw",
}

# --- SKU -> generic mapping (machine, reviewable). Status: reviewed | candidate | not_characterized.
# Keyed by bsip1_product_id. not_characterized carries NO generic (blends never synthesized).
SKU_MAP = {
    # plain-veg ----------------------------------------------------------------
    "bsip1_103457": ("cauliflower", "reviewed"),        # מיני כרובית
    "bsip1_103471": ("broccoli", "reviewed"),           # מיני ברוקולי
    "bsip1_103488": ("jerusalem_artichoke", "candidate"),  # ארטישוק ירושלמי (sunchoke; raw-only generic)
    "bsip1_104683": ("green_beans", "reviewed"),        # שעועית ירוקה שלמה
    "bsip1_104690": ("sweet_corn", "reviewed"),         # גרעיני תירס
    "bsip1_104720": ("green_beans", "reviewed"),        # שעועית ירוקה חתוכה
    "bsip1_104737": ("yellow_wax_beans", "reviewed"),   # שעועית צהובה חתוכה
    "bsip1_104744": ("cauliflower", "reviewed"),        # כרובית מוקפאת
    "bsip1_104768": ("spinach", "reviewed"),            # עלי תרד
    "bsip1_104775": ("spinach", "candidate"),           # מדליוני תרד (spinach medallions - pressed)
    "bsip1_104836": ("green_beans", "reviewed"),        # שעועית עדינה שלמה (green)
    "bsip1_7290013994776": ("sweet_corn", "reviewed"),  # גרגירי תירס אורגני
    "bsip1_7290013994783": ("green_beans", "reviewed"), # שעועית ירוקה אורגני
    "bsip1_7296073173205": ("green_beans", "reviewed"), # שעועית ירוקה עדינה
    "bsip1_7296073173212": ("green_beans", "reviewed"), # שעועית ירוקה שלמה
    "bsip1_7296073173229": ("green_beans", "reviewed"), # שעועית ירוקה חתוכה
    "bsip1_7296073445166": ("okra", "reviewed"),        # במיה
    "bsip1_7296073692621": ("broccoli", "reviewed"),    # ברוקולי
    "bsip1_7296073692638": ("cauliflower", "reviewed"), # כרובית
    "bsip1_7296073705529": ("broccoli", "reviewed"),    # ברוקולי
    "bsip1_7296073705536": ("cauliflower", "reviewed"), # כרובית
    # legumes ------------------------------------------------------------------
    "bsip1_104201": ("green_peas", "reviewed"),         # אפונה עדינה
    "bsip1_104676": ("green_peas", "reviewed"),         # אפונה ירוקה
    "bsip1_104713": ("fava_beans", "reviewed"),         # פול ירוק
    "bsip1_104799": ("white_beans", "reviewed"),        # שעועית לבנה מבושלת
    "bsip1_104805": ("chickpeas", "reviewed"),          # גרגרי חומוס מבושל
    "bsip1_7290013994806": ("green_peas", "reviewed"),  # אפונה עדינה אורגני
    "bsip1_7296073173199": ("green_peas", "reviewed"),  # אפונה ירוקה עדינה
    "bsip1_7296073224891": ("green_peas", "reviewed"),  # אפונה ירוקה
    "bsip1_7296073691358": ("soybeans_green", "candidate"),  # פולי סויה שלמים (edamame; whole vs mature ambiguous)
    "bsip1_7296073691365": ("soybeans_green", "candidate"),  # פולי סויה שלמים
    "bsip1_7296073691372": ("soybeans_green", "candidate"),  # פולי סויה קלופים (shelled edamame)
    "bsip1_7296073705505": ("chickpeas", "reviewed"),   # חומוס
    "bsip1_7296073705512": ("white_beans", "reviewed"), # שעועית לבנה
    "bsip1_7296073746546": ("soybeans_green", "candidate"),  # פולי סויה
    # herbs-seasonings (band 4) -- garlic/parsley/ginger generics for IDENTITY only;
    # benefit micros are NOT surfaced for this band (display rule), but we record the
    # generic so identity facts (e.g. it IS garlic) are sourced.
    "bsip1_2253006": ("garlic", "reviewed"),            # שום כתוש דורות
    "bsip1_2253105": ("garlic", "reviewed"),            # שום כתוש מגשית
    "bsip1_7290018989357": ("garlic", "reviewed"),      # ממרח שום
    "bsip1_7290018989364": ("garlic", "reviewed"),      # שום כתוש
    "bsip1_7290018989371": ("parsley", "reviewed"),     # פטרוזיליה
    "bsip1_7290018989456": ("ginger", "reviewed"),      # ג'ינג'ר
    "bsip1_7296073124160": ("garlic", "reviewed"),      # שום כתוש מגשית
    "bsip1_7296073124177": ("garlic", "reviewed"),      # שום כתוש בצנצנת
    # processed -> split by item (Phase 1 §1 note) -----------------------------
    "bsip1_107189": ("artichoke", "candidate"),         # ארטישוק תחתיות -> band4 single-veg prepped
    "bsip1_7296073445159": ("artichoke", "candidate"),  # תחתיות ארטישוק -> band4 single-veg prepped
    "bsip1_104874": (None, "not_characterized"),        # לקט לקוסקוס (blend) -> band3
    # blends / mixes / pasta-blends -> NOT characterized (no clean generic) -----
    "bsip1_103730": (None, "not_characterized"),        # לקט פסטה פוזילי (pasta-blend)
    "bsip1_104904": (None, "not_characterized"),        # לקט ירקות מעורבים (mix)
    "bsip1_104911": (None, "not_characterized"),        # לקט נורמנדי (mix)
    "bsip1_106175": (None, "not_characterized"),        # לקט כפרי (mix)
    "bsip1_107622": (None, "not_characterized"),        # ירקות ופסטה (pasta-blend)
    "bsip1_7290013994790": (None, "not_characterized"), # לקט ירקות אורגני (mix)
    "bsip1_7290018400173": (None, "not_characterized"), # צמד ברוקולי וכרובית (mix)
}

# processed-split + band assignment notes carried into artifact for review
PROCESSED_SPLIT = {
    "bsip1_107189": "band4_single_veg",
    "bsip1_7296073445159": "band4_single_veg",
    "bsip1_104874": "band3_blend",
}


def load_cache() -> dict:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict) -> None:
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def pull_generic(query_key: str, query: str, cache: dict) -> dict:
    """Return a cache record for one generic. Calls API once; caches result.
    On rate-limit / error, returns a pending record (no fabricated values)."""
    if query_key in cache and cache[query_key].get("status") == "ok":
        return cache[query_key]
    try:
        food = usda_fdc.lookup(query, prefer_generic=True)
        if not food or not food.found:
            rec = {"status": "no_match", "query": query, "fdc_id": None,
                   "data_type": None, "publication_date": None, "values": {}}
        else:
            vals = {k: food.values[k] for k in BENEFIT_KEYS if k in food.values}
            rec = {
                "status": "ok",
                "query": query,
                "fdc_id": food.fdc_id,
                "description": food.description,
                "data_type": food.data_type,
                "publication_date": (food.raw or {}).get("publicationDate"),
                "values": vals,
            }
        cache[query_key] = rec
        save_cache(cache)
        time.sleep(2.2)  # throttle for DEMO_KEY (~30/min)
        return rec
    except HttpError as e:
        # 429 = rate limited; anything else network -> persist pending, do not fabricate
        rec = {"status": "rate_limited" if e.status == 429 else f"http_{e.status}",
               "query": query, "fdc_id": None, "data_type": None,
               "publication_date": None, "values": {}}
        cache[query_key] = rec
        save_cache(cache)
        return rec


def main() -> None:
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    cache = load_cache()
    api_key_mode = "FDC_API_KEY" if os.environ.get("FDC_API_KEY") else "DEMO_KEY"

    # Which generics are actually referenced by at least one mapped SKU
    used_generics = sorted({g for (g, _) in SKU_MAP.values() if g})

    # Pull each distinct generic once
    for gk in used_generics:
        q = GENERIC_QUERIES[gk]
        rec = pull_generic(gk, q, cache)
        print(f"[generic] {gk:22s} {rec['status']:12s} fdc={rec.get('fdc_id')}")

    # Build generics table
    generics_table = {}
    for gk in used_generics:
        rec = cache.get(gk, {"status": "pending", "query": GENERIC_QUERIES[gk]})
        generics_table[gk] = {
            "generic_query": rec.get("query", GENERIC_QUERIES[gk]),
            "fdc_id": rec.get("fdc_id"),
            "usda_description": rec.get("description"),
            "data_type": rec.get("data_type"),
            "publication_date": rec.get("publication_date"),
            "pull_status": rec.get("status"),
            "is_generic_reference": True,  # machine-visible: typical-for-vegetable, NOT product-measured
            "per": "100g",
            "values_per_100g": rec.get("values", {}),
            "verification_status": "candidate",
            "source": "usda_fdc",
            "client_version": usda_fdc.CLIENT_VERSION,
        }

    # Display fields allowed per segment (encode Phase 1 §2 table)
    display_fields_by_segment = {
        "ירקות בודדים": {
            "_cluster_sources": ["plain-veg"],
            "serving_basis": "~100g cooked portion (~1 cup)",
            "benefit_facts_allowed": ["fiber_g", "vitc_mg", "vita_rae_ug", "vitk_ug"],
            "identity_allowed": ["single_ingredient"],
            "watch_out_allowed": [],
            "forbidden": ["added_additive_claims", "per_100g_sodium_alarm"],
            "suppressed": [],
        },
        "קטניות": {
            "_cluster_sources": ["legumes"],
            "serving_basis": "~100g portion",
            "benefit_facts_allowed": ["fiber_g", "protein_g", "folate_ug"],
            "headline": ["fiber_g", "protein_g"],
            "identity_allowed": ["single_ingredient", "legume"],
            "watch_out_allowed": [],
            "forbidden": ["substitute_for_watery_veg_implication"],
            "suppressed": [],
        },
        "תערובות וארוחות": {
            "_cluster_sources": ["mixes", "pasta-blends", "processed(blend)"],
            "serving_basis": "per realistic portion INCLUDING added component",
            "benefit_facts_allowed": ["vegetable_split_percent", "veg_base_contribution"],
            "watch_out_allowed": ["added_sodium", "added_sugar", "refined_carb", "sauce_sachet"],
            "forbidden": ["benefit_micros_from_generic"],  # no clean join -> not characterized
            "micros_policy": "not_characterized",
            "suppressed": [],
        },
        "תיבול ובישול": {
            "_cluster_sources": ["herbs-seasonings", "processed(single-veg)"],
            "serving_basis": "per ~5g use (≈1 teaspoon)",
            "benefit_facts_allowed": [],  # NO benefit-micro claim for seasonings
            "identity_allowed": ["identity", "ingredient_simplicity", "convenience"],
            "watch_out_allowed": [],
            "forbidden": ["portion_nutrition_ranking", "any_benefit_nutrient_claim",
                          "treating_oil_or_salt_as_flaw"],
            "suppressed": ["energy_kcal", "fat_g", "sodium_mg"],  # stated as plain fact only if mentioned
        },
    }

    # Build SKU rows
    cluster_to_band = seed["segment_to_consumer_band"]
    skus_out = []
    counts = {"reviewed": 0, "candidate": 0, "not_characterized": 0}
    unmapped_for_nutrition = []

    for p in seed["products"]:
        pid = p["bsip1_product_id"]
        cluster = p["segment_cluster"]
        generic, status = SKU_MAP.get(pid, (None, "not_characterized"))
        counts[status] = counts.get(status, 0) + 1

        # Resolve consumer band (handle processed split)
        if cluster == "processed":
            split = PROCESSED_SPLIT.get(pid, "band4_single_veg")
            band = "תערובות וארוחות" if split == "band3_blend" else "תיבול ובישול"
        else:
            band = cluster_to_band.get(cluster, cluster)

        label_present = [k for k, v in p["label_present"].items() if v]
        label_absent = [k for k, v in p["label_present"].items() if not v]

        # USDA fills ONLY missing benefit fields, display-only, for non-not_characterized.
        # It never overwrites a present label value, and seasonings get no micro fill.
        usda_filled = []
        if status != "not_characterized" and generic:
            gvals = generics_table.get(generic, {}).get("values_per_100g", {})
            seasoning = band == "תיבול ובישול"
            allowed = set(display_fields_by_segment.get(band, {}).get("benefit_facts_allowed", []))
            if not seasoning:
                for k in BENEFIT_KEYS:
                    if k not in allowed:
                        continue
                    label_key = {"fiber_g": "dietary_fiber_g", "protein_g": "protein_g",
                                 "energy_kcal": "energy_kcal"}.get(k, k)
                    # fill only if NOT present on the label AND USDA has a value
                    if not p["label_present"].get(label_key, False) and k in gvals:
                        usda_filled.append(k)

        row = {
            "bsip1_product_id": pid,
            "name_he": p["name_he"],
            "barcode": p["barcode"],
            "segment_cluster": cluster,
            "consumer_band": band,
            "generic_query_ref": generic,
            "join_status": status,
            "is_generic_reference": generic is not None,  # typical-for-veg, not product-measured
            "label_present_fields": label_present,
            "label_absent_fields": label_absent,
            "usda_filled_fields": usda_filled,  # display-only candidate fills
        }
        if cluster == "processed":
            row["processed_split"] = PROCESSED_SPLIT.get(pid, "band4_single_veg")
        skus_out.append(row)

        if status == "candidate":
            unmapped_for_nutrition.append({
                "bsip1_product_id": pid, "name_he": p["name_he"],
                "generic_query_ref": generic, "reason": "plausible match, needs human eye",
            })

    artifact = {
        "meta": {
            "task": "TASK-235 Phase 2 — USDA generic-reference benefit lookup",
            "scope": "frozen-vegetables ONLY; not a precedent (owner 2026-06-10)",
            "usda_client_version": usda_fdc.CLIENT_VERSION,
            "generation_date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "api_key_mode": api_key_mode,
            "n_skus": len(skus_out),
            "join_status_counts": counts,
            "distinct_generics_referenced": len(used_generics),
            "policy": {
                "usda_role": "generic reference enrichment ONLY; never product-measured panel",
                "verification_status": "every USDA value is candidate (provenance.py)",
                "no_overwrite": "USDA never overwrites a present BSIP0 label value; fills missing only, display-only",
                "blends": "no clean generic -> not_characterized; micros never synthesized",
                "absence_rule": "missing label nutrient = absent, not zero (Phase 1 §2 locked)",
                "no_score": "no benefit score, no computed benefit number, no ranking",
            },
        },
        "generics": generics_table,
        "skus": skus_out,
        "display_fields_by_segment": display_fields_by_segment,
        "phrasing_draft_PENDING_NUTRITION_SIGNOFF": {
            "_status": "DRAFT — PENDING NUTRITION SIGN-OFF. NOT approved. Produced by Data Agent; "
                       "Nutrition signs off in a later step (Phase 1 §4 / Hard-rule 5).",
            "generic_reference_label_he": "ערכים אופייניים לירק זה (מקור ייחוס: USDA), לא נמדדו על המוצר עצמו.",
            "per_fact_framing_template_he": "{ירק} מספק בדרך כלל ~{ערך} {יחידה} ל-100 גרם (ערך ייחוס גנרי, לא נמדד על המוצר).",
            "not_characterized_he": "תערובת — אין ערך ייחוס גנרי נקי; ערכי המיקרו לא אופיינו ולא הומצאו.",
            "seasoning_reframe_he": "תיבול — נשפט ככזה. הערכים מתייחסים לשימוש של כ-5 גרם (כפית), לא למנה נאכלת.",
            "attribution_template": "מקור: USDA FoodData Central, fdc_id={fdc_id}, {data_type}, {publication_date}.",
        },
    }

    OUT.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT}")
    print(f"counts: {counts}")
    print(f"distinct generics: {len(used_generics)}")
    pulled = [g for g in used_generics if cache.get(g, {}).get("status") == "ok"]
    pending = [g for g in used_generics if cache.get(g, {}).get("status") != "ok"]
    print(f"pulled ok: {len(pulled)} -> {pulled}")
    print(f"pending/failed: {len(pending)} -> {pending}")


if __name__ == "__main__":
    main()
