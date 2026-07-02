"""
TASK-391 Stage 1 — Fresh re-score of the chocolate tablets corpus.

Rules:
- Set env flags BEFORE importing the engine (module-level flag reads happen at import).
- Print runtime flag values immediately after import to confirm.
- Use the same bsip0 raw file as the authoritative run (choc_bsip0_raw_20260621T093256.json).
- Write real BSIP2 traces.
- Output a machine-readable manifest for comparison.
- No env vars set explicitly (match the defaults used by the original score_chocolate_task362.py).
"""
from __future__ import annotations
import os, sys, io, json, pathlib, glob, datetime, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")

# ── STEP 1: Set env flags BEFORE importing engine ──────────────────────────────
# The original script set NO env vars — relying entirely on module defaults.
# We do the same: no explicit sets. But we do NOT inherit any env BARI_ vars
# that might be set in the shell, so we explicitly clear them to get defaults:
for k in list(os.environ.keys()):
    if k.startswith("BARI_"):
        del os.environ[k]
        print(f"[env-clean] removed inherited {k}")

# ── STEP 2: Import engine ───────────────────────────────────────────────────────
sys.path.insert(0, str(ROOT / "02_products" / "snack_bars"))
sys.path.insert(0, str(ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))

from plausibility_gate import classify_chocolate
from bsip0_nutrition import parse_nutrition_numeric
import run_task360_phase3 as P3

# ── STEP 3: Print runtime flag values (from the imported score_engine) ──────────
bsip2_src = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
sys.path.insert(0, str(bsip2_src))
import score_engine as SE

print("\n=== RUNTIME FLAG VALUES (read at import time) ===")
flags = {
    "BARI_GRAN_SUGAR_25G_V1": SE.BARI_GRAN_SUGAR_25G_V1,
    "BARI_GLASSBOX_W4":       SE.BARI_GLASSBOX_W4,
    "BARI_FIBER_FERMENT_V1":  SE.BARI_FIBER_FERMENT_V1,
    "BARI_SHELF_RELATIVE_V1": SE.BARI_SHELF_RELATIVE_V1,
    "BARI_FAT_TECH_V1":       SE.BARI_FAT_TECH_V1,
    "BARI_REDLABEL_V1":       SE.BARI_REDLABEL_V1,
    "BARI_TASK144_FIXES_ON":  SE.TASK144_FIXES_ON,
    "BARI_RECAL_P0_ON":       SE.RECAL_P0_ON,
    "BARI_GRAD_SODIUM_V1":    SE.BARI_GRAD_SODIUM_V1,
    "BARI_D4_SCORE_V1":       SE.BARI_D4_SCORE_V1,
    "BARI_HC_DAIRY_SATFAT_V1": SE.BARI_HC_DAIRY_SATFAT_V1,
    "BARI_TASK250_CONF":      SE.BARI_TASK250_CONF,
    "BARI_GLASSBOX_D5D6_ON":  SE.GLASSBOX_D5D6_ON,
    "BARI_SODIUM_CEREAL":     SE.BARI_SODIUM_CEREAL,
}
for k, v in flags.items():
    print(f"  {k} = {v}")
print()

# ── STEP 4: Same scope filter as original ──────────────────────────────────────
_OUT = [
    "מארז", "מבחר", "אסורטי", "מתנה", "סלסל", "קופסה", "קופסת",
    "פרלין", "בונבונ", "טרופל", "כדורי שוקולד", "כדורים",
    "חג", "פורים", "משלוח מנות", "חנוכה", "סנטה", "ביצת", "ביצה",
    "מטבע", "דמות", "סוכריה על מקל", "מדליה",
    "לאפיה", "לבישול", "קוברטור", "קולינר", "אבקת", "קקאו לאפיה",
    "ממרח", "משקה", "שתיה", "שתייה", "סירופ", "נוטלה",
]
def in_scope(name: str) -> bool:
    return not any(tok in (name or "") for tok in _OUT)

# ── STEP 5: Setup run dirs ─────────────────────────────────────────────────────
RUN_ID = "fresh_rescore_task391_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BSIP1_DIR = ROOT / "03_operations" / "bsip1" / RUN_ID / "output"
BSIP2_DIR = ROOT / "02_products" / "chocolate" / "bsip2_outputs" / RUN_ID / "products"
for d in (BSIP1_DIR, BSIP2_DIR):
    d.mkdir(parents=True, exist_ok=True)

print(f"RUN_ID: {RUN_ID}")
print(f"BSIP1_DIR: {BSIP1_DIR}")
print(f"BSIP2_DIR: {BSIP2_DIR}")

# ── STEP 6: Use the same scrape file as the authoritative run ──────────────────
raw_path = ROOT / "02_products/chocolate/bsip0_outputs/choc_bsip0_raw_20260621T093256.json"
raw = json.load(open(raw_path, encoding="utf-8"))
print(f"\nLoaded {len(raw)} products from {raw_path.name}")

# ── STEP 7: Score all products ─────────────────────────────────────────────────
scored = []
counts = {"out_of_scope": 0, "no_nutrition": 0, "quarantine": 0, "scored": 0}
seen_barcodes = set()

for p in raw:
    name = p.get("name_he") or p.get("name", "")
    barcode = p.get("barcode", "")
    if not barcode or barcode in seen_barcodes:
        continue
    seen_barcodes.add(barcode)
    if not in_scope(name):
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
        print(f"  BSIP2 ERROR {barcode}: {res.get('error')}"); continue
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

# ── STEP 8: Split and sort ─────────────────────────────────────────────────────
from collections import Counter
def dist(items): return dict(Counter(s["grade"] for s in items))

tablets = sorted([s for s in scored if s["category"] == "chocolate_tablet"], key=lambda x: -(x["score"] or 0))
bars = sorted([s for s in scored if s["category"] == "chocolate_bar"], key=lambda x: -(x["score"] or 0))

print(f"\n=== FUNNEL ===", counts)
print(f"=== TABLETS ({len(tablets)}) grades={dist(tablets)} ===")
print(f"=== BARS ({len(bars)}) grades={dist(bars)} ===")
print(f"=== ENGINE CATEGORIES (tablets): {set(s['engine_category'] for s in tablets)} ===")

# ── STEP 9: Write manifest ─────────────────────────────────────────────────────
manifest = {
    "run_id": RUN_ID,
    "scored": len(scored),
    "funnel": counts,
    "flag_snapshot": {k: str(v) for k, v in flags.items()},
    "source_scrape": str(raw_path.name),
    "chocolate_tablet": tablets,
    "chocolate_bar": bars,
    "bsip1_dir": str(BSIP1_DIR),
    "bsip2_dir": str(BSIP2_DIR),
}
out = ROOT / "02_products" / "chocolate" / f"{RUN_ID}_manifest.json"
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nManifest written: {out}")

# ── STEP 10: Print tablet scores for comparison ────────────────────────────────
print("\n=== TABLET SCORES (fresh run) ===")
print(f"{'barcode':<16} {'name'[:30]:<32} {'score':>6} {'grade':>5}")
print("-" * 65)
for t in tablets:
    print(f"{t['barcode']:<16} {t['name'][:30]:<32} {str(t['score']):>6} {t['grade']:>5}")
