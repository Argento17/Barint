"""
Build cereals_frontend_v2.json — merges frozen run_cereals_008 (Shufersal, 37 products)
with run_cereals_multiretailer_001 (Carrefour + Yohananof, 35 scored new products).
TASK-210 Phase D.

Rules:
- Shufersal products: carry ALL fields verbatim from cereals_frontend_v1.json (scores frozen).
- New retailer products: build from BSIP2 trace + BSIP1 data (no authored copy; use trace data).
- Every product MUST have retailer field set.
- New products with data_sufficiency=insufficient or final_score_estimate=None are excluded.
- Products misrouted (not cereal/snack_bar_granola) are excluded from the standard cereal pool.
"""
import sys, io, json, pathlib, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

LIVE_V1       = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cereals_frontend_v1.json")
MULTIRETAILER_TRACES = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_multiretailer_001\products")
MULTIRETAILER_BSIP1  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\output")
DEDUP_REPORT  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\dedup_report.json")
OUT_PATH      = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\cereals_frontend_v2.json")
OUT_WEB_PATH  = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cereals_frontend_v2.json")

CEREAL_CATEGORIES = {"cereal", "breakfast_cereals", "cereal_system", "snack_bar_granola"}

# --- Load frozen Shufersal v1 products ---
live_v1 = json.loads(LIVE_V1.read_text("utf-8"))
shufersal_products = live_v1.get("products", [])
# Ensure retailer field is set on all Shufersal products
for p in shufersal_products:
    p.setdefault("retailer", "shufersal")

print(f"Shufersal frozen products: {len(shufersal_products)}")

# --- Load dedup report to know which barcodes are truly new ---
dedup = json.loads(DEDUP_REPORT.read_text("utf-8"))
new_barcodes = {str(r["barcode"]) for r in dedup.get("new_products", [])}
print(f"New barcodes from dedup: {len(new_barcodes)}")

# --- Load BSIP1 data for new products (for ingredients, governance) ---
bsip1_by_pid: dict[str, dict] = {}
for f in MULTIRETAILER_BSIP1.glob("bsip1_*.json"):
    d = json.loads(f.read_text("utf-8"))
    pid = d.get("canonical_product_id")
    bc = str(d.get("barcode", ""))
    if bc in new_barcodes:
        bsip1_by_pid[pid] = d

print(f"BSIP1 records for new products: {len(bsip1_by_pid)}")

# --- Load BSIP2 traces for new products ---
def load_traces(trace_dir):
    traces = {}
    for pid_dir in trace_dir.iterdir():
        trace_path = pid_dir / "bsip2_trace.json"
        if not trace_path.exists():
            continue
        t = json.loads(trace_path.read_text("utf-8"))
        pid = t.get("canonical_product_id") or (t.get("input_reference") or {}).get("canonical_product_id")
        if pid:
            traces[pid] = t
    return traces

traces = load_traces(MULTIRETAILER_TRACES)
print(f"Multiretailer BSIP2 traces: {len(traces)}")

# --- Confidence label mapping ---
def confidence_label(lvl: str | None) -> str:
    if lvl == "sufficient":
        return "נתונים מלאים"
    if lvl == "partial":
        return "נתונים חלקיים"
    return "נתונים חלקיים"

def confidence_badge(lvl: str | None) -> str:
    if lvl == "sufficient":
        return "verified"
    return "partial"

def grade_from_score(score) -> str:
    if score is None:
        return "?"
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"

def retailer_from_bsip1(b1: dict) -> str:
    retailers = b1.get("source_retailers") or []
    return retailers[0] if retailers else "unknown"

# --- Build new retailer product records ---
new_products = []
skipped_reason = {}

for pid, trace in traces.items():
    # Only include genuinely new barcodes (not in Shufersal baseline)
    ref = trace.get("input_reference") or {}
    bc = str(ref.get("barcode") or "")
    if bc and bc not in new_barcodes:
        skipped_reason[pid] = "duplicate_in_shufersal_baseline"
        continue

    # Exclude misrouted products
    category = trace.get("category")
    if category not in CEREAL_CATEGORIES:
        skipped_reason[pid] = f"misrouted_to_{category}"
        continue

    # Exclude insufficient data
    suf = trace.get("data_sufficiency")
    score = trace.get("final_score_estimate")
    if suf == "insufficient" or score is None:
        skipped_reason[pid] = "insufficient_data"
        continue

    b1 = bsip1_by_pid.get(pid, {})
    signals = trace.get("L1_observed_signals") or {}
    gov = b1.get("cereals_governance") or {}
    subpool_info = (gov.get("construct_1_granola_subpool") or {})
    subpool = subpool_info.get("subpool", "standard_cereal")
    is_childrens = bool((gov.get("construct_2_childrens") or {}).get("flag"))
    whole_grain = bool((gov.get("construct_3_whole_grain") or {}).get("flag"))

    name = ref.get("product_name_he") or ref.get("canonical_name_he") or b1.get("canonical_name_he") or ""
    brand = b1.get("brand") or ""
    confidence_lvl = trace.get("confidence") or b1.get("confidence") or "partial"
    grade = grade_from_score(score)

    # Image: prefer OFF image from bsip1
    img_urls = b1.get("image_urls") or []
    image_url = img_urls[0] if img_urls else ""

    # Nutrition from trace signals
    nutrition = {
        "energyKcal": signals.get("energy_kcal"),
        "protein":    signals.get("protein_g"),
        "sugar":      signals.get("sugars_g"),
        "fat":        signals.get("fat_g"),
        "fiber":      signals.get("dietary_fiber_g"),
        "sodium":     signals.get("sodium_mg"),
    }

    ingredients = b1.get("ingredients_text_he") or b1.get("ingredients_raw") or ""
    retailer = retailer_from_bsip1(b1)

    # Build insight line from score drivers
    score_components = trace.get("score_components") or {}
    nova = trace.get("nova_proxy")
    energy = nutrition.get("energyKcal")
    protein = nutrition.get("protein")
    fiber = nutrition.get("fiber")
    sugar = nutrition.get("sugar")
    sodium_mg = nutrition.get("sodium")

    # Generate a minimal factual insight line
    facts = []
    if sugar is not None:
        facts.append(f"{round(sugar, 1)} גרם סוכר ל-100 גרם")
    if fiber is not None and fiber > 3:
        facts.append(f"{round(fiber, 1)} גרם סיבים")
    if protein is not None and protein > 8:
        facts.append(f"{round(protein, 1)} גרם חלבון")
    if nova is not None:
        facts.append(f"NOVA {nova}")
    insight_line = " — ".join(facts[:3]) if facts else f"ציון {round(score, 0):.0f}/{grade}"

    # Build row verdict from score range context
    row_verdict = f"{name}: {insight_line}. מקור: {retailer}."

    # Retailer display name
    retailer_display = {
        "carrefour": "קרפור",
        "yohananof": "יוחננוף",
        "shufersal": "שופרסל",
    }.get(retailer, retailer)

    record = {
        "id": pid,
        "name": name,
        "brand": brand,
        "imageUrl": image_url,
        "score": round(score),
        "grade": grade,
        "insightLine": insight_line,
        "confidence": confidence_badge(confidence_lvl),
        "expansion": {
            "nutrition": nutrition,
            "ingredients": ingredients,
            "confidenceLabel": confidence_label(confidence_lvl),
            "servingNote": "ל-100 גרם",
        },
        "rowVerdict": row_verdict,
        "_subpool": subpool,
        "_isChildrens": is_childrens,
        "_wholeGrainClaim": whole_grain,
        "confidence_level": confidence_lvl,
        "retailer": retailer,
        "retailer_he": retailer_display,
        "provenance": "off_candidate_panel",
    }
    new_products.append(record)

print(f"New retailer products included: {len(new_products)}")
print(f"Skipped: {skipped_reason}")

# --- Retailer breakdown ---
from collections import Counter
retailer_counts = Counter(p["retailer"] for p in new_products)
print(f"New products by retailer: {dict(retailer_counts)}")

# --- Combine: Shufersal + new retailer products ---
# Shufersal products go first (by score desc), then new
shufersal_sorted = sorted(shufersal_products, key=lambda p: -(p.get("score") or 0))
new_sorted = sorted(new_products, key=lambda p: -(p.get("score") or 0))
all_products = shufersal_sorted + new_sorted

# Grade distribution
grade_dist = Counter(p.get("grade") for p in all_products)
scored_count = sum(1 for p in all_products if p.get("score") is not None)

output = {
    "_meta": {
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "category": "breakfast-cereals",
        "product_count": len(all_products),
        "scored_count": scored_count,
        "schema": "BariProductVM[]",
        "version": "v2",
        "provenance": (
            "TASK-210 multi-retailer expansion. "
            "Shufersal pool (37 products): frozen from cereals_frontend_v1.json / run_cereals_008. "
            f"New retailer pool ({len(new_products)} products): run_cereals_multiretailer_001 — "
            f"Carrefour ({retailer_counts.get('carrefour', 0)}) + "
            f"Yohananof ({retailer_counts.get('yohananof', 0)}). "
            "Source: Israeli price-transparency feeds (il_prices) + OFF candidate panels (EDPG). "
            "BSIP0 filters applied (F1-F4). Deduped vs Shufersal baseline: 16 cross-retailer overlaps removed. "
            f"Score range: {min(p['score'] for p in new_products) if new_products else 'N/A'}–"
            f"{max(p['score'] for p in new_products) if new_products else 'N/A'}. "
            f"Grade dist (new): {dict(Counter(p['grade'] for p in new_products))}."
        ),
        "retailer_breakdown": {
            "shufersal": len(shufersal_products),
            **dict(retailer_counts),
        },
        "dedup_notes": {
            "cross_retailer_overlaps_removed": 16,
            "cross_retailer_duplicates_carrefour_yohananof": 2,
            "baseline": "run_cereals_005 / run_cereals_008 (66 Shufersal barcodes)",
        },
    },
    "products": all_products,
}

OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_WEB_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Written: {OUT_PATH}")
print(f"Written: {OUT_WEB_PATH}")
print(f"Total products: {len(all_products)} (Shufersal: {len(shufersal_products)}, New: {len(new_products)})")
print(f"Grade distribution (all): {dict(grade_dist)}")
