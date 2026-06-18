# P112 — TASK-278 Phase-5: Definitive Corrected Cereals Pilot (route: C1-CURSOR)
# Re-run clean pilot with n=34 corrected calibration constants; gate against revised P110 criteria

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-278.md` (Phase-5, definitive gate run)
**Prior clean pilot:** `run_cereals_002_clean_pilot/` (P109, stale n=45 stats — superseded)
**Existing script:** `03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py`
**Updated constants:** `03_operations/bsip2/proto_v0/src/constants.py` (n=34 stats set by P111)
**Output dir:** `02_products/breakfast_cereals/bsip2_outputs/run_cereals_003_corrected_pilot/`

---

## Context

P111 (D6 Nutrition Agent) recomputed cereal shelf-relative stats on n=34 cereal-only products and updated `constants.py`:
- `SUGAR_SHELF_REL_CEREAL_MEDIAN = 13.0g` (was 14.0)
- `SUGAR_SHELF_REL_CEREAL_IQR = 13.5g` (was 11.0)
- `SUGAR_SHELF_REL_CEREAL_SCALE = 11.8608` (was 8.896, +33%)

The scale increase means SR adjustments are ~25% smaller in magnitude. P109's provisional results used wrong n=45 stats. This run (P112) is the definitive gate run using corrected n=34 calibration.

**The existing dual-pilot script** (`batch_run_cereals_002_clean_pilot.py`) reads from `constants.py` at runtime. Since constants.py is already updated, you do NOT need to modify the script logic. You only need to:
1. Update the OUTPUT directory in the script (or pass as parameter) to `run_cereals_003_corrected_pilot/`
2. Run it
3. Report gate criteria

---

## Step 1: Update output path in script

Open `03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py`.
Find where the output directory is defined (likely `RUN_ID`, `OUTPUT_DIR`, or a literal path).
Change it to point to: `02_products/breakfast_cereals/bsip2_outputs/run_cereals_003_corrected_pilot/`

Update the `run_id` to `"run_cereals_003_corrected_pilot"` (for run_record.json provenance).

---

## Step 2: Run the corrected pilot

From `C:\Bari`:
```
python 03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py
```

Expected: 45 products scored twice (flag-on + flag-off), 34 cereal + 11 granola, output to `run_cereals_003_corrected_pilot/`.

**Key difference from P109**: With scale=11.861 vs 8.896, r values are ~25% smaller. Lower-magnitude SR adjustments are expected. The gate is scored against the revised P110 criteria (C2-revised threshold now A+C, C3 threshold ≥4.5 pts).

---

## Step 3: Score the revised gate

Report all 11 criteria (revised gate from P110, `tasks/TASK-278.md ## D7 Gate Revision`):

| # | Criterion | Pass Condition |
|---|---|---|
| C1 | resolution_restored | Fewer tied-score clusters at flag-on vs flag-off |
| C2-revised | grade_dist_and_magnitude | **(A)** 0 sugar≥25g cereals at grade B (score≥70) at flag-on AND ≥2 sugar≤8g cereals at grade A/S (score≥80) at flag-on; **(C)** mean\|clean_delta\|≥0.5 among SR-firing cereals; mean clean_delta≥0 for sugar≤8g cluster |
| C3 | inversion_b_gap | Clean gap (7290100000042 flag_on − 5054568100022 flag_on) ≥ 4.5 pts |
| C4 | min_movers_cereal | ≥15 cereal products with clean_delta≠0 |
| C5 | min_grade_changes_cereal | ≥1 cereal grade change (flag_on vs flag_off) |
| C6 | max_absorption_cereal | ≤40% absorbed (delta=0) among SR-firing cereals |
| C7 | anti_immunity | 0 cereal products with sugar≥25g at grade B (score≥70) at flag-on |
| C8 | floor_compliance | All sugar≥25g cereal products: flag-on score ≤62 |
| C9 | no_scope_bleed | All 11 granola products: clean_delta=0 |
| C10 | brined_byte_id | brined_005 byte-identical at BARI_SHELF_RELATIVE_V1=True (if brined_005 script needs re-run with explicit SR=True flag, do so; else report from P109 evidence: 48/48 PASS, not expected to change) |
| C11 | flag_off_drift | Flag-off mismatches vs synthesis_001: documented (non-blocking); report count |

**Key focus areas** (most likely to be affected by scale correction):
- **C2-revised(A)**: Sugar≤8g products at grade A — need ≥2. P109 showed 5 products at 80–87; with smaller delta they might drop. Check carefully.
- **C3**: Inversion B gap — P109 showed 5.0 pts under stale stats. With corrected stats: 7290100000042 (5g, r_below=0.674) delta might be smaller; 5054568100022 (16g, r_above=0.253) delta might be small penalty. Report exact flag_on scores and gap.
- **C2-revised(C)**: Mean |delta| ≥ 0.5 — with smaller adjustments, need to verify this still holds.

---

## Step 4: Per-product table (cereal-only)

Report the full per-product table: barcode | sugars_g | flag_off | flag_on | clean_delta | grade_flag_off | grade_flag_on

Sort by sugars_g ascending. This is the definitive evidence table for gate scoring.

---

## Step 5: engine_invariants 342

Run: `python 03_operations/shadow/engine_invariants.py`
Report: PASS or FAIL.

---

## Definition of Done

- [ ] Output directory updated to `run_cereals_003_corrected_pilot/`
- [ ] Pilot run complete: 45 traces + `run_record.json`
- [ ] All 11 gate criteria scored (cereal-only, clean delta basis)
- [ ] Per-product table (34 cereal products): barcode, sugar, flag_off, flag_on, delta, grade_off, grade_on
- [ ] Inversion B gap explicitly reported (7290100000042 vs 5054568100022, both flag_on scores)
- [ ] C2-revised(A) explicitly checked: count of sugar≤8g products at grade A/S at flag-on
- [ ] C2-revised(C) explicitly checked: mean |delta| for SR-firing cereals; mean delta for sugar≤8g
- [ ] engine_invariants 342 PASS
- [ ] OFF=0

---

## Constraints

- **MEASURED NOT PUBLISHED** — no comparison JSON, no frontend changes, no go-live
- **OFF ban absolute**
- **Do NOT change constants.py or score_engine.py** — constants already corrected by P111; just run
- **Do NOT use synthesis_001 as baseline** — delta = flag_on − flag_off (same engine run)

---

## Return format

Write to `C:\Bari\tasks\returns\P112_return.md`:

```json
{
  "task_id": "TASK-278",
  "phase": "Phase-5 definitive corrected pilot (n=34 stats)",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "constants_used": {
    "SUGAR_SHELF_REL_CEREAL_MEDIAN": 13.0,
    "SUGAR_SHELF_REL_CEREAL_IQR": 13.5,
    "SUGAR_SHELF_REL_CEREAL_SCALE": 11.8608
  },
  "pilot_run_dir": "run_cereals_003_corrected_pilot",
  "clean_delta_method": "flag_on_score - flag_off_score (same engine, corrected n=34 constants)",
  "inversion_b": {
    "7290100000042": {"sugars_g": 5.0, "flag_off": <f>, "flag_on": <f>, "delta": <f>},
    "5054568100022": {"sugars_g": 16.0, "flag_off": <f>, "flag_on": <f>, "delta": <f>},
    "gap_flag_on": <f>,
    "criterion_pass_c3": true/false
  },
  "c2_revised_a": {
    "sugar_le_8g_at_grade_a_or_s": <n>,
    "sugar_le_8g_products": [{"barcode": "...", "sugars_g": <f>, "flag_on": <f>, "grade": "..."}],
    "pass": true/false
  },
  "c2_revised_c": {
    "mean_abs_delta_sr_firing": <f>,
    "mean_delta_sugar_le_8g": <f>,
    "pass": true/false
  },
  "cereal_movers_clean": <n>,
  "cereal_grade_changes_clean": <n>,
  "absorption_cereal_clean": <f>,
  "anti_immunity_pass": true/false,
  "floor_compliance_pass": true/false,
  "granola_delta_non_zero": <n>,
  "brined_byte_id": {"pass": true/false, "evidence": "..."},
  "engine_invariants": "342 PASS",
  "off_used": false,
  "gate_results": [
    {"criterion": "C1", "name": "resolution_restored", "pass": true/false, "evidence": "..."},
    {"criterion": "C2-revised", "name": "grade_dist_and_magnitude", "pass": true/false, "evidence": "A: X products at A/S; C: mean|delta|=X, mean_low_sugar_delta=X"},
    {"criterion": "C3", "name": "inversion_b_gap", "pass": true/false, "evidence": "gap=X"},
    {"criterion": "C4", "name": "min_movers_cereal", "pass": true/false, "evidence": "n=X"},
    {"criterion": "C5", "name": "min_grade_changes_cereal", "pass": true/false, "evidence": "n=X"},
    {"criterion": "C6", "name": "max_absorption_cereal", "pass": true/false, "evidence": "X/Y=Z%"},
    {"criterion": "C7", "name": "anti_immunity", "pass": true/false, "evidence": "..."},
    {"criterion": "C8", "name": "floor_compliance", "pass": true/false, "evidence": "..."},
    {"criterion": "C9", "name": "no_scope_bleed", "pass": true/false, "evidence": "..."},
    {"criterion": "C10", "name": "brined_byte_id", "pass": true/false, "evidence": "..."},
    {"criterion": "C11", "name": "flag_off_drift", "pass": "n/a-docs-only", "evidence": "X mismatches"}
  ],
  "per_product_table": [
    {"barcode": "...", "sugars_g": <f>, "flag_off": <f>, "flag_on": <f>, "delta": <f>, "grade_off": "...", "grade_on": "..."},
    ...
  ],
  "not_done": []
}
```

**Do not close. Propose RETURNED — orchestrator verifies the gate and closes TASK-278 Phase-5.**
