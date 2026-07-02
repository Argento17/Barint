import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DATA_DIR = r"C:\bari\bari-web\src\data\comparisons"

CATEGORY_JSON_MAP = {
    "bread": "bread_frontend_v3.json",
    "breakfast-cereals": "cereals_frontend_v2.json",
    "brined-cheeses": "brined_cheeses_frontend_v2.json",
    "cakes": "cakes_hard_cookies_frontend_v1.json",
    "cheese": "cheese_frontend_v4.json",
    "chocolate-bars": "chocolate_bars_frontend_v1.json",
    "chocolate-tablets": "chocolate_tablets_frontend_v1.json",
    "cookies-coffee": "cookies_coffee_frontend_v2.json",
    "granola": "granola_frontend_v1.json",
    "hard-cheeses": "hard_cheeses_frontend_v2.json",
    "hummus": "hummus_frontend_v5.json",
    "juices": "juices_frontend_v3.json",
    "milk-comparison": "milk_frontend_v1.json",
    "protein-bars": "protein_combined_frontend_v2.json",
    "snacks": "snacks_frontend_v5.json",
}

print("Scanning for null expansion.nutrition.sugar across all frontend JSONs...")
print()

all_null_sugar = []
category_summary = []

for cat, fname in CATEGORY_JSON_MAP.items():
    fpath = os.path.join(DATA_DIR, fname)
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    prods = data.get("products", data if isinstance(data, list) else [])
    total = len(prods)
    null_sugar = []

    for p in prods:
        exp = p.get("expansion", {})
        nutr = exp.get("nutrition", {}) if isinstance(exp, dict) else {}
        sugar = nutr.get("sugar") if isinstance(nutr, dict) else None

        if sugar is None:
            rank = p.get("rank", None)
            is_top3 = rank is not None and isinstance(rank, int) and rank <= 3

            null_sugar.append({
                "category": cat,
                "name": p.get("name", "UNKNOWN"),
                "barcode": p.get("barcode", p.get("id", "UNKNOWN")),
                "score": p.get("score", "N/A"),
                "grade": p.get("grade", "N/A"),
                "rank": rank,
                "is_top3": is_top3,
                "nutrition": nutr,
            })
            all_null_sugar.append(null_sugar[-1])

    category_summary.append({
        "category": cat,
        "total": total,
        "null_sugar": len(null_sugar),
        "null_sugar_products": null_sugar,
    })

print("=" * 80)
print("CATEGORY SUMMARY: null sugar in expansion.nutrition.sugar")
print("=" * 80)
for s in category_summary:
    pct = (s["null_sugar"] / s["total"] * 100) if s["total"] > 0 else 0
    print(f"  {s['category']:<25} null_sugar={s['null_sugar']:>3}/{s['total']:<4} ({pct:.0f}%)")

print()
print(f"TOTAL null-sugar products: {len(all_null_sugar)}")
print()
print("=" * 80)
print("DETAIL: All null-sugar products")
print("=" * 80)
for p in all_null_sugar:
    top3_tag = " [TOP3]" if p["is_top3"] else ""
    print(f"  CAT: {p['category']}")
    print(f"  NAME: {p['name']}")
    bc = p['barcode']
    sc = p['score']
    gr = p['grade']
    rk = p['rank']
    print(f"  barcode={bc}  score={sc}  grade={gr}  rank={rk}{top3_tag}")
    print(f"  nutrition: {p['nutrition']}")
    print()
