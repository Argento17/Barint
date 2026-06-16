"""TASK-171 revival — v3 re-measurement sprint: build the addressable shelf sample.

Reads the LIVE Super-Pharm supplement catalog, maps each SKU to one of the 15 engine
actives (detect_active_slug on the Hebrew name), and writes the addressable rows +
a representative sample for the agent-driven panel-find sprint.

EDPG: identity-only (barcode/name/brand/price); no panel here; nothing scored; candidate.
"""
import sys, json, pathlib, collections

ROOT = r"C:\Bari"
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from integrations.clients import il_prices as p
from integrations.clients.il_supplement_panels import detect_active_slug
from integrations.clients import il_panel_resolver as rez

HERE = pathlib.Path(__file__).resolve().parent

# the 15 engine actives (dossier slugs we can score)
ENGINE_ACTIVES = {
    "creatine", "magnesium", "vitamin_d3", "caffeine", "omega3", "vitamin_c",
    "zinc", "iron", "calcium", "folic_acid", "vitamin_b12", "melatonin",
    "biotin", "vitamin_e", "coq10",
}


def brand_bucket(name, manuf):
    b = rez._brand_token(manuf or "", name or "")
    return b or "other"


def main():
    catalog = p.fetch_super_pharm_supplements()
    print(f"live Super-Pharm oral-supplement catalog: {len(catalog)} SKUs")

    rows = []
    for it in catalog:
        slug = detect_active_slug(it.name or "")
        if slug not in ENGINE_ACTIVES:
            continue
        rows.append({
            "barcode": it.barcode,
            "name_he": it.name,
            "manufacturer": it.manufacturer,
            "price_ils": it.price,
            "active": slug,
            "brand_bucket": brand_bucket(it.name, it.manufacturer),
        })

    by_active = collections.Counter(r["active"] for r in rows)
    by_brand = collections.Counter(r["brand_bucket"] for r in rows)
    print(f"addressable (maps to 15 engine actives): {len(rows)} / {len(catalog)} "
          f"= {100*len(rows)/max(1,len(catalog)):.1f}%")
    print("by active:", dict(by_active.most_common()))
    print("by brand :", dict(by_brand.most_common()))

    out = {"source": "super_pharm_pricefull_live", "total_catalog": len(catalog),
           "addressable": len(rows), "by_active": dict(by_active),
           "by_brand": dict(by_brand), "rows": rows}
    (HERE / "_addressable_shelf.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {HERE/'_addressable_shelf.json'}")


if __name__ == "__main__":
    main()
