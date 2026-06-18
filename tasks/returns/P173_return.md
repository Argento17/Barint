# Return: P173

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P173_hp_carb_sodium_method.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-18T04:51:46.423262+00:00 |
| Finished | 2026-06-18T04:52:57.660084+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P173 task prompt and return contract first, then execute the task body below the separator.
No `---` separator in the prompt file — executing the full task body. Exploring existing HP methods, constants, and how rescore traces are structured.
Building the detection method module and calibration runner.
## P173 Return — HP carb+sodium detection method + calibration dataset

Built a standalone measurement-only detector for the third Fazzino hyper-palatability cluster (carbohydrates + sodium). No scoring path was touched.

### Deliverables

1. **`03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py`**
   - `evaluate_hp_carb_sodium()` on normalized per-100g nutrition
   - Returns `{fires: true|false|"insufficient_data", carb_pct_kcal, sodium_mg_100g, reason}`
   - Fazzino thresholds as inert `HP_CARB_SODIUM_*` module constants (not in `constants.py` / `score_engine.py`)
   - Carb % kcal = `(carbohydrates_g × 4 / energy_kcal) × 100`; Atwater fallback `(P×4 + C×4 + F×9)` when energy is missing
   - Missing carbs or sodium → `insufficient_data` (no OFF, no invented fills)
   - CLI: `--calibrate` (full corpus run), `--nutrition-json` (single-product test)

2. **Calibration dataset** under `03_operations/bsip2/proto_v0/reports/methods/hp_carb_sodium/`:
   - `calibration.json` — 979 products across 12 live shelves
   - `calibration.md` — summary + per-shelf fire rates + manual false-positive review table (EV-013 `risk_of_misuse` framing)

### Calibration results (979 BSIP1 products, 12 shelves)

| Outcome | Count |
|---------|------:|
| Fired (carb >40% kcal AND sodium ≥200 mg/100g) | 283 |
| Insufficient data | 89 |
| Did not fire | 607 |

**Fire rate by shelf:** cakes 88/167 (52.7%), cookies_coffee 113/209 (54.1%), granola 40/103 (38.8%), cereals 24/63 (38.1%), snacks 10/53 (18.9%), hummus 4/69 (5.8%), brined_cheeses 1/48 (2.1%), cheese 2/59 (3.4%), juices 1/32 (3.1%), hard_cheeses/milk/yogurts 0 fired (hard_cheeses has 40/67 insufficient_data from missing sodium).

**FP review highlights:** cookies/cakes/granola skew `likely_true_positive`; brined cheese and some cake/cheese items flagged `candidate_false_positive` per EV-013 endemic-food risk.

### Verify at file:line

| File | What to check |
|------|---------------|
| `method_hp_carb_sodium.py:27-28` | Inert `HP_CARB_SODIUM_*` thresholds (40% carb, 200 mg sodium) |
| `method_hp_carb_sodium.py:44-108` | Detection logic + Atwater fallback + `insufficient_data` guards |
| `method_hp_carb_sodium.py:175-220` | Calibration runner over page_generator configs |
| `calibration.json` | 979 products; counts reconcile (283 fired + 89 insufficient + 607 not fired) |
| `calibration.md:8-29` | Summary table matches JSON |
| `calibration.md:37+` | 283-row false-positive review table |
| `score_engine.py`, `constants.py` | `git diff` = empty (no scoring wiring) |

```json
{
  "task": "P173",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py", "action": "created", "sha256": "B4888DF5CF6853FB5E5E05E9D1AAFE2A384B447998D311CD9AA0CA954B6DFB6D"},
    {"path": "03_operations/bsip2/proto_v0/reports/methods/hp_carb_sodium/calibration.json", "action": "created", "sha256": "08461362E28D03789F6EA26DBBE627CA041200BD22BDCD0CC18CA4B2FC7FD39A"},
    {"path": "03_operations/bsip2/proto_v0/reports/methods/hp_carb_sodium/calibration.md", "action": "created", "sha256": "1EC9451C9FD1E4F0E0D65B62DB31B30B3BAC9A373122BEA6D5552AB1FF4BA507"}
  ],
  "counts": {
    "products_evaluated": "979/979 (BSIP1 corpora via page_generator configs)",
    "fired": "283/979 (calibration.json)",
    "insufficient_data": "89/979 (calibration.json)",
    "not_fired": "607/979 (calibration.json)",
    "fired_per_shelf_brined_cheeses": "1/48",
    "fired_per_shelf_cakes": "88/167",
    "fired_per_shelf_cereals": "24/63",
    "fired_per_shelf_cheese": "2/59",
    "fired_per_shelf_cookies_coffee": "113/209",
    "fired_per_shelf_granola": "40/103",
    "fired_per_shelf_hard_cheeses": "0/67",
    "fired_per_shelf_hummus_shelfrel_002": "4/69",
    "fired_per_shelf_juices": "1/32",
    "fired_per_shelf_milk": "0/20",
    "fired_per_shelf_snacks": "10/53",
    "fired_per_shelf_yogurts": "0/89"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py --calibrate", "exit_code": 0},
    {"cmd": "python -c \"import json; from pathlib import Path; d=json.loads(Path('03_operations/bsip2/proto_v0/reports/methods/hp_carb_sodium/calibration.json').read_text()); prods=d['products']; print(len(prods), sum(1 for x in prods if x['fires'] is True), sum(1 for x in prods if x['fires']=='insufficient_data'))\"", "exit_code": 0},
    {"cmd": "git diff -- 03_operations/bsip2/proto_v0/src/score_engine.py 03_operations/bsip2/proto_v0/src/constants.py", "exit_code": 0},
    {"cmd": "git diff --name-only -- bari-web/src/data/comparisons/", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Acceptance (a) calibration run exit 0 over 12 live BSIP1 shelves; (b) calibration.json + calibration.md exist, counts reconcile 283+89+607=979; (c) git diff empty for score_engine.py, constants.py, and live page JSON — all PASS"
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
?? tasks/TASK-322.md
?? tasks/TASK-323.md
?? tasks/TASK-324.md
?? tasks/TASK-325.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P173_hp_carb_sodium_method.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P200_return.md
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
?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
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
?? tasks/TASK-322.md
?? tasks/TASK-323.md
?? tasks/TASK-324.md
?? tasks/TASK-325.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P173_hp_carb_sodium_method.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P200_return.md
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

### New / modified since dispatch
  ?? 03_operations/bsip2/proto_v0/reports/methods/
  ?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
