"""
BSIP0 Yohananof — Cheese acquisition (TASK-210 Phase B).

Uses il_prices + OFF model (same as multiretailer_cereals and yohananof_yogurt).
Cheese covers: קוטג', גבינה צהובה, גבינה בולגרית, גבינה לבנה, לאבנה, ריקוטה, פטה, etc.

Output: C:\Bari\02_products\cheese_spreads\bsip0_outputs\yohananof_cheese_bsip0_raw_<ts>.json
"""
from __future__ import annotations
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari")

from integrations.clients import il_prices as ip
from integrations.clients import open_food_facts as off

OUT_DIR = Path(r"C:\Bari\02_products\cheese_spreads\bsip0_outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

YOHANANOF_CHAIN = "7290455000004"
RETAILER_ID = "yohananof"
RETAILER_NAME = "יוחננוף"
CATEGORY = "cheese"

CHEESE_INCLUDE = [
    "גבינה", "גביש", "קוטג", "ריקוטה",
    "לאבנה", "ממרח גבינה", "פטה", "בולגרית",
    "מוצרלה", "צהובה", "פרמזן",
    "גאודה", "אמנטל", "צ'דר", "ברי",
    "cheese", "גבינת", "גבינות",
    "קשקבל", "מנצ'גו", "הלומי",
    "ממרח חלב", "ממרח שמנת",
    "פרובולונה", "גורגונזולה",
]

CHEESE_HARD_DROP = [
    "גלידה", "שוקולד ממרח", "ממרח שוקולד", "ממרח שקדים", "ממרח בוטנים",
    "ממרח תמרים", "ממרח פירות", "ממרח אגוזים",
    "שמפו", "סבון", "ניקוי", "חיתול",
    "חטיף", "עוגיית", "ביסקוויט",
    "קרם פנים", "קרם גוף",
]


def name_matches(name: str, signals: list, hard_drop: list) -> bool:
    nl = (name or "").lower()
    if any(h.lower() in nl for h in hard_drop):
        return False
    return any(s.lower() in nl for s in signals)


def extract_weight_g(name: str):
    for pat in (
        re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.I),
        re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.I),
        re.compile(r"(\d[\d,.]*)\s*g\b", re.I),
    ):
        m = pat.search(name)
        if m:
            try:
                v = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    v *= 1000
                if 50 < v < 5000:
                    return v
            except ValueError:
                pass
    return None


def off_to_bsip0(price_item, off_p, retailer_id, retailer_name, category) -> dict:
    n = off_p.nutriments if off_p and off_p.found else {}

    def g(*keys):
        for k in keys:
            if k in n and n[k] not in (None, ""):
                return n[k]
        return ""

    name = (off_p.name if (off_p and off_p.found and off_p.name) else price_item.name) or price_item.name
    ingredients = (off_p.ingredients_text if (off_p and off_p.found and off_p.ingredients_text) else "") or ""
    images = [off_p.image_url] if (off_p and off_p.found and off_p.image_url) else []
    weight_g = extract_weight_g(price_item.name)

    return {
        "retailer_id": retailer_id,
        "retailer_name": retailer_name,
        "source_url": (off_p.provenance.source_url if (off_p and off_p.provenance) else ""),
        "scraped_at": datetime.utcnow().isoformat(),
        "name_he": name,
        "name_en": "",
        "brand": (off_p.brand if (off_p and off_p.found) else (price_item.manufacturer or "")) or "",
        "barcode": str(price_item.barcode),
        "category_raw": category,
        "subcategory_raw": category,
        "nutrition": {
            "energy_kcal_raw": str(g("energy-kcal_100g", "energy-kcal", "energy_100g")),
            "protein_raw":     str(g("proteins_100g", "proteins")),
            "carbs_raw":       str(g("carbohydrates_100g", "carbohydrates")),
            "fat_raw":         str(g("fat_100g", "fat")),
            "fiber_raw":       str(g("fiber_100g", "fiber")),
            "sodium_raw":      str(g("sodium_100g", "sodium")),
            "sugar_raw":       str(g("sugars_100g", "sugars")),
            "saturated_fat_raw": str(g("saturated-fat_100g", "saturated-fat")),
        },
        "nutrition_raw_source": {"source": "open_food_facts", "barcode": str(price_item.barcode)},
        "ingredients_raw": ingredients[:1200],
        "ingredients_language": "he" if ingredients and any("א" <= c <= "ת" for c in ingredients) else "",
        "claims_raw": "",
        "image_urls": [u for u in images if u][:3],
        "extraction_method": "il_prices_identity+off_panel",
        "extraction_confidence": "high" if (n and ingredients) else ("medium" if n else "low"),
        "price": str(price_item.price) if price_item.price is not None else "",
        "weight_g": weight_g,
        "price_per_100g": None,
        "acquisition_query": f"price_feed:{retailer_id}",
        "acquisition_tier": "price_feed",
        "provenance": {
            "identity_source": (price_item.provenance.source if price_item.provenance else None),
            "identity_source_url": (price_item.provenance.source_url if price_item.provenance else None),
            "panel_source": "open_food_facts" if (off_p and off_p.found) else None,
            "panel_found": bool(off_p and off_p.found),
            "panel_has_macros": bool(off_p and off_p.has_panel),
            "off_completeness": (off_p.completeness if off_p and off_p.found else None),
            "verification_status": "candidate",
            "fetched_at": datetime.utcnow().isoformat(),
        },
    }


def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    print("=== Acquiring cheese from Yohananof (TASK-210 Phase B) ===")

    files = ip.list_laibcatalog_files(YOHANANOF_CHAIN)
    pf = [f for f in files if f.type == "PriceFull"]
    if not pf:
        print("ERROR: No PriceFull files found for Yohananof!")
        return []

    items = ip.fetch_items(pf[0])
    print(f"Total catalog items: {len(items)}")

    cand = []
    seen = set()
    for it in items:
        bc = str(it.barcode)
        if not bc or bc in seen:
            continue
        if name_matches(it.name or "", CHEESE_INCLUDE, CHEESE_HARD_DROP):
            seen.add(bc)
            cand.append(it)

    print(f"Name-gate candidates: {len(cand)}")

    out = []
    no_panel = 0
    for i, it in enumerate(cand[:200]):
        try:
            p = off.get_product(str(it.barcode))
        except Exception as e:
            print(f"  OFF error {it.barcode}: {e}")
            p = None
        if not (p and p.has_panel):
            no_panel += 1
        out.append(off_to_bsip0(it, p, RETAILER_ID, RETAILER_NAME, CATEGORY))
        if i % 20 == 0 and i:
            print(f"  [{i}/{len(cand[:200])}] no-panel so far: {no_panel}")
        time.sleep(0.2)

    with_panel = sum(1 for r in out if r["provenance"]["panel_has_macros"])
    print(f"Acquired: {len(out)} | OFF panel(macros)={with_panel} no-panel={no_panel} ({100*with_panel//max(len(out),1)}% panel rate)")

    out_path = OUT_DIR / f"yohananof_cheese_bsip0_raw_{ts}.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {out_path}")
    return out


if __name__ == "__main__":
    main()
