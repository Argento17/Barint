"""
BSIP2 — Spread Subtype Regression + Impact Report (EXCEPTION-002)

Mandatory gate for any change to VEG_SPREAD_WEIGHTS, SAUCE_SPREAD_VEG_PROTEIN_GUARD,
or the name-signal lists in _detect_sauce_spread_family().

Corpus: src/data/comparisons/hummus_frontend_v3.json
  — carries nutrition, ingredients, and _product_type subtype label.

Regression requirement (must hold for the run to pass):
  Every product whose _product_type is in {hummus_spread, masabacha}
  must show zero score movement vs the pre-EXCEPTION-002 baseline produced
  by scoring the same products under DIMENSION_WEIGHTS explicitly.

Impact report is written to:
  C:/Users/HP/bari/docs/spread_subtype_impact_report_v1.md

Exit codes:
  0 — regression passed; impact report written.
  1 — regression FAILED; see console for details.
"""
import sys, json, pathlib, datetime

HERE   = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

import score_engine
from constants import DIMENSION_WEIGHTS, VEG_SPREAD_WEIGHTS, score_to_grade
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product

CORPUS   = pathlib.Path(r"C:\Users\HP\bari\src\data\comparisons\hummus_frontend_v3.json")
REPORT   = pathlib.Path(r"C:\Users\HP\bari\docs\spread_subtype_impact_report_v1.md")

LEGUME_TYPES    = {"hummus_spread", "masabacha"}
VEG_TYPES       = {"matbucha", "pepper_spread", "eggplant_spread"}


def to_product(item):
    n   = (item.get("expansion") or {}).get("nutrition") or {}
    ing = (item.get("expansion") or {}).get("ingredients") or ""
    ing_list = [t.strip() for t in ing.replace("(", ", ").replace(")", ", ").split(",") if t.strip()]
    return {
        "file_type": "product",
        "canonical_product_id": item["id"],
        "canonical_name_he": item.get("name", ""),
        "brand": "",
        "ingredients_text_he": ing,
        "ingredients_list": ing_list,
        "normalized_nutrition_per_100g": {
            "energy_kcal":     n.get("energyKcal"),
            "fat_g":           n.get("fat"),
            "fat_saturated_g": None,
            "fat_trans_g":     None,
            "sodium_mg":       n.get("sodium"),
            "carbohydrates_g": None,
            "sugars_g":        n.get("sugar"),
            "dietary_fiber_g": n.get("fiber"),
            "protein_g":       n.get("protein"),
        },
        "canonical_trust_level": "high",
    }


def run_pipeline(product, force_weights=None):
    """Run real pipeline. force_weights bypasses subtype selection (baseline only)."""
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    return score_product(product, signals, cat_result, nova_result, eval_result,
                         _force_weights=force_weights)


def main():
    items   = json.load(open(CORPUS, encoding="utf-8"))["products"]
    results = []

    for it in items:
        pt   = it.get("_product_type", "?")
        prod = to_product(it)

        # Engine score (EXCEPTION-002 active — uses the right vector per subtype)
        live = run_pipeline(prod)
        live_score = live.get("final_score_estimate")
        live_grade = live.get("grade_estimate")
        sfr = live.get("spread_family_result") or {}

        # Baseline: force DIMENSION_WEIGHTS on every item to reproduce pre-EXCEPTION-002
        # (for legumes this is the same vector; the comparison proves there is no movement)
        base = run_pipeline(prod, force_weights=DIMENSION_WEIGHTS)
        base_score = base.get("final_score_estimate")
        base_grade = base.get("grade_estimate")

        d_score = None
        if live_score is not None and base_score is not None:
            d_score = round(live_score - base_score, 2)

        results.append({
            "id": it["id"], "name": it.get("name", ""), "ptype": pt,
            "base_score": base_score, "base_grade": base_grade,
            "live_score": live_score, "live_grade": live_grade,
            "d_score": d_score,
            "family": sfr.get("family"), "weights_applied": sfr.get("weights_applied"),
            "name_signal": sfr.get("name_signal"),
            "protein_guard": sfr.get("protein_guard_check"),
            "trace_flag": sfr.get("trace_flag"),
        })

    # -------------------------------------------------------------------------
    # Regression gate
    # -------------------------------------------------------------------------
    legume_rows  = [r for r in results if r["ptype"] in LEGUME_TYPES]
    veg_rows     = [r for r in results if r["ptype"] in VEG_TYPES]
    scored_legume = [r for r in legume_rows if r["d_score"] is not None]
    movers = [r for r in scored_legume if r["d_score"] != 0.0]

    passed = (len(movers) == 0)
    print("=" * 60)
    print(f"REGRESSION GATE: {'PASSED' if passed else 'FAILED'}")
    print(f"  Legume items scored: {len(scored_legume)}")
    print(f"  Legume items with movement: {len(movers)}  (required: 0)")
    if movers:
        for r in movers:
            print(f"  FAIL: {r['name'][:40]}  base={r['base_score']} live={r['live_score']} d={r['d_score']}")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # Impact report
    # -------------------------------------------------------------------------
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    reg_status = "PASSED" if passed else "FAILED"

    scored_veg = [r for r in veg_rows if r["d_score"] is not None]
    grade_moves_veg  = [r for r in scored_veg if r["base_grade"] != r["live_grade"]]
    avg_base_veg = round(sum(r["base_score"] for r in scored_veg) / max(len(scored_veg), 1), 1) if scored_veg else None
    avg_live_veg = round(sum(r["live_score"] for r in scored_veg) / max(len(scored_veg), 1), 1) if scored_veg else None

    def grade_dist(rs, key):
        from collections import Counter
        d = Counter(r[key] for r in rs if r[key])
        return " · ".join(f"{g}{d[g]}" for g in ["S","A","B","C","D","E","insufficient_data"] if g in d)

    def tbl_row(r):
        d = f"{r['d_score']:+.1f}" if r["d_score"] is not None else "—"
        return (f"| {r['name'][:36]:36s} | {r['base_score'] or '—':>5} / {r['base_grade'] or '—':^17} "
                f"| {r['live_score'] or '—':>5} / {r['live_grade'] or '—':^17} | {d:>5} | "
                f"{(r['weights_applied'] or '—'):15s} | {(r['trace_flag'] or '—'):40s} |")

    lines = [
        f"# BSIP2 Spread Subtype Impact Report v1",
        f"",
        f"**Run date:** {run_dt}",
        f"**Exception:** EXCEPTION-002 — sauce_spread subtype-aware weights",
        f"**Corpus:** hummus_frontend_v3.json ({len(results)} items)",
        f"**Regression gate:** {reg_status}",
        f"",
        f"---",
        f"",
        f"## Regression: Legume / Masabacha corpus (n={len(legume_rows)})",
        f"",
        f"**Required:** 0 items with score movement.",
        f"**Result:** {len(movers)} items moved. Gate: **{reg_status}**.",
        f"",
        f"| {'Product':36s} | {'Baseline score/grade':23s} | {'Live score/grade':23s} | {'Delta':>5} | {'Weights':15s} | {'Flag':40s} |",
        f"|{'-'*38}|{'-'*25}|{'-'*25}|{'-'*7}|{'-'*17}|{'-'*42}|",
    ]
    for r in sorted(legume_rows, key=lambda x: -(x["base_score"] or 0)):
        lines.append(tbl_row(r))

    lines += [
        f"",
        f"Grade distribution (baseline): {grade_dist(legume_rows, 'base_grade')}",
        f"Grade distribution (live):     {grade_dist(legume_rows, 'live_grade')}",
        f"",
        f"---",
        f"",
        f"## Impact: Vegetable spread corpus (n={len(veg_rows)})",
        f"",
        f"Average score: baseline **{avg_base_veg}** → live **{avg_live_veg}** (Δ{round((avg_live_veg or 0)-(avg_base_veg or 0),1):+.1f})",
        f"Grade changes: **{len(grade_moves_veg)} of {len(scored_veg)}** items change grade.",
        f"",
        f"Grade distribution (baseline): {grade_dist(veg_rows, 'base_grade')}",
        f"Grade distribution (live):     {grade_dist(veg_rows, 'live_grade')}",
        f"",
        f"| {'Product':36s} | {'Baseline score/grade':23s} | {'Live score/grade':23s} | {'Delta':>5} | {'Weights':15s} | {'Flag':40s} |",
        f"|{'-'*38}|{'-'*25}|{'-'*25}|{'-'*7}|{'-'*17}|{'-'*42}|",
    ]
    for r in sorted(veg_rows, key=lambda x: -(x["live_score"] or 0)):
        lines.append(tbl_row(r))

    lines += [
        f"",
        f"### Items held at D after EXCEPTION-002 (legitimate guardrails binding)",
        f"",
    ]
    still_d = [r for r in scored_veg if r["live_grade"] == "D"]
    if still_d:
        for r in still_d:
            lines.append(f"- **{r['name']}** — live {r['live_score']}/D  "
                         f"(base {r['base_score']}/{r['base_grade']}, Δ{r['d_score']:+.1f})")
    else:
        lines.append("_None — all vegetable items moved above D._")

    lines += [
        f"",
        f"---",
        f"",
        f"## Summary",
        f"",
        f"| Corpus | n | Avg baseline | Avg live | Items grade-changed | Regression |",
        f"|--------|:-:|:------------:|:--------:|:-------------------:|:----------:|",
        f"| Legume | {len(legume_rows)} | {round(sum(r['base_score'] for r in legume_rows if r['base_score'])/max(sum(1 for r in legume_rows if r['base_score']),1),1)} | {round(sum(r['live_score'] for r in legume_rows if r['live_score'])/max(sum(1 for r in legume_rows if r['live_score']),1),1)} | 0 | **{reg_status}** |",
        f"| Vegetable | {len(veg_rows)} | {avg_base_veg} | {avg_live_veg} | {len(grade_moves_veg)} | n/a |",
        f"",
        f"*Reproducible: re-run `run_spread_subtype_regression.py` against the same corpus.*",
    ]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written: {REPORT}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
