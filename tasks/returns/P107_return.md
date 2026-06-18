# P107 Return — TASK-278 Phase-4: Cereals × Sugar D7 Co-Sign

**Agent:** Product Agent
**Date:** 2026-06-14
**Status proposed:** RETURNED

---

## Summary

D7 co-sign for cereals × sugar shelf-relative enrollment is complete. All four tasks executed:
D6 spec validated, budget raise question resolved (Option A), pilot gate locked, EV-087 registered,
and `cereals_d7_cosign_v1.md` written. No engine files modified. No scores moved. OFF ban satisfied.

---

## D6 Validation Results

All four D6 elements confirmed:

**Scope — CONFIRMED.** `"cereal"` is the correct router key. All 45 corpus products carry
`category="cereal"` in traces (orchestrator-verified from run_cereals_synthesis_001). Dairy bleed
risk is NONE — the `DAIRY_HEAD_TERMS` suppression guard prevents dairy products from receiving
`category="cereal"`. Granola bar (`snack_bar_granola`) bleed risk is NONE — the router splits are
clean. This enrollment does not cover `snack_bar_granola` and creates no precedent for skipping
that category's future D7.

**Bands — CONFIRMED.** P=6 / B=3 (same r-unit structure as biscuits EV-085) is correct for the
larger scale (8.896g vs biscuits' 5.115g). The r-unit normalization is the right abstraction:
same breakpoints at different scales produce the correct raw-gram thresholds per shelf. P=6 fires
only at sugar ≥ 36.2g (r_above ≥ 2.5) for maximum penalty — appropriate for Frosties-type
products. Practical maximum relief in this corpus is 2pts (plain oats at 0.5g sugar → r_below=1.52
→ band [1.5,3.0]). B_max=3 is a theoretical ceiling structurally unreachable in this distribution
(requires sugar ≤ −12.7g). Asymmetry P>B confirmed.

**Floor — CONFIRMED.** `formulation_absolute_floor=62` at trigger `sugars_g ≥ 25g/100g` is the
correct calibration. Floor=55 (biscuits level) would be non-binding on cereals — current high-sugar
cereal scores are 30–52, already below 55. Floor=62 is the calibrated Anti-Immunity point: above
current corpus range, 8 points below grade B. Floor=65 is too close to grade B (2pt headroom).

**Anti-Immunity — CONFIRMED AND AIRTIGHT.** floor(62) + max_relief(3) = 65 < 70 (grade B).
Structural note: all products with sugar ≥ 25g are in the surcharge path (25g >> 14g median,
r_above = +1.24 minimum), making the floor+relief combination structurally impossible for the
exact cohort the floor protects. Belt-and-suspenders is correct architecture.

**D6 issues: NONE.**

---

## Budget Raise Decision

**Decision: Option A — NO budget raise. SUGAR_CEREAL_BUDGET_RAISE is not required.**

The decisive reason is not the Nutrition Agent's stated rationale (that absolute backbone sugar
penalties for cereals are lower). The decisive reason is that high-sugar cereal products score
30–52 from the absolute backbone — they have substantial remaining family budget headroom. The
6pt relative surcharge stacks on top without hitting any budget ceiling. The biscuit budget raise
addressed a specific pattern (heavy HP_SUGAR accumulation approaching the budget cap) that is
absent in cereals. The budget is non-binding in both penalty and relief directions for this corpus.

Reversal condition: if the pilot shows any product's combined penalty is clipped by
SUGAR_FAMILY_BUDGET before the floor logic runs, add SUGAR_CEREAL_BUDGET_RAISE=6 before pilot
acceptance. The pilot must log a flag when the budget cap fires.

---

## Pilot Gate Criteria (Locked)

All 11 criteria must pass. Any failure is a hard stop.

| # | Criterion | Pass Condition |
|---|---|---|
| 1 | Resolution restored | Fewer products pinned at identical scores vs. baseline |
| 2 | Inversion A corrected | 7290100000029 ranks above 5054568100011 post-SR (direction flipped) |
| 3 | Inversion B gap widened | Gap between 7290100000042 and 5054568100022 widens to ≥5.5pts (from 4.5pts) |
| 4 | Min movers | n_movers ≥ 15 of 45 products |
| 5 | Min grade changes | n_grade_changes ≥ 1 |
| 6 | Max absorption rate | ≤ 40% (≤18/45 show zero net movement despite relative term firing) |
| 7 | Anti-Immunity holds | No cereal with sugars_g ≥ 25g reaches grade B (score ≥ 70) |
| 8 | Floor enforced | All 9 products with sugars_g ≥ 25g: composite score ≤ 62 (full distribution) |
| 9 | No dairy bleed | Zero non-cereal products moved |
| 10 | Brined byte-identical | run_brined_004 byte-identical at flag-on (frozen invariant) |
| 11 | Flag-off byte-identical | BARI_SHELF_RELATIVE_V1=off → zero movement across all published categories |

---

## Artifacts

- `C:\Bari\01_framework\bsip2_framework\project_rescore\cereals_d7_cosign_v1.md` — created
- `C:\Bari\03_operations\bsip2\evidence_registry\bsip2_evidence_registry_v1.md` — EV-087 appended at line 2093

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-4 D7 cereals sugar co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "d6_validated": true,
  "d6_issues": [],
  "budget_raise_decision": "none",
  "budget_raise_rationale": "High-sugar cereal products score 30-52 from the absolute backbone — substantial family budget headroom remains. The 6pt relative surcharge stacks without hitting the budget ceiling. The HP_SUGAR accumulation pattern that necessitated biscuits' SUGAR_SHELF_BISCUIT_BUDGET_RAISE=6 is absent in cereals. Budget is non-binding in both surcharge and relief directions. Reversal: add SUGAR_CEREAL_BUDGET_RAISE=6 if pilot shows any product clipped by SUGAR_FAMILY_BUDGET before floor logic runs.",
  "pilot_gate_criteria": {
    "min_movers": 15,
    "min_grade_changes": 1,
    "max_absorption_rate": 0.40,
    "inversion_a_corrected": true,
    "inversion_a_detail": "7290100000029 (24g/33.0) must rank above 5054568100011 (38g/35.0) post-SR — expected ~31.0 vs ~29.0",
    "inversion_b_gap_min_pts": 5.5,
    "inversion_b_detail": "7290100000042 (5g/74.9) vs 5054568100022 (16g/70.4) — gap from 4.5pts to >=5.5pts",
    "no_dairy_bleed": true,
    "brined_byte_identical": true,
    "flag_off_byte_identical": true,
    "anti_immunity": "no cereal with sugar>=25g reaches grade B (score>=70)",
    "floor_compliance": "all 9 products with sugar>=25g confirm composite score<=62 (full distribution not spot-check)"
  },
  "ev_087_registered": true,
  "ev_087_registry_line": 2093,
  "deliverable": "01_framework/bsip2_framework/project_rescore/cereals_d7_cosign_v1.md",
  "engine_files_modified": false,
  "off_ban_satisfied": true,
  "not_done": [
    "Pilot rescore (Phase-5) — requires Data Agent implementation gated on this D7 co-sign",
    "constants.py: add cereal to SUGAR_SHELF_REL_SCOPE frozenset; add SUGAR_SHELF_REL_CEREAL_FLOOR=62 and HIGH_SUGAR_CEREAL_FLOOR_THRESHOLD_G=25.0",
    "score_engine.py: add EV-087 cereal floor branch parallel to biscuit EV-085 branch",
    "compute_shelf_stats() IQR-primary verification for cereals corpus (must yield scale=8.896)",
    "SUGAR_SHELF_REL_V1 rule tag verification in traces for 4 named inversion barcodes",
    "Full-distribution floor compliance check: all 9 products with sugar>=25g individually confirmed",
    "Budget cap non-binding confirmation: pilot must log when SUGAR_FAMILY_BUDGET clips any product",
    "EV-085 biscuit path byte-identical after cereals scope addition",
    "Owner go-live gate before any published score movement (tripwire-1 — non-negotiable)"
  ],
  "artifacts": [
    {
      "path": "01_framework/bsip2_framework/project_rescore/cereals_d7_cosign_v1.md",
      "action": "created",
      "sha256": "verify-at-close"
    },
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "action": "modified",
      "line_appended": 2093,
      "ev_id": "EV-087"
    }
  ],
  "counts": {
    "d6_elements_validated": 4,
    "d6_elements_denominator": "scope, bands, floor, anti-immunity",
    "d6_issues": 0,
    "hard_conditions_total": 10,
    "hard_conditions_carried_from_phase1": 6,
    "hard_conditions_enrollment_specific": 4,
    "pilot_acceptance_criteria": 11,
    "named_inversions_ratified": 2,
    "tripwires_fired": 0,
    "ev_id_registered": "EV-087",
    "ev_track_max_before_this": "EV-086",
    "published_scores_moved": 0,
    "engine_files_modified": 0,
    "scope_categories": 1,
    "floor_value": 62,
    "floor_threshold_g": 25.0,
    "max_penalty_P_pts": 6,
    "max_relief_B_pts": 3,
    "practical_max_relief_in_corpus_pts": 2,
    "corpus_n_with_sugar": 45,
    "corpus_n_total": 45,
    "median_sugar_g": 14.0,
    "robust_scale_g": 8.896,
    "budget_raise_pts": 0
  },
  "commands_run": [
    {"cmd": "Read P107_c1_product_cereals_sugar_d7_cosign.md", "exit_code": 0, "output_summary": "Full spec read — 4 tasks, constraints, return format"},
    {"cmd": "Read cereals_sugar_enrollment_v1.md", "exit_code": 0, "output_summary": "D6 ruling confirmed — 9 sections, stats exact match, 2 named inversions, floor=62, Anti-Immunity proof"},
    {"cmd": "Read shelf_relative_d7_cosign_v1.md", "exit_code": 0, "output_summary": "Phase-1 D7 co-sign — 6 hard conditions, asymmetric P>B, IQR-primary, anti-rule-accumulation"},
    {"cmd": "Read shelf_relative_sugar_enrollment_d7_cosign_v1.md (biscuits Phase-2)", "exit_code": 0, "output_summary": "Biscuits D7 co-sign — pattern reference; floor=55, P=6, B=3, SUGAR_SHELF_BISCUIT_BUDGET_RAISE=6, 10 conditions, 7 pilot criteria"},
    {"cmd": "Read evidence registry lines 2050-2096", "exit_code": 0, "output_summary": "Registry tail confirmed — EV-086 ends at line 2089; EV-087 appended at line 2093"},
    {"cmd": "Read TASK-278.md", "exit_code": 0, "output_summary": "Full task history confirmed — Phase 4 dispatch at line 124-134; P107 dispatched at line 131"},
    {"cmd": "grep -n EV-087 evidence_registry_v1.md", "exit_code": 0, "output_summary": "EV-087 at line 2093 (heading) and 2097 (finding_id field) — confirmed unique, no prior entries"},
    {"cmd": "wc -l evidence_registry_v1.md (before append)", "exit_code": 0, "output_summary": "2096 lines before append"},
    {"cmd": "wc -l evidence_registry_v1.md (after append)", "exit_code": 0, "output_summary": "2126 lines after append — 30 lines added for EV-087"}
  ],
  "not_done_count": 9,
  "acceptance_test": {
    "spec": "D6 spec validated (scope/bands/floor/anti-immunity each confirmed or flagged); family budget raise decision made with rationale; pilot gate criteria locked (min_movers, min_grade_changes, max_absorption, 2 inversion checks, brined byte-id, 11 criteria total); EV-087 registered in evidence registry (append only); cereals_d7_cosign_v1.md written; NO engine files modified; NO scores moved; OFF ban absolute",
    "result": "PASS — all 4 D6 elements confirmed; Option A (no budget raise) decided with binding rationale and reversal condition; 11-criterion pilot gate locked including both named inversions with specific score predictions; EV-087 appended at line 2093; cereals_d7_cosign_v1.md created; 0 engine files touched; 0 scores moved; OFF ban satisfied (stats from trace L1_observed_signals only)"
  }
}
```
