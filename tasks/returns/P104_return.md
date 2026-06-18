# P104 Return — TASK-280 Phase-2: PHVO D7 Product Co-Sign
**Agent:** product-agent  
**Date:** 2026-06-14  
**Task:** TASK-280 Phase-2  
**Status:** RETURNED  

---

## D7 Ratification Summary

All four D6 rulings RATIFIED with one precision note and one condition.

**Q1 (מחמאה REMOVE): RATIFIED.** מחמאה is animal fat, not PHVO. The chemical distinction is settled. The double-penalty with sat_fat dimension is a structural error. The Fix-B code comment misidentifying it as "margarine/shortening" must be corrected.

**Q2 (ceiling=40 + N≤8 gate): RATIFIED with precision note.** The BSIP2 `ingredient_order` uses 1-indexed positions (`item["position"]` starts at 1). Implementation must use `item["position"] <= 8`, not `<= 7`. The D6 ruling framed it as "0-indexed positions 0–7" but the codebase convention is 1-indexed. Gate covers the same 8 ingredients. Data Agent must verify against the snacks corpus before the first re-score.

**Q3 (all-categories): RATIFIED.** Q1 removal eliminates the primary false-positive path. No category exclusion list.

**Q4 (patch principle): RATIFIED.** Grade-change only. Within-grade score movement ships on next scheduled re-score.

## snk-019 Ruling: Option A

Fire as-is. "מרגרינה" label = industrial-processing signal regardless of the specific fat source. Option B (sub-exclusion for coconut/palm-declared margarines) adds audit complexity without proportional benefit. Data Agent notes the finding in the run log; does not override.

Reversal condition: >10% of snacks corpus has coconut/palm-declared margarines causing material score distortion.

## EV-086 Registration

**Spec conflict found and resolved:** P104 brief specified writing EV-086 to `C:\Bari\01_framework\operations\evidence_registry_v1.md` — that path does not exist. The correct registry for BSIP2 scoring engine entries (EV-NNN prefix, where EV-050 lives) is `C:\Bari\03_operations\bsip2\evidence_registry\bsip2_evidence_registry_v1.md`. The framework governance registry at `01_framework\governance\evidence_registry_v1.md` uses BEV-NNN prefix and BEV-086 is already occupied. EV-086 was written to the correct path (line 2064, BSIP2 registry). No EV-086 duplicate exists.

## Implementation Spec Confirmed

signal_extractor.py: four changes authorized (remove מחמאה, fix line 1167 comment, fix line 1158 comment, replace full-text `has_phvo` with position-aware detection using `ingredient_order` with 1-indexed `item["position"] <= 8` and full-text fallback).

score_engine.py: no changes. Ceiling logic is correct; position gate lives in signal_extractor.py.

No-regression gates: engine_invariants.py PASS 342, brined byte-identical to run_brined_004, milk byte-identical to run_005_headpin.

## What Was Not Done

- No engine source files modified (per spec)
- No comparison JSON files modified (per spec)
- No snacks re-score authorized (orchestrator decision after Phase-3 implementation)
- No patch of deployed JSON (orchestrator decision after corrected engine + grade-impact check)

---

## Return Contract

```json
{
  "task_id": "TASK-280",
  "phase": "Phase-2 D7 co-sign",
  "status": "RETURNED",
  "return_date": "2026-06-14",
  "agent": "product-agent",
  "d7_ratification": {
    "Q1_mchama": "RATIFIED",
    "Q2_ceiling_and_gate": "RATIFIED",
    "Q3_category_scope": "RATIFIED",
    "Q4_patch_principle": "RATIFIED"
  },
  "snk_019_ruling": "option_A",
  "ev_086_registered": true,
  "ev_086_line": 2064,
  "ev_086_path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
  "ev_086_path_correction": "Brief specified non-existent path (01_framework/operations/evidence_registry_v1.md); written to correct BSIP2 registry path where EV-050 and all engine EVs live",
  "d7_doc_path": "01_framework/bsip2_framework/phvo_governance/phvo_d7_cosign_v1.md",
  "implementation_spec_confirmed": true,
  "implementation_precision_note": "ingredient_order is 1-indexed in BSIP2 codebase; position gate must use item['position'] <= 8 (not <= 7); D6 ruling used 0-indexed framing but effect is identical",
  "artifacts": [
    {
      "path": "03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md",
      "type": "ev_registry_entry",
      "line": 2064,
      "description": "EV-086 appended"
    },
    {
      "path": "01_framework/bsip2_framework/phvo_governance/phvo_d7_cosign_v1.md",
      "type": "d7_cosign_document",
      "description": "D7 co-sign with ratification, implementation spec, decision log"
    },
    {
      "path": "tasks/returns/P104_return.md",
      "type": "return_contract",
      "description": "This file"
    }
  ],
  "counts": {
    "questions_ratified": 4,
    "questions_total": 4,
    "questions_overridden": 0,
    "snk019_options_considered": 2,
    "snk019_option_chosen": 1,
    "ev_entries_written": 1,
    "ev_duplicates_found": 0,
    "spec_conflicts_found": 1,
    "spec_conflicts_resolved": 1,
    "signal_extractor_changes_authorized": 4,
    "score_engine_changes_authorized": 0,
    "files_modified": 1,
    "files_created": 2
  },
  "commands_run": [
    {"cmd": "grep -n EV-086 bsip2_evidence_registry_v1.md", "exit": 0, "result": "line 2064 — no prior EV-086 found before append"},
    {"cmd": "grep -n 'has_phvo' signal_extractor.py", "exit": 0, "result": "line 1170 full-text assignment; line 1228 l3 emit"},
    {"cmd": "grep -n 'has_phvo' score_engine.py", "exit": 0, "result": "line 1409 Fix-C read; line 1984 EV-050 gate read"}
  ],
  "not_done": [
    "Phase-3 implementation dispatch (P105 to Data Agent) — orchestrator step",
    "snacks corpus position analysis — Data Agent task pre-re-score",
    "snk-019 grade impact determination — requires corrected engine run",
    "Snacks re-score authorization — orchestrator decision after no-regression proof",
    "Deployed JSON patch decision — orchestrator decision after grade-impact check"
  ],
  "acceptance_test": "Four D6 rulings ratified with explicit RATIFIED statements. EV-086 written to correct BSIP2 registry path (spec-conflict flagged and resolved). Implementation spec confirmed with precision note on 1-indexed positions. snk-019 ruled Option A with reversal condition. D7 co-sign document written with decision log. No engine or JSON files modified."
}
```
