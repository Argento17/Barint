"""
TASK-089A — Subtype-aware calibration impact analysis for spreads.

ANALYSIS ONLY. Does NOT modify the engine. It drives the real BSIP2 pipeline to
get authentic BSIP2-native dimension scores, then re-scores each item under a
PROPOSED subtype-aware DIMENSION_WEIGHTS vector by temporarily rebinding
score_engine.DIMENSION_WEIGHTS at runtime (restored afterward). The engine's
own cap / penalty / floor / ceiling logic runs unchanged under both weightings.

Corpus: src/data/comparisons/hummus_frontend_v3.json (carries nutrition,
ingredients, and the already-assigned _product_type subtype label).
"""
import json, pathlib, sys, copy

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

import score_engine
from constants import DIMENSION_WEIGHTS, score_to_grade
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product

CORPUS = pathlib.Path(r"C:\Users\HP\bari\src\data\comparisons\hummus_frontend_v3.json")

# --- subtype grouping -------------------------------------------------------
LEGUME   = {"hummus_spread", "masabacha"}          # legume + tahini-heavy archetype
VEGETABLE = {"matbucha", "pepper_spread", "eggplant_spread"}

# --- PROPOSED vegetable-spread weight vector (TASK-089A) --------------------
# Reduce protein/fiber-driven dims; redistribute to universal density/quality dims.
VEG_WEIGHTS = {
    "processing_quality":   0.17,   # +0.02
    "nutrient_density":     0.10,   # -0.05
    "calorie_density":      0.19,   # +0.04
    "glycemic_quality":     0.16,   # +0.04
    "protein_quality":      0.03,   # -0.07
    "additive_quality":     0.13,   # +0.03
    "satiety_support":      0.03,   # -0.03
    "fat_quality":          0.08,   #  0
    "regulatory_quality":   0.07,   # +0.02
    "whole_food_integrity": 0.04,   #  0
}
assert abs(sum(VEG_WEIGHTS.values()) - 1.0) < 1e-9, sum(VEG_WEIGHTS.values())
assert abs(sum(DIMENSION_WEIGHTS.values()) - 1.0) < 1e-9


def load_corpus():
    d = json.load(open(CORPUS, encoding="utf-8"))
    return d["products"]


def to_product(item):
    n = item.get("expansion", {}).get("nutrition", {}) or {}
    ing = item.get("expansion", {}).get("ingredients", "") or ""
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


def score_one(product, weights):
    """Run the full real pipeline; weights rebinds score_engine.DIMENSION_WEIGHTS."""
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    saved = score_engine.DIMENSION_WEIGHTS
    try:
        score_engine.DIMENSION_WEIGHTS = weights
        res = score_product(product, signals, cat_result, nova_result, eval_result)
    finally:
        score_engine.DIMENSION_WEIGHTS = saved
    return res, cat_result, nova_result


def subtype_of(pt):
    if pt in LEGUME:    return "legume"
    if pt in VEGETABLE: return "vegetable"
    return "other"


def main():
    items = load_corpus()
    rows = []
    for it in items:
        pt = it.get("_product_type", "?")
        st = subtype_of(pt)
        prod = to_product(it)
        base, cat, nova = score_one(prod, DIMENSION_WEIGHTS)
        prop_weights = VEG_WEIGHTS if st == "vegetable" else DIMENSION_WEIGHTS
        prop, _, _ = score_one(prod, prop_weights)
        rows.append({
            "id": it["id"], "name": it.get("name", ""), "ptype": pt, "subtype": st,
            "cat": cat["category"], "nova": nova["nova_level"],
            "v3_score": it.get("score"), "v3_grade": it.get("grade"),
            "base_score": base.get("final_score_estimate"),
            "base_grade": base.get("grade_estimate"),
            "prop_score": prop.get("final_score_estimate"),
            "prop_grade": prop.get("grade_estimate"),
            "cap": base.get("binding_cap"),
            "dims": base.get("dimension_scores"),
        })

    # rankings (by BSIP2-native baseline vs proposed), full corpus
    def ranks(key):
        order = sorted([r for r in rows if r[key] is not None], key=lambda r: -r[key])
        return {r["id"]: i + 1 for i, r in enumerate(order)}
    rb = ranks("base_score"); rp = ranks("prop_score")
    for r in rows:
        r["rank_base"] = rb.get(r["id"]); r["rank_prop"] = rp.get(r["id"])
        if r["base_score"] is not None and r["prop_score"] is not None:
            r["d_score"] = round(r["prop_score"] - r["base_score"], 1)
            r["d_rank"]  = (r["rank_base"] - r["rank_prop"])
        else:
            r["d_score"] = None; r["d_rank"] = None

    out = {"rows": rows, "veg_weights": VEG_WEIGHTS, "base_weights": dict(DIMENSION_WEIGHTS)}
    pathlib.Path(HERE / "spread_subtype_impact.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- console summary ----
    def grp(st): return [r for r in rows if r["subtype"] == st]
    def dist(rs, key):
        from collections import Counter
        return dict(Counter(r[key] for r in rs))

    print("=== CORPUS:", len(rows), "items ===")
    for st in ("legume", "vegetable"):
        rs = grp(st)
        scored = [r for r in rs if r["d_score"] is not None]
        moved = [r for r in scored if r["d_score"] != 0]
        gmoved = [r for r in scored if r["base_grade"] != r["prop_grade"]]
        avg_base = round(sum(r["base_score"] for r in scored)/max(len(scored),1), 1)
        avg_prop = round(sum(r["prop_score"] for r in scored)/max(len(scored),1), 1)
        print(f"\n--- {st.upper()}  (n={len(rs)}) ---")
        print("  base grade dist:", dist(scored, "base_grade"))
        print("  prop grade dist:", dist(scored, "prop_grade"))
        print(f"  avg score: base {avg_base} -> prop {avg_prop} (Δ{round(avg_prop-avg_base,1)})")
        print(f"  items with score change: {len(moved)}/{len(scored)}; grade change: {len(gmoved)}")
        for r in gmoved:
            print(f"    {r['name'][:34]:34s} {r['base_score']}/{r['base_grade']} -> "
                  f"{r['prop_score']}/{r['prop_grade']}  (Δrank {r['d_rank']:+d}) nova{r['nova']} cap={r['cap']}")

    # legume sanity: any legume score move at all?
    leg_moves = [r for r in grp("legume") if r["d_score"] not in (None, 0)]
    print(f"\nLEGUME score changes (should be 0): {len(leg_moves)}")

    # case study item
    cs = [r for r in rows if "פלפלים" in r["name"]]
    print("\n=== pepper-spread items ===")
    for r in cs:
        print(f"  {r['name'][:34]:34s} base {r['base_score']}/{r['base_grade']} "
              f"-> prop {r['prop_score']}/{r['prop_grade']}  dims ND={r['dims']['nutrient_density']} "
              f"PQ={r['dims']['protein_quality']} SS={r['dims']['satiety_support']}")
    print("\nwrote spread_subtype_impact.json")


if __name__ == "__main__":
    main()
