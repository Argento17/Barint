# P121 Return — TASK-278 Phase-8: hard_cheeses × sat_fat D6 Enrollment Proposal

**Agent:** Nutrition Agent
**Date:** 2026-06-14
**Task:** TASK-278
**Phase:** Phase-8 hard_cheeses×sat_fat D6 enrollment proposal

---

## Summary

D6 proposal created for hard_cheeses × sat_fat shelf-relative enrollment. Two critical findings
that differ from the cheese_spreads Phase-7 template:

1. **Router heterogeneity**: 11/37 corpus products (29.7%) misroute to `dessert` (genuine hard
   cheeses with NOVA 1 that the router fires "מוס" signal on). SR cannot fix router errors. Scope
   must restrict to `dairy_protein`-routed products only.

2. **Tight cluster problem**: Within the recommended Scope A (yellow+yellow_light+hard_grating,
   n=22), the yellow cluster is extremely tight (17.5–19.5g sat_fat). IQR=1.5g → IQR/1.349=1.11 →
   robust_scale hits the minimum floor at 1.40. The mechanism primarily differentiates the outlier
   reduced-fat variants (5–10g, getting +3 relief) from the tight full-fat cluster. This is a D7
   scale adequacy question.

---

## Return Block (machine-readable)

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-8 hard_cheeses×sat_fat D6 enrollment proposal",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "nutrition-agent",
  "authoritative_run": "02_products/hard_cheeses/bsip2_outputs/run_hard_cheeses_001",
  "n_products_total": 37,
  "n_products_with_satfat": 37,
  "router_category": "dairy_protein (25/37 correctly routed; 11/37 misroute to dessert; 1 to whole_food_fat)",
  "scope_guard_type": "subtype_guard (bsip_cheese_subpool in HARD_CHEESE_YELLOW_SUBPOOLS)",
  "scope_guard_field": "bsip_cheese_subpool (from BSIP1 input, same mechanism as brined EV-055)",
  "scope_guard_values": ["yellow", "yellow_light", "hard_grating"],
  "recommended_scope_n": 22,
  "shelf_stats": {
    "scope": "yellow+yellow_light+hard_grating (n=22)",
    "n": 22,
    "median": 18.0,
    "q1": 17.5,
    "q3": 19.0,
    "iqr": 1.50,
    "mad": 0.50,
    "iqr_scaled": 1.1119,
    "mad_scaled": 0.7413,
    "min_scale_floor": 1.4,
    "robust_scale": 1.4000,
    "primary": "at_floor (IQR/1.349=1.11 < floor=1.4)",
    "min": 5.0,
    "max": 21.0,
    "stdev": 4.8269,
    "near_median_dead_pct": 31.8,
    "alt_full_corpus_n37": {
      "n": 37, "median": 17.5, "q1": 10.0, "q3": 18.0, "iqr": 8.0,
      "robust_scale": 5.9303, "primary": "IQR"
    }
  },
  "band_design": {
    "p_max": 6,
    "b_max": 3,
    "floor": 62,
    "floor_threshold_g": 19.0,
    "near_median_z_threshold": 0.3,
    "direction": "asymmetric",
    "normalize_distance": true
  },
  "anti_immunity_proof": "floor(62) + B_max(3) = 65 < 70 (grade B threshold) PASS",
  "named_inversions": [
    {
      "id": "INV-1",
      "note": "Same-side inversion (both below median): A gets +3 relief, B gets +1 — gap narrows",
      "barcode_A": "7290000062426",
      "name_A": "עמק צהוב 9% מופחת שומן",
      "sat_fat_A": 5.5,
      "score_A": 64.3,
      "grade_A": "C",
      "median_side_A": "BELOW median (18.0g) — z=-8.93, r_below=8.93 → delta=+3",
      "barcode_B": "7290000062433",
      "name_B": "עמק גאודה שנה 28%",
      "sat_fat_B": 17.5,
      "score_B": 77.6,
      "grade_B": "B",
      "median_side_B": "BELOW median (18.0g) — z=-0.357, r_below=0.357 → delta=+1",
      "gap_before": 13.3,
      "delta_A": 3,
      "delta_B": 1,
      "gap_after": 11.3,
      "gap_narrowed_by": 2.0
    },
    {
      "id": "INV-2",
      "note": "Opposite-side inversion: A below median gets +3, B above median gets -2 — gap nearly closes",
      "barcode_A": "7290000062426",
      "name_A": "עמק צהוב 9% מופחת שומן",
      "sat_fat_A": 5.5,
      "score_A": 64.3,
      "grade_A": "C",
      "median_side_A": "BELOW median (18.0g) — z=-8.93, r_below=8.93 → delta=+3",
      "barcode_B": "8866972",
      "name_B": "גבינה גרוויר 31%",
      "sat_fat_B": 19.5,
      "score_B": 69.9,
      "grade_B": "B",
      "median_side_B": "ABOVE median (18.0g) — z=+1.071, r_above=1.071 → delta=-2",
      "gap_before": 5.6,
      "delta_A": 3,
      "delta_B": -2,
      "gap_after": 0.6,
      "gap_narrowed_by": 5.0
    }
  ],
  "next_ev_number": "EV-090 (not yet registered — D7 + orchestrator register after acceptance)",
  "d7_open_questions": [
    "Q1 (CRITICAL): Scope guard — Option A (yellow+yellow_light+hard_grating, n=22, scale=1.4) vs Option B (full corpus n=37, scale=5.93). Nutrition Agent recommends Option A (coherent peer group) but flags that scale hits floor and mechanism primarily differentiates outlier reduced-fat products",
    "Q2 (CRITICAL): Scale adequacy — robust_scale=1.40 is at the minimum floor. Does this justify enrollment cost? SR primarily gives +3 relief to yellow_light outliers (5-10g sat_fat), modest ±1 to the tight yellow cluster. Product Agent must assess if this is meaningful differentiation",
    "Q3: Misrouted products — 11/37 hard cheeses route to 'dessert' (category instability). Should router correction precede SR enrollment, or does enrollment proceed for dairy_protein-routed products only?",
    "Q4: Floor threshold — Q3=19.0g (statistical, recommended) vs 15.0g (Israeli red-label regulatory threshold, deprecated per redlabel-de-anchor directive). Q3=19.0g recommended",
    "Q5: FAT_QUALITY_FAMILY_BUDGET raise — prior enrollments (cereals, yogurt, cheese_spreads) did not raise the budget. With sat_fat as the dominant fat signal for hard cheeses, verify SR penalty is not absorbed into existing budget cap at pilot"
  ],
  "enrollment_doc_path": "02_products/hard_cheeses/methodology/shelf_relative_satfat_enrollment_hardcheeses_v1.md",
  "engine_invariants": "PASS — no engine edits (constants.py and score_engine.py both unchanged)",
  "off_used": false,
  "not_done": [
    "D7 co-sign from Product Agent (required before any pilot or constants.py edit)",
    "EV-090 registration in evidence registry (held pending D7)",
    "Constants HARD_CHEESE_YELLOW_SUBPOOLS + FATSAT_SHELF_REL_HARDCHEESE_* in constants.py (post-D7)",
    "Call site addition in score_engine.py (post-D7)",
    "Pilot run to verify gap-narrowing empirically",
    "Router correction for 11 misrouted hard cheese products (separate task, not blocked by this D6)"
  ]
}
```

## Machine-Readable Return Contract

```json
{
  "artifacts_claimed": [
    {
      "path": "02_products/hard_cheeses/methodology/shelf_relative_satfat_enrollment_hardcheeses_v1.md",
      "change": "created"
    },
    {
      "path": "tasks/returns/P121_return.md",
      "change": "created"
    }
  ],
  "counts": {
    "corpus_products_total": {"value": 37, "denominator": "run_hard_cheeses_001 trace files"},
    "products_with_satfat": {"value": 37, "denominator": "37 total (100% coverage)"},
    "scope_a_products": {"value": 22, "denominator": "yellow+yellow_light+hard_grating subpools"},
    "misrouted_to_dessert": {"value": 11, "denominator": "37 total corpus"},
    "correctly_routed_dairy_protein": {"value": 25, "denominator": "37 total corpus"},
    "named_inversions_valid": {"value": 2, "denominator": "opposite-side: 1 (INV-2); same-side: 1 (INV-1)"},
    "d7_open_questions": {"value": 5, "denominator": "Q1-Q5 as listed"}
  },
  "commands_run": [
    {"cmd": "python3 tmp_stats.py", "exit_code": 0, "purpose": "sat_fat statistics + inversion search"},
    {"cmd": "python3 -c [glob+json corpus reader]", "exit_code": 0, "purpose": "extract sat_fat/category/score from all 37 traces"},
    {"cmd": "python3 -c [bsip1 subpool reader]", "exit_code": 0, "purpose": "identify subpool distribution and field availability"}
  ],
  "spec_conflicts_flagged": [
    "SC-1: scope guard uses bsip_cheese_subpool (not category_subtype) — different from EV-089 pattern",
    "SC-2: rollout_spread_analysis used full corpus (n=37, scale=5.93); this D6 recommends Scope A (n=22, scale=1.4) — scope reduction from analysis reference",
    "SC-3: 11/37 products misrouted to 'dessert' — SR cannot address routing errors; router fix is a separate prerequisite"
  ],
  "acceptance_test": "WOULD_PASS if: (a) enrollment doc exists at stated path (verified), (b) no engine edits (verified), (c) EV-090 not yet registered (verified), (d) named inversions have explicit above/below-median annotation (INV-2 is opposite-side; INV-1 is same-side with explicit annotation), (e) Anti-Immunity: 62+3=65<70 PASS",
  "propose": "RETURNED"
}
```
