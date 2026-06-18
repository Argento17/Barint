# Return: P176

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P176_additive_burden_index_method.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-18T05:00:39.315929+00:00 |
| Finished | 2026-06-18T05:03:47.669543+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P176 task prompt and the return contract so I can execute the task exactly as specified.
Reading the template module and related files to understand the trace structure and implementation pattern.
Implementing the additive burden method module and running it across live shelf traces.
Deduplication was too aggressive across shelves; I'll scope it per shelf so each shelf keeps its own products.
## P176 Return — Additive burden aggregate index method

Built a standalone representation-only method that rolls existing EV-002/003/019 additive signals from BSIP2 traces into a single displayable burden index. No scoring path was touched.

### Deliverables

1. **`03_operations/bsip2/proto_v0/src/method_additive_burden.py`**
   - `evaluate_additive_burden(trace)` reads L3 trace fields: `tax_named_concern_additives` (EV-002), `sprint1_high_risk_emulsifier_found` / `sprint1_neutral_emulsifier_found` (EV-003), `sprint1_prebiotic_gum_found` (EV-019)
   - Returns `{at_risk_count, high_risk_emulsifiers, neutral_emulsifiers, prebiotic_exempt, additive_burden_index, burden_band, components}` or `index:null` with reason
   - Inert weights: at-risk ×3, high-risk emulsifier ×2, neutral ×0, prebiotic exempt ×−1
   - Bands: NONE ≤0, LOW ≤2.99, MED ≤5.99, HIGH >5.99
   - OFF-ban: traces referencing OFF/`off_candidate_panel` → `index:null`
   - CLI: `--calibrate` (all shelves), `--single` (one trace)

2. **Reports** under `03_operations/bsip2/proto_v0/reports/methods/additive_burden/`:
   - `index.json` — 935 per-shelf products with full index payloads
   - `index.md` — burden-band distribution, index histogram (min/max/median/stdev/most-common), per-shelf table, highest-burden products

### Results (935 products, 12 live shelves via `run_products_dir`)

| Metric | Count |
|--------|------:|
| Products processed | 935 |
| Index computed | 898 |
| Index null (OFF-ban) | 37 |
| With at-risk additives (EV-002) | 320 |

**Burden bands:** NONE 574 · LOW 4 · MED 280 · HIGH 40

**Index distribution:** min −1.0 · max 13.0 · median 0.0 · stdev 2.3391 · most_common 0.0 (571 products)

Highest burden: cakes/cookies_coffee products at index 13.0 (3 at-risk + 2 high-risk emulsifiers).

### Verify at file:line

| File | What to check |
|------|---------------|
| `method_additive_burden.py:28-45` | Inert `ADDITIVE_BURDEN_*` weights and band thresholds |
| `method_additive_burden.py:68-175` | `evaluate_additive_burden()` — trace-only rollup, no re-derivation |
| `method_additive_burden.py:177-280` | Calibration runner over page_generator configs |
| `index.json:24-55` | Counts reconcile with product array |
| `index.md:51-66` | Per-shelf burden-band table with named denominators |
| `index.md:68-80` | Highest-burden (HIGH band) products |
| `score_engine.py`, `constants.py`, configs, live page JSON | `git diff` empty |

```json
{
  "task": "P176",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip2/proto_v0/src/method_additive_burden.py", "action": "created", "sha256": "BA52BDFDBAAB743B63344855CE28948B45D7CF7DF74AF84AC516B7D94DCA963C"},
    {"path": "03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.json", "action": "created", "sha256": "95E105026F72780F9509A5DFA0E01A13552A773B995DF74E3BCEC8DDCE4B8EA4"},
    {"path": "03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.md", "action": "created", "sha256": "066840269EF58CBB312FC82AE1806016EC57D52B9ADA167B05288128D824493F"}
  ],
  "counts": {
    "products_processed": "935/935 (BSIP2 traces via page_generator configs run_products_dir; 952 trace files − 17 within-shelf dedup cookies_coffee)",
    "index_computed": "898/935 (index.json products where index != null)",
    "index_null": "37/935 (index.json; all OFF-ban: trace contains off_candidate_panel)",
    "products_with_at_risk_additives": "320/935 (index.json; at_risk_count > 0)",
    "burden_band_NONE": "574/898 (index.json burden_band_distribution)",
    "burden_band_LOW": "4/898 (index.json burden_band_distribution)",
    "burden_band_MED": "280/898 (index.json burden_band_distribution)",
    "burden_band_HIGH": "40/898 (index.json burden_band_distribution)",
    "additive_burden_index_min": "-1.0 (index.json additive_burden_index_distribution)",
    "additive_burden_index_max": "13.0 (index.json additive_burden_index_distribution)",
    "additive_burden_index_median": "0.0 (index.json additive_burden_index_distribution)",
    "additive_burden_index_stdev": "2.3391 (index.json additive_burden_index_distribution)",
    "additive_burden_index_most_common": "0.0(571) (index.json additive_burden_index_distribution.most_common_value)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip2/proto_v0/src/method_additive_burden.py --calibrate", "exit_code": 0},
    {"cmd": "git diff -- 03_operations/bsip2/proto_v0/src/score_engine.py 03_operations/bsip2/proto_v0/src/constants.py 03_operations/page_generator/configs bari-web/src/data", "exit_code": 0},
    {"cmd": "python -c \"spot-check + count reconcile from index.json\"", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Acceptance (a–d): --calibrate exit 0 over 935 live traces; index.json + index.md exist and counts reconcile (935 processed, 37 null, band dist 574/4/280/40); git diff empty on score_engine.py/constants.py/configs/live page JSON; spot-check barcode 2472148 confirms index=13.0 = 3×3.0 + 2×2.0 faithful rollup of trace EV-002/003/019 fields (PASS)"
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
?? tasks/TASK-325.md
?? tasks/closed/TASK-322.md
?? tasks/closed/TASK-324.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P176_additive_burden_index_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/prompts/_done/P175_omega_lipid_extract_method.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
?? tasks/returns/P175_return.md
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
?? tasks/TASK-325.md
?? tasks/closed/TASK-322.md
?? tasks/closed/TASK-324.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P174_counterfactual_method.md
?? tasks/prompts/P176_additive_burden_index_method.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/prompts/_done/P175_omega_lipid_extract_method.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
?? tasks/returns/P175_return.md
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
  ?? 03_operations/bsip2/proto_v0/src/method_additive_burden.py
