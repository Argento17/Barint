# Return: P177

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P177_counterfactual_minimize_fix.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-18T05:09:46.799052+00:00 |
| Finished | 2026-06-18T05:11:11.797168+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P177 task prompt and the return contract so I can execute the task exactly as specified.
I'll inspect sample outputs and engine thresholds, and search for continuous-lever cases that hit extreme values.
The bug is searching for the lowest target (extreme) instead of the highest value that still crosses the grade boundary — I'll implement binary search for that and update double-lever handling.
## P177 Return — Counterfactual continuous-lever minimization fix

Fixed the central defect in `method_counterfactual.py`: continuous levers (sugars_g, sodium_mg) now use **binary search for the largest value closest to current** that crosses the next grade boundary, instead of searching down to the floor (0.0). Binary/cliff levers unchanged — `ingredient_count` cliff confirmed at **12** via `constants.py` `PROCESSING_PENALTIES` (`LONG_INGREDIENT_LIST`, `ingredients>12`, 4pt penalty).

### What changed
- Added `_solve_minimal_continuous()` — threshold-solve between floor and current
- Single-lever path uses solver for all continuous levers; sodium no longer hardcoded to 599 mg
- Double-lever path fixes cliff/binary levers at their discrete targets, then solves continuous partner minimally (no more `sugars_g → 0.0` defaults)
- Each achievable lever now carries a `note` showing simulated score and grade flip at the boundary

### New distribution (53 live traces)
| Metric | P174 (before) | P177 (after) |
|---|---|---|
| Products processed | 53 | 53 |
| Achievable | 13 | **17** |
| Single-lever | 3 | **8** |
| Two-lever | 10 | **9** |
| Achievable:false | 40 | **36** |
| Partial continuous targets | 0 | **19** |

**Score distribution** (current_score, 53 traces): min=12.4, max=65.0, median=37.2, stdev=14.55, most_common=50.0 (6 products).

**Acceptance example** — barcode `5900020015174`: sugars_g 24.8 → **6.5** (not 0.0); note: `sugars_g=6.5 → simulated score 35.0 (D), crosses E→D boundary at 35`.

**Scope guard**: `git diff` empty on `score_engine.py`, `constants.py`, configs, live page JSON.

### Files touched
1. `03_operations/bsip2/proto_v0/src/method_counterfactual.py` — continuous minimization fix
2. `03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.json` — regenerated
3. `03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.md` — regenerated

### Verify at
- `method_counterfactual.py:159-210` — `_solve_minimal_continuous` + single-lever solver loop
- `method_counterfactual.py:291-370` — double-lever minimal continuous partner
- `constants.py:116` — ingredient_count cliff = 12
- `sample.json:171-177` — partial sugars_g target with grade-flip note
- `sample.md:5-9` — reconciled counts (8 single + 9 double = 17 achievable)

```json
{
  "task": "P177",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip2/proto_v0/src/method_counterfactual.py", "action": "modified", "sha256": "EBE6F3FA0DC96E84DF468AFB2BD87C219EC56090C6CD47F711BA64E2C91D6530"},
    {"path": "03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.json", "action": "modified", "sha256": "52705FCAC0E8504439CC213FD4C356DADE3C166EA70FDB54799CBCC1809499A2"},
    {"path": "03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.md", "action": "modified", "sha256": "DBC92BB1501F5110ED039AF0B9A480A14F24D69927B0FACAEBA6078BDE351FFB"}
  ],
  "counts": {
    "products_processed": "53/53 (bsip2_trace.json in proto_v0/outputs/products)",
    "achievable": "17/53",
    "single_lever": "8/53",
    "two_lever": "9/53",
    "achievable_false": "36/53",
    "partial_continuous_targets": "19/53 (sugars_g or sodium_mg target > floor and < current)",
    "current_score_dist": "min=12.4 max=65.0 median=37.2 stdev=14.55 most_common=50.0(6) /53"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip2/proto_v0/src/method_counterfactual.py", "exit_code": 0},
    {"cmd": "git diff -- 03_operations/bsip2/proto_v0/src/score_engine.py 03_operations/bsip2/proto_v0/src/constants.py 03_operations/page_generator/configs/ 02_products/", "exit_code": 0},
    {"cmd": "python -c \"<counts derivation from sample.json>\"", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "(a) method exit 0 over 53 traces PASS; (b) barcode 5900020015174 sugars_g target=6.5 (partial, not 0.0) with note showing score 35.0/D crossing E→D boundary at 35 PASS; (c) scope-guard git diff empty on score_engine/constants/configs/live JSON PASS"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M .claude/agents/nutrition-agent.md
 M 01_framework/knowledge/nutrition_reference_kb_v1.md
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/page_generator/rescore_all.py
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-314.md
?? 03_operations/bsip2/proto_v0/reports/methods/
?? 03_operations/bsip2/proto_v0/src/method_additive_burden.py
?? 03_operations/bsip2/proto_v0/src/method_counterfactual.py
?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
?? 03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py
?? 03_operations/page_generator/_generated_milk.json
?? 03_operations/page_generator/_generated_milk_gates_report.md
?? 03_operations/page_generator/configs/cheese.json
?? 03_operations/page_generator/configs/milk.json
?? 03_operations/page_generator/configs/yogurts.json
?? tasks/TASK-321.md
?? tasks/TASK-321A.md
?? tasks/TASK-321B.md
?? tasks/TASK-321C.md
?? tasks/TASK-321D.md
?? tasks/TASK-321E.md
?? tasks/TASK-321F.md
?? tasks/TASK-321G.md
?? tasks/TASK-321H.md
?? tasks/TASK-321I.md
?? tasks/TASK-323.md
?? tasks/closed/TASK-322.md
?? tasks/closed/TASK-324.md
?? tasks/closed/TASK-325.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P177_counterfactual_minimize_fix.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/prompts/_done/P174_counterfactual_method.md
?? tasks/prompts/_done/P175_omega_lipid_extract_method.md
?? tasks/prompts/_done/P176_additive_burden_index_method.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
?? tasks/returns/P174_return.md
?? tasks/returns/P175_return.md
?? tasks/returns/P176_return.md
?? tasks/returns/P200_return.md
?? tasks/returns/P201_return.md
?? tasks/scripts/p163_build_output.txt
?? tasks/scripts/p163_overlay_merge.py
?? tasks/scripts/p163_run_output.txt
?? tasks/scripts/p171_build_exclusions.py
?? tasks/scripts/p171_cheese_scope.py
?? tasks/scripts/p171_cheese_verify.py
?? tasks/scripts/p171_cheese_verify2.py
?? tasks/scripts/p171_cheese_verify3.py
?? tasks/yogurt_copy_audit.txt
?? tasks/yogurt_list.txt
?? terminals/
?? tmp/yogurts_gen_test_final.json
?? yogurts.json
```

### After dispatch

```
M .claude/agents/nutrition-agent.md
 M 01_framework/knowledge/nutrition_reference_kb_v1.md
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/page_generator/rescore_all.py
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-314.md
?? 03_operations/bsip2/proto_v0/reports/methods/
?? 03_operations/bsip2/proto_v0/src/method_additive_burden.py
?? 03_operations/bsip2/proto_v0/src/method_counterfactual.py
?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
?? 03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py
?? 03_operations/page_generator/_generated_milk.json
?? 03_operations/page_generator/_generated_milk_gates_report.md
?? 03_operations/page_generator/configs/cheese.json
?? 03_operations/page_generator/configs/milk.json
?? 03_operations/page_generator/configs/yogurts.json
?? tasks/TASK-321.md
?? tasks/TASK-321A.md
?? tasks/TASK-321B.md
?? tasks/TASK-321C.md
?? tasks/TASK-321D.md
?? tasks/TASK-321E.md
?? tasks/TASK-321F.md
?? tasks/TASK-321G.md
?? tasks/TASK-321H.md
?? tasks/TASK-321I.md
?? tasks/TASK-323.md
?? tasks/closed/TASK-322.md
?? tasks/closed/TASK-324.md
?? tasks/closed/TASK-325.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P177_counterfactual_minimize_fix.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/prompts/_done/P174_counterfactual_method.md
?? tasks/prompts/_done/P175_omega_lipid_extract_method.md
?? tasks/prompts/_done/P176_additive_burden_index_method.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
?? tasks/returns/P174_return.md
?? tasks/returns/P175_return.md
?? tasks/returns/P176_return.md
?? tasks/returns/P200_return.md
?? tasks/returns/P201_return.md
?? tasks/scripts/p163_build_output.txt
?? tasks/scripts/p163_overlay_merge.py
?? tasks/scripts/p163_run_output.txt
?? tasks/scripts/p171_build_exclusions.py
?? tasks/scripts/p171_cheese_scope.py
?? tasks/scripts/p171_cheese_verify.py
?? tasks/scripts/p171_cheese_verify2.py
?? tasks/scripts/p171_cheese_verify3.py
?? tasks/yogurt_copy_audit.txt
?? tasks/yogurt_list.txt
?? terminals/
?? tmp/yogurts_gen_test_final.json
?? yogurts.json
```

### Delta

*(no changes detected)*
