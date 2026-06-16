# P114 Return — TASK-278 Phase-6: Product D7 Co-Sign (Yogurt × Sugar)

**Agent:** product-agent
**Date:** 2026-06-14
**Propose:** RETURNED

---

## Summary

D6 ratified (all 6 elements confirmed). All 5 D7 open questions decided and bound. EV-088
registered at registry line 2123 (confirmed free — 0 prior hits). 11-criterion pilot gate locked
with yogurt-specific C2/C3/C4/C9/C10 thresholds. Co-sign doc written. Engine invariants 342 PASS
confirmed. No engine edits. OFF=0.

---

## D6 Ratification

All 6 elements confirmed:

1. **Scope guard Option A** — confirmed. `category == "dairy_protein" AND category_subtype in
   CULTURED_YOGURT_SUBTYPES`. No router edit. Constant already in codebase, already used by
   fermentation bonus gate. Cleanly excludes milk, hard cheese, brined cheese, kefir, cottage,
   cream cheese.

2. **Corpus n=74** — confirmed. 88 total, 87 yogurt-only (1 cereal outlier excluded), 74 with
   non-null sugars_g. Source: `L1_observed_signals.sugars_g` in committed trace files only.

3. **Stats median=5.45/IQR=5.80/scale=4.299** — confirmed. IQR-primary formula:
   `max(IQR/1.349=4.299, 1.4826×MAD=3.781, 1.4)` = 4.299. Exact match to P103 pilot (0.0g divergence).

4. **Asymmetric P>B** — confirmed. P=6, B=3. P_max value finalized under D7-YS-01.

5. **Floor=62/threshold=12.0g/Anti-Immunity 65<70** — confirmed. Anti-Immunity: floor(62) +
   B_max(3) = 65 < 70 PASS.

6. **Named inversions** — both real and directionally correct. Inversion 1 (7290110321697 9.8g vs
   7290102397600 13.6g): confirmed cause (additive complexity gap) and SR correction path (both in
   surcharge zone, higher sugar → larger penalty → direction reversal). Inversion 2 (7290102396740
   4.5g vs 7290102393060 14.0g): confirmed partial correction (A near-median, z=−0.22 < 0.3
   threshold → unchanged; B receives 4pt surcharge → gap narrows 7.1→~3.1pts; partial correction
   is honest and expected).

---

## D7 Decisions

### D7-YS-01: P_max = 6

Option: Standardize at 6. Pilot value of 8 not adopted.

Rationale: No corpus product reaches z≥2.5 (the band tier where 6 and 8 would produce different
outcomes). Raising to 8 would only affect products with sugars_g ≥ 16.2g — none present in the
current 74-product corpus. The pilot used P_max=8 as a diagnostic probe, not a production
commitment. Standardization at 6 reduces rule accumulation and maintains consistency with cereals
and biscuits. Anti-Immunity proof holds regardless.

Reversal: Raise to 8 if corpus expands to include products ≥ 16g sugar and 6pt max fails to
differentiate from the 12–14g segment.

### D7-YS-02: Floor = 62

Confirmed at the D6 proposed value.

Rationale: The highest-scoring high-sugar corpus product (7290102397600, 13.6g) scores 62.4 at
baseline — the floor binds at exactly the natural upper bound of the current high-sugar segment.
62 is above the current range (binding as a forward guard), below grade B (70) by 8 pts (adequate
Anti-Immunity headroom), and consistent with cereals (same floor value). Floor=65 would narrow
headroom to 2pts; floor=60 would fall inside the current range and be non-binding.

Reversal: Recalibrate if corpus adds products with ≥12g sugar and baseline scores above 62.

### D7-YS-03: Threshold = 12.0g

Confirmed at the D6 proposed value.

Rationale: 12.0g is 2.3g above Q3 (9.7g) — clearly in the high-sugar segment, not the
upper-quartile boundary. Threshold aligns with the 4pt-surcharge band entry (z=1.52), creating
clean co-activation: a product that triggers the floor also receives the strongest common
surcharge. Alternative at 10.0g would apply the floor to products receiving only a 2pt surcharge
(z≈1.06) — the floor's severity would mismatch the mechanism's signal for that cohort.

Reversal: Lower to 10.0g if pilot shows 10–12g products are systematically misranked and the
floor would improve their calibration.

### D7-YS-04: Near-median z-threshold = 0.3

Decision: 0.3 (not the D6 proposal of 0.5).

Rationale: The plain yogurt cluster sits at Q1=3.9g (z=−0.36 from median). At threshold=0.5,
products at 3.9g are excluded from SR computation entirely (|z|=0.36 < 0.5). At threshold=0.3,
these products pass the gate, compute the band, and receive 0pts (band [0,0.5)→0) — they appear
in traces with delta=0, which is more observable and consistent with the cereals implementation
pattern (where z=0.464 was observed to have fired). The 0.3 threshold does not change any
product's score vs 0.5 (the difference is in traceability, not outcome, for the [0.3,0.5) range).
Better observability is worth the minor implementation difference.

Reversal: Raise to 0.5 if pilot shows >20% of SR-trace entries have delta=0 (noise without value).

### D7-YS-05: Null-sugars = Option A (no adjustment)

Option A confirmed.

Rationale: Missing sugars_g = no SR opinion. The SR mechanism expresses a relative position on
the shelf — without the value, the position is unknown, so no adjustment fires. Option B (median
imputation → z=0 → 0pts) is functionally identical for all current corpus products but creates
misleading trace entries with imputed data. Option A is cleaner, aligned with the owner's
missing-data discard rule, and requires simpler implementation (null check → skip SR computation
entirely for this product).

No reversal — Option A is correct by principle.

---

## EV-088 Registration

- **EV-088 verified free:** 0 matches for "EV-088" in registry before this return.
- **EV-088 registered at line 2123** in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`.
- **0 deletions to existing entries** — append only.
- Anti-Immunity proof in registry: floor(62) + B_max(3) = 65 < 70 PASS.

---

## Pilot Gate (11 Criteria — Locked)

| # | Name | Pass Condition | Class |
|---|---|---|---|
| C1 | resolution_restored | Fewer tied-score clusters among 74 yogurt products at flag-on vs flag-off | Hard |
| C2 | grade_dist_and_magnitude | (A) 0 yogurts sugars≥12g at grade B; (B) ≥2 yogurts sugars≤5g at grade A/S; (C) mean\|delta\|≥0.5; (D) mean delta≥0 for sugars≤5g products — all 4 required | Hard |
| C3 | inversion_gap | 7290110321697 flag-on > 7290102397600 flag-on by ≥ 2.0 pts (Inversion 1 direction corrected) | Hard |
| C4 | min_movers | ≥ 25 yogurt products with clean_delta ≠ 0 (of 74 with sugars_g non-null) | Hard |
| C5 | min_grade_changes | ≥ 1 yogurt grade change at flag-on vs flag-off | Hard |
| C6 | max_absorption | ≤ 40% absorption among SR-firing yogurts | Hard |
| C7 | anti_immunity | 0 yogurts with sugars_g ≥ 12g at grade B (score ≥ 70) at flag-on | Hard |
| C8 | floor_compliance | All yogurts with sugars_g ≥ 12g: flag-on score ≤ 62 (full distribution) | Hard |
| C9 | no_scope_bleed | 0 non-yogurt dairy_protein products with non-zero clean_delta; verify milk + brined cheese explicitly | Hard |
| C10 | frozen_byte_id | milk run_005_headpin byte-identical when BARI_SHELF_RELATIVE_V1=True — CRITICAL; any milk score movement = immediate pilot FAIL | Hard — CRITICAL |
| C11 | flag_off_drift | Flag-off scores for 87 yogurt products match run_yogurt_006 baseline; ≤10 mismatches informational; non-blocking | Docs only |

**Critical note on C10:** yogurt and milk share `dairy_protein`. If any milk product has
`category_subtype in CULTURED_YOGURT_SUBTYPES` due to miscoding, SR would fire on milk scores —
which are a FROZEN INVARIANT. C10 is the mandatory safety gate. Pilot must run milk products
explicitly with BARI_SHELF_RELATIVE_V1=True and confirm zero movement.

---

## Engine Invariants

```
python 03_operations/shadow/engine_invariants.py
I6_MONOTONICITY: pass=true, cases=342, failures=0
```

342 PASS confirmed. No engine files modified.

---

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-6 yogurt×sugar D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "d6_ratified": true,
  "d7_decisions": {
    "D7-YS-01_P_max": 6,
    "D7-YS-01_justification": "No corpus product reaches z>=2.5 where 6 and 8 differ; pilot P_max=8 was a diagnostic probe, not a production commitment; standardization at 6 reduces rule accumulation; reversal if corpus expands to >=16g sugar products",
    "D7-YS-02_floor_value": 62,
    "D7-YS-02_justification": "Highest-scoring high-sugar corpus product (62.4) sits exactly at this value; floor binds at the natural upper bound of the current segment; 8pts of headroom to grade B (70) is adequate Anti-Immunity guard; consistent with cereals",
    "D7-YS-03_floor_threshold_g": 12.0,
    "D7-YS-03_justification": "2.3g above Q3=9.7g; aligns floor activation with 4pt-surcharge band entry at z=1.52; 10.0g alternative would apply the floor to products receiving only a 2pt surcharge — mismatch between floor severity and mechanism signal",
    "D7-YS-04_near_median_threshold_z": 0.3,
    "D7-YS-04_justification": "Plain cluster at Q1=3.9g has |z|=0.36 which falls below 0.5 threshold; 0.3 threshold includes these products in SR trace with delta=0 (more observable, no score change); cereals fired at z=0.464 setting practical precedent; better traceability than hard exclusion at 0.5",
    "D7-YS-05_null_sugars_treatment": "no_adjustment",
    "D7-YS-05_justification": "Missing data = no SR opinion; null check skips SR computation entirely; Option B (median imputation) is functionally identical but creates misleading trace entries; aligns with owner missing-data discard rule"
  },
  "ev_088_registered": true,
  "ev_088_registry_line": 2123,
  "anti_immunity_proof": "floor(62) + B_max(3) = 65 < 70 PASS",
  "pilot_gate_criteria_count": 11,
  "pilot_gate_criteria": [
    {"criterion": "C1", "name": "resolution_restored", "pass_condition": "Fewer tied-score clusters at flag-on vs flag-off among 74 yogurt products with non-null sugars_g"},
    {"criterion": "C2", "name": "grade_dist_and_magnitude", "pass_condition": "(A) 0 yogurts sugars>=12g at grade B; (B) >=2 yogurts sugars<=5g at grade A/S; (C) mean|delta|>=0.5 among SR-firing; (D) mean delta>=0 for sugars<=5g — all 4 required"},
    {"criterion": "C3", "name": "inversion_gap", "pass_condition": "7290110321697 flag-on > 7290102397600 flag-on by >= 2.0 pts (Inversion 1 direction corrected; minimum gap)"},
    {"criterion": "C4", "name": "min_movers", "pass_condition": ">= 25 yogurt products (of 74 with non-null sugars_g) with clean_delta != 0"},
    {"criterion": "C5", "name": "min_grade_changes", "pass_condition": ">= 1 yogurt grade change at flag-on vs flag-off"},
    {"criterion": "C6", "name": "max_absorption", "pass_condition": "<= 40% absorption among SR-firing yogurts (clean_delta=0 despite SR term non-zero)"},
    {"criterion": "C7", "name": "anti_immunity", "pass_condition": "0 yogurts with sugars_g >= 12g at grade B (score >= 70) at flag-on; full distribution check"},
    {"criterion": "C8", "name": "floor_compliance", "pass_condition": "All yogurts with sugars_g >= 12g: flag-on score <= 62; full distribution, not spot-check"},
    {"criterion": "C9", "name": "no_scope_bleed", "pass_condition": "0 non-yogurt dairy_protein products (milk, hard cheese, brined cheese, kefir, cottage, cream cheese) with non-zero clean_delta; verify milk and brined explicitly"},
    {"criterion": "C10", "name": "frozen_byte_id", "pass_condition": "milk run_005_headpin byte-identical when BARI_SHELF_RELATIVE_V1=True — CRITICAL; any milk score movement = immediate FAIL; must run milk products explicitly with flag on"},
    {"criterion": "C11", "name": "flag_off_drift", "pass_condition": "Flag-off scores for 87 yogurt products match run_yogurt_006 baseline; <=10 mismatches informational; docs-only non-blocking"}
  ],
  "cosign_doc": "02_products/yogurt_system/methodology/yogurt_sugar_d7_cosign_v1.md",
  "engine_invariants": "342 PASS",
  "off_used": false,
  "not_done": []
}
```

```json
{
  "artifacts_claimed": [
    {"path": "02_products/yogurt_system/methodology/yogurt_sugar_d7_cosign_v1.md", "sha256": "4a606f35fa9131d34e74025817b9a7623234e0e32eafc32571b2b7fcf6aa7fb7"},
    {"path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md", "sha256": "22ebe35b3f97856e1a84b6323932e1a756ae60880961ae5bdb51a97b6db40980"}
  ],
  "counts": {
    "d7_decisions_made": {"count": 5, "denominator": "5 open questions from D6"},
    "pilot_gate_criteria_locked": {"count": 11, "denominator": "11 required per spec"},
    "ev_entries_added": {"count": 1, "denominator": "EV-088 only, 0 deletions"},
    "engine_invariant_cases": {"count": 342, "denominator": "342 required PASS"},
    "engine_files_modified": {"count": 0, "denominator": "score_engine.py/constants.py/router_v2.py"}
  },
  "commands_run": [
    {"cmd": "python 03_operations/shadow/engine_invariants.py", "exit_code": 0, "result": "342 PASS"}
  ],
  "claims_verified_by_agent": true,
  "propose": "RETURNED"
}
```
