#!/usr/bin/env python3
"""
TASK-061 build + TASK-080 reconciliation — the single authoritative Hummus dataset.

Produces ONE website-consumable artifact: {_meta, products} where products are
BariProductVM and nutrition is BariNutritionVM (camelCase, the shape the UI renders).

Product Agent ruling (TASK-080):
  - nutrition panel VISIBLE
  - fat suppressed   (fat: null  -> NutritionGrid hides the cell)
  - saturated_fat suppressed (absent from BSIP1; never emitted)
  - do NOT null the whole panel

Source: run_hummus_002 ONLY (run_hummus_001 is INVALID and never read).
  - scores/grades/confidence : QA-reviewed run_hummus_002 build (deployed VM file),
    asserted via _meta.source_run_id == run_hummus_002.
  - nutrition + ingredients  : BSIP1 canonical records, mapped to BariNutritionVM.

BariNutritionVM rendered keys (NUTRIENT_LABELS): energyKcal, protein, sugar, fat, sodium.
  energyKcal = bsip1 energy_kcal | protein = protein_g | sodium = sodium_mg
  fiber      = dietary_fiber_g (carried; not in grid) | fat = null (SUPPRESSED) | sugar = null (HUM-002)
  carbohydrates_g has no VM field -> dropped (consistent with the view model).

Output: ./hummus_frontend_v1.json  (canonical; deployed verbatim to the website).
"""
import json, glob, datetime, collections, statistics, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE       = os.path.dirname(os.path.abspath(__file__))
DEPLOYED   = r"C:\bari-web\src\data\comparisons\hummus_frontend_v1.json"
BSIP1_GLOB = r"C:\Bari\02_products\hummus\canonical_bsip1\bsip1_*.json"
OUT        = os.path.join(HERE, "hummus_frontend_v1.json")
GENERATED  = datetime.datetime.now(datetime.timezone.utc).isoformat()

TYPE_LABELS = {
    "hummus_spread": "חומוס", "matbucha": "מטבוחה", "eggplant_spread": "סלט חצילים",
    "pepper_spread": "ממרח פלפלים", "masabacha": "מסבחה", "other_spread": "ממרח אחר",
}

# ── Authoritative scored records (run_hummus_002) ─────────────────────────────
dep = json.load(open(DEPLOYED, encoding="utf-8"))
assert (dep.get("_meta") or {}).get("source_run_id") == "run_hummus_002", \
    "Refusing to build: deployed source is not run_hummus_002"
scored_records = dep["products"]

# ── BSIP1 nutrition + ingredients ─────────────────────────────────────────────
bsip1 = {}
for f in glob.glob(BSIP1_GLOB):
    d = json.load(open(f, encoding="utf-8"))
    bsip1[d["canonical_product_id"]] = d

def to_nutrition_vm(raw):
    """Map BSIP1 nutrition -> BariNutritionVM. fat suppressed (null); sugar absent (null)."""
    if not raw:
        return None
    return {
        "energyKcal": raw.get("energy_kcal"),
        "protein":    raw.get("protein_g"),
        "sugar":      None,                       # HUM-002 — no sugar data
        "fat":        None,                       # HUM-001 / TASK-060 Option B — SUPPRESSED
        "fiber":      raw.get("dietary_fiber_g"),
        "sodium":     raw.get("sodium_mg"),
    }

# ── Build BariProductVM products ──────────────────────────────────────────────
products = []
fat_dropped = 0
panels_visible = 0
for rec in scored_records:
    pid = rec["id"]
    b1  = bsip1.get(pid, {})
    raw = b1.get("normalized_nutrition_per_100g") or {}
    if raw.get("fat_g") is not None:
        fat_dropped += 1

    insufficient = rec.get("confidence") == "insufficient" or rec.get("score") is None
    nutrition = None if insufficient else to_nutrition_vm(raw)
    if nutrition and any(nutrition[k] is not None for k in ("energyKcal", "protein", "sodium")):
        panels_visible += 1

    products.append({
        "id": pid,
        "name": rec.get("name") or b1.get("canonical_name_he"),
        "_product_type": rec.get("_product_type"),
        "imageUrl": rec.get("imageUrl") or b1.get("image_url"),
        "score": rec.get("score"),
        "grade": rec.get("grade"),
        "insightLine": "",                                  # Content Agent fills (TASK-067/073)
        "confidence": rec.get("confidence"),
        "expansion": {
            "nutrition": nutrition,                         # VM shape; fat=null
            "ingredients": b1.get("ingredients_text_he") or None,
            "confidenceLabel": (rec.get("expansion") or {}).get("confidenceLabel") or "",
            "servingNote": (rec.get("expansion") or {}).get("servingNote") or "ל-100 גרם",
        },
    })

# Hard guarantees
for p in products:
    nut = p["expansion"]["nutrition"]
    if isinstance(nut, dict):
        assert nut.get("fat") is None, f"FAT LEAK (fat not null) in {p['id']}"
        assert set(nut.keys()) == {"energyKcal","protein","sugar","fat","fiber","sodium"}, \
            f"nutrition not in BariNutritionVM shape for {p['id']}"

# ── Aggregates ────────────────────────────────────────────────────────────────
scores = [p["score"] for p in products if p["score"] is not None]
grade_dist = collections.Counter(p["grade"] for p in products)
type_dist  = collections.Counter(p["_product_type"] for p in products)
conf_dist  = collections.Counter(p["confidence"] for p in products)

# ── Single authoritative artifact: {_meta (+docs nested), products} ───────────
out = {
    "_meta": {
        "schema": "BariProductVM[]",
        "generated": GENERATED,
        "category": "hummus",
        "version": "v1-authoritative",
        "product_count": len(products),
        "scored_count": len(scores),
        "source_run_id": "run_hummus_002",
        "invalid_run_never_used": "run_hummus_001",
        "authoritative": True,
        "reconciliation_task": "TASK-080",
        "build_task": "TASK-061",
        "name_he": "חומוס וממרחים",
        "name_en": "Hummus & Savory Spreads",
        "retailer": "shufersal",
        "scrape_date": "2026-05-30",
        "grade_distribution": dict(grade_dist),
        "confidence_distribution": dict(conf_dist),
        "product_type_distribution": dict(type_dist),
        "score_statistics": {
            "count": len(scores), "min": min(scores), "max": max(scores),
            "mean": round(statistics.mean(scores), 2),
            "median": round(statistics.median(scores), 2),
        },
        "nutrition_policy": {
            "panel_visible": True,
            "suppressed": ["fat", "saturated_fat"],
            "suppressed_reason": "HUM-001 — Shufersal fat-row defect (TASK-039); TASK-060 Option B; "
                                 "Product ruling TASK-080: show panel, hide fat only.",
            "rendered_fields": ["energyKcal", "protein", "sodium"],
            "null_fields": {"sugar": "HUM-002 no sugar coverage", "fat": "suppressed",
                            "fiber": "carried but not in NUTRIENT_LABELS grid"},
            "fat_values_dropped": fat_dropped,
            "panels_visible": panels_visible,
            "remediation": "Fix Shufersal fat scraper -> run_hummus_003 -> restore fat in v2 (Q3 2026).",
        },
        "known_limitations": [
            {"id": "HUM-001", "severity": "high",
             "title": "fat corrupted ~58/69 — fat hidden (panel kept)",
             "detail": "Scraper captured saturated-fat sub-row (TASK-039). fat=null per ruling; other nutrition shown."},
            {"id": "HUM-002", "severity": "medium",
             "title": "sugars_g 0% coverage", "detail": "sugar=null; not surfaced."},
            {"id": "HUM-003", "severity": "low",
             "title": "run_hummus_001 INVALID — not used", "detail": "run_002 authoritative (TASK-044 routing fix)."},
            {"id": "HUM-004", "severity": "high",
             "title": "2 products score-unavailable",
             "detail": "confidence=insufficient -> null score/grade; UI shows 'no data' state.",
             "products": [p["id"] for p in products if p["score"] is None]},
        ],
        "qa_notes": {
            "pre_launch_qa": "TASK-072 — verdict WARN; W-1 (content spec) gates final sign-off (TASK-073).",
            "data_qa": "qa_report_hummus.md PASS (TRC-003, COV-005 non-blocking).",
            "go_live_gate": "DEC-002 pending (Product approval), gated on TASK-073.",
        },
    },
    "products": products,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Written: {OUT}  ({os.path.getsize(OUT)/1024:.1f} KB)")
print(f"  products {len(products)} | scored {len(scores)} | grade {dict(grade_dist)}")
print(f"  fat values dropped: {fat_dropped} | visible nutrition panels: {panels_visible}")
print(f"  nutrition shape: BariNutritionVM (fat=null, sugar=null)")
