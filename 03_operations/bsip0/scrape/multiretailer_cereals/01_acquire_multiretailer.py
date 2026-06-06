"""
BSIP0 Multi-retailer — Breakfast Cereals + Granola/Muesli acquisition (TASK-184).

Broadens the cereals corpus beyond single-source Shufersal across additional Israeli
retailers, to (a) widen brand coverage and (b) validate the EV-045/045b corpus-purity
ruling on UNSEEN data.

ACQUISITION MODEL (honest, no scraping, no fabrication):
  Israeli price-transparency law publishes full SKU catalogs (barcode + Hebrew name +
  brand + price) per chain. We use those as the IDENTITY layer, then pair each barcode
  with an Open Food Facts (OFF) panel for nutrition + ingredients (the documented
  il_prices -> open_food_facts pairing). A barcode miss in OFF = "no panel", never an
  invented panel. Provenance is stamped per the EDPG rule; everything stays `candidate`
  until BSIP0/QA promotion.

REACHABILITY (probed live 2026-06-05 from this network):
  * Carrefour    7290055700007  prices.carrefour.co.il (self-hosted JSON file list)  REACHABLE
  * Yochananof   7290455000004  via laibcatalog.co.il (publisher portal)             REACHABLE
  * Rami-Levy    -              prices.rami-levy.co.il / publishedprices / SPA        BLOCKED (ConnectionError/DNS)

Output (one raw file per reachable retailer), schema mirrors
  shufersal_cereals/01_scrape_cereals.py so the existing
  02_build_bsip1_cereals.py _curate() (EV-045/045b) runs UNCHANGED:
    C:\\Bari\\02_products\\breakfast_cereals\\bsip0_outputs\\multiretailer\\<retailer>_bsip0_raw_<ts>.json
"""
from __future__ import annotations

import json
import re
import sys
import gzip
import time
from datetime import datetime
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari")

from integrations.clients import il_prices as ip
from integrations.clients import open_food_facts as off

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
           "Accept-Language": "he-IL,he;q=0.9"}

OUT_DIR = Path(r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs\multiretailer")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CARREFOUR_PORTAL = "https://prices.carrefour.co.il/"
CARREFOUR_CHAIN = "7290055700007"
YOHANANOF_CHAIN = "7290455000004"   # confirmed Yochananof via StoresFull branch names (Netivot/Sderot)

# ── Cereal-shelf name gate ──────────────────────────────────────────────────────
# A price feed is a WHOLE-STORE catalog (10k+ SKUs), so the name gate must be broad
# enough to catch the shelf but is deliberately NOT the purity filter — the EV-045/045b
# _curate() layer in 02_build_bsip1_cereals.py is the ruling under test and does the real
# contaminant removal. We INCLUDE liberally and let curation reject; that is precisely how
# we measure the ruling's precision/recall on unseen data.
INCLUDE_SIGNALS = [
    "דגני בוקר", "דגני ", "דגנים", "קורנפלקס", "קורן פלקס", "cornflakes", "גרנולה", "granola",
    "מוזלי", "מוסלי", "muesli", "שיבולת שועל", "קוואקר", "quaker", "צ'יריוס", "ציריוס",
    "cheerios", "נסקוויק", "nesquik", "קוקו פופס", "coco pops", "צ'וקפיק", "chocapic",
    "פצפוצי", "פצפוצים", "כריות", "בראן", "bran", "fitness", "פיטנס", "קלוגס", "kellogg",
    "weetabix", "ויטבי", "כוסמין פתית", "cereal", "פתיתי תירס", "טריקס", "trix", "פריכים עם",
]
# Cheap pre-gate to keep OFF lookups bounded — drop the obvious non-shelf SKUs by name
# BEFORE we spend an OFF request. (Curation still re-checks everything that survives.)
HARD_DROP = ["סוכריות", "שוקולד למריחה", "גלידה", "במבה", "ביסלי", "צ'יפס", "טישו",
             "שמפו", "סבון", "משחת", "חיתול", "מגבונים", "ניקוי", "אקונומיקה"]


def _name_candidate(name: str) -> bool:
    n = name or ""
    nl = n.lower()
    if any(h in n for h in HARD_DROP):
        return False
    return any(s.lower() in nl for s in INCLUDE_SIGNALS)


def _extract_weight_g(name: str):
    for pat in (re.compile(r"(\d[\d,.]*)\s*ק[\"']?ג", re.I),
                re.compile(r"(\d[\d,.]*)\s*גר?(?:\b|')", re.I),
                re.compile(r"(\d[\d,.]*)\s*g\b", re.I)):
        m = pat.search(name)
        if m:
            try:
                v = float(m.group(1).replace(",", "."))
                if "ק" in m.group(0):
                    v *= 1000
                if 50 < v < 2000:
                    return v
            except ValueError:
                pass
    return None


# ── Per-retailer catalog readers ─────────────────────────────────────────────────

def carrefour_pricefull_items() -> list:
    """Self-hosted Carrefour portal: index page embeds a `files` JSON; pick the largest
    PriceFull (a store-wide catalog) and parse it with the shared transparency parser."""
    t = requests.get(CARREFOUR_PORTAL, headers=HEADERS, timeout=40, verify=False).text
    path = re.search(r"const path = '(\d+)'", t).group(1)
    files = json.loads(re.search(r"const files = (\[.*?\]);", t, re.S).group(1))
    pf = sorted([f for f in files if f["name"].startswith("PriceFull")],
                key=lambda f: -f["size"])
    if not pf:
        return []
    url = f"{CARREFOUR_PORTAL}{path}/{pf[0]['name']}"
    blob = requests.get(url, headers=HEADERS, timeout=120, verify=False).content
    items = ip.parse_price_xml(gzip.decompress(blob))
    for it in items:
        it.provenance = ip.stamp(source=f"il_prices:{CARREFOUR_CHAIN}", source_id=it.barcode,
                                 source_url=url, client_version=ip.CLIENT_VERSION)
    return items


def yohananof_pricefull_items() -> list:
    """Yochananof via laibcatalog publisher portal."""
    files = ip.list_laibcatalog_files(YOHANANOF_CHAIN)
    pf = [f for f in files if f.type == "PriceFull"]
    if not pf:
        return []
    return ip.fetch_items(pf[0])  # stamps provenance per item


# ── OFF panel enrichment ─────────────────────────────────────────────────────────

def _off_to_bsip0(price_item, off_p, retailer_id, retailer_name) -> dict:
    """Assemble a BSIP0-shaped raw record from price identity + OFF candidate panel.

    Mirrors shufersal_cereals/01_scrape_cereals.py output so the existing
    02_build_bsip1_cereals.py curation/enrichment runs byte-identically.
    Nutrition values are OFF `candidate` data (EDPG): provenance carried, never promoted.
    """
    n = off_p.nutriments if off_p and off_p.found else {}

    def g(*keys):
        for k in keys:
            if k in n and n[k] not in (None, ""):
                return n[k]
        return ""

    name = (off_p.name if (off_p and off_p.found and off_p.name) else price_item.name) or price_item.name
    ingredients = (off_p.ingredients_text if (off_p and off_p.found and off_p.ingredients_text) else "") or ""
    images = [off_p.image_url] if (off_p and off_p.found and off_p.image_url) else []
    weight_g = _extract_weight_g(price_item.name)

    return {
        "retailer_id": retailer_id,
        "retailer_name": retailer_name,
        "source_url": (off_p.provenance.source_url if (off_p and off_p.provenance) else ""),
        "scraped_at": datetime.utcnow().isoformat(),
        "name_he": name,
        "name_en": "",
        "brand": (off_p.brand if (off_p and off_p.found) else (price_item.manufacturer or "")) or "",
        "barcode": str(price_item.barcode),
        "category_raw": "",
        "subcategory_raw": "breakfast_cereal",
        "serving_size_g_hint": None,
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
        # provenance envelope (EDPG) — carried into the run record; candidate until QA pass
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


def acquire_retailer(retailer_id, retailer_name, items, off_cap=400):
    cand = []
    seen = set()
    for it in items:
        bc = str(it.barcode)
        if not bc or bc in seen:
            continue
        if not _name_candidate(it.name):
            continue
        seen.add(bc)
        cand.append(it)
    print(f"[{retailer_id}] catalog items={len(items)} -> name-gate cereal candidates={len(cand)}")

    out = []
    no_panel = 0
    for i, it in enumerate(cand[:off_cap]):
        try:
            p = off.get_product(str(it.barcode))
        except Exception as e:
            print(f"  OFF error {it.barcode}: {e}")
            p = None
        if not (p and p.has_panel):
            no_panel += 1
        out.append(_off_to_bsip0(it, p, retailer_id, retailer_name))
        if i % 25 == 0 and i:
            print(f"  [{i}/{len(cand[:off_cap])}] panels missing so far: {no_panel}")
        time.sleep(0.2)
    with_panel = sum(1 for r in out if r["provenance"]["panel_has_macros"])
    print(f"[{retailer_id}] acquired={len(out)} | OFF panel(macros)={with_panel} "
          f"no-panel={no_panel} ({100*with_panel//max(len(out),1)}% panel rate)")
    return out


def main():
    import urllib3
    urllib3.disable_warnings()
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    results = {}

    # ── Carrefour ──
    try:
        c_items = carrefour_pricefull_items()
        c_raw = acquire_retailer("carrefour", "קרפור", c_items)
        (OUT_DIR / f"carrefour_bsip0_raw_{ts}.json").write_text(
            json.dumps(c_raw, ensure_ascii=False, indent=2), encoding="utf-8")
        results["carrefour"] = len(c_raw)
    except Exception as e:
        print(f"[carrefour] ACQUISITION FAILED: {type(e).__name__}: {e}")
        results["carrefour"] = f"FAILED: {e}"

    # ── Yochananof ──
    try:
        y_items = yohananof_pricefull_items()
        y_raw = acquire_retailer("yohananof", "יוחננוף", y_items)
        (OUT_DIR / f"yohananof_bsip0_raw_{ts}.json").write_text(
            json.dumps(y_raw, ensure_ascii=False, indent=2), encoding="utf-8")
        results["yohananof"] = len(y_raw)
    except Exception as e:
        print(f"[yohananof] ACQUISITION FAILED: {type(e).__name__}: {e}")
        results["yohananof"] = f"FAILED: {e}"

    # ── Rami-Levy — documented BLOCKED, recorded honestly, not fabricated ──
    results["rami_levy"] = "BLOCKED: prices.rami-levy.co.il + publishedprices portals unreachable " \
                           "(ConnectionError/DNS); storefront is a login-gated SPA with no public " \
                           "catalog API. Recommend Playwright session or a live publishedprices login."

    print("\n=== ACQUISITION SUMMARY ===")
    for k, v in results.items():
        print(f"  {k}: {v}")
    (OUT_DIR / f"acquisition_summary_{ts}.json").write_text(
        json.dumps({"ts": ts, "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    return results


if __name__ == "__main__":
    main()
