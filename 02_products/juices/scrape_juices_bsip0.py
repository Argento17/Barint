"""
BSIP0 scrape for Juices & Fruit Drinks category — run_juices_001 (TASK-214).

Retailers: Shufersal (self-hosted), Yochananof (laibcatalog chain 7290455000004),
           Carrefour (laibcatalog — search by Hebrew name keywords).
Enrichment: Open Food Facts (barcode → nutrition panel candidate).

CRITICAL: nutrition panels are recorded per 100ml — this is the only Bari category
with a volume-based unit. unit="per_100ml" is set on every product.

Juice keyword classifier: scans Hebrew item name for juice/nectar/drink markers.
Output: one JSON per retailer in 02_products/juices/bsip0_outputs/
"""
from __future__ import annotations
import sys
import json
import pathlib
import re
import logging
import datetime

# ── path setup ────────────────────────────────────────────────────────────────
ROOT = pathlib.Path(r"C:\Bari")
sys.path.insert(0, str(ROOT / "integrations"))

from clients.il_prices import (
    list_shufersal_files, list_laibcatalog_files,
    fetch_items, PriceItem,
)
from clients.open_food_facts import get_product as off_get
from source_validator import require_il_prices_accessible, SourceAccessError

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

OUTPUT_DIR = ROOT / "02_products" / "juices" / "bsip0_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── juice keyword sets ────────────────────────────────────────────────────────
INCLUDE_KW = (
    "מיץ", "מיצים", "נקטר", "משקה פירות", "משקאות פירות",
    "שייק", "עגבניות 100%", "תפוחים 100%", "תפוזים 100%",
    "juice", "nectar", "smoothie",
    "מיץ תפוזים", "מיץ תפוחים", "מיץ ענבים", "מיץ גרייפ פרוט",
    "מיץ רימון", "מיץ גזר", "מיץ אשכולית", "מיץ אננס",
    "מיץ מנגו", "מיץ תות", "מיץ לימון", "מיץ סחוט",
    "פירות טבעי", "100% פרי", "סחוט קר",
)
EXCLUDE_KW = (
    "גזוז", "קולה", "מים מוגזים", "ספורט", "אנרג'י",
    "טוניק", "סודה", "מי ברז", "מים",
)

JUICE_VOLUME_PATTERN = re.compile(
    r"(\d[\d,\.]*)\s*(מ[\"ל\s]|מ\"ל|ml|ל\'|ליטר|liter|cl)",
    re.IGNORECASE
)


def is_juice(name: str) -> bool:
    name_lower = name.lower()
    if any(ex in name for ex in EXCLUDE_KW):
        return False
    return any(kw in name for kw in INCLUDE_KW)


def extract_volume_ml(name: str, quantity_str: str | None) -> int | None:
    """Extract volume in ml from name or quantity field."""
    for src in [quantity_str or "", name]:
        m = JUICE_VOLUME_PATTERN.search(src)
        if m:
            num_str = m.group(1).replace(",", "")
            try:
                val = float(num_str)
                unit = m.group(2).strip()
                # ליטר / liter = x1000
                if "ליטר" in unit or "liter" in unit.lower():
                    return int(val * 1000)
                if unit.startswith("ל") and not unit.startswith("ל\""):
                    return int(val * 1000)
                return int(val)
            except ValueError:
                pass
    return None


def classify_sub_pool(name: str, ingredients_he: str | None, off_data) -> str:
    """Classify product into sub-pool based on name and label signals."""
    txt = (name + " " + (ingredients_he or "")).lower()
    if "סחוט קר" in txt or "cold pressed" in txt.lower() or "cold-pressed" in txt.lower():
        return "cold_pressed"
    if "שייק" in txt or "smoothie" in txt:
        return "smoothie"
    # Check fruit content % from name
    m = re.search(r"(\d+)\s*%\s*(פרי|מיץ|fruit)", txt)
    if m:
        pct = int(m.group(1))
        if pct >= 100:
            return "juice_100"
        elif pct >= 25:
            return "nectar"
        else:
            return "fruit_drink"
    # Label text signals
    if "100% פרי" in name or "100% מיץ" in name or "מיץ טבעי" in name:
        return "juice_100"
    if "נקטר" in name:
        return "nectar"
    if "משקה פירות" in name or "משקה" in name:
        return "fruit_drink"
    # Default juice names without qualifier → 100% if name says "מיץ" without "נקטר"/"משקה"
    if "מיץ" in name:
        return "juice_100"
    return "juice_100"


def extract_fruit_content_pct(name: str, ingredients_he: str | None) -> float | None:
    """Try to extract declared fruit content % from name or ingredients."""
    for src in [name, ingredients_he or ""]:
        m = re.search(r"(\d+)\s*%\s*(פרי|מיץ פירות|juice|fruit)", src, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return None


def nova_from_sub_pool_and_ingredients(sub_pool: str, ingredients_he: str | None, off_nova: int | None) -> int:
    """Assign NOVA group per pipeline brief rules."""
    if off_nova and isinstance(off_nova, int):
        return off_nova
    ings = (ingredients_he or "").lower()
    # Cold-pressed / fresh-squeezed — minimal processing
    if sub_pool == "cold_pressed":
        return 1
    # 100% juice with no additives / added sugar
    additive_markers = ("צבע", "טעם", "ריח", "חומצה לימונית", "חומר משמר", "סוכר", "גלוקוז")
    has_additives = any(m in ings for m in additive_markers)
    if sub_pool == "juice_100" and not has_additives:
        return 3
    # Nectar or drink with added sugar / additives
    return 4


def build_bsip0_record(item: PriceItem, retailer: str, off_data) -> dict:
    """Assemble a BSIP0 raw observation record."""
    name = item.name or ""
    vol = extract_volume_ml(name, item.quantity)
    off_has_panel = off_data.has_panel if off_data and off_data.found else False

    # Nutrition panel — from OFF, per 100ml
    nutrition = {}
    if off_has_panel:
        n = off_data.nutriments
        nutrition = {
            "energy_kcal": n.get("energy-kcal_100g"),   # OFF stores per 100ml for liquids
            "fat_g": n.get("fat_100g"),
            "fat_saturated_g": n.get("saturated-fat_100g"),
            "fat_trans_g": n.get("trans-fat_100g"),
            "sodium_mg": n.get("sodium_100g", 0) * 1000 if n.get("sodium_100g") else n.get("sodium_100g"),
            "carbohydrates_g": n.get("carbohydrates_100g"),
            "sugars_g": n.get("sugars_100g"),
            "dietary_fiber_g": n.get("fiber_100g"),
            "protein_g": n.get("proteins_100g"),
        }

    ingredients_he = None
    if off_data and off_data.found:
        ingredients_he = (
            getattr(off_data, "ingredients_text_he", None)
            or off_data.ingredients_text
        )

    sub_pool = classify_sub_pool(name, ingredients_he, off_data)
    fruit_pct = extract_fruit_content_pct(name, ingredients_he)
    off_nova = getattr(off_data, "nova_group", None) if off_data else None
    nova = nova_from_sub_pool_and_ingredients(sub_pool, ingredients_he, off_nova)

    return {
        "schema_version": "bsip0_v1",
        "barcode": item.barcode,
        "product_name_he": name,
        "brand": item.manufacturer or (off_data.brand if off_data and off_data.found else None),
        "retailer": retailer,
        "price": item.price,
        "volume_ml": vol,
        "unit": "per_100ml",
        "category_tag": sub_pool,
        "fruit_content_pct": fruit_pct,
        "nova_group_candidate": nova,
        "image_url": (off_data.image_url if off_data and off_data.found else None),
        "nutrition_per_100ml": nutrition,
        "ingredients_text_he": ingredients_he,
        "off_found": off_data.found if off_data else False,
        "off_has_panel": off_has_panel,
        "off_nova_group": off_nova,
        "data_sufficiency": "sufficient" if off_has_panel else "insufficient",
        "provenance": {
            "identity_source": f"il_prices:{item.provenance.source_id if item.provenance else retailer}",
            "panel_source": "open_food_facts",
            "panel_found": off_data.found if off_data else False,
            "verification_status": "candidate",
            "fetched_at": datetime.datetime.now().isoformat(),
        }
    }


# Maps scraper retailer names → source_registry IDs for il_prices pre-flight checks.
# Retailers not yet in the registry (yohananof) are skipped for the portal check.
_REGISTRY_ID: dict[str, str] = {
    "shufersal": "shufersal",
    "victory": "victory",
    "carrefour": "carrefour",
    "rami_levi": "rami_levi",
}


def scrape_retailer(retailer_name: str, chain_id: str | None, is_shufersal: bool,
                    max_items: int = 5000) -> list[dict]:
    """Scrape one retailer's price feed and return juice BSIP0 records."""
    log.info("=== Scraping %s ===", retailer_name)

    # Pre-flight: confirm il_prices portal is reachable before spending API budget.
    registry_id = _REGISTRY_ID.get(retailer_name)
    if registry_id:
        require_il_prices_accessible(registry_id)

    # Get price files
    if is_shufersal:
        all_files = list_shufersal_files()
    else:
        all_files = list_laibcatalog_files(chain_id=chain_id)

    pf_files = [f for f in all_files if f.type == "PriceFull"]
    if not pf_files:
        raise SourceAccessError(
            retailer_id=retailer_name,
            access_status="NO_PRICEFULL_FILES",
            detail=(
                f"Portal for '{retailer_name}' returned {len(all_files)} files "
                f"but none of type PriceFull. Portal may be throttling or the "
                f"chain_id '{chain_id}' may be wrong. Do not continue to OFF enrichment."
            ),
        )

    # Use one store catalog (representative sample)
    pf = pf_files[0]
    log.info("Fetching %s from %s", pf.type, pf.url[:80])
    items = fetch_items(pf, limit=max_items)
    log.info("  Total items in catalog: %d", len(items))

    # Filter to juices
    juice_items = [it for it in items if is_juice(it.name)]
    log.info("  Juice items after name filter: %d", len(juice_items))

    records = []
    for item in juice_items:
        # Enrich with OFF
        try:
            off_data = off_get(item.barcode, timeout=20)
        except Exception as e:
            log.warning("OFF lookup failed for %s: %s", item.barcode, e)
            off_data = None

        rec = build_bsip0_record(item, retailer_name, off_data)
        records.append(rec)
        log.info("  [%s] %s | vol=%s | pool=%s | panel=%s",
                 item.barcode, item.name[:50], rec["volume_ml"],
                 rec["category_tag"], rec["off_has_panel"])

    return records


def run():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Retailer configurations — source access status as of 2026-06-07:
    #   shufersal  il_prices feed LIVE; storefront BLOCKED_TLS_FINGERPRINT_FAKE_200
    #   victory    il_prices feed LIVE (laibcatalog 7290696200003); storefront CLEAR
    #   yohananof  chain_id 7290455000004 NAME-UNCONFIRMED on laibcatalog; no storefront test
    #   carrefour  storefront BLOCKED_F5_BIGIP_403; chain_id NAME-UNCONFIRMED — removed
    # See integrations/source_registry.py for full classification.
    retailers = [
        ("shufersal",  None,              True),
        ("victory",    "7290696200003",   False),   # LIVE-VERIFIED 2026-06-07
        ("yohananof",  "7290455000004",   False),   # NAME-UNCONFIRMED — verify via Stores file
    ]

    all_records = {}
    for name, chain_id, is_shuf in retailers:
        try:
            recs = scrape_retailer(name, chain_id, is_shuf)
            error_info = None
        except SourceAccessError as e:
            log.error(
                "SOURCE BLOCKED — %s | status=%s | %s",
                name, e.access_status, e.detail,
            )
            recs = []
            error_info = {
                "blocked": True,
                "access_status": e.access_status,
                "detail": e.detail,
                "fingerprint": e.fingerprint.name if e.fingerprint else None,
            }
        except Exception as e:
            log.error("Scrape failed for %s: %s", name, e)
            recs = []
            error_info = {"blocked": False, "error": str(e)}

        out_path = OUTPUT_DIR / f"bsip0_{name}_juices_{timestamp}.json"
        output = {
            "schema_version": "bsip0_v1",
            "retailer": name,
            "category": "juices",
            "run_id": "run_juices_001",
            "scraped_at": datetime.datetime.now().isoformat(),
            "product_count": len(recs),
            "sufficient_count": sum(1 for r in recs if r["data_sufficiency"] == "sufficient"),
            "products": recs,
        }
        if error_info:
            output["source_error"] = error_info
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        log.info("Wrote %d records → %s", len(recs), out_path)
        all_records[name] = recs

    return all_records


if __name__ == "__main__":
    run()
