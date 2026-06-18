# Return: P109

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P109_c1cursor_cereals_clean_pilot.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-14T12:05:21.721315+00:00 |
| Finished | 2026-06-14T12:12:06.427998+00:00 |
| Exit code | 0 |

---

## Output

```
**RETURNED** (TASK-278 Phase-5 cereals corrected pilot / P109)

**Summary of execution (exact per prompt body after first --- separator):**
- Step 1: Scanned `02_products/breakfast_cereals/bsip2_outputs/run_cereals_001_shelfrel_pilot/products/*/bsip2_trace.json` (45 traces); extracted `category`. Produced exact lists (34 cereal-routed barcodes, 11 `snack_bar_granola` barcodes). Granola excluded from gate per spec.
- Step 2: Created `03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py` (dual flag-on/off via score_engine module patch on `BARI_SHELF_RELATIVE_V1` after single import + shared shelf_stats; common flags exactly as specified; loads from `03_operations/bsip1/run_cereals_001/output/`; writes 45 flag-on traces + run_record + artifacts to `02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot/`; clean `delta = flag_on_score - flag_off_score`; cereal-only filtering + gate logic; no subprocess helper needed as patch is simpler/explicit and matches prior yogurt pattern; documented approach in code + logs).
- Executed the pilot (produced outputs).
- Step 3: Computed clean deltas for all 45 (cereal n=34); reported revised interim 11-criteria gate (cereal-only basis). Key numbers: movers=26, grade_changes=6, absorption=0.0 (0/26), granola bleed=0, anti-immunity=0, floor=0 violations, inversion-B gap 4.0→5.0 (widened_by=1.0, <5.5), resolution restored (pinned 3→2), flag-off vs synth_001 drift=25 (cereal), brined pre-verified.
- Step 4: Edited brined batch runner (added explicit `BARI_SHELF_RELATIVE_V1=on`); snapshot pre scores; re-ran `batch_run_brined_cheeses_005.py`; post-compare: 48/48 score/grade identical (no bleed). (Pre/post snapshots + compare in tmp/ for audit.)
- Step 5: Ran `python 03_operations/shadow/engine_invariants.py` → overall PASS (I1_BOUNDS/I2_DETERMINISM/I6_MONOTONICITY at 342 cases each; off_introduced=0; I4_OFF_FREE PASS).
- All DoD items complete (34/11 lists, script+run+45 traces+record, clean delta+gate on cereal, inversion-B clean, crit11 drift doc, brined byte-id pass+evidence, invariants 342 PASS, OFF=0, no engine source edits).
- Hard rules: OFF ban absolute (traces/records/invariants I4 + code audits clean; no OFF data source, import, or substitution ever; "unknown acceptable; OFF is not"); no changes to `constants.py`/`score_engine.py`; measured not published; frozen invariants untouched.

**Files changed (to verify at file:line):**
- Created: `03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py` (full dual harness + cereal lists hardcoded post-Step1 + gate calc + run_record + p109_gate_values.json writer + console summary; verify dual patch at ~line 140s, CEREAL_BARCODES list ~line 60, gate_results ~line 290s, off_used=False asserts).
- Edited: `03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_005.py:54` (added `os.environ["BARI_SHELF_RELATIVE_V1"] = "on"` with P109 comment in flag block before imports; verify no other changes).
- Produced (deliverables): `02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot/run_record.json` (verify inversion_b + gate_results + self_check + off_used + 45 traces written during on-pass), `.../products/` (exactly 45 `bsip1_*/bsip2_trace.json`; spot-check e.g. 7290100000042 has SUGAR_SHELF_REL_V1 term + score 74.5), `.../verification_table_clean.csv`, `.../p109_gate_values.json` (compact extract of return numbers; updated post-invariants to "342 PASS").
- Created: `tasks/returns/P109_return.md` (exact json per prompt return-format + summary of changes + verification notes; propose RETURNED; see full content).
- (No other files; tmp/ snapshots for brined/synth/compare were transient audit aids.)

**Return json (exact as written to tasks/returns/P109_return.md; also embedded in run outputs):**
```json
{
  "task_id": "TASK-278",
  "phase": "Phase-5 cereals corrected pilot",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "data-agent",
  "cereal_barcodes_n": 34,
  "granola_barcodes_n": 11,
  "pilot_run_dir": "02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot",
  "clean_delta_method": "flag_on_score - flag_off_score (same engine, same run)",
  "inversion_b": {
    "7290100000042": {"flag_off": 73.5, "flag_on": 74.5, "delta": 1.0},
    "5054568100022": {"flag_off": 69.5, "flag_on": 69.5, "delta": 0.0},
    "gap_flag_off": 4.0,
    "gap_flag_on": 5.0,
    "gap_widened_by": 1.0,
    "criterion_pass": false
  },
  "cereal_movers_clean": 26,
  "cereal_grade_changes_clean": 6,
  "absorption_cereal_clean": 0.0,
  "anti_immunity_pass": true,
  "floor_compliance_pass": true,
  "flag_off_vs_synthesis_001_mismatches": 25,
  "granola_delta_non_zero": 0,
  "brined_byte_id": {"pass": true, "mismatches": 0},
  "engine_invariants": "342 PASS",
  "off_used": false,
  "gate_results": [
    {"criterion": 1, "name": "resolution_restored", "pass": true, "evidence": "on_max_pinned=2, off_max_pinned=3 (fewer identical in on = restored resolution)"},
    {"criterion": 2, "name": "inversion_a", "pass": null, "evidence": "n/a — D6 corpus correction (7290100000029 routes to snack_bar_granola); P110 provides revised gate"},
    {"criterion": 3, "name": "inversion_b_gap", "pass": false, "evidence": "gap_flag_off=4.0, gap_flag_on=5.0, widened_by=1.0 (need >=5.5)"},
    {"criterion": 4, "name": "min_movers_cereal", "pass": true, "evidence": "n_cereal_movers=26 (need >=15)"},
    {"criterion": 5, "name": "min_grade_changes_cereal", "pass": true, "evidence": "n_cereal_grade_changes=6 (need >=1)"},
    {"criterion": 6, "name": "max_absorption_cereal", "pass": true, "evidence": "absorbed_zero_net_cereal=0/fired=26 rate=0.0 (need <=0.40)"},
    {"criterion": 7, "name": "anti_immunity", "pass": true, "evidence": "high_sugar (>=25g) cereal at B(>=70) flag-on: 0 (need=0)"},
    {"criterion": 8, "name": "floor_compliance", "pass": true, "evidence": "7 cereal sugar>=25g checked, 0 >62 violations (need=0); floor=62"},
    {"criterion": 9, "name": "no_granola_bleed", "pass": true, "evidence": "granola products with non-zero delta: 0 (need=0)"},
    {"criterion": 10, "name": "brined_byte_id", "pass": true, "evidence": "48/48 scores byte-identical (pre vs post re-run of brined_005 with BARI_SHELF_RELATIVE_V1=on explicit)"},
    {"criterion": 11, "name": "flag_off_drift_check", "pass": false, "evidence": "25 cereal mismatches vs synthesis_001 (need=0)"}
  ],
  "not_done": []
}
```

**What to verify (orchestrator):**
- `tasks/returns/P109_return.md:163` (the json block + file list).
- Script creation + no engine edits + cereal lists + dual patch + outputs at `03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py:1` (header), ~60 (lists), ~140 (patch), and run dir.
- Brined edit + 0-mismatch: `03_operations/bsip2/proto_v0/src/batch_run_brined_cheeses_005.py:54` + tmp compare logs + run_record in brined dir.
- Invariants: `03_operations/shadow/engine_invariants.py` run output (342 cases, overall PASS, I4=0).
- Traces/records: spot `.../run_cereals_002_clean_pilot/products/bsip1_7290100000042/bsip2_trace.json` (SR term + 74.5) + run_record.json + p109_gate_values.json + OFF=0 in all.
- OFF ban: full audit (no data source in code/outputs; invariants confirm).
- Gate numbers match run logs + p109_gate_values.json (cereal-only, clean delta).

All prompt rules + constraints followed exactly. No more work. (Propose RETURNED; orchestrator verifies/closes per registry protocol.)
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
  ?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_002_clean_pilot/
  ?? 03_operations/bsip2/proto_v0/src/batch_run_cereals_002_clean_pilot.py
  ?? tmp/
