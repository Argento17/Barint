# Return: P56

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P56_impl_sodium_protein.md` |
| Model | `cursor/agent-cli` |
| Started | 2026-06-13T12:23:12.469570+00:00 |
| Finished | 2026-06-13T12:28:06.420550+00:00 |
| Exit code | 0 |

---

## Output

```
## P56 Return — Shelf-relative sodium + dairy-protein reweight (flag-gated)

Implemented both default-OFF flags per `sodium_protein_design_v1.md`. Both gates pass with flags OFF; `run_brined_005` written with both flags ON.

### Files changed

| File | Action |
|------|--------|
| `03_operations/bsip2/proto_v0/src/constants.py` | Added `DAIRY_PROTEIN_WEIGHTS`, `SODIUM_SHELF_SURCHARGE_BANDS`, `SODIUM_FAMILY_BUDGET_BRINED=16`, `SODIUM_SHELF_STDEV_GUARD=150` |
| `03_operations/bsip2/proto_v0/src/score_engine.py` | Added `BARI_SODIUM_SHELF_RELATIVE_V1`, `BARI_DAIRY_PROTEIN_REWEIGHT_V1`, shelf-stats helpers, EV-056 surcharge, EV-057 reweight + HP suppression |
| `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` | Added EV-056, EV-057 |
| `03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_005.py` | Created — flags ON, emits `verification_table.csv` |
| `03_operations/bsip2/proto_v0/src/p56_byte_identity.py` | Created — gate 1 verifier |
| `02_products/brined_cheeses/bsip2_outputs/run_brined_005/` | Created — 48 traces + `run_record.json` + `verification_table.csv` |

**Default-OFF confirmed:** `BARI_SODIUM_SHELF_RELATIVE_V1=False`, `BARI_DAIRY_PROTEIN_REWEIGHT_V1=False` when env vars unset.

---

### Gate 1 — Default-OFF byte-identity

```
P56 GATE 1 — default-OFF byte-identity vs run_brined_004
Flags: BARI_SODIUM_SHELF_RELATIVE_V1=False BARI_DAIRY_PROTEIN_REWEIGHT_V1=False
Products checked: 48
PASS — all 48 scores byte-identical to run_brined_004
```

Baseline preserved: grade_dist **A:12 B:28 C:7 D:1** (unchanged from `run_brined_004`).

---

### Gate 2 — Invariant suite

```
OVERALL: ALL PASS
I1_BOUNDS PASS (342) | I2_DETERMINISM PASS (342) | I3_NULL_SAFETY PASS (11)
I4_OFF_FREE PASS (342) | I5_GRADE_CONSISTENCY PASS (113) | I6_MONOTONICITY PASS (342)
→ 6/6 PASS
```

---

### Gate 3 — Flag-ON brined re-grade (`run_brined_005`)

**Shelf sodium stats (corpus, 48 products with valid sodium panel):**
- `SHELF_SODIUM_MEDIAN_MG` = **1000.0**
- `SHELF_SODIUM_STDEV_MG` = **266.25** (above 150mg guard → surcharge active)

**Grade distribution (48/48 from `verification_table.csv`):**
- **A: 9 | B: 28 | C: 9 | D: 2**
- Score range: min **46.0**, max **85.4**, median **72.9**, stdev **9.36**
- Most common scores: **75.0 (5)**, **72.9 (2)**, **73.6 (2)**

**Acceptance pin — barcode 7290102397334 (bulgarit 5%, 1550mg):**
- `run_brined_004`: **88.2 / A**
- `run_brined_005`: **83.6 / A** (−4.6 pts; within design target ~80–83)

Full verification table at `02_products/brined_cheeses/bsip2_outputs/run_brined_005/verification_table.csv` (48 rows, schema: `barcode,score,grade,binding_caps,nova,fat,sodium,context_flag`).

---

### Implementation notes

- **EV-056:** Surcharge adds to `SODIUM_LOAD_GENERAL_GRAD`; combined penalty capped at `SODIUM_FAMILY_BUDGET_BRINED=16`. Requires `BARI_GRAD_SODIUM_V1=on` + `BARI_SODIUM_SHELF_RELATIVE_V1=on`.
- **EV-057:** `DAIRY_PROTEIN_WEIGHTS` sum = 1.00; HP_FAT_SODIUM suppressed for clean `dairy_protein` (sodium ≤400mg, zero additive markers).

**Proposed status: RETURNED** — orchestrator to verify artifacts and close.

```json
{
  "task": "P56",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip2/proto_v0/src/constants.py", "action": "modified", "sha256": "7a1a9643b6a61f5176c5a0105128060e84d27cd280473d0f13c8a34311a9ae1f"},
    {"path": "03_operations/bsip2/proto_v0/src/score_engine.py", "action": "modified", "sha256": "2ba0c5b5cd67a8a3e455e12238a83e6a505485f8b07c5de15fb98a1c47dda8d5"},
    {"path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md", "action": "modified", "sha256": "af5ea867ac73e7d4c07628e0bd4b37e475cd4a8473314d08c24c79490b53fdf8"},
    {"path": "03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_005.py", "action": "created", "sha256": "39799c85b029ad51ff61c9a270d49a8684d20798b6bc51ed12ee20684f37a554"},
    {"path": "03_operations/bsip2/proto_v0/src/p56_byte_identity.py", "action": "created", "sha256": "608557479f3c3c408ec9238922505f15683185d5b1f9b187c2d74a9d589d4e98"},
    {"path": "02_products/brined_cheeses/bsip2_outputs/run_brined_005/run_record.json", "action": "created", "sha256": "486d8e1ca9cbcaac8e30d688162b2e2e7eb872a1aa0926c7050721d1be755377"},
    {"path": "02_products/brined_cheeses/bsip2_outputs/run_brined_005/verification_table.csv", "action": "created", "sha256": "da93f8b8233818081f6ef3aa79c966b46515860a8c8afedc86347185b929ce4f"}
  ],
  "counts": {
    "byte_identity_pass": "48/48 (p56_byte_identity.py vs run_brined_004 traces)",
    "invariants_pass": "6/6 (engine_invariants.py, 342 cases)",
    "run_brined_005_scored": "48/48 (verification_table.csv)",
    "grade_dist_run005": "A:9/B:28/C:9/D:2 (verification_table.csv)",
    "bulgarit_7290102397334_delta": "88.2/A→83.6/A (verification_table.csv vs run_brined_004 trace)",
    "flags_default_off": "2/2 (score_engine module load with unset env)"
  },
  "commands_run": [
    {"cmd": "cd C:/Bari/03_operations/bsip2/proto_v0/src && python p56_byte_identity.py", "exit_code": 0},
    {"cmd": "cd C:/Bari/03_operations/bsip2/proto_v0/src && python ../../../shadow/engine_invariants.py", "exit_code": 0},
    {"cmd": "cd C:/Bari/03_operations/bsip2/proto_v0/src && python batch_run_brined_cheeses_005.py", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Gate 1: 48/48 byte-identical to run_brined_004 with both P56 flags OFF. Gate 3: bulgarit 7290102397334 dropped 88.2/A→83.6/A; SHELF_SODIUM_MEDIAN_MG=1000.0; grade_dist A:9 B:28 C:9 D:2."
}
```
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
 M 01_framework/operations/comp/source_registry_v1.yaml
 M 01_framework/operations/orchestration_model_v1.md
 M 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_recal_p0_trim/run_record.json
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/bsip2/proto_v0/src/evaluation_scope.py
 M 03_operations/bsip2/proto_v0/src/router_v2.py
 M 03_operations/bsip2/proto_v0/src/score_engine.py
 M 99_archive/command_center_retired_2026-06-13/cc-agent_AGENT_DEFINITION.md
 M 99_archive/command_center_retired_2026-06-13/command_center.json
 M 99_archive/command_center_retired_2026-06-13/command_center_archive.json
 M 99_archive/command_center_retired_2026-06-13/command_center_live.json
 M CLAUDE.md
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/granola_frontend_v1.json
 D tasks/TASK-218.md
 D tasks/TASK-221.md
 D tasks/TASK-244.md
 D tasks/TASK-249.md
 M tasks/closed/TASK-226.md
?? .github/
?? 01_framework/bsip2_framework/docs/scoring/additive_cocktail_cluster_proposal_v1.md
?? 01_framework/governance/grade_boundary_policy_v1.json
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
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_008_reconstruction/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_multiretailer_001_reconstruction/
?? 02_products/breakfast_cereals/cereals_copy_remediation_draft_v1.json
?? 02_products/breakfast_cereals/cereals_copy_remediation_draft_v2.json
?? 02_products/breakfast_cereals/cereals_qa_report_v1.md
?? 02_products/brined_cheeses/
?? 02_products/frozen_vegetables/.usda_generic_cache_v1.json
?? 02_products/frozen_vegetables/_build_copy_v2.py
?? 02_products/frozen_vegetables/build_benefit_lookup.py
?? 02_products/frozen_vegetables/frozen_vegetables_benefit_lookup_v1.json
?? 02_products/frozen_vegetables/frozen_vegetables_copy_v2_draft.json
?? 02_products/frozen_vegetables/frozen_vegetables_shell_copy_v2.json
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase1_spec_v1.md
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase2_seed_v1.json
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase3_copyinput_v1.json
?? 02_products/yogurt_system/bsip0/yogurt_bsip0_log_20260611T072535.txt
?? 02_products/yogurt_system/bsip0/yogurt_bsip0_raw_20260611T072535.json
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_005/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_006/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg/
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
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_005.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_006.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_006_shipcfg.py
?? 03_operations/bsip2/proto_v0/src/shadow_backtest.py
?? 03_operations/bsip2/proto_v0/src/task238_off_remediation.py
?? 03_operations/bsip2/proto_v0/tests/
?? 03_operations/claim_entailment/
?? 03_operations/off_sweep/
?? 03_operations/page_generator/
?? 03_operations/router/
?? 03_operations/runs/
?? 03_operations/shadow/
?? 03_operations/spine/
?? 99_archive/bread_retail_001_OFF_superseded_TASK238/
?? AGENTS.md
?? Bari-task243/
?? "C\357\200\272Bari02_productsyogurt_systemreportsrt_a_grades_tmp.json"
?? "C\357\200\272Bari02_productsyogurt_systemreportsrt_anomalies_tmp.json"
?? bari-web/src/app/hashvaot/brined-cheeses/
?? bari-web/src/components/comparisons/brined-cheeses-comparison-page.tsx
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v1.json
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/yogurts_frontend_v4_gates_report.md
?? bari-web/src/lib/comparisons/brined-cheeses-page-data.ts
?? err.txt
?? err2.txt
?? err3.txt
?? git
?? out.txt
?? out2.txt
?? out3.txt
?? reports/
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
?? tasks/TASK-268.md
?? tasks/TASK-269.md
?? tasks/TASK-270.md
?? tasks/_build.log
?? tasks/_dev.log
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
?? tasks/new_task.py
?? tasks/prompts/
?? tasks/returns/
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
 M 01_framework/operations/comp/source_registry_v1.yaml
 M 01_framework/operations/orchestration_model_v1.md
 M 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_recal_p0_trim/run_record.json
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/bsip2/proto_v0/src/constants.py
 M 03_operations/bsip2/proto_v0/src/evaluation_scope.py
 M 03_operations/bsip2/proto_v0/src/router_v2.py
 M 03_operations/bsip2/proto_v0/src/score_engine.py
 M 99_archive/command_center_retired_2026-06-13/cc-agent_AGENT_DEFINITION.md
 M 99_archive/command_center_retired_2026-06-13/command_center.json
 M 99_archive/command_center_retired_2026-06-13/command_center_archive.json
 M 99_archive/command_center_retired_2026-06-13/command_center_live.json
 M CLAUDE.md
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/granola_frontend_v1.json
 D tasks/TASK-218.md
 D tasks/TASK-221.md
 D tasks/TASK-244.md
 D tasks/TASK-249.md
 M tasks/closed/TASK-226.md
?? .github/
?? 01_framework/bsip2_framework/docs/scoring/additive_cocktail_cluster_proposal_v1.md
?? 01_framework/governance/grade_boundary_policy_v1.json
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
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_008_reconstruction/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_multiretailer_001_reconstruction/
?? 02_products/breakfast_cereals/cereals_copy_remediation_draft_v1.json
?? 02_products/breakfast_cereals/cereals_copy_remediation_draft_v2.json
?? 02_products/breakfast_cereals/cereals_qa_report_v1.md
?? 02_products/brined_cheeses/
?? 02_products/frozen_vegetables/.usda_generic_cache_v1.json
?? 02_products/frozen_vegetables/_build_copy_v2.py
?? 02_products/frozen_vegetables/build_benefit_lookup.py
?? 02_products/frozen_vegetables/frozen_vegetables_benefit_lookup_v1.json
?? 02_products/frozen_vegetables/frozen_vegetables_copy_v2_draft.json
?? 02_products/frozen_vegetables/frozen_vegetables_shell_copy_v2.json
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase1_spec_v1.md
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase2_seed_v1.json
?? 02_products/frozen_vegetables/frozen_vegetables_v2_phase3_copyinput_v1.json
?? 02_products/yogurt_system/bsip0/yogurt_bsip0_log_20260611T072535.txt
?? 02_products/yogurt_system/bsip0/yogurt_bsip0_raw_20260611T072535.json
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_005/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_006/
?? 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg/
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
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_005.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_006.py
?? 03_operations/bsip2/proto_v0/src/batch_run_yogurt_006_shipcfg.py
?? 03_operations/bsip2/proto_v0/src/p56_byte_identity.py
?? 03_operations/bsip2/proto_v0/src/shadow_backtest.py
?? 03_operations/bsip2/proto_v0/src/task238_off_remediation.py
?? 03_operations/bsip2/proto_v0/tests/
?? 03_operations/claim_entailment/
?? 03_operations/off_sweep/
?? 03_operations/page_generator/
?? 03_operations/router/
?? 03_operations/runs/
?? 03_operations/shadow/
?? 03_operations/spine/
?? 99_archive/bread_retail_001_OFF_superseded_TASK238/
?? AGENTS.md
?? Bari-task243/
?? "C\357\200\272Bari02_productsyogurt_systemreportsrt_a_grades_tmp.json"
?? "C\357\200\272Bari02_productsyogurt_systemreportsrt_anomalies_tmp.json"
?? bari-web/src/app/hashvaot/brined-cheeses/
?? bari-web/src/components/comparisons/brined-cheeses-comparison-page.tsx
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v1.json
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/yogurts_frontend_v4_gates_report.md
?? bari-web/src/lib/comparisons/brined-cheeses-page-data.ts
?? err.txt
?? err2.txt
?? err3.txt
?? git
?? out.txt
?? out2.txt
?? out3.txt
?? reports/
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
?? tasks/TASK-268.md
?? tasks/TASK-269.md
?? tasks/TASK-270.md
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
?? tasks/new_task.py
?? tasks/prompts/
?? tasks/returns/
```

### Delta

### New / modified since dispatch
   M 03_operations/bsip2/proto_v0/src/constants.py
  ?? 03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_005.py
  ?? 03_operations/bsip2/proto_v0/src/p56_byte_identity.py
  ?? tasks/_p56_patch_score_engine.py
