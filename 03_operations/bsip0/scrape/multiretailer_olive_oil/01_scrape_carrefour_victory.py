"""
BSIP0 — Olive Oil: Carrefour + Victory API scraper

Both retailers share the same backend platform (retailer IDs differ).
No Playwright needed — pure REST API with JSON response.

Outputs:
  02_products/olive_oil/bsip0_raw/carrefour/all_discovered_raw.json
  02_products/olive_oil/bsip0_raw/victory/all_discovered_raw.json
"""

import sys, json, urllib.parse, urllib.request, re, pathlib, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RETAILERS = [
    {
        "name": "carrefour",
        "host": "www.carrefour.co.il",
        "retailer_id": 1540,
        "branch_id": 3003,
    },
    {
        "name": "victory",
        "host": "www.victoryonline.co.il",
        "retailer_id": 1470,
        "branch_id": 2930,
    },
]

BASE_FILTERS = json.dumps({
    "must": {
        "exists": ["family.id", "family.categoriesPaths.id", "branch.regularPrice"],
        "term": {"branch.isActive": True, "branch.isVisible": True},
    },
    "mustNot": {"term": {"branch.regularPrice": 0}},
})

# Signals for olive oil relevance (cooking oil, not tuna/labaneh that contain olive oil)
OLIVE_OIL_RE = re.compile(
    r"שמן\s*זית\s*(כתית|קלאסי|ישראלי|פרמיום|בכבישה|טהור|מעולה|תרסיס|ארומה|זן)",
    re.IGNORECASE,
)
REJECT_RE = re.compile(
    r"טונה|סרדין|לאבנה|גבינה|ממרח|זיתים|קרקר|פיצה|כעכ|רוטב|מרכך|קמיל|בשמן",
    re.IGNORECASE,
)

OUT_DIR = pathlib.Path(r"C:\Bari\02_products\olive_oil\bsip0_raw")


def fetch_all(host: str, rid: int, bid: int) -> list:
    all_products, offset, PAGE = [], 0, 50
    while True:
        params = urllib.parse.urlencode({
            "appId": "4",
            "filters": BASE_FILTERS,
            "from": str(offset),
            "isSearch": "true",
            "languageId": "1",
            "query": "שמן זית",
            "size": str(PAGE),
        })
        url = f"https://{host}/v2/retailers/{rid}/branches/{bid}/products?{params}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124",
            "Accept": "application/json",
            "Referer": f"https://{host}/",
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        products = data.get("products", [])
        total = data.get("total", 0)
        all_products.extend(products)
        print(f"  offset={offset} fetched={len(products)} total={total}")
        if offset + PAGE >= total or not products:
            break
        offset += PAGE
    return all_products


def extract_fields(p: dict) -> dict:
    name_obj = (p.get("names") or {}).get("1", {})
    name = name_obj.get("long", "") if isinstance(name_obj, dict) else ""
    name = name or p.get("localName", "") or ""
    brand_obj = p.get("brand") or {}
    brand = (brand_obj.get("names") or {}).get("1", "") or ""
    ingr = ((p.get("data") or {}).get("1") or {}).get("ingredients", "") or ""
    price = ((p.get("branch") or {}).get("regularPrice") or 0)
    weight = p.get("weight", "")
    product_id = p.get("id") or p.get("productId") or ""
    return {
        "id": product_id,
        "name": name,
        "brand": brand,
        "ingredients": ingr,
        "price": price,
        "weight": weight,
    }


def is_olive_oil(rec: dict) -> bool:
    name = rec["name"]
    ingr = rec["ingredients"]
    if REJECT_RE.search(name):
        return False
    if OLIVE_OIL_RE.search(name):
        return True
    # Fallback: name contains שמן זית and ingredients are just שמן זית כתית
    if "שמן זית" in name and ("כתית" in ingr or ingr == ""):
        return True
    return False


def main():
    scraped_at = datetime.datetime.utcnow().isoformat() + "Z"

    for r in RETAILERS:
        rname = r["name"]
        host = r["host"]
        rid = r["retailer_id"]
        bid = r["branch_id"]

        print(f"\n{'='*50}")
        print(f"Retailer: {rname} (retailer_id={rid}, branch_id={bid})")

        raw = fetch_all(host, rid, bid)
        records = [extract_fields(p) for p in raw]

        olive = [rec for rec in records if is_olive_oil(rec)]
        rejected = [rec for rec in records if not is_olive_oil(rec)]

        print(f"\n  Total fetched: {len(records)}")
        print(f"  Olive oil products: {len(olive)}")
        print(f"  Rejected (tuna/labaneh/etc): {len(rejected)}")

        brands = {}
        for rec in olive:
            b = rec["brand"] or "(no brand)"
            brands.setdefault(b, []).append(rec["name"])

        print(f"\n  Olive oil brands ({len(brands)}):")
        for b, prods in sorted(brands.items(), key=lambda x: -len(x[1])):
            print(f"    [{len(prods):2d}] {b}")

        out = {
            "retailer": rname,
            "retailer_id": rid,
            "branch_id": bid,
            "scraped_at": scraped_at,
            "total_search_results": len(records),
            "olive_oil_products": olive,
            "rejected_products": [r["name"] for r in rejected],
        }

        out_path = OUT_DIR / rname / "all_discovered_raw.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n  Saved to {out_path}")


if __name__ == "__main__":
    main()
