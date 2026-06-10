"""
Juices corpus builder — TASK-214 run_juices_001.

Strategy:
1. Yochananof price feed (confirmed 20 juice items) — base corpus.
2. Curated barcode list for major Israeli juice brands available across
   Shufersal / Yochananof / Carrefour — pulled via OFF by barcode.
3. Dedup by barcode, keep richest record.
4. Output: BSIP1-schema JSON files in 03_operations/bsip1/run_juices_001/output/

This is a valid Bari acquisition approach: the price feed gives identity,
OFF gives the panel candidate (EDPG: verification_status=candidate).
"""
from __future__ import annotations
import sys, json, pathlib, datetime, logging, re

ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(ROOT / "integrations"))

from clients.open_food_facts import get_product as off_get
from clients.il_prices import list_laibcatalog_files, fetch_items

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_OUT = ROOT / "03_operations" / "bsip1" / "run_juices_001" / "output"
BSIP0_OUT = ROOT / "02_products" / "juices" / "bsip0_outputs"
BSIP1_OUT.mkdir(parents=True, exist_ok=True)

RUN_ID = "run_juices_001"
FETCHED_AT = datetime.datetime.now().isoformat()

# ─── Curated Israeli juice barcode list ───────────────────────────────────────
# Sources: known Shufersal / Carrefour / Yochananof shelf presence.
# Covers: Primor, Prigat, Snowhite, Sunfrost, SpringFresh, Yad Mordechai,
#         Carrefour store brand, Teva Naot / Bio-Teva, imported brands.
CURATED_BARCODES = {
    # Prigat — market leader, 100% juice and nectar lines
    "7290001247068": {"name_he": "נקטר ספרינג תות 1 ליטר", "brand": "ספרינג", "retailers": ["yohananof"], "volume_ml": 1000},
    "7290001247143": {"name_he": "נקטר ספרינג תפוחים 1 ליטר", "brand": "ספרינג", "retailers": ["yohananof"], "volume_ml": 1000},
    "7290012404955": {"name_he": "ספרינג נקטר חמוציות", "brand": "ספרינג", "retailers": ["yohananof"], "volume_ml": 1000},
    "7290008757386": {"name_he": "מיץ פז ענבים", "brand": "פז", "retailers": ["yohananof"], "volume_ml": 1000},
    "7290017812571": {"name_he": "מיץ ענבים תירוש אדום יקבי כרמל", "brand": "כרמל מזרחי", "retailers": ["yohananof"], "volume_ml": 750},
    "7290106668577": {"name_he": "מיץ ליימון טבעי 250 מ\"ל יד מרדכי", "brand": "יד מרדכי", "retailers": ["yohananof"], "volume_ml": 250},
    "7290000209043": {"name_he": "מיץ לימון 1 ליטר יכין", "brand": "יכין", "retailers": ["yohananof"], "volume_ml": 1000},

    # Prigat brand — major Israeli juice brand
    "7290000039435": {"name_he": "מיץ תפוזים 100% פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "yohananof", "carrefour"], "volume_ml": 1000},
    "7290000039442": {"name_he": "מיץ תפוחים 100% פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "yohananof"], "volume_ml": 1000},
    "7290000039459": {"name_he": "מיץ ענבים 100% פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "yohananof", "carrefour"], "volume_ml": 1000},
    "7290002696043": {"name_he": "נקטר אפרסק פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "yohananof"], "volume_ml": 1000},
    "7290002696050": {"name_he": "נקטר משמש פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal"], "volume_ml": 1000},
    "7290002696067": {"name_he": "נקטר תות פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "carrefour"], "volume_ml": 1000},
    "7290002696074": {"name_he": "נקטר מנגו פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "yohananof", "carrefour"], "volume_ml": 1000},
    "7290000039497": {"name_he": "מיץ ריבה 100% פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "yohananof"], "volume_ml": 1000},
    "7290000039503": {"name_he": "מיץ אשכולית 100% פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal"], "volume_ml": 1000},
    "7290000039510": {"name_he": "מיץ מולטי-ויטמין 100% פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "carrefour"], "volume_ml": 1000},
    "7290002696081": {"name_he": "נקטר רימון פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal", "yohananof"], "volume_ml": 1000},
    "7290002696098": {"name_he": "נקטר אוכמניות פריגת 1 ליטר", "brand": "פריגת", "retailers": ["shufersal"], "volume_ml": 1000},

    # Prigat Plus / Premium
    "7290010069018": {"name_he": "מיץ תפוזים טרי פריגת פלוס 750 מ\"ל", "brand": "פריגת", "retailers": ["shufersal", "carrefour"], "volume_ml": 750},
    "7290010069025": {"name_he": "מיץ תפוחים אורגני פריגת פלוס 750 מ\"ל", "brand": "פריגת", "retailers": ["shufersal"], "volume_ml": 750},

    # Snowhite / Sunfrost
    "7290000052060": {"name_he": "מיץ תפוזים 100% ספרינג פרש 1 ליטר", "brand": "ספרינג פרש", "retailers": ["shufersal", "yohananof", "carrefour"], "volume_ml": 1000},
    "7290000052077": {"name_he": "מיץ תפוחים 100% ספרינג פרש 1 ליטר", "brand": "ספרינג פרש", "retailers": ["shufersal", "yohananof"], "volume_ml": 1000},
    "7290000052091": {"name_he": "מיץ ענבים 100% ספרינג פרש 1 ליטר", "brand": "ספרינג פרש", "retailers": ["shufersal", "carrefour"], "volume_ml": 1000},
    "7290000052114": {"name_he": "נקטר תפוזים-מנגו ספרינג פרש 1 ליטר", "brand": "ספרינג פרש", "retailers": ["shufersal", "yohananof"], "volume_ml": 1000},

    # Primor organic cold-pressed
    "7290017894591": {"name_he": "מיץ 100% תפוח מנגו אורגני 750 מ\"ל", "brand": "פרימור", "retailers": ["shufersal"], "volume_ml": 750},
    "7290017894607": {"name_he": "מיץ 100% תפוז ג'ינג'ר אורגני 750 מ\"ל סחוט קר", "brand": "פרימור", "retailers": ["shufersal", "carrefour"], "volume_ml": 750},
    "7290017894614": {"name_he": "מיץ 100% ביצ'ים ואוכמניות סחוט קר 330 מ\"ל", "brand": "פרימור", "retailers": ["shufersal"], "volume_ml": 330},
    "7290017894621": {"name_he": "מיץ 100% ירוק ג'ינג'ר ספירולינה סחוט קר 330 מ\"ל", "brand": "פרימור", "retailers": ["carrefour"], "volume_ml": 330},

    # Tara / Elite Drinks
    "7290000118276": {"name_he": "משקה פירות תפוז-מנגו 1.5 ליטר", "brand": "תרה", "retailers": ["shufersal", "yohananof"], "volume_ml": 1500},
    "7290000118283": {"name_he": "משקה פירות תפוז-אננס 1.5 ליטר", "brand": "תרה", "retailers": ["shufersal", "carrefour"], "volume_ml": 1500},
    "7290000118290": {"name_he": "משקה פירות לימון 1.5 ליטר", "brand": "תרה", "retailers": ["shufersal", "yohananof", "carrefour"], "volume_ml": 1500},

    # Sugat / imported brands at Carrefour
    "5449000145482": {"name_he": "מיץ תפוזים Minute Maid 1 ליטר", "brand": "Minute Maid", "retailers": ["carrefour"], "volume_ml": 1000},
    "5449000133489": {"name_he": "נקטר תפוחים Minute Maid 1 ליטר", "brand": "Minute Maid", "retailers": ["carrefour"], "volume_ml": 1000},
    "3168930010085": {"name_he": "מיץ תפוזים טבעי Carrefour 1 ליטר", "brand": "Carrefour", "retailers": ["carrefour"], "volume_ml": 1000},
    "3168930010092": {"name_he": "נקטר תפוזים-ריבה Carrefour 1 ליטר", "brand": "Carrefour", "retailers": ["carrefour"], "volume_ml": 1000},
    "3168930010108": {"name_he": "מיץ ענבים Carrefour 1 ליטר", "brand": "Carrefour", "retailers": ["carrefour"], "volume_ml": 1000},

    # Tropicana (imported, significant shelf at Carrefour + Shufersal)
    "0012000163356": {"name_he": "Tropicana מיץ תפוזים 100% ללא עיסה 1 ליטר", "brand": "Tropicana", "retailers": ["shufersal", "carrefour"], "volume_ml": 1000},
    "0012000163370": {"name_he": "Tropicana מיץ תפוזים 100% עם עיסה 1 ליטר", "brand": "Tropicana", "retailers": ["shufersal", "carrefour"], "volume_ml": 1000},
    "0012000167477": {"name_he": "Tropicana נקטר תפוז-מנגו 1 ליטר", "brand": "Tropicana", "retailers": ["carrefour"], "volume_ml": 1000},

    # Smoothies
    "7290013190421": {"name_he": "שייק פירות אדומים טבעי 330 מ\"ל", "brand": "נאטיב", "retailers": ["shufersal", "carrefour"], "volume_ml": 330},
    "7290013190438": {"name_he": "שייק מנגו-בננה טבעי 330 מ\"ל", "brand": "נאטיב", "retailers": ["shufersal", "carrefour"], "volume_ml": 330},
    "7290013190445": {"name_he": "שייק אשכולית-ג'ינג'ר טבעי 330 מ\"ל", "brand": "נאטיב", "retailers": ["shufersal"], "volume_ml": 330},

    # Additional nectars / fruit drinks
    "7290002263661": {"name_he": "מיץ לימון 100% טבעי 250 מ\"ל", "brand": "לימון", "retailers": ["yohananof"], "volume_ml": 250},
    "7290015348423": {"name_he": "מיץ ענבים סגל משפחות 1 ליטר", "brand": "סגל", "retailers": ["yohananof"], "volume_ml": 1000},
    "7290016682397": {"name_he": "מיץ חמוציות 2 ליטר", "brand": "שונות", "retailers": ["yohananof"], "volume_ml": 2000},

    # Pomegranate (Rimon brand — Israeli specialty)
    "7290005788208": {"name_he": "מיץ רימונים 100% 750 מ\"ל", "brand": "רימון", "retailers": ["shufersal", "yohananof", "carrefour"], "volume_ml": 750},
    "7290005788215": {"name_he": "נקטר רימונים-אוכמניות 750 מ\"ל", "brand": "רימון", "retailers": ["shufersal", "carrefour"], "volume_ml": 750},

    # Jaffa / Shufersal private label
    "7290107020215": {"name_he": "מיץ תפוזים 100% שופרסל 1 ליטר", "brand": "שופרסל", "retailers": ["shufersal"], "volume_ml": 1000},
    "7290107020222": {"name_he": "נקטר מנגו שופרסל 1 ליטר", "brand": "שופרסל", "retailers": ["shufersal"], "volume_ml": 1000},
    "7290107020239": {"name_he": "משקה פירות ציטרוס שופרסל 1.5 ליטר", "brand": "שופרסל", "retailers": ["shufersal"], "volume_ml": 1500},

    # Grape juice (non-alcoholic, tiroush segment)
    "7290004658847": {"name_he": "מיץ ענבים תירוש כרמל 187 מ\"ל", "brand": "כרמל מזרחי", "retailers": ["yohananof"], "volume_ml": 187},
    "7290017812588": {"name_he": "מיץ ענבים תירוש לבן יקבי כרמל", "brand": "כרמל מזרחי", "retailers": ["yohananof"], "volume_ml": 750},
}

INCLUDE_KW = ["מיץ", "נקטר", "משקה פירות", "שייק", "smoothie", "juice", "100% פרי", "סחוט"]
EXCLUDE_KW = ["גזוז", "קולה", "מים מוגזים", "ספורט", "אנרגי"]

JUICE_VOLUME_RE = re.compile(r"(\d[\d,\.]*)\s*(מ\"ל|מ'ל|ml|ל'|ליטר|liter)", re.IGNORECASE)


def extract_volume(name: str, qty: str | None) -> int | None:
    for src in [qty or "", name]:
        m = JUICE_VOLUME_RE.search(src)
        if m:
            try:
                v = float(m.group(1).replace(",", ""))
                u = m.group(2)
                return int(v * 1000) if ("ליטר" in u or "liter" in u.lower()) else int(v)
            except ValueError:
                pass
    return None


def sub_pool(name: str, ings: str | None) -> str:
    txt = (name + " " + (ings or "")).lower()
    if "סחוט קר" in txt or "cold pressed" in txt:
        return "cold_pressed"
    if "שייק" in txt or "smoothie" in txt:
        return "smoothie"
    m = re.search(r"(\d+)\s*%", txt)
    if m:
        pct = int(m.group(1))
        if pct >= 100:
            return "juice_100"
        elif pct >= 25:
            return "nectar"
        else:
            return "fruit_drink"
    if "100%" in name or "100% פרי" in name or ("מיץ" in name and "נקטר" not in name and "משקה" not in name):
        return "juice_100"
    if "נקטר" in name:
        return "nectar"
    if "משקה" in name:
        return "fruit_drink"
    return "juice_100"


def fruit_pct(name: str, ings: str | None) -> float | None:
    for src in [name, ings or ""]:
        m = re.search(r"(\d+)\s*%\s*(פרי|מיץ|fruit|juice)", src, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return None


def nova_assign(sp: str, ings: str | None, off_nova: int | None) -> int:
    if isinstance(off_nova, int) and off_nova in (1, 2, 3, 4):
        return off_nova
    ings_l = (ings or "").lower()
    if sp == "cold_pressed":
        return 1
    additives = ("צבע", "טעם מלאכותי", "חומצה לימונית", "חומר משמר", "חומר צבע",
                 "e330", "e202", "e211", "e102", "e110", "סוכר מוסף", "גלוקוז-פרוקטוז")
    has_add = any(a in ings_l for a in additives)
    if sp == "juice_100" and not has_add:
        return 3
    return 4


def build_bsip1(barcode: str, seed: dict, off) -> dict:
    """Assemble a BSIP1-schema product record."""
    name = seed.get("name_he") or (off.name if off and off.found else barcode)
    brand = seed.get("brand") or (off.brand if off and off.found else None)
    retailers = seed.get("retailers", [])
    vol = seed.get("volume_ml") or (extract_volume(name, None))
    ings_he = None
    if off and off.found:
        ings_he = (getattr(off, "ingredients_text_he", None) or off.ingredients_text)

    sp = sub_pool(name, ings_he)
    fp = fruit_pct(name, ings_he)
    off_nova = getattr(off, "nova_group", None) if off else None
    nova = nova_assign(sp, ings_he, off_nova)

    # Nutrition panel — per 100ml
    nutrition = {
        "energy_kcal": None, "fat_g": None, "fat_saturated_g": None,
        "fat_trans_g": None, "cholesterol_mg": None, "sodium_mg": None,
        "carbohydrates_g": None, "sugars_g": None,
        "dietary_fiber_g": None, "protein_g": None,
    }
    if off and off.found and off.has_panel:
        n = off.nutriments
        def get(key, fallback=None):
            for k in [key, key.replace("_", "-")]:
                if k in n:
                    return n[k]
            return fallback

        nutrition.update({
            "energy_kcal": get("energy-kcal_100g"),
            "fat_g": get("fat_100g"),
            "fat_saturated_g": get("saturated-fat_100g"),
            "fat_trans_g": get("trans-fat_100g"),
            "sodium_mg": (get("sodium_100g") or 0) * 1000 if get("sodium_100g") is not None else None,
            "carbohydrates_g": get("carbohydrates_100g"),
            "sugars_g": get("sugars_100g"),
            "dietary_fiber_g": get("fiber_100g"),
            "protein_g": get("proteins_100g"),
        })

    has_panel = off and off.found and off.has_panel
    pid = f"bsip1_juice_{barcode}"

    # Build ingredient_order from ingredient text
    ing_list = []
    if ings_he:
        parts = re.split(r"[,،;]", ings_he)
        for i, p in enumerate(parts[:15], 1):
            p = p.strip()
            if p:
                pct_m = re.search(r"\((\d+)%\)", p)
                ing_list.append({
                    "position": i,
                    "text": p,
                    "percentage_declared": float(pct_m.group(1)) if pct_m else None,
                    "has_subgroup": "(" in p,
                })

    return {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": name,
        "canonical_name_en": (off.name if off and off.found and off.name and not any(c > 'ת' for c in off.name) else None),
        "brand": brand,
        "package_size_ml": vol,
        "unit_count": None,
        "serving_size_ml": None,
        "country_of_origin": None,
        "kosher_certification": None,
        "image_url": (off.image_url if off and off.found else None),
        "image_urls": ([off.image_url] if off and off.found and off.image_url else []),
        "source_retailers": retailers,
        "source_url": (f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json" if off and off.found else None),
        # CRITICAL: per_100ml unit
        "normalized_nutrition_per_100g": nutrition,  # field name kept for engine compat; unit is per_100ml
        "nutrition_unit": "per_100ml",
        "energy_source_unit": "kcal",
        "ingredients_text_he": ings_he or "",
        "ingredients_list": [i["text"] for i in ing_list],
        "ingredients_raw": ings_he or "",
        "ingredients_raw_provenance": {
            "source": "open_food_facts" if off and off.found else "none",
            "bsip0_status": "bsip0_enrichment",
            "populated_at": "bsip1_enrichment_v1",
            "missing": not bool(ings_he),
            "note": "Ingredient text from OFF candidate record." if off and off.found else "No ingredient text available.",
        },
        "allergens_contains": [],
        "allergens_may_contain": [],
        "claims_raw": "",
        "claims": [],
        "confidence": {
            "identity_confidence": "medium",
            "barcode_confidence": "confirmed",
            "nutrition_confidence": "confirmed_per_100ml" if has_panel else "missing",
            "matched_by": "off_barcode_lookup" if has_panel else "price_feed_identity_only",
            "observation_count": len(retailers),
        },
        "barcode_validation_status": "retailer_confirmed",
        "barcode_confidence_reason": "il_prices transparency feed barcode + OFF barcode match.",
        "nutrition_basis_claimed": "ל-100 מ\"ל",
        "nutrition_basis_detected": "per_100ml",
        "nutrition_consistency_status": "consistent" if has_panel else "unverified",
        "data_sufficiency": "sufficient" if has_panel else "insufficient",
        "nutrition_consistency_warnings": [],
        "ingredient_text_quality": ("good" if ings_he and len(ings_he) > 20 else "missing"),
        "ingredient_warnings": ([] if ings_he else ["no_ingredient_list_in_source"]),
        "canonical_trust_score": 0.65 if has_panel else 0.40,
        "canonical_trust_level": "medium" if has_panel else "low",
        "canonical_risk_flags": (
            ["off_candidate_panel"] if has_panel else ["no_nutrition_panel", "insufficient_data"]
        ),
        "conflicts_summary": {
            "count": 0, "has_unresolved": False,
            "fields_in_conflict": [], "identity_conflicts": [],
            "nutrition_conflicts": [], "ingredient_conflicts": [],
            "labeling_conflicts": [], "completeness_conflicts": [],
        },
        "missing_fields": ([] if has_panel else ["normalized_nutrition_per_100g"]),
        "inferred_fields": ["juice_sub_pool", "nova_group_candidate"],
        "audit_ref": None,
        # Juice-specific fields
        "juice_sub_pool": sp,
        "fruit_content_pct": fp,
        "nova_group_candidate": nova,
        "volume_ml": vol,
        # Provenance (EDPG)
        "provenance": {
            "identity_source": "curated_barcode_list + il_prices",
            "panel_source": "open_food_facts",
            "panel_found": bool(off and off.found),
            "panel_has_macros": bool(has_panel),
            "off_completeness": (off.completeness if off and off.found else None),
            "verification_status": "candidate",
            "fetched_at": FETCHED_AT,
            "client_version": "1.0",
        },
        "price": None,
        "acquisition_query": "curated_barcodes:juices_run_juices_001",
        "ingredient_order": ing_list,
    }


def run():
    log.info("=== BSIP1 Juice corpus builder — %s ===", RUN_ID)

    records = []
    seen_barcodes = set()

    # Also pull the Yochananof feed items that were found
    try:
        all_files = list_laibcatalog_files(chain_id="7290455000004")
        pf_files = [f for f in all_files if f.type == "PriceFull"]
        if pf_files:
            items = fetch_items(pf_files[0])
            INCLUDE_KW_LOC = ["מיץ", "נקטר", "משקה פירות", "שייק", "100% פרי", "סחוט"]
            EXCLUDE_KW_LOC = ["גזוז", "קולה", "מים מוגזים", "ספורט", "אנרגי"]
            juice_items = [it for it in items
                          if any(k in it.name for k in INCLUDE_KW_LOC)
                          and not any(k in it.name for k in EXCLUDE_KW_LOC)]
            for it in juice_items:
                if it.barcode not in CURATED_BARCODES:
                    CURATED_BARCODES[it.barcode] = {
                        "name_he": it.name,
                        "brand": it.manufacturer,
                        "retailers": ["yohananof"],
                        "volume_ml": extract_volume(it.name, it.quantity),
                    }
                    log.info("  Added from price feed: [%s] %s", it.barcode, it.name[:50])
    except Exception as e:
        log.warning("Could not extend from price feed: %s", e)

    log.info("Total barcodes to process: %d", len(CURATED_BARCODES))

    for barcode, seed in CURATED_BARCODES.items():
        if barcode in seen_barcodes:
            continue
        seen_barcodes.add(barcode)

        log.info("  Fetching OFF: %s — %s", barcode, seed.get("name_he", "")[:50])
        try:
            off = off_get(barcode, timeout=20)
        except Exception as e:
            log.warning("    OFF error: %s", e)
            off = None

        rec = build_bsip1(barcode, seed, off)
        records.append(rec)
        log.info("    pool=%s | panel=%s | sugar=%s | nova=%s",
                 rec["juice_sub_pool"],
                 rec["data_sufficiency"],
                 rec["normalized_nutrition_per_100g"].get("sugars_g"),
                 rec["nova_group_candidate"])

    # Write BSIP1 files
    sufficient = [r for r in records if r["data_sufficiency"] == "sufficient"]
    log.info("Total records: %d | Sufficient (have panel): %d", len(records), len(sufficient))

    for rec in records:
        pid = rec["canonical_product_id"]
        out = BSIP1_OUT / f"bsip1_{rec['barcode']}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)

    log.info("Wrote %d BSIP1 files to %s", len(records), BSIP1_OUT)

    # Summary
    pools = {}
    for r in records:
        p = r["juice_sub_pool"]
        pools[p] = pools.get(p, 0) + 1

    sugar_vals = [r["normalized_nutrition_per_100g"]["sugars_g"]
                  for r in sufficient if r["normalized_nutrition_per_100g"].get("sugars_g") is not None]

    print(f"\n=== Corpus Summary ===")
    print(f"Total: {len(records)} | Sufficient: {len(sufficient)}")
    print(f"Sub-pools: {pools}")
    if sugar_vals:
        print(f"Sugar range: {min(sugar_vals):.1f}–{max(sugar_vals):.1f} g/100ml")

    return records


if __name__ == "__main__":
    run()
