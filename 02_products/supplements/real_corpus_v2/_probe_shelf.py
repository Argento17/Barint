"""TASK-171J probe: inspect the LIVE addressable Super-Pharm shelf.

Classify the live oral-supplement catalog by (a) engine active and (b) brand, so the
MVP run can target the addressable SKUs the adapter stack can actually reach. Identity
only (price feed) — no panel. Aggregate a few store catalogs to widen the addressable set.
"""
import sys, json, pathlib
sys.path.insert(0, r"C:\Bari")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from integrations.clients.il_prices import (
    list_super_pharm_files, fetch_items, is_oral_supplement)

OUT = pathlib.Path(__file__).resolve().parent

# Active-detection over the Hebrew/Latin item name -> engine active slug.
# Precision-first; ordered so a more specific token wins. A miss = "not addressable".
ACTIVE_KW = [
    ("vitamin_b12", ("b12", "b-12", "ויטמין b12", "קובלמין")),
    ("folic_acid", ("חומצה פולית", "פולית", "folic", "folate")),
    ("vitamin_d3", ("d3", "d-3", "ויטמין d", "ויטמין די")),
    ("omega3", ("אומגה 3", "אומגה", "omega", "אומגה3", "epa", "dha", "שמן דגים")),
    ("magnesium", ("מגנזיום", "magnesium", "מגנז")),
    ("vitamin_c", ("ויטמין c", "vitamin c", "ויטמין סי", "חומצה אסקורבית")),
    ("zinc", ("אבץ", "zinc")),
    ("iron", ("ברזל", "iron", "פרוס")),
    ("calcium", ("סידן", "calcium")),
    ("biotin", ("ביוטין", "biotin")),
    ("caffeine", ("קפאין", "caffeine")),
    ("vitamin_e", ("ויטמין e", "vitamin e", "ויטמין אי", "טוקופרול")),
]

# multi-active markers -> ambiguous/deferred blend, NOT a single-active corpus member.
MULTI_MARKERS = ("מולטי", "multi", "קומפלקס", "complex", " + ", "+ ", " ועוד", "b-קומפלקס",
                 "b קומפלקס", "מינרלים", "ויטמינים")

# Brand normalization from manufacturer/name -> coarse brand bucket.
BRAND_KW = {
    "altman": ("altman", "אלטמן"),
    "supherb": ("supherb", "סופהרב", "סאפהרב", "סאפ הרב", "אמברוזיה", "ambrosia"),
    "life": ("life", "לייף", "לייף ", "ל.מ.מ", "סופר-פארם", "super-pharm", "super pharm"),
    "solgar": ("solgar", "סולגאר", "סולגר"),
    "tink": ("tink", "tinc", "טינק"),
    "now": ("now foods", "נאו"),
    "centrum": ("centrum", "סנטרום"),
    "floris": ("floris", "florish", "פלוריש", "פלוריס"),
    "magnesia": ("magnesia", "מגנזיה"),
    "amorphical": ("amorphical", "אמורפיקל"),
    "marshall": ("marshall", "מרשל"),
    "sequoia": ("sequoia", "סקויה"),
    "neópharm": ("neopharm", "ניאופארם"),
}


def detect_active(name):
    if any(m in name.lower() for m in MULTI_MARKERS):
        # still allow a clear single active to override only if exactly one active matched
        pass
    n = name.lower()
    hits = []
    for slug, kws in ACTIVE_KW:
        if any(k in n for k in kws):
            hits.append(slug)
    return hits


def detect_brand(name, manuf):
    blob = f"{manuf or ''} {name}".lower()
    for b, kws in BRAND_KW.items():
        if any(k in blob for k in kws):
            return b
    return "other"


def main():
    files = list_super_pharm_files("PriceFull", max_pages=2)  # walk up to ~40 store catalogs
    print(f"Super-Pharm PriceFull files listed: {len(files)}")
    # aggregate several stores to widen the unique-barcode shelf
    seen = {}
    stores_used = 0
    for f in files[:6]:
        try:
            items = fetch_items(f, limit=None)
        except Exception as e:
            print(f"  store {f.store_id}: fetch error {e}")
            continue
        stores_used += 1
        for it in items:
            if it.barcode not in seen and is_oral_supplement(it.name):
                seen[it.barcode] = it
    print(f"aggregated {stores_used} stores -> {len(seen)} unique oral-supplement barcodes")

    addressable = {}        # barcode -> (item, [actives], brand)
    multi = 0
    for bc, it in seen.items():
        hits = detect_active(it.name)
        is_multi = any(m in it.name.lower() for m in MULTI_MARKERS)
        if len(hits) == 1 and not is_multi:
            addressable[bc] = (it, hits[0], detect_brand(it.name, it.manufacturer))
        elif len(hits) >= 1 and is_multi:
            multi += 1

    print(f"\naddressable single-active SKUs: {len(addressable)}  (deferred multi/blend: {multi})")

    by_active, by_brand = {}, {}
    for bc, (it, act, brand) in addressable.items():
        by_active[act] = by_active.get(act, 0) + 1
        by_brand[brand] = by_brand.get(brand, 0) + 1

    print("\nby active:")
    for a, n in sorted(by_active.items(), key=lambda x: -x[1]):
        print(f"  {a:14s} {n}")
    print("\nby brand:")
    for b, n in sorted(by_brand.items(), key=lambda x: -x[1]):
        print(f"  {b:14s} {n}")

    # dump the addressable list for the run harness
    rows = []
    for bc, (it, act, brand) in addressable.items():
        rows.append({
            "barcode": bc, "name_he": it.name, "brand_bucket": brand,
            "manufacturer": it.manufacturer, "active": act, "price_ils": it.price,
            "source": it.provenance.source if it.provenance else None,
            "source_url": it.provenance.source_url if it.provenance else None,
        })
    (OUT / "_addressable_shelf.json").write_text(
        json.dumps({"count": len(rows), "by_active": by_active, "by_brand": by_brand,
                    "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT/'_addressable_shelf.json'}")


if __name__ == "__main__":
    main()
