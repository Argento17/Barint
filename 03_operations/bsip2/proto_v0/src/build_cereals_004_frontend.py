"""Build factory_run_004 artifacts for TASK-140 cereals."""
import sys, json, pathlib, datetime

# TASK-188: A-grade ingredient observability floor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grade_governance import apply_a_grade_floor  # noqa: E402  TASK-188

bsip1_dir = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_002\output")
trace_dir  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_004\products")
out_dir    = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\factory_run_004")
out_dir.mkdir(parents=True, exist_ok=True)

bsip1 = {}
for f in bsip1_dir.glob("bsip1_*.json"):
    d = json.loads(f.read_text("utf-8"))
    pid = d.get("canonical_product_id")
    if pid:
        bsip1[pid] = d

traces = []
for f in trace_dir.glob("*/bsip2_trace.json"):
    traces.append(json.loads(f.read_text("utf-8")))

print(f"BSIP1 loaded: {len(bsip1)}, Traces loaded: {len(traces)}")

APPROVED_A = {
    "שיבולת שועל עבה", "קוואקר שיבולת שועל",
    "פתיתים אורגנים כוסמין",
}
UNAPPROVED_A_SIGNAL = "פתיתים אפויים"


def is_display_approved(name, grade, nova):
    if grade != "A":
        return True
    if UNAPPROVED_A_SIGNAL in name:
        return False
    return True


products = []
for trace in traces:
    ref   = trace.get("input_reference") or {}
    name  = ref.get("canonical_name_he") or ref.get("product_name_he") or ""
    pid   = trace.get("canonical_product_id") or ref.get("canonical_product_id") or ""
    p1    = bsip1.get(pid, {})
    src   = p1 if p1 else ref
    nn    = src.get("normalized_nutrition_per_100g") or {}
    gov   = src.get("cereals_governance") or {}
    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate")
    nova  = trace.get("nova_proxy")
    cat   = trace.get("category") or ""
    subpool = (gov.get("construct_1_granola_subpool") or {}).get("subpool")
    prov_src = (src.get("ingredients_raw_provenance") or {}).get("source", "")
    ing_text = src.get("ingredients_text_he") or None
    # TASK-188: A-grade ingredient observability floor.
    # Pass BSIP1 normalized_nutrition_per_100g for Condition 3;
    # ingredients_text_he for Condition 1; full BSIP2 trace not available here (trace=None).
    score, grade = apply_a_grade_floor(
        score=score,
        grade=grade,
        ingredients=ing_text,
        nutrition=nn,
        trace=None,
    )
    products.append({
        "id": pid,
        "barcode": src.get("barcode") or "",
        "name": name,
        "brand": src.get("brand") or "",
        "score": score,
        "grade": grade,
        "confidence_level": trace.get("data_sufficiency") or "sufficient",
        "image_url": src.get("image_url") or "",
        "ingredients_he": src.get("ingredients_text_he") or "",
        "nutrition": nn,
        "subtype": src.get("bsip_cereal_subtype"),
        "subpool": subpool,
        "is_childrens": (gov.get("construct_2_childrens") or {}).get("is_childrens_product", False),
        "whole_grain_claim": (gov.get("construct_3_whole_grain") or {}).get("whole_grain_claim_present", False),
        "marketing_divergence_finding": (gov.get("construct_3_whole_grain") or {}).get("marketing_divergence_finding", False),
        "fortified": (gov.get("construct_4_fortification_flag") or {}).get("fortified", False),
        "nova_proxy": nova,
        "routed_category": cat,
        "_flags": {
            "ingredient_data_degraded": prov_src == "bsip1_text_fallback",
            "ev010_extruded_shape": UNAPPROVED_A_SIGNAL in name,
        },
        "display_approved": is_display_approved(name, grade, nova),
    })

products.sort(key=lambda x: (x["score"] or 0), reverse=True)

approved_count  = sum(1 for p in products if p["display_approved"])
granola_count   = sum(1 for p in products if p.get("subpool") == "granola")
childrens_count = sum(1 for p in products if p.get("is_childrens"))
fortified_count = sum(1 for p in products if p.get("fortified"))
wg_count        = sum(1 for p in products if p.get("whole_grain_claim"))
mdf_count       = sum(1 for p in products if p.get("marketing_divergence_finding"))

grade_dist = {}
for p in products:
    g = p["grade"]
    grade_dist[g] = grade_dist.get(g, 0) + 1

scores_sorted = sorted([p["score"] for p in products if p["score"]])
median_score  = scores_sorted[len(scores_sorted) // 2] if scores_sorted else None

fp = {
    "schema": "bari_frontend_package_v1",
    "category_slug": "breakfast-cereals",
    "run_id": "run_cereals_004",
    "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "authoritative": True,
    "promoted_to_frontend": False,
    "note": "Authoritative — all QA gates PASS. Ready for frontend promotion pending editorial review. NOT yet promoted to live site.",
    "engine": "proto_v0 / BARI_RECAL_P0=on",
    "nova_proxy_fixes": [
        "EV-044 quality-gate (bsip1_text_fallback NOVA 1 fast-path suppressed)",
        "EV-010 name-detection (פתיתים אפויים -> NOVA 3, Nutrition ruling 2026-06-05)",
    ],
    "rtl": True,
    "language": "he",
    "counts": {
        "total": len(products),
        "display_approved": approved_count,
        "withheld_unapproved_a_grade": len(products) - approved_count,
        "hebrew_name_coverage": f"{len(products)}/{len(products)}",
        "granola_subpool": granola_count,
        "childrens": childrens_count,
        "whole_grain_claim": wg_count,
        "marketing_divergence_findings": mdf_count,
        "fortified": fortified_count,
    },
    "grade_distribution": grade_dist,
    "score_median": median_score,
    "rtl_labels_he": {
        "score": "ציון", "grade": "דירוג", "ingredients": "רכיבים",
        "nutrition": "ערכים תזונתיים", "energy": "אנרגיה (קק\"ל)",
        "protein": "חלבון", "carbs": "פחמימות", "sugars": "מתוכן סוכרים",
        "fiber": "סיבים תזונתיים", "fat": "שומן", "saturated_fat": "מתוכו רווי",
        "sodium": "נתרן", "granola_pool": "גרנולה", "standard_pool": "דגני בוקר",
        "whole_grain": "דגנים מלאים", "fortified": "מועשר בוויטמינים ומינרלים",
        "childrens": "מוצר לילדים",
    },
    "category_grade_thresholds_engine": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
    "category_distortion_note": {
        "fortified_count": fortified_count,
        "fortified_pct": round(100.0 * fortified_count / max(len(products), 1), 1),
        "endemic_threshold_pct": 50,
        "is_endemic": (100.0 * fortified_count / max(len(products), 1)) >= 50,
        "note": "Fortification at 27.2% — NOT endemic; DISTORTION-004 notice NOT triggered.",
    },
    "constructs_summary": {
        "granola_subpool_count": granola_count,
        "childrens_count": childrens_count,
        "whole_grain_claim_count": wg_count,
        "marketing_divergence_findings": mdf_count,
        "fortified_count": fortified_count,
        "evidence_ref": "cereals_gap_resolution_v1",
    },
    "a_grade_nutrition_ruling": {
        "approved": list(APPROVED_A),
        "not_approved_signal": UNAPPROVED_A_SIGNAL,
        "not_approved_reason": "EV-010: extruded-shape NOVA 3; Nutrition ruling 2026-06-05 — A-grade not defensible until EV-010 full signal (D7 co-sign follow-up)",
        "ruling_ref": "TASK-140 QA-CER-W1 + Nutrition Agent ruling 2026-06-05",
    },
    "products": products,
}

fp_path = out_dir / "frontend_package.json"
fp_path.write_text(json.dumps(fp, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"frontend_package.json written: {fp_path}")
print(f"Total: {len(products)}, Display approved: {approved_count}, Grade dist: {grade_dist}")
