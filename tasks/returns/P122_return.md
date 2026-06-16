# P122 Return — TASK-278 Phase-8: hard_cheeses × sat_fat D7 Co-Sign

**Agent:** Product Agent
**Date:** 2026-06-14
**Task:** TASK-278
**Phase:** Phase-8 hard_cheeses×sat_fat D7 co-sign
**Verdict:** CO-SIGN APPROVED WITH CONDITIONS

---

## Summary

D7 co-sign approved for hard_cheeses × sat_fat shelf-relative enrollment.

All 5 D6 open questions resolved. EV-090 registered. 11-criterion pilot gate locked.

Key decisions:
- Q1 (scope): Option A approved — Scope A (n=22, yellow+yellow_light+hard_grating, scale=1.40).
  Full corpus (Option B) rejected: scale=5.93 is cross-group ecological variation, not
  within-shelf quality variation — same reasoning as Phase-7 rejection of whole-corpus dairy_protein.
- Q2 (scale adequacy): Enroll at scale=1.40 (at minimum floor). Tight scale is an honest finding
  about the homogeneous yellow cheese shelf. 4 yellow_light outliers get genuine +3 relief.
  Phase-7 precedent (accepted tight scale as correct behavior) applies. Limitation acknowledged
  in Section 2 of co-sign doc.
- Q3 (router sequencing): Proceed. Router fix is orthogonal to SR scope — subpool guard already
  correctly excludes 11 misrouted products.
- Q4 (floor threshold): 19.0g (Q3-based). Red-label 15g threshold rejected per de-anchor directive.
- Q5 (budget): No raise. Trace bc=7290000062426 confirms fat_quality.coordinated_penalty=0.0,
  binding_cap=null. FAT_QUALITY_FAMILY_BUDGET=8 is non-binding.

Critical new pilot criteria: C10b (cheese_spread scope isolation) and C10c (yogurt scope isolation)
are NEW for Phase-8 — required because this adds a third call site in dairy_protein.

Critical Data Agent pre-check: confirm `bsip_cheese_subpool` is accessible at scoring time via
`nn.get("bsip_cheese_subpool")` before any wiring. This field mechanism differs from yogurt
and cheese_spreads (which use category_subtype).

---

## Decisions

| Q | Decision | Option | Decisive reason | Reversal condition |
|---|---|---|---|---|
| Q1 — Scope | Scope A (n=22) | A | Full corpus scale driven by cross-group ecological variation (bulgarians at 2.5g vs yellow at 19g), not within-shelf quality signal; same reasoning Phase-7 applied to reject whole-corpus dairy_protein | Reassess if n≥30 and IQR>3g after router correction |
| Q2 — Scale | Enroll at 1.40 | A | 4 yellow_light outliers get genuine +3 relief; Phase-7 precedent accepted tight scale; router fix timeline unknown and orthogonal | Defer if pilot C4 fails (<5 movers) |
| Q3 — Router | Proceed | proceed | Subpool guard already excludes 11 misrouted products; SR cannot interact with router errors | None |
| Q4 — Floor | 19.0g (Q3) | a | Red-label de-anchor directive; 15g would floor 59% of scope (overbuilding) | Lower if 15–19g products exceed score 62 at pilot |
| Q5 — Budget | No raise | no raise | Trace confirms fat_quality.binding_cap=null, coordinated_penalty=0.0 | Raise by 6 if pilot shows absorption |

---

## Anti-Immunity Proof

floor(62) + B_max(3) = 65 < 70 (grade B threshold) **PASS**

Structural double-protection: products at or above floor_threshold_g (19.0g sat_fat) are above
the median (18.0g) → surcharge zone → cannot receive B_max relief → floor+relief scenario
structurally impossible for the protected cohort.

---

## Pilot Gate (11 Criteria — Locked)

All hard criteria must pass before Phase-8 wire+pilot results accepted. C11 = docs only.

| # | Name | Pass condition | Class |
|---|---|---|---|
| C1 | directional_distribution | Mean delta above-median scope products ≤ 0 AND below-median ≥ 0 | Hard |
| C2 | grade_dist_and_magnitude | (A) 0 scope products with sat_fat≥19.0g at B; (B) ≥1 scope product sat_fat≤10g at C or better; (C) mean |clean_delta|≥0.5 among SR-firing scope products | Hard |
| C3 | gap_narrows_inversion | INV-1: |7290000062426 − 7290000062433| flag_on < flag_off (expect 11.3 < 13.3); INV-2: |7290000062426 − 8866972| flag_on < flag_off (expect 0.6 < 5.6) | Hard |
| C4 | min_movers | ≥5 HARD_CHEESE_YELLOW_SUBPOOLS products with clean_delta ≠ 0 | Hard |
| C5 | min_grade_changes | ≥1 scope product grade change at flag-on | Hard |
| C6 | max_absorption | ≤40% of SR-firing scope products show clean_delta=0 despite non-zero SR term | Hard |
| C7 | anti_immunity | 0 scope products with sat_fat≥19.0g reach grade B (score≥70) at flag-on | Hard |
| C8 | floor_compliance | All scope products with sat_fat≥19.0g: flag-on score ≤62 | Hard |
| C9 | no_scope_bleed | 0 non-HARD_CHEESE_YELLOW_SUBPOOLS dairy_protein products with non-zero clean_delta from hard_cheese SR branch | Hard |
| C10 | frozen_byte_id_milk | All milk run_005_headpin products (20): clean_delta=0.0 at flag-on | Hard — CRITICAL |
| C10b | cheese_spread_byte_id | All CREAM_CHEESE_SPREAD_SUBTYPES products: clean_delta=0.0 from hard_cheese SR branch (NEW — third call site in dairy_protein) | Hard — NEW |
| C10c | yogurt_byte_id | All CULTURED_YOGURT_SUBTYPES products: clean_delta=0.0 from hard_cheese SR branch (NEW — third call site in dairy_protein) | Hard — NEW |
| C11 | flag_off_drift | Flag-off scores for 22 scope products match run_hard_cheeses_001 baseline within ±5pts | Docs only |

---

## Return Block (machine-readable)

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-8 hard_cheeses×sat_fat D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "q1_decision": "Option A",
  "q1_scope_n": 22,
  "q1_scale": 1.40,
  "q2_decision": "Option A (enroll)",
  "q2_scale_adequacy": "accepted — tight scale is honest finding about homogeneous yellow cheese shelf; 4 yellow_light outliers get meaningful +3 relief",
  "q3_decision": "proceed",
  "q4_floor_threshold_g": 19.0,
  "q4_rationale": "Q3-based; red-label 15g threshold rejected per de-anchor directive; 15g would floor 59% of scope",
  "q5_budget_raise": "no raise",
  "q5_evidence": "bc=7290000062426 trace: fat_quality.binding_cap=null, coordinated_penalty=0.0",
  "ev090_registered": true,
  "ev090_line": 2192,
  "pilot_gate_criteria_count": 11,
  "pilot_gate_criteria": ["C1_directional_distribution", "C2_grade_dist_and_magnitude", "C3_gap_narrows_inversion", "C4_min_movers", "C5_min_grade_changes", "C6_max_absorption", "C7_anti_immunity", "C8_floor_compliance", "C9_no_scope_bleed", "C10_frozen_byte_id_milk", "C10b_cheese_spread_byte_id_NEW", "C10c_yogurt_byte_id_NEW", "C11_flag_off_drift_docs_only"],
  "anti_immunity_proof": "floor(62) + B_max(3) = 65 < 70 PASS",
  "d7_cosign_doc": "02_products/hard_cheeses/methodology/hard_cheeses_satfat_d7_cosign_v1.md",
  "data_agent_precheck": "Verify bsip_cheese_subpool accessible via nn.get('bsip_cheese_subpool') at scoring time before wiring",
  "off_used": false,
  "tripwire_assessment": "No tripwire fires — flag default=off, zero score movement, internal pilot, no published changes, within approved TASK-278 program",
  "not_done": [
    "Data Agent pre-implementation check: verify bsip_cheese_subpool accessible in nn dict at scoring time",
    "Phase-8 wire+pilot rescore by Data Agent (P123 or equivalent)",
    "Router correction for 11 misrouted hard cheese products (separate task, does not gate this enrollment)",
    "Owner go-live gate before any published score movement"
  ]
}
```

---

## Machine-Readable Return Contract

```json
{
  "artifacts_claimed": [
    {
      "path": "02_products/hard_cheeses/methodology/hard_cheeses_satfat_d7_cosign_v1.md",
      "change": "created"
    },
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "change": "EV-090 appended at line 2192"
    },
    {
      "path": "tasks/returns/P122_return.md",
      "change": "created"
    }
  ],
  "counts": {
    "q_decisions_resolved": {"value": 5, "denominator": "Q1–Q5 as listed in D6"},
    "pilot_gate_criteria": {"value": 11, "denominator": "C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C10b C10c C11"},
    "new_gate_criteria_vs_phase7": {"value": 2, "denominator": "C10b C10c (third dairy_protein call site isolation)"},
    "ev090_registered": {"value": 1, "denominator": "EV-090 at line 2192"},
    "engine_files_modified": {"value": 0, "denominator": "constants.py, score_engine.py — no changes in D7 phase"},
    "score_movement": {"value": 0, "denominator": "all 37 corpus products — D7 phase"},
    "off_data_sources": {"value": 0, "denominator": "all stats from L1_observed_signals in run_hard_cheeses_001 trace files"}
  },
  "commands_run": [
    {"cmd": "Read bsip2_trace.json for bc=7290000062426 (fat_quality budget check)", "exit_code": 0, "purpose": "Q5 — verify FAT_QUALITY_FAMILY_BUDGET non-binding; confirmed fat_quality.binding_cap=null, coordinated_penalty=0.0"},
    {"cmd": "Grep EV-090 in evidence_registry", "exit_code": 0, "purpose": "confirm EV-090 slot was free before registration; result: no matches (free)"},
    {"cmd": "Grep EV-090 after append", "exit_code": 0, "purpose": "confirm registration at line 2192"}
  ],
  "spec_conflicts_flagged": [
    "SC-1 (inherited from D6): scope guard uses bsip_cheese_subpool (BSIP1 field) not category_subtype (router field) — different from EV-088/EV-089 pattern; Data Agent must verify field accessibility in nn dict before wiring",
    "SC-2 (inherited from D6): scope reduction from rollout_spread_analysis (n=37, scale=5.93) to Scope A (n=22, scale=1.40) — resolved: coherent peer group is the correct calibration; Option B cross-group variation is not SR signal"
  ],
  "acceptance_test": "PASS — (a) co-sign doc exists at stated path; (b) no engine edits; (c) EV-090 registered at line 2192; (d) named inversions both show explicit gap-narrowing with stated expected values; (e) Anti-Immunity: 62+3=65<70 PASS; (f) pilot gate has 11 criteria including 3 scope-bleed criteria for the third dairy_protein call site",
  "propose": "RETURNED"
}
```
