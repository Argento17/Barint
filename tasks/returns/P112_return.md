# Return: P112

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P112_c1cursor_cereals_definitive_pilot.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-14T12:20:01.264365+00:00 |
| Finished | 2026-06-14T12:25:06.792572+00:00 |
| Exit code | 0 |

---

## Output

```
**P112 executed exactly per task body (after first `---` separator in `tasks/prompts/P112_c1cursor_cereals_definitive_pilot.md`).**

- Ignored owner meta above separator.
- **Hard rules followed**: NEVER used OFF (any field, any purpose; confirmed via code comments, run logs/self_check "off_used":false, I4_OFF_FREE, invariants, no substitution). No invented data. No changes to published scores, scoring logic, constants.py, or score_engine.py. Only updated output path/RUN_ID in the existing pilot script (no logic changes). Measured/not-published (no comp JSON/frontend/go-live). Used direct BSIP1 scrape data only. Followed all steps, gate table, DoD, constraints, return format exactly. No scope bleed or other violations.
- **Step 1**: Edited output dir + run_id (only) in script → new `run_cereals_003_corrected_pilot/`.
- **Step 2**: Ran the script (from repo root). 45 products (34 cereal + 11 granola) scored flag-on + flag-off (same engine, clean delta, corrected n=34 constants). 45 traces + run_record.json + verification_table_clean.csv + artifacts written to `02_products/breakfast_cereals/bsip2_outputs/run_cereals_003_corrected_pilot/`.
- **Step 3**: Scored all 11 revised gate criteria (C2-revised A+C, C3 ≥4.5, etc.) from fresh outputs + CSV + run data (cereal-only clean basis where specified). Full details + evidence in return JSON below + `run_record.json` + `p109_gate_values.json` (in output dir).
- **Step 4**: Full per-product table (34 cereals): barcode | sugars_g | flag_off | flag_on | clean_delta | grade_off | grade_on (sorted sugars_g asc) extracted + embedded in return JSON.
- **Step 5**: Ran `python 03_operations/shadow/engine_invariants.py` → 342 PASS (incl. I4_OFF_FREE).
- All DoD checked. C1 (resolution): 2<3 pinned (full harness). C2-revised(A): 5 (≥2) sugar≤8g at A/S flag-on + 0 high-sugar at B. C2-revised(C): mean|d|=1.7769 (≥0.5), mean low-sugar d=+1.0769 (≥0). C3: gap=5.0 (≥4.5; explicit 74.5 vs 69.5). C4=26 movers, C5=6 grade ch, C6=0%, C7=0, C8=0 viol (7 checked), C9=0, C10=48/48 (P109 evidence; no brined re-run needed), C11=25 (non-blocking doc). Granola=0 bleed. OFF=0. engine_invariants=342 PASS.
- Key numbers (post-correction, smaller-magnitude SR as predicted): cereal movers=26, grade ch=6, SR-fired=26/absorbed=0, inversion gap_on=5.0, high-sugar floor ok (max ~48.4).

**Files changed (to verify at file:line; per return contract + AGENTS.md):**
- Edited: `03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py:47` (BSIP2_OUTPUT=.../run_cereals_003_corrected_pilot), `:49` (RUN_ID="run_cereals_003_corrected_pilot"), `:559` (pilot_run_dir literal in gate_compact for provenance). (Only path/RUN_ID updates; no logic/score changes; verify at these lines + run_id usage in record writer.)
- Produced (deliverables): `02_products/breakfast_cereals/bsip2_outputs/run_cereals_003_corrected_pilot/run_record.json` (verify run_id, off_used:false, n=45/34, inversion_b with gap_flag_on=5.0 + deltas for 7290100000042/5054568100022, cereal_only movers/grade_changes/absorption, self_check off_used, gate_results), `.../products/` (exactly 45 `bsip1_*/bsip2_trace.json`; spot-check e.g. 7290100000042 flag_on=74.5 + SR term, 5054568100022 flag_on=69.5), `.../verification_table_clean.csv` (full source for per-product table + sugars_g/deltas/grades), `.../p109_gate_values.json` (compact; verify pilot_run_dir updated).
- Created: `tasks/returns/P112_return.md` (summary of steps + files:line list + exact filled JSON contract per P112 return-format spec + DoD/C2/C3/inversion explicit checks + propose RETURNED).
- (No other source changes. Brined not re-run/edited per prompt allowance + "not expected to change". No OFF, no frozen invariant touches.)

**Return json (exact per P112 prompt spec; also written to `tasks/returns/P112_return.md`):**
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
    "7290100000042": {"sugars_g": 5.0, "flag_off": 73.5, "flag_on": 74.5, "delta": 1.0},
    "5054568100022": {"sugars_g": 16.0, "flag_off": 69.5, "flag_on": 69.5, "delta": 0.0},
    "gap_flag_on": 5.0,
    "criterion_pass_c3": true
  },
  "c2_revised_a": {
    "sugar_le_8g_at_grade_a_or_s": 5,
    "sugar_le_8g_products": [
      {"barcode": "5900100000005", "sugars_g": 0.5, "flag_on": 81.8, "grade": "A"},
      {"barcode": "7290100000002", "sugars_g": 1.0, "flag_on": 80.4, "grade": "A"},
      {"barcode": "5900100000003", "sugars_g": 1.1, "flag_on": 80.8, "grade": "A"},
      {"barcode": "7290100000001", "sugars_g": 1.1, "flag_on": 81.2, "grade": "A"},
      {"barcode": "7290100000004", "sugars_g": 1.5, "flag_on": 86.9, "grade": "A"}
    ],
    "pass": true
  },
  "c2_revised_c": {
    "mean_abs_delta_sr_firing": 1.7769,
    "mean_delta_sugar_le_8g": 1.0769,
    "pass": true
  },
  "cereal_movers_clean": 26,
  "cereal_grade_changes_clean": 6,
  "absorption_cereal_clean": 0.0,
  "anti_immunity_pass": true,
  "floor_compliance_pass": true,
  "granola_delta_non_zero": 0,
  "brined_byte_id": {"pass": true, "evidence": "48/48 PASS from P109 evidence (run_brined_005); no re-run performed (cereal sugar stats change has no effect on brined scope exclusion)"},
  "engine_invariants": "342 PASS",
  "off_used": false,
  "gate_results": [
    {"criterion": "C1", "name": "resolution_restored", "pass": true, "evidence": "on_max_pinned=2, off_max_pinned=3 (fewer identical in on = restored resolution; full 45-set per harness)"},
    {"criterion": "C2-revised", "name": "grade_dist_and_magnitude", "pass": true, "evidence": "A: 5 products at A/S; C: mean|delta|=1.7769, mean_low_sugar_delta=1.0769"},
    {"criterion": "C3", "name": "inversion_b_gap", "pass": true, "evidence": "gap=5.0"},
    {"criterion": "C4", "name": "min_movers_cereal", "pass": true, "evidence": "n=26"},
    {"criterion": "C5", "name": "min_grade_changes_cereal", "pass": true, "evidence": "n=6"},
    {"criterion": "C6", "name": "max_absorption_cereal", "pass": true, "evidence": "0/26=0%"},
    {"criterion": "C7", "name": "anti_immunity", "pass": true, "evidence": "0 high_sugar (>=25g) cereal at B(>=70) flag-on"},
    {"criterion": "C8", "name": "floor_compliance", "pass": true, "evidence": "7 cereal sugar>=25g checked, 0 >62 violations (all <=48.4)"},
    {"criterion": "C9", "name": "no_scope_bleed", "pass": true, "evidence": "granola products with non-zero delta: 0 (need=0)"},
    {"criterion": "C10", "name": "brined_byte_id", "pass": true, "evidence": "48/48 PASS (P109 evidence; brined out of cereal SR scope)"},
    {"criterion": "C11", "name": "flag_off_drift", "pass": "n/a-docs-only", "evidence": "25 mismatches (non-blocking per spec)"}
  ],
  "per_product_table": [
    {"barcode": "5900100000005", "sugars_g": 0.5, "flag_off": 79.8, "flag_on": 81.8, "delta": 2.0, "grade_off": "B", "grade_on": "A"},
    {"barcode": "7290100000002", "sugars_g": 1.0, "flag_off": 79.4, "flag_on": 80.4, "delta": 1.0, "grade_off": "B", "grade_on": "A"},
    {"barcode": "5900100000003", "sugars_g": 1.1, "flag_off": 79.8, "flag_on": 80.8, "delta": 1.0, "grade_off": "B", "grade_on": "A"},
    {"barcode": "7290100000001", "sugars_g": 1.1, "flag_off": 80.2, "flag_on": 81.2, "delta": 1.0, "grade_off": "A", "grade_on": "A"},
    {"barcode": "7290100000004", "sugars_g": 1.5, "flag_off": 85.9, "flag_on": 86.9, "delta": 1.0, "grade_off": "A", "grade_on": "A"},
    {"barcode": "4013228100001", "sugars_g": 2.0, "flag_off": 78.7, "flag_on": 79.7, "delta": 1.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "8437014100001", "sugars_g": 4.0, "flag_off": 68.3, "flag_on": 69.3, "delta": 1.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "5011145100001", "sugars_g": 4.5, "flag_off": 74.2, "flag_on": 75.2, "delta": 1.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "7290100000008", "sugars_g": 5.0, "flag_off": 77.5, "flag_on": 78.5, "delta": 1.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "7290100000042", "sugars_g": 5.0, "flag_off": 73.5, "flag_on": 74.5, "delta": 1.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "7290100000011", "sugars_g": 7.5, "flag_off": 62.5, "flag_on": 63.5, "delta": 1.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "5054568100001", "sugars_g": 8.0, "flag_off": 62.4, "flag_on": 63.4, "delta": 1.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "7290100000041", "sugars_g": 8.0, "flag_off": 71.7, "flag_on": 72.7, "delta": 1.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "7613031100001", "sugars_g": 8.5, "flag_off": 58.0, "flag_on": 59.0, "delta": 1.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "5054568100002", "sugars_g": 9.0, "flag_off": 61.2, "flag_on": 62.2, "delta": 1.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "7290100000045", "sugars_g": 10.0, "flag_off": 64.3, "flag_on": 64.3, "delta": 0.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "7613031100050", "sugars_g": 12.0, "flag_off": 63.0, "flag_on": 63.0, "delta": 0.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "5054568100050", "sugars_g": 14.0, "flag_off": 62.9, "flag_on": 62.9, "delta": 0.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "5054568100022", "sugars_g": 16.0, "flag_off": 69.5, "flag_on": 69.5, "delta": 0.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "5054568100040", "sugars_g": 16.0, "flag_off": 68.0, "flag_on": 68.0, "delta": 0.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "5900100000007", "sugars_g": 16.0, "flag_off": 67.7, "flag_on": 67.7, "delta": 0.0, "grade_off": "B", "grade_on": "B"},
    {"barcode": "7613031100020", "sugars_g": 16.0, "flag_off": 52.1, "flag_on": 52.1, "delta": 0.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "5054568100020", "sugars_g": 17.0, "flag_off": 61.2, "flag_on": 61.2, "delta": 0.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "5054568100021", "sugars_g": 18.5, "flag_off": 52.0, "flag_on": 51.0, "delta": -1.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "5900100000006", "sugars_g": 18.5, "flag_off": 55.0, "flag_on": 54.0, "delta": -1.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "7613031100021", "sugars_g": 18.5, "flag_off": 52.0, "flag_on": 51.0, "delta": -1.0, "grade_off": "C", "grade_on": "C"},
    {"barcode": "5000159100001", "sugars_g": 24.0, "flag_off": 51.8, "flag_on": 49.8, "delta": -2.0, "grade_off": "C", "grade_on": "D"},
    {"barcode": "7613031100011", "sugars_g": 26.0, "flag_off": 50.4, "flag_on": 48.4, "delta": -2.0, "grade_off": "C", "grade_on": "D"},
    {"barcode": "7613031100012", "sugars_g": 28.0, "flag_off": 30.0, "flag_on": 26.0, "delta": -4.0, "grade_off": "E", "grade_on": "E"},
    {"barcode": "7290100000020", "sugars_g": 30.0, "flag_off": 34.3, "flag_on": 30.3, "delta": -4.0, "grade_off": "E", "grade_on": "E"},
    {"barcode": "5054568100010", "sugars_g": 35.0, "flag_off": 31.8, "flag_on": 30.2, "delta": -1.6, "grade_off": "E", "grade_on": "E"},
    {"barcode": "7613031100010", "sugars_g": 36.0, "flag_off": 30.5, "flag_on": 28.9, "delta": -1.6, "grade_off": "E", "grade_on": "E"},
    {"barcode": "5054568100011", "sugars_g": 38.0, "flag_off": 36.3, "flag_on": 30.3, "delta": -6.0, "grade_off": "D", "grade_on": "E"},
    {"barcode": "5054568100012", "sugars_g": 39.0, "flag_off": 31.1, "flag_on": 25.1, "delta": -6.0, "grade_off": "E", "grade_on": "E"}
  ],
  "not_done": []
}
```

**Propose RETURNED. Orchestrator to verify claims vs artifacts (e.g. run_record:47+, verification CSV, traces for named barcodes, invariants output, P112_return.md:xx, script edits at :47/49/559) then close TASK-278 Phase-5. (Per return contract + AGENTS.md 01_framework/operations/return_contract_v1.md + registry_first.)**
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M .claude/agents/content-agent.md
 M .claude/agents/data-agent.md
 M .claude/agents/design-agent.md
 M .claude/agents/frontend-agent.md
 M .claude/agents/marketing-agent.md
 M .claude/agents/nutrition-agent.md
 M .claude/agents/product-agent.md
 M .claude/agents/qa-agent.md
 M .claude/agents/red-team-agent.md
 M .claude/agents/research-agent.md
 M .claude/commands/orchestrate.md
 M .claude/settings.json
 M .claude/skills/bari-category-factory/SKILL.md
 M 01_framework/glass_box/additive_tiered_library_v1.md
 M 01_framework/operations/comp/source_registry_v1.yaml
 M 01_framework/operations/orchestration_model_v1.md
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2107071/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2107798/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2133162/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2133889/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2385455/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2511229/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2511236/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2511243/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_3075805/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_369617/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_48413/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_4861056/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_4861070/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_4861360/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_554457/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_554532/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_5992872/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499051/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499105/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499112/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499129/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499303/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499327/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499358/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499365/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290017065236/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290017065663/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019635222/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019635826/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019790112/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019790402/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019790808/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290102393718/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290102397334/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290108509106/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290108509755/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290114310550/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290114312486/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290114312707/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290114314015/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641902/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641919/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641940/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641957/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641964/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073644996/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073730330/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_8606370/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/run_record.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_5411188112709/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_5411188124689/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_5411188300328/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290000051352/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290014760141/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290019790259/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290102392094/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290107932134/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290110324773/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290110324926/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290110325619/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290114313285/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290114313865/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290116936116/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290119385560/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7394376619939/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7394376620904/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7394376621451/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_8000215204219/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_8000215204554/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/run_record.json
 M 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_recal_p0_trim/run_record.json
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/bsip2/proto_v0/src/constants.py
 M 03_operations/bsip2/proto_v0/src/evaluation_scope.py
 M 03_operations/bsip2/proto_v0/src/nova_proxy.py
 M 03_operations/bsip2/proto_v0/src/router_v2.py
 M 03_operations/bsip2/proto_v0/src/score_engine.py
 M 03_operations/bsip2/proto_v0/src/signal_extractor.py
 M 03_operations/reports/regression/regression_check_001.md
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/folic_acid.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/omega3_epa_dha.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M 99_archive/command_center_retired_2026-06-13/cc-agent_AGENT_DEFINITION.md
 M 99_archive/command_center_retired_2026-06-13/command_center.json
 M 99_archive/command_center_retired_2026-06-13/command_center_archive.json
 M 99_archive/command_center_retired_2026-06-13/command_center_live.json
 M CLAUDE.md
 M bari-web/src/app/hashvaot/bread/page.tsx
 M bari-web/src/app/hashvaot/breakfast-cereals/page.tsx
 M bari-web/src/app/hashvaot/brined-cheeses/page.tsx
 M bari-web/src/app/hashvaot/butter/page.tsx
 M bari-web/src/app/hashvaot/cheese/page.tsx
 M bari-web/src/app/hashvaot/granola/page.tsx
 M bari-web/src/app/hashvaot/hard-cheeses/page.tsx
 M bari-web/src/app/hashvaot/hummus/page.tsx
 M bari-web/src/app/hashvaot/juices/page.tsx
 M bari-web/src/app/hashvaot/page.tsx
 M bari-web/src/app/hashvaot/salty-snacks/page.tsx
 M bari-web/src/app/hashvaot/snacks/page.tsx
 M bari-web/src/app/hashvaot/vegetable-spreads/page.tsx
 M bari-web/src/app/hashvaot/yogurts/page.tsx
 M bari-web/src/app/robots.ts
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/granola_frontend_v1.json
 M integrations/clients/il_supplement_panels.py
 D tasks/TASK-218.md
 D tasks/TASK-221.md
 D tasks/TASK-244.md
 D tasks/TASK-249.md
 M tasks/closed/TASK-226.md
?? .github/
?? 01_framework/bsip2_framework/docs/scoring/additive_cocktail_cluster_proposal_v1.md
?? 01_framework/bsip2_framework/phvo_governance/
?? 01_framework/bsip2_framework/project_rescore/
?? 01_framework/governance/grade_boundary_policy_v1.json
?? 01_framework/operations/bari_router_v4_2.md
?? 01_framework/operations/brined_session_retrospective_v1.md
?? 01_framework/operations/comparison_chain_gap_analysis_v1.html
?? 01_framework/operations/comparison_chain_gap_analysis_v1.md
?? 01_framework/operations/comparison_chain_gap_analysis_v1.pdf
?? 01_framework/operations/comparison_chain_tech_leaps_v1.html
?? 01_framework/operations/comparison_page_production_map_v1.html
?? 01_framework/operations/comparison_page_production_map_v1.md
?? 01_framework/operations/comparison_page_production_map_v1.pdf
?? 01_framework/operations/lane_routing_rules_v1.md
?? 01_framework/operations/prod_repo_sync_decision_v1.md
?? 01_framework/operations/return_contract_v1.md
?? 01_framework/operations/task255_scrape_recon_v1.md
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_008_reconstruction/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_multiretailer_001_reconstruction/
?? 02_products/breakfast_cereals/cereals_copy_remediation_draft_v1.json
?? 02_products/breakfast_cereals/cereals_copy_remediation_draft_v2.json
?? 02_products/breakfast_cereals/cereals_qa_report_v1.md
?? 02_products/breakfast_cereals/methodology/
?? 02_products/cookies_coffee/bsip0_outputs/
?? 02_products/cookies_coffee/bsip2_outputs/run_cookies_005_shelfrel_pilot/
?? 02_products/cookies_coffee/cookies_coffee_copy_v1.json
?? 02_products/cookies_coffee/factory_run_001/
?? 02_products/cookies_coffee/gen_frontend_json.py
?? 02_products/cookies_coffee/methodology/
?? 02_products/cookies_coffee/reports/
?? 02_products/frozen_vegetables/.usda_generic_cache_v1.json
?? 02_products/frozen_vegetables/_build_copy_v2.py
?? 02_products/frozen_vegetables/build_benefit_lookup.py
?? 02_products/frozen_vegetables/frozen_vegetables_benefit_lookup_v1.json
?? 02_products/frozen_vegetables/frozen_vegetables_copy_v2_draft.json
?? 02_products/frozen_vegetables/frozen_vegetables_shell_copy_v2.json
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase1_spec_v1.md
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase2_seed_v1.json
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase3_copyinput_v1.json
?? 02_products/supplements/real_corpus_v3/
?? 02_products/yogurt_system/bsip0/yogurt_bsip0_log_20260611T072535.txt
?? 02_products/yogurt_system/bsip0/yogurt_bsip0_raw_20260611T072535.json
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_005/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_006/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_pilot/
?? 02_products/yogurt_system/build_yogurts_frontend_v006.py
?? 02_products/yogurt_system/build_yogurts_frontend_v4.py
?? 02_products/yogurt_system/reports/red_team_yogurts_v4.md
?? 02_products/yogurt_system/reports/run_yogurt_005_run_summary.json
?? 02_products/yogurt_system/reports/run_yogurt_006_run_summary.json
?? 02_products/yogurt_system/reports/run_yogurt_006_shipcfg_run_record.json
?? 02_products/yogurt_system/reports/run_yogurt_006_shipcfg_run_summary.json
?? 02_products/yogurt_system/reports/run_yogurt_006_shipcfg_vs_v3_comparison.json
?? 02_products/yogurt_system/reports/yogurts_off_remediation_decision_brief_v1.md
?? 02_products/yogurt_system/reports/yogurts_v4_methodology_rulings_v1.md
?? 02_products/yogurt_system/s_grade_explanations_v1.md
?? 02_products/yogurt_system/yogurt_relaunch_failure_audit_v1.md
?? 02_products/yogurt_system/yogurts_copy_regen_draft_v1.json
?? 02_products/yogurt_system/yogurts_frontend_v006_staging.json
?? 02_products/yogurt_system/yogurts_frontend_v4.json
?? 03_operations/bsip0/raw_store/
?? 03_operations/bsip0/scrape/_shared/bsip0_gate.py
?? 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py
?? 03_operations/bsip0/scrape/image_backfill_task243/
?? 03_operations/bsip0/scrape/shufersal_brined_cheeses/
?? 03_operations/bsip0/scrape/shufersal_cookies_coffee/
?? 03_operations/bsip0/scrape/shufersal_yogurt/02_build_bsip1_yogurt_005.py
?? 03_operations/bsip0/scrape_runner/
?? 03_operations/bsip1/core/build_precondition.py
?? 03_operations/bsip1/run_brined_cheeses_001/
?? 03_operations/bsip1/run_brined_cheeses_002/
?? 03_operations/bsip1/run_yogurt_005/
?? 03_operations/bsip1/run_yogurt_006/
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_001.py
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_002.py
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_003.py
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_004.py
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_005.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cereals_001_shelfrel_pilot.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_001.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_002.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_003.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_004.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_005_shelfrel_pilot.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_005.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_006.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_006_shipcfg.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_shelfrel_pilot.py
?? 03_operations/bsip2/proto_v0/src/p56_byte_identity.py
?? 03_operations/bsip2/proto_v0/src/p75_no_regression.py
?? 03_operations/bsip2/proto_v0/src/p75_no_regression_template_skip.py
?? 03_operations/bsip2/proto_v0/src/p75b_gate.py
?? 03_operations/bsip2/proto_v0/src/p99_shelf_relative_guards.py
?? 03_operations/bsip2/proto_v0/src/run_p75b_bleed_sim.py
?? 03_operations/bsip2/proto_v0/src/shadow_backtest.py
?? 03_operations/bsip2/proto_v0/src/task238_off_remediation.py
?? 03_operations/bsip2/proto_v0/tests/
?? 03_operations/claim_entailment/
?? 03_operations/off_sweep/
?? 03_operations/page_generator/
?? 03_operations/router/
?? 03_operations/runs/
?? 03_operations/seo/generate_faq_schema.py
?? 03_operations/seo/run_all_faq_schemas.py
?? 03_operations/shadow/
?? 03_operations/spine/
?? 99_archive/bread_retail_001_OFF_superseded_TASK238/
?? AGENTS.md
?? Bari-task243/
?? "C\357\200\272Bari02_productsyogurt_systemreportsrt_a_grades_tmp.json"
?? "C\357\200\272Bari02_productsyogurt_systemreportsrt_anomalies_tmp.json"
?? __b64_bsip1_stub.txt
?? __bsip1_b64.txt
?? __check_ramiLevy.py
?? __gen.py
?? __gen_cookies_scripts.py
?? __gen_part1.py
?? _parse_traces.py
?? bari-web/_start_c3.log
?? bari-web/_start_cookies.log
?? bari-web/_start_cookies2.log
?? bari-web/_start_final.log
?? bari-web/build_cookies.log
?? bari-web/build_cookies2.log
?? bari-web/build_cookies3.log
?? bari-web/build_cookies4.log
?? bari-web/build_cookies_verify.log
?? bari-web/build_final.log
?? bari-web/public/qa/brined/
?? bari-web/public/qa/cookies/
?? bari-web/scripts/shot-charts-mobile-full.mjs
?? bari-web/scripts/shot-charts-parts.mjs
?? bari-web/scripts/shot-charts-zoom.mjs
?? bari-web/scripts/shot-cookies-page.mjs
?? bari-web/src/app/hashvaot/cookies-coffee/
?? bari-web/src/components/comparisons/cookies-coffee-comparison-page.tsx
?? bari-web/src/components/comparisons/cookies-coffee-prologue-visualizations.tsx
?? bari-web/src/components/hashvaot/featured-cookies-coffee-intelligence-card.tsx
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/yogurts_frontend_v4_gates_report.md
?? bari-web/src/data/seo/
?? bari-web/src/lib/comparisons/cookies-coffee-page-data.ts
?? bari-web/src/lib/seo/
?? err.txt
?? err2.txt
?? err3.txt
?? git
?? out.txt
?? out2.txt
?? out3.txt
?? reports/
?? "research/Algorithmic Foundations of Consumer Food Scoring Engines.pdf"
?? tasks/DISPATCH_BOARD.md
?? tasks/HANDOVER.md
?? tasks/TASK-233F.md
?? tasks/TASK-235.md
?? tasks/TASK-236.md
?? tasks/TASK-246.md
?? tasks/TASK-250.md
?? tasks/TASK-251.md
?? tasks/TASK-252.md
?? tasks/TASK-253.md
?? tasks/TASK-254.md
?? tasks/TASK-255.md
?? tasks/TASK-256.md
?? tasks/TASK-257.md
?? tasks/TASK-258.md
?? tasks/TASK-259.md
?? tasks/TASK-260.md
?? tasks/TASK-261.md
?? tasks/TASK-262.md
?? tasks/TASK-263.md
?? tasks/TASK-264.md
?? tasks/TASK-265.md
?? tasks/TASK-266.md
?? tasks/TASK-269.md
?? tasks/TASK-270.md
?? tasks/TASK-274.md
?? tasks/TASK-275.md
?? tasks/TASK-276.md
?? tasks/TASK-277.md
?? tasks/TASK-278.md
?? tasks/TASK-279.md
?? tasks/TASK-281.md
?? tasks/TASK-282.md
?? tasks/_build.log
?? tasks/_dev.log
?? tasks/_p56_patch_score_engine.py
?? tasks/archive/
?? tasks/closed/TASK-218.md
?? tasks/closed/TASK-221.md
?? tasks/closed/TASK-242.md
?? tasks/closed/TASK-243.md
?? tasks/closed/TASK-244.md
?? tasks/closed/TASK-245.md
?? tasks/closed/TASK-245A.md
?? tasks/closed/TASK-245B.md
?? tasks/closed/TASK-247.md
?? tasks/closed/TASK-248.md
?? tasks/closed/TASK-249.md
?? tasks/closed/TASK-267.md
?? tasks/closed/TASK-271.md
?? tasks/closed/TASK-277.md
?? tasks/closed/TASK-279.md
?? tasks/closed/TASK-280.md
?? tasks/new_task.py
?? tasks/prompts/
?? tasks/returns/
?? tasks/scripts/
?? tmp/
```

### After dispatch

```
M .claude/agents/content-agent.md
 M .claude/agents/data-agent.md
 M .claude/agents/design-agent.md
 M .claude/agents/frontend-agent.md
 M .claude/agents/marketing-agent.md
 M .claude/agents/nutrition-agent.md
 M .claude/agents/product-agent.md
 M .claude/agents/qa-agent.md
 M .claude/agents/red-team-agent.md
 M .claude/agents/research-agent.md
 M .claude/commands/orchestrate.md
 M .claude/settings.json
 M .claude/skills/bari-category-factory/SKILL.md
 M 01_framework/glass_box/additive_tiered_library_v1.md
 M 01_framework/operations/comp/source_registry_v1.yaml
 M 01_framework/operations/orchestration_model_v1.md
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2107071/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2107798/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2133162/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2133889/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2385455/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2511229/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2511236/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_2511243/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_3075805/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_369617/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_48413/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_4861056/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_4861070/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_4861360/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_554457/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_554532/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_5992872/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499051/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499105/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499112/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499129/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499303/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499327/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499358/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290011499365/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290017065236/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290017065663/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019635222/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019635826/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019790112/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019790402/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290019790808/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290102393718/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290102397334/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290108509106/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290108509755/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290114310550/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290114312486/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290114312707/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7290114314015/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641902/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641919/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641940/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641957/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073641964/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073644996/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_7296073730330/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/products/bsip1_brinedcheese_8606370/bsip2_trace.json
 M 02_products/brined_cheeses/bsip2_outputs/run_brined_005/run_record.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_5411188112709/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_5411188124689/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_5411188300328/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290000051352/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290014760141/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290019790259/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290102392094/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290107932134/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290110324773/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290110324926/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290110325619/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290114313285/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290114313865/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290116936116/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7290119385560/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7394376619939/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7394376620904/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_7394376621451/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_8000215204219/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/products/bsip1_8000215204554/bsip2_trace.json
 M 02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/run_record.json
 M 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_recal_p0_trim/run_record.json
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/bsip2/proto_v0/src/constants.py
 M 03_operations/bsip2/proto_v0/src/evaluation_scope.py
 M 03_operations/bsip2/proto_v0/src/nova_proxy.py
 M 03_operations/bsip2/proto_v0/src/router_v2.py
 M 03_operations/bsip2/proto_v0/src/score_engine.py
 M 03_operations/bsip2/proto_v0/src/signal_extractor.py
 M 03_operations/reports/regression/regression_check_001.md
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/folic_acid.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/omega3_epa_dha.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M 99_archive/command_center_retired_2026-06-13/cc-agent_AGENT_DEFINITION.md
 M 99_archive/command_center_retired_2026-06-13/command_center.json
 M 99_archive/command_center_retired_2026-06-13/command_center_archive.json
 M 99_archive/command_center_retired_2026-06-13/command_center_live.json
 M CLAUDE.md
 M bari-web/src/app/hashvaot/bread/page.tsx
 M bari-web/src/app/hashvaot/breakfast-cereals/page.tsx
 M bari-web/src/app/hashvaot/brined-cheeses/page.tsx
 M bari-web/src/app/hashvaot/butter/page.tsx
 M bari-web/src/app/hashvaot/cheese/page.tsx
 M bari-web/src/app/hashvaot/granola/page.tsx
 M bari-web/src/app/hashvaot/hard-cheeses/page.tsx
 M bari-web/src/app/hashvaot/hummus/page.tsx
 M bari-web/src/app/hashvaot/juices/page.tsx
 M bari-web/src/app/hashvaot/page.tsx
 M bari-web/src/app/hashvaot/salty-snacks/page.tsx
 M bari-web/src/app/hashvaot/snacks/page.tsx
 M bari-web/src/app/hashvaot/vegetable-spreads/page.tsx
 M bari-web/src/app/hashvaot/yogurts/page.tsx
 M bari-web/src/app/robots.ts
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/granola_frontend_v1.json
 M integrations/clients/il_supplement_panels.py
 D tasks/TASK-218.md
 D tasks/TASK-221.md
 D tasks/TASK-244.md
 D tasks/TASK-249.md
 M tasks/closed/TASK-226.md
?? .github/
?? 01_framework/bsip2_framework/docs/scoring/additive_cocktail_cluster_proposal_v1.md
?? 01_framework/bsip2_framework/phvo_governance/
?? 01_framework/bsip2_framework/project_rescore/
?? 01_framework/governance/grade_boundary_policy_v1.json
?? 01_framework/operations/bari_router_v4_2.md
?? 01_framework/operations/brined_session_retrospective_v1.md
?? 01_framework/operations/comparison_chain_gap_analysis_v1.html
?? 01_framework/operations/comparison_chain_gap_analysis_v1.md
?? 01_framework/operations/comparison_chain_gap_analysis_v1.pdf
?? 01_framework/operations/comparison_chain_tech_leaps_v1.html
?? 01_framework/operations/comparison_page_production_map_v1.html
?? 01_framework/operations/comparison_page_production_map_v1.md
?? 01_framework/operations/comparison_page_production_map_v1.pdf
?? 01_framework/operations/lane_routing_rules_v1.md
?? 01_framework/operations/prod_repo_sync_decision_v1.md
?? 01_framework/operations/return_contract_v1.md
?? 01_framework/operations/task255_scrape_recon_v1.md
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_003_corrected_pilot/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_008_reconstruction/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_multiretailer_001_reconstruction/
?? 02_products/breakfast_cereals/cereals_copy_remediation_draft_v1.json
?? 02_products/breakfast_cereals/cereals_copy_remediation_draft_v2.json
?? 02_products/breakfast_cereals/cereals_qa_report_v1.md
?? 02_products/breakfast_cereals/methodology/
?? 02_products/cookies_coffee/bsip0_outputs/
?? 02_products/cookies_coffee/bsip2_outputs/run_cookies_005_shelfrel_pilot/
?? 02_products/cookies_coffee/cookies_coffee_copy_v1.json
?? 02_products/cookies_coffee/factory_run_001/
?? 02_products/cookies_coffee/gen_frontend_json.py
?? 02_products/cookies_coffee/methodology/
?? 02_products/cookies_coffee/reports/
?? 02_products/frozen_vegetables/.usda_generic_cache_v1.json
?? 02_products/frozen_vegetables/_build_copy_v2.py
?? 02_products/frozen_vegetables/build_benefit_lookup.py
?? 02_products/frozen_vegetables/frozen_vegetables_benefit_lookup_v1.json
?? 02_products/frozen_vegetables/frozen_vegetables_copy_v2_draft.json
?? 02_products/frozen_vegetables/frozen_vegetables_shell_copy_v2.json
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase1_spec_v1.md
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase2_seed_v1.json
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase3_copyinput_v1.json
?? 02_products/supplements/real_corpus_v3/
?? 02_products/yogurt_system/bsip0/yogurt_bsip0_log_20260611T072535.txt
?? 02_products/yogurt_system/bsip0/yogurt_bsip0_raw_20260611T072535.json
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_005/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_006/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_shelfrel_pilot/
?? 02_products/yogurt_system/build_yogurts_frontend_v006.py
?? 02_products/yogurt_system/build_yogurts_frontend_v4.py
?? 02_products/yogurt_system/reports/red_team_yogurts_v4.md
?? 02_products/yogurt_system/reports/run_yogurt_005_run_summary.json
?? 02_products/yogurt_system/reports/run_yogurt_006_run_summary.json
?? 02_products/yogurt_system/reports/run_yogurt_006_shipcfg_run_record.json
?? 02_products/yogurt_system/reports/run_yogurt_006_shipcfg_run_summary.json
?? 02_products/yogurt_system/reports/run_yogurt_006_shipcfg_vs_v3_comparison.json
?? 02_products/yogurt_system/reports/yogurts_off_remediation_decision_brief_v1.md
?? 02_products/yogurt_system/reports/yogurts_v4_methodology_rulings_v1.md
?? 02_products/yogurt_system/s_grade_explanations_v1.md
?? 02_products/yogurt_system/yogurt_relaunch_failure_audit_v1.md
?? 02_products/yogurt_system/yogurts_copy_regen_draft_v1.json
?? 02_products/yogurt_system/yogurts_frontend_v006_staging.json
?? 02_products/yogurt_system/yogurts_frontend_v4.json
?? 03_operations/bsip0/raw_store/
?? 03_operations/bsip0/scrape/_shared/bsip0_gate.py
?? 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py
?? 03_operations/bsip0/scrape/image_backfill_task243/
?? 03_operations/bsip0/scrape/shufersal_brined_cheeses/
?? 03_operations/bsip0/scrape/shufersal_cookies_coffee/
?? 03_operations/bsip0/scrape/shufersal_yogurt/02_build_bsip1_yogurt_005.py
?? 03_operations/bsip0/scrape_runner/
?? 03_operations/bsip1/core/build_precondition.py
?? 03_operations/bsip1/run_brined_cheeses_001/
?? 03_operations/bsip1/run_brined_cheeses_002/
?? 03_operations/bsip1/run_yogurt_005/
?? 03_operations/bsip1/run_yogurt_006/
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_001.py
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_002.py
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_003.py
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_004.py
?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_005.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cereals_001_shelfrel_pilot.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_001.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_002.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_003.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_004.py
?? 03_operations/bsip2/proto_v0/src/batch_run_cookies_005_shelfrel_pilot.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_005.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_006.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_006_shipcfg.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_shelfrel_pilot.py
?? 03_operations/bsip2/proto_v0/src/p56_byte_identity.py
?? 03_operations/bsip2/proto_v0/src/p75_no_regression.py
?? 03_operations/bsip2/proto_v0/src/p75_no_regression_template_skip.py
?? 03_operations/bsip2/proto_v0/src/p75b_gate.py
?? 03_operations/bsip2/proto_v0/src/p99_shelf_relative_guards.py
?? 03_operations/bsip2/proto_v0/src/run_p75b_bleed_sim.py
?? 03_operations/bsip2/proto_v0/src/shadow_backtest.py
?? 03_operations/bsip2/proto_v0/src/task238_off_remediation.py
?? 03_operations/bsip2/proto_v0/tests/
?? 03_operations/claim_entailment/
?? 03_operations/off_sweep/
?? 03_operations/page_generator/
?? 03_operations/router/
?? 03_operations/runs/
?? 03_operations/seo/generate_faq_schema.py
?? 03_operations/seo/run_all_faq_schemas.py
?? 03_operations/shadow/
?? 03_operations/spine/
?? 99_archive/bread_retail_001_OFF_superseded_TASK238/
?? AGENTS.md
?? Bari-task243/
?? "C\357\200\272Bari02_productsyogurt_systemreportsrt_a_grades_tmp.json"
?? "C\357\200\272Bari02_productsyogurt_systemreportsrt_anomalies_tmp.json"
?? __b64_bsip1_stub.txt
?? __bsip1_b64.txt
?? __check_ramiLevy.py
?? __gen.py
?? __gen_cookies_scripts.py
?? __gen_part1.py
?? _parse_traces.py
?? bari-web/_start_c3.log
?? bari-web/_start_cookies.log
?? bari-web/_start_cookies2.log
?? bari-web/_start_final.log
?? bari-web/build_cookies.log
?? bari-web/build_cookies2.log
?? bari-web/build_cookies3.log
?? bari-web/build_cookies4.log
?? bari-web/build_cookies_verify.log
?? bari-web/build_final.log
?? bari-web/public/qa/brined/
?? bari-web/public/qa/cookies/
?? bari-web/scripts/shot-charts-mobile-full.mjs
?? bari-web/scripts/shot-charts-parts.mjs
?? bari-web/scripts/shot-charts-zoom.mjs
?? bari-web/scripts/shot-cookies-page.mjs
?? bari-web/src/app/hashvaot/cookies-coffee/
?? bari-web/src/components/comparisons/cookies-coffee-comparison-page.tsx
?? bari-web/src/components/comparisons/cookies-coffee-prologue-visualizations.tsx
?? bari-web/src/components/hashvaot/featured-cookies-coffee-intelligence-card.tsx
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/yogurts_frontend_v4_gates_report.md
?? bari-web/src/data/seo/
?? bari-web/src/lib/comparisons/cookies-coffee-page-data.ts
?? bari-web/src/lib/seo/
?? err.txt
?? err2.txt
?? err3.txt
?? git
?? out.txt
?? out2.txt
?? out3.txt
?? reports/
?? "research/Algorithmic Foundations of Consumer Food Scoring Engines.pdf"
?? tasks/DISPATCH_BOARD.md
?? tasks/HANDOVER.md
?? tasks/TASK-233F.md
?? tasks/TASK-235.md
?? tasks/TASK-236.md
?? tasks/TASK-246.md
?? tasks/TASK-250.md
?? tasks/TASK-251.md
?? tasks/TASK-252.md
?? tasks/TASK-253.md
?? tasks/TASK-254.md
?? tasks/TASK-255.md
?? tasks/TASK-256.md
?? tasks/TASK-257.md
?? tasks/TASK-258.md
?? tasks/TASK-259.md
?? tasks/TASK-260.md
?? tasks/TASK-261.md
?? tasks/TASK-262.md
?? tasks/TASK-263.md
?? tasks/TASK-264.md
?? tasks/TASK-265.md
?? tasks/TASK-266.md
?? tasks/TASK-269.md
?? tasks/TASK-270.md
?? tasks/TASK-274.md
?? tasks/TASK-275.md
?? tasks/TASK-276.md
?? tasks/TASK-277.md
?? tasks/TASK-278.md
?? tasks/TASK-279.md
?? tasks/TASK-281.md
?? tasks/TASK-282.md
?? tasks/_build.log
?? tasks/_dev.log
?? tasks/_p56_patch_score_engine.py
?? tasks/archive/
?? tasks/closed/TASK-218.md
?? tasks/closed/TASK-221.md
?? tasks/closed/TASK-242.md
?? tasks/closed/TASK-243.md
?? tasks/closed/TASK-244.md
?? tasks/closed/TASK-245.md
?? tasks/closed/TASK-245A.md
?? tasks/closed/TASK-245B.md
?? tasks/closed/TASK-247.md
?? tasks/closed/TASK-248.md
?? tasks/closed/TASK-249.md
?? tasks/closed/TASK-267.md
?? tasks/closed/TASK-271.md
?? tasks/closed/TASK-277.md
?? tasks/closed/TASK-279.md
?? tasks/closed/TASK-280.md
?? tasks/new_task.py
?? tasks/prompts/
?? tasks/returns/
?? tasks/scripts/
?? tmp/
```

### Delta

### New / modified since dispatch
  ?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_003_corrected_pilot/
