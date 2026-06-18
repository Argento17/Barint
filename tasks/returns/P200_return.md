# Return: P200

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P200_milk_spine_config.md` |
| Model | `grok/build-cli` |
| Started | 2026-06-18T04:38:54.106737+00:00 |
| Finished | 2026-06-18T04:42:50.595264+00:00 |
| Exit code | 0 |

---

## Output

```
**Return block for P200 (executed per task body below `---` in tasks/prompts/P200_milk_spine_config.md exactly; all hard rules followed, including OFF ban + no data invention + no edits outside listed scope + no other configs/engine/frontend touched).**

- Command(s) run (verbatim):  
  `cd 03_operations/page_generator ; python generate_page.py --config configs/milk.json --out _generated_milk.json`  
  (generator executed its default self-gating; full stdout + _generated_milk_gates_report.md captured/ read post-run).

- Product count in output / scored (run universe) / exclusions: 0 / 20 / 20.

- Grade distribution (S/A/B/C/D/E counts): 0/0/0/0/0/0 (0 products in generated output JSON; _meta confirms product_count=0).

- Gate table:  
  G1 SCHEMA: PASS  
  G2 COVERAGE: FAIL  
  G3 SCOPE: PASS  
  G4 OFF: PASS (literal OFF count: 0 — "No OFF markers detected in frontend JSON or displayed corpus records")  
  G5 GRADE-INTEGRITY: PASS  
  G6 COPY-SAFETY: PASS  
  G8 DATA-SANITY: PASS  
  (G7 PARITY: SKIP — no baseline provided, as expected with baseline_json=null; not in required table per prompt).

- Top 3 products: barcode, score, grade: (none; 0 products in output).

- Any FAIL: G2 COVERAGE — "No products in frontend JSON". Offending barcodes (all 20 traces excluded at runtime with reason "no_corpus_record: barcode not found in any corpus_dir"; listed per missing-data-discard doctrine; no fabricated fixes applied):  
  5411188112709, 5411188124689, 5411188300328, 7290000051352, 7290014760141, 7290019790259, 7290102392094, 7290107932134, 7290110324773, 7290110324926, 7290110325619, 7290114313285, 7290114313865, 7290116936116, 7290119385560, 7394376619939, 7394376620904, 7394376621451, 8000215204219, 8000215204554.  
  (G4 OFF=0 confirmed; full hard-rule scan of traces + loaded corpus + generated JSON + generator logic = 0 OFF markers/contamination anywhere used. G3 SCOPE passed because _meta.exclusions documented all 20.)

- Files changed (path + 1-line what):  
  03_operations/page_generator/configs/milk.json — edited exactly per P200 task 1 bullets (baseline_json set to null; render_fields TODO string replaced by list `["novaGroup", "confidence_level", "d4_additives"]` mirroring cheese.json; scoring.flags left 100% untouched as MILK_CANONICAL_FLAGS with BARI_RECAL_P0=off; _status set to "READY — spine-runnable"; _comment trimmed to single line noting finalized for spine/P200/TASK-321 Wave 3).  
  (Run side-effects per task 2/3: 03_operations/page_generator/_generated_milk.json created; 03_operations/page_generator/_generated_milk_gates_report.md created. No other files touched anywhere.)

**Verification notes (per overall Bari rules + P200):** Only milk.json edited (config now matches required shape for spine); generator run + gate report read from 03_operations/page_generator/; G4 OFF=0 (hard rule green); no OFF source used/substituted for any field (unknown acceptable); no product/nutrition/ingredient data invented or fabricated; no engine/rescore_all.py/other-category/config touches; exclusions reported raw for orchestrator (no "fix" attempted); numbers/grades/gates taken verbatim from generator stdout + _generated_milk.json + _generated_milk_gates_report.md (trace-derived cross-check on 20 barcodes for dist only, not claimed in output); config _status/_comment updated; reference configs (yogurts.json, cheese.json) read only to mirror shape exactly. Run produced empty output due to pre-existing draft corpus_dirs mismatch (dummies in canonical_bsip1/run_001 vs. real 20 barcodes in run_milk_002/output); this is reported as-is per "if gate fails... list barcodes... do NOT fabricate".

```json
{
  "task": "P200",
  "proposed_status": "BLOCKED",
  "artifacts": [
    {"path": "03_operations/page_generator/configs/milk.json", "action": "modified", "sha256": "deff0bf1361dc58369bf74eaf86d44a55afedcaf48c9e0ed4bd65ad2a45ef964"},
    {"path": "03_operations/page_generator/_generated_milk.json", "action": "created", "sha256": "c01900d1a78e3fc4ada8fb6f7943b228f1ff35642fab031029dd42cc19355e18"},
    {"path": "03_operations/page_generator/_generated_milk_gates_report.md", "action": "created", "sha256": "9049ae5d28c772996f0e947f65e5a2a1309bf3bf691ea6a8fc5bb63c40ff5d5c"}
  ],
  "counts": {
    "products_in_output": "0 (generated page JSON from run)",
    "scored_run_universe": "20/20 (bsip2 traces in 02_products/milk_and_alternatives/intelligence_bsip2/run_006_shelfrel_refreeze/products)",
    "exclusions": "20/20 (all no_corpus_record per generator _meta)",
    "grade_dist_output": "S:0 A:0 B:0 C:0 D:0 E:0 (0 products in _generated_milk.json)",
    "g4_off_count": "0 (G4 OFF gate PASS + INFO: no markers in JSON/corpus/trace scan)",
    "gates_green": "6/7 (G1/G3/G4(0)/G5/G6/G8 PASS per gates_report.md; G2 FAIL; G7 SKIP as expected)"
  },
  "commands_run": [
    {"cmd": "python generate_page.py --config configs/milk.json --out _generated_milk.json", "exit_code": 1}
  ],
  "not_done": [
    "all gates green (G2 COVERAGE FAIL with 0 products; pre-existing draft corpus_dirs points to non-matching canonical_bsip1/run_001 (8 dummies) instead of data-containing 03_operations/bsip1/run_milk_002/output (contains all 20 barcodes) — no additional edits to milk.json beyond the 4 exact bullets, no exclusions added, no other changes per 'do exactly these' + 'do not touch other configs'"
  ],
  "self_check": "P200 tasks 1-3 executed exactly (reference configs read to mirror shape; milk.json deltas limited to listed bullets with scoring.flags untouched; run from page_generator dir with specified --out; gate report read verbatim); hard rules 100% followed (OFF=0 confirmed multiple ways, no data invented, no scope violations); return numbers + barcodes + gates taken directly from artifacts (generator stderr/stdout + _generated_milk.json + _generated_milk_gates_report.md); config sha + generated shas from Get-FileHash post-edit/run"
}
```

**RETURNED (or BLOCKED per above; see contract).** (All per P200 return-format + Bari return_contract_v1.md + Agents.md/Claude.md.)
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
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
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
?? tasks/generate_yogurt_copy.py
?? tasks/prompts/P171_cheese_conformance_config.md
?? tasks/prompts/P172_yogurt_conformance_config.md
?? tasks/prompts/P200_milk_spine_config.md
?? tasks/prompts/P201_cheese_branch_rehab.md
?? tasks/returns/P169_return.md
?? tasks/returns/P171_return.md
?? tasks/returns/P172_return.md
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
  ?? 03_operations/page_generator/_generated_milk.json
  ?? 03_operations/page_generator/_generated_milk_gates_report.md
