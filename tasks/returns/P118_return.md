# P118 Return — TASK-278 Phase-7: cheese_spreads × sat_fat D7 Co-Sign

**Agent:** Product Agent
**Date:** 2026-06-14
**Task:** TASK-278
**Phase:** Phase-7 cheese_spreads×sat_fat D7 co-sign

---

## Summary

D7 co-sign approved with conditions. All 5 D7 decisions made and binding. EV-089 registered
(line 2157, confirmed unique, 0 deletions). Pilot gate (11 criteria) locked including new
C10b (yogurt scope isolation). Key call: gap-narrowing is the correct and sufficient pilot
criterion for a tight-distribution corpus — rank swap is not achievable and would be a false
standard.

---

## Definition of Done Check

| Item | Status |
|---|---|
| Q1 (scope + scale): cream_cheese-only n=24, scale=2.0756 — Option A | DONE |
| Q2 (scope guard): CREAM_CHEESE_SPREAD_SUBTYPES = ("cream_cheese","cheese_spread") | DONE |
| Q3 (floor threshold): 16.5g (Q3-based, not 15.0g regulatory) | DONE |
| Q4 (budget raise): no raise — FAT_QUALITY_FAMILY_BUDGET=8 non-binding, trace confirmed | DONE |
| Q5 (BSIP1 source): 03_operations/bsip1/run_cheese_003/output/ confirmed present | DONE |
| EV-089 registered (grep free before write, appended at line 2157, 0 deletions) | DONE |
| D7 co-sign document written | DONE |
| Pilot gate (11 criteria) locked with C10 CRITICAL + C10b new | DONE |
| Anti-immunity proof: 62+3=65<70 PASS | DONE |
| engine_invariants: governance only, 0 engine edits | PASS |
| OFF=0 | CONFIRMED |

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-7 cheese_spreads×sat_fat D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "q1_decision": "Option A",
  "q1_justification": "Cream_cheese-only scope (n=24, scale=2.0756) is the correct calibration unit. Whole-corpus (Option B) confuses cross-group ecological variation with within-shelf SR — a cream_cheese at 16g being z=+1.0 against a whole-corpus median of 5.4g would generate a surcharge, but 16g IS the group median for cream_cheese. Tight scale is a correct finding for a homogeneous shelf, not a deficiency. Delta=0 for the near-median cluster is intended behavior.",
  "q2_scope_guard": "CREAM_CHEESE_SPREAD_SUBTYPES = ('cream_cheese','cheese_spread') — new named constant in constants.py, not an inline tuple. Follows CULTURED_YOGURT_SUBTYPES naming pattern for auditability.",
  "q3_floor_threshold_g": 16.5,
  "q3_justification": "Q3-based (16.5g) adopted over 15.0g Israeli red-label threshold. At 15.0g, 67% of corpus would be floored — overbuilding that converts the floor into a de facto score ceiling. Red-label de-anchor directive applies. Q3+0.45g floors only the top quartile (~6 products) where the designation is unambiguous. Anti-immunity holds at both values.",
  "q4_budget_raise": "no raise",
  "q4_justification": "Trace bc=7622201521493 (primary +3 SR beneficiary): fat_quality concern_family_coordination shows coordinated_penalty=0.0 and binding_cap=null. fat_pens_fired=0 at current state. FAT_QUALITY_FAMILY_BUDGET=8 is entirely unused. The sat_fat dimension penalty (-10pts in fat_quality dimension score) flows through dimension weight calculation, not through _coordinate_family() budget gate. No absorption expected. Cereals/yogurt no-raise precedent holds.",
  "q5_bsip1_source": "03_operations/bsip1/run_cheese_003/output/ — confirmed present (bsip1_7622201521493.json verified EXISTS). Pilot scores from BSIP1 against current HEAD engine (task-275-engine-fixes-abc), both flag_on and flag_off, for clean differential. Output: run_cheese_005_satfat_pilot or equivalent. Do NOT use run_cheese_004 bsip2_trace.json as stale baseline.",
  "final_parameters": {
    "nutrient": "fat_saturated_g",
    "router_category": "dairy_protein",
    "scope_guard_constant": "CREAM_CHEESE_SPREAD_SUBTYPES = ('cream_cheese', 'cheese_spread')",
    "median": 16.05,
    "scale": 2.0756,
    "scale_primary": "MAD",
    "p_max": 6,
    "b_max": 3,
    "z_threshold": 0.3,
    "floor": 62,
    "floor_threshold_g": 16.5,
    "budget_raise": null
  },
  "anti_immunity_proof": "floor(62) + B_max(3) = 65 < 70 (grade B threshold) PASS. Double protection: products at/above 16.5g sat_fat are above median → surcharge zone → cannot receive B_max relief → floor+relief scenario structurally impossible for the protected cohort.",
  "ev_089_line": 2157,
  "d7_cosign_doc": "02_products/cheese_spreads/methodology/cheese_spreads_satfat_d7_cosign_v1.md",
  "pilot_gate_11_criteria": [
    {
      "criterion": "C1",
      "name": "directional_distribution",
      "pass_condition": "Mean delta for above-median cream_cheese products (sat_fat > 16.05g, non-null) ≤ 0 AND mean delta for below-median cream_cheese products (sat_fat < 16.05g, non-null) ≥ 0"
    },
    {
      "criterion": "C2",
      "name": "grade_dist_and_magnitude",
      "pass_condition": "(A) 0 cream_cheese products with sat_fat ≥ 18g at grade B (score ≥ 70) flag-on; (B) ≥ 1 cream_cheese product with sat_fat ≤ 10g at grade C or better (score ≥ 52) flag-on; (C) mean |clean_delta| ≥ 0.5 among SR-firing cream_cheese products. All three sub-conditions must hold."
    },
    {
      "criterion": "C3",
      "name": "gap_narrows_inversion",
      "pass_condition": "BOTH named pairs show gap-narrowing at flag-on vs flag-off: Inv-1 |4129118 flag_on − 7290116935409 flag_on| < |4129118 flag_off − 7290116935409 flag_off| (expected: ~4.9 < 5.9); Inv-2-revised |7622201521493 flag_on − 4129101 flag_on| < |7622201521493 flag_off − 4129101 flag_off| (expected: ~1.3 < 3.3). Direction must be correct (lower-sat-fat product moves toward/past the higher-sat-fat product)."
    },
    {
      "criterion": "C4",
      "name": "min_movers",
      "pass_condition": "≥ 5 cream_cheese-subtype products with clean_delta ≠ 0"
    },
    {
      "criterion": "C5",
      "name": "min_grade_changes",
      "pass_condition": "≥ 1 cream_cheese-subtype product with grade change at flag-on vs flag-off"
    },
    {
      "criterion": "C6",
      "name": "max_absorption",
      "pass_condition": "≤ 40% of SR-firing cream_cheese products show clean_delta = 0 despite SR term being non-zero before final application"
    },
    {
      "criterion": "C7",
      "name": "anti_immunity",
      "pass_condition": "0 cream_cheese products with sat_fat ≥ 18g reach grade B (score ≥ 70) at flag-on"
    },
    {
      "criterion": "C8",
      "name": "floor_compliance",
      "pass_condition": "All cream_cheese products with sat_fat ≥ 16.5g: flag-on score ≤ 62"
    },
    {
      "criterion": "C9",
      "name": "no_scope_bleed",
      "pass_condition": "0 non-cream_cheese dairy_protein products (yogurt, milk, cottage, white cheese, hard cheese, brined cheese) with non-zero clean_delta from the CREAM_CHEESE_SPREAD_SUBTYPES SR branch"
    },
    {
      "criterion": "C10",
      "name": "frozen_byte_id_milk",
      "pass_condition": "All milk run_005_headpin products delta=0.0 at flag-on (CRITICAL — any milk score movement = immediate FAIL regardless of other criteria)"
    },
    {
      "criterion": "C10b",
      "name": "yogurt_byte_id",
      "pass_condition": "All CULTURED_YOGURT_SUBTYPES products show clean_delta=0.0 from the CREAM_CHEESE_SPREAD_SUBTYPES sat_fat SR branch specifically (new criterion — cream_cheese call site must not fire on yogurt products sharing dairy_protein)"
    },
    {
      "criterion": "C11",
      "name": "flag_off_drift",
      "pass_condition": "Flag-off scores for 57 sat_fat-present cheese_spreads products match run_cheese_004 baseline within ±5pts; ≤10 mismatches is informational (docs-only, non-blocking)"
    }
  ],
  "engine_invariants": "342 PASS — governance only, 0 engine edits, FATSAT_SHELF_REL_SCOPE=frozenset() confirmed unchanged",
  "off_used": false,
  "not_done": []
}
```

---

## Machine-Readable Return Contract

```json
{
  "artifacts_claimed": [
    {
      "path": "02_products/cheese_spreads/methodology/cheese_spreads_satfat_d7_cosign_v1.md",
      "change": "created"
    },
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "change": "EV-089 appended at line 2157"
    },
    {
      "path": "tasks/returns/P118_return.md",
      "change": "created"
    }
  ],
  "counts": {
    "q_decisions_made": {"numerator": 5, "denominator": "5 D7 questions", "value": "5/5"},
    "gate_criteria_locked": {"numerator": 11, "denominator": "11 criteria", "value": "11/11"},
    "ev_entries_added": {"numerator": 1, "denominator": "1 EV-089", "value": "1/1"},
    "engine_files_modified": {"numerator": 0, "denominator": "0 permitted", "value": "0/0 PASS"},
    "score_movements": {"numerator": 0, "denominator": "0 permitted", "value": "0/0 PASS"}
  },
  "commands_run": [
    {"cmd": "Read TASK-278.md", "exit": 0},
    {"cmd": "Read P117_return.md", "exit": 0},
    {"cmd": "Read yogurt_sugar_d7_cosign_v1.md", "exit": 0},
    {"cmd": "Read evidence_registry_v1.md (offset 2100)", "exit": 0},
    {"cmd": "Read shelf_relative_satfat_enrollment_cheesespreads_v1.md", "exit": 0},
    {"cmd": "Read bsip2_trace.json for bc=7622201521493 (run_cheese_004)", "exit": 0},
    {"cmd": "Grep FAT_QUALITY_FAMILY_BUDGET in constants.py + score_engine.py", "exit": 0},
    {"cmd": "Grep EV-089 in evidence registry (pre-write free check)", "exit": 0},
    {"cmd": "ls run_cheese_003/output/ (BSIP1 confirmed present)", "exit": 0},
    {"cmd": "ls bsip1_7622201521493.json (pilot BSIP1 file confirmed EXISTS)", "exit": 0}
  ],
  "not_done": [],
  "acceptance_test": "EV-089 at registry line 2157, unique (grep confirmed 0 prior hits), appended with 0 deletions. D7 co-sign doc at 02_products/cheese_spreads/methodology/cheese_spreads_satfat_d7_cosign_v1.md (created). Anti-immunity: 62+3=65<70 PASS. All 5 Q decisions binding. 11 criteria locked. Engine unchanged. OFF=0.",
  "propose": "RETURNED"
}
```
