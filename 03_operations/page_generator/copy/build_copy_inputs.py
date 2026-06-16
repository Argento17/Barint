#!/usr/bin/env python3
"""build_copy_inputs.py — Part 1 of the Copy Engine (P29 / TASK-257 Phase 2 + TASK-262 / P43 v3).

DETERMINISTIC. Assembles a FACT SHEET per product: the ONLY material the
Hebrew author (Part 2) is permitted to use. No copy is written here — this
script only extracts verifiable facts from the generated page JSON + the BSIP2
traces, and computes corpus statistics that make superlative claims safe.

Inputs:
  --config   category config JSON (configs/<category>.json) — for run_products_dir
  --page     generated page JSON (outputs/<category>_generated_v1.json)
  --out      fact_sheets.json

Per product the fact sheet carries:
  barcode, id, name, retailer, score, grade
  driver:           the REAL driver from the trace
                      - if a cap binds (binding_cap present AND ~= score) → cap story
                      - else → lowest-dimension story (explanation_drivers)
  cap_misclaim_risk: TRUE when binding_cap is present but binding_cap > score
                     (the cap did NOT actually bind — author must NOT claim a
                     cap/processing limit; tell the dimension story instead)
  nutrition:        protein / sugar / fat / kcal / sodium / fiber from the
                    product's OWN expansion.nutrition (null stays null)
  ingredients_head: first 3 ingredients if present
  additive_count:   len(d4_additives)
  superlatives_allowed: list of superlative tokens THIS product may use,
                    proven by corpus stats (e.g. "lowest_kcal"). Empty = none.
  s_verbatim:       for the 2 S products only — the Nutrition-APPROVED verbatim
                    Hebrew (insight line + S paragraph). Author may NOT paraphrase.

  v3 additions (TASK-262 / P43):
  bari_interpretation_inputs: list of {key, label, score, strength} from the
                    page's bariInterpretation (already deterministic; author reads
                    these to write each interpretation sentence).
  best_use_cases_pending: boolean — True when the page carries PENDING_COPY for
                    bestUseCases (author must fill); False = already deterministic.

stdlib only. No network. No OFF. null stays null.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# The two S products and their Nutrition-APPROVED verbatim Hebrew.
# Source: 02_products/yogurt_system/s_grade_explanations_v1.md (APPROVED 2026-06-12).
# These strings are byte-verbatim and MUST NOT be paraphrased by the author.
S_VERBATIM = {
    "7290112336712": {
        "insightLine": "שני מרכיבים בלבד: חלב מפוסטר וחיידקי יוגורט. ללא חומרי טעם, ממתיקים או תוספות.",
        "s_grade_explanation": (
            "דנונה פרו 21 הוא אחד מיחידים בקטגוריית היוגורטים שקיבל ציון S. "
            "הציון נובע משלושה גורמים שמצטברים: הרכב מינימלי — רק חלב מפוסטר "
            "וחיידקי יוגורט, ללא כל תוסף, ממתיק או סמיכה; צפיפות קלורית נמוכה "
            "במיוחד — 58 קילוקלוריות ל-100 גרם ללא שומן; וריכוז חלבון גבוה — "
            "10.5 גרם ל-100 גרם, כולו ממקור מלא. כל מרכיב ניקוד שנבחן — עיבוד, "
            "תוספות, טיב השומן, רמת הסוכר, תרומת חלבון — יצא נקי. לא הופעלה אף "
            "הגבלת ניקוד."
        ),
    },
    "7290110565527": {
        "insightLine": "שני מרכיבים: חלב מפוסטר וחיידקי יוגורט. ללא תוספות, ממתיקים או חומרי סמיכה.",
        "s_grade_explanation": (
            "דנונה פרו 20 קיבל ציון S על בסיס אותו עיקרון כמו תאומו ה-21 גרם: "
            "מרכיב יחיד — חלב מפוסטר עם חיידקי יוגורט — ללא שום תוספת. בהשוואה "
            "לגרסת ה-21 גרם, מוצר זה מכיל 1.5 גרם שומן ל-100 גרם (לעומת 0%) "
            "ו-10 גרם חלבון (לעומת 10.5 גרם), מה שמוריד אותו ב-2 נקודות. בכל "
            "שאר המרכיבים — עיבוד, תוספות, רמת הסוכר, רגולציה — אין הבדל: שני "
            "המוצרים עברו את כל שערי הניקוד ולא הופעל אף קנס."
        ),
    },
}

# Cap rule → consumer-vocabulary tag (for the author; NOT final copy).
# The author writes the Hebrew; this only names the honest story.
CAP_RULE_STORY = {
    "NOVA_PROXY_4_ULTRA_PROCESSED": "heavy_processing_additives",
    "ADDITIVE_MARKERS_3_PLUS": "several_additives",
    "ADDITIVE_MARKERS_5_PLUS": "many_additives",
    "HIGH_SUGAR_25G_PLUS": "high_added_sugar",
    "HIGH_CAL_HIGH_SUGAR_SEVERE": "calorie_and_sugar_load",
    "HIGH_CAL_HIGH_SUGAR_MODERATE": "calorie_and_sugar_load",
    "SWEETENER_PRESENT": "sweetener_present",
}

PENALTY_STORY = {
    "MULTIPLE_ADDED_SUGAR_MARKERS": "multiple_added_sugar_sources",
    "LONG_INGREDIENT_LIST": "long_ingredient_list",
    "SEED_OIL_PRESENT": "seed_oil_present",
}

# lowest dimension → consumer-vocabulary tag
DIMENSION_STORY = {
    "processing_quality": "processing_is_the_ceiling",
    "nutrient_density": "modest_nutrient_density",
    "calorie_density": "calorie_dense",
    "glycemic_quality": "sugar_load",
    "protein_quality": "protein_modest_or_fortified",
    "additive_quality": "additives_present",
    "satiety_support": "low_satiety",
    "fat_quality": "fat_profile",
    "regulatory_quality": "regulatory_flag",
    "whole_food_integrity": "distance_from_whole_food",
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def trace_path(run_dir, product_id):
    return os.path.join(run_dir, product_id, "bsip2_trace.json")


CAP_TOLERANCE = 0.5


def derive_driver(trace, score):
    """Return (driver_type, story_tag, detail, cap_misclaim_risk).

    driver_type ∈ {"cap", "cap_plus_penalty", "dimension"}.

    A binding_cap is a CEILING. Three honest cases:
      score ~= binding_cap  → "cap": the cap IS the reason; pure cap story.
      score <  binding_cap  → "cap_plus_penalty": the cap set the ceiling AND
                              named penalties pushed the score further down.
                              cap_misclaim_risk=TRUE so the author must NOT claim
                              the cap is the sole reason — name the penalty too.
      score >  binding_cap  → data anomaly (cap is a ceiling); fall back to the
                              dimension story and flag.
      no binding_cap        → "dimension": lowest dimension is the story.
    """
    binding_cap = trace.get("binding_cap")
    caps_applied = trace.get("caps_applied") or []
    dim_scores = trace.get("dimension_scores") or {}
    penalties = [p.get("rule") for p in (trace.get("penalties_applied") or [])]
    pen_stories = [PENALTY_STORY.get(p, p) for p in penalties]

    if binding_cap is not None and score is not None:
        rules = [c.get("rule") for c in caps_applied]
        cap_stories = [CAP_RULE_STORY.get(r, r) for r in rules]
        primary_cap_story = cap_stories[0] if cap_stories else "cap_bound"

        if abs(score - binding_cap) <= CAP_TOLERANCE:
            # cap is the operative limit
            return ("cap", primary_cap_story, {
                "binding_cap": binding_cap,
                "cap_rules": rules,
                "penalties": pen_stories,
            }, False)

        if score < binding_cap - CAP_TOLERANCE:
            # The cap is recorded but the score sits below it. Two sub-cases:
            #   (a) penalties pushed it down → "cap_plus_penalty": cap ceiling +
            #       named penalty are the joint story. Author names BOTH, never
            #       the cap alone.
            #   (b) no penalties → the cap is NOT the operative limit at all
            #       (e.g. a 94.8 ceiling at score 80). The honest driver is the
            #       lowest dimension. Fall through to the dimension story.
            lowest_dim = min(dim_scores.items(), key=lambda kv: kv[1]) if dim_scores else None
            if pen_stories:
                return ("cap_plus_penalty", primary_cap_story, {
                    "binding_cap": binding_cap,
                    "cap_rules": rules,
                    "penalties": pen_stories,
                    "gap_below_cap": round(binding_cap - score, 1),
                    "lowest_dimension": lowest_dim[0] if lowest_dim else None,
                    "lowest_dimension_value": round(lowest_dim[1], 1) if lowest_dim else None,
                }, True)
            # no penalties: cap is non-operative; dimension story, flagged so the
            # author does NOT claim a cap/processing limit.
            story = DIMENSION_STORY.get(lowest_dim[0], lowest_dim[0]) if lowest_dim else "unknown"
            return ("dimension", story, {
                "lowest_dimension": lowest_dim[0] if lowest_dim else None,
                "lowest_dimension_value": round(lowest_dim[1], 1) if lowest_dim else None,
                "cap_recorded_non_operative": binding_cap,
                "penalties": pen_stories,
            }, True)
        # score > cap: anomaly — fall through to dimension story, flagged

    # dimension story (no cap, or anomaly): lowest dimension
    lowest = None
    if dim_scores:
        lowest = min(dim_scores.items(), key=lambda kv: kv[1])
    story = DIMENSION_STORY.get(lowest[0], lowest[0]) if lowest else "unknown"
    anomaly = binding_cap is not None and score is not None and score > binding_cap + CAP_TOLERANCE
    return ("dimension", story, {
        "lowest_dimension": lowest[0] if lowest else None,
        "lowest_dimension_value": round(lowest[1], 1) if lowest else None,
        "binding_cap_anomaly": binding_cap if anomaly else None,
        "penalties": pen_stories,
    }, anomaly)


def compute_corpus_stats(products):
    """Per-metric min/max/median over displayed products (non-null only)."""
    stats = {}
    metrics = ["protein", "sugar", "energyKcal", "fat", "sodium", "fiber"]
    for m in metrics:
        vals = []
        for p in products:
            v = (p.get("expansion", {}).get("nutrition") or {}).get(m)
            if v is not None:
                vals.append(v)
        if vals:
            stats[m] = {
                "n": len(vals),
                "min": round(min(vals), 2),
                "max": round(max(vals), 2),
                "median": round(statistics.median(vals), 2),
            }
        else:
            stats[m] = {"n": 0, "min": None, "max": None, "median": None}
    return stats


def superlatives_for(product, stats):
    """Return the list of superlative tokens this product may safely use.

    A superlative is granted ONLY if this product's own value equals the
    corpus extreme AND it is uniquely or jointly the extreme. We grant the
    extremes that matter editorially:
      highest_protein, lowest_kcal, lowest_sugar.
    Joint extremes (ties) are NOT granted "the X-est" — a tie is not a
    superlative. Ties get nothing.
    """
    nut = product.get("expansion", {}).get("nutrition") or {}
    granted = []

    def is_unique_extreme(metric, want_max):
        v = nut.get(metric)
        if v is None or stats[metric]["n"] == 0:
            return False
        extreme = stats[metric]["max"] if want_max else stats[metric]["min"]
        if abs(v - extreme) > 1e-9:
            return False
        # uniqueness: count how many products hit this extreme
        count = 0
        for p in stats["_products"]:
            pv = (p.get("expansion", {}).get("nutrition") or {}).get(metric)
            if pv is not None and abs(pv - extreme) <= 1e-9:
                count += 1
        return count == 1

    if is_unique_extreme("protein", want_max=True):
        granted.append("highest_protein")
    if is_unique_extreme("energyKcal", want_max=False):
        granted.append("lowest_kcal")
    if is_unique_extreme("sugar", want_max=False):
        granted.append("lowest_sugar")
    return granted


def main():
    ap = argparse.ArgumentParser(description="Build copy fact sheets (Part 1).")
    ap.add_argument("--config", required=True)
    ap.add_argument("--page", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    config = load_json(args.config)
    page = load_json(args.page)
    run_dir = config["run_products_dir"]

    products = page["products"]
    stats = compute_corpus_stats(products)
    stats["_products"] = products  # internal handle for uniqueness checks

    sheets = []
    ambiguous = []
    for p in products:
        bc = p["barcode"]
        tp = trace_path(run_dir, p["id"])
        trace = load_json(tp) if os.path.isfile(tp) else {}
        score = p.get("score")

        driver_type, story_tag, detail, cap_misclaim = derive_driver(trace, score)
        if story_tag in ("unknown", "cap_bound"):
            ambiguous.append({"barcode": bc, "name": p["name"], "reason": story_tag})

        nut = p.get("expansion", {}).get("nutrition") or {}
        ingredients = p.get("expansion", {}).get("ingredients")
        ing_head = None
        if ingredients:
            parts = [s.strip() for s in ingredients.split(",") if s.strip()]
            ing_head = parts[:3]

        # v3: extract bariInterpretation inputs for the author
        bari_interp_inputs = []
        for entry in (p.get("bariInterpretation") or []):
            # Carry key/label/score/strength to author; NOT interpretation (PENDING)
            bari_interp_inputs.append({
                "key": entry.get("key"),
                "label": entry.get("label"),
                "score": entry.get("score"),
                "strength": entry.get("strength"),
            })

        # v3: is bestUseCases PENDING or already deterministic?
        best_uc = p.get("bestUseCases") or []
        best_use_cases_pending = (
            len(best_uc) == 0
            or (len(best_uc) == 1 and best_uc[0] == "PENDING_COPY")
        )

        sheet = {
            "barcode": bc,
            "id": p["id"],
            "name": p["name"],
            "retailer": p.get("retailer"),
            "score": score,
            "grade": p.get("grade"),
            "driver": {
                "type": driver_type,
                "story": story_tag,
                "detail": detail,
            },
            "cap_misclaim_risk": cap_misclaim,
            "nutrition": {
                "protein": nut.get("protein"),
                "sugar": nut.get("sugar"),
                "fat": nut.get("fat"),
                "kcal": nut.get("energyKcal"),
                "sodium": nut.get("sodium"),
                "fiber": nut.get("fiber"),
            },
            "ingredients_head": ing_head,
            "additive_count": len(p.get("d4_additives") or []),
            "superlatives_allowed": superlatives_for(p, stats),
            # v3 additions
            "bari_interpretation_inputs": bari_interp_inputs,
            "best_use_cases_pending": best_use_cases_pending,
            "best_use_cases_deterministic": [] if best_use_cases_pending else list(best_uc),
        }
        if bc in S_VERBATIM:
            sheet["s_verbatim"] = S_VERBATIM[bc]
        sheets.append(sheet)

    del stats["_products"]
    out = {
        "_meta": {
            "category": config.get("category"),
            "page_source": os.path.abspath(args.page),
            "config_source": os.path.abspath(args.config),
            "product_count": len(sheets),
            "corpus_stats": stats,
            "ambiguous_drivers": ambiguous,
            "s_products": list(S_VERBATIM.keys()),
            "note": "FACT SHEETS — the only material the author may use. null stays null.",
        },
        "sheets": sheets,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(sheets)} fact sheets to {args.out}")
    print(f"Ambiguous drivers: {len(ambiguous)}")
    if ambiguous:
        for a in ambiguous:
            print(f"  - {a['barcode']} {a['name']}: {a['reason']}")
    cap_risk = sum(1 for s in sheets if s["cap_misclaim_risk"])
    print(f"cap_misclaim_risk flagged: {cap_risk}/{len(sheets)}")


if __name__ == "__main__":
    main()
