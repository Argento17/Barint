"""
TASK-278 Spread Analysis Runner
Extracts sugar/sat_fat/sodium distributions + floor-saturation metrics
from committed BSIP2 traces for every live category.
ANALYSIS ONLY — no edits to any engine or trace.

Formats handled:
  A) Standard: products/bsip1_XXX/bsip2_trace.json  (full L1+L2+scoring fields)
  B) Flat-dir: bsip2/bsip2_shufersal_XXX.json  (bread — has nutrition{} + final_score)
  C) Nested: products/products/bsip1_XXX/bsip2_trace.json  (yogurt shipcfg2 quirk)
"""

import json
import os
import math
import statistics
from pathlib import Path


def safe_val(v):
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def load_traces_standard(products_dir):
    """Format A / C: scan for bsip2_trace.json at depth 1 or 2."""
    traces = []
    p = Path(products_dir)
    if not p.exists():
        return traces

    for product_dir in p.iterdir():
        if product_dir.is_dir():
            trace_file = product_dir / "bsip2_trace.json"
            if not trace_file.exists():
                # Check one level deeper (yogurt products/products/…)
                for sub in product_dir.iterdir():
                    if sub.is_dir():
                        tf2 = sub / "bsip2_trace.json"
                        if tf2.exists():
                            try:
                                with open(tf2, encoding='utf-8') as f:
                                    traces.append(json.load(f))
                            except Exception as e:
                                print(f"  WARN: {tf2}: {e}")
            else:
                try:
                    with open(trace_file, encoding='utf-8') as f:
                        traces.append(json.load(f))
                except Exception as e:
                    print(f"  WARN: {trace_file}: {e}")
    return traces


def load_traces_bread(flat_dir):
    """Format B: bread bsip2/ flat JSON files — nutrition + final_score schema."""
    traces = []
    p = Path(flat_dir)
    if not p.exists():
        return traces
    for f in p.glob("bsip2_*.json"):
        try:
            with open(f, encoding='utf-8') as fp:
                d = json.load(fp)
            # Normalise to common trace schema
            nutr = d.get("nutrition") or {}
            t = {
                "_format": "bread_flat",
                "final_score_estimate": safe_val(d.get("final_score")),
                "grade_estimate": d.get("final_grade"),
                "score_after_cap": safe_val(d.get("final_score")),  # no cap field
                "score_after_floors": safe_val(d.get("final_score")),
                "total_penalty_after_scaling": 0.0,
                "evaluation_status": "scored" if d.get("final_score") is not None else "unscored",
                "L1_observed_signals": {
                    "sugars_g": safe_val(nutr.get("sugars_g")),
                    "fat_saturated_g": safe_val(nutr.get("fat_saturated_g")),
                    "sodium_mg": safe_val(nutr.get("sodium_mg")),
                }
            }
            traces.append(t)
        except Exception as e:
            print(f"  WARN: {f}: {e}")
    return traces


def percentile(sorted_vals, p):
    if not sorted_vals:
        return None
    n = len(sorted_vals)
    idx = (p / 100) * (n - 1)
    lo = int(idx)
    hi = min(lo + 1, n - 1)
    frac = idx - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def compute_distribution(vals):
    clean = sorted([v for v in vals if v is not None])
    if not clean:
        return {"n": 0, "median": None, "iqr": None, "robust_scale": None,
                "min": None, "max": None, "stdev": None, "mean": None,
                "q1": None, "q3": None}
    n = len(clean)
    med = percentile(clean, 50)
    q1 = percentile(clean, 25)
    q3 = percentile(clean, 75)
    iqr = q3 - q1 if q1 is not None and q3 is not None else None
    deviations = sorted([abs(v - med) for v in clean])
    mad = percentile(deviations, 50)
    rs_candidates = [1.4]
    if iqr is not None:
        rs_candidates.append(iqr / 1.349)
    if mad is not None:
        rs_candidates.append(1.4826 * mad)
    robust_scale = max(rs_candidates)
    stdev = statistics.stdev(clean) if n >= 2 else 0.0
    return {
        "n": n,
        "median": round(med, 2),
        "q1": round(q1, 2),
        "q3": round(q3, 2),
        "iqr": round(iqr, 2) if iqr is not None else None,
        "robust_scale": round(robust_scale, 3),
        "min": round(clean[0], 2),
        "max": round(clean[-1], 2),
        "stdev": round(stdev, 2),
        "mean": round(statistics.mean(clean), 2),
    }


def analyze_category(category, spec):
    """
    spec is either:
      {"type": "standard", "path": "..."}
      {"type": "bread_flat", "path": "..."}
      None  → no run
    """
    result = {
        "category": category,
        "run_id": None,
        "products_path": None,
    }

    if spec is None:
        result["status"] = "no_run"
        result["n_scored"] = 0
        return result

    result["products_path"] = spec["path"]

    if spec["type"] == "standard":
        traces = load_traces_standard(spec["path"])
        # Derive run_id from path
        parts = spec["path"].replace("\\", "/").split("/")
        run_id = None
        for p in parts:
            if p.startswith("run_") or p.startswith("butter_run_"):
                run_id = p
        result["run_id"] = run_id
    elif spec["type"] == "bread_flat":
        traces = load_traces_bread(spec["path"])
        result["run_id"] = "real_bread_retail_003_v1"
    else:
        result["status"] = "unknown_type"
        return result

    if not traces:
        result["status"] = "no_traces"
        result["n"] = 0
        result["n_scored"] = 0
        return result

    result["status"] = "ok"
    result["n"] = len(traces)

    sugars = []
    sat_fat = []
    sodium = []
    final_scores = []
    scores_after_cap = []
    absorption_gaps = []

    for t in traces:
        ev = t.get("evaluation_status", "scored")
        if ev in ("excluded", "skipped", "not_scored", "unscored"):
            continue
        fse = safe_val(t.get("final_score_estimate"))
        if fse is None:
            continue

        L1 = t.get("L1_observed_signals", {})
        sugars.append(safe_val(L1.get("sugars_g")))
        sat_fat.append(safe_val(L1.get("fat_saturated_g")))
        sodium.append(safe_val(L1.get("sodium_mg")))

        final_scores.append(fse)

        sac = safe_val(t.get("score_after_cap"))
        if sac is not None:
            absorption_gaps.append(sac - fse)

    result["n_scored"] = len(final_scores)

    result["sugar"] = compute_distribution(sugars)
    result["sat_fat"] = compute_distribution(sat_fat)
    result["sodium"] = compute_distribution(sodium)
    result["score"] = compute_distribution(final_scores)

    # Floor saturation: % with final_score ≤ 33 (floor=30, +3 buffer)
    scored_final = [v for v in final_scores if v is not None]
    abs_floor_threshold = 33.0
    n_at_floor = sum(1 for s in scored_final if s <= abs_floor_threshold)
    pct_floored = round(100 * n_at_floor / len(scored_final), 1) if scored_final else 0.0

    result["floor_saturation"] = {
        "n_at_floor": n_at_floor,
        "n_scored": len(scored_final),
        "pct_floored": pct_floored,
        "floor_threshold": 33,
        "obs_min_score": round(min(scored_final), 1) if scored_final else None,
        "obs_max_score": round(max(scored_final), 1) if scored_final else None,
        "score_range": round(max(scored_final) - min(scored_final), 1) if scored_final else 0,
    }

    # Scaling-pinned absorption: score_after_cap - final_score > 5
    n_pinned = sum(1 for g in absorption_gaps if g > 5)
    pct_pinned = round(100 * n_pinned / len(absorption_gaps), 1) if absorption_gaps else 0.0

    result["absorption"] = {
        "n_pinned": n_pinned,
        "n_with_gap": len(absorption_gaps),
        "pct_scaling_pinned": pct_pinned,
        "gap_median": round(statistics.median(absorption_gaps), 1) if absorption_gaps else 0,
        "gap_max": round(max(absorption_gaps), 1) if absorption_gaps else 0,
    }

    return result


def classify(r):
    if r.get("status") in ("no_run", "no_traces"):
        return "N-A", "no committed run"
    if r.get("n_scored", 0) < 5:
        return "N-A", f"only {r.get('n_scored', 0)} scored products — too thin"

    pct_floored = r["floor_saturation"]["pct_floored"]
    pct_pinned = r["absorption"]["pct_scaling_pinned"]
    score_stdev = r["score"]["stdev"] or 0
    sugar_scale = r["sugar"].get("robust_scale") or 0

    # COSMETIC: heavily floor-saturated OR heavily pinned with compressed scores
    if pct_floored >= 40 and score_stdev < 10:
        return "COSMETIC", f"{pct_floored}% floored, score_stdev={score_stdev} — floor absorption dominates"
    if pct_pinned >= 70 and score_stdev < 10:
        return "COSMETIC", f"{pct_pinned}% absorption-pinned, score_stdev={score_stdev}"
    if pct_floored >= 60:
        return "COSMETIC", f"{pct_floored}% floored — shelf-relative term absorbed by floor"

    # LAND: real spread, low floor saturation
    if pct_floored < 20 and score_stdev >= 6:
        return "LAND", f"only {pct_floored}% floored, score_stdev={score_stdev}"
    if pct_floored < 30 and score_stdev >= 10:
        return "LAND", f"{pct_floored}% floored, score_stdev={score_stdev}"

    # Mixed: pinned but not floored OR moderate floor
    if pct_pinned >= 80 and pct_floored < 10:
        return "MARGINAL-PINNED", (
            f"{pct_pinned}% absorption-pinned despite {pct_floored}% floored — "
            "penalty-scaling absorbs relative term even without floor saturation"
        )
    return "MARGINAL", f"{pct_floored}% floored, {pct_pinned}% pinned, score_stdev={score_stdev}"


def candidate_nutrient(r):
    if r.get("status") not in ("ok",) or r.get("n_scored", 0) < 5:
        return "N-A"
    cat = r["category"]

    # Category-specific overrides based on what actually drives the score
    if cat in ("juices",):
        return "sugar"
    if cat in ("butter",):
        return "sat_fat"
    if cat in ("brined_cheeses",):
        return "sodium"
    if cat in ("salty_snacks",):
        return "sodium"
    if cat in ("milk",):
        return "sat_fat"  # milk differentiation is fat type / % fat

    # Default: pick highest robust_scale
    sugar_scale = r["sugar"].get("robust_scale") or 0
    sf_scale = r["sat_fat"].get("robust_scale") or 0
    # Normalize sodium (mg) to same rough scale as g nutrients: /100
    na_scale = (r["sodium"].get("robust_scale") or 0) / 100

    candidates = {"sugar": sugar_scale, "sat_fat": sf_scale, "sodium": na_scale}
    best = max(candidates, key=candidates.get)
    if candidates[best] == 0:
        return "insufficient_data"
    return best


# ── Main ──────────────────────────────────────────────────────────────────────

RUN_SPECS = {
    "milk": {
        "type": "standard",
        "path": "C:/Bari/02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products"
    },
    "bread": {
        "type": "bread_flat",
        "path": "C:/Bari/02_products/bread_retail_003/bsip2"
    },
    "snack_bars": {
        "type": "standard",
        "path": "C:/Bari/02_products/snack_bars/bsip2_outputs/run_snack_bars_001/products"
    },
    "cereals": {
        "type": "standard",
        "path": "C:/Bari/02_products/breakfast_cereals/bsip2_outputs/run_cereals_synthesis_001/products"
    },
    "hummus": {
        "type": "standard",
        "path": "C:/Bari/02_products/hummus/intelligence_bsip2/run_hummus_002/products"
    },
    "salty_snacks": {
        "type": "standard",
        "path": "C:/Bari/02_products/salty_snacks/bsip2_outputs/run_salty_snacks_002/products"
    },
    "juices": {
        "type": "standard",
        "path": "C:/Bari/02_products/juices/bsip2_outputs/run_juices_yohananof_002/products"
    },
    "hard_cheeses": {
        "type": "standard",
        "path": "C:/Bari/02_products/hard_cheeses/bsip2_outputs/run_hard_cheeses_001/products"
    },
    "butter": {
        "type": "standard",
        "path": "C:/Bari/02_products/butter/bsip2_outputs/butter_run_003/products"
    },
    "cheese_spreads": {
        "type": "standard",
        "path": "C:/Bari/02_products/cheese_spreads/bsip2_outputs/run_cheese_004/products"
    },
    "yogurt": {
        "type": "standard",
        "path": "C:/Bari/02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2/products/products"
    },
    "brined_cheeses": {
        "type": "standard",
        "path": "C:/Bari/02_products/brined_cheeses/bsip2_outputs/run_brined_005/products"
    },
    "cookies_coffee": {
        "type": "standard",
        "path": "C:/Bari/02_products/cookies_coffee/bsip2_outputs/run_cookies_005_shelfrel_pilot/products"
    },
    "granola": None,  # No separate run — granola products are inside cereals corpus
    "frozen_vegetables": {
        "type": "standard",
        "path": "C:/Bari/02_products/frozen_vegetables/bsip2_outputs/run_frozen_vegetables_001/products"
    },
    "maadanim": {
        "type": "standard",
        "path": "C:/Bari/02_products/maadanim/bsip2_outputs/run_maadanim_001/products"
    },
}


def main():
    results = {}

    for cat, spec in RUN_SPECS.items():
        print(f"Processing {cat}...")
        r = analyze_category(cat, spec)
        classification, reason = classify(r)
        r["classification"] = classification
        r["classification_reason"] = reason
        r["candidate_nutrient"] = candidate_nutrient(r)
        results[cat] = r

        if r.get("status") == "ok":
            print(f"  n_scored={r['n_scored']}, "
                  f"score_stdev={r['score']['stdev']}, "
                  f"pct_floored={r['floor_saturation']['pct_floored']}, "
                  f"pct_pinned={r['absorption']['pct_scaling_pinned']}, "
                  f"sugar_med={r['sugar']['median']}, "
                  f"sugar_IQR={r['sugar']['iqr']}, "
                  f"=> {classification}")
        else:
            print(f"  status={r.get('status')} => {classification}")

    # Save raw results
    out_path = "C:/Bari/01_framework/bsip2_framework/project_rescore/spread_analysis_raw_v1.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nRaw results saved to: {out_path}")
    return results


if __name__ == "__main__":
    main()
