"""Build hummus_frontend_v1.json from run_hummus_002."""
import sys, json, pathlib, datetime, statistics

sys.stdout.reconfigure(encoding="utf-8")

BSIP1_DIR    = pathlib.Path(r"C:\Bari\02_products\hummus\canonical_bsip1")
TRACES_DIR   = pathlib.Path(r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_002\products")
VAL_JSON     = pathlib.Path(r"C:\Bari\03_operations\bsip2\run_hummus_002_validation.json")
OUT_JSON     = pathlib.Path(r"C:\Bari\02_products\hummus\hummus_frontend_v1.json")

GENERATED_AT = datetime.datetime.utcnow().isoformat() + "Z"

# ── Load data ────────────────────────────────────────────────────────────────

with open(VAL_JSON, encoding="utf-8") as f:
    val = json.load(f)

full_table  = {r["pid"]: r for r in val["full_score_table"]}
flagged_map = {fp["pid"]: fp for fp in val["flagged_products"]}
insuff_pids = {fp["pid"] for fp in val["insufficient_products"]}

bsip1 = {}
for p in sorted(BSIP1_DIR.glob("bsip1_*.json")):
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    bsip1[d["canonical_product_id"]] = d

traces = {}
for p in sorted(TRACES_DIR.glob("*/bsip2_trace.json")):
    with open(p, encoding="utf-8") as f:
        t = json.load(f)
    pid = (t.get("input_reference") or {}).get("canonical_product_id", p.parent.name)
    traces[pid] = t

# ── Helpers ──────────────────────────────────────────────────────────────────

def infer_type(name, ings):
    n = (name or "").lower()
    if "מטבוחה" in n or "סלט טורקי" in n:
        return "matbucha"
    if "חציל" in n or "חצילים" in n:
        return "eggplant_spread"
    if "פלפל" in n:
        return "pepper_spread"
    if "מסבחה" in n:
        return "masabacha"
    if "חומוס" in n:
        return "hummus_spread"
    return "other_spread"

TYPE_LABELS = {
    "hummus_spread":  "חומוס",
    "matbucha":       "מטבוחה",
    "eggplant_spread":"סלט חצילים",
    "pepper_spread":  "ממרח פלפלים",
    "masabacha":      "מסבחה",
    "other_spread":   "ממרח אחר",
}

def resolve_display(pid, trace, b1, flags):
    if pid in insuff_pids:
        return "unavailable", False, ["score_unavailable: no nutrition panel"]
    caveats = []
    if any("STRUCTURAL_EMPTINESS" in f for f in flags):
        caveats.append("structural_emptiness: calorie_density capped; score may understate product quality")
    if any("LOW_NOVA_CONFIDENCE" in f for f in flags):
        caveats.append("low_nova_confidence: processing_quality dimension unreliable — do not surface as highlight")
    if any("CATEGORY_INSTABILITY" in f for f in flags):
        caveats.append("category_routing_imprecise: display as Savory spread, not internal routing code")
    state = "caveated" if caveats else "normal"
    return state, True, caveats

# ── Build products ────────────────────────────────────────────────────────────

all_pids = sorted(bsip1.keys(), key=lambda p: -(full_table.get(p, {}).get("score") or 0))

fat_unreliable = set()
products = []

for pid in all_pids:
    b1    = bsip1.get(pid, {})
    trace = traces.get(pid, {})
    name  = b1.get("canonical_name_he") or ""
    ings  = b1.get("ingredients_list") or []
    bsip0 = b1.get("bsip0_source") or {}
    nn    = b1.get("normalized_nutrition_per_100g") or {}
    enr   = b1.get("enrichment_summary") or {}

    ptype = infer_type(name, ings)
    flags = list(trace.get("unresolved_flags") or [])
    state, displayable, caveats = resolve_display(pid, trace, b1, flags)

    # Score/grade
    if pid in insuff_pids:
        score = None; grade = "insufficient_data"; nova = trace.get("nova_proxy")
        conf = None; cap = None; dims = None
    else:
        row = full_table.get(pid, {})
        score = row.get("score"); grade = row.get("grade")
        nova = row.get("nova"); conf = row.get("confidence"); cap = row.get("binding_cap")
        dims = {
            "processing_quality":   row.get("dim_pq"),
            "nutrient_density":     row.get("dim_nd"),
            "calorie_density":      row.get("dim_cd"),
            "glycemic_quality":     row.get("dim_gq"),
            "protein_quality":      row.get("dim_prq"),
            "additive_quality":     row.get("dim_aq"),
            "satiety_support":      row.get("dim_ss"),
            "fat_quality":          row.get("dim_fq"),
            "regulatory_quality":   row.get("dim_rq"),
            "whole_food_integrity": row.get("dim_wfi"),
        }

    fat_g = nn.get("fat_g")
    fat_ok = (fat_g is not None and fat_g > 1.0)
    if not fat_ok:
        fat_unreliable.add(pid)

    price = bsip0.get("price_ils")
    try:
        price = float(price) if price else None
    except Exception:
        price = None

    products.append({
        "product_id":              pid,
        "barcode":                 b1.get("barcode"),
        "name_he":                 name,
        "brand":                   b1.get("brand"),
        "product_type":            ptype,
        "product_type_label_he":   TYPE_LABELS.get(ptype, ptype),
        "score":                   score,
        "grade":                   grade,
        "displayable":             displayable,
        "display_state":           state,
        "display_caveats":         caveats,
        "image_url":               b1.get("image_url"),
        "source_url":              bsip0.get("source_url"),
        "price_ils":               price,
        "nova":                    nova,
        "confidence_score":        conf,
        "binding_cap":             cap,
        "ingredient_count":        len(ings),
        "additive_count":          enr.get("additive_count", 0),
        "fat_quality_reliable":    fat_ok,
        "category_display":        "savory_spread",
        "dimension_scores":        dims,
        "dimension_note":          (
            "fat_quality unreliable — Shufersal fat-row scraping defect (TASK-039)"
            if not fat_ok and dims else None
        ),
        "unresolved_flags":        flags,
    })

# ── Aggregates ────────────────────────────────────────────────────────────────

scored = [p for p in products if p["score"] is not None]
scores = [p["score"] for p in scored]
grade_dist = {}
type_dist  = {}
for p in products:
    g = str(p["grade"]); grade_dist[g] = grade_dist.get(g, 0) + 1
    t = p["product_type"]; type_dist[t] = type_dist.get(t, 0) + 1

# ── Final JSON ────────────────────────────────────────────────────────────────

out = {
    "schema_version":        "hummus_frontend_v1",
    "generated_at":          GENERATED_AT,
    "source_run_id":         "run_hummus_002",
    "source_task":           "TASK-061",
    "display_rules_source":  "TASK-045 baseline freeze report (TASK-060 file not found — TASK-045 rules applied as authoritative)",
    "frozen_date":           "2026-05-31",

    "category": {
        "id":               "hummus",
        "name_he":          "חומוס וממרחים",
        "name_en":          "Hummus & Savory Spreads",
        "description_he":   "השוואת מוצרי חומוס, מטבוחה, ממרח חצילים וממרחי ירקות — שופרסל, 2026-05-30.",
        "description_en":   "Hummus, matbucha, eggplant spreads, and savory dip comparison. Shufersal, 2026-05-30.",
        "retailer":         "shufersal",
        "bsip2_version":    "proto_v0",
        "router_version":   "router_v2_savory_anchors",
        "total_products":   69,
        "displayable_products": sum(1 for p in products if p["displayable"]),
        "unavailable_products": sum(1 for p in products if not p["displayable"]),
        "grade_distribution": grade_dist,
        "product_type_distribution": type_dist,
        "score_statistics": {
            "count":  len(scores),
            "mean":   round(statistics.mean(scores), 2) if scores else None,
            "median": round(statistics.median(scores), 2) if scores else None,
            "stdev":  round(statistics.stdev(scores), 2) if len(scores) > 1 else None,
            "min":    min(scores) if scores else None,
            "max":    max(scores) if scores else None,
            "p25":    sorted(scores)[len(scores)//4] if scores else None,
            "p75":    sorted(scores)[3*len(scores)//4] if scores else None,
        },
        "nova_distribution": val.get("nova_distribution"),
        "corpus_note": "fat_quality dimension unreliable for 58/69 products — Shufersal fat-row scraping defect (TASK-039)",
    },

    "grade_thresholds": {
        "S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0,
        "note": "From constants.py GRADE_THRESHOLDS"
    },

    "dimension_weights": {
        "processing_quality": 0.15, "nutrient_density": 0.15, "calorie_density": 0.15,
        "glycemic_quality": 0.12, "protein_quality": 0.10, "additive_quality": 0.10,
        "satiety_support": 0.06, "fat_quality": 0.08, "regulatory_quality": 0.05,
        "whole_food_integrity": 0.04,
    },

    "dimension_display_flags": {
        "fat_quality": {
            "display_breakdown": False,
            "reason": "Unreliable for 84% of corpus — Shufersal fat-row scraping defect (TASK-039). Show corpus-level note only."
        }
    },

    "filter_options": {
        "grades": [
            {"value": g, "label_he": f"ציון {g}", "count": grade_dist.get(g, 0)}
            for g in ["A", "B", "C", "D"]
        ],
        "product_types": [
            {"value": k, "label_he": TYPE_LABELS.get(k, k), "count": v}
            for k, v in sorted(type_dist.items(), key=lambda x: -x[1])
        ],
        "nova_levels": [
            {"value": n, "label": f"NOVA {n}", "count": sum(1 for p in products if p["nova"] == n)}
            for n in [1, 2, 3]
        ],
    },

    "known_limitations": [
        {
            "id": "KL-1", "severity": "medium",
            "title": "fat_quality dimension unreliable — 84% of products",
            "detail": (
                "The Shufersal scraper captured saturated fat instead of total fat for 58/69 products (TASK-039). "
                "fat_quality scores are neutral (50) for affected products, not genuine quality signals. "
                "Score impact: approximately -1 to -2 points vs. corrected data. Grade distributions are not materially affected."
            ),
            "products_affected": len(fat_unreliable),
            "blocks_display": False,
            "ui_action": "Do not display fat_quality dimension breakdown. Add corpus-level caveat where fat_quality appears.",
        },
        {
            "id": "KL-2", "severity": "high",
            "title": "2 products — score unavailable (no nutrition data)",
            "detail": (
                "bsip1_7296073733317 (חומוס) and bsip1_7296073733348 (חומוס ענק) have no scraped nutrition panel. "
                "displayable=false for both. Grade = insufficient_data."
            ),
            "products_affected": 2,
            "blocks_display": True,
            "ui_action": "Show 'score unavailable' UI state. Do not display grade or score.",
        },
        {
            "id": "KL-3", "severity": "low",
            "title": "2 products — imprecise category routing (default)",
            "detail": (
                "סלט טורקי and סלט פלפלים קלויים route to 'default'. Scores are valid. "
                "Display category as 'Savory spread' not the internal routing code."
            ),
            "products_affected": 2,
            "blocks_display": False,
            "ui_action": "Override category label to 'Savory spread' for these products.",
        },
        {
            "id": "KL-4", "severity": "low",
            "title": "2 matbucha products — structural emptiness gate suppresses scores",
            "detail": (
                "מטבוחה אמיתית and מטבוחה חריפה scored D due to structural emptiness gate (SRC-04). "
                "Their calorie_density is capped at 50 rather than ~90 expected for low-kcal vegetable spreads. "
                "Grades are mechanically correct but counterintuitive."
            ),
            "products_affected": 2,
            "blocks_display": False,
            "ui_action": "Display with caveated display_state. Add product-level note about incomplete data.",
        },
        {
            "id": "KL-5", "severity": "low",
            "title": "2 products — NOVA confidence too low to surface processing_quality",
            "detail": (
                "bsip1_1990261 and bsip1_3643714 have NOVA confidence=0.2 (no ingredient data). "
                "processing_quality dimension score is unreliable."
            ),
            "products_affected": 2,
            "blocks_display": False,
            "ui_action": "Suppress processing_quality as a highlight dimension for these 2 products.",
        },
    ],

    "qa_notes": {
        "run_validity":    "run_hummus_002 is the AUTHORITATIVE baseline (TASK-045 frozen). run_hummus_001 is INVALID — do not use.",
        "routing_fix":     "64/69 products were rerouted from dessert/whole_food_fat/default to sauce_spread in TASK-044.",
        "fat_anomaly":     "Shufersal fat-row defect confirmed (TASK-039). 58/69 products have corrupt fat_g values. fix in BSIP0 scraper before run_hummus_003.",
        "grade_boundaries":"Grade thresholds from constants.py: S≥90, A≥80, B≥65, C≥50, D≥35, E≥0.",
        "task_060_note":   "TASK-060 (Product Agent decision) output file not found. Display rules applied from TASK-045 baseline freeze report Section 10.",
        "next_action":     "Fix Shufersal fat scraper (TASK-039 root cause) and re-run as run_hummus_003 for corrected fat_quality scores.",
    },

    "bsip_metadata": {
        "bsip0_scrape_date":   "2026-05-30",
        "bsip0_retailer":      "shufersal",
        "bsip1_task":          "TASK-034",
        "bsip2_run_id":        "run_hummus_002",
        "bsip2_frozen":        True,
        "bsip2_frozen_task":   "TASK-045",
        "routing_fix_task":    "TASK-044",
        "fat_anomaly_task":    "TASK-039",
        "invalid_run":         "run_hummus_001",
    },

    "products": products,
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

size_kb = OUT_JSON.stat().st_size / 1024
print(f"Written: {OUT_JSON}")
print(f"Size: {size_kb:.1f} KB")
print(f"Products: {len(products)} total, {sum(1 for p in products if p['displayable'])} displayable")
print(f"Grade dist: {grade_dist}")
print(f"Type dist: {type_dist}")
print(f"Fat unreliable: {len(fat_unreliable)}")
