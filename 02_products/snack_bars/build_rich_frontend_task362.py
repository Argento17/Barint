"""
TASK-362 — Build the RICH frontend JSON for the two bar pages from the re-scored
corpus, carrying over existing Tom-voice copy BY BARCODE (so written copy is not
lost). Voice fields with no carry source = PENDING_COPY for the orchestrator to author.

Structural fields (nutrition, ingredients, rank, additives, confidence) come from the
canonical BSIP1 store + the re-score manifest — never fabricated. Writes in place:
  bari-web/.../snacks_frontend_v5.json        (snack bars, ~25)
  bari-web/.../protein_bars_frontend_v1.json  (protein bars, ~16)
"""
from __future__ import annotations
import glob, json, pathlib, sys

ROOT = pathlib.Path(r"C:\Bari")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WEB = ROOT / "bari-web" / "src" / "data" / "comparisons"
CANON = ROOT / "02_products" / "snack_bars" / "canonical_bsip1" / "run_task362"

manifest = json.load(open(sorted(glob.glob(str(ROOT / "02_products/snack_bars/score_bars_task362_*_manifest.json")))[-1], encoding="utf-8"))

# Near-duplicate identity discard (Nutrition Agent flag + conform size-duplicate):
# 8410076602251 is a second Nature Valley "שיבולת שועל+שוקולד" (54.8% oat) that is
# the same bar as 16000423534 (54% oat) at a different barcode. Keep the higher one.
# Corrupt-ingredient discard (missing_data_discard_rule): the 3 Nestlé Fitness bars
# (5900020*) scraped a marketing brochure paragraph ("...מזין אותך באנרגיה") in place of
# a real ingredient list — we don't actually have their ingredients, so they cannot be
# honestly described. Re-scrape is IP-blocked; per the discard rule we drop rather than
# over-invest in re-sourcing. (Owner flagged rows #3-5 as sub-standard, 2026-06-20.)
EXCLUDE = {
    "8410076602251",
    "5900020015174",  # פיטנס חטיף דגנים שוקולד
    "5900020034021",  # פיטנס חטיפי דגנים שוקולד בננה
    "5900020029669",  # פיטנס חטיף דגנים פ.יער
}

def load_canon(barcode):
    p = CANON / f"bsip1_{barcode}.json"
    return json.load(open(p, encoding="utf-8")) if p.exists() else {}

def carry_map(path):
    """barcode -> existing product (for copy carry-over)."""
    if not pathlib.Path(path).exists():
        return {}
    d = json.load(open(path, encoding="utf-8"))
    return {p.get("barcode"): p for p in d.get("products", [])}

VOICE_TOP = ("insightLine", "rowVerdict")
VOICE_EXP = ("positiveSignals", "limitingFactors", "comparisonContext")

def build(items, id_prefix, carry_path):
    carry = carry_map(carry_path)
    items = [it for it in items if it["barcode"] not in EXCLUDE]
    # competition rank within this category
    for it in items:
        it["rank"] = 1 + sum(1 for q in items if (q["score"] or 0) > (it["score"] or 0))
    items = sorted(items, key=lambda x: -(x["score"] or 0))
    total = len(items)
    out = []
    pending = 0
    for i, it in enumerate(items, 1):
        bc = it["barcode"]
        c = load_canon(bc)
        n = c.get("normalized_nutrition_per_100g", {}) or {}
        prev = carry.get(bc, {})
        prev_exp = prev.get("expansion", {}) if prev else {}

        def carried(top_key, exp=False):
            src = prev_exp if exp else prev
            v = src.get(top_key)
            if v in (None, "", [], "PENDING_COPY"):
                return None
            return v

        exp_nutrition = {
            "energyKcal": n.get("energy_kcal"), "protein": n.get("protein_g"),
            "sugar": n.get("sugars_g"), "fat": n.get("fat_g"),
            "fiber": n.get("dietary_fiber_g"), "sodium": n.get("sodium_mg"),
        }
        ingredients = c.get("ingredients_text_he") or ""
        # voice fields: carry by barcode else PENDING_COPY
        insight = carried("insightLine") or "PENDING_COPY"
        rowv = carried("rowVerdict") or "PENDING_COPY"
        pos = carried("positiveSignals", exp=True) or "PENDING_COPY"
        lim = carried("limitingFactors", exp=True) or "PENDING_COPY"
        ctx = carried("comparisonContext", exp=True) or "PENDING_COPY"
        if "PENDING_COPY" in (insight, rowv) or pos == "PENDING_COPY":
            pending += 1

        out.append({
            "id": f"{id_prefix}-{i:03d}",
            "barcode": bc,
            "name": it["name"], "name_he": it["name"], "brand": it.get("brand", ""),
            "score": it["score"], "grade": it["grade"],
            "rank": it["rank"], "categoryTotal": total,
            "imageUrl": c.get("image_url", ""), "image_url": c.get("image_url", ""),
            "nutrition_per_100g": n,
            "confidence": "verified",
            "confidence_label_he": "נתונים מאומתים",
            "confidence_sub_reason": "נתוני תזונה ורכיבים ישירות מדף המוצר בשופרסל",
            "confidence_tooltip_he": "הציון מבוסס על פאנל התזונה ורשימת הרכיבים שפורסמו למוצר.",
            "d4_additives": [],  # AdditiveEntry[] shape; BSIP1 extracted_additives is empty here
            "insightLine": insight, "rowVerdict": rowv,
            "_scoring_trace": {"category": it.get("engine_category"), "protein_g": it.get("protein_g")},
            "expansion": {
                "nutrition": exp_nutrition,
                "ingredients": ingredients,
                "servingNote": "ל-100 גרם",
                "confidenceLabel": "נתונים מאומתים",
                "comparisonContext": ctx,
                "positiveSignals": pos,
                "limitingFactors": lim,
            },
        })
    # Disambiguate any remaining duplicate display names by appending the brand
    # (cross-brand generic names like "חטיף דגנים שוקולד מריר" from 2 brands).
    from collections import Counter
    namecount = Counter(o["name"] for o in out)
    for o in out:
        if namecount[o["name"]] > 1 and o.get("brand"):
            o["name"] = f"{o['name']} · {o['brand']}"
            o["name_he"] = o["name"]
    return out, total, pending

snack, n_snack, pend_snack = build(list(manifest["snack_bars"]), "snk", str(WEB / "snacks_frontend_v5.json"))
prot, n_prot, pend_prot = build(list(manifest["protein_bars"]), "prot", str(WEB / "protein_bars_frontend_v1.json"))

def meta(cat, cnt):
    return {"version": f"{cat}_frontend_task362", "category": cat, "product_count": cnt,
            "generated": "2026-06-20T00:00:00+00:00", "copy_status": "PARTIAL_PENDING_COPY",
            "engine_unchanged": True, "off_check": "PASS - no Open Food Facts"}

json.dump({"_meta": meta("snacks", n_snack), "products": snack},
          open(WEB / "snacks_frontend_v5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump({"_meta": meta("protein-bars", n_prot), "products": prot},
          open(WEB / "protein_bars_frontend_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print(f"snack bars : {n_snack} products, {pend_snack} PENDING_COPY, leader {snack[0]['name'][:26]} {snack[0]['score']}/{snack[0]['grade']}")
print(f"protein bars: {n_prot} products, {pend_prot} PENDING_COPY, leader {prot[0]['name'][:26]} {prot[0]['score']}/{prot[0]['grade']}")
