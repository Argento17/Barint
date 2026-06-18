# Return: P203

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P203_yohananof_parser_salvage.md` |
| Model | `cursor/agent-cli` |
| Started | 2026-06-18T08:46:17.964675+00:00 |
| Finished | 2026-06-18T08:48:39.688825+00:00 |
| Exit code | 0 |

---

## Output

```
## P203 complete — Yohananof parser salvaged

Branch **`sweep/yohananof-parser-salvage`** is pushed from `origin/master` (commit `2ff786fb`).

### What was ported
From salvage commit `376319982` onto master's Shufersal dual-table parser (additive only):

- **`_find_yohananof_basis`** — verbatim basis read; real page caption is `ל100 גרם` (no hyphen)
- **`_parse_yohananof_nutrition`** — unknown basis → `insufficient=True, rows=[]`; >1 numeric token rejects panel
- **`_sniff_unit`** — mg detection across bare `מג`, gershayim `מ״ג`, ASCII `מ"ג` (shared with Victory)
- Victory parser + **`extract_nutrition_raw_auto`** dispatch (required for 31-test suite)
- Real fixtures: `yohananof_16000423534.html`, `victory_7290005610509.html`

### `git diff --numstat origin/master`
```
355	0	03_operations/bsip0/scrape/_shared/bsip0_nutrition.py
1	0	03_operations/bsip0/scrape/_shared/fixtures/victory_7290005610509.html
1	0	03_operations/bsip0/scrape/_shared/fixtures/yohananof_16000423534.html
186	0	03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py
```

### Full test-runner stdout
```
PASS  test_classify_basis_tokens
PASS  test_clean_panel_no_integrity_key
PASS  test_dual_table_per_cube_never_wins
PASS  test_dual_table_selects_per_100g_not_per_cube
PASS  test_dual_table_values_match_per_100g_fixture
PASS  test_extract_nutrition_raw_auto_dispatches_by_retailer
PASS  test_extract_nutrition_raw_carries_selection
PASS  test_fat_subtypes_keep_their_own_fields
PASS  test_fixture_exists_and_carries_the_bug_signature
PASS  test_fixture_panels_flagged_by_guard
PASS  test_full_panel_reads_total_not_subrow
PASS  test_label_is_nutrient_name_not_unit
PASS  test_multi_table_no_per_100g_is_insufficient
PASS  test_parse_num_byte_identical_to_legacy
PASS  test_parse_value_bound_less_than
PASS  test_sat_gt_total_flagged
PASS  test_single_table_still_parses
PASS  test_sniff_unit_matches_all_mg_quote_forms
PASS  test_subrow_final_mem_does_not_overwrite_total_fat
PASS  test_sugar_of_which_is_still_captured
PASS  test_target_product_bound_is_recoverable
PASS  test_total_fat_row_still_classifies_as_fat
PASS  test_victory_ambiguous_header_insufficient
PASS  test_victory_basis_per_100g_from_header
PASS  test_victory_multi_td_row_insufficient
PASS  test_victory_th_td_rows_parse
PASS  test_yohananof_ambiguous_row_is_insufficient
PASS  test_yohananof_header_read_verbatim_not_synthesized
PASS  test_yohananof_li_rows_parse_from_real_fixture
PASS  test_yohananof_sodium_mg_preserved_end_to_end
PASS  test_yohananof_unknown_basis_is_insufficient

31 passed, 0 failed
```

### OFF check
`grep -rn "off\.get_product\|open_food_facts" 03_operations/bsip0/scrape/_shared/bsip0_nutrition.py` → **no matches**

### Push confirmation
```
To https://github.com/Argento17/Barint.git
 * [new branch]          sweep/yohananof-parser-salvage -> sweep/yohananof-parser-salvage
branch 'sweep/yohananof-parser-salvage' set up to track 'origin/sweep/yohananof-parser-salvage'.
```

```json
{
  "task": "P203",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip0/scrape/_shared/bsip0_nutrition.py", "action": "modified", "sha256": "513cc747286eb62df2776cb5872e509817f71967a5880a5dc4deb6095a8ddc83"},
    {"path": "03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py", "action": "modified", "sha256": "b180f0b8cdbd1d7a48237d315693ef51c35b520ad7266639cdbf4e5c0abe051a"},
    {"path": "03_operations/bsip0/scrape/_shared/fixtures/yohananof_16000423534.html", "action": "created", "sha256": "967cee46bbdbc0bf11b6fe607e5529768286040f010049e6f8f778b4ca14de93"},
    {"path": "03_operations/bsip0/scrape/_shared/fixtures/victory_7290005610509.html", "action": "created", "sha256": "6d651be144a5da02b0e0ad49c5021563a613cb396dc9c6fee71a5863be154b36"}
  ],
  "counts": {
    "tests_passed": "31/31 (test_bsip0_nutrition.py bare runner)",
    "off_references_in_parser": "0/1 files checked"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py", "exit_code": 0},
    {"cmd": "git push -u origin sweep/yohananof-parser-salvage", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "31/31 tests pass; Yohananof header verbatim 'ל100 גרם'; OFF grep clean"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M .claude/agents/nutrition-agent.md
 M .claude/commands/orchestrate.md
 M 01_framework/knowledge/nutrition_reference_kb_v1.md
 M 01_framework/operations/bari_router_v4_2.md
 M 01_framework/operations/lane_routing_rules_v1.md
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/router/dispatch.py
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-314.md
?? 03_operations/bsip2/proto_v0/reports/methods/
?? 03_operations/bsip2/proto_v0/src/method_additive_burden.py
?? 03_operations/bsip2/proto_v0/src/method_counterfactual.py
?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
?? 03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py
?? 03_operations/page_generator/_generated_milk.json
?? 03_operations/page_generator/_generated_milk_gates_report.md
?? 03_operations/page_generator/configs/author_set.json
?? "C\357\200\272UsersHPAppDataLocalTempsalty_bsip0_nutrition.py"
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
?? tasks/closed/TASK-322.md
?? tasks/closed/TASK-323.md
?? tasks/closed/TASK-324.md
?? tasks/closed/TASK-325.md
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/prompts/P202_c3_topology_consult.md
?? tasks/prompts/P203_yohananof_parser_salvage.md
?? tasks/prompts/P204_image_backfill_salvage.md
?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
?? tasks/prompts/_done/P174_counterfactual_method.md
?? tasks/prompts/_done/P175_omega_lipid_extract_method.md
?? tasks/prompts/_done/P176_additive_burden_index_method.md
?? tasks/prompts/_done/P177_counterfactual_minimize_fix.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
?? tasks/returns/P173_return.md
?? tasks/returns/P174_return.md
?? tasks/returns/P175_return.md
?? tasks/returns/P176_return.md
?? tasks/returns/P177_return.md
?? tasks/returns/P200_return.md
?? tasks/returns/P201_return.md
?? tasks/returns/P202_return.md
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
(clean)
```

### Delta

### Removed / cleaned since dispatch
   M .claude/commands/orchestrate.md
   M 01_framework/knowledge/nutrition_reference_kb_v1.md
   M 01_framework/operations/bari_router_v4_2.md
   M 01_framework/operations/lane_routing_rules_v1.md
   M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
   M 03_operations/router/dispatch.py
   M tasks/DISPATCH_BOARD.md
   M tasks/TASK-314.md
  ?? "C\357\200\272UsersHPAppDataLocalTempsalty_bsip0_nutrition.py"
  ?? 03_operations/bsip2/proto_v0/reports/methods/
  ?? 03_operations/bsip2/proto_v0/src/method_additive_burden.py
  ?? 03_operations/bsip2/proto_v0/src/method_counterfactual.py
  ?? 03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py
  ?? 03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py
  ?? 03_operations/page_generator/_generated_milk.json
  ?? 03_operations/page_generator/_generated_milk_gates_report.md
  ?? 03_operations/page_generator/configs/author_set.json
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
  ?? tasks/closed/TASK-322.md
  ?? tasks/closed/TASK-323.md
  ?? tasks/closed/TASK-324.md
  ?? tasks/closed/TASK-325.md
  ?? tasks/generate_yogurt_copy.py
  ?? tasks/prompts/P171_cheese_conformance_config.md
  ?? tasks/prompts/P172_yogurt_conformance_config.md
  ?? tasks/prompts/P200_milk_spine_config.md
  ?? tasks/prompts/P201_cheese_branch_rehab.md
  ?? tasks/prompts/P202_c3_topology_consult.md
  ?? tasks/prompts/P203_yohananof_parser_salvage.md
  ?? tasks/prompts/P204_image_backfill_salvage.md
  ?? tasks/prompts/_done/P173_hp_carb_sodium_method.md
  ?? tasks/prompts/_done/P174_counterfactual_method.md
  ?? tasks/prompts/_done/P175_omega_lipid_extract_method.md
  ?? tasks/prompts/_done/P176_additive_burden_index_method.md
  ?? tasks/prompts/_done/P177_counterfactual_minimize_fix.md
  ?? tasks/returns/P169_return.md
  ?? tasks/returns/P171_return.md
  ?? tasks/returns/P172_return.md
  ?? tasks/returns/P173_return.md
  ?? tasks/returns/P174_return.md
  ?? tasks/returns/P175_return.md
  ?? tasks/returns/P176_return.md
  ?? tasks/returns/P177_return.md
  ?? tasks/returns/P200_return.md
  ?? tasks/returns/P201_return.md
  ?? tasks/returns/P202_return.md
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
  M .claude/agents/nutrition-agent.md
