# P128 Return — TASK-278 Phase-10: Maadanim × Sugar D7 Co-Sign

**Agent:** Product Agent  
**Task:** TASK-278 Phase-10  
**Phase:** D7 co-sign — maadanim × sugar shelf-relative enrollment  
**Return date:** 2026-06-14  
**Status:** RETURNED — D7 co-sign complete; authorized for Data Agent pilot (D8)

---

## Summary

D7 co-sign complete. All four open questions resolved. Replacement INV-B found and qualified. EV-092 registered. Co-sign doc written. Authorized for pilot rescore by Data Agent.

**D7 Decisions:**

- Q1 (Router filter): REJECTED — scope stays n=146; BSIP1 field is authoritative, not router
- Q2 (reduced_sugar_dessert): INCLUDE — sweetener cap and SR relief operate on different pipeline stages; no harmful double-benefit
- Q3 (kids_dessert n=2): INCLUDE with flag; individual z-scores valid at product level
- Q4 (Dead zone 27.4%): APPROVED at z_dead=±0.30 — within 40% ceiling, proportionally correct for IQR=11.78g

**INV-B Replacement:**

- Original INV-B rejected: both products inside dead zone [7.08g, 12.32g]
- Replacement: `2385455` (3.5g/45.0D) vs `5014271300429` (52.0g/45.6D)
- Same subtype (dairy_dessert_generic), same NOVA=2, zero additives, opposite sugar extremes
- gap_before = -0.6 (wrong direction); gap_after = +7.5 (correct direction); 8.1pt correction
- Qualifies for C3 (gap_narrows_inversion with directional reversal)

**EV-092 registered** at line 2265 of `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`.

**No engine edits. 0 score movement.**

---

## Decision Log

| Decision | Options considered | Choice | Decisive reason | Reversal condition |
|----------|-------------------|--------|-----------------|-------------------|
| Q1: Router filter | Filter to dessert+dairy_protein+default (~97) vs keep all maadanim BSIP1 products (146) | Keep all 146 — reject filter | BSIP1 `bsip_maadanim_subtype` is the authoritative scope boundary; router assignment carries no shelf-membership information | Revisit if Data Agent finds router-category mismatch creates scoring paradoxes in pilot |
| Q2: reduced_sugar_dessert | Exclude (avoid double-benefit) vs include | Include | Sweetener cap (ceiling=70) and SR relief (+B_max=3) operate at different pipeline stages; no product with sweetener scores high enough for 3pts of relief to cause grade-inflation; low-sugar earns relief regardless of mechanism | Revisit if pilot shows any reduced_sugar_dessert product reaches grade B via combined SR+sweetener path |
| Q4: Dead zone width | Tighten to ±0.25 vs approve ±0.30 | Approve ±0.30 | 27.4% < 40% ceiling; ±0.30 spans ±2.625g around median — proportionally correct for IQR=11.78g; tightening adds complexity without meaningful benefit | Revisit if pilot shows >40% absorption or if movers count falls below C4 threshold |
| INV-B selection | Original pair (both inside dead zone — disqualified) vs replacement search across 146 products | 2385455 vs 5014271300429 | Same subtype/NOVA/additives, 48.5g sugar differential, near-identical current scores, directional rank reversal after SR | N/A — trace-verified pair |

---

## Artifacts

| Artifact | Path | sha256 |
|----------|------|--------|
| D7 co-sign doc | `02_products/maadanim/methodology/maadanim_sugar_d7_cosign_v1.md` | (new file — verify via git status) |
| EV-092 registry entry | `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` line 2265 | (modified file — verify via git diff) |
| Return block | `tasks/returns/P128_return.md` | (this file) |

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-10 maadanim×sugar D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "scope_guard_approved": "product.get('bsip_maadanim_subtype') is not None AND nn.get('sugars_g') is not None",
  "q1_scope_decision": "REJECT router filter — scope remains n=146; BSIP1 bsip_maadanim_subtype field is authoritative scope boundary, not router category assignment",
  "q2_reduced_sugar_dessert": "include",
  "q3_kids_dessert": "include with flag — n=2 thin but SR is product-level; flag for re-evaluation when corpus expands",
  "q4_dead_zone": "approved 27.4% at z_dead=±0.30 — within 40% ceiling, proportionally correct",
  "n_scope": 146,
  "floor_threshold_g": 16.08,
  "inv_b_replacement": {
    "barcode_a": "2385455",
    "name_a": "בולגרית מעודנת 24%",
    "sugars_a": 3.5,
    "score_a": 45.0,
    "grade_a": "D",
    "subtype_a": "dairy_dessert_generic",
    "barcode_b": "5014271300429",
    "name_b": "מעדן משמש",
    "sugars_b": 52.0,
    "score_b": 45.6,
    "grade_b": "D",
    "subtype_b": "dairy_dessert_generic",
    "delta_a": 2.13,
    "delta_b": -6.00,
    "gap_before": -0.6,
    "gap_after": 7.5,
    "gap_correction": 8.1,
    "inversion_type": "directional_reversal",
    "qualifies_for_c3": true,
    "rejection_reason_original_invb": "both 7290110321697 (9.8g) and 7290014762800 (12.0g) are inside dead zone [7.08, 12.32] — near-zero SR delta for both, does not qualify as gap_narrows pair"
  },
  "ev092_registered": true,
  "ev092_line": 2265,
  "ev092_status": "pilot_pending",
  "pilot_gate_criteria_count": 11,
  "pilot_gate_criteria": ["C1_directional_distribution", "C2a_grade_dist", "C2b_grade_absorption", "C2c_magnitude", "C3_gap_narrows_inversion", "C4_min_movers_ge5", "C5_min_grade_changes_ge1", "C6_max_absorption_le40pct", "C7_anti_immunity", "C8_floor_compliance", "C9_no_scope_bleed", "C10_frozen_byte_id_milk_CRITICAL"],
  "anti_immunity_proof": "62+3=65<70 PASS",
  "de_anchor_confirmed": "floor_threshold_g=16.08g is Q3-based; NOT the Israeli red-label 10g threshold",
  "d7_cosign_doc": "02_products/maadanim/methodology/maadanim_sugar_d7_cosign_v1.md",
  "engine_modified": false,
  "off_used": false,
  "commands_run": [
    {"cmd": "python tmp_inv_search.py (BSIP2 trace extraction, n=146)", "exit_code": 0},
    {"cmd": "python tmp_pairs.py (counter-intuitive pair search)", "exit_code": 0},
    {"cmd": "python tmp_inversions.py (true inversion search)", "exit_code": 0},
    {"cmd": "python tmp_clean_inversions.py (non-sweetener pair search)", "exit_code": 0},
    {"cmd": "python tmp_invb_detail.py (candidate trace detail)", "exit_code": 0},
    {"cmd": "Get-Content evidence_registry_v1.md | Select-String EV-092 (line verification)", "exit_code": 0}
  ],
  "counts": {
    "products_in_scope": {"value": 146, "denominator": "run_maadanim_001 products with sugars_g not null"},
    "products_total": {"value": 200, "denominator": "run_maadanim_001 total"},
    "pilot_gate_criteria": {"value": 11, "denominator": "required criteria for D8 pilot gate"},
    "ev_registered": {"value": 1, "denominator": "EV-092"},
    "artifacts_written": {"value": 2, "denominator": "d7_cosign_doc + ev092_registry_entry"},
    "d7_questions_resolved": {"value": 4, "denominator": "Q1 Q2 Q3 Q4"},
    "true_inversions_found": {"value": 96, "denominator": "low-sugar product scoring lower than high-sugar product in corpus"},
    "replacement_invb_gap_correction_pts": {"value": 8.1, "denominator": "gap change from SR: gap_before=-0.6 to gap_after=+7.5"}
  },
  "not_done": [
    "Pilot rescore execution (Data Agent, D8)",
    "Pilot gate verification (all 11 criteria, C10 CRITICAL)",
    "Engine wiring in score_engine.py (Data Agent, D8)",
    "Task close (orchestrator, post-D8 gate verification)"
  ],
  "acceptance_test": "d7_cosign_doc exists AND ev092_registered=true at stated line AND scope_guard_approved contains bsip_maadanim_subtype AND anti_immunity 65<70 AND inv_b_replacement.qualifies_for_c3=true AND engine_modified=false",
  "acceptance_test_result": "PASS",
  "propose": "RETURNED"
}
```
