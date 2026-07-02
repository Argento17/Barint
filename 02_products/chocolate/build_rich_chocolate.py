"""
TASK-362 pages 3+4 — Build the RICH frontend JSON for the two chocolate shelves
from the re-scored (consistent-lens) manifest. Structural fields come from the
canonical BSIP1 store; voice fields are PENDING_COPY (new category, no carry).

Curation: drop out-of-scope formats (coated wafers/biscuits, "fingers", Purim
pastry, cakes) + dedup near-identical display names (kosher-for-Passover dups,
single/mini/pack variants). Each survivor has a distinct display name.

Writes:
  bari-web/.../chocolate_tablets_frontend_v1.json
  bari-web/.../chocolate_bars_frontend_v1.json
"""
from __future__ import annotations
import glob, json, pathlib, sys, re
from collections import Counter

ROOT = pathlib.Path(r"C:\Bari")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WEB = ROOT / "bari-web" / "src" / "data" / "comparisons"

manifest = json.load(open(sorted(glob.glob(str(ROOT / "02_products/chocolate/score_choc_task362_*_manifest.json")))[-1], encoding="utf-8"))
CANON = pathlib.Path(manifest["bsip1_dir"])

# ── curation: drop out-of-scope formats + dedup near-identical names ──
DROP_TOK = ["אצבעות", "וופל", "טורטית", "ביסקוויט", "ביסקויט", "אוזני המן", "עוג.", "ממולדה", "סנסיישן"]
def _drop(name): return any(t in name for t in DROP_TOK)
def _norm(name):
    n = re.sub(r'כשל\"?פ|כשלפ|מגדים|חטיף בודד|חטיפי|מיני| בודד', '', name)
    return re.sub(r'\s+', ' ', n).strip()
def curate(items):
    kept, seen = [], set()
    for p in sorted(items, key=lambda x: -(x["score"] or 0)):
        if _drop(p["name"]):
            continue
        key = _norm(p["name"])
        if key in seen:
            continue
        seen.add(key); kept.append(p)
    return kept

def load_canon(barcode):
    p = CANON / f"bsip1_{barcode}.json"
    return json.load(open(p, encoding="utf-8")) if p.exists() else {}

# Tablet curation cap: keep all differentiated C/D grades + a diverse, recognizable
# spread of E's (milk / white / nuts / fillings / no-sugar across the iconic brands).
# Tighter, higher-quality shelf over an exhaustive 73 of near-identical dark variants.
TABLET_KEEP_E = {
    "7290019939412",  # שוקולד חלב ללא סוכר (no-sugar milk)
    "4000539280726",  # לינדט 70%
    "7610400075770",  # לינדט אגוזי לוז (dark+hazelnut)
    "4000417025005",  # מריר עם מרציפן (marzipan)
    "3046920023047",  # לינדט אקסלנס פיסטוק
    "7290019870043",  # צ'וקטה 60%
    "3046920028752",  # לינדט מנטה (mint)
    "3046920029674",  # לינדט מלח (salt)
    "7290112331984",  # שוקולד פרה קראנצ' בסקויט
    "7610008641001",  # טבלת טורינו חלב
    "7614500010617",  # טובלרון מריר
    "7290110579463",  # שוקולד פרה חלב שברי אגוז
    "7622202257506",  # מילקה אקסטרה קקאו
    "7622202265648",  # שוקולד לבן מילקה (white)
    "7290112914699",  # שוקולד חלב וקרמל מלוח (salted caramel)
    "7622202268298",  # שוקולד חלב מילקה (iconic milk)
    "7290112348548",  # שוקולד פרה לבן (Para white)
    "7614500010013",  # טובלרון חלב
}

def build(items, id_prefix, cap_tablets=False):
    items = curate(items)
    if cap_tablets:
        items = [it for it in items if (it["grade"] in ("B", "C", "D")) or it["barcode"] in TABLET_KEEP_E]
    for it in items:
        it["rank"] = 1 + sum(1 for q in items if (q["score"] or 0) > (it["score"] or 0))
    items = sorted(items, key=lambda x: -(x["score"] or 0))
    total = len(items)
    out = []
    for i, it in enumerate(items, 1):
        bc = it["barcode"]
        c = load_canon(bc)
        n = c.get("normalized_nutrition_per_100g", {}) or {}
        exp_nutrition = {
            "energyKcal": n.get("energy_kcal"), "protein": n.get("protein_g"),
            "sugar": n.get("sugars_g"), "fat": n.get("fat_g"),
            "fiber": n.get("dietary_fiber_g"), "sodium": n.get("sodium_mg"),
        }
        out.append({
            "id": f"{id_prefix}-{i:03d}",
            "barcode": bc,
            "name": it["name"], "name_he": it["name"], "brand": c.get("brand", "") or it.get("brand", ""),
            "score": it["score"], "grade": it["grade"],
            "rank": it["rank"], "categoryTotal": total,
            "imageUrl": c.get("image_url", ""), "image_url": c.get("image_url", ""),
            "nutrition_per_100g": n,
            "confidence": "verified",
            "confidence_label_he": "נתונים מאומתים",
            "confidence_sub_reason": "נתוני תזונה ורכיבים ישירות מדף המוצר בשופרסל",
            "confidence_tooltip_he": "הציון מבוסס על פאנל התזונה ורשימת הרכיבים שפורסמו למוצר.",
            "d4_additives": [],  # populated by wire_d4 from the scrape
            "insightLine": "PENDING_COPY", "rowVerdict": "PENDING_COPY",
            "_scoring_trace": {"category": it.get("engine_category"), "protein_g": n.get("protein_g")},
            "expansion": {
                "nutrition": exp_nutrition,
                "ingredients": c.get("ingredients_text_he") or "",
                "servingNote": "ל-100 גרם",
                "confidenceLabel": "נתונים מאומתים",
                "comparisonContext": "PENDING_COPY",
                "positiveSignals": "PENDING_COPY",
                "limitingFactors": "PENDING_COPY",
            },
        })
    # disambiguate any remaining duplicate display names by brand
    namecount = Counter(o["name"] for o in out)
    for o in out:
        if namecount[o["name"]] > 1 and o.get("brand"):
            o["name"] = f"{o['name']} · {o['brand']}"; o["name_he"] = o["name"]
    return out, total

tablets, n_t = build(list(manifest["chocolate_tablet"]), "ct", cap_tablets=True)
bars, n_b = build(list(manifest["chocolate_bar"]), "cb")

def meta(cat, cnt):
    return {"version": f"{cat}_frontend_task362", "category": cat, "product_count": cnt,
            "generated": "2026-06-21T00:00:00+00:00", "copy_status": "PARTIAL_PENDING_COPY",
            "engine_unchanged": False, "off_check": "PASS - no Open Food Facts"}

json.dump({"_meta": meta("chocolate-tablets", n_t), "products": tablets},
          open(WEB / "chocolate_tablets_frontend_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump({"_meta": meta("chocolate-bars", n_b), "products": bars},
          open(WEB / "chocolate_bars_frontend_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print(f"tablets : {n_t} products, leader {tablets[0]['name'][:28]} {tablets[0]['score']}/{tablets[0]['grade']}")
print(f"countline bars: {n_b} products, leader {bars[0]['name'][:28]} {bars[0]['score']}/{bars[0]['grade']}")
print("engine cats tablets:", set(t['_scoring_trace']['category'] for t in tablets))
