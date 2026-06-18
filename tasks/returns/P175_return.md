# Return: P175

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P175_omega_lipid_extract_method.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-18T04:55:09.044770+00:00 |
| Finished | 2026-06-18T04:59:11.339460+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P175 task prompt and the return contract so I can execute the task exactly as specified.
Next I'll read the P173 template, TASK-324, and the page_generator configs to mirror the pattern.
I'll search the codebase for omega/lipid fields and inspect sample BSIP0/BSIP1 records to understand the data shape.
Building the extraction module and coverage runner, mirroring the P173 pattern.
Fixing overly greedy panel-text regex that was swallowing the omega-6 match.
## P175 Return — Omega lipid extraction method + label-coverage dataset

Built a standalone measurement-only extractor for omega-3/omega-6 and specific-lipid declarations from in-house BSIP0/BSIP1 label data. No scoring path was touched.

### Deliverables

1. **`03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py`**
   - `evaluate_omega_lipid_extract(bsip1, bsip0=None)` returns `{omega3_mg_100g, omega6_mg_100g, omega6_3_ratio|null, specific_lipids, qualitative_oil_signals, declared, source_field}`
   - Sources (priority): BSIP0 `nutrition_raw_source.rows` → BSIP1 `normalized_nutrition_per_100g` (OFF-skipped) → panel bleed text (`ערכים תזונתיים`, `_data_remediation.before_*`)
   - EV-011: absent quantitative omega → `declared:false` (not zero, not `insufficient_data`)
   - Qualitative call-outs (claims, oil ingredients) recorded separately; never converted to mg
   - OFF-ban: skips normalized nutrition when `provenance.panel_source == open_food_facts`, `_off_data_used`, or `off_candidate_panel`
   - CLI: `--coverage` (full corpus), `--single` + optional `--bsip0-json`

2. **Coverage dataset** under `03_operations/bsip2/proto_v0/reports/methods/omega_lipid/`:
   - `coverage.json` — 979 products across 12 live shelves
   - `coverage.md` — per-shelf coverage rates with named denominators

### Coverage results (979 BSIP1 products, 12 shelves)

| Metric | Count |
|--------|------:|
| Products evaluated | 979 |
| Declaring omega-3 (quantitative) | 0 |
| Declaring omega-6 (quantitative) | 0 |
| Declaring either | 0 |
| Ratio computable (both ω6 and ω3) | 0 |
| Qualitative oil-signal mentions (non-quantitative) | 186 |

**Finding:** No product in the live corpora declares quantitative omega-3 or omega-6 on its nutrition panel. Coverage is effectively 0% — consistent with EV-011’s “present-when-declared” pattern and the known Israeli label gap for fatty-acid breakdown. The method is ready for when declarations appear; inline tests confirm extraction from BSIP0 rows and panel bleed text.

### Verify at file:line

| File | What to check |
|------|---------------|
| `method_omega_lipid_extract.py:27-28` | Inert `OMEGA_LIPID_METHOD_VERSION` constant |
| `method_omega_lipid_extract.py:68-78` | OFF-ban guard `_is_off_sourced()` |
| `method_omega_lipid_extract.py:310-365` | `evaluate_omega_lipid_extract()` + EV-011 `declared:false` contract |
| `method_omega_lipid_extract.py:430-520` | Coverage runner over page_generator configs |
| `coverage.json` | 979 products; counts reconcile 0+0+0 declared |
| `coverage.md:8-34` | Summary + per-shelf table matches JSON |
| `score_engine.py`, `constants.py`, configs | `git diff` empty |

```json
{
  "task": "P175",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py", "action": "created", "sha256": "678A91875B2681C2FFCE751B9C2E28B3543E117D19055571E2CF1CAE53155AAB"},
    {"path": "03_operations/bsip2/proto_v0/reports/methods/omega_lipid/coverage.json", "action": "created", "sha256": "B488093FF782E42290037ED5F7BE9F59A1D23953CF53219FA9C9DC644411F513"},
    {"path": "03_operations/bsip2/proto_v0/reports/methods/omega_lipid/coverage.md", "action": "created", "sha256": "296BC6919B34645497FB313543FA98CE484A361A578E01144D5A8D0C2493363C"}
  ],
  "counts": {
    "products_evaluated": "979/979 (BSIP1 corpora via page_generator configs)",
    "declaring_omega3": "0/979 (coverage.json)",
    "declaring_omega6": "0/979 (coverage.json)",
    "declaring_either": "0/979 (coverage.json)",
    "ratio_computable": "0/979 (coverage.json)",
    "qualitative_oil_signals": "186/979 (coverage.json products with non-empty qualitative_oil_signals)",
    "either_per_shelf_brined_cheeses": "0/48",
    "either_per_shelf_cakes": "0/167",
    "either_per_shelf_cereals": "0/63",
    "either_per_shelf_cheese": "0/59",
    "either_per_shelf_cookies_coffee": "0/209",
    "either_per_shelf_granola": "0/103",
    "either_per_shelf_hard_cheeses": "0/67",
    "either_per_shelf_hummus_shelfrel_002": "0/69",
    "either_per_shelf_juices": "0/32",
    "either_per_shelf_milk": "0/20",
    "either_per_shelf_snacks": "0/53",
    "either_per_shelf_yogurts": "0/89"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py --coverage", "exit_code": 0},
    {"cmd": "python -c \"import json; from pathlib import Path; d=json.loads(Path('03_operations/bsip2/proto_v0/reports/methods/omega_lipid/coverage.json').read_text()); prods=d['products']; print(len(prods), sum(1 for x in prods if x['declared']), sum(1 for x in prods if x['qualitative_oil_signals']))\"", "exit_code": 0},
    {"cmd": "python -c \"import sys; sys.path.insert(0, '03_operations/bsip2/proto_v0/src'); from method_omega_lipid_extract import evaluate_omega_lipid_extract; ... unit tests quantitative/qualitative/panel_bleed/OFF-ban ...\"", "exit_code": 0},
    {"cmd": "git diff -- 03_operations/bsip2/proto_v0/src/score_engine.py 03_operations/bsip2/proto_v0/src/constants.py 03_operations/page_generator/configs/", "exit_code": 0},
    {"cmd": "git diff --name-only -- bari-web/src/data/comparisons/", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Acceptance (a) coverage run exit 0 over 12 live BSIP1 shelves; (b) coverage.json + coverage.md exist, counts reconcile 0/979 declared across all shelves; (c) git diff empty for score_engine.py, constants.py, configs, and live page JSON; inline unit tests pass for quantitative BSIP0 rows, qualitative-only claims, panel bleed, and OFF-ban — all PASS"
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
?? tasks/TASK-323.md
?? tasks/TASK-324.md
?? tasks/TASK-325.md
?? tasks/closed/TASK-322.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P175_omega_lipid_extract_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
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
?? tasks/TASK-324.md
?? tasks/TASK-325.md
?? tasks/closed/TASK-322.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P175_omega_lipid_extract_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
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

### New / modified since dispatch
  ?? 03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py
  ?? tasks/returns/P201_return.md
