"""
TASK-362 pages 3+4 — Score the chocolate scrape through the BSIP2 engine.

Input : 02_products/chocolate/bsip0_outputs/choc_bsip0_raw_*.json (146 products).
Gates : light chocolate scope filter (drop gift boxes / pralines / seasonal /
        eggs / coins / figures that aren't a flat tablet or a countline bar) +
        plausibility_gate (per-100g sanity). Engine: build_bsip1 + run_bsip2 from
        run_task360_phase3 (same proven path as the bars). classify_chocolate
        splits chocolate_tablet vs chocolate_bar (countline).

Output: BSIP1 + BSIP2 traces + a scored manifest split by the two chocolate shelves.
        Data only — no frontend, no copy (those follow the two-gate pipeline).
"""
from __future__ import annotations
import glob, json, pathlib, sys, datetime, re

ROOT = pathlib.Path(r"C:\Bari")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(ROOT / "02_products" / "snack_bars"))
sys.path.insert(0, str(ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))

from plausibility_gate import classify_chocolate
from bsip0_nutrition import parse_nutrition_numeric
import run_task360_phase3 as P3

# ── light chocolate scope: drop formats that aren't a flat tablet or a countline ──
# (assortment boxes, pralines/truffles, seasonal gifts, eggs, coins, figures,
#  baking/cooking chocolate, spreads/drinks that slipped past the scraper exclude).
_OUT = [
    "מארז", "מבחר", "אסורטי", "מתנה", "סלסל", "קופסה", "קופסת",
    "פרלין", "בונבונ", "טרופל", "כדורי שוקולד", "כדורים",
    "חג", "פורים", "משלוח מנות", "חנוכה", "סנטה", "ביצת", "ביצה",
    "מטבע", "דמות", "סוכריה על מקל", "מדליה",
    "לאפיה", "לבישול", "קוברטור", "קולינר", "אבקת", "קקאו לאפיה",
    "ממרח", "משקה", "שתיה", "שתייה", "סירופ", "נוטלה",
]
def in_scope(name: str, ingr: str) -> bool:
    nm = (name or "")
    return not any(tok in nm for tok in _OUT)

RUN_ID = "score_choc_task362_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / RUN_ID / "output"
BSIP2_DIR = ROOT / "02_products" / "chocolate" / "bsip2_outputs" / RUN_ID / "products"
for d in (BSIP1_DIR, BSIP2_DIR):
    d.mkdir(parents=True, exist_ok=True)

raw_path = sorted(glob.glob(str(ROOT / "02_products/chocolate/bsip0_outputs/choc_bsip0_raw_*.json")))[-1]
raw = json.load(open(raw_path, encoding="utf-8"))
print(f"loaded {len(raw)} scraped chocolate from {pathlib.Path(raw_path).name}")

scored = []
counts = {"out_of_scope": 0, "no_nutrition": 0, "quarantine": 0, "scored": 0}
seen_barcodes = set()
for p in raw:
    name = p.get("name_he") or p.get("name", "")
    barcode = p.get("barcode", "")
    if not barcode or barcode in seen_barcodes:
        continue
    seen_barcodes.add(barcode)
    if not in_scope(name, p.get("ingredients_raw", "")):
        counts["out_of_scope"] += 1; continue

    nutr_num = parse_nutrition_numeric(p["nutrition"])
    if nutr_num.get("energy_kcal") is None and nutr_num.get("carbohydrates_g") is None:
        counts["no_nutrition"] += 1; continue

    gate = P3.run_plausibility_gate(nutr_num, p.get("ingredients_raw", ""), barcode,
                                    p.get("serving_size_g_hint"))
    if gate["verdict"] not in ("pass", "converted_pass"):
        counts["quarantine"] += 1; continue

    meta = {"description": name, "name_truncated": name, "brand": p.get("brand", ""),
            "code": "P_" + barcode, "sku": barcode, "image_url": (p.get("image_urls") or [""])[0],
            "unit_description": "", "health_attrs": [], "all_cat_codes": []}
    scraped = {"plausibility_gate": gate, "ingredients_raw": p.get("ingredients_raw", ""),
               "weight_g": p.get("weight_g"), "serving_g": p.get("serving_size_g_hint"),
               "nutrition_numeric_per_100g": nutr_num}
    bsip1 = P3.build_bsip1(meta, scraped, barcode, RUN_ID)
    bsip1_path = BSIP1_DIR / f"bsip1_{barcode}.json"
    bsip1_path.write_text(json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8")

    res = P3.run_bsip2(bsip1_path, BSIP2_DIR)
    if res["status"] != "ok":
        print("  BSIP2 ERROR", barcode, res.get("error")); continue
    tr = res["trace"]
    sc_val = tr.get("final_score_estimate", tr.get("score"))
    scored.append({
        "barcode": barcode, "name": name, "brand": p.get("brand", ""),
        "score": round(sc_val, 1) if sc_val is not None else None,
        "grade": tr.get("grade_estimate", tr.get("grade")),
        "category": classify_chocolate(name),
        "engine_category": tr.get("category"),
        "kcal": nutr_num.get("energy_kcal"), "sugar_g": nutr_num.get("sugars_g"),
        "satfat_g": nutr_num.get("saturated_fat_g"),
    })
    counts["scored"] += 1

tablets = sorted([s for s in scored if s["category"] == "chocolate_tablet"], key=lambda x: -(x["score"] or 0))
bars = sorted([s for s in scored if s["category"] == "chocolate_bar"], key=lambda x: -(x["score"] or 0))

def dist(items):
    from collections import Counter
    return dict(Counter(s["grade"] for s in items))

print("\n=== FUNNEL ===", counts)
print(f"\n=== TABLETS ({len(tablets)}) grades={dist(tablets)} | engine_cats={set(s['engine_category'] for s in tablets)} ===")
print(f"=== COUNTLINE BARS ({len(bars)}) grades={dist(bars)} | engine_cats={set(s['engine_category'] for s in bars)} ===")

manifest = {"run_id": RUN_ID, "scored": len(scored), "funnel": counts,
            "chocolate_tablet": tablets, "chocolate_bar": bars,
            "bsip1_dir": str(BSIP1_DIR), "bsip2_dir": str(BSIP2_DIR),
            "source_scrape": pathlib.Path(raw_path).name}
out = ROOT / "02_products" / "chocolate" / f"{RUN_ID}_manifest.json"
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nmanifest:", out)
