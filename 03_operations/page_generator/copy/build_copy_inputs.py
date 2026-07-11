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
  s_verbatim:       for S-grade products only — the Nutrition-APPROVED verbatim
                    Hebrew (insight line + S paragraph). Author may NOT paraphrase.
                    Loaded from s_verbatim/<category-slug>.json (per-category file).
                    If no file exists for this category, s_verbatim is never attached.

  v3 additions (TASK-262 / P43):
  bari_interpretation_inputs: list of {key, label, score, strength} from the
                    page's bariInterpretation (already deterministic; author reads
                    these to write each interpretation sentence).
  best_use_cases_pending: boolean — True when the page carries PENDING_COPY for
                    bestUseCases (author must fill); False = already deterministic.

stdlib only. No network. No OFF. null stays null.

--- TASK-553 changes (2026-07-11) ---

Fix 1: Superlative margin gate (superlatives_allowed_policy_v1.md rule 3).
  superlatives_for() now enforces all 5 policy conditions:
    1. Uniqueness — already enforced (is_unique_extreme).
    2. Corpus n >= 12 — now enforced.
    3. Margin >= 10% of corpus range over 2nd place — now enforced (margin_gate).
    4. Null-awareness — enforced in superlatives_context_for (RT-6 fix, TASK-550).
    5. Driver relevance — core metrics (protein/energyKcal/sugar) are always
       eligible (current whitelist); all other metrics are excluded by omission.
       Sodium exclusion is explicit (Nutrition Agent ruling, TASK-550, 2026-07-10).
       NOTE: Rule 5 "tier 2" (non-core metrics must appear in the product's fired
       driver chain) cannot be applied here to EXTEND the whitelist — the current
       whitelist covers core metrics only and tier-2 non-core tokens are never
       minted anyway. If the whitelist is ever extended to include e.g. fiber, the
       driver-chain check must be added at that time. Flagged here as an explicit
       code comment so it is not silently skipped.

Fix 2: De-hardcode S_VERBATIM (uniform-baseline doctrine, TASK-553).
  The module-level S_VERBATIM global (hardcoded with yogurt barcodes/text) is
  REMOVED. Approved S-grade verbatim copy is now loaded from per-category JSON
  files under s_verbatim/<category-slug>.json (same directory as this script).
  s_products in _meta is derived from the run's actual products whose grade == "S"
  (read from the page JSON), not from the keys of any hardcoded dict.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# S-verbatim loader (TASK-553 Fix 2)
# ---------------------------------------------------------------------------
# Per-category approved S-grade copy lives in s_verbatim/<category-slug>.json
# in the same directory as this script. Format:
#   { "<barcode>": { "insightLine": "...", "s_grade_explanation": "..." }, ... }
# The file is ONLY loaded when the category slug matches. If no file exists for
# the current category, the dict is empty and no s_verbatim field is attached.
#
# NOTE: this file must be created/updated by the Nutrition Agent approval process
# whenever a new category earns S-grade products. The barcode keys are the
# authoritative list of products whose verbatim copy is approved — NOT an
# authoritative list of which products are S-grade (that is derived from the page
# JSON's grade field). If a barcode is in the page as grade=S but has no entry
# in this file, it gets no s_verbatim (the author writes normal copy for it and
# the MISSING entry should be escalated).

_S_VERBATIM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "s_verbatim")


def _load_s_verbatim(category: str | None) -> dict:
    """Load Nutrition-approved S-grade verbatim copy for this category.

    Returns a dict keyed by barcode string (may be empty if no approved file
    exists for this category). Never raises — missing file → empty dict.
    """
    if not category:
        return {}
    slug = category  # e.g. "yogurt-spoonable"
    path = os.path.join(_S_VERBATIM_DIR, f"{slug}.json")
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # Strip metadata keys (prefixed with "_") — they are not barcode entries
    return {k: v for k, v in data.items() if not k.startswith("_")}


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

    Enforces superlatives_allowed_policy_v1.md (TASK-553 Fix 1, 2026-07-11):

    Rule 1 — Uniqueness: product's value equals the corpus extreme AND no other
      product ties it. Ties grant nothing. (is_unique_extreme, existing gate.)

    Rule 2 — Minimum corpus n >= 12: below 12 non-null observations the token
      is withheld regardless. (Now enforced; was previously un-coded.)

    Rule 3 — Margin >= 10% of corpus range over 2nd place: the gap between the
      extreme and the next-closest value must be >= (max - min) * 0.10.
      This is the guard against a 0.1g gap minting a superlative. If the corpus
      range is 0 (all products identical), no token is granted. (Now enforced;
      was previously un-coded — this is the fix that revokes rice-apple's
      lowest_sugar.)

    Rule 4 — Null-awareness: enforced downstream in superlatives_context_for()
      which attaches n_measured / phrase_as_among_measured to every token.
      No action needed in this function.

    Rule 5 — Driver relevance:
      Tier 1 (core consumer-priority metrics): protein, energyKcal, sugar are
        ALWAYS eligible — they are universally understood shopping priorities.
        These are the only metrics in this whitelist.
      Tier 2 (every other metric): additionally requires the metric to appear in
        the product's fired driver chain (cap_rules / penalties_applied /
        lowest_dimension). Sodium and other non-core metrics are NOT in the
        whitelist here. If the whitelist is ever extended (e.g. to include fiber),
        the caller MUST pass the product's trace and add a driver-chain check here.
        CANNOT-COMPUTE note: adding a tier-2 non-core token is currently impossible
        without passing the trace to this function (not on the current call site
        signature). The restriction is enforced by omission from the whitelist.
      Sodium is explicitly excluded (Nutrition Agent ruling, TASK-550, 2026-07-10):
        sodium superlatives are decorative (not a fired scoring driver in any
        current category run) and must not be minted. See
        01_framework/editorial/superlatives_allowed_policy_v1.md.

    CANNOT-COMPUTE conditions (must be noted explicitly per TASK-553 spec):
      - Rule 5 tier-2 driver-chain check for non-core metrics: requires the BSIP2
        trace to be passed to this function. Currently unsupported because: (a) no
        non-core metric is in the whitelist today, so the check is vacuously
        satisfied by omission; (b) adding it requires a signature change AND passing
        the trace. Flagged here so it is not silently skipped if the whitelist grows.
    """
    nut = product.get("expansion", {}).get("nutrition") or {}
    granted = []

    def is_unique_extreme(metric: str, want_max: bool) -> bool:
        """Rule 1: product is the sole corpus extreme for this metric."""
        v = nut.get(metric)
        if v is None or stats[metric]["n"] == 0:
            return False
        extreme = stats[metric]["max"] if want_max else stats[metric]["min"]
        if abs(v - extreme) > 1e-9:
            return False
        count = sum(
            1
            for p in stats["_products"]
            if (p.get("expansion", {}).get("nutrition") or {}).get(metric) is not None
            and abs((p.get("expansion", {}).get("nutrition") or {}).get(metric) - extreme) <= 1e-9
        )
        return count == 1

    def passes_n_gate(metric: str) -> bool:
        """Rule 2: at least 12 non-null observations in the corpus."""
        return stats[metric]["n"] >= 12

    def passes_margin_gate(metric: str, want_max: bool) -> bool:
        """Rule 3: gap to 2nd place >= 10% of corpus range (max - min).

        Collects all non-null values for the metric, sorts them, and checks that
        the gap from the extreme to the next-closest value clears the threshold.
        If the corpus range is 0 (all values identical), returns False — a
        superlative on a perfectly flat metric is always spurious.
        """
        corpus_stats = stats[metric]
        cmin = corpus_stats["min"]
        cmax = corpus_stats["max"]
        if cmin is None or cmax is None:
            return False
        corpus_range = cmax - cmin
        if corpus_range < 1e-9:
            # All values identical — no meaningful superlative
            return False
        threshold = corpus_range * 0.10

        # Collect sorted non-null values for this metric
        all_vals = sorted(
            v
            for p in stats["_products"]
            for v in [(p.get("expansion", {}).get("nutrition") or {}).get(metric)]
            if v is not None
        )
        if len(all_vals) < 2:
            return False

        if want_max:
            # gap from maximum down to second-highest
            margin = all_vals[-1] - all_vals[-2]
        else:
            # gap from minimum up to second-lowest
            margin = all_vals[1] - all_vals[0]

        return margin >= threshold

    def token_granted(metric: str, want_max: bool) -> bool:
        """Apply rules 1–3 (rule 4 is downstream; rule 5 by whitelist)."""
        return (
            is_unique_extreme(metric, want_max)
            and passes_n_gate(metric)
            and passes_margin_gate(metric, want_max)
        )

    if token_granted("protein", want_max=True):
        granted.append("highest_protein")
    if token_granted("energyKcal", want_max=False):
        granted.append("lowest_kcal")
    if token_granted("sugar", want_max=False):
        granted.append("lowest_sugar")
    return granted


def superlatives_context_for(granted_tokens, stats):
    """RT-6 fix: for each granted token, carry the TRUE denominator the
    author must cite. When the underlying metric has nulls in the corpus
    (n < total product_count), a superlative MUST be phrased "among N
    measured" — never implied across the full displayed set. This removes
    the ambiguity that let rice-apple's copy claim "among all 20 tested"
    for a sugar metric that only 19/20 products carry.
    """
    metric_for_token = {
        "highest_protein": "protein",
        "lowest_kcal": "energyKcal",
        "lowest_sugar": "sugar",
    }
    ctx = {}
    for tok in granted_tokens:
        metric = metric_for_token.get(tok)
        if metric and metric in stats:
            ctx[tok] = {
                "n_measured": stats[metric]["n"],
                "phrase_as_among_measured": stats[metric]["n"] < stats.get("_product_count", stats[metric]["n"]),
            }
    return ctx


def main():
    ap = argparse.ArgumentParser(description="Build copy fact sheets (Part 1).")
    ap.add_argument("--config", required=True)
    ap.add_argument("--page", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    config = load_json(args.config)
    page = load_json(args.page)
    run_dir = config["run_products_dir"]
    category = config.get("category")

    # TASK-553 Fix 2: load per-category S-verbatim approved copy.
    # This replaces the former module-level S_VERBATIM global (which was
    # hardcoded with yogurt barcodes and leaked into every category's _meta).
    s_verbatim = _load_s_verbatim(category)

    products = page["products"]
    stats = compute_corpus_stats(products)
    stats["_products"] = products  # internal handle for uniqueness/margin checks
    stats["_product_count"] = len(products)

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

        # Compute superlatives once (avoid double-call on lines 369-370)
        sup_allowed = superlatives_for(p, stats)
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
            "superlatives_allowed": sup_allowed,
            "superlatives_context": superlatives_context_for(sup_allowed, stats),
            # v3 additions
            "bari_interpretation_inputs": bari_interp_inputs,
            "best_use_cases_pending": best_use_cases_pending,
            "best_use_cases_deterministic": [] if best_use_cases_pending else list(best_uc),
        }
        # TASK-553 Fix 2: s_verbatim from per-category file, not a shared global.
        # A missing entry for an S-grade product is intentional — the author writes
        # normal copy; the absence should be escalated to the Nutrition Agent.
        if bc in s_verbatim:
            sheet["s_verbatim"] = s_verbatim[bc]
        sheets.append(sheet)

    del stats["_products"]
    del stats["_product_count"]

    # TASK-553 Fix 2: derive s_products from THIS run's actual grade==S products
    # (read from page JSON). Do NOT derive from s_verbatim keys — the verbatim
    # file is the approved-copy registry, not the grade authority. A product can
    # be S-grade without yet having approved verbatim copy (escalation required).
    s_products_in_run = [
        s["barcode"] for s in sheets if s.get("grade") == "S"
    ]

    out = {
        "_meta": {
            "category": category,
            "page_source": os.path.abspath(args.page),
            "config_source": os.path.abspath(args.config),
            "product_count": len(sheets),
            "corpus_stats": stats,
            "ambiguous_drivers": ambiguous,
            "s_products": s_products_in_run,
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
    s_missing_verbatim = [
        bc for bc in s_products_in_run if bc not in s_verbatim
    ]
    if s_missing_verbatim:
        print(f"WARNING: {len(s_missing_verbatim)} S-grade product(s) have no approved verbatim copy:")
        for bc in s_missing_verbatim:
            print(f"  - {bc} (escalate to Nutrition Agent for s_verbatim/{category}.json)")


if __name__ == "__main__":
    main()
