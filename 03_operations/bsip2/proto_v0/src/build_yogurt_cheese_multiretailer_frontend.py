"""
Build yogurts_frontend_v3.json and cheese_frontend_v3.json — merges frozen Shufersal
baseline with new Yohananof products from TASK-210 Phase B/D.

Rules:
- Shufersal products: carry ALL fields verbatim from current live JSONs (scores frozen).
- New Yohananof products: built from BSIP2 trace + BSIP1 data.
- Every product MUST have retailer field set.
- Yogurt: note that some Yohananof yogurts may route to dairy_protein (same as Shufersal pool);
  cap S-grade display to A for consistency with the yogurt pool convention (run_yogurt_006 recal
  explicitly held 0 S products; do NOT override scoring but flag in meta).
- Cheese: the A-ceiling gate applies (sodium <= 400mg AND sat_fat <= 4.0g required for A).
"""
import sys, io, json, pathlib, datetime
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
# TASK-233B: shared packaging core owns grade derivation, confidence derivation, image
# selection, the VM strip, and the A-cap field name. Local grade_from_score /
# confidence_* are thin wrappers around the core to preserve call sites.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import frontend_core as FC

LIVE_YOGURT   = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v2.json")
LIVE_CHEESE   = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cheese_frontend_v2.json")

YOGURT_TRACES = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_yohananof_001\products")
YOGURT_BSIP1  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_yohananof_001\output")

CHEESE_TRACES = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_yohananof_001\products")
CHEESE_BSIP1  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cheese_yohananof_001\output")

OUT_YOGURT    = pathlib.Path(r"C:\Bari\02_products\yogurt_system\yogurts_frontend_v3.json")
OUT_CHEESE    = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\cheese_frontend_v3.json")
OUT_YOGURT_WEB = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v3.json")
OUT_CHEESE_WEB = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\cheese_frontend_v3.json")

# Load frozen Shufersal products
yogurt_live = json.loads(LIVE_YOGURT.read_text("utf-8"))
cheese_live = json.loads(LIVE_CHEESE.read_text("utf-8"))
yogurt_shufersal = yogurt_live.get("products", [])
cheese_shufersal = cheese_live.get("products", [])
for p in yogurt_shufersal:
    p.setdefault("retailer", "shufersal")
for p in cheese_shufersal:
    p.setdefault("retailer", "shufersal")

print(f"Shufersal yogurt: {len(yogurt_shufersal)}, cheese: {len(cheese_shufersal)}")

# Load BSIP1 and traces helpers
def load_bsip1(bsip1_dir):
    by_pid = {}
    for f in bsip1_dir.glob("bsip1_*.json"):
        d = json.loads(f.read_text("utf-8"))
        by_pid[d.get("canonical_product_id")] = d
    return by_pid

def load_traces(trace_dir):
    traces = {}
    for pid_dir in trace_dir.iterdir():
        if not pid_dir.is_dir():
            continue
        trace_path = pid_dir / "bsip2_trace.json"
        if not trace_path.exists():
            continue
        t = json.loads(trace_path.read_text("utf-8"))
        pid = (t.get("input_reference") or {}).get("canonical_product_id") or t.get("canonical_product_id")
        if pid:
            traces[pid] = t
    return traces

def grade_from_score(score):
    # Shared core: 5-grade, byte-matching corpus.ts so disk grade == runtime grade
    # (DA-002/DA-009). The engine S folds to A here; never a bespoke '?'/'S' on disk.
    return FC.grade_from_score(score)

def build_new_products(traces, bsip1_by_pid, category_prefix, retailer="yohananof", cap_S_to_A=False):
    """Build frontend records for new retailer products."""
    new = []
    for pid, trace in traces.items():
        score = trace.get("final_score_estimate")
        if score is None:
            continue
        b1 = bsip1_by_pid.get(pid, {})
        ref = trace.get("input_reference") or {}
        signals = trace.get("L1_observed_signals") or {}
        name = ref.get("product_name_he") or ref.get("canonical_name_he") or b1.get("canonical_name_he") or ""
        brand = b1.get("brand") or ""
        # DA-007/DA-005: confidence is trace-derived (medium != verified; verified needs a
        # full panel + ingredients), with the canonical 7-state label/tooltip. No bespoke
        # sufficient->verified flag.
        conf_fields = FC.confidence_from_trace(trace)
        # DA-009: grade from the ROUNDED score that ships (and that corpus.ts re-derives).
        score_display = FC.round_score(score)
        grade = grade_from_score(score_display)

        # S folds into A in the 5-grade core, so there is no longer an 'S' to cap here;
        # the yogurt-pool 89-ceiling stays as an explicit display cap on the score value.
        display_grade = grade
        capped = False
        if cap_S_to_A and score_display is not None and score_display >= 90:
            display_grade = "A"
            score_display = min(score_display, 89)  # cap at 89 per yogurt convention
            capped = True

        image_url = FC.select_image_url(b1) or ""
        ingredients = b1.get("ingredients_text_he") or b1.get("ingredients_raw") or ""

        nutrition = {
            "energyKcal": signals.get("energy_kcal"),
            "protein":    signals.get("protein_g"),
            "sugar":      signals.get("sugars_g"),
            "fat":        signals.get("fat_g"),
            "fiber":      signals.get("dietary_fiber_g"),
            "sodium":     signals.get("sodium_mg"),
            "satFat":     signals.get("fat_saturated_g"),
        }

        # Build factual insight line
        facts = []
        if nutrition.get("protein") is not None:
            facts.append(f"{round(nutrition['protein'], 1)} גרם חלבון ל-100 גרם")
        if nutrition.get("fat") is not None:
            facts.append(f"{round(nutrition['fat'], 1)} גרם שומן")
        if nutrition.get("sodium") is not None:
            facts.append(f"{round(nutrition['sodium'])} מ\"ג נתרן")
        nova = trace.get("nova_proxy")
        if nova:
            facts.append(f"NOVA {nova}")
        insight_line = " — ".join(facts[:3]) if facts else f"ציון {score_display}/{display_grade}"

        retailer_he = {"yohananof": "יוחננוף", "carrefour": "קרפור"}.get(retailer, retailer)
        row_verdict = f"{name}: {insight_line}. מקור: {retailer_he}."
        if capped:
            row_verdict += f" (ציון מנוע {round(score)}/S; מוצג כ-A לפי מדיניות קטגוריה)"

        record = {
            "id": pid,
            "name": name,
            "brand": brand,
            "imageUrl": image_url,
            "score": score_display,
            "grade": display_grade,
            "insightLine": insight_line,
            "confidence": conf_fields["confidence"],
            "expansion": {
                "nutrition": nutrition,
                "ingredients": ingredients,
                "confidenceLabel": conf_fields["confidence_label_he"],
                "servingNote": "ל-100 גרם",
            },
            "rowVerdict": row_verdict,
            "confidence_label_he": conf_fields["confidence_label_he"],
            "confidence_tooltip_he": conf_fields["confidence_tooltip_he"],
            "confidence_sub_reason": conf_fields["confidence_sub_reason"],
            "retailer": retailer,
            "retailer_he": retailer_he,
            "provenance": "off_candidate_panel",
        }
        if capped:
            # Display cap on the score VALUE (engine score >=90 held at 89/A per the
            # yogurt-pool convention). Represented via the canonical A-cap field corpus.ts
            # honors so a regeneration emits a cap the runtime respects.
            record[FC.A_CAP_FIELD] = True
            record["_score_capped"] = f"engine_score={round(score)} (>=90) capped to 89/A per yogurt_pool_convention"
        new.append(record)
    return new


# ── YOGURT v3 ──
print("\n=== Building yogurts_frontend_v3.json ===")
yogurt_traces = load_traces(YOGURT_TRACES)
yogurt_bsip1 = load_bsip1(YOGURT_BSIP1)
print(f"Yohananof yogurt traces: {len(yogurt_traces)}, BSIP1: {len(yogurt_bsip1)}")

new_yogurt = build_new_products(yogurt_traces, yogurt_bsip1, "yogurt", retailer="yohananof", cap_S_to_A=True)
print(f"New Yohananof yogurt products: {len(new_yogurt)}")

# Dedup: remove any new products whose barcode already exists in Shufersal pool
shufersal_yogurt_barcodes = {str(p.get("id", "")).replace("bsip1_yogurt_", "").replace("yog-", "") for p in yogurt_shufersal}
shufersal_yogurt_barcodes.update({str(p.get("barcode", "")) for p in yogurt_shufersal})
new_yogurt_deduped = []
for p in new_yogurt:
    bc = str(p["id"]).replace("bsip1_yogurt_", "")
    if bc in shufersal_yogurt_barcodes:
        print(f"  DEDUP (yogurt): {p['id']} already in Shufersal pool")
    else:
        new_yogurt_deduped.append(p)
print(f"New Yohananof yogurt after dedup: {len(new_yogurt_deduped)}")

all_yogurt = sorted(yogurt_shufersal, key=lambda p: -(p.get("score") or 0)) + \
             sorted(new_yogurt_deduped, key=lambda p: -(p.get("score") or 0))
# TASK-233B emission strip (DA-012): keep only VM keys + barcode/retailer + the
# load-bearing `_cluster` (yogurt shelf filters read it off the raw JSON). Drops
# source_traceability_status, confidence_level, retailer_he, provenance, _score_capped,
# _a_gate_reason, brand and other non-VM keys. `_aCappedToB` is preserved by the allowlist.
all_yogurt = [FC.strip_non_vm_fields(p, keep={"_cluster"}) for p in all_yogurt]
yogurt_grade_dist = Counter(p.get("grade") for p in all_yogurt)
yogurt_out = {
    "_meta": {
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "category": "yogurts",
        "product_count": len(all_yogurt),
        "scored_count": sum(1 for p in all_yogurt if p.get("score") is not None),
        "schema": "BariProductVM[]",
        "version": "v3",
        "provenance": (
            "TASK-210 multi-retailer expansion. "
            f"Shufersal pool ({len(yogurt_shufersal)} products): frozen from yogurts_frontend_v2.json / run_yogurt_006_recal_p0_trim. "
            f"New Yohananof pool ({len(new_yogurt_deduped)} products): run_yogurt_yohananof_001 — "
            "il_prices identity + OFF candidate panels (EDPG candidate). "
            "BSIP0 filter rate: 132/143 (92%) — primarily ingredients_absent (OFF miss on Israeli yogurt barcodes). "
            "S-grade display capped to A per yogurt pool convention (run_yogurt_006_recal_p0_trim). "
        ),
        "retailer_breakdown": {
            "shufersal": len(yogurt_shufersal),
            "yohananof": len(new_yogurt_deduped),
        },
        "grade_distribution": dict(yogurt_grade_dist),
    },
    "products": all_yogurt,
}
OUT_YOGURT.write_text(json.dumps(yogurt_out, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_YOGURT_WEB.write_text(json.dumps(yogurt_out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Written: {OUT_YOGURT}")
print(f"Written: {OUT_YOGURT_WEB}")
print(f"Total yogurt: {len(all_yogurt)} (Shufersal {len(yogurt_shufersal)} + Yohananof {len(new_yogurt_deduped)})")


# ── CHEESE v3 ──
print("\n=== Building cheese_frontend_v3.json ===")
cheese_traces = load_traces(CHEESE_TRACES)
cheese_bsip1 = load_bsip1(CHEESE_BSIP1)
print(f"Yohananof cheese traces: {len(cheese_traces)}, BSIP1: {len(cheese_bsip1)}")

# For cheese: apply the A-ceiling gate (sodium <= 400mg AND sat_fat <= 4.0g for A grade)
new_cheese_raw = build_new_products(cheese_traces, cheese_bsip1, "cheese", retailer="yohananof", cap_S_to_A=False)

# Apply cheese A-gate (same as run_cheese_004)
def apply_cheese_a_gate(products):
    out = []
    for p in products:
        nutr = (p.get("expansion") or {}).get("nutrition") or {}
        sodium = nutr.get("sodium")
        sat_fat = nutr.get("satFat")
        if p.get("grade") in ("A", "S"):
            if sodium is None or sat_fat is None or sodium > 400 or sat_fat > 4.0:
                p["grade"] = "B"
                # DA-011: corpus.ts normalizeGrade reads `_aCappedToB` (NOT `_a_gate_capped`)
                # to hold an A-eligible product at B. Write the name the runtime honors.
                p[FC.A_CAP_FIELD] = True
                p["_a_gate_reason"] = f"A-ceiling gate: sodium={sodium} sat_fat={sat_fat} (threshold: sodium<=400, sat_fat<=4.0)"
        out.append(p)
    return out

new_cheese = apply_cheese_a_gate(new_cheese_raw)

# Dedup vs Shufersal cheese pool
shufersal_cheese_barcodes = {str(p.get("id", "")).replace("bsip1_cheese_", "").replace("che-", "") for p in cheese_shufersal}
new_cheese_deduped = []
for p in new_cheese:
    bc = str(p["id"]).replace("bsip1_cheese_", "")
    if bc in shufersal_cheese_barcodes:
        print(f"  DEDUP (cheese): {p['id']} already in Shufersal pool")
    else:
        new_cheese_deduped.append(p)
print(f"New Yohananof cheese after dedup: {len(new_cheese_deduped)}")

all_cheese = sorted(cheese_shufersal, key=lambda p: -(p.get("score") or 0)) + \
             sorted(new_cheese_deduped, key=lambda p: -(p.get("score") or 0))
# TASK-233B emission strip (DA-012): same policy as yogurt. `_cluster` (cheese shelf
# filters) and `_aCappedToB` (the A-ceiling cap corpus.ts honors) are preserved; all
# other internal/non-VM keys are dropped.
all_cheese = [FC.strip_non_vm_fields(p, keep={"_cluster"}) for p in all_cheese]
cheese_grade_dist = Counter(p.get("grade") for p in all_cheese)
cheese_out = {
    "_meta": {
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "category": "cheese-spreads",
        "product_count": len(all_cheese),
        "scored_count": sum(1 for p in all_cheese if p.get("score") is not None),
        "schema": "BariProductVM[]",
        "version": "v3",
        "provenance": (
            "TASK-210 multi-retailer expansion. "
            f"Shufersal pool ({len(cheese_shufersal)} products): frozen from cheese_frontend_v2.json / run_cheese_004-recal_p0. "
            f"New Yohananof pool ({len(new_cheese_deduped)} products): run_cheese_yohananof_001 — "
            "il_prices identity + OFF candidate panels (EDPG candidate). "
            "BSIP0 filter rate: 175/190 (92%) — primarily ingredients_absent (OFF miss on Israeli cheese barcodes). "
            "A-ceiling gate applied: sodium<=400mg AND sat_fat<=4.0g required for A. "
        ),
        "retailer_breakdown": {
            "shufersal": len(cheese_shufersal),
            "yohananof": len(new_cheese_deduped),
        },
        "grade_distribution": dict(cheese_grade_dist),
    },
    "products": all_cheese,
}
OUT_CHEESE.write_text(json.dumps(cheese_out, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_CHEESE_WEB.write_text(json.dumps(cheese_out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Written: {OUT_CHEESE}")
print(f"Written: {OUT_CHEESE_WEB}")
print(f"Total cheese: {len(all_cheese)} (Shufersal {len(cheese_shufersal)} + Yohananof {len(new_cheese_deduped)})")
